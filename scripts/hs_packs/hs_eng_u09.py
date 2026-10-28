"""単元パック：英語コミュニケーションⅠ 長文読解（パラグラフの構成・ディスコースマーカー・要旨把握）。

本文はすべてこのパックのためのオリジナル英文。
"""
from banks._common import desc, mc, order, stim
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U09"

# ======================================================================
# 授業プリント
# ======================================================================

MINI = ("Many people think that a good memory is something you are born with. However, memory is more like a muscle. "
        "For example, actors remember long scripts by practicing a little every day. In short, the more we train our memory, the stronger it becomes.")

LESSON = lesson(
    goals=["パラグラフが主題文（topic sentence）・支持文・まとめの文から成ることを理解し、主題文を見つけられる。",
           "ディスコースマーカー（however / for example / as a result / in short など）の働きから、文と文、段落と段落の論理関係をつかめる。",
           "各段落の役割を押さえ、具体例を除いて筆者の主張を中心に要旨をまとめられる。"],
    duration=50,
    readiness=["中学で学んだ接続詞（and / but / so / because）の意味を知っている。",
               "中学3年の長文読解で、段落ごとの内容を日本語で言える。",
               "文型（S・V・O・C）を手がかりに、1文の意味を取ることができる（HS-ENG-U01）。"],
    flow=[("導入：論理の「道しるべ」", 5, "However の前後で内容がどう変わるかを考えさせ、つなぎの語が読みの道しるべになることを示す"),
          ("パラグラフの構成", 12, "主題文・支持文・まとめの文の働きを確認し、主題文の見つけ方を例題で練習する（例題1）"),
          ("ディスコースマーカー", 13, "逆接・例示・追加・結果・対比・言いかえ・結論の7つの働きに分類する（例題2）"),
          ("要旨把握の手順", 13, "段落の役割を書きこみ、具体例を除いて要旨をまとめる手順を示す（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "長文は「1文ずつ」ではなく「論理の流れ」で読む",
              "長い英文を読むとき、すべての単語を訳そうとすると、途中で何の話かわからなくなりやすい。英語の論説文は、1つの段落に1つの主張を置き、それを例や理由で支え、段落どうしを however や for example などの語でつなぐという、決まった組み立て方で書かれていることが多い。この組み立てを知っていれば、知らない単語があっても筆者の言いたいことをつかめる。",
              bullets=["段落の最初（または最後）に、その段落の主張（主題文）が置かれることが多い。",
                       "However の後ろには、前と反対の内容や筆者の本当の主張が来やすい。",
                       "For example の後ろは具体例なので、要旨には入れないことが多い。"],
              points=[tp("However の前後の2文だけを板書し、「どちらが筆者の言いたいことか」を考えさせる。", ask="However の前と後ろでは、どちらが筆者の主張に近いか。",
                         expect="後ろ。前は一般的な考えで、後ろで筆者がそれを否定している。", timing="導入の冒頭"),
                      tp("長文読解は「単語力」だけでなく「構成を読む力」で差がつくことを最初に伝える。")]),
        definition("df1", "パラグラフの構成",
                   "英語のパラグラフ（段落）は、ふつう1つの中心的な考えを述べる。その考えを示す文を主題文（topic sentence）、それを理由・例・説明で支える文を支持文（supporting sentences）、段落の終わりで考えを言いかえてまとめる文をまとめの文（concluding sentence）という。",
                   bullets=["主題文：段落の中で最も一般的・抽象的な文。ほかの文はすべてこの文を支える。",
                            "支持文：理由（because ～）、具体例（for example ～）、詳しい説明。",
                            "まとめの文：In short / In this way / That is why などで始まることが多い。",
                            "文章全体も同じ構造になる：導入の段落 → 本論の段落 → 結論の段落。"],
                   conditions=["主題文は段落の最初にあることが多いが、However の後ろや段落の最後に置かれることもある。",
                               "疑問文で始まる段落では、その問いへの答えが主題文になることが多い。"],
                   points=[tp("「段落の中で、ほかのすべての文が説明している文はどれか」と問いかけ、主題文を内容の包含関係で見つけさせる。", caution="段落の最初の文を機械的に主題文と決めつける生徒が多い。")]),
        theorem("th1", "ディスコースマーカーの働き",
                "逆接 however, but, nevertheless ／ 例示 for example, for instance ／ 追加 in addition, moreover, also ／ 結果 as a result, therefore, so ／ 対比 on the other hand, in contrast ／ 言いかえ in other words, that is ／ 結論 in short, in conclusion, to sum up",
                ["逆接・対比の後ろには、筆者の主張や重要な情報が来やすい。",
                 "例示の後ろは具体例で、直前の一般的な文を説明している。",
                 "結果・結論の後ろは、前の内容から導かれることや全体のまとめである。"],
                body="ディスコースマーカーは文と文、段落と段落の論理関係を示す「道しるべ」である。マーカーの働きがわかれば、後ろに来る内容を予測しながら読める。",
                points=[tp("マーカーを7つの働きに分類する表を生徒に作らせ、それぞれの後ろに来る内容を予測させる。",
                           ask="In short の後ろにはどんな内容が来ると予測できるか。", expect="それまでの内容の短いまとめ。")]),
        derivation("dv1", "要旨をまとめる手順（なぜ具体例を除くのか）",
                   ["① 各段落の主題文に下線を引く。主題文が見つからない段落は、その段落が何について述べているかを一言で書く。",
                    "② 各段落の役割（問題提起・具体例・反対の視点・結論など）を、ディスコースマーカーを手がかりに書きこむ。",
                    "③ 具体例の段落・文は、主張を支えるための材料なので、要旨からは外す。",
                    "④ 反対の視点（However / On the other hand の段落）は、筆者がそれを認めたうえで主張を述べる部分なので、主張と取り違えない。",
                    "⑤ 結論の段落（In short / Therefore / In conclusion）と導入の問題提起を中心に、筆者の主張を1〜2文にまとめる。",
                    "⑥ まとめた文を読み返し、本文にない情報や本文と逆の内容が入っていないかを確かめる。"],
                   body="要旨とは「筆者が最も伝えたいこと」である。具体例は読者を納得させるための材料であり、例を変えても筆者の主張は変わらない。だから要旨では具体例を除き、主張とその主な理由を残す。",
                   points=[tp("手順②の役割の書きこみを、例題3の短い文章で全員で行う。", ask="For example で始まる文を要旨に入れるべきか。",
                              expect="入れない。具体例なので主張を支える材料にすぎない。", timing="手順③の説明時")]),
        example("ex1", "例題1　主題文を見つける",
                "次の段落の主題文を①〜④から選びなさい。\n① Many people think that cats do not care about their owners. ② However, cats show their feelings in quiet ways. ③ For example, a cat may slowly blink at you or follow you from room to room. ④ These small actions are signs that the cat trusts you.",
                ["①は一般的な考えで、筆者はこれを However で否定している。", "②が筆者の主張で、③は For example で始まる具体例、④は例の意味の説明。",
                 "③④はどちらも②の「静かな方法で気持ちを示す」を支えている。"],
                "②",
                thinking="段落の最初の文が主題文とは限らない。However の後ろに筆者の主張が来ることが多い。",
                points=[tp("①を主題文と答えた生徒に、「③④は①を支えているか」と問い返し、包含関係で判断させる。")],
                misconceptions=[("最初の文①が主題文である。", "①は筆者が否定する一般的な考え。However の後ろの②が主題文")]),
        example("ex2", "例題2　ディスコースマーカー",
                "（　）に入る最も適切な語句を選びなさい。\nThe road was closed because of the snow. (　　), we had to take another route.\n［ For example ／ As a result ／ However ／ In contrast ］",
                ["前の文は原因（雪で道路が閉鎖された）、後ろの文はその結果（別の道を通らなければならなかった）。", "原因 → 結果の関係を示すのは As a result。"],
                "As a result",
                thinking="（　）の前後の文の関係（原因と結果、一般と具体、反対、追加など）を先に日本語で考えてから、マーカーを選ぶ。",
                points=[tp("前後の関係を「→」「⇔」「＋」「＝」などの記号で書かせてからマーカーを選ばせる。")]),
        example("ex3", "例題3　短い文章の要旨",
                f"次の文章の要旨を日本語40字以内でまとめなさい。\n{MINI}",
                ["1文目：一般的な考え（記憶力は生まれつき）。", "2文目：However → 筆者の主張（記憶力は筋肉のようなもの）。",
                 "3文目：For example → 具体例（俳優）なので要旨から外す。", "4文目：In short → まとめ（鍛えるほど強くなる）。"],
                "記憶力は生まれつきのものではなく、筋肉のように鍛えるほど強くなる。（33字）",
                thinking="However の後ろと In short の後ろを中心にまとめ、For example の部分は外す。",
                points=[tp("俳優の例を要旨に入れた答案を取り上げ、「例を別のもの（スポーツ選手など）に変えても主張は変わるか」と問う。", ask="例を変えると筆者の主張は変わるか。",
                           expect="変わらない。だから例は要旨に入れなくてよい。")]),
        board("bd1", "板書案",
              [("① パラグラフの構成", ["主題文（topic sentence）", "＝段落の中心の考え", "支持文：理由・例・説明", "まとめの文：In short …", "主題文は However の後ろにも"]),
               ("② ディスコースマーカー", ["逆接：however, nevertheless", "例示：for example", "追加：in addition, moreover", "結果：as a result, therefore", "対比・言いかえ・結論"]),
               ("③ 要旨把握の手順", ["主題文に下線", "段落の役割を書きこむ", "具体例は外す", "反対の視点を主張と取り違えない", "結論＋問題提起でまとめる"])],
              points=[tp("②のマーカーは働きごとに色を変えて書き、生徒にも本文中のマーカーを同じ色で囲ませる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("本文を読む前に、各段落の最初の文と最後の文だけを読ませ、全体の流れを予測させる。", ask="この4つの段落はどんな順で話が進みそうか。", expect="問題提起 → 例 → 反対 → 結論など。"),
               tp("However・On the other hand の段落を筆者の主張と取り違える答案が多いので、「認めたうえで主張する（譲歩）」の流れを図で示す。", caution="Of course ～. Still … のような譲歩の形にも注意させる。"),
               tp("要旨の答案は、具体例が入っていないか、本文にない内容が入っていないかの2点で自己点検させる。", timing="例題3の後"),
               tp("内容一致問題では、選択肢の根拠となる本文の箇所に線を引かせ、言いかえ（paraphrase）に気づかせる。"),
               tp("問題プリント D の誤答例を使い、「例だけの要約」「反対の視点を主張とする要約」「マーカーの誤訳」の3種類を扱う。")],
              misconceptions=[("For example の後ろの具体例を要旨の中心にする。", "具体例は主張を支える材料。主張そのものをまとめる"),
                              ("However で始まる段落の内容を、いつも筆者の主張と考える。", "However で筆者が反対の視点や限界を述べる場合もある。結論の段落と合わせて判断する"),
                              ("段落の最初の文はいつも主題文である。", "However の後ろや段落の最後に主題文が置かれることもある")]),
        summary("sm1", "まとめ",
                ["パラグラフは主題文を中心に、支持文（理由・例）とまとめの文で組み立てられている。",
                 "ディスコースマーカーの働き（逆接・例示・追加・結果・対比・言いかえ・結論）から、後ろの内容を予測して読む。",
                 "要旨は、各段落の役割を押さえ、具体例を除いて、問題提起と結論を中心にまとめる。"]),
        check("ck1", "確認問題",
              [("for instance と同じ働きをするディスコースマーカーを1つ答えなさい。", "for example（例示）"),
               ("In other words の働きを答えなさい。", "言いかえ（前の内容を別の言葉で説明し直す）"),
               ("要旨をまとめるとき、For example で始まる文を入れないのはなぜか。", "具体例は主張を支える材料であり、筆者の主張そのものではないから。")]),
    ])


# ======================================================================
# 本文（オリジナル）
# ======================================================================

ROLES = {
    "intro": "問題提起・話題の導入",
    "example": "具体例による説明",
    "solution": "解決策の提示",
    "benefit": "利点の説明",
    "contrast": "反対の視点・限界の指摘",
    "cause": "原因・理由の説明",
    "conclusion": "結論・筆者の主張のまとめ",
    "counter": "一般的な考えへの反論",
}
ROLE_ORDER = list(ROLES)

PASSAGES = [
    dict(key="BORE", title="Why Boredom Can Be Good for Us",
         paras=["Most of us try hard to avoid boredom. When we have a few free minutes, we take out our phones and look for something to watch or read. Being bored feels like a waste of time, so we fill every empty moment. But is boredom really something we should run away from?",
                "Some people say that boredom actually helps us think in new ways. When there is nothing to hold our attention, our minds begin to wander. We start to remember past events, imagine the future, and connect ideas that seem unrelated. For example, many people say they get their best ideas while taking a shower or waiting for a bus, moments when they have nothing else to do.",
                "However, this does not mean that all boredom is useful. If a student feels bored in every class for months, it may be a sign that something needs to change. Long-lasting boredom can lower our motivation and make us feel unhappy.",
                "In short, a little boredom is not our enemy. Instead of reaching for our phones every time we have nothing to do, we can sometimes let our minds wander. Those quiet moments may give us the space we need to think creatively."],
         roles=[("intro", "退屈を避けようとする私たちの習慣を示し、退屈は本当に避けるべきものかと問いかけている", ["counter"]),
                ("example", "退屈すると心がさまよい新しい発想が生まれることを、シャワーやバス待ちの例で説明している", ["benefit", "counter"]),
                ("contrast", "長く続く退屈は意欲を下げるなど、すべての退屈が役に立つわけではないと限界を述べている", []),
                ("conclusion", "少しの退屈は敵ではなく、創造的に考える余地を与えてくれるとまとめている", [])],
         main="Short periods of boredom can help us think creatively, so we do not always need to avoid them.",
         main_wrong=[("Many people get good ideas while taking a shower.", "narrow"), ("People today use smartphones for many different purposes.", "broad"),
                     ("Boredom always lowers our motivation, so we should avoid it.", "contra")],
         title_ok="The Hidden Value of Boredom",
         title_wrong=[("How to Use Your Smartphone Wisely", "off"), ("Getting Ideas in the Shower", "narrow"), ("Why Students Dislike School", "off")],
         details=[("According to the passage, what do many people do when they have a few free minutes?", "They look at their phones.",
                   [("They take a shower.", "シャワーは、よいアイデアが浮かぶ場面の例として第2段落に出てくるだけである。"),
                    ("They talk with their friends.", "友人と話すことは本文に書かれていない。"),
                    ("They make plans for the future.", "未来を想像するのは心がさまようときの例で、空き時間の行動としては述べられていない。")]),
                  ("When do many people say they get their best ideas?", "When they have nothing else to do, such as while waiting for a bus.",
                   [("When they are watching videos on their phones.", "第2段落では、何もすることがないときにアイデアが浮かぶと述べている。"),
                    ("When they are working hard in class.", "授業中にアイデアが浮かぶとは書かれていない。"),
                    ("When they are talking with other people.", "他人と話しているときとは書かれていない。")]),
                  ("What can long-lasting boredom do, according to the writer?", "It can make people less motivated and unhappy.",
                   [("It can help people get better ideas.", "よいアイデアにつながるのは短い退屈で、長く続く退屈ではない。"),
                    ("It can make classes more interesting.", "授業がおもしろくなるとは書かれていない。"),
                    ("It can make people use their phones less.", "スマートフォンの使用が減るとは書かれていない。")])],
         trues=["The writer thinks that some boredom can be helpful.", "When we are bored, our minds may start to wander.", "Boredom that continues for a long time can be a problem."],
         falses=[("The writer says we should never use our phones.", "第4段落では、退屈するたびにスマートフォンに手を伸ばすのではなく、と述べているだけで、使ってはいけないとは言っていない。"),
                 ("According to the writer, all kinds of boredom are useful.", "第3段落で However に続けて、すべての退屈が役に立つわけではないと述べている。"),
                 ("Students who feel bored in class for months do not need to change anything.", "第3段落では、何かを変える必要があるサインかもしれないと述べている。"),
                 ("People rarely get ideas while waiting for a bus.", "第2段落では、バスを待っている間などに最良のアイデアが浮かぶと言う人が多いと述べている。")],
         summary="退屈すると心がさまよい、新しい発想が生まれやすい。長く続く退屈は問題だが、短い退屈は避けるべきものではなく、創造的に考える余地を与えてくれる。",
         skeys=[("退屈すると心がさまよい新しい発想が生まれることを述べている", 3), ("長く続く退屈は問題だという限定に触れている", 2), ("短い退屈は避けなくてよいという主張でまとめている", 3)],
         exq="筆者が第2段落で、シャワーを浴びているときやバスを待っているときの例を挙げているのはなぜか。日本語で説明しなさい。",
         exa="何もすることがないときに心がさまよい、関係のなさそうな考えどうしが結びついて新しい発想が生まれる、という主張を、多くの人が経験している身近な場面で裏づけるため。",
         wrong_sum=[("多くの人は、シャワーを浴びているときやバスを待っているときに、よいアイデアを思いつく。", "第2段落の具体例だけをまとめており、筆者の主張（短い退屈は創造的に考える余地を与える）が入っていない。"),
                    ("退屈は意欲を下げて人を不幸にするので、スマートフォンなどを使って退屈な時間をなくすべきだ。", "第3段落の「長く続く退屈」の限界を主張と取り違えており、結論（少しの退屈は敵ではない）と逆の内容になっている。")],
         opinion="I agree with the writer. When I walk home without music, I often think of good ideas for my essays."),
    dict(key="GARD", title="Gardens That Grow Communities",
         paras=["In many cities, people live close to one another but rarely talk with their neighbors. Some people do not even know the names of the people next door. How can city residents build stronger connections?",
                "One answer is a community garden. In a community garden, people who live in the same area share a piece of land and grow vegetables and flowers together. While they are working, they naturally start talking about the weather, their plants, and their daily lives. As a result, people who were once strangers can become friends.",
                "Community gardens also help in other ways. Children can learn where food comes from, and older people can share their knowledge of farming. In addition, the gardens make the area greener and more beautiful.",
                "Of course, a garden needs time and care, and not everyone has free time. Still, even a small garden can bring people together. Working side by side with our neighbors may be one of the simplest ways to make a city feel like home."],
         roles=[("intro", "都市では隣人とほとんど話さないという問題を示し、どうすればつながりを築けるかと問いかけている", []),
                ("solution", "コミュニティガーデンで一緒に作業するうちに自然に会話が生まれ、友人になれるという解決策を示している", ["example", "benefit"]),
                ("benefit", "子どもの学び、高齢者の知識の共有、地域の緑化という別の利点を加えている", ["example"]),
                ("conclusion", "時間がかかるという難点を認めたうえで、小さな庭でも人々を結びつけられるとまとめている", ["contrast"])],
         main="Community gardens can help city residents build connections with their neighbors.",
         main_wrong=[("Children can learn where food comes from in community gardens.", "narrow"), ("Cities are becoming more and more crowded.", "broad"),
                     ("Community gardens take too much time, so they are not useful.", "contra")],
         title_ok="Gardens That Bring Neighbors Together",
         title_wrong=[("How to Grow Vegetables at Home", "off"), ("Learning Where Food Comes From", "narrow"), ("Why Cities Are Lonely Places", "narrow")],
         details=[("What problem does the writer describe in the first paragraph?", "People in cities often do not talk with their neighbors.",
                   [("There is not enough land in cities for farming.", "土地の不足は第1段落で述べられていない。"),
                    ("Vegetables in cities are too expensive.", "野菜の値段については書かれていない。"),
                    ("Older people do not know how to grow plants.", "第3段落では、高齢者は農業の知識を伝えられると述べており、逆である。")]),
                  ("How do strangers become friends in a community garden?", "They start talking naturally while working together.",
                   [("They are told to introduce themselves at the first meeting.", "自己紹介をするよう言われるとは書かれていない。"),
                    ("They sell their vegetables to one another.", "野菜を売り合うとは書かれていない。"),
                    ("They take part in a cooking contest.", "料理コンテストは本文に出てこない。")]),
                  ("What is one difficulty of a community garden mentioned in the passage?", "It needs time and care.",
                   [("It is too expensive to start.", "費用については書かれていない。"),
                    ("It makes the area less beautiful.", "第3段落では、地域をより美しくすると述べている。"),
                    ("Children cannot join it.", "第3段落で、子どもは食べ物の由来を学べると述べている。")])],
         trues=["In a community garden, people from the same area share land.", "Older people can teach others about farming in the garden.", "The writer admits that not everyone has free time."],
         falses=[("The writer says only large gardens can bring people together.", "第4段落で、小さな庭でも人々を結びつけられると述べている。"),
                 ("Community gardens make cities less green.", "第3段落で、地域をより緑豊かで美しくすると述べている。"),
                 ("Children are not allowed to work in community gardens.", "第3段落で、子どもたちは食べ物の由来を学べると述べている。"),
                 ("Most people in cities know all of their neighbors well.", "第1段落で、隣人の名前さえ知らない人もいると述べている。")],
         summary="都市では近所付き合いが少ないが、地域の人が土地を共有して野菜や花を育てるコミュニティガーデンでは自然に会話が生まれ、人々のつながりを築ける。",
         skeys=[("都市で隣人とのつながりが弱いという問題に触れている", 2), ("コミュニティガーデンで一緒に作業すると会話が生まれることを述べている", 3), ("人々のつながりを築けるという主張でまとめている", 3)],
         exq="第2段落で、コミュニティガーデンで見知らぬ人どうしが友人になれるのはなぜだと述べられているか。日本語で説明しなさい。",
         exa="同じ土地で一緒に作業をしているうちに、天気や植物、日々の生活について自然に話し始めるから。",
         wrong_sum=[("コミュニティガーデンでは、子どもは食べ物の由来を学び、高齢者は農業の知識を伝えることができる。", "第3段落の補足的な利点だけをまとめており、中心の主張（隣人どうしのつながりを築ける）が入っていない。"),
                    ("庭の世話には時間がかかり、暇のない人も多いので、都市でコミュニティガーデンを作るのは難しい。", "第4段落の Of course で認めた難点を主張と取り違えている。筆者は Still に続けて、小さな庭でも人々を結びつけられると述べている。")],
         opinion="I think community gardens are a good idea because working together is an easy way to start a conversation."),
    dict(key="MIST", title="Mistakes as Teachers",
         paras=["Many students are afraid of making mistakes. In class, they stay quiet because they do not want to give a wrong answer in front of others. They feel that a mistake shows they are not smart.",
                "However, mistakes are an important part of learning. When we make a mistake, we find out exactly what we do not understand yet. For example, if you get a math problem wrong and check each step, you can see where your thinking went off track. The next time, you are much less likely to make the same mistake.",
                "This is true outside school as well. Athletes watch videos of their failed plays, and scientists learn from experiments that do not work. In both cases, people improve by looking carefully at what went wrong.",
                "Therefore, we should change the way we think about mistakes. A mistake is not proof that we are not smart; it is information that shows us how to improve. If we are willing to make mistakes and learn from them, we will grow faster."],
         roles=[("intro", "多くの生徒が間違いを恐れて発言しないという、よく見られる考え方を示している", ["counter"]),
                ("counter", "However に続けて、間違いは学びの重要な一部だと反論し、数学の例で説明している", ["example", "contrast", "benefit"]),
                ("example", "運動選手や科学者という学校の外の例を加え、間違いから学ぶことが広く当てはまると示している", ["benefit"]),
                ("conclusion", "間違いは賢くない証拠ではなく改善のための情報だと考え方を改めるべきだとまとめている", [])],
         main="Mistakes help us learn, so we should not be afraid of making them.",
         main_wrong=[("Athletes watch videos of their failed plays.", "narrow"), ("Students have many different problems at school.", "broad"),
                     ("Students who make mistakes are not smart.", "contra")],
         title_ok="Learning Through Mistakes",
         title_wrong=[("How Athletes Train", "narrow"), ("Math Problems for Beginners", "off"), ("Why Students Stay Quiet in Class", "narrow")],
         details=[("Why do many students stay quiet in class?", "They do not want to give a wrong answer in front of others.",
                   [("They already know all the answers.", "答えをすべて知っているとは書かれていない。"),
                    ("They are not interested in the class.", "授業に興味がないとは書かれていない。"),
                    ("Their teachers tell them not to speak.", "先生が話すなと言うとは書かれていない。")]),
                  ("What can we find out when we make a mistake, according to the writer?", "What we do not understand yet.",
                   [("How smart other students are.", "ほかの生徒の賢さについては書かれていない。"),
                    ("Which teacher is the best.", "先生の比較は本文に出てこない。"),
                    ("How to avoid all difficult problems.", "難しい問題を避ける方法は書かれていない。")]),
                  ("What do scientists do, according to the passage?", "They learn from experiments that do not work.",
                   [("They only do experiments that always work.", "第3段落では、うまくいかない実験から学ぶと述べている。"),
                    ("They watch videos of athletes.", "映像を見るのは運動選手で、科学者ではない。"),
                    ("They never check what went wrong.", "第3段落では、何がうまくいかなかったかを注意深く見ることで上達すると述べている。")])],
         trues=["Checking each step of a wrong answer can show where our thinking went wrong.", "The writer believes that mistakes give us useful information.",
                "Learning from mistakes is useful outside school too."],
         falses=[("The writer says a mistake shows that a person is not smart.", "第4段落で、間違いは賢くない証拠ではないと述べている。"),
                 ("Athletes avoid watching their failed plays.", "第3段落で、失敗したプレーの映像を見ると述べている。"),
                 ("Checking a wrong answer makes us more likely to repeat the mistake.", "第2段落で、同じ間違いをする可能性はずっと低くなると述べている。"),
                 ("The writer thinks we should try never to make mistakes.", "第4段落で、間違いを恐れずそこから学べば速く成長すると述べている。")],
         summary="間違いは、自分がまだ理解していない点を教えてくれる情報であり、学校の内外で人はそこから学んで上達する。だから間違いを恐れず、そこから学ぶべきだ。",
         skeys=[("間違いは理解していない点を教えてくれることを述べている", 3), ("学校の外でも当てはまることに触れている", 2), ("間違いを恐れず学ぶべきだという主張でまとめている", 3)],
         exq="第4段落で筆者は、間違いを何だと言いかえているか。また、そのように考えるべき理由を本文に即して日本語で説明しなさい。",
         exa="間違いは賢くない証拠ではなく、どうすれば上達できるかを示す情報だと言いかえている。間違いを見直せば、まだ理解していない点がはっきりわかり、次に同じ間違いをしにくくなるから。",
         wrong_sum=[("運動選手は失敗したプレーの映像を見て、科学者はうまくいかなかった実験から学ぶ。", "第3段落の具体例だけをまとめており、筆者の主張（間違いを恐れず学ぶべきだ）が入っていない。"),
                    ("多くの生徒は間違えるのを恐れて、授業中に発言しない。", "第1段落の問題提起だけをまとめており、However 以降の筆者の主張が抜けている。")],
         opinion="I agree with the writer because I learned the most from the questions I got wrong on my tests."),
    dict(key="BIKE", title="The Bicycle: A Small Answer to Big Problems",
         paras=["Every morning, roads in many cities are full of cars. Traffic jams waste people's time, and the exhaust from cars makes the air dirty. City governments are looking for ways to solve these problems.",
                "One simple solution is to encourage people to ride bicycles. Bicycles do not need fuel, so they do not produce exhaust. They also take up much less space than cars, so more people can travel on the same road. In addition, riding a bicycle is good exercise.",
                "On the other hand, cycling in a city can be dangerous if there are no safe lanes for bicycles. Bad weather and long distances can also make cycling difficult. For these reasons, some people hesitate to choose bicycles.",
                "Therefore, cities need to do more than simply tell people to ride bicycles. If they build safe bicycle lanes and places to park bicycles, more people will feel comfortable cycling. In this way, a small change in how we travel can help with big problems."],
         roles=[("intro", "都市の渋滞と排気ガスによる大気の汚れという問題を示している", []),
                ("solution", "自転車の利用を勧めるという解決策と、その理由（排気ガスを出さない、場所をとらない）を示している", ["benefit"]),
                ("contrast", "安全な車線がないと危険で、天候や距離の問題もあるという自転車の難点を指摘している", []),
                ("conclusion", "都市は安全な車線や駐輪場を整えるべきだと、具体的な提案でまとめている", ["solution"])],
         main="If cities make cycling safe and convenient, bicycles can help reduce traffic and air pollution.",
         main_wrong=[("Riding a bicycle is good exercise.", "narrow"), ("Many people around the world live in cities.", "broad"),
                     ("Bicycles are too dangerous, so cities should not encourage cycling.", "contra")],
         title_ok="How Bicycles Can Help Our Cities",
         title_wrong=[("The History of the Bicycle", "off"), ("Cycling as Exercise", "narrow"), ("Traffic Jams in the Morning", "narrow")],
         details=[("What two problems caused by cars are mentioned in the first paragraph?", "Traffic jams and dirty air.",
                   [("Noise and expensive fuel.", "騒音や燃料の値段は本文に出てこない。"),
                    ("Accidents and a lack of parking spaces.", "事故や駐車場不足は第1段落で述べられていない。"),
                    ("Long distances and bad weather.", "距離と天候は、自転車の難点として第3段落で述べられている。")]),
                  ("Why can more people travel on the same road by bicycle?", "Because bicycles take up less space than cars.",
                   [("Because bicycles are faster than cars.", "自転車が車より速いとは書かれていない。"),
                    ("Because bicycles do not need fuel.", "燃料が不要なのは、排気ガスを出さない理由として述べられている。"),
                    ("Because there are already many bicycle lanes.", "第3段落では、安全な車線がない場合の危険が述べられており、車線が多いとは書かれていない。")]),
                  ("What does the writer suggest cities should do?", "Build safe bicycle lanes and places to park bicycles.",
                   [("Tell people to stop driving cars.", "車の運転をやめるよう言うとは書かれていない。また、勧めるだけでは不十分と述べている。"),
                    ("Make roads wider for cars.", "車のために道路を広げるとは書かれていない。"),
                    ("Ask people to ride bicycles only on sunny days.", "晴れた日だけ乗るよう求めるとは書かれていない。")])],
         trues=["Bicycles do not produce exhaust because they need no fuel.", "Some people do not choose bicycles because cycling can be dangerous.",
                "The writer thinks that simply telling people to ride bicycles is not enough."],
         falses=[("Bicycles take up more space on roads than cars.", "第2段落で、車よりずっと場所をとらないと述べている。"),
                 ("The writer says that bad weather has no effect on cycling.", "第3段落で、悪天候が自転車の利用を難しくすると述べている。"),
                 ("City governments are not interested in traffic problems.", "第1段落で、市当局は解決策を探していると述べている。"),
                 ("The writer believes that cycling is always safe in cities.", "第3段落で、安全な車線がないと危険になりうると述べている。")],
         summary="自転車は排気ガスを出さず場所もとらないので、渋滞や大気汚染の解決に役立つ。ただし安全面などの課題があるため、都市は専用車線や駐輪場を整えるべきだ。",
         skeys=[("自転車が渋滞や大気汚染の解決に役立つことを述べている", 3), ("安全面などの課題に触れている", 2), ("都市が環境を整えるべきだという主張でまとめている", 3)],
         exq="第4段落の冒頭の Therefore は、どのような内容を受けて、どのような結論を導いているか。日本語で説明しなさい。",
         exa="第3段落の、安全な車線がないと危険で、天候や距離の問題もあるため自転車を選ばない人がいる、という内容を受けて、都市は自転車に乗るよう勧めるだけでなく、安全な専用車線や駐輪場を整備する必要があるという結論を導いている。",
         wrong_sum=[("自転車に乗ることはよい運動になる。", "第2段落で追加された利点の1つだけをまとめており、文章全体の主張（都市が環境を整えれば自転車が問題の解決に役立つ）が入っていない。"),
                    ("都市で自転車に乗るのは危険で、天気や距離の問題もあるので、自転車は都市の交通には向かない。", "第3段落の On the other hand で示した難点を主張と取り違えている。筆者は Therefore に続けて、環境を整えるべきだと述べている。")],
         opinion="I agree with the writer. If there were safe bicycle lanes in my town, I would ride my bicycle to school every day."),
    dict(key="LIBR", title="Libraries Are More Than Books",
         paras=["When people think of a library, they usually imagine a quiet room full of books. For a long time, that image was correct. Libraries were mainly places to borrow books and study in silence.",
                "Today, however, many libraries are changing. Some offer free Internet access for people who do not have it at home. Others hold events such as language classes, computer lessons, and story time for small children. In some libraries, there are even rooms where people can talk and work together on projects.",
                "Why are libraries changing in this way? One reason is that people can now find a lot of information online. To stay useful, libraries have started to offer services that people cannot easily get elsewhere.",
                "In other words, libraries are becoming community centers where people can learn and meet. Books are still important, but a modern library is also a place that connects people with information and with one another."],
         roles=[("intro", "図書館は本を借りて静かに勉強する場所だという、従来のイメージを示している", []),
                ("example", "インターネットの提供や講座、共同作業の部屋など、変わりつつある図書館の具体例を挙げている", ["contrast", "counter", "benefit"]),
                ("cause", "オンラインで情報が得られるようになったことを、図書館が変わる理由として説明している", []),
                ("conclusion", "図書館は人々が学び交流する地域の拠点になりつつあると、言いかえてまとめている", [])],
         main="Libraries are changing into places where people can learn and connect with one another, not just borrow books.",
         main_wrong=[("Some libraries hold story time for small children.", "narrow"), ("Books have been important to people for a long time.", "broad"),
                     ("Libraries should remain quiet places only for reading books.", "contra")],
         title_ok="The Changing Role of Libraries",
         title_wrong=[("How to Find Information Online", "off"), ("Story Time for Small Children", "narrow"), ("Why We Should Read More Books", "off")],
         details=[("What did libraries mainly do in the past?", "They lent books and gave people a quiet place to study.",
                   [("They held computer lessons.", "コンピューター教室は、今日の図書館の変化の例として第2段落で挙げられている。"),
                    ("They offered free Internet access.", "無料のインターネット接続は、今日の変化の例である。"),
                    ("They were places to talk and work together.", "話し合いや共同作業の部屋は、今日の一部の図書館の例である。")]),
                  ("Why have libraries started to offer new services?", "Because people can now find a lot of information online.",
                   [("Because people have stopped reading books.", "本を読まなくなったとは書かれていない。第4段落では、本は今でも重要だと述べている。"),
                    ("Because libraries have too many books.", "本が多すぎるとは書かれていない。"),
                    ("Because children do not like quiet rooms.", "子どもが静かな部屋を嫌うとは書かれていない。")]),
                  ("Which of the following is NOT mentioned as a service that some libraries offer today?", "Selling new books to visitors",
                   [("Free Internet access", "第2段落で、一部の図書館のサービスとして挙げられている。"),
                    ("Language classes", "第2段落で、催しの例として挙げられている。"),
                    ("Story time for small children", "第2段落で、催しの例として挙げられている。")])],
         trues=["Some libraries have rooms where people can work together.", "The writer says books are still important.",
                "Libraries want to provide services that are hard to get elsewhere."],
         falses=[("The writer says that books are no longer necessary in libraries.", "第4段落で、本は今でも重要だと述べている。"),
                 ("All libraries today have stopped lending books.", "本の貸し出しをやめたとは書かれていない。新しいサービスを加えていると述べている。"),
                 ("Libraries hold events only for adults.", "第2段落で、小さな子ども向けの読み聞かせを挙げている。"),
                 ("People cannot find much information online.", "第3段落で、今ではオンラインで多くの情報が見つかると述べている。")],
         summary="図書館は本を借りて静かに勉強する場所だったが、情報をオンラインで得られる今、他では得にくいサービスを提供し、人々が学び交流する地域の拠点へと変わりつつある。",
         skeys=[("従来の図書館のイメージに触れている", 2), ("オンラインで情報が得られることが変化の理由だと述べている", 3), ("人々が学び交流する場へ変わりつつあるという主張でまとめている", 3)],
         exq="第3段落で述べられている、図書館が変わりつつある理由を、日本語で説明しなさい。",
         exa="今ではインターネットで多くの情報を得られるようになったので、図書館が役に立ち続けるために、他の場所では簡単に得られないサービスを提供し始めたから。",
         wrong_sum=[("図書館では、語学教室やコンピューター教室、子ども向けの読み聞かせなどの催しが開かれている。", "第2段落の具体例を並べただけで、筆者の主張（図書館は人々が学び交流する地域の拠点になりつつある）が入っていない。"),
                    ("インターネットで情報が手に入るので、図書館の本はもう必要なくなった。", "第4段落で本は今でも重要だと述べており、本文と逆の内容になっている。")],
         opinion="I agree with the writer. My local library has a study room, and I often work there with my friends."),
    dict(key="SHAR", title="Why Buy When You Can Borrow?",
         paras=["Think about the things in your home that you rarely use. Many families own a drill, a tent, or a large cooking pot that they use only once or twice a year. These items take up space and cost money, but most of the time they just sit in a closet.",
                "Because of this, some communities have started \"libraries of things.\" Like a book library, these places lend items to members for a short time. For example, a family that wants to go camping can borrow a tent instead of buying one.",
                "Sharing items in this way has several benefits. People save money and space at home. Also, if fewer items are produced, fewer resources are used, which is better for the environment.",
                "To sum up, we do not always need to own everything we use. By borrowing and sharing, we can live more simply and protect the environment at the same time."],
         roles=[("intro", "めったに使わない物が場所とお金の負担になっているという問題を示している", []),
                ("solution", "物を短期間貸し出す「物の図書館」という解決策を、テントの例とともに示している", ["example"]),
                ("benefit", "お金と場所の節約、資源の使用の削減という共有の利点を説明している", []),
                ("conclusion", "使う物すべてを所有する必要はなく、借りて共有すれば簡素に暮らし環境も守れるとまとめている", [])],
         main="Borrowing and sharing items we rarely use can save money and help the environment.",
         main_wrong=[("A family can borrow a tent to go camping.", "narrow"), ("Families keep many different things in their homes.", "broad"),
                     ("We should buy our own tools so that we can use them at any time.", "contra")],
         title_ok="Sharing Instead of Owning",
         title_wrong=[("How to Enjoy Camping", "narrow"), ("Cleaning Your Closet", "off"), ("A Short History of Book Libraries", "off")],
         details=[("What is the problem with items that people rarely use?", "They take up space and cost money.",
                   [("They break easily.", "壊れやすいとは書かれていない。"),
                    ("They are difficult to use.", "使いにくいとは書かれていない。"),
                    ("They are hard to find in stores.", "店で見つけにくいとは書かれていない。")]),
                  ("How is a \"library of things\" similar to a book library?", "It lends items to members for a short time.",
                   [("It sells used books.", "古本を売るとは書かれていない。"),
                    ("It is open only to children.", "子どもだけが利用できるとは書かれていない。"),
                    ("It gives items to people to keep forever.", "第2段落では、短期間貸し出すと述べている。")]),
                  ("Why is sharing items better for the environment?", "Because fewer items need to be produced.",
                   [("Because people go camping more often.", "キャンプの回数と環境の関係は書かれていない。"),
                    ("Because closets become larger.", "押し入れが大きくなるとは書かれていない。"),
                    ("Because people buy more tools.", "共有すれば買う物は減る。本文と逆である。")])],
         trues=["Some families use certain items only once or twice a year.", "A library of things lends items for a short time.",
                "The writer thinks sharing can help us live more simply."],
         falses=[("A library of things sells items at low prices.", "第2段落で、短期間貸し出すと述べており、販売するとは書かれていない。"),
                 ("The writer says we must own everything we use.", "第4段落で、使う物すべてを所有する必要はないと述べている。"),
                 ("Sharing items costs families more money.", "第3段落で、お金と場所の節約になると述べている。"),
                 ("Producing more items is better for the environment.", "第3段落で、生産が減れば資源の使用も減り、環境によいと述べている。")],
         summary="めったに使わない物は場所とお金の負担になる。「物の図書館」などで物を借りて共有すれば、お金と場所を節約でき、資源の使用も減って環境にもよい。",
         skeys=[("めったに使わない物が負担になるという問題に触れている", 2), ("物を借りて共有するという方法を述べている", 3), ("節約と環境への利点でまとめている", 3)],
         exq="第3段落で述べられている、物を共有することの利点を2つ、日本語で説明しなさい。",
         exa="①人々はお金と家の中の場所を節約できる。②生産される物が減れば使われる資源も減るので、環境によい。",
         wrong_sum=[("キャンプに行きたい家族は、テントを買わずに借りることができる。", "第2段落の具体例だけをまとめており、筆者の主張（借りて共有すれば節約でき環境にもよい）が入っていない。"),
                    ("多くの家庭には、年に1、2回しか使わない物がたくさんある。", "第1段落の問題提起だけをまとめており、解決策と筆者の主張が抜けている。")],
         opinion="I agree with the writer. My family has a tent that we used only once, so borrowing one would have been better."),
    dict(key="READ", title="The Power of Reading Aloud",
         paras=["Most students read English silently. They move their eyes across the page and try to understand the meaning. This is an important skill, but there is another way of reading that is often forgotten: reading aloud.",
                "Reading aloud helps learners in several ways. First, it makes them pay attention to the sounds of words and the rhythm of sentences. Second, saying sentences out loud many times helps them remember useful expressions. As a result, many learners find it easier to speak and listen.",
                "However, reading aloud is not effective if learners do not understand what they are reading. Simply making sounds without thinking about the meaning does not help much. Learners should first understand the text and then read it aloud.",
                "In conclusion, reading aloud is a simple but powerful way to improve English. If learners understand a text first and then read it aloud again and again, they can build skills that silent reading alone cannot give them."],
         roles=[("intro", "多くの生徒は黙読するが、忘れられがちな音読という読み方があると話題を導入している", []),
                ("benefit", "音や文のリズムへの注意、表現の定着という音読の利点を First / Second で説明している", ["cause", "example"]),
                ("contrast", "意味を理解せずに音読しても効果が薄いという限界を述べている", []),
                ("conclusion", "理解してから繰り返し音読すれば英語力を伸ばせるとまとめている", [])],
         main="Reading aloud, after understanding a text, is an effective way to improve English.",
         main_wrong=[("Reading aloud helps learners pay attention to rhythm.", "narrow"), ("Many students study English at school.", "broad"),
                     ("Silent reading is the only useful way to read English.", "contra")],
         title_ok="Why You Should Read English Aloud",
         title_wrong=[("How to Read Faster", "off"), ("The Rhythm of English Songs", "off"), ("Learning to Read Silently", "contra")],
         details=[("What do most students do when they read English?", "They read silently.",
                   [("They read aloud with their friends.", "第1段落では、多くの生徒は黙読すると述べている。"),
                    ("They listen to recordings.", "録音を聞くとは書かれていない。"),
                    ("They translate every word into Japanese.", "すべての語を和訳するとは書かれていない。")]),
                  ("According to the passage, why does reading aloud help learners remember expressions?", "Because they say sentences out loud many times.",
                   [("Because they write the sentences in a notebook.", "ノートに書くとは書かれていない。"),
                    ("Because they read very fast.", "速く読むとは書かれていない。"),
                    ("Because they read without thinking about the meaning.", "第3段落では、意味を考えずに声を出しても効果は薄いと述べている。")]),
                  ("What should learners do before reading a text aloud?", "Understand the text.",
                   [("Memorize every word in it.", "すべての語を暗記するとは書かれていない。"),
                    ("Listen to music.", "音楽を聞くとは書かれていない。"),
                    ("Read it as fast as possible.", "できるだけ速く読むとは書かれていない。")])],
         trues=["Reading aloud makes learners pay attention to sounds and rhythm.", "Making sounds without thinking about meaning does not help much.",
                "The writer says learners should read a text aloud again and again."],
         falses=[("The writer says silent reading is not an important skill.", "第1段落で、黙読は重要な技能だと述べている。"),
                 ("Reading aloud is effective even if learners do not understand the text.", "第3段落で、理解していなければ効果的でないと述べている。"),
                 ("Reading aloud makes it harder to speak and listen.", "第2段落で、話したり聞いたりしやすくなると述べている。"),
                 ("Learners should read aloud first and try to understand the text later.", "第3段落で、まず理解してから音読するべきだと述べている。")],
         summary="音読は語の音や文のリズムに注意を向けさせ、表現の定着を助ける。ただし意味の理解が前提で、理解した文を繰り返し音読すれば英語力を伸ばせる。",
         skeys=[("音読の利点（音・リズムへの注意、表現の定着）を述べている", 3), ("意味の理解が前提であることに触れている", 2), ("理解してから繰り返し音読すべきだという主張でまとめている", 3)],
         exq="第3段落で筆者が述べている、音読が効果的でない場合とはどのような場合か。また、その場合どうすべきだと述べているか。日本語で説明しなさい。",
         exa="読んでいる内容を理解しないまま、意味を考えずにただ声に出している場合。その場合は、まず文章を理解してから音読するべきだと述べている。",
         wrong_sum=[("音読をすると、語の音や文のリズムに注意を払うようになる。", "第2段落の利点の1つだけをまとめており、筆者の主張（理解してから繰り返し音読すれば英語力が伸びる）が入っていない。"),
                    ("意味を考えずに声を出しても効果がないので、音読より黙読のほうがよい。", "第3段落の限界を主張と取り違えており、結論（音読は英語力を伸ばす有力な方法だ）と逆の内容になっている。")],
         opinion="I agree with the writer. When I read my textbook aloud, I can remember new expressions more easily."),
    dict(key="VOLU", title="What Volunteers Gain",
         paras=["Volunteer work is often seen as something we do only for others. People clean parks, help at events, or visit elderly people without being paid. It is easy to think that volunteers give their time and get nothing back.",
                "In fact, volunteers often gain a great deal. For example, a high school student who helps at a local festival may learn how to work in a team and how to talk with adults she has never met. These are skills that are hard to learn in a classroom.",
                "Volunteering can also help young people discover what they want to do in the future. A student who reads picture books to children at a library might realize that she enjoys teaching. Experiences like this can guide students when they choose a career.",
                "Thus, volunteer work is not a one-way gift. When we help others, we also help ourselves grow. Students who are looking for new experiences should consider volunteering in their communities."],
         roles=[("intro", "ボランティアは他人のためだけで何も得ないという、一般的な見方を示している", []),
                ("counter", "In fact に続けて、ボランティアは多くを得ると反論し、祭りの手伝いの例で説明している", ["example", "benefit", "contrast"]),
                ("benefit", "将来やりたいことに気づけるという別の利点を、読み聞かせの例とともに加えている", ["example"]),
                ("conclusion", "ボランティアは一方通行の贈り物ではなく自分も成長できると述べ、参加を勧めている", [])],
         main="Volunteer work helps not only others but also the volunteers themselves.",
         main_wrong=[("A student can read picture books to children at a library.", "narrow"), ("Many people work in their communities.", "broad"),
                     ("Volunteers give their time and get nothing in return.", "contra")],
         title_ok="Helping Others, Helping Ourselves",
         title_wrong=[("How to Clean a Park", "off"), ("Choosing a Career Early", "narrow"), ("Festivals in Our Town", "off")],
         details=[("What do many people think about volunteer work?", "Volunteers give their time and get nothing back.",
                   [("Volunteers are paid a lot of money.", "第1段落で、ボランティアは報酬なしで行うと述べている。"),
                    ("Volunteer work is only for adults.", "大人だけのものとは書かれていない。高校生の例も挙がっている。"),
                    ("Volunteer work is too difficult for students.", "学生には難しすぎるとは書かれていない。")]),
                  ("What can a student learn by helping at a local festival?", "How to work in a team and talk with adults.",
                   [("How to cook festival food.", "祭りの料理の作り方は書かれていない。"),
                    ("How to read picture books.", "絵本の読み聞かせは、図書館での別の例である。"),
                    ("How to clean parks.", "公園の清掃は、ボランティアの種類の例として第1段落に出てくるだけである。")]),
                  ("How can volunteering help young people with their future?", "It can help them discover what they want to do.",
                   [("It can help them earn money for college.", "第1段落で、ボランティアは報酬なしで行うと述べている。"),
                    ("It can help them avoid working in teams.", "第2段落では、チームで働く方法を学べると述べており、逆である。"),
                    ("It can help them get better grades in every class.", "成績がよくなるとは書かれていない。")])],
         trues=["Volunteers are not paid for their work.", "Some skills learned through volunteering are hard to learn in a classroom.",
                "The writer encourages students to volunteer in their communities."],
         falses=[("The writer agrees that volunteers get nothing back.", "第2段落で In fact に続けて、多くを得ると述べている。"),
                 ("Students can learn teamwork only in the classroom.", "第2段落で、教室では学びにくい技能だと述べている。"),
                 ("Reading to children has nothing to do with choosing a career.", "第3段落で、教えることが好きだと気づき、進路選びの手がかりになりうると述べている。"),
                 ("The writer says volunteer work is a one-way gift.", "第4段落で、一方通行の贈り物ではないと述べている。")],
         summary="ボランティアは他人のためだけの活動と思われがちだが、実際には協力の仕方や大人との話し方を学び、将来やりたいことに気づくなど、自分自身も成長できる。",
         skeys=[("他人のためだけという一般的な見方に触れている", 2), ("技能の習得や将来の目標への気づきなど、得られるものを述べている", 3), ("自分自身も成長できるという主張でまとめている", 3)],
         exq="第4段落の a one-way gift とはどういう意味か。筆者がボランティアをそう呼ばない理由とともに日本語で説明しなさい。",
         exa="「一方通行の贈り物」、つまりボランティアが他人に時間を与えるだけで何も得ないという意味。実際にはボランティアは技能を身につけたり将来の目標に気づいたりして自分自身も成長できるので、筆者はそう呼ばない。",
         wrong_sum=[("地域の祭りを手伝う高校生は、チームで働く方法を学ぶことができる。", "第2段落の具体例だけをまとめており、筆者の主張（ボランティアは自分自身も成長させる）が入っていない。"),
                    ("ボランティアは、報酬なしで他人のために時間を使う活動である。", "第1段落の一般的な見方だけをまとめており、In fact 以降の筆者の主張が抜けている。")],
         opinion="I agree with the writer. When I helped at a summer event, I learned how to explain things clearly to small children."),
]
PBY = {p["key"]: p for p in PASSAGES}


def pstim(p):
    return stim(f"RD-{p['key']}", "\n\n".join(p["paras"]), "passage", f"次の英文（“{p['title']}”）を読んで、あとの問いに答えなさい。", source="オリジナル")


def head(p):
    return f"英文“{p['title']}”について答えなさい。"


MAIN_WHY = {
    "narrow": ("本文の一部（具体例や1つの段落）だけを述べており、文章全体の主旨としては狭すぎる。", "具体例と主旨の混同"),
    "broad": ("本文の話題よりも一般的・広すぎる内容で、筆者の主張を表していない。", "話題と主旨の混同"),
    "contra": ("本文の主張と逆の内容である。反対の視点や一般的な考えを、筆者の主張と取り違えている。", "譲歩・反対の視点と主張の混同"),
    "off": ("本文で扱われていない内容である。", "本文にない情報の読みこみ"),
}


# ======================================================================
# 短文・段落の資料
# ======================================================================

FUNCS = ["逆接", "例示", "追加", "結果", "対比", "言いかえ", "結論・要約"]
FUNC_DESC = {
    "逆接": "前の内容から予想されることと反対の内容が続く",
    "例示": "前の一般的な内容の具体例が続く",
    "追加": "前の内容に同じ方向の情報を付け加える",
    "結果": "前の内容が原因となって起きる結果が続く",
    "対比": "前の内容と別のものを比べ、違いを示す",
    "言いかえ": "前の内容を別の言葉で説明し直す",
    "結論・要約": "それまでの内容をまとめる",
}
FUNC_MARKERS = {
    "逆接": ["However", "Nevertheless", "Even so"],
    "例示": ["For example", "For instance"],
    "追加": ["In addition", "Moreover", "Besides"],
    "結果": ["As a result", "Therefore", "Consequently"],
    "対比": ["On the other hand", "In contrast"],
    "言いかえ": ["In other words", "That is"],
    "結論・要約": ["In short", "To sum up", "In conclusion"],
}

# (前の文, マーカー, 後ろの文, 働き, 関係の説明, 誤答から除く働き)
MARK = [
    ("I studied hard for the test.", "However", "I could not get a good score.", "逆接", "一生懸命勉強した → よい点がとれなかった（予想と反対の結果）", ["対比"]),
    ("Some animals sleep through the winter.", "For example", "bears sleep for several months.", "例示", "冬眠する動物がいる → クマ（その具体例）", ["追加"]),
    ("This phone is light and easy to carry.", "In addition", "it is cheaper than other models.", "追加", "軽く持ち運びやすい ＋ 値段も安い（同じ方向の長所の追加）", ["結論・要約"]),
    ("It rained heavily all night.", "As a result", "the morning game was canceled.", "結果", "一晩中大雨だった → 朝の試合が中止（原因と結果）", ["結論・要約"]),
    ("My brother loves sports.", "On the other hand", "my sister prefers reading.", "対比", "兄はスポーツ好き ⇔ 妹は読書好き（2人の違い）", ["逆接"]),
    ("He is a vegetarian.", "In other words", "he does not eat meat.", "言いかえ", "菜食主義者 ＝ 肉を食べない（同じ内容の言い直し）", ["結果", "例示"]),
    ("Exercise improves both our health and our mood.", "In short", "it makes our lives better.", "結論・要約", "健康も気分もよくなる → 要するに生活がよくなる（まとめ）", ["結果", "言いかえ"]),
    ("The road was closed because of the snow.", "Therefore", "we had to take another route.", "結果", "雪で道路が閉鎖 → 別の道を通った（原因と結果）", ["結論・要約"]),
    ("The town has beautiful beaches.", "Moreover", "its seafood is famous all over the country.", "追加", "美しい海岸がある ＋ 海産物も有名（長所の追加）", ["結論・要約"]),
    ("Online shopping is very convenient.", "Nevertheless", "some people still prefer to shop in stores.", "逆接", "ネット通販は便利 → それでも店で買う人がいる（予想と反対）", ["対比"]),
    ("There are many easy ways to save energy at home.", "For instance", "you can turn off the lights when you leave a room.", "例示", "省エネの方法がある → 部屋を出るとき電気を消す（具体例）", ["追加"]),
    ("Life in a big city is busy and exciting.", "In contrast", "life in the countryside is quiet and slow.", "対比", "都会の生活 ⇔ 田舎の生活（2つの違い）", ["逆接"]),
    ("We finished all our work before noon.", "Consequently", "we were able to leave early.", "結果", "正午前に仕事を終えた → 早く帰れた（原因と結果）", ["結論・要約"]),
    ("Reading helps us learn new words, ideas, and ways of thinking.", "To sum up", "it is one of the best ways to grow as a person.", "結論・要約", "語・考え・考え方を学べる → まとめると成長の最良の方法（まとめ）", ["結果", "言いかえ"]),
]

# 段落の資料：(文のリスト, 主題文の番号, まとめの文の番号 or None, 段落の話題)
PARAS = [
    (["Japanese convenience stores offer far more than snacks and drinks.", "Customers can pay their bills, send packages, and print documents there.",
      "Some stores even have small spaces where people can sit and eat.", "For many people, the convenience store has become a part of daily life."], 0, 3, "コンビニエンスストアのサービス"),
    (["Sleep is not just a time when the body rests.", "While we sleep, the brain sorts the information we took in during the day.",
      "Important memories become stronger, and unimportant ones fade.", "That is why a good night's sleep before a test can be more helpful than studying all night."], 0, 3, "睡眠と記憶"),
    (["Last summer, our town started a program to collect used clothes.", "Residents brought shirts and jackets they no longer wore to the community center.",
      "The clothes were cleaned and given to people who needed them.", "This program showed that small actions by many people can make a big difference."], 3, None, "古着回収の取り組み"),
    (["Learning a musical instrument takes patience.", "At first, your fingers do not move the way you want them to.",
      "You may practice the same few notes for weeks without improving much.", "However, if you keep going, one day you will notice that you can play a whole song."], 0, None, "楽器の練習"),
    (["Many people think that cats do not care about their owners.", "However, cats show their feelings in quiet ways.",
      "For example, a cat may slowly blink at you or follow you from room to room.", "These small actions are signs that the cat trusts you."], 1, None, "猫の気持ちの表し方"),
    (["Bamboo is a very useful plant.", "Because it grows quickly, it can be harvested again and again.",
      "It is strong and light, so people use it to build houses and make furniture.", "Its young shoots can even be eaten."], 0, None, "竹の有用性"),
    (["Writing a diary in English is a good way to improve your writing.", "You can write about anything, such as what you ate or whom you met.",
      "Because you write a little every day, you gradually get used to expressing your ideas in English.", "In this way, a diary can turn writing into a daily habit."], 0, 3, "英語の日記"),
    (["In autumn, the leaves of many trees turn yellow.", "During spring and summer, leaves are green because they contain a green substance called chlorophyll.",
      "As the days get shorter and colder, trees stop making chlorophyll.", "When the green color fades, the yellow color that was hidden in the leaves becomes visible."], 0, None, "紅葉（黄葉）のしくみ"),
    (["Public transportation in a big city has many advantages.", "Trains and buses can carry a large number of people at once.",
      "They also reduce the number of cars on the road.", "For these reasons, many cities are trying to improve their train and bus services."], 0, 3, "公共交通機関の利点"),
    (["Maps on smartphones have changed the way we travel.", "In the past, travelers had to study paper maps before visiting a new place.",
      "Now, we can simply follow the directions on a screen.", "Some people worry, however, that we are losing the ability to find our own way."], 0, None, "スマートフォンの地図"),
    (["Recycling is important, but reducing waste is even better.", "When we recycle, we still use energy to collect and process the materials.",
      "If we do not create the waste in the first place, that energy is not needed.", "So the best choice is to buy only what we need and use things for a long time."], 0, 3, "リサイクルとごみの削減"),
    (["My grandmother has a simple rule for staying healthy.", "She walks for thirty minutes every morning, no matter what the weather is like.",
      "She also eats plenty of vegetables and goes to bed early.", "Although she is over eighty, she is still full of energy."], 0, None, "祖母の健康法"),
]
NUMS = ["①", "②", "③", "④"]


def numbered(sents):
    return " ".join(f"{NUMS[i]} {s}" for i, s in enumerate(sents))


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["concept", "computation"])
def marker_function(r):
    a, m, b, f, rel, excl = r.choice(MARK)
    pool = [x for x in FUNCS if x != f and x not in excl]
    wrongs = r.sample(pool, 3)
    why = {w: (f"「{w}」は{FUNC_DESC[w]}働き。この2文は「{rel}」という関係なので「{f}」である。", "ディスコースマーカーの働きの混同") for w in wrongs}
    return mc(f"次の英文の下線部のディスコースマーカーの働きとして最も適切なものを選びなさい。\n{a} [[u:{m}]], {b}", [f] + wrongs,
              f"{m} は「{f}」を表す。前後の関係：{rel}。", d=1,
              ap="マーカーの前の文と後ろの文の関係（反対・具体例・追加・原因と結果・違い・言い直し・まとめ）を先に日本語で考える。",
              steps=["前の文と後ろの文の意味をそれぞれ確認する。", f"2文の関係を考える：{rel}。", f"その関係を表す働きは「{f}」。"],
              alt=[f"{m} を同じ働きの別のマーカー（{'、'.join(x for x in FUNC_MARKERS[f] if x != m) or m}）に置きかえても文意が通るかを確かめる。"],
              pc=[("2文の関係をとらえている", 1), ("マーカーの働きを正しく選んでいる", 1)],
              pit=["マーカーの日本語訳だけを覚えていて、前後の関係から確かめない。"], why=why)


@gen("basic_check", 5, ["condition_check", "common_error"])
def marker_fill(r):
    a, m, b, f, rel, excl = r.choice(MARK)
    pool = [x for x in FUNCS if x != f and x not in excl]
    wf = r.sample(pool, 3)
    wrongs = [(r.choice(FUNC_MARKERS[x]), x) for x in wf]
    why = {w: (f"{w} は「{x}」（{FUNC_DESC[x]}）を表す。この2文は「{rel}」という関係なので合わない。", "ディスコースマーカーの働きの混同") for w, x in wrongs}
    return mc(f"2つの文の関係を考えて、（　）に入る最も適切な語句を選びなさい。\n{a} (　　), {b}", [m] + [w for w, _ in wrongs],
              f"{m}（{f}）が入る。前後の関係：{rel}。", d=2,
              ap="（　）の前後の文の関係を、「→（結果）」「⇔（対比）」「＋（追加）」「＝（言いかえ）」などの記号で表してから選ぶ。",
              steps=["前後の文の意味を確認する。", f"関係を考える：{rel}。", f"「{f}」を表すマーカーは {m}。"],
              alt=["選んだマーカーを入れた2文を日本語に訳し、つながりが自然かを確かめる。"],
              pc=[("2文の関係をとらえている", 1), ("適切なマーカーを選んでいる", 1)],
              pit=["前後の関係を考えずに、よく見る However などを選ぶ。"], why=why)


@gen("basic_check", 5, ["concept", "condition_check"])
def topic_sentence(r):
    sents, ti, ci, topic = r.choice(PARAS)
    ask_concl = ci is not None and r.random() < 0.4
    target = ci if ask_concl else ti
    label = "まとめの文（concluding sentence）" if ask_concl else "主題文（topic sentence）"
    others = [i for i in range(4) if i != target]

    def role(i):
        if i == ti:
            return "段落の中心の考えを述べた主題文"
        if i == ci:
            return "主題文の内容を言いかえてまとめた文"
        if sents[i].startswith("For example"):
            return "主題文を支える具体例"
        if sents[i].startswith("However") and i != ti:
            return "流れを転換する支持文"
        return "主題文を支える説明・具体的な情報"
    why = {NUMS[i]: (f"{NUMS[i]}は{role(i)}であり、{label}ではない。", "主題文と支持文の区別") for i in others}
    return mc(f"次の段落の{label}として最も適切なものを①〜④から選びなさい。\n{numbered(sents)}", NUMS,
              f"{NUMS[target]}。段落の話題は「{topic}」で、{NUMS[target]}は{role(target)}。", d=2, keep=True, ai=target,
              ap="「ほかのすべての文が説明している文はどれか」を考える。最初の文とは限らず、However の後ろや段落の最後に置かれることもある。",
              steps=[f"段落の話題をとらえる：{topic}。", "各文が一般的な考えか、具体的な説明・例かを分ける。", f"{label}は{NUMS[target]}。"],
              alt=[f"{NUMS[target]}を取り除くと段落の中心が見えなくなるかどうかを確かめる。"],
              pc=[("各文の働きを区別している", 1), ("正しい文を選んでいる", 1)],
              pit=["段落の最初の文を機械的に主題文とする。"], why=why)


@gen("basic_check", 5, ["computation", "concept"])
def detail(r):
    p = r.choice(PASSAGES)
    q, ok, wrongs = r.choice(p["details"])
    return mc(f"{head(p)}\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　本文の該当箇所を探し、言いかえに注意して照合する。", d=2, stim=pstim(p),
              ap="設問の中のキーワードを本文から探し、その前後を丁寧に読む。選択肢は本文の言いかえになっていることが多い。",
              steps=["設問のキーワードを確認する。", "本文で同じ語句・言いかえを探す。", "該当箇所と選択肢を照合する。", f"答え：{ok}"],
              alt=["誤りの選択肢について、本文のどこと食い違うか（書かれていない・逆・別の話）を1つずつ確かめる。"],
              pc=[("本文の該当箇所を見つけている", 1), ("正しい選択肢を選んでいる", 1)],
              pit=["本文に出てくる語句を含むだけの選択肢を選ぶ。"], why={w: (reason, "本文との照合不足") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["concept", "application"])
def main_or_title(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.5:
        ok, wrongs, what = p["main"], p["main_wrong"], "本文の主旨"
    else:
        ok, wrongs, what = p["title_ok"], p["title_wrong"], "本文に最もふさわしい題名"
    return mc(f"{head(p)}\n{what}として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　導入の問題提起と結論の段落を中心に、具体例を除いて筆者の主張をとらえる。", d=3, stim=pstim(p),
              ap="第1段落の問題提起と最終段落の結論を先に読み、筆者の主張をつかむ。具体例や反対の視点だけを述べた選択肢は外す。",
              steps=["第1段落で話題・問題提起を確認する。", "最終段落の結論（In short / Therefore など）を確認する。", "各選択肢が、狭すぎないか・広すぎないか・逆でないかを点検する。", f"答え：{ok}"],
              alt=["各段落の役割を書き出し、すべての段落の内容を含む選択肢を選ぶ。"],
              pc=[("問題提起と結論をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["具体例の内容を主旨として選ぶ。", "However の段落の内容を主旨として選ぶ。"], why={w: MAIN_WHY[k] for w, k in wrongs})


@gen("standard_practice", 5, ["concept", "condition_check"])
def paragraph_role(r):
    p = r.choice(PASSAGES)
    i = r.randrange(4)
    role, gist, excl = p["roles"][i]
    pool = [x for x in ROLE_ORDER if x != role and x not in excl]
    wrongs = r.sample(pool, 3)
    why = {ROLES[w]: (f"第{i + 1}段落は{gist}。「{ROLES[w]}」の働きはしていない。", "段落の役割の取り違え") for w in wrongs}
    return mc(f"{head(p)}\n第{i + 1}段落が文章全体の中で果たしている役割として最も適切なものを選びなさい。", [ROLES[role]] + [ROLES[w] for w in wrongs],
              f"「{ROLES[role]}」。第{i + 1}段落は{gist}。", d=3, stim=pstim(p),
              ap="段落の最初のディスコースマーカー（However / For example / Therefore など）と、前後の段落とのつながりから役割を判断する。",
              steps=[f"第{i + 1}段落の最初の語句と主題文を確認する。", "前の段落・後ろの段落との関係を考える。", f"役割は「{ROLES[role]}」。"],
              alt=["4つの段落すべてに役割を書きこみ、全体の流れ（導入 → 本論 → 結論）として自然かを確かめる。"],
              pc=[("段落の内容をとらえている", 2), ("役割を正しく選んでいる", 2)],
              pit=["段落の内容は読めているが、文章全体の中での働きを考えない。"], why=why)


@gen("standard_practice", 5, ["computation", "application"])
def sentence_order(r):
    sents, ti, ci, topic = r.choice([x for x in PARAS if x[3] != "竹の有用性"])
    return order(f"次の4つの英文を、意味が通る段落になるように並べかえなさい（話題：{topic}）。", sents,
                 "主題文 → 支持文（説明・例）→ まとめ・転換の順になる。指示語やディスコースマーカーが手がかりになる。", d=3, p=4,
                 ap="まず最も一般的な文（主題文）か、ほかの文を受ける語（This / These / However / For example など）を含まない文を探して先頭に置く。",
                 steps=["ほかの文を前提としない文を探し、先頭に置く。", "指示語（they / it / these）やディスコースマーカーが何を受けているかで順序を決める。",
                        "まとめ・転換の文（That is why / In this way / However など）を後ろに置く。", "完成した段落を通して読み、流れを確かめる。"],
                 alt=["隣り合う2文ごとに「前の文がないと意味が通らないか」を確かめ、つながりを1組ずつ決める。"],
                 pc=[("先頭の文を正しく選んでいる", 2), ("残りの文の順序が正しい", 2)],
                 pit=["指示語が何を指すかを確かめずに並べる。"])


@gen("standard_practice", 5, ["condition_check", "common_error"])
def true_statement(r):
    p = r.choice(PASSAGES)
    ok = r.choice(p["trues"])
    wrongs = r.sample(p["falses"], 3)
    return mc(f"{head(p)}\n本文の内容に合うものを1つ選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　本文の該当箇所と照合し、言いかえを見抜く。", d=3, stim=pstim(p),
              ap="選択肢ごとに根拠となる本文の箇所を探し、「書かれている」「逆」「書かれていない」のどれかに分ける。",
              steps=["選択肢のキーワードを本文で探す。", "該当箇所と選択肢の内容を照合する（not・only・all などの語に注意）。", f"本文と一致するのは：{ok}"],
              alt=["誤りの選択肢について、本文のどの語句と食い違うかを書き出して確かめる。"],
              pc=[("根拠となる本文の箇所を見つけている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["only / all / never などの強い限定の語を見落とす。"], why={w: (reason, "本文との照合不足") for w, reason in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def summarize(r):
    p = r.choice(PASSAGES)
    lim = r.choice([80, 90])
    return desc(f"{head(p)}\n本文の要旨を、具体例を除いて日本語{lim}字以内でまとめなさい。", p["summary"],
                "各段落の役割（問題提起・具体例・反対の視点・結論）を押さえ、具体例を除いて筆者の主張とその主な理由をまとめる。",
                p["skeys"], d=4, p=8, grid=lim, stim=pstim(p),
                ap="第1段落の問題提起と最終段落の結論を中心にし、本論の段落からは主張を支える主な理由だけを取り出す。具体例は入れない。",
                steps=["各段落に役割（問題提起・具体例・反対の視点・結論など）を書きこむ。", "具体例の部分を除く。", "問題提起・主な理由・結論をつないで1〜2文にまとめる。", "字数と、本文にない内容が入っていないかを確かめる。"],
                alt=["まず英語で主旨を1文（主語＋動詞）で書き、それを日本語に直して肉づけする方法もある。"],
                pc=[(k, v) for k, v in p["skeys"]],
                pit=["具体例を要旨に入れる。", "However などで示された反対の視点を筆者の主張としてまとめる。"])


@gen("thinking_writing", 3, ["written_reasoning", "concept"])
def explain_detail(r):
    p = r.choice(PASSAGES)
    return desc(f"{head(p)}\n{p['exq']}", p["exa"],
                "設問が指す段落を特定し、ディスコースマーカーや指示語を手がかりに、本文の言葉を使って説明する。",
                [("設問が指す本文の箇所を正しく特定している", 3), ("本文の内容に即して説明している", 3), ("設問の問い方に合った文末で答えている", 2)], d=4, p=8, lines=5, stim=pstim(p),
                ap="設問が指す段落と文を特定し、その前後のディスコースマーカー（because / For example / Therefore など）から理由や関係をとらえる。",
                steps=["設問が指す段落・語句を本文で確認する。", "前後の文から、理由・内容・関係を示す部分を探す。", "本文の内容を日本語でまとめ、設問の問い方（なぜ → 「～から」など）に合わせて答える。"],
                alt=["答えを書いたら、その答えを英文の該当箇所と1文ずつ対応させて、抜けや付け足しがないかを確かめる。"],
                pc=[("箇所の特定", 3), ("内容の説明", 3), ("文末の形", 2)],
                pit=["本文に書かれていない自分の考えを加える。", "「なぜか」と問われているのに「～から」で結ばない。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U10", "JH-ENG-G3-U07"])
def respond_english(r):
    p = r.choice(PASSAGES)
    return desc(f"{head(p)}\n(1) 筆者の主張を英語1文で書きなさい。\n(2) その主張に対するあなたの意見を、理由を1つ挙げて英語で書きなさい（20語程度）。",
                f"(1) {p['main']}　(2)（例）{p['opinion']}",
                "(1) は結論の段落を中心に、具体例を含めずに主張を1文で表す。(2) は賛否をはっきり述べ、自分の経験などを理由として1つ挙げる。",
                [("(1) 筆者の主張を正しく英語1文で表している", 3), ("(2) 意見と理由を明確に述べている", 3), ("(2) 文法・語法が正しく、語数が適切である", 2)], d=4, p=8, lines=6, stim=pstim(p),
                ap="(1) は最終段落の結論を、本文の語句を使って主語＋動詞の1文にまとめる。(2) は I agree / I disagree with the writer. で始め、because や具体的な経験で理由を述べる。",
                steps=["最終段落と第1段落から筆者の主張をとらえる。", "(1) 具体例を除いて、主張を英語1文で書く。", "(2) 賛成か反対かを決め、理由を1つ考える。", "(2) 意見 → 理由（経験・例）の順に20語程度で書く。"],
                alt=["(2) は反対の立場から、本文の反対の視点の段落（However / On the other hand）を手がかりにして理由を書くこともできる。"],
                pc=[("主張の英文", 3), ("意見と理由", 3), ("文法・語数", 2)],
                pit=["(1) に具体例を書く。", "(2) で理由を書かずに意見だけで終える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 5, ["common_error", "written_reasoning"])
def err_summary(r):
    p = r.choice(PASSAGES)
    wrong, why = r.choice(p["wrong_sum"])
    return desc(f"{head(p)}\n本文の要旨を日本語でまとめる問題に、ある生徒は次のように答えた。\n［ある生徒の解答］\n{wrong}\nこの解答の問題点を指摘し、正しい要旨を書きなさい。",
                f"問題点：{why}　正しい要旨：{p['summary']}",
                "要旨には、具体例や反対の視点ではなく、筆者の主張とその主な理由を入れる。",
                [("解答の問題点を正しく指摘している", 2), ("正しい要旨を書いている", 3), ("段落の役割に触れて説明している", 1)], d=4, p=6, lines=6, stim=pstim(p),
                ap="生徒の解答が本文のどの段落の内容かを確かめ、その段落の役割（具体例・反対の視点・問題提起だけ）を考える。",
                steps=["生徒の解答が本文のどの段落に対応するかを確かめる。", "その段落の役割を判断し、要旨として不十分な点を指摘する。", "問題提起と結論を中心に、正しい要旨を書く。"],
                alt=["生徒の解答と正しい要旨を並べ、最終段落の結論が含まれているかどうかで比べる。"],
                pc=[("問題点の指摘", 2), ("正しい要旨", 3), ("段落の役割への言及", 1)],
                pit=["具体例を言いかえただけで、主張を書かない。"],
                err=dict(sol=wrong, step="要旨の中心に選んだ段落", type="interpretation", tempt="印象に残りやすい具体例や、However の後ろの内容を主張だと思いこんだ。",
                         fix=p["summary"]))


MARK_ERR = [
    ("The plan sounded good. However, it was too expensive.", "その計画はよさそうだった。そのうえ、費用が高すぎた。", "その計画はよさそうだった。しかし、費用が高すぎた。", "However", "逆接"),
    ("He practiced every day. As a result, he won the contest.", "彼は毎日練習した。それにもかかわらず、コンテストで優勝した。", "彼は毎日練習した。その結果、コンテストで優勝した。", "As a result", "結果"),
    ("Some fruits are rich in vitamin C. For instance, oranges and strawberries contain a lot of it.", "ビタミンCを多く含む果物がある。それに対して、オレンジやイチゴはそれを多く含む。",
     "ビタミンCを多く含む果物がある。例えば、オレンジやイチゴはそれを多く含む。", "For instance", "例示"),
    ("Tom is very quiet. In contrast, his brother talks all the time.", "トムはとても無口だ。つまり、彼の兄弟はいつも話している。", "トムはとても無口だ。それとは対照的に、彼の兄弟はいつも話している。", "In contrast", "対比"),
    ("The store is open twenty-four hours a day. In other words, you can shop there at any time.", "その店は1日24時間営業している。そのうえ、いつでも買い物ができる。",
     "その店は1日24時間営業している。つまり、いつでも買い物ができる。", "In other words", "言いかえ"),
    ("The test was difficult. Nevertheless, most students passed it.", "テストは難しかった。そのため、ほとんどの生徒が合格した。", "テストは難しかった。それにもかかわらず、ほとんどの生徒が合格した。", "Nevertheless", "逆接"),
    ("Smartphones are useful. On the other hand, they can make it hard to concentrate.", "スマートフォンは便利だ。その結果、集中しにくくなることがある。", "スマートフォンは便利だ。一方で、集中しにくくなることもある。", "On the other hand", "対比"),
    ("This book is easy to read. Moreover, it is full of beautiful pictures.", "この本は読みやすい。しかし、美しい絵がたくさん載っている。", "この本は読みやすい。さらに、美しい絵がたくさん載っている。", "Moreover", "追加"),
    ("I was very tired. Even so, I finished my homework.", "私はとても疲れていた。だから、宿題を終えた。", "私はとても疲れていた。それでも、宿題を終えた。", "Even so", "逆接"),
    ("We need more sleep, healthier food, and regular exercise. In short, we must take better care of ourselves.", "私たちにはもっと睡眠と健康的な食事と定期的な運動が必要だ。例えば、自分の体をもっと大切にしなければならない。",
     "私たちにはもっと睡眠と健康的な食事と定期的な運動が必要だ。要するに、自分の体をもっと大切にしなければならない。", "In short", "結論・要約"),
]


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_marker(r):
    en, wrong, fix, m, f = r.choice(MARK_ERR)
    return desc(f"次の英文を日本語に訳しなさい。\n{en}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい日本語訳に直しなさい。", fix,
                f"{m} は「{f}」（{FUNC_DESC[f]}）を表す。前後の文の関係もそれに合っている。",
                [("誤訳した語句とその理由を指摘している", 2), ("正しい訳に直している", 3), ("マーカーの働きを説明している", 1)], d=3, p=6, lines=5,
                ap="誤訳のある部分（つなぎの言葉）に注目し、英文のディスコースマーカーの働きと前後の文の関係を確かめる。",
                steps=[f"英文のディスコースマーカー {m} を確認する。", f"{m} の働きは「{f}」。前後の文の関係もそれに合っている。", f"正しい訳：{fix}"],
                alt=["生徒の訳のつなぎの言葉を英語に戻すと別のマーカーになることを確かめ、元の英文と違うことを示す。"],
                pc=[("誤りの指摘", 2), ("正しい訳", 3), ("働きの説明", 1)],
                pit=["マーカーを読み飛ばし、前後の内容から推測して訳す。"],
                err=dict(sol=wrong, step=f"{m} の訳", type="interpretation", tempt="前後の文の内容から関係を推測し、マーカーの意味を確かめなかった。", fix=fix))


GENERATORS = [marker_function, marker_fill, topic_sentence, detail,
              main_or_title, paragraph_role, sentence_order, true_statement,
              summarize, explain_detail, respond_english,
              err_summary, err_marker]
