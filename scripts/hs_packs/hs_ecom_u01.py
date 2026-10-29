"""単元パック：英語コミュニケーションⅡ・Ⅲ　論説文・説明文の精読と要旨把握。

段落の役割と論理展開、主張と根拠、要約、文脈からの語の推測を扱う。
本文・例文はすべてこのパックのためのオリジナル英文。例文中の数値・事例は架空のものである。
"""
import re

from banks._common import desc, mc, order, stim
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ECOM-U01"

# ======================================================================
# 授業プリント
# ======================================================================

EX_ROLE = ("[1] Many people assume that the best way to remember new words is to write them out again and again. "
           "[2] Repetition by hand, however, does little to help words stay in long-term memory. "
           "[3] According to researchers who study memory, trying to recall a word before checking the answer strengthens memory far more than copying it. "
           "[4] Admittedly, writing words out can help learners notice their spelling. "
           "[5] Even so, learners who want to remember vocabulary should spend less time copying and more time testing themselves.")

EX_SUM = ("Cities often try to reduce traffic by building wider roads. Unfortunately, wider roads tend to attract more drivers, "
          "and within a few years the traffic is as heavy as before. Some cities have taken the opposite approach: they have "
          "improved buses and trains and made streets safer for walking and cycling. In those cities, many people have chosen "
          "to leave their cars at home. The way to reduce traffic, it seems, is not to make driving easier but to make the alternatives better.")

LESSON = lesson(
    goals=["論説文・説明文の各段落が文章全体の中で果たす役割（問題提起・定義・原因・根拠・譲歩・解決策・結論）を判断し、論理展開を図にまとめられる。",
           "筆者の主張と、それを支える根拠（数値・事例・研究の知見・体験・たとえ）を区別し、根拠が主張を本当に支えているかを吟味できる。",
           "譲歩（Admittedly / While / Of course … Still）や否定の構文（not A but B / far from / not so much A as B）から筆者の立場を正確に読み取れる。",
           "未知語の意味を、言いかえ・対比・例・因果・語の成り立ちの手がかりから推測し、具体例を除いた要約を日本語と英語で書ける。"],
    duration=50,
    readiness=["パラグラフの主題文・支持文とディスコースマーカーの働きを理解している（HS-ENG-U09）。",
               "関係詞・分詞・比較など、高校1年で学んだ構文を使って1文の構造をとらえられる（HS-ENG-U01〜U08）。",
               "日本語で文章の要旨を60〜80字程度にまとめた経験がある。"],
    flow=[("導入：主張はどこにあるか", 5, "Admittedly の文と Even so の文を比べ、筆者の立場はどちらかを考えさせる"),
          ("段落の役割と論理展開", 12, "8つの役割を確認し、短い文章の各文に役割を書きこむ（例題1）"),
          ("主張と根拠・譲歩の構文", 10, "根拠の5つの種類と、譲歩・否定の構文の読み方を整理する"),
          ("語の推測", 9, "文脈の5つの手がかりで未知語の意味を絞りこむ（例題2）"),
          ("要約の手順", 10, "段落の要点 → 論理でつなぐ → 一般化して圧縮する手順で要約する（例題3）"),
          ("まとめと確認", 4, "確認問題3問、問題プリントの課題指示")],
    sections=[
        intro("in1", "精読とは「筆者の論理を再構成する」読み方である",
              "英語コミュニケーションⅡ・Ⅲで読む論説文は、1段落が長く、筆者が反対の立場をいったん認めてから自説を述べるなど、論理の運びが複雑になる。1文ずつ訳せても、どの文が主張で、どの文がその根拠で、どの文が譲歩なのかを区別できなければ、要旨は取れない。この単元では、段落の役割・主張と根拠・語の推測・要約の4つの技能を、1つの手順として身につける。",
              bullets=["段落ごとに「この段落は文章全体の中で何をしているか」を一言で書く。",
                       "主張（筆者が読者に受け入れてほしい考え）と根拠（それを支える材料）を分ける。",
                       "譲歩の後ろの but / still / even so に筆者の本当の立場が来る。",
                       "未知語は辞書を引く前に、文脈から意味の方向を推測する。"],
              points=[tp("例題1の[4]と[5]だけを板書し、「筆者はどちらの立場か」を問う。", ask="Admittedly で始まる文は筆者の主張か。",
                         expect="主張ではない。いったん相手の言い分を認め、Even so の後ろで自分の主張を述べている。", timing="導入の冒頭"),
                      tp("高1の長文読解（HS-ENG-U09）との違いは「段落の役割が増える」「根拠の質を吟味する」「語を推測する」の3点であると最初に示す。")]),
        definition("df1", "段落の役割（8種類）",
                   "論説文の段落は、文章全体の主張に対して次のいずれかの役割を果たす。1つの段落が2つの役割を兼ねることもあるが、そのときは「主たる役割」を決める。",
                   bullets=["話題の導入と問題提起：一般的な考えや現状を示し、問いを立てる（… But is this really true?）。",
                            "中心となる概念の定義・説明：What we call X is … / X, often called Y, occurs when …",
                            "問題の原因の分析：Part of the reason lies in … / Several factors have contributed to …",
                            "主張を裏づける研究・事例の提示：In several studies … / Research suggests …",
                            "利点の説明：X has clear advantages. / Another benefit is …",
                            "反対の立場への譲歩と論点の限定：Admittedly … / This is not to say that … / Of course …",
                            "解決策・対応の紹介：In response, … / For this reason, many … now …",
                            "結論・筆者の主張のまとめ：The lesson, then, is … / In the end … / Nonetheless, …"],
                   conditions=["役割は段落の最初の1〜2文と、前後の段落とのつながりで判断する。",
                               "段落の中に具体例があっても、その段落の役割が「具体例」とは限らない。例が何を裏づけているかを考える。"],
                   points=[tp("8つの役割を、典型的な書き出しの表現と一緒にカードにして配り、本文の段落に貼らせる活動を行う。", caution="「具体例が入っている＝具体例の段落」と判断する生徒が多い。例が支えている主張を先に言わせる。")]),
        theorem("th1", "主張と根拠・譲歩の構文",
                "主張＝筆者が読者に受け入れてほしい考え（should / need to / the key is / what matters is）　根拠＝①統計・調査の数値 ②具体的な事例 ③専門家・研究の知見 ④筆者自身の体験 ⑤たとえ（類推）　譲歩＝Admittedly / Of course / While … ＋ but / still / even so / nonetheless の後ろが主張",
                ["根拠は主張と同じ方向を向いていなければならない。反対の立場を支える事実は、譲歩の材料である。",
                 "not A but B / not so much A as B / far from A / rather than A では、A は筆者が退ける考えで、主張は B（または A の否定）である。",
                 "may / tend to / suggest / it seems などのぼかし（hedging）は、主張の強さを限定している。選択肢の always / never / all は言いすぎを疑う。"],
                body="論説文を読むときは、各文を「主張」「根拠」「譲歩」「背景」に分類しながら読む。主張を見つけたら「なぜそう言えるのか」と問い、その答えになっている文が根拠である。根拠の種類がわかると、その根拠が主張をどの程度強く支えているかも判断できる。",
                points=[tp("同じ主張（例：朝食は集中力を高める）を5種類の根拠で支える英文を示し、どれが最も説得力があるかを話し合わせる。",
                           ask="筆者自身の体験だけで主張を支えるとき、どんな弱点があるか。", expect="一人の例なので、ほかの人にも当てはまるとは限らない。")]),
        derivation("dv1", "未知語の推測と要約の手順（なぜその手がかりで意味が決まるのか）",
                   ["① 語の推測1（言いかえ・定義）：that is / in other words / , known as … / コンマやダッシュではさまれた同格は、未知語を別の言葉で説明している。だから説明の部分がそのまま意味になる。",
                    "② 語の推測2（対比）：but / rather than / unlike / instead の前後は反対の内容になる。反対側の意味がわかれば、未知語の意味は「その逆」に絞れる。",
                    "③ 語の推測3（例・因果）：such as / for example の後ろの例をまとめた上位概念が未知語の意味になる。so … that / because の前後では、結果から原因の語の意味を逆算できる。",
                    "④ 語の推測4（語の成り立ち）：un- / in- / im-（否定）、re-（再び）、-able（～できる）、-ly（副詞）などから品詞と意味の方向を決める。最後に推測した意味を文に戻して、文意が通るかを確かめる。",
                    "⑤ 要約1：各段落の役割と要点を一文で書く。根拠の段落は「何を示すための根拠か」だけを残し、例の細部（人名・数値・場所）は捨てる。",
                    "⑥ 要約2：譲歩の段落は「～という面もあるが」と従属的に扱い、主張の段落と結論を中心に、論理の接続（～なので／～だが）で要点をつなぐ。",
                    "⑦ 要約3：具体的な語を上位の語に言いかえて圧縮し（cars, buses and trains → 交通手段）、字数・語数に合わせて調整する。本文にない判断や情報が入っていないかを最後に点検する。"],
                   body="語の推測が成り立つのは、論説文の筆者が読者に誤解されないよう、重要な語を言いかえ・対比・例で説明しながら書くからである。また、要約で具体例を捨ててよいのは、例は主張を支える材料であって、例を別のものに変えても主張は変わらないからである。",
                   points=[tp("同じ未知語（例：deliberately）を含む文を、手がかりのある文と手がかりのない文の2通りで示し、手がかりがあると意味が絞れることを体験させる。",
                              ask="手がかりがないとき、どこまで推測できるか。", expect="-ly から副詞であることと、文の中での役割まではわかる。", timing="手順④の説明時")]),
        example("ex1", "例題1　段落の中の文の役割",
                f"次の英文の[1]〜[5]の役割を「背景（一般的な考え）・主張・根拠・譲歩・結論」から選び、筆者の主張を日本語で答えなさい。\n{EX_ROLE}",
                ["[1] Many people assume … は一般的な考え（背景）。筆者はこれを[2]の however で否定する。",
                 "[2] 筆者の主張（手で何度も書いても長期記憶にはあまり役立たない）。",
                 "[3] According to researchers … は専門家・研究の知見による根拠。",
                 "[4] Admittedly … は譲歩（書くことにはつづりに気づく利点もある）。",
                 "[5] Even so … は結論（書き写す時間を減らし、自分をテストする時間を増やすべきだ）。"],
                "[1] 背景　[2] 主張　[3] 根拠　[4] 譲歩　[5] 結論　主張：単語は何度も書き写すより、答えを見る前に思い出そうとする（自分をテストする）ほうが記憶に残るので、テストする時間を増やすべきだ。",
                thinking="Many people assume / however / According to / Admittedly / Even so の5つの合図で役割が決まる。",
                points=[tp("[4]を主張と答えた生徒に、[5]の Even so の意味を確認させ、譲歩 → 主張の流れを矢印で示す。")],
                misconceptions=[("Admittedly で始まる[4]が筆者の主張である。", "[4]は譲歩。Even so の後ろの[5]が主張（結論）"),
                                ("[3]の研究者の見解が筆者の主張である。", "[3]は主張[2]を支える根拠（専門家・研究の知見）")]),
        example("ex2", "例題2　未知語の推測",
                "下線部の語の意味を推測し、使った手がかりを説明しなさい。\n(1) Rather than [[u:hoarding]] old magazines, she gives them to the library as soon as she has read them.\n(2) The town's population has been [[u:dwindling]]: twenty years ago it had 8,000 residents, but today it has fewer than 5,000.",
                ["(1) Rather than A, B の対比：B は「読んだらすぐ図書館に寄付する」。A はその反対なので「手放さずにため込む」。",
                 "(2) コロン（:）の後ろが具体的な説明：8,000人 → 5,000人未満。よって「（しだいに）減っている」。",
                 "推測した意味を文に戻して文意が通るかを確かめる。"],
                "(1) ため込む（手がかり：rather than による対比）　(2) しだいに減っている（手がかり：コロンの後ろの数値による説明）",
                thinking="未知語の前後にある rather than / コロン / but / such as などの合図を探し、その合図が示す関係（対比・言いかえ・例）を使う。",
                points=[tp("推測した意味を辞書で確かめ、文脈から推測した意味と辞書の意味がどの程度一致するかを確認させる。", ask="辞書の意味と完全に一致しなくても、読解に支障はあるか。",
                           expect="意味の方向（増える／減る、手放す／ため込む）が合っていれば、文意は取れる。")]),
        example("ex3", "例題3　要約（日本語・英語）",
                f"次の英文の要旨を、具体例を除いて日本語60字以内でまとめなさい。また、英語25語程度でも要約しなさい。\n{EX_SUM}",
                ["1文目：一般的な対策（道路を広げる）＝背景。", "2文目：Unfortunately → その対策は効果が続かない（広い道路はより多くの車を呼ぶ）。",
                 "3・4文目：反対のやり方（公共交通・徒歩・自転車の改善）とその結果＝根拠となる事例。",
                 "5文目：not A but B → 主張：運転を楽にするのではなく、代わりの手段をよくすること。",
                 "具体的な交通手段は「車以外の移動手段」とまとめて圧縮する。"],
                "（日本語）道路を広げても車が増えるだけなので、交通量を減らすには運転を楽にするより車以外の移動手段を充実させるべきだ。（55字）　（英語）Building wider roads does not reduce traffic for long, so cities should improve public transport, walking, and cycling instead of making driving easier.（24語）",
                thinking="not A but B の B が主張。2つのやり方の対比を「～ではなく…」の形で要約に残す。",
                points=[tp("英語の要約では、本文の文をつなぎ合わせるのではなく、主語を Cities などにそろえて1〜2文で言い直させる。", caution="本文の文をそのまま書き写した要約は、語数が多くなり、論理の接続も失われやすい。")]),
        board("bd1", "板書案",
              [("① 段落の役割", ["導入・問題提起", "定義・説明", "原因の分析", "根拠（研究・事例）", "利点", "譲歩・限定", "解決策", "結論"]),
               ("② 主張と根拠", ["主張：should / the key is", "根拠：数値・事例・研究・体験・たとえ", "譲歩 → but / still / even so", "not A but B → 主張は B", "always / never → 言いすぎ注意"]),
               ("③ 推測と要約", ["言いかえ：that is / 同格", "対比：rather than / unlike", "例・因果：such as / so … that", "語の成り立ち：un- re- -able", "要約：要点 → つなぐ → 圧縮"])],
              points=[tp("①の8つの役割は、本文の段落の横に略号（導・定・因・根・利・譲・解・結）で書きこませ、板書と同じ記号を使わせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("本文を読む前に、各段落の第1文だけを読ませて役割を予測させ、読後に答え合わせをする。", ask="第4段落の第1文が Admittedly で始まるとき、この段落の役割は何と予測できるか。", expect="譲歩と論点の限定。"),
               tp("根拠を問う設問では、選択肢が「本文に書かれているか」だけでなく「その主張を支えているか」を確かめさせる。本文にある事実でも、別の主張の根拠であれば誤り。", caution="本文に書かれている＝正解と考える生徒が非常に多い。"),
               tp("語の推測は、推測した意味を文に戻して読ませる「代入チェック」を必ず行わせる。", timing="例題2の後"),
               tp("要約の答案は「具体例・数値が入っていないか」「譲歩を主張にしていないか」「結論と同じ向きか」の3点で相互点検させる。"),
               tp("問題プリント D の誤答例（具体例だけの要約、譲歩を主張とする要約、なじみのある意味での誤推測、別の主張の根拠の取り違え）を、授業の終わりに1つずつ扱う。")],
              misconceptions=[("段落に For example があれば、その段落の役割は「具体例」である。", "例が何を支えているかで役割を決める。研究・事例を示して主張を裏づける段落なら「根拠の提示」"),
                              ("Admittedly / Of course / While で始まる文の内容は筆者の主張である。", "譲歩。後ろの but / still / even so / nonetheless に筆者の主張がある"),
                              ("本文に書かれている事実なら、どの主張の根拠としても正しい。", "根拠は特定の主張を支える。別の主張（譲歩など）を支える事実は根拠として不適切"),
                              ("知っている語は、いつも知っている意味で読めばよい。", "fixed（固定された）、concentrated（集中した）のように、文脈によって意味が変わる語は文脈から確かめる")]),
        summary("sm1", "まとめ",
                ["段落の役割（導入・定義・原因・根拠・利点・譲歩・解決策・結論）を書きこみ、論理展開を図にする。",
                 "主張と根拠を分け、根拠の種類と、根拠が主張と同じ向きかを確かめる。譲歩・否定の構文では、筆者が退ける考えと主張を区別する。",
                 "未知語は言いかえ・対比・例・因果・語の成り立ちから推測し、文に戻して確かめる。",
                 "要約は、段落の要点を論理でつなぎ、具体例を捨て、上位の語に言いかえて圧縮する。"]),
        check("ck1", "確認問題",
              [("Far from solving the problem, the plan made it worse. の筆者の判断を日本語で答えなさい。", "その計画は問題を解決するどころか、悪化させた（計画は失敗だった）。"),
               ("The lake was so [[u:shallow]] that we could walk across it without getting our knees wet. の下線部の意味を推測し、手がかりを答えなさい。", "浅い。so … that の結果（ひざもぬらさずに歩いて渡れた）から推測できる。"),
               ("要約で、譲歩の段落の内容はどのように扱うか。", "主張の中心にはせず、「～という面もあるが」と従属的に扱うか、字数が少なければ省く。")]),
    ])


# ======================================================================
# 本文（オリジナル）
# ======================================================================

ROLES = {
    "intro": "話題の導入と問題提起",
    "definition": "中心となる概念の定義・説明",
    "cause": "問題の原因の分析",
    "evidence": "主張を裏づける研究・事例の提示",
    "benefit": "利点の説明",
    "concession": "反対の立場への譲歩と論点の限定",
    "solution": "解決策・対応の紹介",
    "conclusion": "結論・筆者の主張のまとめ",
}
ROLE_ORDER = list(ROLES)
ORD = ["第1", "第2", "第3", "第4", "第5"]

PASSAGES = [
    dict(key="DARK", title="Darkness Worth Saving",
         paras=["For most of human history, nights were dark. Once the sun went down, people relied on fire, candles, and the moon, and above them the sky was crowded with stars. Today, however, a large share of the world's population lives under skies so bright that the Milky Way can no longer be seen. We rarely think of this change as a problem. After all, light makes streets safer and allows cities to stay active around the clock. But is more light always better?",
                "A growing body of research suggests that artificial light at night can disturb wildlife. Many birds that migrate at night use the stars to find their way, and brightly lit buildings can confuse them, sometimes causing fatal collisions. On some beaches, newly hatched sea turtles, which normally head toward the brighter horizon over the sea, crawl inland toward streetlights instead and never reach the water.",
                "Humans are affected, too. Our bodies follow a daily rhythm that is set largely by light and darkness. Exposure to bright light late in the evening, especially the bluish light of screens and strong white lamps, can delay the release of melatonin, a hormone that helps us feel sleepy. As a result, people who live and work under constant light may find it harder to get the rest they need.",
                "Admittedly, nobody is suggesting that we should switch off every light. Lighting prevents accidents and helps people feel secure when they walk home at night. The problem is not light itself but light that is wasted: lamps that shine upward into the sky, signs that stay on in empty streets, and offices that are lit long after everyone has gone home.",
                "Fortunately, light pollution is one of the easiest forms of pollution to reduce. Unlike plastic in the ocean, it disappears the moment a switch is turned off. By using shielded lamps that point downward, choosing warmer colors, and turning off lights that no one needs, communities can protect wildlife and human health while keeping their streets safe. Darkness, it turns out, is a resource worth saving."],
         roles=[("intro", "夜が明るくなった現状と「光は多いほどよいのか」という問いを示している", []),
                ("evidence", "渡り鳥の衝突やウミガメの子が海にたどり着けない例で、夜の人工光が野生生物を乱すことを裏づけている", []),
                ("evidence", "夜の明るい光が眠りを促すホルモンの分泌を遅らせることを示し、人間への影響を裏づけている", ["cause", "definition"]),
                ("concession", "照明の必要性を認めたうえで、問題は光そのものではなく無駄な光だと論点を限定している", ["definition"]),
                ("conclusion", "光害は減らしやすいとして、下向きの照明や消灯などで暗さを守るべきだとまとめている", ["solution", "benefit"])],
         main="Because artificial light at night harms both wildlife and people, we should cut wasted light while keeping the light we truly need.",
         main_wrong=[("Newly hatched sea turtles sometimes crawl toward streetlights instead of the sea.", "narrow"),
                     ("Modern cities have changed the way people live and work.", "broad"),
                     ("Since light makes streets safer, cities should install as many lights as possible.", "contra"),
                     ("Every outdoor light should be switched off at night to protect animals.", "over")],
         title_ok="Darkness: A Resource Worth Protecting",
         title_wrong=[("How Sea Turtles Find the Sea", "narrow"), ("A History of Street Lighting", "off"), ("Why Every Light Should Be Switched Off", "over")],
         vocab=[dict(w="fatal", para=1, ok="causing death", clue="collisions（衝突）が結果として何を引き起こすかを考える。sometimes causing … collisions の形から、衝突の重大な結果を表す形容詞だとわかる。",
                     wrongs=[("happening by chance", "偶然かどうかではなく、衝突の結果の重大さを表している。"), ("causing only slight harm", "建物に激突する鳥の話であり、軽い被害では「乱す（disturb）」例として弱すぎる。"),
                             ("very easy to see", "見えやすさは文脈と関係がない。")],
                     tempt="collisions と並んでいるので「よくある」「偶然の」と、事故の起こり方の意味に引きずられた。"),
                dict(w="inland", para=1, ok="away from the sea and toward the land", clue="instead（その代わりに）と never reach the water から、本来向かう海とは反対の方向だとわかる。",
                     wrongs=[("along the edge of the water", "never reach the water（水にたどり着かない）と合わない。"), ("toward the brighter sea", "instead は海に向かう本来の行動の「代わりに」という意味なので逆である。"),
                             ("back into their eggs", "孵化した後の移動の話で、文脈に合わない。")],
                     tempt="in-（中へ）から「水の中へ」と考え、instead と never reach the water を確かめなかった。"),
                dict(w="shielded", para=4, ok="covered so that the light is directed downward", clue="直後の that point downward（下を向いた）が説明になっている。第4段落の lamps that shine upward into the sky（空へ漏れる光）との対比も手がかり。",
                     wrongs=[("much brighter than ordinary", "明るさを増すことは、光を減らすという段落の趣旨と逆である。"), ("painted in warm colors", "warmer colors は別の対策として並べられている。"),
                             ("switched off automatically", "消灯は turning off lights … として別に挙げられている。")],
                     tempt="同じ文の warmer colors や turning off と混同し、直後の that point downward を手がかりにしなかった。")],
         evid=[dict(claim="artificial light at night can disturb wildlife", cpara=1,
                    ok="Some newly hatched sea turtles move toward streetlights instead of the sea.",
                    wrongs=[("Lighting helps people feel secure when they walk home at night.", "照明の必要性を認める譲歩の材料で、野生生物への害を支えていない。"),
                            ("Light pollution disappears as soon as a switch is turned off.", "光害が減らしやすいという別の主張（第5段落）の根拠である。"),
                            ("Bright light in the evening can delay the release of melatonin.", "人間の眠りへの影響の根拠で、野生生物についての主張を支えていない。")]),
               dict(claim="light pollution is one of the easiest forms of pollution to reduce", cpara=4,
                    ok="Unlike plastic in the ocean, it disappears the moment a switch is turned off.",
                    wrongs=[("Many birds that migrate at night use the stars to find their way.", "光が野生生物を乱すという主張の背景で、減らしやすさの根拠ではない。"),
                            ("A large share of the world's population can no longer see the Milky Way.", "夜空が明るくなった現状の説明で、減らしやすさとは関係がない。"),
                            ("Lighting prevents accidents.", "照明を残すべき理由（譲歩）で、光害の減らしやすさを示していない。")])],
         details=[("第2段落によると、ウミガメの子が海にたどり着けないことがあるのはなぜか。", "They crawl toward streetlights instead of the brighter horizon over the sea.",
                   [("They are confused by the stars above the beach.", "星を道しるべにするのは夜に渡る鳥である。"),
                    ("They are hit by birds that migrate at night.", "鳥とウミガメの関係は述べられていない。"),
                    ("They cannot see in complete darkness.", "暗さではなく、陸側の明るい街灯に引き寄せられることが原因である。")]),
                  ("第3段落によると、夜遅くに明るい光を浴びるとどうなることがあるか。", "The body may release a sleep-related hormone later than usual.",
                   [("People may stop needing sleep.", "眠りが不要になるとは書かれていない。休息がとりにくくなると述べている。"),
                    ("The body may produce more melatonin.", "分泌が遅れる（delay）のであり、増えるのではない。"),
                    ("People's eyes may adjust to the dark more quickly.", "目の順応については書かれていない。")]),
                  ("第4段落で、筆者が問題だと考えているのはどのような光か。", "Light that serves no useful purpose",
                   [("All light used at night", "筆者はすべての光を消すべきだとは考えていない（nobody is suggesting …）。"),
                    ("Light that keeps streets safe", "安全のための照明は必要なものとして認めている。"),
                    ("Light from the moon and stars", "月や星の光は昔の夜の描写で、問題とされていない。")])],
         trues=["The writer accepts that some lighting is necessary for safety.", "Bright light late in the evening can make it harder for people to sleep well.",
                "According to the writer, lamps that point downward are one way to reduce light pollution."],
         falses=[("The writer argues that all lights should be turned off at night.", "第4段落で、すべての光を消すべきだと言う人はいないと述べている。"),
                 ("Light pollution is harder to reduce than plastic pollution in the ocean.", "第5段落で、海のプラスチックと違ってスイッチを切ればすぐ消えるので減らしやすいと述べている。"),
                 ("Sea turtles normally move toward the darker land after hatching.", "第2段落で、本来は海の上の明るい水平線に向かうと述べている。"),
                 ("Only animals, not humans, are affected by artificial light at night.", "第3段落で、人間も影響を受けると述べている。")],
         summary="夜の人工光は、渡り鳥やウミガメなどの野生生物を乱し、人間の眠りも妨げる。照明は安全のために必要だが、問題は無駄な光なので、下向きの照明や不要な消灯によって減らし、暗さを守るべきだ。",
         skeys=[("野生生物と人間の両方への悪影響を述べている", 3), ("照明の必要性を認め、問題は無駄な光だと限定している", 2), ("無駄な光を減らして暗さを守るべきだという主張でまとめている", 3)],
         en_sum="Artificial light at night disturbs wildlife and human sleep. Although some lighting is needed for safety, much of it is wasted, so communities should use downward-facing lamps and turn off unnecessary lights to protect darkness.",
         exqs=[("第4段落の The problem is not light itself but light that is wasted について、筆者がこのように論点を限定しているのはなぜか。前後の段落の内容に触れて日本語で説明しなさい。",
                "第2・3段落で夜の光の害を述べたが、照明は事故を防ぎ人を安心させるので、すべての光を否定すると現実的でない。そこで害の原因を「無駄な光」に限定し、第5段落の「不要な光を減らせば安全を保ったまま害を防げる」という提案につなげるため。"),
               ("第5段落で筆者が、光害を海のプラスチックと比べているのはなぜか。日本語で説明しなさい。",
                "海のプラスチックは一度出ると取り除くのが難しいが、光害はスイッチを切った瞬間に消える。この違いを示して、光害は最も減らしやすい汚染の一つであり、すぐに対策できることを強調するため。")],
         wrong_sum=[("夜に渡る鳥は星を頼りに飛ぶので、明るい建物に混乱して衝突することがあり、ウミガメの子も街灯に向かってしまう。", "第2段落の根拠となる事例だけをまとめており、人間への影響や筆者の主張（無駄な光を減らして暗さを守るべきだ）が入っていない。"),
                    ("照明は事故を防ぎ、人が夜道を安心して歩けるようにするので、夜の光はできるだけ多いほうがよい。", "第4段落の譲歩（照明の必要性）を主張と取り違えており、筆者の結論（無駄な光を減らすべきだ）と逆になっている。")]),
    dict(key="MULT", title="The Myth of Multitasking",
         paras=["Many of us are proud of our ability to do several things at once. We answer messages while watching an online lecture, listen to podcasts while writing reports, and check the news while talking with friends. In a busy world, multitasking seems not only useful but necessary. Yet the belief that we can give our full attention to two demanding tasks at the same time is, for the most part, an illusion.",
                "What we call multitasking is usually something else: rapid task switching. When we move from writing an essay to reading a message and back again, the brain does not handle both tasks in parallel. Instead, it repeatedly stops one activity and restarts the other. Each switch takes a small amount of time and mental effort, as we remind ourselves where we were and what we were trying to do.",
                "These small costs add up. In many laboratory experiments, people who are asked to switch between tasks take longer and make more errors than people who complete the same tasks one at a time. Interruptions also make it harder to return to deep thinking. After checking a single notification, a student may need several minutes to regain the concentration needed to solve a difficult math problem.",
                "This is not to say that we can never do two things at once. Walking while talking, or folding laundry while listening to music, causes few problems, because at least one of the activities is so familiar that it requires almost no conscious attention. Difficulties arise when both tasks demand careful thought, such as reading a textbook while following a conversation.",
                "The lesson, then, is not that we should feel guilty about every distraction, but that we should protect our attention when it matters most. Setting aside blocks of time for a single important task, and putting our phones out of sight during that time, may feel slow at first. In the end, however, doing one thing at a time is often the fastest way to get things done well."],
         roles=[("intro", "同時にいくつものことをこなせるという一般的な考えを示し、それは錯覚だと問題提起している", []),
                ("definition", "マルチタスクの実態は、作業を高速で切り替えることだと説明し直している", ["cause"]),
                ("evidence", "実験で切り替えると時間がかかり誤りも増えることなどを示し、切り替えのコストを裏づけている", ["cause"]),
                ("concession", "なじんだ作業との組み合わせなら同時にこなせると認め、問題を両方が思考を要する場合に限定している", ["definition"]),
                ("conclusion", "大切な場面では注意を守り、一度に一つのことをするのが結局は速いとまとめている", ["solution"])],
         main="Because switching between demanding tasks wastes time and attention, we should focus on one important task at a time.",
         main_wrong=[("Checking a notification can break a student's concentration for several minutes.", "narrow"),
                     ("People today live very busy lives.", "broad"),
                     ("Multitasking is a necessary skill that saves time in a busy world.", "contra"),
                     ("We should never do two things at the same time, even simple ones.", "over")],
         title_ok="Doing One Thing at a Time",
         title_wrong=[("How to Fold Laundry Efficiently", "off"), ("Notifications and Math Problems", "narrow"), ("Never Do Two Things at Once", "over")],
         vocab=[dict(w="illusion", para=0, ok="something that seems true but is not", clue="Yet（しかし）で前の「マルチタスクは必要だと思える（seems）」と対比されている。「そう思えるが実は違うもの」という意味になる。",
                     wrongs=[("a skill that everyone should learn", "Yet の対比から、筆者は前の考えを否定しているので、身につけるべき技能という肯定的な意味にはならない。"),
                             ("a common habit among students", "for the most part（大部分は）で強さを調整しているのは「信念が正しいかどうか」であり、習慣の話ではない。"),
                             ("a task that requires full attention", "the belief … is an illusion の主語は信念（belief）で、作業ではない。")],
                     tempt="直前の give our full attention … tasks に引きずられ、Yet による対比と主語 the belief を確かめなかった。"),
                dict(w="in parallel", para=1, ok="at the same time", clue="直後の Instead, it repeatedly stops one activity and restarts the other（代わりに、一方を止めては他方を再開する）が、in parallel を否定した後の実際の姿になっている。",
                     wrongs=[("one after the other", "Instead の後ろで述べられた「交互に行う」様子そのもので、in parallel はその反対である。"),
                             ("very slowly", "速さではなく、2つの作業が同時か交互かが論点である。"),
                             ("in the correct order", "順序の正しさは文脈と関係がない。")],
                     tempt="parallel を「並べる」と考えて「順番に」と取り、Instead による対比を確かめなかった。"),
                dict(w="regain", para=2, ok="get back something that was lost", clue="re-（再び）＋gain（得る）。通知を確認したことで集中が途切れた後の話なので、「取り戻す」になる。",
                     wrongs=[("lose completely", "re-（再び）と gain（得る）の組み合わせで、失うという意味にはならない。"),
                             ("gain for the first time", "re- は「再び」を表し、集中はもともとあったものである。"),
                             ("share with others", "共有の意味を示す手がかりはない。")],
                     tempt="通知で集中が途切れるという文脈から「失う」と考え、語の成り立ち（re-＋gain）を確かめなかった。")],
         evid=[dict(claim="switching between tasks has hidden costs", cpara=2,
                    ok="In experiments, people who switch between tasks take longer and make more errors.",
                    wrongs=[("Walking while talking causes few problems.", "同時にこなせる場合を認める譲歩の材料で、切り替えのコストを示していない。"),
                            ("Many people answer messages while watching online lectures.", "マルチタスクが広く行われている現状の描写で、コストの根拠ではない。"),
                            ("Setting aside time for a single task may feel slow at first.", "結論の提案についての補足で、切り替えのコストを示していない。")]),
               dict(claim="we can do two things at once when one of them is very familiar", cpara=3,
                    ok="Folding laundry while listening to music causes few problems.",
                    wrongs=[("A student may need several minutes to regain concentration after a notification.", "切り替えのコストの根拠で、同時にこなせる場合を支えていない。"),
                            ("The brain repeatedly stops one activity and restarts the other.", "マルチタスクの実態（切り替え）の説明で、同時にこなせるという主張とは逆向きである。"),
                            ("Reading a textbook while following a conversation is difficult.", "両方が思考を要する場合の例で、同時にこなせない側の事例である。")])],
         details=[("第2段落によると、作業を切り替えるたびに時間と労力がかかるのはなぜか。", "Because we have to remind ourselves where we were and what we were doing.",
                   [("Because the brain handles both tasks at the same time.", "脳は2つの作業を同時に処理しない（does not handle both tasks in parallel）と述べている。"),
                    ("Because the tasks are always too difficult for us.", "作業が常に難しすぎるとは書かれていない。"),
                    ("Because we forget the first task completely.", "完全に忘れるのではなく、どこまで進んだかを思い出す必要があると述べている。")]),
                  ("第3段落の実験について、本文の内容に合うものはどれか。", "Switching between tasks led to slower work and more mistakes.",
                   [("Switching between tasks led to faster work but more mistakes.", "切り替えた人は時間も長くかかっている（take longer）。"),
                    ("People who did one task at a time made more errors.", "誤りが多かったのは切り替えた人である。"),
                    ("Most people were able to do two tasks in parallel.", "同時に処理できたとは述べられていない。")]),
                  ("第4段落によると、2つのことを同時にしても問題が起こりにくいのはどのような場合か。", "When one of the activities needs almost no conscious attention",
                   [("When both activities demand careful thought", "両方が思考を要するときに困難が生じると述べている。"),
                    ("When the activities are done in a quiet room", "場所の静かさについては書かれていない。"),
                    ("When a person feels guilty about distractions", "罪悪感は第5段落の話で、同時にこなせる条件ではない。")])],
         trues=["What people call multitasking is often a quick series of switches between tasks.", "The writer admits that some combinations of activities cause few problems.",
                "The writer recommends keeping phones out of sight while working on an important task."],
         falses=[("The writer says that the brain can handle two demanding tasks in parallel.", "第2段落で、脳は2つの作業を同時に処理しないと述べている。"),
                 ("According to the writer, we should feel guilty about every distraction.", "第5段落で、すべての気晴らしに罪悪感を持つべきだということではないと述べている。"),
                 ("Doing one thing at a time is always slower in the end.", "第5段落で、結局は一度に一つのことをするのが最も速いことが多いと述べている。"),
                 ("Walking while talking is a good example of a difficult combination.", "第4段落で、歩きながら話すことはほとんど問題を起こさない例として挙げられている。")],
         summary="私たちがマルチタスクと呼ぶものの実態は作業の切り替えであり、切り替えるたびに時間と注意が失われる。なじんだ作業との組み合わせは問題ないが、大切な作業では注意を守り、一度に一つのことに集中すべきだ。",
         skeys=[("マルチタスクの実態は作業の切り替えだと述べている", 3), ("切り替えで時間と注意が失われることを述べている", 2), ("大切な作業では一つに集中すべきだという主張でまとめている", 3)],
         en_sum="What we call multitasking is really rapid switching between tasks, which costs time and causes errors. Simple, familiar activities can be combined, but for important work we should focus on one task at a time.",
         exqs=[("第1段落の最後の文で、筆者が for the most part という表現を加えているのはなぜか。第4段落の内容に触れて日本語で説明しなさい。",
                "第4段落で、歩きながら話すなど、一方がほとんど意識を必要としない作業の組み合わせなら同時にこなせると認めているので、「同時にできるという考えはすべて錯覚だ」と言いすぎないよう、主張の範囲を限定するため。"),
               ("第5段落の doing one thing at a time is often the fastest way to get things done well とはどういうことか。第2・3段落の内容に触れて日本語で説明しなさい。",
                "作業を切り替えるたびに、どこまで進んだかを思い出す時間と労力がかかり、誤りも増え、深い集中を取り戻すのにも時間がかかる。そのため、一つの作業に集中するほうが、結果として速く、しかも質の高い仕事ができるということ。")],
         wrong_sum=[("通知を一度確認しただけで、難しい数学の問題を解くための集中力を取り戻すのに数分かかることがある。", "第3段落の具体例だけをまとめており、マルチタスクの実態（切り替え）や筆者の主張（一つに集中すべきだ）が入っていない。"),
                    ("歩きながら話したり、音楽を聞きながら洗濯物をたたんだりできるので、人は二つのことを同時にこなすことができる。", "第4段落の譲歩を主張と取り違えている。筆者は、両方が思考を要する作業は同時にできないと述べ、一つに集中すべきだと結論づけている。")]),
    dict(key="REPA", title="Why Repair Matters",
         paras=["When a phone screen cracks or a toaster stops working, many people today do not even consider fixing it. Buying a new one is often quicker, and sometimes it costs almost the same as a repair. As a result, huge numbers of electronic devices are thrown away every year, many of which could have worked for years longer.",
                "Part of the reason lies in how products are designed. Some devices are held together with glue instead of screws, which makes them difficult to open without damaging them. Spare parts may be hard to find, and repair manuals are often unavailable to ordinary users. In other words, many products are simply not built to be repaired.",
                "Repairing things, however, has clear advantages. Making a new smartphone requires metals that must be mined, as well as large amounts of energy, so keeping an existing device in use for longer reduces the burden on the environment. Repair also creates local jobs, and it can save consumers a considerable amount of money over time.",
                "In response, a movement has grown in many countries to make repair easier. Volunteers run events where people bring broken items and learn to fix them together, and some governments have begun to require manufacturers to keep spare parts available for a certain number of years after a product is sold.",
                "Of course, not every product can or should be repaired. Some old appliances use so much electricity that replacing them with efficient new models is better for the environment. Still, a world in which repair is the normal first choice, rather than the last, would waste far fewer resources. Before throwing something away, it is worth asking a simple question: can this be fixed?"],
         roles=[("intro", "壊れた製品をすぐ買いかえる現状と、大量の電子機器が捨てられている問題を示している", []),
                ("cause", "接着剤で固められた構造や部品・説明書の入手難など、修理しにくい設計が原因だと分析している", ["definition"]),
                ("benefit", "資源とエネルギーの節約、地域の雇用、消費者の出費の削減という修理の利点を説明している", ["evidence"]),
                ("solution", "修理会の活動や部品の保有を義務づける政府の動きなど、修理を容易にする取り組みを紹介している", ["evidence"]),
                ("conclusion", "修理すべきでない製品もあると認めつつ、修理を最初の選択肢にすべきだとまとめている", ["concession", "solution"])],
         main="We should make repair, rather than replacement, the normal first choice, because it saves resources and money.",
         main_wrong=[("Some electronic devices are held together with glue instead of screws.", "narrow"),
                     ("Electronic devices have become an important part of modern life.", "broad"),
                     ("Since buying a new product is quicker, people should replace broken items.", "contra"),
                     ("Every broken product should be repaired, no matter how old it is.", "over")],
         title_ok="Fix It First",
         title_wrong=[("How Smartphones Are Made", "off"), ("Glue Versus Screws", "narrow"), ("Never Buy Anything New", "over")],
         vocab=[dict(w="unavailable", para=1, ok="impossible to get or use", clue="un-（否定）＋available（手に入る）。同じ文の Spare parts may be hard to find と並べられており、修理しにくさの理由になっている。",
                     wrongs=[("easy to understand", "修理しにくい理由を並べた文の中なので、肯定的な意味にはならない。un- は否定を表す。"),
                             ("free of charge", "値段の話は出てこない。"),
                             ("written in a foreign language", "言語の手がかりはない。")],
                     tempt="available を「利用できる」と覚えていても un- の否定を落とし、修理しにくさを述べる文脈と照らし合わせなかった。"),
                dict(w="manufacturers", para=3, ok="companies that make products", clue="政府が「製品の販売後も部品を保有するよう」義務づける相手なので、製品を作って売る側だとわかる。manu-（手）＋factur-（作る）も手がかり。",
                     wrongs=[("people who repair products as volunteers", "ボランティアは同じ段落の前半に出てくる別の主語である。"),
                             ("people who buy products", "購入者に部品の保有を義務づけるのは文脈に合わない。"),
                             ("government officials", "義務づける側が政府で、manufacturers は義務づけられる側である。")],
                     tempt="同じ段落の Volunteers と同じ立場の人だと考え、require A to do（A に～するよう義務づける）の A が誰かを確かめなかった。"),
                dict(w="efficient", para=4, ok="using less energy to do the same work", clue="use so much electricity（電気を多く使う）古い家電と対比されている。新しい型にすると環境によいのだから、電気をあまり使わないという意味になる。",
                     wrongs=[("larger and more powerful", "電気を多く使う古い家電との対比なので、大きく強力という意味では環境によい理由にならない。"),
                             ("cheaper to buy", "購入価格の話ではなく、電気の使用量の話である。"),
                             ("easier to repair", "修理のしやすさは、この文の比較の観点ではない。")],
                     tempt="「新しい型」という言葉から性能が高い（強力な）製品を思い浮かべ、use so much electricity との対比を確かめなかった。")],
         evid=[dict(claim="many products are not built to be repaired", cpara=1,
                    ok="Some devices are held together with glue, which makes them hard to open without damage.",
                    wrongs=[("Repair creates local jobs.", "修理の利点の根拠で、修理しにくい設計を示していない。"),
                            ("Some old appliances use a great deal of electricity.", "修理すべきでない製品もあるという譲歩の根拠である。"),
                            ("Volunteers run events where people learn to fix broken items.", "修理を容易にする取り組みの例で、設計の問題を示していない。")]),
               dict(claim="keeping an existing device in use reduces the burden on the environment", cpara=2,
                    ok="Making a new smartphone requires mined metals and a large amount of energy.",
                    wrongs=[("Buying a new device is often quicker than repairing it.", "人々が買いかえを選ぶ理由で、環境への負担の根拠ではない。"),
                            ("Repair manuals are often unavailable to ordinary users.", "修理しにくい原因の説明である。"),
                            ("A repair sometimes costs almost the same as a new product.", "買いかえが選ばれる理由で、環境の話ではない。")])],
         details=[("第1段落によると、多くの人が壊れた製品を修理しようとしない理由は何か。", "Replacing it is often faster and may cost about the same.",
                   [("Repair is against the law in many countries.", "修理が違法だとは書かれていない。"),
                    ("New products always last longer than repaired ones.", "新品のほうが長持ちするとは書かれていない。"),
                    ("Repair always costs much more than a new product.", "ほぼ同じ費用になることがあると述べており、always much more は言いすぎである。")]),
                  ("第4段落で紹介されている政府の取り組みはどれか。", "Requiring companies to keep spare parts available for some years",
                   [("Running events where people fix items together", "修理会を運営するのはボランティアである。"),
                    ("Banning the use of glue in all devices", "接着剤の禁止は述べられていない。"),
                    ("Paying people to buy new appliances", "買いかえへの補助は述べられていない。")]),
                  ("第5段落によると、古い家電を新しいものにかえたほうがよいのはどのような場合か。", "When the old appliance uses a lot of electricity",
                   [("When the old appliance is held together with glue", "接着剤は修理しにくさの原因として第2段落に出てくる話である。"),
                    ("When a repair takes more than one day", "修理にかかる日数は述べられていない。"),
                    ("When spare parts are available", "部品が手に入るなら、むしろ修理しやすい。")])],
         trues=["Some products are difficult to open without damaging them.", "The writer admits that replacing some products can be better for the environment.",
                "In some countries, governments have started to make repair easier."],
         falses=[("The writer believes every product should be repaired.", "第5段落で、修理できない・すべきでない製品もあると認めている。"),
                 ("Repairing a device usually increases the burden on the environment.", "第3段落で、使い続けることで環境への負担が減ると述べている。"),
                 ("Repair manuals are easy for ordinary users to get.", "第2段落で、一般の利用者は手に入らないことが多いと述べている。"),
                 ("Repair events are run by manufacturers to sell new products.", "第4段落で、修理会を運営するのはボランティアだと述べている。")],
         summary="修理しにくい設計のために多くの製品がすぐ捨てられているが、修理には資源とお金の節約などの利点がある。買いかえたほうがよい製品もあるが、修理を最初の選択肢にすべきだ。",
         skeys=[("修理しにくい設計のために製品が捨てられている現状・原因に触れている", 2), ("修理の利点（資源・お金の節約など）を述べている", 3), ("修理を最初の選択肢にすべきだという主張でまとめている", 3)],
         en_sum="Many devices are thrown away because they are hard to repair, yet repair saves resources and money. Although some old products are better replaced, repair should become our normal first choice.",
         exqs=[("第5段落の a world in which repair is the normal first choice, rather than the last とはどのような世界か。現在の状況と対比して日本語で説明しなさい。",
                "現在は、壊れたらまず買いかえを考え、修理は最後の手段か、考えもしない。これに対して、物が壊れたらまず修理できないかを考え、買いかえはそれができないときに選ぶ世界のこと。"),
               ("第2段落の In other words 以下で、筆者は第2段落の内容をどのようにまとめているか。そのまとめに至る理由を3つ挙げて日本語で説明しなさい。",
                "多くの製品はそもそも修理されるように作られていない、とまとめている。理由は、①接着剤で固められていて壊さずに開けにくい、②交換部品が見つけにくい、③修理説明書が一般の利用者には手に入らないことが多い、の3つである。")],
         wrong_sum=[("接着剤で固められた機器は壊さずに開けるのが難しく、交換部品や説明書も手に入りにくい。", "第2段落の原因の説明だけをまとめており、修理の利点や筆者の主張（修理を最初の選択肢にすべきだ）が入っていない。"),
                    ("古い家電は電気を多く使うので、新しい効率的な製品に買いかえたほうが環境によい。", "第5段落の Of course に続く譲歩を主張と取り違えている。筆者は Still に続けて、修理を最初の選択肢にすべきだと述べている。")]),
    dict(key="PRAI", title="Praise That Helps Children Grow",
         paras=["Parents and teachers praise children because they want them to feel confident. \"You're so smart!\" seems like a harmless, even helpful, thing to say. However, some psychologists argue that the kind of praise we give matters as much as how often we give it.",
                "Praise that focuses on ability, such as \"You're a natural,\" sends the message that success comes from a fixed quality that a child either has or does not have. Praise that focuses on the process, such as \"You worked hard on that\" or \"You tried a new strategy,\" sends a different message: success comes from things the child can control.",
                "This difference can shape how children respond to difficulty. In several studies, children who had been praised for their intelligence were more likely to avoid challenging tasks afterward, perhaps because failing would suggest that they were not smart after all. Children praised for their effort, by contrast, were more willing to try harder problems and kept going for longer when they struggled.",
                "Process praise is not a magic formula, though. Praising effort that was not actually made, or praising effort alone when a child's strategy is clearly not working, can sound empty and does little to help the child improve. Children are quick to notice when praise is insincere.",
                "The goal, then, is not to stop praising children but to praise them more thoughtfully. Specific, honest comments about the strategies and effort that led to a result help children see that their abilities can grow. In the long run, that belief may be worth more than any compliment about being smart."],
         roles=[("intro", "子どもをほめるのは自信のためだという考えを示し、ほめ方の種類が重要だという問題を提起している", []),
                ("definition", "能力をほめる言葉と過程をほめる言葉が、それぞれどんな考えを子どもに伝えるかを説明している", ["cause"]),
                ("evidence", "能力をほめられた子は難しい課題を避け、努力をほめられた子は挑戦を続けたという研究を示している", ["cause"]),
                ("concession", "実際にはない努力をほめるなど、過程をほめれば何でもよいわけではないと限定している", []),
                ("conclusion", "ほめるのをやめるのではなく、具体的で正直なほめ方をすべきだとまとめている", ["solution"])],
         main="Honest, specific praise for children's effort and strategies, rather than their ability, can help them face challenges.",
         main_wrong=[("Some children avoid difficult tasks after being told they are smart.", "narrow"),
                     ("Parents and teachers play an important role in children's lives.", "broad"),
                     ("Telling children that they are smart is the best way to build their confidence.", "contra"),
                     ("Parents and teachers should stop praising children altogether.", "over")],
         title_ok="Praising the Process, Not the Person",
         title_wrong=[("How Smart Children Solve Problems", "off"), ("Why Children Avoid Hard Tasks", "narrow"), ("Never Praise a Child", "over")],
         vocab=[dict(w="fixed", para=1, ok="unable to change", clue="that a child either has or does not have（あるかないかのどちらか）と説明され、第2段落後半の things the child can control と対比されている。",
                     wrongs=[("repaired after being broken", "「修理された」という意味の fix は文脈に合わない。能力の性質を述べている。"),
                             ("decided by a teacher", "先生が決めるという手がかりはない。"),
                             ("growing quickly", "第5段落の abilities can grow はほめ方を変えた結果の考えで、fixed はその反対の意味である。")],
                     tempt="fix を「修理する」の意味で覚えていたため、同じ文の either has or does not have を手がかりにしなかった。"),
                dict(w="struggled", para=2, ok="had difficulty", clue="kept going for longer when they struggled（～のときも長く続けた）の形と、前の try harder problems から、難しい問題で苦労している場面だとわかる。",
                     wrongs=[("succeeded easily", "kept going（やめずに続けた）が意味をもつのは、うまくいかない場面である。"),
                             ("felt proud", "誇りを感じる場面で「続けた」ことを強調する理由がない。"),
                             ("argued with friends", "友人との口論の手がかりはない。")],
                     tempt="struggle を「戦う」とだけ覚えていて、問題を解く文脈では「苦労する」になることを考えなかった。"),
                dict(w="insincere", para=3, ok="not honest or not truly meant", clue="in-（否定）＋sincere（心からの）。前の文の sound empty（中身がないように聞こえる）と、実際にはしていない努力をほめる例が言いかえになっている。",
                     wrongs=[("very detailed", "具体的なほめ方は第5段落で勧められているもので、子どもが見抜く悪いほめ方とは逆である。"),
                             ("given too late", "時機の手がかりはない。"),
                             ("spoken loudly", "声の大きさの手がかりはない。")],
                     tempt="in- を「中へ」と取り違え、前の文の sound empty との言いかえ関係を確かめなかった。")],
         evid=[dict(claim="the type of praise can shape how children respond to difficulty", cpara=2,
                    ok="Children praised for intelligence were more likely to avoid hard tasks, while those praised for effort tried harder problems.",
                    wrongs=[("Parents praise children because they want them to feel confident.", "ほめる目的の説明（背景）で、ほめ方による違いを示していない。"),
                            ("Children are quick to notice when praise is insincere.", "過程をほめる場合の注意点（譲歩）の根拠である。"),
                            ("\"You're so smart!\" seems like a harmless thing to say.", "筆者が問い直す一般的な考えで、根拠ではない。")]),
               dict(claim="process praise is not a magic formula", cpara=3,
                    ok="Praising effort that was not really made can sound empty.",
                    wrongs=[("Children praised for effort kept going for longer when they struggled.", "過程をほめる効果を示す根拠で、限界を示していない。"),
                            ("Praise that focuses on ability sends the message that success is fixed.", "能力をほめることの問題点の説明である。"),
                            ("Honest comments help children see that their abilities can grow.", "結論の主張で、限界の根拠ではない。")])],
         details=[("第2段落によると、過程をほめる言葉は子どもにどのような考えを伝えるか。", "Success comes from things the child can control.",
                   [("Success depends on a quality the child was born with.", "能力をほめる言葉が伝える考えである。"),
                    ("Success comes mainly from good luck.", "運については書かれていない。"),
                    ("Success is not important at all.", "成功が重要でないとは書かれていない。")]),
                  ("第3段落で、知能をほめられた子どもが難しい課題を避けた理由として、筆者が推測していることは何か。", "Failing might show that they were not smart after all.",
                   [("They were too tired after the first task.", "疲れについては書かれていない。"),
                    ("Their parents told them not to try.", "親の指示については書かれていない。"),
                    ("They thought the tasks were too easy.", "易しすぎると考えたとは書かれていない。")]),
                  ("第5段落で、筆者が勧めているほめ方はどれか。", "Specific, honest comments on the strategies and effort that led to a result",
                   [("Frequent comments about how smart the child is", "知能をほめる言葉で、筆者が問題にしているほめ方である。"),
                    ("Praise for effort even when no effort was made", "第4段落で、中身がないように聞こえると述べている。"),
                    ("No praise at all, so that children work harder", "ほめるのをやめるのではないと述べている。")])],
         trues=["Some psychologists believe the type of praise is as important as how often it is given.", "Children can tell when praise is not sincere.",
                "The writer does not want parents and teachers to stop praising children."],
         falses=[("Children praised for their intelligence were more willing to try harder problems.", "第3段落で、挑戦に前向きだったのは努力をほめられた子だと述べている。"),
                 ("According to the writer, praising effort always helps children improve.", "第4段落で、過程をほめれば必ずうまくいくわけではないと述べている。"),
                 ("The writer says that \"You're so smart!\" is completely harmless.", "第1段落でそう思われていることを紹介し、筆者はそれを問い直している。"),
                 ("Process praise sends the message that ability cannot change.", "第2段落で、成功は自分で左右できることから生まれると伝えると述べている。")],
         summary="能力をほめると子どもは失敗を恐れて挑戦を避けやすいが、努力や工夫をほめると困難に粘り強く取り組む。中身のない称賛は逆効果なので、具体的で正直に過程をほめるべきだ。",
         skeys=[("能力をほめると挑戦を避けやすいことを述べている", 3), ("中身のない称賛は効果がないという限定に触れている", 2), ("具体的で正直に努力・過程をほめるべきだという主張でまとめている", 3)],
         en_sum="Praising children for their intelligence may make them avoid challenges, while praising their effort and strategies helps them keep trying. Such praise should be specific and honest, not empty.",
         exqs=[("第3段落の perhaps because failing would suggest that they were not smart after all について、知能をほめられた子どもがこのように感じるのはなぜか。第2段落の内容に触れて日本語で説明しなさい。",
                "知能をほめる言葉は、成功が生まれつきの変わらない能力から生まれるという考えを伝える。そう信じている子どもにとって、失敗することは自分にその能力がない証拠になってしまうので、失敗の可能性がある難しい課題を避けるようになるから。"),
               ("第5段落の that belief が指す内容を明らかにし、筆者がそれを「賢いというほめ言葉よりも価値がある」と考える理由を日本語で説明しなさい。",
                "that belief は「自分の能力は伸ばすことができる」という信念を指す。この信念があれば、子どもは失敗を恐れずに難しい課題に挑戦し、苦労しても粘り強く続けられるので、一時的な自信を与えるだけの「賢い」というほめ言葉よりも長い目で見て役に立つから。")],
         wrong_sum=[("いくつかの研究では、知能をほめられた子どもは、その後、難しい課題を避ける傾向があった。", "第3段落の研究結果の一部だけをまとめており、ほめ方の違いの意味や筆者の主張（具体的で正直に過程をほめるべきだ）が入っていない。"),
                    ("努力をほめても中身がないと子どもに見抜かれるので、子どもをほめるのはやめたほうがよい。", "第4段落の限定を主張と取り違え、言いすぎている。筆者は第5段落で、ほめるのをやめるのではなくほめ方を工夫すべきだと述べている。")]),
    dict(key="TOUR", title="When Visitors Become Too Many",
         paras=["Tourism brings money and jobs to many communities, and for some towns it is the most important industry of all. In recent years, however, a number of popular destinations have begun to suffer from a problem that once seemed unimaginable: too many visitors.",
                "This situation, often called overtourism, occurs when the number of visitors exceeds what a place can comfortably handle. Narrow streets become so crowded that residents struggle to get to work, buses are too full for local people to board, and rents rise as apartments are turned into short-term rentals for tourists.",
                "Several factors have contributed to the problem. Cheaper flights have made travel affordable for more people, and social media encourages visitors to go to the same famous spots to take the same photographs. Because tourists tend to arrive at the same places at the same times, the pressure is concentrated rather than spread out.",
                "Some cities have started to respond. A few charge an entry fee on the busiest days, others limit the size of tour groups, and many promote less famous neighborhoods and off-season visits in order to spread visitors more evenly across places and times.",
                "Such measures will not satisfy everyone, and businesses that depend on tourism may worry about losing income. Yet the aim is not to stop people from traveling. It is to make sure that the places people love to visit remain places where people can also live. Travelers, too, can help by visiting at quieter times and treating each destination as someone's home."],
         roles=[("intro", "観光は地域に利益をもたらすが、訪問者が多すぎるという問題が生じていると提起している", []),
                ("definition", "オーバーツーリズムとは何かを定義し、住民の生活への具体的な影響を説明している", ["cause", "evidence"]),
                ("cause", "安い航空運賃やSNSなど、観光客が同じ場所・時期に集中する原因を分析している", []),
                ("solution", "入域料や団体の人数制限、分散の促進など、都市の対応を紹介している", ["evidence"]),
                ("conclusion", "反対の声も認めつつ、目的は観光を止めることではなく住める場所を守ることだとまとめている", ["concession", "solution"])],
         main="Because too many visitors can make popular places hard to live in, cities and travelers need to spread tourism more evenly.",
         main_wrong=[("Social media encourages tourists to take the same photographs.", "narrow"),
                     ("Travel has become an important part of modern life.", "broad"),
                     ("Since tourism brings money, cities should attract as many visitors as possible.", "contra"),
                     ("People should stop traveling to famous places altogether.", "over")],
         title_ok="Keeping Popular Places Livable",
         title_wrong=[("The Cheapest Ways to Fly", "off"), ("Taking Photos at Famous Spots", "narrow"), ("Why We Should Stop Traveling", "over")],
         vocab=[dict(w="exceeds", para=1, ok="is greater than", clue="overtourism（観光過剰）の定義の文で、over-（超えて）の意味と、後ろの「住民が通勤できないほど混む」という結果から、受け入れられる量を超えるとわかる。",
                     wrongs=[("is equal to", "等しいだけなら、後ろに述べられた混雑の問題は起こらない。"),
                             ("is much smaller than", "訪問者が少ない状況では overtourism にならない。"),
                             ("is measured by", "数を測るという意味では、問題の定義にならない。")],
                     tempt="what a place can comfortably handle（快適に受け入れられる量）と「合う」と考え、over- と後ろの具体的な問題を確かめなかった。"),
                dict(w="affordable", para=2, ok="cheap enough for many people to pay for", clue="Cheaper flights（より安い航空券）が原因で、for more people（より多くの人にとって）旅行が～になった。afford（買う余裕がある）＋-able（～できる）。",
                     wrongs=[("more dangerous", "安い航空券が旅行を危険にするという関係は不自然で、観光客が増える理由にならない。"),
                             ("less interesting", "観光客が増える原因の説明に合わない。"),
                             ("possible only in summer", "季節の手がかりはない。")],
                     tempt="-able を見て「～できる」とだけ考え、主語と原因（Cheaper flights）から意味を絞りこまなかった。"),
                dict(w="concentrated", para=2, ok="gathered in one place", clue="直後の rather than spread out（分散するのではなく）と対比されている。同じ場所・同じ時間に集まるという前半の内容の言いかえでもある。",
                     wrongs=[("paying close attention", "「集中して取り組む」という意味の concentrate は、主語 the pressure（負担）に合わない。"),
                             ("made weaker", "負担が弱まるのなら、問題の原因の説明にならない。"),
                             ("divided equally", "spread out（分散した）とほぼ同じ意味で、rather than による対比と逆になる。")],
                     tempt="concentrate を「（注意を）集中する」とだけ覚えていて、rather than spread out との対比を確かめなかった。")],
         evid=[dict(claim="overtourism makes life difficult for residents", cpara=1,
                    ok="Buses become too full for local people to board.",
                    wrongs=[("Cheaper flights have made travel affordable for more people.", "観光客が増える原因の説明で、住民の生活への影響を示していない。"),
                            ("Tourism brings money and jobs to many communities.", "観光の利点で、住民の困難とは逆向きである。"),
                            ("Some cities charge an entry fee on the busiest days.", "都市の対応の例で、問題そのものの根拠ではない。")]),
               dict(claim="the pressure from tourism is concentrated rather than spread out", cpara=2,
                    ok="Social media encourages visitors to go to the same famous spots.",
                    wrongs=[("Many cities promote less famous neighborhoods.", "集中を和らげる対策で、集中の原因を示していない。"),
                            ("Businesses that depend on tourism may worry about losing income.", "対策への反対の声で、集中の根拠ではない。"),
                            ("Rents rise as apartments are turned into short-term rentals.", "住民への影響の例で、観光客が同じ場所に集まる原因ではない。")])],
         details=[("第2段落で述べられている、オーバーツーリズムが住民に与える影響として本文に合わないものはどれか。", "Local shops close because there are too few customers.",
                   [("Residents find it hard to get to work.", "第2段落で、通りが混んで通勤に苦労すると述べており、本文に合う。"),
                    ("Local people cannot get on crowded buses.", "第2段落で、バスが満員で地元の人が乗れないと述べており、本文に合う。"),
                    ("Rents go up as apartments become tourist rentals.", "第2段落で、家賃が上がると述べており、本文に合う。")]),
                  ("第4段落によると、多くの都市が知名度の低い地区や観光の閑散期の訪問を勧めているのは何のためか。", "To spread visitors more evenly across places and times",
                   [("To earn more money from entry fees", "入域料は一部の都市の別の対策である。"),
                    ("To make tour groups larger", "団体の人数はむしろ制限している。"),
                    ("To stop people from traveling", "第5段落で、目的は旅行を止めることではないと述べている。")]),
                  ("第5段落によると、旅行者自身にできることは何か。", "Visit at quieter times and treat each place as someone's home.",
                   [("Use social media to find famous spots", "SNSは集中の原因として第3段落に出てくる話である。"),
                    ("Stay only in short-term rental apartments", "短期貸しの増加は家賃上昇の原因として述べられている。"),
                    ("Travel only in large tour groups", "団体の規模は制限される側の話である。")])],
         trues=["For some towns, tourism is the most important industry.", "Social media is one reason why visitors gather at the same places.",
                "The writer admits that not everyone will be happy with the new measures."],
         falses=[("The writer thinks that people should stop traveling.", "第5段落で、目的は旅行を止めることではないと述べている。"),
                 ("Overtourism happens when a place has fewer visitors than it can handle.", "第2段落で、受け入れられる量を超えたときに起こると定義している。"),
                 ("Every city now charges tourists an entry fee.", "第4段落で、入域料を取るのは一部（a few）の都市だと述べている。"),
                 ("Cheaper flights have made it harder for people to travel.", "第3段落で、より多くの人が旅行できるようになったと述べている。")],
         summary="安い航空運賃やSNSのために観光客が同じ場所と時期に集中し、住民の生活が損なわれている。観光を止めるのではなく、都市の対策と旅行者の配慮によって訪問を分散させ、住める場所を守るべきだ。",
         skeys=[("観光客の集中が住民の生活を損なっている問題を述べている", 3), ("集中の原因（安い航空運賃・SNSなど）に触れている", 2), ("観光を分散させて住める場所を守るべきだという主張でまとめている", 3)],
         en_sum="Cheap flights and social media send crowds of tourists to the same places at the same times, making life hard for residents. Without stopping travel, cities and visitors should spread tourism out so that these places remain livable.",
         exqs=[("第3段落の the pressure is concentrated rather than spread out とはどういうことか。また、それが第4段落の対策とどのように結びついているか。日本語で説明しなさい。",
                "観光客が同じ場所に同じ時期に集まるため、観光の負担が特定の場所と時間に集中しているということ。第4段落の対策は、知名度の低い地区や閑散期の訪問を勧めるなどして、この集中を場所と時間の両面で分散させようとするものである。"),
               ("第5段落で、筆者は対策の目的をどのように説明しているか。Yet の前後の関係に触れて日本語で説明しなさい。",
                "Yet の前では、対策は観光に頼る事業者などすべての人を満足させるものではないと認めている。そのうえで Yet の後ろで、目的は旅行を止めることではなく、人々が訪れたいと思う場所が、人が住み続けられる場所であり続けるようにすることだと説明している。")],
         wrong_sum=[("混雑のために住民が通勤に苦労し、バスに乗れず、短期貸しの増加で家賃も上がっている。", "第2段落の住民への影響の具体例だけをまとめており、原因や筆者の主張（観光を分散させて住める場所を守るべきだ）が入っていない。"),
                    ("観光は地域にお金と仕事をもたらす最も重要な産業なので、観光客を減らす対策はとるべきではない。", "第1段落の背景と第5段落の反対の声を主張と取り違えており、筆者の結論と逆になっている。")]),
    dict(key="FIRE", title="Fire as a Friend of the Forest",
         paras=["For much of the twentieth century, forest managers in many countries treated every wildfire as an enemy to be defeated as quickly as possible. The goal seemed obvious: fire destroys trees, so preventing fire must protect forests. Ecologists now know that the relationship between fire and forests is far more complicated.",
                "In many forests, small fires are a natural and even necessary event. Low-intensity fires burn away dead leaves, fallen branches, and small plants on the forest floor while leaving most large trees alive. This clears space and returns nutrients to the soil, allowing new plants to grow. Some species have even adapted to depend on fire. Certain pine trees, for example, produce cones that open and release their seeds only after being exposed to intense heat.",
                "When every small fire is put out, however, dead wood and dry plants build up year after year. Eventually, when a fire does start, it has so much fuel that it can grow into a huge, extremely hot blaze that kills even the oldest trees and is almost impossible to control.",
                "For this reason, many forest agencies now use controlled burns: small fires that are set deliberately under careful supervision, usually when the weather is cool and the wind is calm. By reducing the amount of fuel on the forest floor, these planned fires lower the risk of disastrous ones.",
                "Controlled burns are not without risks. Smoke can affect people's health, and on rare occasions a planned fire escapes control. Nonetheless, the lesson of the past century is clear: trying to remove fire completely from forests that evolved with it can make them more dangerous, not less. Protecting forests sometimes means letting them burn."],
         roles=[("intro", "山火事はすべて消すべき敵だという20世紀の考えを示し、実際はもっと複雑だと問題提起している", []),
                ("benefit", "小さな火が地表を片づけ養分を土に返すなど、森にとって必要な役割を果たすことを説明している", ["evidence", "definition"]),
                ("cause", "小さな火をすべて消すと燃料がたまり、手に負えない大火事が起こる仕組みを分析している", ["evidence"]),
                ("solution", "燃料を減らすために計画的に小さな火を入れる「管理された火入れ」を紹介している", ["definition"]),
                ("conclusion", "火入れの危険も認めつつ、火を森から完全になくそうとするとかえって危険になるとまとめている", ["concession"])],
         main="Because small fires are a natural part of many forests, removing fire completely can lead to worse fires, so carefully managed burning can protect forests.",
         main_wrong=[("Certain pine cones open only after being exposed to intense heat.", "narrow"),
                     ("Forests are home to many kinds of plants and animals.", "broad"),
                     ("Every wildfire should be put out as quickly as possible to protect forests.", "contra"),
                     ("Forest fires should always be allowed to burn without any control.", "over")],
         title_ok="Why Some Forests Need Fire",
         title_wrong=[("How Pine Cones Release Their Seeds", "narrow"), ("The Dangers of Smoke", "narrow"), ("Let Every Forest Burn", "over")],
         vocab=[dict(w="blaze", para=2, ok="a large and powerful fire", clue="huge, extremely hot（巨大で非常に熱い）が修飾し、kills even the oldest trees（最も古い木まで枯らす）と続く。燃料が多い火事の話なので、大きな火事だとわかる。",
                     wrongs=[("a small fire on the forest floor", "huge, extremely hot と矛盾する。小さな火は第2段落の低強度の火である。"),
                             ("a pile of dead wood", "枯れ木はこの火の燃料（fuel）であり、火そのものではない。"),
                             ("a group of firefighters", "人を表す手がかりはない。")],
                     tempt="同じ段落に出てくる dead wood（枯れ木）と結びつけ、修飾語 huge, extremely hot を確かめなかった。"),
                dict(w="deliberately", para=3, ok="on purpose", clue="controlled burns の言いかえの中にあり、under careful supervision（注意深い監督のもとで）や後ろの these planned fires（計画された火）が手がかりになる。",
                     wrongs=[("by accident", "planned fires（計画された火）と矛盾する。"),
                             ("very quickly", "速さの手がかりはなく、むしろ天候を選んで慎重に行う。"),
                             ("without permission", "careful supervision（注意深い監督）のもとで行われる。")],
                     tempt="山火事の話なので火は偶然起こるものだと思いこみ、these planned fires との言いかえを確かめなかった。"),
                dict(w="adapted", para=1, ok="changed over time to suit their surroundings", clue="直後の for example 以下（高熱を受けたときだけ種を出す松かさ）が具体例で、火のある環境に合った性質を身につけたことを示している。",
                     wrongs=[("been destroyed completely", "火に依存して種を出す例と矛盾する。"),
                             ("moved to another forest", "移動の手がかりはない。"),
                             ("stopped producing seeds", "例では、熱を受けると種を出すと述べている。")],
                     tempt="火で焼かれる話だと考えて「破壊された」と推測し、for example 以下の例を確かめなかった。")],
         evid=[dict(claim="some species have adapted to depend on fire", cpara=1,
                    ok="Certain pine cones release their seeds only after being exposed to intense heat.",
                    wrongs=[("Smoke from controlled burns can affect people's health.", "火入れの危険（譲歩）の根拠で、生物が火に適応していることを示していない。"),
                            ("Dead wood builds up when every small fire is put out.", "大火事が起こる原因の説明である。"),
                            ("Forest managers once treated every wildfire as an enemy.", "かつての考え方の紹介で、根拠ではない。")]),
               dict(claim="putting out every small fire can make forests more dangerous", cpara=2,
                    ok="Fuel builds up, so a later fire can become huge and almost impossible to control.",
                    wrongs=[("Low-intensity fires leave most large trees alive.", "小さな火が森に害が少ないことの説明で、消火の危険を直接示していない。"),
                            ("Controlled burns are usually set when the wind is calm.", "火入れの方法の説明である。"),
                            ("On rare occasions a planned fire escapes control.", "火入れの危険の根拠で、すべての火を消すことの危険とは別の話である。")])],
         details=[("第2段落によると、低強度の火は森にどのような働きをするか。", "It clears the forest floor and returns nutrients to the soil.",
                   [("It kills most of the large trees.", "大きな木の多くは生き残ると述べている。"),
                    ("It adds more dead wood to the forest floor.", "枯れ葉や落ちた枝を燃やして片づけると述べており、逆である。"),
                    ("It stops new plants from growing.", "新しい植物が育てるようになると述べている。")]),
                  ("第4段落によると、管理された火入れはふつうどのような条件で行われるか。", "When the weather is cool and the wind is calm",
                   [("When the forest floor is completely clear", "燃料を減らすために行うので、地表が片づいていることは条件ではない。"),
                    ("When a large wildfire is already burning", "大火事の危険を下げるために前もって行うものである。"),
                    ("When the weather is hot and dry", "涼しく風の穏やかなときに行うと述べている。")]),
                  ("第5段落で述べられている、管理された火入れの危険はどれか。", "Its smoke can harm people's health.",
                   [("It always grows into a huge blaze.", "制御できなくなるのはまれ（on rare occasions）だと述べている。"),
                    ("It increases the amount of fuel in the forest.", "燃料を減らすために行うと述べている。"),
                    ("It prevents pine cones from opening.", "松かさは熱を受けて開くと述べている。")])],
         trues=["Some pine cones need intense heat to release their seeds.", "Controlled burns are meant to reduce the fuel in a forest.",
                "The writer admits that controlled burns have some risks."],
         falses=[("Low-intensity fires usually kill most of the large trees in a forest.", "第2段落で、大きな木の多くは生き残ると述べている。"),
                 ("Putting out every small fire makes large fires less likely.", "第3段落で、燃料がたまり、手に負えない大火事が起こりやすくなると述べている。"),
                 ("Controlled burns are set without any supervision.", "第4段落で、注意深い監督のもとで行うと述べている。"),
                 ("Ecologists today agree that every wildfire is an enemy of the forest.", "第1段落で、生態学者は関係がもっと複雑だと考えていると述べている。")],
         summary="多くの森では小さな火は自然で必要なものであり、すべての火を消すと燃料がたまって手に負えない大火事を招く。危険もあるが、計画的な火入れで燃料を減らすことが森を守ることにつながる。",
         skeys=[("小さな火が森にとって自然で必要なものだと述べている", 3), ("すべての火を消すと大火事を招くという因果を述べている", 2), ("計画的な火入れが森を守るという主張でまとめている", 3)],
         en_sum="Small fires are a natural and useful part of many forests. Putting out every fire lets fuel build up and leads to huge, uncontrollable fires, so carefully controlled burns can actually protect forests.",
         exqs=[("第5段落の Protecting forests sometimes means letting them burn という逆説的な表現は、どのような意味か。本文の因果関係に即して日本語で説明しなさい。",
                "小さな火をすべて消すと、枯れ木や乾いた植物が燃料としてたまり、いったん火事が起きると最も古い木まで枯らす手に負えない大火事になる。そこで、管理された小さな火で燃料を減らしておくことが、結果として大火事を防ぎ森を守ることになるという意味。"),
               ("第1段落の The goal seemed obvious に続く考え方には、どのような見落としがあったか。第2・3段落の内容に触れて日本語で説明しなさい。",
                "「火は木を枯らすので、火を防げば森を守れる」という考えは、小さな火が地表の枯れ葉などを燃やして養分を土に返し、火に頼って種を出す植物もいるという、火の必要な働きを見落としていた。また、小さな火をすべて消すと燃料がたまり、かえって大火事を招くことも見落としていた。")],
         wrong_sum=[("ある種の松は、高熱を受けたときにだけ松かさが開き、種を放出する。", "第2段落の具体例だけをまとめており、文章全体の主張（計画的な火入れが森を守る）が入っていない。"),
                    ("管理された火入れは煙が健康に影響し、制御できなくなることもあるので、行うべきではない。", "第5段落で認めた危険（譲歩）を主張と取り違えている。筆者は Nonetheless に続けて、火を完全になくそうとするとかえって危険だと結論づけている。")]),
]
PBY = {p["key"]: p for p in PASSAGES}

MAIN_WHY = {
    "narrow": ("本文の一部（具体例や1つの段落の内容）だけを述べており、文章全体の主旨としては狭すぎる。", "具体例と主旨の混同"),
    "broad": ("本文の話題よりも一般的で広すぎる内容で、筆者の主張を表していない。", "話題と主旨の混同"),
    "contra": ("本文の主張と逆の内容である。筆者が退けている一般的な考えや譲歩の内容を、主張と取り違えている。", "譲歩・一般的な考えと主張の混同"),
    "over": ("筆者は譲歩の段落で主張の範囲を限定しており、always / every / never などで範囲を広げたこの選択肢は言いすぎである。", "ぼかし・限定の見落とし（言いすぎ）"),
    "off": ("本文で扱われていない内容である。", "本文にない情報の読みこみ"),
}


def pstim(p):
    return stim(f"EC1-{p['key']}", "\n\n".join(p["paras"]), "passage", f"次の英文（“{p['title']}”）を読んで、あとの問いに答えなさい。", source="オリジナル")


def head(p):
    return f"英文“{p['title']}”について答えなさい。"


def sentence_with(p, para, word):
    for s in re.split(r"(?<=[.!?])\s+", p["paras"][para]):
        if re.search(rf"\b{re.escape(word)}\b", s):
            return re.sub(rf"\b{re.escape(word)}\b", f"[[u:{word}]]", s, count=1)
    raise ValueError(word)


# ======================================================================
# 短文の資料
# ======================================================================

SUPPORT_TYPES = ["統計・調査の数値", "具体的な事例", "専門家・研究の知見", "筆者自身の体験", "たとえ（類推）"]
SUPPORT_DESC = {
    "統計・調査の数値": "調査・記録の数値で、主張の傾向を量的に示す",
    "具体的な事例": "特定の場所・集団で実際に起きた出来事を示す",
    "専門家・研究の知見": "研究者・専門家の見解や研究の結果を示す",
    "筆者自身の体験": "筆者（I）が自分で経験した出来事を示す",
    "たとえ（類推）": "似た構造をもつ別のものになぞらえて説明する",
}
SUPPORT_CUE = {
    "統計・調査の数値": "percent / survey / rose by などの数値表現",
    "具体的な事例": "At one school / In one town などの特定の場所",
    "専門家・研究の知見": "According to researchers / Psychologists have found / Scientists report",
    "筆者自身の体験": "主語 I と過去の出来事",
    "たとえ（類推）": "Just as … / Like … / is like …",
}
SUPPORT = [
    ("Reading for pleasure has become less common among teenagers.", "In one survey of 1,000 high school students, only 28 percent said they had read a book for fun in the past month.", "統計・調査の数値"),
    ("Small changes in a classroom can make a big difference.", "At one school, simply moving desks into small groups led to much more discussion during lessons.", "具体的な事例"),
    ("Breakfast affects how well students concentrate.", "According to researchers who study nutrition, students who skip breakfast tend to lose focus earlier in the morning.", "専門家・研究の知見"),
    ("Studying abroad can change the direction of a person's life.", "When I studied in Spain for a year, I made friends whose way of thinking completely changed my plans for the future.", "筆者自身の体験"),
    ("Roads and railways need regular maintenance.", "Just as the human body needs exercise and rest to stay healthy, transport systems need constant care to keep working.", "たとえ（類推）"),
    ("City parks have become more popular with local residents.", "Last year, the number of visitors to the city's three main parks rose by 15 percent.", "統計・調査の数値"),
    ("Signs in several languages help visitors feel welcome.", "In one town, after signs in English and Chinese were added at the station, tourists said they found their way much more easily.", "具体的な事例"),
    ("Learning works better when it is spread out over time.", "Psychologists have found that studying a little on several days leads to better long-term memory than studying the same amount in one long session.", "専門家・研究の知見"),
    ("Kindness can spread from one person to another.", "Last winter, a stranger helped me push my bicycle up a snowy hill, and the next day I found myself helping an elderly man carry his shopping.", "筆者自身の体験"),
    ("New ideas need time to develop.", "Like seeds planted in soil, new ideas need patience and the right conditions before they produce anything.", "たとえ（類推）"),
    ("Online grocery shopping is growing quickly.", "In our town, the share of households that ordered food online at least once a month doubled from 12 percent to 24 percent in five years.", "統計・調査の数値"),
    ("A good team is more than a group of talented individuals.", "A team is like an orchestra: even the finest musicians sound poor if they do not listen to one another.", "たとえ（類推）"),
    ("Sleep plays an important role in learning.", "Scientists who study the brain report that sleep helps strengthen the memories we form during the day.", "専門家・研究の知見"),
    ("Practicing in front of others reduces nervousness.", "Before my first speech contest, I practiced in front of my family every evening, and on the day of the contest I felt surprisingly calm.", "筆者自身の体験"),
    ("Young people can bring a declining event back to life.", "In one small village, students from a nearby high school took over the planning of a festival that had nearly disappeared, and it now attracts visitors from across the region.", "具体的な事例"),
]

# 論理構造（否定・譲歩・強調）の読み取り：(英文, 正しい読み, [(誤った読み, 理由)], 構文)
LOGIC = [
    ("It is not that young people read less; it is that they read in different ways.", "若者の読書量が減ったのではなく、読み方が変わったのだ。",
     [("若者の読書量は減っており、読み方も変わった。", "It is not that ～ は「～というわけではない」と否定しており、読書量の減少は筆者が退けている考えである。"),
      ("若者は以前と同じやり方で本を読んでいる。", "it is that they read in different ways（読み方が違う）を無視している。"),
      ("若者はもっと多くの本を読むべきだ。", "提案は述べられていない。")], "It is not that A; it is that B"),
    ("Far from saving time, the new booking system made the whole process slower.", "新しい予約システムは時間の節約になるどころか、手続き全体を遅くした。",
     [("新しい予約システムは時間を大幅に節約した。", "far from ～ は「～どころか（少しも～ない）」で、節約したことを否定している。"),
      ("新しい予約システムは時間の節約には不十分だったが、手続きは速くなった。", "後半の made the whole process slower（遅くした）と逆である。"),
      ("新しい予約システムは遠くからでも使えるので時間が節約できる。", "far を距離の意味に取り違えている。")], "far from A"),
    ("What matters is not how many books you own but how many you actually read.", "大切なのは本を何冊持っているかではなく、実際に何冊読むかだ。",
     [("本はたくさん持っているほど価値がある。", "not A but B の A（持っている冊数）は、筆者が退けている考えである。"),
      ("本を何冊持っているかと何冊読むかは、同じくらい大切だ。", "not A but B は A を否定して B を主張する形で、両方を同等とはしていない。"),
      ("読まない本は買うべきではない。", "購入についての提案は述べられていない。")], "not A but B"),
    ("Admittedly, the new library will be expensive to build, but the cost of doing nothing would be far greater.", "新しい図書館の建設には確かに費用がかかるが、何もしないことの損失のほうがはるかに大きい。",
     [("新しい図書館は費用がかかりすぎるので、建てるべきではない。", "Admittedly は譲歩で、筆者の主張は but の後ろ（何もしないほうが損失が大きい）にある。"),
      ("新しい図書館は安く建てられる。", "expensive to build と逆である。"),
      ("何もしないほうが費用がかからないので賢明だ。", "the cost of doing nothing would be far greater と逆である。")], "Admittedly A, but B"),
    ("Success in sports depends not so much on talent as on persistence.", "スポーツでの成功は、才能というよりむしろ粘り強さで決まる。",
     [("スポーツでの成功は、粘り強さというよりむしろ才能で決まる。", "not so much A as B は「AというよりむしろB」で、比較の向きが逆である。"),
      ("スポーツでの成功には、才能も粘り強さも関係がない。", "not を depends on 全体の否定と取り違えている。"),
      ("才能のある人ほど粘り強い。", "才能と粘り強さの関係は述べられていない。")], "not so much A as B"),
    ("While online courses are convenient, they cannot fully replace the experience of learning alongside others.", "オンライン講座は便利ではあるが、他の人と一緒に学ぶ経験の完全な代わりにはならない。",
     [("オンライン講座は便利なので、他の人と一緒に学ぶ授業に完全に取って代わるだろう。", "While はここでは譲歩（～だけれども）で、主節の「完全には代われない」が主張である。"),
      ("オンライン講座は不便なので、受けるべきではない。", "convenient（便利だ）と認めており、逆である。"),
      ("オンライン講座を受けている間は、他の人と一緒に学ぶことはできない。", "While を「～している間」という時の意味に取り違えている。")], "While A, B"),
    ("Few people would deny that exercise is good for us, yet most of us do not get enough of it.", "運動が体によいことを否定する人はほとんどいないが、たいていの人は十分に運動していない。",
     [("運動が体によいことを否定する人も少しはいる。", "few は「ほとんど～ない」という否定的な意味で、a few（少しはいる）とは違う。"),
      ("たいていの人は、運動が体によいとは思っていない。", "否定する人がほとんどいない＝ほとんどの人は認めている、という二重の否定を読み落としている。"),
      ("たいていの人は十分に運動している。", "do not get enough of it と逆である。")], "Few … would deny"),
    ("Only when we lose our health do we realize how valuable it is.", "健康を失って初めて、私たちはそのありがたさに気づく。",
     [("健康を失うと、私たちはそのありがたさを忘れてしまう。", "realize は「気づく」で、忘れるのではない。"),
      ("健康なときにこそ、私たちはそのありがたさに気づく。", "Only when ～「～して初めて」の意味と逆である。"),
      ("健康を失うことだけが、価値のあることだ。", "Only when … の倒置構文を、Only が主語を修飾する形と取り違えている。")], "Only when A do we B"),
    ("The question is no longer whether we should act, but how quickly we can.", "もはや問題は行動すべきかどうかではなく、どれだけ早く行動できるかだ。",
     [("行動すべきかどうかについては、まだ議論の余地がある。", "no longer（もはや～ない）で、「行動すべきか」はもう問題ではないと述べている。"),
      ("急いで行動すべきではない。", "how quickly we can（どれだけ早くできるか）が問題だと述べており、逆である。"),
      ("もう行動する必要はない。", "no longer が否定しているのは「行動すべきかどうかという問い」で、行動そのものではない。")], "no longer A, but B"),
    ("Rather than banning smartphones in class, schools should teach students how to use them wisely.", "学校は授業中のスマートフォンを禁止するのではなく、賢い使い方を教えるべきだ。",
     [("学校は授業中のスマートフォンの使用を禁止すべきだ。", "rather than ～ は「～ではなく」で、禁止は筆者が退けている案である。"),
      ("学校はスマートフォンの使い方を教えたうえで、授業中は禁止すべきだ。", "禁止と指導を両立させており、rather than の意味と合わない。"),
      ("生徒は自分でスマートフォンの使い方を学ぶべきだ。", "主語は schools（学校）で、学校が教えるべきだと述べている。")], "Rather than A, B"),
    ("Much as I admire her courage, I cannot agree with her conclusion.", "私は彼女の勇気には大いに感心するが、その結論には賛成できない。",
     [("私は彼女の勇気に感心しているので、その結論にも賛成する。", "Much as ～ は「～だけれども」という譲歩で、主節では賛成できないと述べている。"),
      ("私は彼女の勇気にも結論にも感心していない。", "admire（感心する）を否定と取り違えている。"),
      ("私は彼女の結論にも、勇気と同じくらい感心している。", "Much as を比較の as ～ as と取り違えている。")], "Much as A, B"),
    ("However advanced machines become, human judgment will still be needed.", "機械がどれほど進歩しても、人間の判断は依然として必要とされるだろう。",
     [("機械が進歩すれば、人間の判断は不要になるだろう。", "will still be needed（依然として必要）と逆である。"),
      ("機械がどのように進歩したかを、人間が判断する必要がある。", "However ＋形容詞は「どれほど～でも」で、「どのように」という意味ではない。"),
      ("しかし、機械は人間の判断よりも進歩するだろう。", "However を逆接の副詞「しかし」と取り違えている。")], "However＋形容詞＋S V"),
]

# 文の並べかえ用の段落（話題, 正しい順の文）
ORDER_PARAS = [
    ("植物の情報伝達", ["Plants may seem silent and passive, but many of them can respond to threats in surprisingly active ways.",
                   "When some plants are attacked by insects, for instance, they release chemicals into the air.",
                   "Nearby plants of the same kind can detect these chemicals and begin producing substances that make their leaves less tasty to insects.",
                   "In this way, the first plant's injury serves as a warning to its neighbors.",
                   "Such findings are changing the way scientists think about what plants are capable of."]),
    ("方言の価値", ["Regional dialects are sometimes regarded as incorrect versions of a standard language.",
               "Linguists, however, reject this view.",
               "In their view, a dialect has its own consistent rules of pronunciation, grammar, and vocabulary, just as the standard language does.",
               "The standard form is simply the variety that came to be associated with education and government.",
               "Seen this way, dialects are not errors but valuable parts of a community's identity."]),
    ("ハチと食料", ["Bees do far more than make honey.",
               "Many of the fruits and vegetables we eat depend on bees and other insects to carry pollen from flower to flower.",
               "Without this process, known as pollination, these plants would produce much less food.",
               "That is why the decline of bee populations in many regions has become a serious concern for farmers.",
               "Protecting bees, therefore, is not only an environmental issue but also a question of food supply."]),
    ("機械翻訳の限界", ["Machine translation has improved dramatically in recent years.",
                  "A sentence typed in one language can now be turned into another almost instantly, often with impressive accuracy.",
                  "Even so, these tools still struggle with humor, cultural references, and words that have several meanings.",
                  "A translation that is grammatically perfect may therefore miss what the writer actually meant.",
                  "For important documents, a human check remains essential."]),
    ("自由な遊び", ["Free play is often seen as a break from learning, but it may be one of the most important ways children learn.",
               "When children invent their own games, they have to agree on rules, settle arguments, and adjust when things do not go as planned.",
               "These experiences build skills that are difficult to teach directly, such as cooperation and self-control.",
               "Unfortunately, many children today have little free time because their schedules are filled with lessons and activities.",
               "Adults may need to protect time for play just as carefully as they protect time for study."]),
    ("練習の質", ["Practice does not automatically lead to improvement.",
             "A pianist who plays the same easy piece a thousand times may become very comfortable with it but learn little that is new.",
             "Real progress usually comes from focusing on specific weaknesses and working on tasks that are slightly beyond one's current level.",
             "This kind of practice is often uncomfortable, because it involves making frequent mistakes.",
             "In short, how we practice matters at least as much as how long we practice."]),
    ("10代の睡眠", ["Teenagers are often criticized for staying up late and sleeping in on weekends.",
               "Yet this pattern is not simply a matter of laziness.",
               "During adolescence, the body's internal clock tends to shift later, so many teenagers do not feel sleepy until late at night.",
               "When they must still wake up early for school, they easily end up with too little sleep.",
               "Understanding this biological change can help adults respond with more patience and better schedules."]),
    ("海の騒音", ["The ocean is often imagined as a silent world, but it is actually full of sound.",
             "Whales and dolphins use sound to communicate and to find food, since light does not travel far underwater.",
             "In recent decades, however, noise from ships and construction has made the sea much louder.",
             "This noise can interfere with the signals that marine animals depend on.",
             "Reducing underwater noise is therefore becoming an important goal in protecting ocean life."]),
]


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["concept", "condition_check"])
def a_vocab(r):
    p = r.choice(PASSAGES)
    v = r.choice(p["vocab"])
    sent = sentence_with(p, v["para"], v["w"])
    return mc(f"{head(p)}\n{ORD[v['para']]}段落の次の文の下線部 {v['w']} の意味として、文脈から最も適切なものを選びなさい。\n{sent}",
              [v["ok"]] + [w for w, _ in v["wrongs"]],
              f"{v['ok']}　{v['clue']}", d=2, stim=pstim(p),
              ap="未知語の前後にある手がかり（言いかえ・対比・例・因果・語の成り立ち）を探し、意味の方向を決めてから選ぶ。",
              steps=["下線部の語の品詞と、文の中での働きを確認する。", f"手がかりを探す：{v['clue']}", f"意味の方向に合う選択肢は：{v['ok']}", "選んだ意味を文に戻して、文意が通るかを確かめる。"],
              alt=["各選択肢を下線部に代入して読み、前後の文や段落の流れと矛盾しないものを残す。"],
              pc=[("文脈の手がかりを見つけている", 1), ("正しい意味を選んでいる", 1)],
              pit=["知っている別の意味や、近くにある別の語に引きずられて選ぶ。"],
              why={w: (reason, "文脈の手がかりの見落とし") for w, reason in v["wrongs"]})


@gen("basic_check", 5, ["concept", "computation"])
def a_support_type(r):
    claim, sup, t = r.choice(SUPPORT)
    wrongs = r.sample([x for x in SUPPORT_TYPES if x != t], 3)
    why = {w: (f"「{w}」は{SUPPORT_DESC[w]}根拠で、手がかりは {SUPPORT_CUE[w]}。B にはそれがなく、{SUPPORT_CUE[t]} から「{t}」とわかる。", "根拠の種類の取り違え") for w in wrongs}
    return mc(f"次の A は、ある論説文の主張、B はそれを支えるために筆者が書いた文である（数値・事例は架空のもの）。B は A をどのような種類の根拠で支えているか。最も適切なものを選びなさい。\nA: {claim}\nB: {sup}",
              [t] + wrongs, f"「{t}」。{SUPPORT_DESC[t]}根拠で、手がかりは {SUPPORT_CUE[t]}。", d=2,
              ap="B の主語・時制・数値・比較の表現に注目し、「誰が・何を根拠に」言っているのかを確かめる。",
              steps=["A の主張を確認する。", f"B の手がかりを探す：{SUPPORT_CUE[t]}。", f"根拠の種類は「{t}」。", "B が A と同じ方向を向いているか（A を支えているか）も確かめる。"],
              alt=["B を別の種類の根拠（例：数値データ）に書きかえるとどうなるかを考え、元の B との違いから種類を確かめる。"],
              pc=[("B の手がかりに気づいている", 1), ("根拠の種類を正しく選んでいる", 1)],
              pit=["数値を含まない研究の知見を「統計・調査の数値」と判断する。", "Like … のたとえを具体的な事例と取り違える。"], why=why)


@gen("basic_check", 5, ["computation", "concept"])
def a_detail(r):
    p = r.choice(PASSAGES)
    q, ok, wrongs = r.choice(p["details"])
    return mc(f"{head(p)}\n{q}最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　設問が指す段落の該当箇所を探し、言いかえに注意して照合する。", d=2, stim=pstim(p),
              ap="設問が指定する段落とキーワードを確認し、その文の前後を精読する。正解の選択肢は本文の言いかえになっていることが多い。",
              steps=["設問の段落とキーワードを確認する。", "本文で同じ語句・言いかえを探す。", "該当箇所と選択肢を、肯定・否定や程度の語（always / only など）まで照合する。", f"答え：{ok}"],
              alt=["誤りの選択肢について、本文のどこと食い違うか（書かれていない・逆・別の段落の話・言いすぎ）を1つずつ確かめる。"],
              pc=[("本文の該当箇所を見つけている", 1), ("正しい選択肢を選んでいる", 1)],
              pit=["本文に出てくる語句を含むだけの選択肢を選ぶ。", "別の段落の情報を、設問の段落の答えとして選ぶ。"],
              why={w: (reason, "本文との照合不足") for w, reason in wrongs})


@gen("basic_check", 5, ["condition_check", "common_error"])
def a_logic(r):
    en, ok, wrongs, form = r.choice(LOGIC)
    return mc(f"次の英文の内容を最も正確に表しているものを選びなさい。構文（{form}）に注意すること。\n{en}", [ok] + [w for w, _ in wrongs],
              f"{ok}　{form} の形では、筆者が退けている考えと主張している考えを区別して読む。", d=2,
              ap="否定・譲歩・強調の構文を見つけ、どの部分が筆者の退ける考えで、どの部分が主張かに線を引き分けてから選ぶ。",
              steps=[f"構文 {form} を確認する。", "筆者が退けている（否定・譲歩している）部分を特定する。", "筆者が主張している部分を特定する。", f"両方を正しく表しているのは：{ok}"],
              alt=["選んだ日本語を英語に戻したとき、元の英文と同じ構造（何を否定し、何を主張するか）になるかを確かめる。"],
              pc=[("構文の働きをとらえている", 1), ("正しい内容を選んでいる", 1)],
              pit=["否定・譲歩されている部分を筆者の主張と取り違える。", "far / while / however などを、ふだんよく使う意味で読む。"],
              why={w: (reason, "否定・譲歩の構文の読み違い") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["concept", "application"])
def b_main(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.5:
        ok, wrongs, what = p["main"], r.sample(p["main_wrong"], 3), "本文の主旨"
    else:
        ok, wrongs, what = p["title_ok"], p["title_wrong"], "本文の題名"
    return mc(f"{head(p)}\n{what}として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　問題提起と結論の段落を中心に、根拠の具体例と譲歩を除いて筆者の主張をとらえる。", d=3, stim=pstim(p),
              ap="第1段落の問題提起と最終段落の結論を先に読み、筆者の主張をつかむ。次に譲歩の段落で主張がどう限定されているかを確かめる。",
              steps=["第1段落で話題と問題提起を確認する。", "最終段落の結論（Nonetheless / Still / The lesson is など）を確認する。", "譲歩の段落で、主張がどの範囲に限定されているかを確認する。",
                     "各選択肢を「狭すぎる・広すぎる・逆・言いすぎ」で点検する。", f"答え：{ok}"],
              alt=["各段落の役割を書き出し、すべての段落の内容を含み、しかも譲歩の限定を越えない選択肢を選ぶ。"],
              pc=[("問題提起・結論・譲歩をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["印象に残る具体例を主旨として選ぶ。", "譲歩で限定された主張を always / every で広げた選択肢を選ぶ。"],
              why={w: MAIN_WHY[k] for w, k in wrongs})


@gen("standard_practice", 4, ["concept", "condition_check"])
def b_role(r):
    p = r.choice(PASSAGES)
    i = r.randrange(5)
    role, gist, excl = p["roles"][i]
    pool = [x for x in ROLE_ORDER if x != role and x not in excl]
    wrongs = r.sample(pool, 3)
    why = {ROLES[w]: (f"{ORD[i]}段落は{gist}。「{ROLES[w]}」はこの段落の主たる働きではない。", "段落の役割の取り違え") for w in wrongs}
    return mc(f"{head(p)}\n{ORD[i]}段落が文章全体の中で果たしている役割として最も適切なものを選びなさい。", [ROLES[role]] + [ROLES[w] for w in wrongs],
              f"「{ROLES[role]}」。{ORD[i]}段落は{gist}。", d=3, stim=pstim(p),
              ap="段落の最初の1〜2文の表現（Admittedly / Part of the reason / In response / Nonetheless など）と、前後の段落とのつながりから役割を判断する。",
              steps=[f"{ORD[i]}段落の書き出しの表現と主題文を確認する。", "前の段落の内容に対して、この段落が何をしているか（説明する・裏づける・認める・解決する・まとめる）を考える。", f"役割は「{ROLES[role]}」。"],
              alt=["5つの段落すべてに役割を書きこみ、全体の流れ（導入 → 本論 → 譲歩 → 結論など）として自然かを確かめる。"],
              pc=[("段落の内容をとらえている", 2), ("役割を正しく選んでいる", 2)],
              pit=["段落の中の具体例だけを見て役割を決める。", "譲歩の段落を結論と取り違える。"], why=why)


@gen("standard_practice", 4, ["application", "condition_check"])
def b_evidence(r):
    p = r.choice(PASSAGES)
    ev = r.choice(p["evid"])
    return mc(f"{head(p)}\n筆者は本文で “{ev['claim']}” と主張している。この主張を支える根拠として本文で用いられているものを選びなさい。",
              [ev["ok"]] + [w for w, _ in ev["wrongs"]],
              f"{ev['ok']}　{ORD[ev['cpara']]}段落で、主張と同じ方向を向いて主張を裏づけている。", d=3, stim=pstim(p),
              ap="主張に対して「なぜそう言えるのか」と問い、その答えになっている文を探す。本文に書かれている事実でも、別の主張を支えるものは根拠にならない。",
              steps=["主張が本文のどの段落にあるかを探す。", "その主張に「なぜ」と問いかけ、答えになる文を同じ段落や前後から探す。",
                     "各選択肢が、この主張を支えているか、別の主張（譲歩・原因・対策など）を支えているかを分ける。", f"答え：{ev['ok']}"],
              alt=["選んだ選択肢と主張を because でつないだ英文（主張 because 根拠）を作り、論理が通るかを確かめる。"],
              pc=[("主張の位置と内容をとらえている", 2), ("主張を支える根拠を選んでいる", 2)],
              pit=["本文に書かれている事実なら、どの主張の根拠にもなると考える。"],
              why={w: (reason, "根拠と主張の対応の取り違え") for w, reason in ev["wrongs"]})


@gen("standard_practice", 4, ["condition_check", "common_error"])
def b_true(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.6:
        ok = r.choice(p["trues"])
        wrongs = r.sample(p["falses"], 3)
        return mc(f"{head(p)}\n本文の内容と一致するものを1つ選びなさい。", [ok] + [w for w, _ in wrongs],
                  f"{ok}　本文の該当箇所の言いかえになっている。", d=3, stim=pstim(p),
                  ap="選択肢ごとに根拠となる本文の箇所を探し、「一致・逆・書かれていない・言いすぎ」に分ける。",
                  steps=["選択肢のキーワードを本文で探す。", "該当箇所と選択肢を照合する（not / only / every / always などに注意）。", f"本文と一致するのは：{ok}"],
                  alt=["誤りの選択肢について、本文のどの語句と食い違うかを書き出して確かめる。"],
                  pc=[("根拠となる本文の箇所を見つけている", 2), ("正しい選択肢を選んでいる", 2)],
                  pit=["every / always / all などの強い限定の語を見落とす。"], why={w: (reason, "本文との照合不足") for w, reason in wrongs})
    f, reason = r.choice(p["falses"])
    oks = r.sample(p["trues"], 3)
    return mc(f"{head(p)}\n本文の内容と一致しないものを1つ選びなさい。", [f] + oks,
              f"{f}　{reason}", d=3, stim=pstim(p),
              ap="「一致しないもの」を選ぶ設問なので、選択肢ごとに本文の根拠を探して〇×をつけ、×が1つだけになることを確かめる。",
              steps=["設問が「一致しないもの」を求めていることを確認する。", "各選択肢の根拠を本文で探して〇×をつける。", f"本文と食い違うのは：{f}（{reason}）"],
              alt=["一致する3つの選択肢の根拠となる段落番号をすべて書き出し、残った1つが本文と食い違うことを確かめる。"],
              pc=[("各選択肢の根拠を確認している", 2), ("一致しないものを選んでいる", 2)],
              pit=["設問の「一致しないもの」を読み落とし、一致するものを選ぶ。"],
              why={o: ("本文の内容と一致するので、「一致しないもの」には当たらない。", "設問の条件の読み落とし") for o in oks})


@gen("standard_practice", 4, ["computation", "application"])
def b_order(r):
    topic, sents = r.choice(ORDER_PARAS)
    return order(f"次の5つの英文を、意味が通る1つの段落になるように並べかえなさい（話題：{topic}）。", sents,
                 "主題文 → 説明・根拠 → 転換や因果 → 結論の順になる。指示語（this / these / such）とつなぎの語（however / therefore / that is why）が手がかりになる。", d=3, p=4,
                 ap="ほかの文を前提にしない一般的な文を先頭に置き、This / These / Such / however / therefore などが何を受けているかで残りの順序を決める。",
                 steps=["指示語やつなぎの語を含まず、話題を一般的に述べる文を先頭に置く。", "指示語（this process / these chemicals / such findings など）が受ける内容を含む文を、その直前に置く。",
                        "逆接（however / even so / yet）の文は、それが否定・転換する内容の直後に置く。", "結論（therefore / in short / seen this way）の文を最後に置き、通して読んで流れを確かめる。"],
                 alt=["隣り合う2文ごとに「後ろの文は前の文がないと意味が通らないか」を確かめ、つながりを1組ずつ決めてからつなぐ。"],
                 pc=[("先頭と最後の文を正しく選んでいる", 2), ("中の3文の順序が正しい", 2)],
                 pit=["指示語が何を指すかを確かめずに並べる。", "however の文を先頭に置く。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_summary_jp(r):
    p = r.choice(PASSAGES)
    lim = r.choice([100, 120])
    return desc(f"{head(p)}\n本文の要旨を、具体例を除いて日本語{lim}字以内でまとめなさい。譲歩の内容をどう扱ったかがわかるように書くこと。", p["summary"],
                "各段落の役割を押さえ、根拠の具体例を除き、譲歩は「～だが」と従属的に扱って、問題提起と結論を中心にまとめる。",
                p["skeys"], d=4, p=8, grid=lim, stim=pstim(p),
                ap="段落ごとの要点を1文ずつ書き、根拠の段落は「何を示すか」だけを残す。譲歩は主張の前に「～だが」で添え、結論の段落の主張で文を閉じる。",
                steps=["5つの段落に役割（導入・定義・原因・根拠・利点・譲歩・解決策・結論）を書きこむ。", "根拠の段落から具体例（人・場所・生き物の名前など）を除き、要点だけを残す。",
                       "譲歩の段落を「～という面もあるが」と従属的に扱う。", "問題提起・要点・結論を論理の接続（～ので／～だが）でつなぎ、字数内に圧縮する。"],
                alt=["まず英語で主旨を1文で書き、それを日本語に直してから、主な理由と譲歩を肉づけする方法もある。"],
                pc=[(k, v) for k, v in p["skeys"]],
                pit=["具体例を要旨に入れる。", "譲歩の段落の内容を筆者の主張としてまとめる。"])


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def c_explain(r):
    p = r.choice(PASSAGES)
    q, a = r.choice(p["exqs"])
    return desc(f"{head(p)}\n{q}", a,
                "設問が指す箇所を特定し、前後の段落との論理関係（原因と結果・譲歩と主張・問題と対策）をたどって、本文の内容に即して説明する。",
                [("設問が指す本文の箇所と、関係する段落を正しく特定している", 3), ("論理関係をたどって本文に即して説明している", 3), ("設問の問い方に合った文末で答えている", 2)], d=4, p=8, lines=6, stim=pstim(p),
                ap="設問の表現を本文で探し、その文の前後のつなぎの語（however / nonetheless / for this reason / yet）から、どの段落とどう結びついているかを確かめる。",
                steps=["設問が指す表現と段落を確認する。", "関係する段落（原因・根拠・譲歩など）を探し、内容を日本語で整理する。",
                       "論理関係（～なので・～だが・～するために）でつないで説明を組み立てる。", "設問の問い方（なぜ → 「～から・ため」、どういうことか → 「～ということ」）に合わせて文末を整える。"],
                alt=["書いた答えを本文の該当箇所と1文ずつ対応させ、抜けている要素や本文にない付け足しがないかを確かめる。"],
                pc=[("箇所の特定", 3), ("論理関係に即した説明", 3), ("文末の形", 2)],
                pit=["設問が指す1文だけを訳して、前後の段落との関係を説明しない。", "本文に書かれていない自分の意見を加える。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U10", "SS-ENG-U01"])
def c_summary_en(r):
    p = r.choice(PASSAGES)
    n = r.choice([35, 45])
    return desc(f"{head(p)}\n本文の要旨を、本文の文をそのまま写さずに、自分の言葉で英語{n}語程度にまとめなさい。筆者の主張と、その主な根拠を含めること。",
                f"（解答例）{p['en_sum']}",
                "主語をそろえて1〜2文で言い直す。具体的な事例は上位の語に言いかえ、譲歩は Although … などで従属節にまとめる。",
                [("筆者の主張を正しく表している", 3), ("主な根拠を含め、具体例の細部を除いている", 3), ("文法・語法が正しく、語数が適切で、本文の写しになっていない", 2)], d=4, p=8, lines=6, stim=pstim(p),
                ap="日本語の要約（段落の要点のつなぎ）を先に作り、それを英語の1〜2文に直す。because / so / although で論理の接続を明示する。",
                steps=["結論の段落から主張を、根拠の段落から主な理由を取り出す。", "具体例は上位の語に言いかえる（sea turtles and birds → wildlife など）。",
                       "主張と理由を because / so で、譲歩を although でつないで英文にする。", "語数を数え、本文の文をそのまま写していないかを確かめる。"],
                alt=["Although（譲歩）, 主張 because 根拠. の型に当てはめて書くと、論理の接続が崩れにくい。"],
                pc=[("主張", 3), ("根拠と具体例の処理", 3), ("文法・語数・言いかえ", 2)],
                pit=["本文の文をつなぎ合わせて語数を超える。", "具体例だけを英語で書き、主張を書かない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "written_reasoning"])
def d_summary_err(r):
    p = r.choice(PASSAGES)
    wrong, why = r.choice(p["wrong_sum"])
    return desc(f"{head(p)}\n本文の要旨を日本語でまとめる問題に、ある生徒は次のように答えた。\n［ある生徒の解答］\n{wrong}\nこの解答の問題点を、段落の役割に触れて指摘し、正しい要旨を書きなさい。",
                f"問題点：{why}　正しい要旨：{p['summary']}",
                "要旨には、根拠の具体例や譲歩の内容ではなく、筆者の主張とその主な理由を入れる。",
                [("解答の問題点を正しく指摘している", 2), ("正しい要旨を書いている", 3), ("段落の役割に触れて説明している", 1)], d=4, p=6, lines=6, stim=pstim(p),
                ap="生徒の解答が本文のどの段落の内容かを確かめ、その段落の役割（根拠の事例・譲歩・背景）を考える。",
                steps=["生徒の解答が本文のどの段落に対応するかを確かめる。", "その段落の役割を判断し、要旨として不十分な点（主張がない・主張と逆）を指摘する。", "問題提起と結論を中心に、正しい要旨を書く。"],
                alt=["生徒の解答と正しい要旨を並べ、最終段落の結論が含まれているかどうかで比べる。"],
                pc=[("問題点の指摘", 2), ("正しい要旨", 3), ("段落の役割への言及", 1)],
                pit=["具体例を言いかえただけで、主張を書かない。"],
                err=dict(sol=wrong, step="要旨の中心に選んだ段落", type="interpretation", tempt="印象に残る事例や、Of course / Admittedly の後ろの内容を、筆者の主張だと思いこんだ。",
                         fix=p["summary"]))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_vocab_err(r):
    p = r.choice(PASSAGES)
    v = r.choice(p["vocab"])
    wrong, reason = v["wrongs"][0]
    sent = sentence_with(p, v["para"], v["w"])
    return desc(f"{head(p)}\n{ORD[v['para']]}段落の次の文の下線部 {v['w']} の意味を推測する問題で、ある生徒は “{wrong}” と答えた。\n{sent}\nこの推測の誤りを、使うべきだった文脈の手がかりに触れて指摘し、正しい意味を答えなさい。",
                f"誤り：{reason}　手がかり：{v['clue']}　正しい意味：{v['ok']}",
                f"{v['clue']}　推測した意味は必ず文に戻して確かめる。",
                [("推測の誤りを指摘している", 2), ("使うべき文脈の手がかりを示している", 2), ("正しい意味を答えている", 2)], d=3, p=6, lines=5, stim=pstim(p),
                ap="生徒の答えを文に代入して、前後の内容と矛盾しないかを確かめる。次に、言いかえ・対比・例・因果・語の成り立ちの手がかりを探す。",
                steps=[f"生徒の答え “{wrong}” を文に代入し、矛盾する点を見つける：{reason}", f"手がかりを探す：{v['clue']}", f"正しい意味：{v['ok']}"],
                alt=["正しい意味を文に代入して読み、段落全体の流れと合うことを確かめる。"],
                pc=[("誤りの指摘", 2), ("手がかりの提示", 2), ("正しい意味", 2)],
                pit=["語の知っている意味や、近くにある別の語だけで推測する。"],
                err=dict(sol=wrong, step=f"{v['w']} の意味の推測", type="interpretation", tempt=v["tempt"], fix=v["ok"]))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_evidence_err(r):
    p = r.choice(PASSAGES)
    ev = r.choice(p["evid"])
    wrong, reason = r.choice(ev["wrongs"])
    return desc(f"{head(p)}\n「筆者の主張 “{ev['claim']}” を支える根拠を本文から1つ挙げよ」という問題に、ある生徒は次の内容を挙げた。\n［ある生徒の解答］\n{wrong}\nこの解答の誤りを指摘し、正しい根拠を本文に即して答えなさい。",
                f"誤り：{reason}　正しい根拠：{ev['ok']}（{ORD[ev['cpara']]}段落）",
                "根拠は、その主張に「なぜそう言えるのか」と問いかけたときの答えになる文である。本文に書かれている事実でも、別の主張を支えるものは根拠にならない。",
                [("生徒の解答が別の主張を支えていることを指摘している", 2), ("正しい根拠を挙げている", 3), ("主張と根拠の関係を説明している", 1)], d=4, p=6, lines=5, stim=pstim(p),
                ap="生徒が挙げた文が本文のどの段落にあり、その段落が何を主張しているかを確かめる。次に、指定された主張に「なぜ」と問いかけて答えになる文を探す。",
                steps=["生徒が挙げた文の位置と、その文が支えている主張を確かめる。", f"指定された主張は{ORD[ev['cpara']]}段落にあることを確認する。",
                       "主張に「なぜ」と問い、答えになる文を探す。", f"正しい根拠：{ev['ok']}"],
                alt=["「主張 because 根拠」の英文を、生徒の答えと正しい答えの両方で作り、どちらが論理的に通るかを比べる。"],
                pc=[("誤りの指摘", 2), ("正しい根拠", 3), ("関係の説明", 1)],
                pit=["本文に書かれていれば根拠として正しいと考え、どの主張を支えているかを確かめない。"],
                err=dict(sol=wrong, step="根拠として選んだ文", type="logic", tempt="本文に書かれている事実であることだけを確かめ、指定された主張と同じ方向を向いているかを確かめなかった。",
                         fix=ev["ok"]))


GENERATORS = [a_vocab, a_support_type, a_detail, a_logic,
              b_main, b_role, b_evidence, b_true, b_order,
              c_summary_jp, c_explain, c_summary_en,
              d_summary_err, d_vocab_err, d_evidence_err]
