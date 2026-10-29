"""単元パック：英語コミュニケーションⅡ・Ⅲ　図表・複数資料を含む英文の読解。

図表と本文の照合、複数の資料の比較、事実と意見の区別、情報の検索と統合を扱う。
記事・意見文・表はすべてこのパックのためのオリジナル英文・架空の資料である（人名・地名・数値も架空）。
"""
from banks._common import desc, mc, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ECOM-U02"


def cm(n):
    return f"{n:,}"


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["図表の単位・基準（何を分母にした割合か）・時期を確かめ、本文の記述と図表の数値を正確に照合できる。",
           "変化を「パーセント（増加率）」と「ポイント（割合の差）」で区別して読み、計算できる。",
           "複数の資料の書き手の立場を比べ、一致点と相違点を整理できる。",
           "事実と意見を区別し、相関を因果と取り違えずに、資料から言えることと言えないことを判断して自分の考えを英語で述べられる。"],
    duration=50,
    readiness=["論説文で主張と根拠を区別できる（HS-ECOM-U01）。",
               "割合（％）と増加率の計算ができる（中学数学・HS-MATH1-U05 データの分析）。",
               "比較級・倍数表現（twice as many as / more than）を読み書きできる（HS-ENG-U07）。"],
    flow=[("導入：「10%増えた」の落とし穴", 5, "20%が30%になったとき、何%増えたかを問い、ポイントと増加率の違いに気づかせる"),
          ("図表と本文の照合", 12, "単位・分母・時期の3点を確認する照合の手順を示す（例題1）"),
          ("事実と意見", 10, "確かめる方法の有無で区別し、報告された意見・推測・評価の語を整理する（例題2）"),
          ("複数資料の比較と統合", 15, "一致点・相違点の表を作り、資料から言えることと言えないこと（相関と因果）を判断する（例題3）"),
          ("まとめと確認", 8, "確認問題3問、問題プリントの課題指示")],
    sections=[
        intro("in1", "資料を「読み合わせる」力",
              "英語コミュニケーションⅡ・Ⅲや共通テストでは、記事と表、賛成と反対の意見文など、複数の資料を読み合わせて判断する問題が多い。1つ1つの英文が読めても、本文の数値が表のどの欄を指しているのか、2人の書き手がどこで一致しどこで対立しているのかを整理できなければ、正しく答えられない。この単元では、照合・区別・比較・統合の4つの手順を身につける。",
              bullets=["本文の数値を見たら、表の「どの行・どの列・どの年」かを必ず特定する。",
                       "割合の変化は「ポイント」と「パーセント」を区別する。",
                       "should / I think / clearly / probably などの語がある文は意見として読む。",
                       "表は「同時に変化している」ことを示すが、「原因である」ことまでは示さない。"],
              points=[tp("「通学に自転車を使う生徒が20%から30%になった」を板書し、「何%増えたか」を挙手で答えさせる。", ask="10%増えたと言ってよいか。",
                         expect="割合の差は10ポイント。増加率は10÷20×100＝50%。", timing="導入の冒頭"),
                      tp("この単元の資料はすべて架空のものであることを伝え、数値の真偽ではなく、資料からの推論の正しさを問う単元であることを示す。")]),
        definition("df1", "図表の読み方の基本",
                   "図表を読むときは、①何についての数値か（見出し・単位）、②何を全体（分母）とした割合か、③いつの数値か（時期・期間）の3点を、本文を読む前に確かめる。",
                   bullets=["単位：人・円・時間・％・ポイント・per day（1日あたり）・per visitor（1人あたり）。",
                            "割合の分母：全体の何%か、その集団の中の何%か（例：3時間以上使う生徒のうち70%）。",
                            "変化の表し方：増加数（差）＝新しい値−元の値。増加率＝差÷元の値×100（％）。",
                            "割合どうしの差はポイント（percentage points）で表す：20% → 30% は10ポイントの増加（増加率は50%）。",
                            "英語の表現：rose / increased by ～、fell / dropped by ～、doubled、more than doubled、half the level、twice as many as。"],
                   conditions=["増加率の分母は「元の値（比べるもとになる値）」である。新しい値で割らない。",
                               "グループの中の割合を、全体の中の割合と読み替えない。"],
                   points=[tp("同じ表から「人数の差」「増加率」「ポイントの差」の3つを計算させ、英語でどう言い分けるかを確認する。", caution="by 10 percent と by 10 percentage points の違いに気づかない生徒が多い。")]),
        theorem("th1", "事実と意見・資料から言えること",
                "事実＝記録・調査・観察で確かめられる内容（数値、出来事、「誰かが～と言った／予測した」という報告）　意見＝書き手の評価・判断・推測・提案（should / I think / clearly / probably / likely / worth / a waste / attractive）　資料から言えること＝表や本文に直接示された内容と、それから計算で導ける内容",
                ["「専門家は～と予測している」は、予測の内容は意見だが、予測したこと自体は事実の報告である。",
                 "数値を含んでいても、評価の語（hardly worth / only … which shows …）がつくと、文全体は意見になる。",
                 "2つの数値が同時に変化している（相関）ことから、一方が他方の原因である（因果）とは言えない。第3の要因を考える。"],
                body="複数の資料を比べるときは、各資料の文を「事実」と「意見」に分け、事実は数値で照合し、意見は書き手ごとに立場（賛成・反対・条件つき）を整理する。最後に、問いが求める判断に必要な情報を、複数の資料から集めて組み合わせる。",
                points=[tp("Nobody can deny that ～ のように断定的な言い方の意見を示し、「言い方が強い＝事実」ではないことを確認させる。",
                           ask="Nobody can deny that the festival has brought the community together. は事実か意見か。", expect="意見。「地域を一つにした」は評価で、確かめる方法がない。")]),
        derivation("dv1", "なぜ増加率は「元の値」で割るのか・なぜ相関は因果ではないのか",
                   ["① 増加率は「元の値を100としたとき、いくつ増えたか」を表す。だから分母は比べるもとになる元の値である。",
                    "② 例：来館者が11,000人から12,500人に増えた。差は1,500人。増加率は 1,500÷11,000×100 ≒ 14%。12,500で割ると約12%となり、基準が変わってしまう。",
                    "③ 割合どうしの比較：20%から30%への変化は、差が10ポイント。増加率は 10÷20×100＝50%。同じ変化でも「10ポイント増」と「50%増」は両方正しく、混同すると誤りになる。",
                    "④ 相関：画面を見る時間が長い生徒ほど睡眠時間が短い、という表は、2つの量が一緒に変化していることを示す。",
                    "⑤ しかし、宿題や部活動で遅くまで起きている生徒が、起きている間に携帯電話を使っているだけかもしれない（第3の要因）。この場合、携帯電話をやめても睡眠時間は延びない。",
                    "⑥ したがって、表から因果を主張するには、ほかの要因を調べる追加の調査や、条件をそろえた比較が必要になる。資料を読むときは「表から言えること」と「書き手の解釈」を分ける。"],
                   body="共通テストや論説文の資料問題では、選択肢が「表と一致しているか」に加えて、「表だけからそこまで言えるか」を問うものが多い。計算の基準と推論の範囲を確かめる習慣が、誤りの選択肢を見抜く力になる。",
                   points=[tp("同じ表について「言えること」「言えないこと」を2列に分けて書かせ、言えないことには「何のデータがあれば言えるか」を添えさせる。",
                              ask="この表から「携帯電話をやめれば睡眠が延びる」と言うには、どんなデータが必要か。", expect="宿題や部活動の時間など、ほかの要因をそろえて比べたデータ。", timing="手順⑥の説明時")]),
        example("ex1", "例題1　図表と本文の照合（ポイントと増加率）",
                "ある町の高校生の通学手段の割合は、2019年は bicycle 20%、bus 35% だったが、2024年は bicycle 30%、bus 25% になった（架空の資料）。次の英文のうち、正しいものをすべて選びなさい。\n(a) The share of students who cycle rose by 10 percentage points.\n(b) The share of students who cycle rose by 10 percent.\n(c) The share of bus users fell by about 29 percent.\n(d) In 2024, more students cycled than took the bus.",
                ["(a) 30−20＝10 なので10ポイントの増加。正しい。", "(b) 増加率は 10÷20×100＝50%。10 percent は誤り。",
                 "(c) バスは35%→25%で10ポイント減。減少率は 10÷35×100 ≒ 28.6% で約29%。正しい。", "(d) 2024年は bicycle 30% > bus 25%。正しい。"],
                "(a)(c)(d)",
                thinking="割合の差（ポイント）と、元の値に対する変化の割合（パーセント）を、分母を意識して区別する。",
                points=[tp("(b) を選んだ生徒に、「20人が30人になったら何%増えたか」と人数に置きかえて考えさせる。")],
                misconceptions=[("20%から30%になったので「10%増えた」と言える。", "差は10ポイント。増加率は元の20に対して50%"),
                                ("減少率は新しい値（25）で割る。", "元の値（35）で割る。10÷35×100 ≒ 29%")]),
        example("ex2", "例題2　事実と意見",
                "次の文を事実と意見に分け、意見の手がかりとなる語を答えなさい。\n(1) According to the survey, 42 percent of the respondents said they used the library at least once a week.\n(2) A 5 percent increase is hardly worth celebrating.\n(3) Several experts have predicted that the population will continue to decline.\n(4) It is likely that most students would welcome the change.",
                ["(1) 調査で回答者がそう答えたという結果の報告。調査の記録で確かめられるので事実。", "(2) 数値はあるが、hardly worth celebrating（祝うほどのことではない）は評価。意見。",
                 "(3) 予測の内容は意見だが、「専門家が予測した」こと自体は確かめられる。事実の報告。", "(4) It is likely（～の可能性が高い）は推測。意見。"],
                "事実：(1)(3)　意見：(2) hardly worth、(4) It is likely",
                thinking="「その文が正しいかどうかを、記録や調査で確かめる方法があるか」を問う。数値の有無や言い方の強さでは決めない。",
                points=[tp("(3) を意見と答えた生徒に、「専門家が予測したかどうか」と「人口が減るかどうか」の2つの問いに分けて考えさせる。", ask="「専門家が予測した」ことは、どうすれば確かめられるか。",
                           expect="専門家の発言や報告書を見れば確かめられる。")]),
        example("ex3", "例題3　2つの資料の比較と統合",
                "図書館の館長は「夜9時までの開館は明らかな成功だ。夜間に月2,500人が来館した」と書き、職員は「日中の来館者は11,000人から10,000人に減り、合計は1,500人しか増えていない」と書いた（架空の資料）。2人の一致点と相違点を整理し、夜間開館の評価について資料から言えることを日本語で述べなさい。",
                ["一致点：夜間開館が利用されている（夜間2,500人）。", "相違点：館長は成功と評価、職員は日中の減少と費用から判断を保留。",
                 "統合：合計の増加1,500人は夜間の2,500人より1,000人少ない → 日中から夜に移った人がいる可能性。",
                 "言えること：夜間開館は利用されているが、新たな来館者は最大でも1,500人程度で、「明らかな成功」とまでは資料から言えない。"],
                "夜間開館が利用されていることは両者とも認めているが、合計の増加は1,500人で夜間来館者より1,000人少なく、日中から移っただけの人もいると考えられるので、「明らかな成功」とまでは言えない。",
                thinking="2人の書き手の数値を1つの表にまとめ、差を計算してから評価の妥当性を判断する。",
                points=[tp("一致点・相違点を「論点 × 書き手」の表に整理させ、空欄になる欄（その書き手が触れていない論点）にも注意させる。", caution="一方の書き手の評価を、そのまま資料の結論として書く答案が多い。")]),
        board("bd1", "板書案",
              [("① 図表の照合", ["単位・分母・時期を確認", "増加数＝新−旧", "増加率＝差÷旧×100", "20%→30%：10ポイント増＝50%増", "グループ内の割合 ≠ 全体の割合"]),
               ("② 事実と意見", ["事実：確かめる方法がある", "報告（said / predicted）は事実", "意見：should / clearly / likely", "数値＋評価語 → 意見", "言い方の強さで決めない"]),
               ("③ 比較と統合", ["論点 × 書き手の表", "一致点・相違点", "相関 ≠ 因果（第3の要因）", "言えること／言えないこと", "数値を根拠に意見を書く"])],
              points=[tp("①の「10ポイント増＝50%増」は色を変えて強調し、問題プリントを解くときに必ず見返させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("表を見たら本文より先に、見出し・単位・脚注（架空の資料、調査対象、時期）に印をつけさせる。", ask="この表の70%は、誰の中での割合か。", expect="3時間以上画面を見る生徒の中での割合。"),
               tp("計算問題は、選択肢の誤りが「分母の取り違え」「ポイントと％の混同」「別の行・年の数値」の3種類で作られていることを示し、選ぶ前に式を書かせる。", caution="暗算で選ぶと、分母の取り違えに気づきにくい。"),
               tp("2人の書き手の比較では、両者が「同じ事実を認めたうえで評価が分かれている」場合が多いことを示し、一致点を先に探させる。", timing="例題3の前"),
               tp("「表から言えるか」を問う選択肢では、all / caused / proves / will などの語に印をつけ、資料の範囲を越えていないかを確かめさせる。"),
               tp("英語で意見を書く課題では、表の数値を1つ以上必ず引用させ、rose from A to B / fell by ～ percent などの表現をその場で確認する。")],
              misconceptions=[("20%から30%への変化を「10%の増加」と言う。", "差は10ポイント。増加率は50%"),
                              ("増加率・減少率を新しい値で割って求める。", "元の値（比べるもとになる値）で割る"),
                              ("数値を含む文はすべて事実である。", "評価の語がつけば意見。確かめる方法があるかで判断する"),
                              ("2つの数値が一緒に変化していれば、一方が他方の原因である。", "相関は因果を示さない。第3の要因を考える")]),
        summary("sm1", "まとめ",
                ["図表は単位・分母・時期を確かめてから本文と照合する。増加率は元の値を分母にし、割合の差はポイントで表す。",
                 "事実は確かめる方法がある内容（報告を含む）、意見は評価・判断・推測・提案。数値の有無や言い方の強さでは決めない。",
                 "複数の資料は「論点 × 書き手」の表で一致点と相違点を整理し、計算で統合して判断する。",
                 "相関から因果を主張しない。資料から言えることと言えないことを区別し、数値を根拠に意見を述べる。"]),
        check("ck1", "確認問題",
              [("ある数値が 800 から 600 に減った。減少率は何%か。", "25%（200÷800×100）"),
               ("40% から 50% への変化を、ポイントと増加率でそれぞれ答えなさい。", "10ポイントの増加、増加率は25%"),
               ("The new park is far more attractive than the old one. は事実か意見か。理由も答えなさい。", "意見。attractive（魅力的な）は評価の語で、確かめる方法がない。")]),
    ])


# ======================================================================
# 資料セット（記事＋表＋意見文。すべて架空）
# ======================================================================

SETS = [
    dict(key="SLEEP", title="Screen Time and Sleep",
         a_head="[Article] by Riko Sato, Northfield High School Newspaper", b_head="[Comment] by Mr. Ellis, biology teacher",
         a="Last month, the health committee at Northfield High School asked all 400 students how they use their phones at night. The survey asked how many hours students spent looking at screens after 9 p.m., how long they usually slept, and whether they often felt sleepy in class. The results are shown in the table.\nThe pattern is easy to see. Students who spent less than one hour on screens after 9 p.m. slept an average of 7.2 hours, while those who spent three hours or more slept only 5.6 hours. In addition, 70 percent of the students in the heaviest group said they often felt sleepy in class.\nThe committee believes that the school should start a \"Phones Off by 10\" campaign. \"If students put their phones away earlier, they will sleep longer and do better at school,\" said the committee leader.",
         b="The survey results are worth taking seriously, but we should be careful about what they actually prove. The table shows that students who use screens late also sleep less. It does not show that screens are the cause. Some students may stay up late because they have club activities, part-time jobs, or a lot of homework, and they may simply use their phones while they are already awake. A campaign might help, but I think we should first find out why students go to bed late. In my opinion, a second survey that asks about homework and other activities would give us a clearer picture.",
         tbl=table([["Less than 1 hour", "80", "7.2", "15"], ["1–2 hours", "150", "6.7", "32"], ["2–3 hours", "110", "6.1", "50"], ["3 hours or more", "60", "5.6", "70"]],
                   header=["Screen time after 9 p.m.", "Number of students", "Average sleep (hours)", "Often sleepy in class (%)"],
                   caption="Northfield High School 全生徒400人の調査結果（架空の資料）"),
         tqs=[("表によると、午後9時以降に画面を見る時間が3時間以上の生徒は、全生徒の何パーセントか。", "15%",
               [("60%", "60 は3時間以上の集団の人数で、割合ではない。60÷400×100 を計算する。"), ("70%", "70% は3時間以上の集団の中で「授業中によく眠くなる」と答えた生徒の割合である。"),
                ("25%", "60÷240 など、全生徒400人以外を分母にしている。")], ("60/400*100", "15")),
              ("記事の第2段落の 70 percent は、何を表しているか。", "画面時間が3時間以上の生徒のうち、授業中によく眠くなると答えた生徒の割合",
               [("全生徒のうち、授業中によく眠くなると答えた生徒の割合", "70% は3時間以上の集団の中の割合で、全生徒の中の割合ではない。"),
                ("全生徒のうち、画面時間が3時間以上の生徒の割合", "3時間以上の生徒は60人で、全体の15%である。"),
                ("画面時間が3時間以上の生徒のうち、睡眠時間が5.6時間未満の生徒の割合", "5.6 は平均睡眠時間で、70% とは別の列の数値である。")], None),
              ("表から、画面時間が最も短い集団と最も長い集団の平均睡眠時間の差は何時間か。", "1.6時間",
               [("1.1時間", "7.2−6.1 で、最も長い集団ではなく「2–3 hours」の集団と比べている。"), ("0.5時間", "隣り合う集団どうし（7.2−6.7）の差である。"),
                ("2.6時間", "引き算の誤り。7.2−5.6＝1.6 である。")], ("7.2-5.6", "1.6"))],
         agree=("Students who spend more time on screens late at night tend to sleep less.",
                [("Screens are the main cause of students' lack of sleep.", "Mr. Ellis は、表は画面が原因であることを示さないと述べている。"),
                 ("A second survey is not necessary.", "Mr. Ellis は2回目の調査を提案している。"),
                 ("The \"Phones Off by 10\" campaign will certainly work.", "Mr. Ellis は might help（役立つかもしれない）と述べるにとどめている。")]),
         contrast=("He accepts the survey results but doubts that they prove screens cause students to sleep less.",
                   [("He thinks the survey results are completely wrong.", "結果は真剣に受け止める価値があると述べている。"),
                    ("He supports the campaign and sees no need for further study.", "まず遅く寝る理由を調べるべきだと述べている。"),
                    ("He believes students should not be allowed to have phones.", "携帯電話の禁止は述べていない。")]),
         facts=["Students who spent less than one hour on screens after 9 p.m. slept an average of 7.2 hours.",
                "The survey asked how many hours students spent looking at screens after 9 p.m.",
                "The committee leader said that students would sleep longer if they put their phones away earlier."],
         opinions=[("The school should start a \"Phones Off by 10\" campaign.", "should（～すべきだ）による提案"),
                   ("The survey results are worth taking seriously.", "worth taking seriously（真剣に受け止める価値がある）という評価"),
                   ("A second survey would give us a clearer picture.", "In my opinion に続く、書き手の判断・予測")],
         support=[("students who use screens longer at night sleep less", "Average sleep falls from 7.2 hours in the lightest group to 5.6 hours in the heaviest group.",
                   [("There are 150 students in the 1–2 hours group.", "集団の人数で、睡眠時間との関係を示していない。"),
                    ("The survey included all 400 students.", "調査の対象を示すだけで、主張の根拠にならない。"),
                    ("15 percent of the lightest group often feel sleepy in class.", "眠気の割合の一部で、睡眠時間の比較になっていない。")]),
                  ("heavy screen users often feel sleepy in class", "70 percent of the heaviest group often feel sleepy, compared with 15 percent of the lightest group.",
                   [("The heaviest group sleeps an average of 5.6 hours.", "睡眠時間の数値で、授業中の眠気を直接示していない。"),
                    ("60 students use screens for three hours or more.", "人数で、眠気の割合を示していない。"),
                    ("The 1–2 hours group sleeps 6.7 hours on average.", "別の集団の睡眠時間で、主張と関係がない。")])],
         claim=("記事の委員会のリーダーは “If students put their phones away earlier, they will sleep longer” と述べている。この主張は表のデータだけから導けるか。Mr. Ellis の意見に触れ、表の数値を用いて日本語で説明しなさい。",
                "導けない。表からは、画面時間が長い集団ほど平均睡眠時間が短い（7.2時間から5.6時間）という関係はわかるが、画面が睡眠不足の原因だとまでは言えない。Mr. Ellis が指摘するように、部活動やアルバイト、宿題で遅くまで起きている生徒が、起きている間に携帯電話を使っているだけかもしれないからである。原因を確かめるには、宿題や活動の時間も尋ねる追加の調査が必要である。"),
         rec=("あなたが保健委員会の一員だとして、2つの資料を踏まえ、学校がとるべき次の一歩を英語で提案しなさい。",
              "I suggest that the school do a second survey before starting the campaign. Students with three or more hours of screen time sleep only 5.6 hours, but we need to know whether homework or club activities also keep them awake."),
         over=[("The survey proves that using a phone at night causes students to sleep less.",
                "表は画面時間と睡眠時間が一緒に変化する（相関）ことを示すだけで、原因と結果の関係は示していない。Mr. Ellis が指摘するように、宿題や部活動など別の要因の可能性がある。",
                "The survey shows that students who use screens longer at night tend to sleep less, but it does not prove that screens are the cause."),
               ("Most students at Northfield High often feel sleepy in class.",
                "70% は3時間以上の集団（60人）の中の割合で、全体ではない。各集団の人数と割合から計算すると、よく眠くなる生徒は 12＋48＋55＋42＝157人で、全体の約39%と半数に満たない。",
                "Fewer than half of all students (about 39 percent) often feel sleepy in class; the 70 percent figure applies only to the heaviest group.")]),
    dict(key="BOTL", title="Refill Stations at Hillside High",
         a_head="[Report] by the Hillside High School Student Council", b_head="[Comment] by Ms. Grant, school cafeteria manager",
         a="In April, the student council installed three water refill stations in the school building, hoping to reduce the number of plastic bottles thrown away at school. Before the stations were installed, the school's recycling bins collected about 2,400 bottles every month.\nAs the table shows, the number of bottles collected fell sharply in the first few months. By July, it had dropped to 1,200, half the level before the stations were installed. Our goal is to cut the number by 60 percent by the end of the year, and we are confident that we can reach it if more students bring their own bottles.\nWe also counted how often the stations were used. In July, the counters on the three stations recorded a total of 9,000 refills.",
         b="I am glad that fewer bottles are being thrown away. However, I would like to point out that the cafeteria also sold fewer bottled drinks in October, when many students were away on school trips. So part of the drop in October may not be due to the refill stations. Still, the stations are clearly popular, and I think the school should add one more station near the gym, where students line up for water after club practice.",
         tbl=table([["March (before)", "2,400", "—"], ["May", "1,800", "5,000"], ["July", "1,200", "9,000"], ["October", "1,100", "9,500"], ["December", "1,000", "10,000"]],
                   header=["Month", "Plastic bottles collected", "Refills recorded (3 stations)"],
                   caption="Hillside High School のペットボトル回収本数と給水回数（月ごと・架空の資料）"),
         tqs=[("表によると、3月から7月までに回収されたペットボトルの本数は何パーセント減ったか。", "50%",
               [("100%", "差の1,200本を7月の1,200本で割っており、分母が誤っている。元の値（3月の2,400本）で割る。"),
                ("約33%", "5月から7月（1,800本→1,200本）の減少率で、期間が違う。"),
                ("60%", "60% は生徒会の目標の数値で、7月までの実際の減少率ではない。")], ("(2400-1200)/2400*100", "50")),
              ("表の12月の数値は、生徒会の目標（年末までに60%減らす）を達成しているか。", "達成していない。目標は960本以下だが、12月は1,000本である。",
               [("達成している。3月から1,400本減り、60%以上減ったから。", "1,400÷2,400×100 ≒ 58% で、60%に届いていない。"),
                ("達成している。7月から12月まで減り続けたから。", "減り続けたことと、目標の削減率に達したことは別である。"),
                ("判断できない。表に12月の数値がないから。", "表には12月の数値（1,000本）がある。")], ("2400*(1-60/100)", "960")),
              ("記事の第3段落の 9,000 refills は、何を表しているか。", "7月に3台の給水機で記録された給水回数の合計",
               [("7月に給水機1台で記録された給水回数", "a total of（合計）とあり、3台の合計である。"),
                ("4月から7月までに記録された給水回数の合計", "In July（7月に）の数値で、期間の合計ではない。"),
                ("7月に回収されたペットボトルの本数", "回収本数は1,200本で、別の列の数値である。")], None)],
         agree=("Fewer plastic bottles are being thrown away than before.",
                [("The refill stations are the only reason for the drop.", "Ms. Grant は、10月の減少の一部は修学旅行の影響かもしれないと述べている。"),
                 ("The school does not need more refill stations.", "Ms. Grant は体育館の近くへの増設を提案している。"),
                 ("The student council has already reached its goal.", "どちらの書き手も目標を達成したとは述べていない。12月も目標の960本に届いていない。")]),
         contrast=("She welcomes the result but thinks that other factors may explain part of the decrease.",
                   [("She believes the refill stations have had no effect at all.", "給水機は明らかに人気があると述べている。"),
                    ("She wants the school to remove the refill stations.", "むしろ増設を提案している。"),
                    ("She thinks the cafeteria should sell more bottled drinks.", "販売を増やすべきだとは述べていない。")]),
         facts=["Before the stations were installed, the recycling bins collected about 2,400 bottles every month.",
                "In July, the counters on the three stations recorded a total of 9,000 refills.",
                "The cafeteria sold fewer bottled drinks in October."],
         opinions=[("We are confident that we can reach the goal if more students bring their own bottles.", "we are confident（自信がある）という書き手の見通し"),
                   ("The school should add one more station near the gym.", "should による提案"),
                   ("The stations are clearly popular.", "clearly popular（明らかに人気がある）という評価")],
         support=[("the refill stations have become popular", "Refills recorded rose from 5,000 in May to 10,000 in December.",
                   [("2,400 bottles were collected in March.", "給水機を設置する前の回収本数で、給水機の利用を示していない。"),
                    ("The council's goal is a 60 percent cut.", "目標の数値で、実際の利用状況ではない。"),
                    ("The cafeteria sold fewer bottled drinks in October.", "表にない情報で、減少の別の要因を示すものである。")]),
                  ("the number of bottles fell sharply in the first few months", "Bottles fell by 1,200 between March and July but by only 200 between July and December.",
                   [("Refills rose from 9,000 in July to 10,000 in December.", "給水回数の変化で、回収本数の減り方を示していない。"),
                    ("The stations recorded 5,000 refills in May.", "給水回数で、ボトルの減少を示していない。"),
                    ("1,000 bottles were collected in December.", "12月の数値だけで、最初の数か月の急な減少を示していない。")])],
         claim=("生徒会は “we are confident that we can reach it” と目標達成の見通しを述べている。表の数値と Ms. Grant の意見を踏まえて、この見通しが妥当かどうかを日本語で説明しなさい。",
                "楽観的すぎる可能性がある。表では3月の2,400本から7月の1,200本までは大きく減ったが、その後は10月1,100本、12月1,000本と減り方が小さくなり、12月でも目標の960本（60%減）に届いていない。さらに Ms. Grant によると、10月の減少の一部は修学旅行で生徒が少なかったためかもしれず、給水機だけの効果とは言えない。目標の達成には、体育館近くへの増設など追加の取り組みが必要だと考えられる。"),
         rec=("生徒会に向けて、2つの資料を踏まえた提案を英語で書きなさい。",
              "I suggest adding a refill station near the gym. The number of bottles fell from 2,400 to 1,000, but this is still above the goal of 960, and students who line up after club practice would use another station."),
         over=[("The refill stations reduced the number of bottles by 60 percent.",
                "3月から12月までの減少は1,400本で、2,400本の約58%であり、60%に届いていない。また、Ms. Grant が指摘するように、減少のすべてが給水機によるとは言えない。",
                "The number of bottles fell by about 58 percent between March and December, slightly short of the 60 percent goal."),
               ("Since the number of refills increased, each student used the stations more and more often.",
                "給水回数の合計が増えたことは、利用する生徒の数が増えた可能性もあり、一人ひとりの利用回数が増えたことを示さない。表には利用者数のデータがない。",
                "The total number of refills increased, but the table does not show whether more students used the stations or each student used them more often.")]),
    dict(key="RAIL", title="The Future of the Ridge Line",
         a_head="[Letter] by Ken Mori, a resident of Maple Valley", b_head="[Comment] by Ms. Hara, Maple Valley town planning office",
         a="The Ridge Line has connected our valley to the city for more than seventy years. Now the railway company says it may close the line because too few people use it. As the table shows, the average number of passengers per day has fallen from 1,200 in 2000 to 480 in 2020.\nHowever, numbers alone do not tell the whole story. Many of the remaining passengers are high school students and elderly people who cannot drive. For them, the train is not a convenience but a necessity. If the line closes, some families may leave the valley, and the population will fall even faster.\nI believe the town should help the railway company keep the line open, for example by paying part of its costs.",
         b="I understand how much the Ridge Line means to residents. However, the line's annual loss has more than doubled since 2000, and the town's budget is limited. Instead of paying for a train that carries fewer people every year, the town could run a bus service that stops closer to homes, the hospital, and the high school. A bus would cost far less to operate. Of course, before making any decision, we must listen carefully to the students and older residents who depend on the line.",
         tbl=table([["2000", "1,200", "80", "15,000"], ["2010", "800", "120", "13,000"], ["2020", "480", "180", "11,000"]],
                   header=["Year", "Average passengers per day", "Annual loss of the line (million yen)", "Population of the valley"],
                   caption="Ridge Line の利用者・赤字と Maple Valley の人口（架空の資料）"),
         tqs=[("表によると、2000年から2020年までに1日あたりの平均乗客数は何パーセント減ったか。", "60%",
               [("40%", "480÷1,200×100＝40 は、2020年の乗客数が2000年の何%かを表しており、減少率ではない。"),
                ("150%", "差の720人を2020年の480人で割っており、分母が誤っている。"),
                ("約27%", "人口の減少率（4,000÷15,000）で、乗客数ではない。")], ("(1200-480)/1200*100", "60")),
              ("Ms. Hara の述べる more than doubled since 2000 は、表のどの数値の変化を指しているか。", "年間の赤字が8,000万円から1億8,000万円に増えたこと",
               [("1日の乗客数が1,200人から480人に減ったこと", "乗客数は減っており、「2倍以上になった」ものではない。"),
                ("人口が15,000人から11,000人に減ったこと", "人口は減っており、2倍以上になったものではない。"),
                ("年間の赤字が2010年から2020年に6,000万円増えたこと", "120から180は1.5倍で、2倍を超えていない。また since 2000 は2000年からの変化である。")], ("180/80", "9/4")),
              ("表から、2000年から2020年の間の乗客数と人口の変化について正しいものはどれか。", "乗客数（60%減）のほうが、人口（約27%減）より大きな割合で減った。",
               [("人口のほうが、乗客数より大きな割合で減った。", "人口は約27%減、乗客数は60%減で、逆である。"),
                ("乗客数も人口も、同じ割合で減った。", "減少率は乗客数60%、人口約27%で、同じではない。"),
                ("乗客数は減ったが、人口は増えた。", "人口も15,000人から11,000人に減っている。")], ("(1200-480)/1200*100", "60"))],
         agree=("The Ridge Line is important for people who cannot drive.",
                [("The town should pay part of the railway company's costs.", "これは Mr. Mori だけの提案で、Ms. Hara は予算が限られていると述べている。"),
                 ("A bus service would be better than the train.", "これは Ms. Hara だけの提案である。"),
                 ("The number of passengers will increase in the future.", "どちらも乗客が増えるとは述べていない。")]),
         contrast=("Ms. Hara suggests replacing the train with a cheaper bus service, while Mr. Mori wants the town to help keep the line open.",
                   [("Ms. Hara wants the town to pay for the train, while Mr. Mori prefers a bus service.", "2人の立場が逆になっている。"),
                    ("Both of them want the line to be closed as soon as possible.", "Mr. Mori は路線の維持を求めている。"),
                    ("Mr. Mori thinks the line should close because few people use it.", "Mr. Mori は数字だけでは全体がわからないと述べ、維持を求めている。")]),
         facts=["The average number of passengers per day fell from 1,200 in 2000 to 480 in 2020.",
                "The Ridge Line has connected the valley to the city for more than seventy years.",
                "The line's annual loss has more than doubled since 2000."],
         opinions=[("The town should help the railway company keep the line open.", "should による提案"),
                   ("For many passengers, the train is not a convenience but a necessity.", "列車を「必需品だ」とみなす書き手の評価"),
                   ("Instead of paying for the train, the town could run a bus service.", "could による提案（別の案の提示）")],
         support=[("the line is becoming more and more expensive for the town", "The annual loss rose from 80 million yen in 2000 to 180 million yen in 2020.",
                   [("The population fell from 15,000 to 11,000.", "人口の変化で、路線の費用を示していない。"),
                    ("The line has run for more than seventy years.", "路線の歴史で、費用の根拠にならない。"),
                    ("Many passengers are high school students.", "利用者の内訳で、費用を示していない。")]),
                  ("fewer and fewer people are using the line", "Passengers per day fell from 1,200 to 800 and then to 480.",
                   [("The annual loss rose from 80 to 180 million yen.", "赤字の変化で、利用者数を直接示していない。"),
                    ("The population was 13,000 in 2010.", "人口の数値で、路線の利用者数ではない。"),
                    ("A bus would cost far less to operate.", "Ms. Hara の見通しで、利用者数の根拠ではない。")])],
         claim=("Mr. Mori は “numbers alone do not tell the whole story” と述べている。彼がそう述べる理由を説明し、Ms. Hara の立場から考えられる反論を、表の数値を用いて日本語で説明しなさい。",
                "Mr. Mori は、乗客が減っても、残る乗客の多くは運転できない高校生や高齢者で、彼らにとって鉄道は必需品であり、廃止すれば家族が流出して人口がさらに減ると考えているから。これに対し Ms. Hara の立場からは、年間の赤字が8,000万円から1億8,000万円へと2倍以上に増え、乗客は1,200人から480人に減っているので、限られた予算で鉄道を支えるより、運行費の安いバスで病院や高校の近くに停まるほうが、同じ人々の移動をより少ない費用で支えられる、と反論できる。"),
         rec=("町の会議で発言するとして、2つの資料を踏まえ、鉄道を残すべきかどうかについてあなたの意見を英語で書きなさい。",
              "I think the town should try a bus service. The line's loss grew from 80 to 180 million yen while passengers fell to 480 a day. However, the bus must stop near the high school and the hospital so that students and older people can still travel easily."),
         over=[("Because the population fell, the number of passengers fell by the same percentage.",
                "人口は15,000人から11,000人へ約27%減ったが、乗客数は1,200人から480人へ60%減っており、減少の割合は同じではない。人口の減少だけでは乗客の減少を説明しきれない。",
                "The number of passengers fell much faster (by 60 percent) than the population (by about 27 percent)."),
               ("The table shows that closing the line will make the population fall faster.",
                "表は2000年から2020年までの変化を示すだけで、廃止した場合の将来の人口は示していない。人口がさらに減るというのは Mr. Mori の予測（意見）である。",
                "Mr. Mori predicts that closing the line would make the population fall faster, but the table does not show what would happen after a closure.")]),
    dict(key="MRKT", title="The Riverside Farmers' Market",
         a_head="[Report] by Lisa Chen, market organizer", b_head="[Comment] by Tom Baker, owner of a grocery store on Station Street",
         a="The Riverside Farmers' Market opened in April last year in the parking lot next to the station. Every Saturday morning, about twenty local farmers sell vegetables, fruit, eggs, and bread directly to customers. In its first year, the market became a popular weekend spot for families.\nThe table shows the average number of visitors and the average total sales per Saturday in four months of last year. Visitors increased steadily from spring to autumn, and in October the market attracted 1,500 people a day. We plan to open the market on Sunday mornings as well from next spring. We believe that a second market day will bring even more people to the station area.",
         b="I welcome anything that brings people to the station area, and the market has certainly done that. However, sales at my store on Saturday mornings have fallen by about 10 percent since the market opened, because some of my customers now buy their vegetables at the market. If the market opens on Sundays too, small shops like mine may suffer even more. I hope the organizers will consider ways for local shops to take part, such as giving us a few spaces in the market.",
         tbl=table([["April", "600", "480,000"], ["June", "900", "630,000"], ["August", "1,100", "660,000"], ["October", "1,500", "960,000"]],
                   header=["Month", "Average visitors per Saturday", "Average total sales per Saturday (yen)"],
                   caption="Riverside Farmers' Market の来場者数と売上（土曜日1日あたりの平均・架空の資料）"),
         tqs=[("表から計算すると、来場者1人あたりの平均購入額が最も低かったのは何月で、いくらか。", "8月、600円",
               [("4月、800円", "4月は480,000÷600＝800円で、最も高い月である。"), ("10月、1,500円", "1,500 は10月の来場者数で、金額ではない。"),
                ("6月、630円", "630 は売上630,000円を1,000で割った数値で、1人あたりの額は630,000÷900＝700円である。")], ("660000/1100", "600")),
              ("4月と10月を比べたとき、表と一致するものはどれか。", "来場者数は2.5倍になったが、売上は2倍にとどまった。",
               [("来場者数も売上も2.5倍になった。", "売上は480,000円から960,000円で2倍である。"),
                ("売上は2.5倍になったが、来場者数は2倍にとどまった。", "来場者数と売上の倍率が逆になっている。"),
                ("来場者は900人増え、売上は900,000円増えた。", "売上の増加は960,000−480,000＝480,000円である。")], ("1500/600", "5/2")),
              ("記事には書かれていないが、表から読み取れることはどれか。", "来場者1人あたりの購入額は、4月が最も高かった。",
               [("来場者数は4月から10月まで増え続けた。", "表から読み取れるが、記事にも Visitors increased steadily と書かれている。"),
                ("10月の来場者は1日1,500人だった。", "表から読み取れるが、記事にも書かれている。"),
                ("来年の春から日曜日にも市場を開く予定である。", "記事に書かれている計画で、表からは読み取れない。")], ("480000/600", "800"))],
         agree=("The market has brought more people to the station area.",
                [("Opening on Sundays will help every business near the station.", "Mr. Baker は、日曜開催で小さな店がさらに苦しくなると心配している。"),
                 ("Sales at shops on Station Street have increased.", "Mr. Baker の店の売上は減っている。"),
                 ("The market should close to protect local shops.", "どちらも閉鎖を求めていない。Mr. Baker は人を呼ぶことを歓迎している。")]),
         contrast=("He welcomes the visitors but is worried that a Sunday market will hurt small local shops.",
                   [("He wants the market to close because it attracts too many people.", "人を呼ぶことは歓迎すると述べている。"),
                    ("He thinks a Sunday market will increase sales at his store.", "さらに苦しくなるかもしれないと述べており、逆である。"),
                    ("He says that the market has had no effect on his store.", "土曜朝の売上が約10%減ったと述べている。")]),
         facts=["The market opened in April last year in the parking lot next to the station.",
                "About twenty local farmers sell vegetables, fruit, eggs, and bread at the market.",
                "Sales at Mr. Baker's store on Saturday mornings have fallen by about 10 percent since the market opened."],
         opinions=[("A second market day will bring even more people to the station area.", "We believe に続く、書き手の予測"),
                   ("Small shops like mine may suffer even more.", "may（～かもしれない）による推測"),
                   ("The market has become a popular weekend spot for families.", "popular（人気の）という評価")],
         support=[("visitors have increased steadily", "Average visitors rose from 600 in April to 900, 1,100, and 1,500 in the following months.",
                   [("Sales per visitor fell from 800 yen to 640 yen.", "1人あたりの購入額の変化で、来場者数の増加を示していない。"),
                    ("About twenty farmers sell their products.", "出店者の数で、来場者の変化を示していない。"),
                    ("Mr. Baker's sales fell by about 10 percent.", "表にない情報で、来場者数の根拠ではない。")]),
                  ("visitors are spending less money each on average", "Sales per visitor fell from 800 yen in April to 640 yen in October.",
                   [("Total sales rose from 480,000 yen to 960,000 yen.", "総売上の増加で、1人あたりの額が減ったことを示していない。"),
                    ("The market attracted 1,500 people a day in October.", "来場者数だけで、1人あたりの額はわからない。"),
                    ("Visitors increased steadily from spring to autumn.", "来場者数の変化で、1人あたりの購入額を示していない。")])],
         claim=("Lisa Chen は “a second market day will bring even more people to the station area” と述べている。表の数値と Mr. Baker の意見を踏まえて、日曜開催を決める前に確かめるべき点を日本語で説明しなさい。",
                "表では来場者数は4月の600人から10月の1,500人に増えたが、1人あたりの購入額は800円から640円に下がっており、来場者の増加がそのまま売上の増加につながっているとは限らない。また Mr. Baker によると、市場の開設以来、駅前の店の土曜朝の売上が約10%減っている。したがって日曜開催の前に、日曜にも十分な来場者と出店者が見込めるか、地元の店への影響をどう抑えるか（出店枠を設けるなど）を確かめるべきである。"),
         rec=("市場の運営者に向けて、2つの資料を踏まえ、日曜開催についてのあなたの提案を英語で書きなさい。",
              "The market should open on Sundays only if local shops can join it. Visitors rose from 600 to 1,500, but Mr. Baker's sales fell by 10 percent, so giving shops a few spaces would help both the market and Station Street."),
         over=[("Each visitor spent more money in October than in April because total sales were higher.",
                "総売上は増えたが、来場者数がそれ以上に増えたので、1人あたりは4月800円、10月640円で、むしろ減っている。",
                "Total sales were higher in October, but each visitor spent less on average: 640 yen compared with 800 yen in April."),
               ("The market caused every shop on Station Street to lose 10 percent of its sales.",
                "10% の減少は Mr. Baker の店の土曜朝の売上についての話で、駅前通りのすべての店に当てはまるとは言えない。",
                "Mr. Baker says that sales at his own store on Saturday mornings fell by about 10 percent.")]),
    dict(key="LIBH", title="Longer Library Hours",
         a_head="[Report] by Daniel Ross, head of the Greenwood City Library", b_head="[Comment] by Ms. Park, library staff member",
         a="Since September, the Greenwood City Library has stayed open until 9 p.m. on weekdays instead of closing at 6 p.m. We made this change after many working adults and high school students told us that they could not visit during the day.\nTo see whether the change was worthwhile, we counted weekday visitors in each time slot in October, the second month of the new hours, and compared the numbers with October of last year. The evening hours are already attracting more than 2,000 visitors a month. We think the longer hours have been a clear success, and we plan to continue them next year.",
         b="The evening hours are clearly popular. But when I look at the numbers, I notice that fewer people are coming during the day than last year. The total has increased by only 1,500 visitors, even though we are now open 15 more hours each week. It is possible that some people who used to come in the afternoon now simply come in the evening instead. Keeping the library open longer also means higher costs for staff and electricity. I suggest that we ask visitors when they would most like the library to be open before deciding about next year.",
         tbl=table([["9 a.m.–12 p.m.", "3,000", "2,800"], ["12 p.m.–3 p.m.", "3,600", "3,400"], ["3 p.m.–6 p.m.", "4,400", "3,800"], ["6 p.m.–9 p.m.", "—", "2,500"], ["Total", "11,000", "12,500"]],
                   header=["Time slot (weekdays in October)", "Last year (closed at 6 p.m.)", "This year (open until 9 p.m.)"],
                   caption="Greenwood City Library の平日の時間帯別来館者数（10月・架空の資料）"),
         tqs=[("表によると、今年の10月、午後6時から9時の来館者は、平日の来館者全体の何パーセントか。", "20%",
               [("25%", "2,500÷10,000 で、日中（9時〜18時）の来館者だけを分母にしている。"),
                ("約23%", "2,500÷11,000 で、昨年の合計を分母にしている。"),
                ("約14%", "合計の増加率（1,500÷11,000）で、夜間の来館者の割合ではない。")], ("2500/12500*100", "20")),
              ("Ms. Park の fewer people are coming during the day than last year は、表のどの数値で確かめられるか。", "午前9時から午後6時までの来館者の合計が、11,000人から10,000人に減ったこと",
               [("午後6時から9時の来館者が2,500人だったこと", "夜間の来館者数で、日中の減少を示していない。"),
                ("来館者全体が11,000人から12,500人に増えたこと", "全体の増加で、日中の減少を示していない。"),
                ("午後3時から6時の来館者が、ほかの日中の時間帯より多いこと", "時間帯どうしの比較で、昨年からの減少を示していない。")], ("2800+3400+3800", "10000")),
              ("合計の増加（1,500人）は夜間の来館者数（2,500人）より1,000人少ない。この差について Ms. Park が考えている可能性はどれか。", "以前は日中に来ていた人の一部が、夜に来るようになっただけかもしれない。",
               [("夜間の来館者の数え方が誤っていたのかもしれない。", "Ms. Park は数え方の誤りには触れていない。"),
                ("昨年も夜間に開館していたのかもしれない。", "昨年は午後6時に閉館しており、表でも夜間の欄は「—」である。"),
                ("日中の来館者が増えたからかもしれない。", "日中の来館者は11,000人から10,000人に減っている。")], ("2500-1500", "1000"))],
         agree=("The evening hours are popular with visitors.",
                [("The longer hours should definitely continue next year.", "これは Mr. Ross の考えで、Ms. Park は利用者に尋ねてから決めるべきだと述べている。"),
                 ("Visitors should be asked before any decision is made.", "これは Ms. Park だけの提案である。"),
                 ("The total number of visitors decreased.", "合計は11,000人から12,500人に増えており、どちらもそう述べていない。")]),
         contrast=("Mr. Ross sees the change as a clear success, while Ms. Park thinks the numbers and costs should be examined more closely before deciding.",
                   [("Mr. Ross wants to stop the evening hours, while Ms. Park wants to continue them.", "Mr. Ross は来年も続ける予定だと述べており、立場が逆である。"),
                    ("Both of them think the evening hours have been a failure.", "どちらも夜間の時間帯は利用されていると認めている。"),
                    ("Ms. Park believes the evening hours attracted no visitors at all.", "Ms. Park は夜間は明らかに人気があると述べている。")]),
         facts=["Since September, the library has stayed open until 9 p.m. on weekdays.",
                "The library is now open 15 more hours each week than before.",
                "The library counted weekday visitors in each time slot in October."],
         opinions=[("The longer hours have been a clear success.", "a clear success（明らかな成功）という評価"),
                   ("It is possible that some people simply come in the evening instead.", "It is possible（～の可能性がある）による推測"),
                   ("We should ask visitors when they would most like the library to be open.", "suggest / should による提案")],
         support=[("fewer people are coming during the day", "Visitors between 9 a.m. and 6 p.m. fell from 11,000 to 10,000.",
                   [("2,500 people came between 6 p.m. and 9 p.m.", "夜間の来館者数で、日中の減少を示していない。"),
                    ("The total rose from 11,000 to 12,500.", "全体の増加で、日中の減少とは逆向きの数値である。"),
                    ("The library is open 15 more hours each week.", "開館時間の増加で、来館者数の根拠ではない。")]),
                  ("the evening hours are attracting many visitors", "2,500 people visited between 6 p.m. and 9 p.m. in October.",
                   [("Visitors between 3 p.m. and 6 p.m. fell from 4,400 to 3,800.", "日中の時間帯の減少で、夜間の利用を示していない。"),
                    ("Last year, the library closed at 6 p.m.", "昨年の開館時間で、夜間の来館者数を示していない。"),
                    ("The morning slot had 2,800 visitors this year.", "午前の来館者数で、夜間とは関係がない。")])],
         claim=("Mr. Ross は “the longer hours have been a clear success” と述べている。表の数値と Ms. Park の意見を用いて、この評価が十分に裏づけられているかを日本語で説明しなさい。",
                "夜間に2,500人が来館し、合計も11,000人から12,500人に増えたので、夜間開館が利用されていることは裏づけられる。しかし、日中の来館者は11,000人から10,000人に減っており、合計の増加は1,500人で夜間の来館者数より1,000人少ない。日中に来ていた人が夜に移っただけの可能性があり、週15時間の延長に伴う人件費や電気代も考えると、「明らかな成功」と言い切るには根拠が不十分である。"),
         rec=("図書館への意見として、2つの資料を踏まえ、来年の開館時間についてのあなたの提案を英語で書きなさい。",
              "I think the library should keep the evening hours on some weekdays only. The evening slot had 2,500 visitors, but the total rose by just 1,500, so many people may have moved from the afternoon. A survey of visitors would show the best days."),
         over=[("The longer hours brought 2,500 new visitors to the library.",
                "夜間の来館者2,500人の中には、以前は日中に来ていた人も含まれている可能性がある。合計の増加は1,500人である。",
                "The evening slot had 2,500 visitors, but the total increased by only 1,500, so not all of them were new visitors."),
               ("Since the total went up by 1,500, the number of visitors increased by 15 percent.",
                "増加率は1,500÷11,000×100 で約14%であり、15%ではない。増加数の1,500から割合を直感で判断し、元の値で割っていない。",
                "The number of visitors increased by about 14 percent (1,500 ÷ 11,000).")]),
]


def sstim(s):
    content = f"{s['a_head']}\n{s['a']}\n\n{s['b_head']}\n{s['b']}"
    return stim(f"EC2-{s['key']}", content, "passage", f"次の資料（“{s['title']}”：記事・表・コメント）を読んで、あとの問いに答えなさい。", source="オリジナル（架空の資料）", tbl=s["tbl"])


def shead(s):
    return f"資料“{s['title']}”について答えなさい。"


# ======================================================================
# 事実と意見の文（単独の文）
# ======================================================================

# (文, fact/opinion, 理由, 取り違えやすい理由)
FO = [
    ("According to the survey, 42 percent of the respondents said they used the library at least once a week.", "fact",
     "調査で回答者がそう答えたという結果の報告で、調査の記録で確かめられる。", "said（～と言った）とあり、回答者の考えを述べた文だと思った。"),
    ("Several experts have predicted that the town's population will continue to decline.", "fact",
     "予測の内容は意見だが、「専門家が予測した」こと自体は発言や報告書で確かめられる事実の報告である。", "predicted と will を見て、推測（意見）の文だと判断した。"),
    ("Some residents have complained about the noise from the construction site.", "fact",
     "苦情が寄せられたことは記録で確かめられる事実である。", "complained（不満を言った）という感情の語から、意見の文だと思った。"),
    ("The town spent 3 million yen on the project last year.", "fact",
     "予算の記録で確かめられる事実である。", "project の評価を述べた文だと読み違えた。"),
    ("The new bus route started operating in April 2023.", "fact",
     "運行開始の日付は記録で確かめられる事実である。", "new（新しい）を評価の語だと考えた。"),
    ("The number of visitors in August was twice that in February.", "fact",
     "来場者の記録で確かめられる数値の比較である。", "twice（2倍）を書き手の強調だと考えた。"),
    ("The results clearly show that the program was a waste of money.", "opinion",
     "a waste of money（お金の無駄）は書き手の評価で、clearly で強めても事実にはならない。", "The results show（結果が示している）とあり、調査結果の報告に見えた。"),
    ("A 5 percent increase is hardly worth celebrating.", "opinion",
     "hardly worth celebrating（祝うほどのことではない）は書き手の評価である。", "5 percent という数値があるので、事実の文だと考えた。"),
    ("It is likely that most students would welcome the change.", "opinion",
     "It is likely（～の可能性が高い）と would による推測である。", "most students という調査結果のような表現に引きずられた。"),
    ("This is probably the most serious problem our town faces.", "opinion",
     "probably（おそらく）と the most serious（最も深刻な）は推測と評価である。", "最上級 the most を、数値で比べた事実の比較だと考えた。"),
    ("Nobody can deny that the festival has brought the community together.", "opinion",
     "断定的な言い方だが、「地域を一つにした」は評価で、確かめる方法がない。", "Nobody can deny（誰も否定できない）という強い言い方から、確かな事実だと考えた。"),
    ("The new library building is far more attractive than the old one.", "opinion",
     "attractive（魅力的な）は評価の語で、確かめる方法がない。", "far more … than という比較の形を、数値の比較だと考えた。"),
    ("Only 30 percent of the members came to the meeting, which shows how little they care about the club.", "opinion",
     "前半の出席率は事実だが、which 以下の「ほとんど関心がない」は書き手の解釈で、文全体としては意見を述べている。", "30 percent という数値に引きずられ、which 以下の解釈を見落とした。"),
    ("The town should use its budget to repair roads instead.", "opinion",
     "should（～すべきだ）による提案である。", "budget や repair という具体的な語から、計画の事実だと思った。"),
]
FACTS = [x for x in FO if x[1] == "fact"]
OPINIONS = [x for x in FO if x[1] == "opinion"]


# ======================================================================
# ランダムな調査表（架空）
# ======================================================================

CTX = [
    dict(topic="How students get to school", jp="通学手段", cats=["walking", "cycling", "taking the bus", "taking the train"]),
    dict(topic="Favorite way to spend free time", jp="自由時間の過ごし方", cats=["playing sports", "reading", "watching videos", "meeting friends"]),
    dict(topic="Main source of news", jp="主なニュースの情報源", cats=["television", "newspapers", "social media", "news websites"]),
    dict(topic="Preferred place to study", jp="好きな勉強場所", cats=["at home", "at school", "in a library", "in a cafe"]),
    dict(topic="Main way to listen to music", jp="主な音楽の聞き方", cats=["streaming apps", "CDs", "the radio", "music videos"]),
]
YEARS = [(2015, 2025), (2018, 2024), (2016, 2026), (2019, 2025)]


def rand_shares(r):
    """5の倍数・各5以上・合計100の4つの割合。"""
    while True:
        a = [r.randrange(1, 12) * 5 for _ in range(3)]
        d = 100 - sum(a)
        if 5 <= d <= 55:
            v = a + [d]
            r.shuffle(v)
            return v


def survey(r):
    ctx = r.choice(CTX)
    y1, y2 = r.choice(YEARS)
    v1, v2 = rand_shares(r), rand_shares(r)
    tbl = table([[c, f"{a}%", f"{b}%"] for c, a, b in zip(ctx["cats"], v1, v2)], header=["Answer", str(y1), str(y2)],
                caption=f"ある高校の生徒に「{ctx['jp']}」を尋ねた調査（各年200人・架空の資料）")
    return ctx, y1, y2, v1, v2, tbl


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "condition_check"])
def a_table_calc(r):
    kind = r.choice(["change", "change", "share"])
    if kind == "change":
        place = r.choice(["the city museum", "the town pool", "the community center", "the botanical garden", "the science hall"])
        y1, y2 = r.choice([(2022, 2024), (2021, 2023), (2020, 2025)])
        base = r.randrange(10, 60) * 20
        p = r.choice([5, 10, 15, 20, 25, 30, 40, 50, -10, -15, -20, -25, -30])
        new = base * (100 + p) // 100
        d = new - base
        up = d > 0
        word = "増加" if up else "減少"
        ok = f"{abs(p)}%{word}"
        wb = round(abs(d) / new * 100)
        cands = [] if wb == abs(p) else [(f"約{wb}%{word}", f"差の{cm(abs(d))}を新しい値の{cm(new)}で割っており、基準が誤っている。増加率・減少率は元の値（{y1}年の{cm(base)}）で割る。", "割合の基準（分母）の取り違え")]
        cands += [(f"{100 + p}%{word}", f"{100 + p}% は{y2}年の値が{y1}年の値の何%にあたるかで、変化の割合ではない。", "比の値と変化率の混同"),
                 (f"{abs(p)}%{'減少' if up else '増加'}", f"{y1}年から{y2}年にかけて{'増えて' if up else '減って'}おり、変化の向きが逆である。", "変化の向きの取り違え")]
        if abs(d) != abs(p):
            cands.append((f"{cm(abs(d))}%{word}", f"{cm(abs(d))} は人数の差で、割合ではない。", "差と割合の混同"))
        wrongs = []
        for c in cands:
            if c[0] != ok and c[0] not in [w[0] for w in wrongs]:
                wrongs.append(c)
        wrongs = wrongs[:3]
        tbl = table([[str(y1), cm(base)], [str(y2), cm(new)]], header=["Year", f"Visitors to {place} in July"], caption="（架空の資料）")
        return mc(f"次の表は、ある施設の7月の来場者数である。{y1}年から{y2}年にかけて、来場者数は何パーセント変化したか。最も適切なものを選びなさい。",
                  [ok] + [w[0] for w in wrongs], f"{ok}。（{cm(new)}−{cm(base)}）÷{cm(base)}×100＝{p}（%）。", d=2, tbl=tbl,
                  ap="変化の割合は「差 ÷ 元の値 × 100」。元の値（比べるもとになる古い年の値）を分母にする。",
                  steps=[f"差を求める：{cm(new)}−{cm(base)}＝{d}。", f"元の値 {cm(base)} で割って100をかける：{d}÷{cm(base)}×100＝{p}。", f"符号から{word}と判断する：{ok}。"],
                  alt=[f"{cm(base)}×{100 + p}/100＝{cm(new)} となることを確かめて逆算する。"],
                  pc=[("元の値を分母にした式を立てている", 1), ("正しい割合を選んでいる", 1)],
                  pit=["新しい値で割る。", "比の値（○%にあたる）と変化率（○%増えた）を混同する。"],
                  why={w[0]: (w[1], w[2]) for w in wrongs}, chk=(f"({new}-{base})/{base}*100", str(p), None, "intermediate"))
    ctx = r.choice(CTX)
    total = r.choice([200, 400, 500])
    unit = {200: 2, 400: 4, 500: 5}[total]
    while True:
        cnt = [r.randrange(4, 40) * unit for _ in range(3)]
        last = total - sum(cnt)
        if last >= 4 * unit and last % unit == 0:
            cnt.append(last)
            break
    i = r.randrange(4)
    share = cnt[i] * 100 // total
    others = total - cnt[i]
    j = (i + 1) % 4
    oth_share = cnt[j] * 100 // total
    alt_sh = round(cnt[i] / others * 100)
    cands = [] if alt_sh == share else [(f"約{alt_sh}%", f"「{ctx['cats'][i]}」以外の人数（{others}人）を分母にしている。全体の{total}人で割る。", "割合の基準（分母）の取り違え")]
    cands += [(f"{cnt[i]}%", f"{cnt[i]} は人数で、割合ではない（全体が100人のときだけ一致する）。", "人数と割合の混同"),
             (f"{oth_share}%", f"「{ctx['cats'][j]}」の割合で、別の行の数値を読んでいる。", "読み取る行の取り違え")]
    cands = [c for c in cands if c[0] != f"{oth_share}%" or oth_share != share]
    ok = f"{share}%"
    wrongs = []
    for c in cands:
        if c[0] != ok and c[0] not in [w[0] for w in wrongs]:
            wrongs.append(c)
    while len(wrongs) < 3:
        v = f"{share + 5 * len(wrongs)}%"
        if v != ok and v not in [w[0] for w in wrongs]:
            wrongs.append((v, "計算の誤り。人数÷全体×100 を計算し直す。", "計算の誤り"))
    tbl = table([[c, str(n)] for c, n in zip(ctx["cats"], cnt)] + [["Total", str(total)]], header=["Answer", "Number of students"], caption=f"「{ctx['jp']}」についての調査（架空の資料）")
    return mc(f"次の表は、ある高校で「{ctx['jp']}」を尋ねた調査の結果である。“{ctx['cats'][i]}” と答えた生徒は、回答者全体の何パーセントか。最も適切なものを選びなさい。",
              [ok] + [w[0] for w in wrongs], f"{ok}。{cnt[i]}÷{total}×100＝{share}（%）。", d=2, tbl=tbl,
              ap="「全体の何%か」は、その項目の人数を全体（Total）で割って100をかける。どの行・どの列を使うかを先に確かめる。",
              steps=[f"“{ctx['cats'][i]}” の行の人数を読む：{cnt[i]}人。", f"全体の人数を確認する：{total}人。", f"{cnt[i]}÷{total}×100＝{share}（%）。"],
              alt=[f"4つの項目の割合をすべて計算し、合計が100%になることを確かめる。"],
              pc=[("正しい行と全体の人数を読み取っている", 1), ("正しい割合を選んでいる", 1)],
              pit=["その項目以外の人数を分母にする。", "隣の行の数値を読む。"],
              why={w[0]: (w[1], w[2]) for w in wrongs[:3]}, chk=(f"{cnt[i]}/{total}*100", str(share), None, "intermediate"))


def chart_statements(ctx, y1, y2, v1, v2):
    cats = ctx["cats"]
    T, F = [], []
    for y, v in ((y1, v1), (y2, v2)):
        m = max(v)
        top = [c for c, x in zip(cats, v) if x == m]
        for c, x in zip(cats, v):
            s = f"In {y}, \"{c}\" was the most common answer."
            if len(top) == 1 and c == top[0]:
                T.append(s)
            elif x < m:
                F.append((s, f"{y}年の “{c}” は{x}%で、最も多いのは “{top[0]}”（{m}%）である。"))
    for c, a, b in zip(cats, v1, v2):
        d = b - a
        if d > 0:
            T.append(f"The percentage for \"{c}\" rose by {d} percentage points between {y1} and {y2}.")
            pct = d * 100 / a
            if pct != d and pct == int(pct):
                F.append((f"The percentage for \"{c}\" rose by {int(pct)} percentage points between {y1} and {y2}.",
                          f"“{c}” は{a}%から{b}%で、差は{d}ポイントである。{int(pct)} は増加率（%）で、ポイントの差ではない。"))
            F.append((f"The percentage for \"{c}\" fell between {y1} and {y2}.", f"“{c}” は{a}%から{b}%に増えている。"))
        elif d < 0:
            T.append(f"The percentage for \"{c}\" fell between {y1} and {y2}.")
            F.append((f"The percentage for \"{c}\" rose between {y1} and {y2}.", f"“{c}” は{a}%から{b}%に減っている。"))
        else:
            T.append(f"The percentage for \"{c}\" did not change between {y1} and {y2}.")
    for y, v in ((y1, v1), (y2, v2)):
        for i in range(4):
            for j in range(4):
                if i != j and v[i] > v[j]:
                    s = f"In {y}, the percentage for \"{cats[i]}\" was twice as high as that for \"{cats[j]}\"."
                    if v[i] == 2 * v[j]:
                        T.append(s)
                    elif (i + j + y) % 3 == 0:
                        F.append((s, f"{y}年は “{cats[i]}” {v[i]}%、“{cats[j]}” {v[j]}%で、2倍ではない。"))
    return T, F


@gen("basic_check", 5, ["concept", "computation"])
def a_chart_statement(r):
    for _ in range(100):
        ctx, y1, y2, v1, v2, tbl = survey(r)
        T, F = chart_statements(ctx, y1, y2, v1, v2)
        if T and len(F) >= 3:
            break
    ok = r.choice(T)
    wrongs = r.sample(F, 3)
    return mc(f"次の表は、ある高校の生徒に「{ctx['jp']}」を尋ねた調査の結果である。表の内容と一致する英文を1つ選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　表の該当する行・年の数値と照合すると一致する。", d=2, tbl=tbl,
              ap="英文の主語（どの回答か）・年・変化の表し方（rose / fell / twice / percentage points）を確かめ、表の該当する欄と照合する。",
              steps=["各英文が表のどの行・どの年を指しているかを特定する。", "rose / fell は2つの年の数値の大小で、percentage points は差で、twice は比で確かめる。", f"表と一致するのは：{ok}"],
              alt=["誤りの英文を、表に合うように書き直してみる（数値・向き・比較の対象を直す）ことで、どこが誤りかを確かめる。"],
              pc=[("英文と表の欄を正しく対応させている", 1), ("一致する英文を選んでいる", 1)],
              pit=["増加率（%）とポイントの差を混同する。", "年を取り違えて、もう一方の年の数値で判断する。"],
              why={w: (reason, "図表と英文の照合の誤り") for w, reason in wrongs})


@gen("basic_check", 5, ["concept", "condition_check"])
def a_fact_opinion(r):
    if r.random() < 0.5:
        ok = r.choice(FACTS)
        wrongs = r.sample(OPINIONS, 3)
        return mc("次の4つの英文は、ある町の課題についての記事や投書からとったものである。意見（opinion）ではなく事実（fact）を述べているものを選びなさい。",
                  [ok[0]] + [w[0] for w in wrongs], f"{ok[0]}　{ok[2]}", d=2,
                  ap="各文について「記録・調査・発言で確かめる方法があるか」を問う。評価・推測・提案の語（clearly / probably / likely / should / attractive / worth）があれば意見。",
                  steps=["各文の評価・推測・提案の語に印をつける。", "印のついた文を意見として外す。", f"確かめる方法がある文：{ok[0]}"],
                  alt=["選んだ文について、どんな資料（記録・調査・報告）で確かめられるかを具体的に言えるかで確認する。"],
                  pc=[("意見の手がかりに気づいている", 1), ("事実の文を選んでいる", 1)],
                  pit=["数値を含む意見文を事実と判断する。", "言い方の強い意見文（Nobody can deny …）を事実と判断する。"],
                  why={w[0]: (w[2], "意見を事実と取り違える") for w in wrongs})
    ok = r.choice(OPINIONS)
    wrongs = r.sample(FACTS, 3)
    return mc("次の4つの英文は、ある町の課題についての記事や投書からとったものである。事実（fact）ではなく意見（opinion）を述べているものを選びなさい。",
              [ok[0]] + [w[0] for w in wrongs], f"{ok[0]}　{ok[2]}", d=2,
              ap="評価・判断・推測・提案を表す語や解釈の部分（which shows … など）を探す。数値の有無では決めない。",
              steps=["各文の中の評価・推測・提案を表す語を探す。", f"意見の文：{ok[0]}（{ok[2]}）", "ほかの3文は、記録・調査・発言で確かめられる事実（報告を含む）である。"],
              alt=["選んだ文について「人によって判断が分かれるか」を考え、分かれるなら意見と確かめる。"],
              pc=[("意見の手がかりを見つけている", 1), ("意見の文を選んでいる", 1)],
              pit=["predicted / complained を含む報告の文を意見と判断する。"],
              why={w[0]: (w[2] + "意見ではない。", "事実の報告を意見と取り違える") for w in wrongs})


@gen("basic_check", 5, ["common_error", "computation"])
def a_points(r):
    ctx = r.choice(CTX)
    c = r.choice(ctx["cats"])
    v1 = r.choice([10, 20, 25, 40, 50])
    d = r.choice([x for x in (5, 10, 15, 20, 25, 30) if x * 100 % v1 == 0 and v1 + x <= 80])
    up = r.random() < 0.6 or v1 - d < 5
    v2 = v1 + d if up else v1 - d
    pct = d * 100 // v1
    w1, w2 = ("rose", "increase") if up else ("fell", "decrease")
    ok = f"It {w1} by {d} percentage points, which is a {pct} percent {w2}."
    cands = [(f"It {w1} by {d} percent, which is a {d} point {w2}.", f"{v1}%から{v2}%への変化は、差が{d}ポイントで、変化の割合は{d}÷{v1}×100＝{pct}%である。{d} percent はポイントとパーセントの混同。", "ポイントとパーセントの混同"),
             (f"It {w1} by {pct} percentage points, which is a {d} percent {w2}.", f"ポイントとパーセントが入れかわっている。差は{d}ポイント、変化率は{pct}%。", "ポイントとパーセントの混同"),
             (f"It {w1} by {d} percentage points, which is a {round(d * 100 / v2) if round(d * 100 / v2) != pct else pct + 5} percent {w2}.", f"変化率を新しい値（{v2}%）で割って求めている。元の値（{v1}%）で割ると{pct}%。", "割合の基準（分母）の取り違え")]
    wrongs = []
    for t, why, mis in cands:
        if t != ok and t not in [w[0] for w in wrongs]:
            wrongs.append((t, why, mis))
    while len(wrongs) < 3:
        t = f"It {'fell' if up else 'rose'} by {d} percentage points, which is a {pct} percent {'decrease' if up else 'increase'}."
        wrongs.append((t, f"{v1}%から{v2}%に{'増えて' if up else '減って'}おり、変化の向きが逆である。", "変化の向きの取り違え"))
    y1, y2 = r.choice(YEARS)
    return mc(f"ある高校の調査で、「{ctx['jp']}」として “{c}” と答えた生徒の割合は、{y1}年は{v1}%、{y2}年は{v2}%だった（架空の資料）。この変化を正しく表している英文を選びなさい。",
              [ok] + [w[0] for w in wrongs[:3]], f"{ok}　差は {v2}−{v1}＝{v2 - v1}（ポイント）、変化率は {d}÷{v1}×100＝{pct}（%）。", d=2,
              ap="割合どうしの差は percentage points、元の割合に対する変化の大きさは percent で表す。変化率の分母は元の値。",
              steps=[f"差を求める：{v2}−{v1}＝{v2 - v1}（ポイント）。", f"変化率を求める：{d}÷{v1}×100＝{pct}（%）。", f"両方を正しく表す英文：{ok}"],
              alt=[f"200人の調査なら{v1}%は{v1 * 2}人、{v2}%は{v2 * 2}人。人数の変化（{d * 2}人）÷{v1 * 2}人×100 でも{pct}%になることを確かめる。"],
              pc=[("ポイントの差を求めている", 1), ("変化率を正しく求めて選んでいる", 1)],
              pit=["割合の差を「○ percent 増えた」と表す。"], why={w[0]: (w[1], w[2]) for w in wrongs[:3]},
              chk=(f"{d}*100/{v1}", str(pct), None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "application"])
def b_integrate(r):
    s = r.choice(SETS)
    q, ok, wrongs, chk = r.choice(s["tqs"])
    kw = {"chk": (chk[0], chk[1], None, "intermediate")} if chk else {}
    return mc(f"{shead(s)}\n{q}最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　本文の記述と表の欄（行・列・時期）を対応させ、必要なら計算して確かめる。", d=3, stim=sstim(s),
              ap="設問の数値・語句が、表のどの行・どの列・どの時期にあたるかを先に特定する。割合は分母（全体か、グループの中か、元の値か）を確かめる。",
              steps=["設問が求めている情報（割合・差・倍率・数値の意味）を確認する。", "本文と表から必要な数値を探し、どの欄の数値かを確かめる。",
                     "必要な計算を式で書いて行う（増加率・減少率は元の値で割る）。", f"答え：{ok}"],
              alt=["誤りの選択肢が「別の行・列の数値」「分母の取り違え」「期間の取り違え」のどれにあたるかを確かめて消去する。"],
              pc=[("本文と表の対応する欄を特定している", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["グループの中の割合を全体の割合として読む。", "本文に出てくる別の数値（目標値など）を選ぶ。"],
              why={w: (reason, "資料の照合・計算の誤り") for w, reason in wrongs}, **kw)


@gen("standard_practice", 5, ["concept", "condition_check"])
def b_compare(r):
    s = r.choice(SETS)
    a_name = s["a_head"].split(" by ")[1].split(",")[0]
    b_name = s["b_head"].split(" by ")[1].split(",")[0]
    if r.random() < 0.5:
        ok, wrongs = s["agree"]
        return mc(f"{shead(s)}\n{a_name} と {b_name} の両方が認めている内容として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
                  f"{ok}　2人の評価や提案は分かれているが、この点はどちらも認めている。", d=3, stim=sstim(s),
                  ap="2人の書き手の文を「論点 × 書き手」の表に整理し、両方の欄に〇がつく論点を探す。一方だけの提案は「両方」の答えにならない。",
                  steps=["記事の主張・根拠・提案を書き出す。", "コメントの主張・根拠・提案を書き出す。", "両者に共通する内容を探す（譲歩の部分 I understand / I welcome / are clearly popular に注目）。", f"答え：{ok}"],
                  alt=["各選択肢に「記事：〇／×」「コメント：〇／×」をつけ、両方〇のものだけを残す。"],
                  pc=[("2人の立場を整理している", 2), ("一致点を選んでいる", 2)],
                  pit=["一方の書き手だけの主張や提案を、両者の一致点として選ぶ。"],
                  why={w: (reason, "一方の意見と共通の意見の混同") for w, reason in wrongs})
    ok, wrongs = s["contrast"]
    return mc(f"{shead(s)}\n記事に対する {b_name} の立場を説明したものとして最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　コメントの前半で記事の内容の一部を認め、However / But 以降で別の見方を示している。", d=3, stim=sstim(s),
              ap="コメントの書き手が記事のどこを認め（譲歩）、どこに異議や別の提案を示しているかを、However / But / Still の前後で分ける。",
              steps=["コメントの最初の文で、記事の何を認めているかを確認する。", "However / But の後ろで、何に異議を示しているかを確認する。", "最後の文で、どんな提案をしているかを確認する。", f"答え：{ok}"],
              alt=["コメントの書き手の立場を「賛成・反対・条件つき」のどれかに分類し、その分類に合う選択肢を選ぶ。"],
              pc=[("譲歩と異議の部分を区別している", 2), ("立場を正しく選んでいる", 2)],
              pit=["コメントの冒頭の譲歩（I welcome / I understand）だけを見て、全面的に賛成していると考える。"],
              why={w: (reason, "書き手の立場の取り違え") for w, reason in wrongs})


@gen("standard_practice", 5, ["concept", "common_error"])
def b_doc_fo(r):
    s = r.choice(SETS)
    if r.random() < 0.5:
        ok = r.choice(s["facts"])
        wrongs = r.sample(s["opinions"], 3)
        return mc(f"{shead(s)}\n次の英文は資料の内容をまとめたものである。意見ではなく事実を述べているものを選びなさい。", [ok] + [w for w, _ in wrongs],
                  f"{ok}　資料の記録や発言で確かめられる事実である。", d=3, stim=sstim(s),
                  ap="各文の評価・推測・提案の語（should / could / may / believe / confident / clearly / popular / necessity）に印をつけ、印のない、確かめられる文を選ぶ。",
                  steps=["各文が資料のどこに対応するかを確かめる。", "評価・推測・提案の語がある文を意見として外す。", f"確かめられる事実の文：{ok}"],
                  alt=["選んだ文が、表の数値や記事の記録のどれで確かめられるかを指し示せるかで確認する。"],
                  pc=[("意見の手がかりを見つけている", 2), ("事実の文を選んでいる", 2)],
                  pit=["書き手の強い確信（we are confident / clearly）を事実の根拠と考える。"],
                  why={w: (f"{sig}を含み、書き手の意見である。", "意見を事実と取り違える") for w, sig in wrongs})
    ok, sig = r.choice(s["opinions"])
    wrongs = r.sample(s["facts"], 3)
    return mc(f"{shead(s)}\n次の英文は資料の内容をまとめたものである。事実ではなく意見を述べているものを選びなさい。", [ok] + wrongs,
              f"{ok}　{sig}を含み、書き手の意見である。", d=3, stim=sstim(s),
              ap="評価・推測・提案の語を探す。数値や発言の報告（said）は事実として扱う。",
              steps=["各文の評価・推測・提案の語を探す。", f"意見の手がかり：{sig}", f"意見の文：{ok}"],
              alt=["選んだ文を「確かめる方法があるか」で点検し、ほかの3文には確かめる方法があることを確認する。"],
              pc=[("意見の手がかりを見つけている", 2), ("意見の文を選んでいる", 2)],
              pit=["発言の報告（The committee leader said …）を意見と判断する。"],
              why={w: ("資料の記録・数値・発言で確かめられる事実で、意見ではない。", "事実を意見と取り違える") for w in wrongs})


@gen("standard_practice", 5, ["application", "condition_check"])
def b_support(r):
    s = r.choice(SETS)
    claim, ok, wrongs = r.choice(s["support"])
    return mc(f"{shead(s)}\n“{claim}” という考えを最もよく裏づける資料の情報はどれか。最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　この考えと同じ向きの変化・比較を、表の数値で直接示している。", d=3, stim=sstim(s),
              ap="考えの中心の語（sleep less / popular / expensive / fewer）を確かめ、その量を直接示す表の列と、比較の相手（どの時期・どの集団と比べるか）を探す。",
              steps=["考えが「何が・どう変化する／違う」と言っているかを確認する。", "その量を表す表の列を特定する。", "比較になっている（2つ以上の時期・集団を比べている）選択肢を選ぶ。", f"答え：{ok}"],
              alt=["選んだ情報と考えを because でつないだ英文（claim because evidence）を作り、論理が通るかを確かめる。"],
              pc=[("考えの中心と表の列を対応させている", 2), ("裏づけとなる情報を選んでいる", 2)],
              pit=["資料に書かれている数値なら、どの考えの根拠にもなると考える。", "比較のない単独の数値を根拠に選ぶ。"],
              why={w: (reason, "根拠と考えの対応の取り違え") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["cross_unit", "computation", "written_reasoning"], rel=["HS-ENG-U10", "HS-MATH1-U05"])
def c_describe(r):
    ctx, y1, y2, v1, v2, tbl = survey(r)
    while len(set(v2)) < 4 or v1 == v2:
        ctx, y1, y2, v1, v2, tbl = survey(r)
    cats = ctx["cats"]
    while True:
        k = r.randrange(4)
        if v1[k] != v2[k]:
            break
    hi = max(range(4), key=lambda i: (v2[i], -i))
    lo = min(range(4), key=lambda i: (v2[i], i))
    if v2[hi] % v2[lo] == 0 and v2[hi] // v2[lo] in (2, 3, 4, 5):
        mult = {2: "twice", 3: "three times", 4: "four times", 5: "five times"}[v2[hi] // v2[lo]]
        s1 = f"In {y2}, the percentage of students who chose \"{cats[hi]}\" ({v2[hi]}%) was {mult} as high as that for \"{cats[lo]}\" ({v2[lo]}%)."
    else:
        s1 = f"In {y2}, \"{cats[hi]}\" was the most common answer ({v2[hi]}%), while \"{cats[lo]}\" was the least common ({v2[lo]}%)."
    d = v2[k] - v1[k]
    verb = "rose" if d > 0 else "fell"
    s2 = f"The percentage for \"{cats[k]}\" {verb} from {v1[k]}% in {y1} to {v2[k]}% in {y2}, a change of {abs(d)} percentage points."
    return desc(f"次の表は、ある高校の生徒に「{ctx['jp']}」を尋ねた調査の結果である。表を見て、(1)(2) の英文を書きなさい。\n(1) {y2}年に最も多かった回答と最も少なかった回答を、数値を含めて比べる英文を1文書きなさい。\n(2) “{cats[k]}” の割合の変化を、{y1}年と{y2}年の数値と、何ポイントの変化かを含めて英文1文で書きなさい。",
                f"(1) {s1}　(2) {s2}",
                f"(1) {y2}年は “{cats[hi]}” {v2[hi]}%、“{cats[lo]}” {v2[lo]}%。(2) {v2[k]}−{v1[k]}＝{d}（ポイント）。",
                [("(1) 最多・最少の回答を正しく読み取り、比較の表現で表している", 4), ("(2) 変化の向きとポイントの差を正しく英語で表している", 4)], d=4, p=8, lines=6, tbl=tbl,
                ap="(1) は最大・最小を見つけ、倍数表現（twice as high as）か while による対比で表す。(2) は rose / fell from A to B と percentage points を使う。",
                steps=[f"{y2}年の最大は “{cats[hi]}”（{v2[hi]}%）、最小は “{cats[lo]}”（{v2[lo]}%）。", f"“{cats[k]}” の変化：{v1[k]}% → {v2[k]}%、差は{abs(d)}ポイント（{'増加' if d > 0 else '減少'}）。",
                       "比較・変化の表現を選んで英文にする。", "数値と年、percentage points と percent の区別を見直す。"],
                alt=[f"(2) は The share of students who chose \"{cats[k]}\" {'increased' if d > 0 else 'decreased'} by {abs(d)} percentage points. のように、変化の大きさを主にして書くこともできる。"],
                pc=[("数値の読み取りと計算", 3), ("比較・変化の表現", 3), ("percentage points などの語法", 2)],
                pit=["割合の差を by ○ percent と書く。", "rise の過去形を rised とする（正しくは rose）。"],
                chk=(f"{v2[k]}-{v1[k]}", str(d), None, "intermediate"))


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def c_evaluate(r):
    s = r.choice(SETS)
    q, a = s["claim"]
    return desc(f"{shead(s)}\n{q}", a,
                "資料から言えること（表の数値・計算結果）と、書き手の解釈・予測を分け、もう一方の書き手の指摘を加えて評価する。",
                [("表の数値を正しく引用・計算して根拠にしている", 3), ("もう一方の書き手の指摘を踏まえている", 3), ("資料から言えることと言えないことを区別して結論を述べている", 2)], d=4, p=8, lines=7, stim=sstim(s),
                ap="評価する主張に必要な数値を表から集めて計算し、それで言える範囲を確かめる。次に、コメント（または記事）の書き手が示した別の要因・費用・影響を加える。",
                steps=["評価する主張が何を言っているかを確認する。", "表から関係する数値を集め、増加率・差・1人あたりなどを計算する。",
                       "もう一方の書き手の指摘（別の要因・費用・影響）を確認する。", "「言えること」と「言えないこと」を分け、主張が十分に裏づけられているかを結論づける。"],
                alt=["答案を「表から言えること → 言えないこと（理由）→ 結論」の3文構成で書くと、論理が崩れにくい。"],
                pc=[("数値の根拠", 3), ("他方の書き手の指摘", 3), ("結論の妥当性", 2)],
                pit=["一方の書き手の評価をそのまま結論として書く。", "相関を因果として述べる。"])


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def c_recommend(r):
    s = r.choice(SETS)
    q, model = s["rec"]
    n = r.choice([40, 50])
    return desc(f"{shead(s)}\n{q}（{n}語程度。表の数値を1つ以上引用し、2人の書き手のどちらの指摘も踏まえること。）",
                f"（解答例）{model}",
                "提案 → 数値の根拠 → もう一方の立場への配慮、の順に書く。数値は rose from A to B / fell by ～ percent などで正確に引用する。",
                [("提案（立場）が明確である", 2), ("表の数値を正確に引用して根拠にしている", 3), ("2人の書き手の指摘を踏まえ、文法・語数が適切である", 3)], d=4, p=8, lines=7, stim=sstim(s),
                ap="I suggest / I think … should で提案を述べ、表の数値で理由を示し、However / but で反対側の心配への対応を加える。",
                steps=["2人の書き手の立場と、その根拠を整理する。", "自分の提案を決める（どちらかに賛成・条件つき・折衷案）。",
                       "表から根拠となる数値を選び、正確な英語で引用する。", "反対側の心配への対応を1文加え、語数を確かめる。"],
                alt=["一方の書き手に全面的に賛成する場合も、もう一方の指摘を Although … で認めてから主張すると説得力が増す。"],
                pc=[("提案", 2), ("数値の引用", 3), ("両者の視点と言語の正確さ", 3)],
                pit=["数値を引用せずに意見だけを書く。", "percent と percentage points、増加と減少の語を取り違える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "computation"])
def d_calc_err(r):
    if r.random() < 0.5:
        ctx = r.choice(CTX)
        c = r.choice(ctx["cats"])
        v1 = r.choice([10, 20, 25, 40, 50])
        d = r.choice([x for x in (5, 10, 15, 20, 25) if x * 100 % v1 == 0 and v1 + x <= 80])
        v2 = v1 + d
        pct = d * 100 // v1
        y1, y2 = r.choice(YEARS)
        wrong = f"The share of students who chose \"{c}\" increased by {d} percent."
        fix = f"The share of students who chose \"{c}\" increased by {d} percentage points (a {pct} percent increase)."
        return desc(f"ある高校の調査で、「{ctx['jp']}」として “{c}” と答えた生徒の割合は、{y1}年の{v1}%から{y2}年には{v2}%になった（架空の資料）。この変化を英語で説明する課題で、ある生徒は次のように書いた。\n［ある生徒の解答］\n{wrong}\nこの解答の誤りを指摘し、正しい英文に直しなさい。",
                    fix, f"割合どうしの差は percentage points で表す。{v2}−{v1}＝{d}（ポイント）、変化率は {d}÷{v1}×100＝{pct}（%）。",
                    [("ポイントとパーセントの混同を指摘している", 2), ("正しい英文に直している", 3), ("変化率を正しく計算している", 1)], d=3, p=6, lines=5,
                    ap="割合の差（ポイント）と、元の割合に対する変化率（パーセント）を両方計算して、生徒の数値がどちらを意味してしまっているかを確かめる。",
                    steps=[f"差を求める：{v2}−{v1}＝{d}（ポイント）。", f"変化率を求める：{d}÷{v1}×100＝{pct}（%）。", f"by {d} percent は「{pct}%増」と言うべきところを誤って表している。", f"正しい英文：{fix}"],
                    alt=[f"200人の調査として人数に直し（{v1 * 2}人 → {v2 * 2}人）、増えた人数 {d * 2}人が元の{v1 * 2}人の{pct}%であることを確かめる。"],
                    pc=[("誤りの指摘", 2), ("正しい英文", 3), ("変化率の計算", 1)],
                    pit=["割合の差を「○%増えた」と表す。"],
                    err=dict(sol=wrong, step=f"by {d} percent", type="concept", tempt="割合（%）どうしの差なので、そのまま percent をつければよいと考えた。", fix=fix),
                    chk=(f"{d}*100/{v1}", str(pct), None, "intermediate"))
    place = r.choice(["ある市の博物館", "ある町の市民プール", "ある地域の公民館", "ある市の植物園", "ある町の科学館"])
    base = r.randrange(10, 50) * 40
    p = r.choice([10, 20, 25, 30, 40, 50])
    new = base * (100 - p) // 100
    diff = base - new
    wb = round(diff / new * 100)
    if wb == p:
        wb = p + 5
    y1, y2 = r.choice([(2022, 2024), (2021, 2023), (2020, 2025)])
    exact = diff * 100 % new == 0 and diff * 100 // new == wb
    wrong = f"（{cm(base)}−{cm(new)}）÷{cm(new)}×100 {'＝' if exact else '≒'} {wb}　答え：{'' if exact else '約'}{wb}%減少"
    fix = f"（{cm(base)}−{cm(new)}）÷{cm(base)}×100＝{p}　答え：{p}%減少"
    return desc(f"{place}の年間来場者数は、{y1}年の{cm(base)}人から{y2}年には{cm(new)}人に減った（架空の資料）。減少率を求める問題で、ある生徒は次のように答えた。\n［ある生徒の解答］\n{wrong}\nこの解答の誤りを指摘し、正しく求め直しなさい。",
                fix, f"減少率の分母は元の値（{y1}年の{cm(base)}人）である。{cm(diff)}÷{cm(base)}×100＝{p}（%）。",
                [("分母の誤りを指摘している", 2), ("正しい式を立てている", 2), ("正しい減少率を求めている", 2)], d=3, p=6, lines=5,
                ap="変化率の分母は「比べるもとになる値（元の値）」。生徒の式の分母が元の値かどうかを確かめる。",
                steps=[f"差を求める：{cm(base)}−{cm(new)}＝{cm(diff)}。", f"元の値で割る：{cm(diff)}÷{cm(base)}×100＝{p}。", f"生徒は新しい値 {cm(new)} で割っているので誤り。正しくは{p}%減少。"],
                alt=[f"{cm(base)}×(1−{p}/100)＝{cm(new)} となることを確かめて逆算する。"],
                pc=[("分母の誤りの指摘", 2), ("正しい式", 2), ("正しい答え", 2)],
                pit=["新しい値で割って変化率を求める。"],
                err=dict(sol=wrong, step="分母に新しい値を使った箇所", type="calculation", tempt="式の中で目に入った小さいほうの数値（新しい値）で割ってしまった。", fix=fix),
                chk=(f"({base}-{new})/{base}*100", str(p), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_over(r):
    s = r.choice(SETS)
    wrong, why, fix = r.choice(s["over"])
    return desc(f"{shead(s)}\n資料からわかることを英語で書く課題で、ある生徒は次のように書いた。\n［ある生徒の解答］\n{wrong}\nこの解答の問題点を、資料の数値や書き手の発言に触れて指摘し、資料から言える範囲の英文に直しなさい。",
                f"問題点：{why}　書き直しの例：{fix}",
                "資料から言えるのは、表の数値とそれから計算できる内容、書き手が実際に述べた内容までである。因果・全体への一般化・将来の予測は、根拠がなければ言えない。",
                [("問題点（因果の取り違え・一般化・計算の誤りなど）を指摘している", 2), ("資料の数値や発言を根拠に示している", 2), ("資料から言える範囲の英文に直している", 2)], d=4, p=6, lines=6, stim=sstim(s),
                ap="生徒の英文の中の強い語（proves / causes / every / most / will / the same）に印をつけ、資料のどの数値・発言がそれを支えているか（支えていないか）を確かめる。",
                steps=["生徒の英文が、資料のどの数値・発言にもとづいているかを確かめる。", f"問題点を特定する：{why}", f"資料から言える範囲に書き直す：{fix}"],
                alt=["書き直した英文の各語句について、表のどの欄、本文のどの文で確かめられるかを指し示して点検する。"],
                pc=[("問題点の指摘", 2), ("根拠の提示", 2), ("書き直し", 2)],
                pit=["相関を因果として述べる。", "一部の集団・一人の発言を全体に広げる。"],
                err=dict(sol=wrong, step="資料の範囲を越えた結論", type="interpretation", tempt="数値の変化や書き手の発言を、そのまま一般的な結論や原因の説明として受け取った。", fix=fix))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_fo_err(r):
    sent, kind, reason, tempt = r.choice(FO)
    wrong_kind = "事実" if kind == "opinion" else "意見"
    right_kind = "意見" if kind == "opinion" else "事実"
    wrong = f"{wrong_kind}である。（この生徒の考え：{tempt}）"
    fix = f"{right_kind}である。{reason}"
    return desc(f"次の英文が事実と意見のどちらを述べているかを判断する問題で、ある生徒は「{wrong_kind}」と答えた。\n{sent}\nこの判断の誤りを指摘し、正しい判断とその理由を答えなさい。",
                fix, f"事実か意見かは、数値の有無や言い方の強さではなく、記録・調査・発言で確かめる方法があるかで決める。{reason}",
                [("生徒の判断の根拠が不適切であることを指摘している", 2), ("正しく判断している", 2), ("判断の理由を説明している", 2)], d=3, p=6, lines=5,
                ap="文を「確かめられる部分」と「書き手の評価・推測・提案の部分」に分け、文全体が何を伝えているかで判断する。",
                steps=["文の中の数値・報告の語（said / predicted / complained）と、評価・推測・提案の語を区別する。", "文全体が「確かめられる内容の報告」か「書き手の判断」かを決める。", f"正しい判断：{fix}"],
                alt=["「この文が正しいかを、どんな資料で確かめられるか」を具体的に言ってみる。言えれば事実、言えなければ意見。"],
                pc=[("誤りの指摘", 2), ("正しい判断", 2), ("理由", 2)],
                pit=["数値の有無や言い方の強さで判断する。"],
                err=dict(sol=wrong, step="事実と意見の判断の根拠", type="concept", tempt=tempt, fix=fix))


GENERATORS = [a_table_calc, a_chart_statement, a_fact_opinion, a_points,
              b_integrate, b_compare, b_doc_fo, b_support,
              c_describe, c_evaluate, c_recommend,
              d_calc_err, d_over, d_fo_err]
