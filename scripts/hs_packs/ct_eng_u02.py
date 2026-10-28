"""単元パック：共通テスト対策　英語リスニング（対話と講義の聞き取り）。

音声教材はないため、聞き取りの素材はすべて印刷したスクリプト（listening_script）として示す。
授業では教師がスクリプトを読み上げる（1回または2回）。読み上げができない場合は、生徒がスクリプトを
読んで答える（その場合も、1回だけ通して読んでから設問に答えるなど、聞き取りに近い条件で取り組ませる）。
対話・講義・議論はすべてこのパックのためのオリジナル英文。調査の数値・表はすべて架空の資料である。
"""
import zlib

from banks._common import desc, mc, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "CT-ENG-U02"

PREREQUISITES = [
    ("JH-ENG-G3-U06", "対話文・説明文・グラフや資料の読み取りの基本（話の流れと必要な情報をつかむ習慣）"),
    ("HS-ENG-U09", "ディスコースマーカー（first / however / so など）から話の構成と主張をつかめること"),
    ("HS-ENG-U03", "助動詞（should / could / might）を使った提案・推量の表現を理解できること"),
]
EXTENSIONS = [
    ("CT-ENG-U01", "聞き取りで身につけた「先読み → 必要な情報の検索 → 言いかえの照合」を、リーディングの資料問題でも使う"),
    ("HS-ENG-U10", "議論で聞いた賛否と理由の述べ方を、自分の意見文・スピーチの型として使う"),
    ("SS-ENG-U02", "複数の意見を比べて自分の立場を述べる力を、二次試験の自由英作文に生かす"),
]

NOTE = "（教師が読み上げる。音声がない場合はスクリプトとして読む）"


def yen(n):
    return f"{n:,} yen"


ONES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
        "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
TENS = ["", "", "twenty", "thirty", "forty", "fifty"]


def nw(n):
    return ONES[n] if n < 20 else TENS[n // 10] + ("" if n % 10 == 0 else "-" + ONES[n % 10])


def tw(m):
    """分 → 話し言葉の時刻（six forty / seven oh five / six o'clock）。"""
    h, mi = divmod(m, 60)
    h12 = h % 12 or 12
    if mi == 0:
        return f"{nw(h12)} o'clock"
    return f"{nw(h12)} {'oh ' + nw(mi) if mi < 10 else nw(mi)}"


def hm(m):
    h, mi = divmod(m, 60)
    return f"{h % 12 or 12}:{mi:02d}"


def lstim(id, content, title):
    return stim(id, content, "listening_script", f"{title}{NOTE}", source="オリジナル")


# ======================================================================
# 短い対話：最終的な決定（最初の案が変わる）
# (id, スクリプト, 問い, 正答, [(誤答, 理由)])  — 誤答の先頭は「最初に出た案」
# ======================================================================

DIALOGS = [
    ("GIFT", "M: What should we get Mom for her birthday? How about a scarf?\nW: She already has a lot of scarves. She said she wants to try cooking Thai food.\nM: Then let's get her a cookbook. Flowers would be nice too, but they don't last long.\nW: Right. Let's go with the book.",
     "What will they buy for their mother?", "A cookbook",
     [("A scarf", "最初に出た案だが、母はすでにたくさん持っているという理由で取りやめている。"),
      ("Flowers", "長持ちしないという理由で選ばれていない。"),
      ("Some Thai food", "タイ料理は母が作ってみたい料理として話題に出ただけである。")]),
    ("TIME", "W: The concert starts at seven. Shall we meet at six thirty?\nM: The hall is far from the station. Let's meet at six fifteen, just in case.\nW: Actually, I finish work at six. Can we make it six twenty?\nM: Sure, no problem.",
     "What time will they meet?", "6:20",
     [("6:30", "最初に女性が提案した時刻だが、男性の提案で早めることになった。"),
      ("6:15", "男性の提案だが、女性の仕事の都合で6時20分に変更された。"),
      ("7:00", "7時はコンサートの開始時刻である。")]),
    ("RIDE", "M: Are you taking the bus to the stadium?\nW: I was going to, but the buses are always crowded on game days.\nM: You could ride your bike. It only takes twenty minutes.\nW: It's supposed to rain this afternoon, though. I'll ask my dad to drive me.",
     "How will the woman get to the stadium?", "By car",
     [("By bus", "最初の予定だったが、試合の日は混むのでやめている。"),
      ("By bike", "男性の提案だが、午後は雨の予報なので選ばれていない。"),
      ("On foot", "歩いて行くとは言っていない。")]),
    ("MENU", "W: I'll have the chicken curry, please.\nM: I'm sorry, we've just sold out of chicken curry. The beef curry is very popular.\nW: Hmm, I don't eat beef. Do you have anything with vegetables?\nM: Yes, the vegetable pasta.\nW: I'll take that, then.",
     "What will the woman eat?", "Vegetable pasta",
     [("Chicken curry", "最初に注文したが、売り切れだった。"),
      ("Beef curry", "店員が勧めたが、女性は牛肉を食べない。"),
      ("Vegetable curry", "対話に出てきた vegetable と curry を組み合わせた、メニューにない料理である。")]),
    ("STUDY", "M: Let's study for the test at the library after school.\nW: The library closes at five today because of a meeting.\nM: Oh. How about the café near the station?\nW: It's too noisy there. Why don't we use an empty classroom? Ms. Kato said we can stay until six.\nM: Great idea.",
     "Where will they study?", "In an empty classroom",
     [("At the library", "最初の案だが、今日は5時に閉まる。"),
      ("At the café near the station", "うるさいという理由で女性が断っている。"),
      ("In Ms. Kato's office", "加藤先生は教室を使える時間を伝えた人で、先生の部屋で勉強するとは言っていない。")]),
    ("SHOE", "W: These running shoes are nice. Do you have them in size 24?\nM: Sorry, we only have sizes 23 and 25 in white. But we have a 24 in black.\nW: Black is fine. Actually, it's better, because white shoes get dirty easily.",
     "Which shoes will the woman buy?", "Black shoes in size 24",
     [("White shoes in size 24", "最初に希望した組み合わせだが、白の24は在庫がない。"),
      ("White shoes in size 25", "白で残っているのは23と25だが、女性はサイズ24を求めている。"),
      ("Black shoes in size 23", "黒で在庫があるのは24である。")]),
    ("HIKE", "M: Do you want to go hiking on Saturday?\nW: I'd love to, but I have a piano lesson on Saturday morning.\nM: We could go in the afternoon.\nW: The weather report says it'll rain on Saturday afternoon. How about Sunday morning?\nM: Sounds good.",
     "When will they go hiking?", "On Sunday morning",
     [("On Saturday morning", "最初の候補だが、女性はピアノのレッスンがある。"),
      ("On Saturday afternoon", "男性の提案だが、雨の予報で取りやめた。"),
      ("On Sunday afternoon", "日曜日の午後は話題に出ていない。")]),
    ("DUE", "W: Is the history report due this Friday?\nM: Mr. Ono said Friday at first, but then he gave us until next Monday.\nW: That's a relief. I still need to find two more books.",
     "When is the history report due?", "Next Monday",
     [("This Friday", "最初に言われた締め切りだが、来週の月曜日に延びた。"),
      ("Tomorrow", "明日とは言っていない。"),
      ("Next Friday", "金曜日と来週を組み合わせた誤りで、締め切りは来週の月曜日である。")]),
    ("DELI", "M: Hello, this is Green Express. We'd like to deliver your package tomorrow morning.\nW: I'll be out in the morning. Could you come after three?\nM: We have a time slot between four and six.\nW: That works for me.",
     "When will the package be delivered?", "Tomorrow between four and six",
     [("Tomorrow morning", "最初の提案だが、女性は午前中は留守にする。"),
      ("Tomorrow at three", "3時は女性が「3時以降」と言った区切りで、配達時間ではない。"),
      ("Today between four and six", "配達は今日ではなく明日である。")]),
    ("SLID", "W: Who's going to make the slides for our presentation?\nM: I can do it, but I'm not good at design. Maybe Aya should do it.\nW: Aya is already writing the script. You make the slides, and I'll help you with the design.\nM: OK, thanks.",
     "Who will make the slides?", "The man, with help from the woman",
     [("Aya", "男性が提案したが、Aya はすでに原稿を書いているので担当しない。"),
      ("The woman alone", "女性はデザインを手伝うだけで、作るのは男性である。"),
      ("Aya and the man", "Aya は原稿担当で、スライドには関わらない。")]),
]

# 発話の意図（言外の意味）：(スクリプト, 問い, 正答, [(誤答, 理由)])
INFER = [
    ("W: Would you like to come to the movies tonight?\nM: I have a big test tomorrow.", "What does the man mean?", "He will not go to the movies tonight.",
     [("He wants to see a movie about a test.", "聞こえた movie と test を組み合わせた選択肢で、誘いへの答えになっていない。"),
      ("He will go to the movies after the test tonight.", "試験は明日であり、今夜行くとは言っていない。"),
      ("He wants the woman to help him study.", "勉強を手伝ってほしいとは言っていない。")]),
    ("W: Can you lend me your dictionary?\nM: Sorry, I left it at home.", "What does the man mean?", "He cannot lend her his dictionary now.",
     [("He will buy a new dictionary.", "新しく買うとは言っていない。"),
      ("He does not want to lend it to anyone.", "貸したくないのではなく、家に置いてきたので貸せない。"),
      ("He will bring it to her house.", "彼女の家に持って行くとは言っていない。")]),
    ("M: Shall I open the window?\nW: Actually, I'm a little cold.", "What does the woman mean?", "She does not want the window opened.",
     [("She wants him to open the window.", "寒いと言っているので、窓を開けてほしくない。"),
      ("She wants to go outside.", "外に出たいとは言っていない。"),
      ("She thinks the room is too hot.", "寒いと言っており、逆である。")]),
    ("W: Did you finish the report?\nM: I'm still on the second page.", "What does the man mean?", "He has not finished the report yet.",
     [("He finished two reports.", "2ページ目を書いている途中で、2つ書き終えたのではない。"),
      ("The report is only two pages long.", "レポートの長さは言っていない。"),
      ("He lost the second page.", "2ページ目をなくしたとは言っていない。")]),
    ("M: Is this seat taken?\nW: My friend is just getting coffee.", "What does the woman mean?", "The seat is not available.",
     [("The man can sit there.", "友人が戻ってくるので、その席は空いていない。"),
      ("She wants the man to get her some coffee.", "コーヒーを買ってきてほしいとは言っていない。"),
      ("Her friend does not drink coffee.", "友人はコーヒーを買いに行っている。")]),
    ("W: The bus is late again.\nM: Let's just walk. It's only ten minutes.", "What does the man suggest?", "Walking instead of waiting for the bus",
     [("Waiting ten more minutes for the bus", "10分は歩いてかかる時間で、待つ時間ではない。"),
      ("Taking a taxi", "タクシーは話題に出ていない。"),
      ("Complaining to the bus company", "苦情を言うとは言っていない。")]),
    ("M: Do you want some more cake?\nW: I couldn't eat another bite.", "What does the woman mean?", "She is too full to eat more.",
     [("She wants another piece of cake.", "もう一口も食べられないと言っており、逆である。"),
      ("She did not like the cake.", "味については何も言っていない。"),
      ("She cannot eat cake because she is sick.", "病気だとは言っていない。")]),
    ("W: Are you coming to the party on Saturday?\nM: I wouldn't miss it.", "What does the man mean?", "He will definitely come to the party.",
     [("He will miss the party.", "wouldn't miss it は「絶対に逃さない」で、逆である。"),
      ("He is not sure if he can come.", "迷っているのではなく、必ず行くと言っている。"),
      ("He forgot about the party.", "忘れていたとは言っていない。")]),
    ("M: Can you help me move this desk?\nW: Give me five minutes.", "What does the woman mean?", "She will help him soon.",
     [("She wants him to give her something.", "Give me five minutes は「5分待って」という意味である。"),
      ("She will not help him.", "断ってはおらず、少し後で手伝うと言っている。"),
      ("The desk will take five minutes to move.", "5分は彼女が待ってほしい時間である。")]),
    ("W: How was the new restaurant?\nM: Well, the view from the window was nice.", "What does the man most likely mean?", "He was not very impressed with the food.",
     [("He enjoyed the food very much.", "景色だけをほめて料理に触れないのは、料理には満足しなかったことを遠回しに伝えている。"),
      ("He could not find the restaurant.", "店に行っており、景色について話している。"),
      ("The restaurant had no windows.", "窓からの景色がよかったと言っている。")]),
]

# 応答の選択：(最後の発話, 正答, [(誤答, 理由)])
RESP = [
    ("W: I lost my umbrella on the train this morning.", "Why don't you ask at the station's lost and found?",
     [("Yes, it rained a lot this morning.", "雨の話にずれており、傘をなくしたことへの応答になっていない。"),
      ("I'll take the train tomorrow.", "自分の予定を述べており、相手の困りごとに応じていない。"),
      ("You're welcome.", "お礼に対する応答で、場面に合わない。")]),
    ("M: Could you tell me how to get to the city library?", "Sure. Go straight and turn left at the second corner.",
     [("I borrowed three books there yesterday.", "道順を聞かれているのに、自分の行動を答えている。"),
      ("No, I'm not a student.", "学生かどうかは聞かれていない。"),
      ("It was built ten years ago.", "建てられた時期は聞かれていない。")]),
    ("W: I've got a terrible headache.", "That's too bad. Maybe you should go home and rest.",
     [("Congratulations!", "よい知らせへの応答で、場面に合わない。"),
      ("Me too. I had a great time.", "楽しかったことへの応答で、頭痛の話と合わない。"),
      ("Sure, here you are.", "物を渡すときの表現で、場面に合わない。")]),
    ("M: Thank you for helping me with my homework.", "No problem. Let me know if you need help again.",
     [("I'm sorry to hear that.", "残念な知らせへの応答で、お礼への返事にならない。"),
      ("Yes, please help me.", "お礼を言われた側が助けを求めるのは不自然である。"),
      ("It's due tomorrow.", "締め切りは話題になっていない。")]),
    ("M: Would you mind if I opened the window?", "Not at all. Go ahead.",
     [("Yes, please open it.", "Would you mind ～? に Yes と答えると「気にする（困る）」の意味になり、please open it と矛盾する。"),
      ("No, you can't open it.", "No は「かまわない」の意味なので、you can't と矛盾する。"),
      ("I'm opening the door now.", "ドアの話にずれている。")]),
    ("W: How long have you lived in this town?", "For about ten years.",
     [("Ten years ago.", "How long（期間）を聞かれているのに、時点（いつ）で答えている。"),
      ("By bus.", "交通手段（How）の答えである。"),
      ("About ten kilometers.", "距離の答えである。")]),
    ("M: Which do you like better, tea or coffee?", "Tea, I think. Coffee is too bitter for me.",
     [("Yes, I like it very much.", "どちらが好きかを聞く疑問文に Yes / No では答えられない。"),
      ("Both of them are 200 yen.", "値段は聞かれていない。"),
      ("I usually drink it in the morning.", "どちらが好きかに答えていない。")]),
    ("W: What time does the next train leave?", "In about fifteen minutes, at three forty.",
     [("For two hours.", "所要時間の答えで、出発時刻ではない。"),
      ("From Platform 2.", "場所の答えで、時刻ではない。"),
      ("It's 500 yen.", "料金の答えである。")]),
    ("M: Have you ever been to Okinawa?", "Yes, I went there with my family two years ago.",
     [("No, I'm going there yesterday.", "be going to（未来）と yesterday（過去）が合わない。"),
      ("Yes, I will go there next year.", "Have you ever ～? は経験を聞いており、未来の予定では Yes の答えにならない。"),
      ("I've been studying for an hour.", "経験の質問に答えていない。")]),
    ("W: I'm thinking of joining the volunteer club.", "That's great. I'm sure you'll enjoy it.",
     [("I'm sorry to hear that.", "残念な知らせへの応答で、場面に合わない。"),
      ("You're welcome.", "お礼への応答で、場面に合わない。"),
      ("No, thank you. I'm full.", "食べ物を断る表現で、場面に合わない。")]),
]


# ======================================================================
# 講義（ワークシート・図表つき）
# ======================================================================

LECTURES = [
    dict(key="TREE", evid="木が日陰をつくり地面を涼しく保つなどの利点があること、一方で落ち葉や根が歩道を壊すなどの問題もあること", title="Why Cities Plant Street Trees",
         text="Today I'd like to talk about street trees. Many cities plant trees along their roads, and there are several good reasons for this. First, trees provide shade. On a hot summer day, the ground under a tree can be much cooler than the ground in the sun. Second, tree roots and soil take in rainwater, so less water runs off the roads after heavy rain. Third, trees give birds and insects places to live, even in the middle of a city. Finally, many people say they feel more relaxed when they walk along a street with trees.\nHowever, street trees also cause some problems. In autumn, fallen leaves must be cleaned up, and large roots can break sidewalks. Taking care of trees also costs money. So when cities plan new streets, they need to choose the right kinds of trees and the right places to plant them.",
         rows=[("Benefit 1", "Shade that keeps the ground cooler"), ("Benefit 2", "Less rainwater running off the roads"), ("Benefit 3", "Homes for birds and insects"),
               ("Benefit 4", "People feel more relaxed"), ("Problem 1", "Fallen leaves must be cleaned up"), ("Problem 2", "Roots can break sidewalks"), ("Problem 3", "Taking care of trees costs money")],
         fake=["Trees make the streets noisier", "Trees block the traffic lights"],
         main="Street trees bring many benefits, but cities must plan carefully because trees also cause problems.",
         main_wrong=[("Trees should not be planted in cities because their roots break sidewalks.", "譲歩で述べた問題点を主張と取り違えている。"),
                     ("Birds and insects need more places to live in cities.", "利点の1つ（具体例）だけで、講義全体の主旨として狭すぎる。"),
                     ("Cities should stop cleaning up fallen leaves to save money.", "講義で述べられていない提案である。")],
         trues=["Trees can help reduce the amount of rainwater running off roads.", "The speaker mentions both good points and bad points of street trees."],
         falses=[("The speaker says trees make people feel nervous.", "多くの人がリラックスできると述べている。"),
                 ("Taking care of street trees costs nothing.", "手入れには費用がかかると述べている。"),
                 ("The speaker thinks any kind of tree can be planted anywhere.", "適切な種類と場所を選ぶ必要があると述べている。")],
         summary="街路樹には日陰をつくる、雨水を吸収する、生き物のすみかになる、人をリラックスさせるなどの利点があるが、落ち葉や根による歩道の損傷、費用などの問題もあるので、種類と場所を考えて計画する必要がある。",
         skeys=[("街路樹の利点を2つ以上述べている", 3), ("落ち葉・根・費用などの問題に触れている", 2), ("種類と場所を考えて計画すべきだという結論でまとめている", 3)],
         chart=table([["Under a street tree", "32°C"], ["Sidewalk in the sun", "45°C"], ["Asphalt road in the sun", "52°C"]], header=["Place", "Ground temperature at 1 p.m."],
                     caption="ある夏の日の地面の温度（架空の資料）"),
         chart_q="講義の後に、次の表が示された。この表は講義のどの内容を裏づけるか。また、この表だけでは確かめられない講義の内容を1つ挙げ、理由とともに日本語で説明しなさい。",
         chart_a="木の下の地面（32°C）が日なたの歩道（45°C）や道路（52°C）より大幅に低いので、「木が日陰をつくり地面を涼しく保つ」という利点1を裏づける。一方、雨水の流出が減ることや、手入れに費用がかかることなどは、温度だけの表では確かめられない（表に雨水の量や費用のデータがないから）。"),
    dict(key="MICR", evid="非常に小さいので海に出ると回収が難しいこと、魚や海鳥が誤って食べてしまうこと", title="Microplastics",
         text="Have you heard of microplastics? They are pieces of plastic smaller than five millimeters. Some of them are made small on purpose, but many come from larger plastic items. When plastic bottles and bags are left outside, sunlight and waves slowly break them into smaller and smaller pieces. Another source is our clothes. Clothes made of synthetic fibers, such as polyester, can release tiny fibers when they are washed.\nThese pieces are so small that it is very hard to collect them once they reach the sea, and fish and seabirds sometimes eat them by mistake. So what can we do? The most effective step is to stop plastic from reaching the sea in the first place. We can use fewer single-use plastic products, put our trash in the right place, and join beach clean-ups before large pieces break down.",
         rows=[("Definition", "Pieces of plastic smaller than five millimeters"), ("Source 1", "Large plastic items broken down by sunlight and waves"),
               ("Source 2", "Fibers released when synthetic clothes are washed"), ("Problem", "Fish and seabirds eat them by mistake"),
               ("Best solution", "Stopping plastic from reaching the sea")],
         fake=["Removing all plastic from the sea with nets", "Plastic melting in hot water"],
         main="Microplastics are very hard to remove once they reach the sea, so we should stop plastic from getting there.",
         main_wrong=[("Clothes made of polyester should never be washed.", "洗濯で繊維が出るという発生源の説明を、極端な提案にすり替えている。"),
                     ("Fish and seabirds are the main cause of microplastics.", "魚や海鳥は誤って食べてしまう被害者で、原因ではない。"),
                     ("Microplastics can easily be collected from the sea.", "海に出ると回収は非常に難しいと述べており、逆である。")],
         trues=["Some microplastics come from clothes.", "The speaker thinks preventing plastic from reaching the sea is the most effective step."],
         falses=[("All microplastics are made small on purpose.", "わざと小さく作られたものもあるが、多くは大きなプラスチックから生じる。"),
                 ("Microplastics are larger than five millimeters.", "5ミリメートルより小さいものと定義している。"),
                 ("Beach clean-ups are useless.", "大きなごみが砕ける前の清掃活動を勧めている。")],
         summary="マイクロプラスチックは5ミリ未満のプラスチックで、大きなごみが日光や波で砕けたものや衣類の繊維から生じる。海に出ると回収が難しく生き物が誤食するので、海に流れ出ないようにすることが最も効果的である。",
         skeys=[("マイクロプラスチックの定義または発生源を述べている", 3), ("海に出ると回収が難しい・生き物が食べるという問題に触れている", 2), ("海に流れ出るのを防ぐことが最も効果的だという結論でまとめている", 3)],
         chart=table([["2019", "120"], ["2021", "180"], ["2023", "260"]], header=["Year", "Pieces of microplastics per square meter of sand"],
                     caption="ある海岸の砂に含まれるマイクロプラスチックの数（架空の資料）"),
         chart_q="講義の後に、次の表が示された。この表から言えることと、この表だけでは言えないことを、講義の内容と関連づけて日本語で説明しなさい。",
         chart_a="砂1平方メートルあたりの数が120 → 180 → 260と年々増えているので、マイクロプラスチックが海岸にたまり続けていることは言える。これは、一度海に出ると回収が難しいという講義の内容と合う。しかし、増えた原因が大きなごみの破片か衣類の繊維かは、この表からは言えない（発生源ごとのデータがないから）。"),
    dict(key="HEAT", evid="アスファルトやコンクリートが熱をため、植物も少ないなど複数の原因があること、屋上緑化や白い屋根などの対策は問題を完全にはなくせないが組み合わせれば効果があること", title="The Urban Heat Island Effect",
         text="Have you noticed that the center of a city often feels hotter than the countryside around it? This is called the urban heat island effect, and it has three main causes. First, roads and buildings made of asphalt and concrete absorb heat during the day and release it slowly at night. Second, cities have fewer plants and less open soil. Plants cool the air by releasing water from their leaves, so fewer plants mean less cooling. Third, air conditioners, cars, and factories produce heat.\nTo reduce the effect, some cities are covering roofs with plants, painting roofs white to reflect sunlight, and planting more trees. These steps cannot remove the problem completely, but together they can make city life more comfortable.",
         rows=[("Cause 1", "Asphalt and concrete absorb heat and release it at night"), ("Cause 2", "Fewer plants to cool the air"), ("Cause 3", "Heat from air conditioners, cars, and factories"),
               ("Measure 1", "Covering roofs with plants"), ("Measure 2", "Painting roofs white"), ("Measure 3", "Planting more trees")],
         fake=["Building more parking lots", "Turning off all street lights"],
         main="Cities are hotter than their surroundings for several reasons, and a combination of measures can reduce the effect.",
         main_wrong=[("White roofs can completely solve the heat island problem.", "対策は問題を完全にはなくせないと述べており、言いすぎである。"),
                     ("Air conditioners are the only cause of heat in cities.", "原因は3つ挙げられており、言いすぎである。"),
                     ("The countryside is becoming hotter than cities.", "講義と逆の内容である。")],
         trues=["Plants help cool the air.", "The speaker says the measures cannot remove the problem completely."],
         falses=[("Concrete releases heat quickly during the day.", "昼に熱を吸収し、夜にゆっくり放出すると述べている。"),
                 ("Cities have more open soil than the countryside.", "都市は土の地面が少ないと述べている。"),
                 ("Painting roofs black helps reflect sunlight.", "日光を反射させるために屋根を白く塗ると述べている。")],
         summary="都市の中心部が周辺より暑くなるのは、アスファルトなどが熱をため夜に放出すること、植物が少ないこと、冷房や車の排熱があることによる。屋上緑化や白い屋根、植樹を組み合わせれば暑さを和らげられる。",
         skeys=[("原因を2つ以上述べている", 3), ("対策を挙げている", 2), ("対策を組み合わせれば和らげられる（完全にはなくせない）という結論でまとめている", 3)],
         chart=table([["Monday", "27°C", "24°C"], ["Wednesday", "28°C", "24°C"], ["Friday", "27°C", "25°C"]], header=["Day", "City center", "Countryside"],
                     caption="ある夏の週の最低気温（架空の資料）"),
         chart_q="講義の後に、次の表が示された。表の数値は講義のどの説明と結びつくか。数値を根拠にして日本語で説明しなさい。",
         chart_a="どの日も都市中心部の最低気温（27〜28°C）が郊外（24〜25°C）より2〜4°C高い。最低気温は夜から明け方の気温なので、アスファルトやコンクリートが昼にためた熱を夜にゆっくり放出するという原因1の説明と結びつく。"),
    dict(key="FOOD", evid="家庭で捨てられる食品の約40%が未開封だったこと、必要以上に買うことや期限表示の誤解が原因であること", title="Food Loss at Home",
         text="Food loss means food that could still be eaten but is thrown away. It happens at every stage, from farms and stores to restaurants and our own homes. In a survey of 300 families in our city, about forty percent of the food thrown away at home had never even been opened.\nWhy does this happen? One reason is that people buy more than they need, especially when items are on sale. Another reason is confusion about date labels. Many people throw food away as soon as the 'best before' date has passed, even though it is usually still safe to eat for some time after that. There are simple ways to reduce food loss at home. Check your fridge before you go shopping, make a shopping list, and learn what date labels really mean. Small changes in each home can add up to a big difference.",
         rows=[("Definition", "Food that could be eaten but is thrown away"), ("Survey result", "About 40% of food thrown away at home was unopened"),
               ("Reason 1", "Buying more than needed, especially on sale"), ("Reason 2", "Confusion about date labels"), ("Tip", "Check the fridge and make a shopping list")],
         fake=["Restaurants serve too little food", "Food is too expensive to buy"],
         main="Food loss at home can be reduced through small changes, such as checking the fridge and understanding date labels.",
         main_wrong=[("Food should be thrown away as soon as the best-before date passes.", "講義では、期限を過ぎてもしばらくは安全に食べられることが多いと述べており、逆である。"),
                     ("Stores should stop having sales.", "講義で述べられていない提案である。"),
                     ("About 40% of all food in the city is thrown away.", "40%は家庭で捨てられた食品のうち未開封のものの割合で、数値の意味を取り違えている。")],
         trues=["Food loss happens not only at home but also at farms and stores.", "The speaker suggests making a shopping list."],
         falses=[("The survey was done with 3,000 families.", "調査対象は300家庭である。"),
                 ("Most food thrown away at home had been opened.", "未開封は約40%だが、そのほかがすべて開封済みかどうかは述べられておらず、選択肢の根拠にならない。"),
                 ("Food is never safe after the best-before date.", "期限後もしばらくは安全なことが多いと述べている。")],
         summary="家庭では、まだ食べられる食品が多く捨てられ、未開封のものも多い。必要以上に買うことや期限表示の誤解が原因なので、買い物前に冷蔵庫を確かめ、リストを作り、表示の意味を理解すれば減らせる。",
         skeys=[("家庭で食べられる食品が捨てられている現状を述べている", 2), ("買いすぎ・期限表示の誤解という原因を述べている", 3), ("冷蔵庫の確認や表示の理解などで減らせるという結論でまとめている", 3)],
         chart=table([["Unopened food", "40%"], ["Leftovers from meals", "33%"], ["Parts cut off while cooking", "27%"]], header=["Type of food thrown away", "Share"],
                     caption="市内300家庭で捨てられた食品の内訳（架空の資料）"),
         chart_q="講義の後に、次の表が示された。講師が勧める「買い物の前に冷蔵庫を確かめ、リストを作る」という方法は、表のどの項目を減らすのに最も役立つと考えられるか。理由とともに日本語で説明しなさい。",
         chart_a="「未開封の食品（40%）」を減らすのに最も役立つ。未開封のまま捨てられるのは、必要以上に買ってしまうことが原因の一つであり、買う前に冷蔵庫を確かめてリストを作れば、余分な食品を買わずにすむから。"),
    dict(key="BUS", evid="路線の廃止で車を運転しない高齢者が困っていること、コミュニティバスは運賃で費用の約20%しか賄えないこと", title="Community Buses in Small Towns",
         text="In many small towns, bus companies have stopped running some routes because too few people use them. This is a serious problem for older residents who no longer drive. To solve it, some towns now run their own community buses. These are usually small buses that stop near hospitals, supermarkets, and the town office. In one town I visited, the fare is only 100 yen, and the number of riders has risen every year since the service started.\nHowever, community buses are not cheap to operate. The town has to pay for drivers and fuel, and in that town, fares cover only about twenty percent of the cost. Now some towns are trying on-demand buses, which run only when someone books a ride by phone. I think towns should keep looking for new ideas like this, so that everyone can get where they need to go.",
         rows=[("Problem", "Bus companies stopped running some routes"), ("Who is affected", "Older residents who no longer drive"),
               ("Where buses stop", "Near hospitals, supermarkets, and the town office"), ("Difficulty", "Fares cover only part of the cost"), ("New idea", "On-demand buses booked by phone")],
         fake=["Free taxis for all students", "Larger buses on every route"],
         main="Community buses help people without cars, but towns need new ideas because the buses are expensive to run.",
         main_wrong=[("Community buses should be stopped because they cost too much.", "費用の問題（譲歩）を主張と取り違えている。講師は新しい工夫を続けるべきだと述べている。"),
                     ("The fare for community buses is 100 yen in every town.", "100円は講師が訪れた1つの町の例であり、言いすぎである。"),
                     ("Older people should start driving again.", "講義で述べられていない内容である。")],
         trues=["In the town the speaker visited, the number of riders has increased every year.", "On-demand buses run only when someone books a ride."],
         falses=[("Fares pay for almost all of the cost of community buses.", "運賃で賄えるのは費用の約20%だけである。"),
                 ("Community buses stop only at train stations.", "病院・スーパー・町役場の近くに止まると述べている。"),
                 ("The speaker thinks towns should stop looking for new ideas.", "新しい工夫を探し続けるべきだと述べている。")],
         summary="利用者の少ない路線の廃止で困る高齢者のために、町がコミュニティバスを運行し利用者も増えているが、運賃では費用の一部しか賄えない。講師は予約制バスなどの新しい工夫を続けるべきだと考えている。",
         skeys=[("路線の廃止と高齢者の困りごとに触れている", 2), ("コミュニティバスの役割と費用の問題を述べている", 3), ("新しい工夫を続けるべきだという講師の考えでまとめている", 3)],
         chart=table([["2021", "8,000"], ["2022", "9,500"], ["2023", "11,200"]], header=["Year", "Number of riders"],
                     caption="ある町のコミュニティバスの年間利用者数（架空の資料）"),
         chart_q="講義の後に、次の表が示された。友人は「利用者が増えているのだから、このバスの費用の問題はもう解決した」と言った。この意見は正しいか。表の数値と講義の内容を根拠に日本語で説明しなさい。",
         chart_a="正しくない。表から利用者は8,000人から11,200人へと毎年増えていることはわかるが、講義によると運賃は100円で、費用の約20%しか賄えていない。利用者が増えても、運転手や燃料の費用を運賃で賄えるほどになったことは表からは言えないので、費用の問題が解決したとは言えない。"),
]
LBY = {lc["key"]: lc for lc in LECTURES}


def lect_stim(lc):
    return lstim(f"LC-{lc['key']}", lc["text"], f"講義“{lc['title']}”")


def worksheet(lc, blank=None, filled=None):
    rows = []
    for i, (lab, val) in enumerate(lc["rows"]):
        if i == blank:
            rows.append([lab, "（　①　）"])
        elif filled and i in filled:
            rows.append([lab, filled[i]])
        else:
            rows.append([lab, val])
    return table(rows, header=["Item", "Notes"], caption=f"Worksheet: {lc['title']}")


# ======================================================================
# 複数の話し手：条件に合うものを選ぶ（CT 型）
# ======================================================================

# (名前, 話し手のスクリプト, 日数, 参加費, 屋内/屋外, 英語を使うか)
PROGRAMS = [
    ("Science Camp", "Science Camp lasts four days. You'll do experiments in a university lab, and the fee is 6,000 yen. All the activities are in Japanese.", 4, 6000, "indoors", False),
    ("Beach Clean-Up Week", "This program is three days long, and it's free. You'll work outdoors on the beach with volunteers from abroad, so you'll use English a lot.", 3, 0, "outdoors", True),
    ("Museum Guide Training", "You'll train for two days at the city museum and then guide foreign visitors around the exhibits in English. It costs 3,000 yen for the materials.", 2, 3000, "indoors", True),
    ("Mountain Hiking Trip", "This is a five-day trip in the mountains. It costs 8,000 yen, including meals. Our guides speak English, and you'll talk with hikers from other countries.", 5, 8000, "outdoors", True),
    ("Library Reading Volunteers", "For three days, you'll read picture books to children in the library. There's no fee, and everything is done in Japanese.", 3, 0, "indoors", False),
    ("Farm Stay", "You'll stay on a farm for two days and help harvest vegetables in the fields. The fee is 4,000 yen. The farmer speaks only Japanese.", 2, 4000, "outdoors", False),
    ("International Cooking Class", "This class meets for three days in a community kitchen. The teacher is from Italy and teaches in English. It costs 5,000 yen.", 3, 5000, "indoors", True),
]


def prog_fail(p, cond):
    name, _, days, fee, place, en = p
    out = []
    if "days" in cond and days > cond["days"]:
        out.append(f"{days}日間で、{cond['days']}日以内という条件に合わない")
    if "fee" in cond and fee > cond["fee"]:
        out.append(f"参加費が{fee:,}円で、{'無料' if cond['fee'] == 0 else str(cond['fee']) + '円以下'}という条件に合わない")
    if "place" in cond and place != cond["place"]:
        out.append(f"活動が{'屋内' if place == 'indoors' else '屋外'}で、条件（{'屋内' if cond['place'] == 'indoors' else '屋外'}）に合わない")
    if "en" in cond and not en:
        out.append("英語を使う機会がない")
    return out


def cond_text(cond):
    t = []
    if "days" in cond:
        t.append(f"A. 期間は{cond['days']}日以内")
    if "fee" in cond:
        t.append("B. 参加費は無料" if cond["fee"] == 0 else f"B. 参加費は{cond['fee']:,}円以下")
    if "place" in cond:
        t.append(f"C. 活動は{'屋内' if cond['place'] == 'indoors' else '屋外'}")
    if "en" in cond:
        t.append("D. 英語を使う機会がある")
    return t


# ======================================================================
# 議論：複数の意見の比較
# ======================================================================

DISCUSSIONS = [
    dict(key="FEST", topic="Should our school festival be open to the public?", jtopic="文化祭を一般公開すべきか",
         sp=[("Aki", True, "I think we should open the festival to everyone. Local people can see what we do at school, and it's a good chance for junior high school students to visit.",
              "地域の人に学校の活動を見てもらえ、中学生が訪れるよい機会になる", "Opening the festival is a good chance to show our school to the community."),
             ("Ben", False, "I'm against it. If too many people come, the hallways will be crowded, and it might not be safe.",
              "人が多すぎると廊下が混雑し、安全でないかもしれない", "Too many visitors could make the festival unsafe."),
             ("Chika", True, "I agree with Aki, but we should limit the number of visitors. We could give out free tickets in advance.",
              "賛成だが、事前に無料の整理券を配って人数を制限すべきだ", "The festival should be open, but with a limit on the number of visitors."),
             ("Daniel", False, "I don't think it's a good idea. Preparing for a lot of visitors would take extra work, and we'd have less time for our club activities.",
              "多くの来場者の準備で仕事が増え、部活動の時間が減る", "Preparing for many visitors would take time away from club activities.")]),
    dict(key="LIBR", topic="Should the school library open on Saturdays?", jtopic="学校図書館を土曜日も開けるべきか",
         sp=[("Emma", True, "Yes. Many students don't have a quiet place to study at home, especially before exams.",
              "家に静かに勉強できる場所がない生徒が多い", "The library would give students a quiet place to study."),
             ("Kenta", False, "I'm not sure that's necessary. The city library is open on weekends, and it's not far from school.",
              "市立図書館が週末も開いていて、学校から遠くない", "Students can already use the city library on weekends."),
             ("Lisa", True, "I'm for it, but it doesn't need to open every Saturday. Opening only during the exam period would be enough.",
              "賛成だが、毎週ではなく試験期間だけで十分だ", "The library should open on Saturdays only during the exam period."),
             ("Ryo", False, "I'm against it, because teachers would have to work on Saturdays, and they're already very busy.",
              "先生が土曜日も働くことになり、すでに忙しい", "Opening on Saturdays would put too much work on teachers.")]),
    dict(key="HWK", topic="Should our school have a no-homework week before the sports festival?", jtopic="体育祭の前に宿題のない週をつくるべきか",
         sp=[("Mai", True, "I'm for it. We practice until late before the sports festival, so we're too tired to do our homework properly.",
              "体育祭前は遅くまで練習していて、疲れて宿題をきちんとできない", "Students are too tired from practice to do homework well."),
             ("Tom", True, "Me too. It would give us time to rest, and we'd enjoy the festival more.",
              "休む時間ができ、体育祭をもっと楽しめる", "A week without homework would let students rest and enjoy the festival."),
             ("Yuki", False, "I see why you think that, but I'm against it. If we stop for a week, it'll be hard to catch up before the midterm tests.",
              "1週間止めると、中間試験の前に追いつくのが難しい", "Stopping homework for a week would make it hard to prepare for tests."),
             ("Hiro", True, "I'm for it too, as long as teachers give us a little extra work after the festival.",
              "体育祭の後に少し課題を増やすなら賛成だ", "It is a good idea if some extra work is given after the festival.")]),
    dict(key="BOTL", topic="Should the cafeteria stop selling drinks in plastic bottles?", jtopic="食堂でペットボトル飲料の販売をやめるべきか",
         sp=[("Nana", True, "Yes. We throw away so many bottles every day. We can bring our own water bottles instead.",
              "毎日多くのボトルが捨てられており、自分の水筒を持って来られる", "Students can bring their own bottles to cut down on waste."),
             ("Josh", False, "I disagree. Some students forget their bottles, and on hot days they really need a drink.",
              "水筒を忘れる生徒もいて、暑い日には飲み物が必要だ", "Students who forget their bottles still need drinks on hot days."),
             ("Saki", False, "I don't think it will help. If the cafeteria stops, students will just buy bottles at the convenience store, so nothing will change.",
              "食堂でやめても、コンビニで買うだけで何も変わらない", "Students would simply buy bottled drinks somewhere else."),
             ("Leo", True, "I'm for it, but the school should put in a water fountain first so that everyone can get water.",
              "賛成だが、先に給水器を設置すべきだ", "The school should first make sure everyone can get water, and then stop selling bottles.")]),
]
COUNT_EN = ["None", "One", "Two", "Three", "Four"]


def disc_stim(ds):
    body = "\n".join(f"{n}: {line}" for n, _, line, _, _ in ds["sp"])
    return lstim(f"DS-{ds['key']}", f"Topic: {ds['topic']}\n{body}", "4人の話し合い")


# ======================================================================
# 数値の計算をともなう対話（パラメータで多様化）
# ======================================================================

def calc_dialog(r):
    kind = r.choice(["leave", "price", "arrive", "change"])
    if kind == "leave":
        S = r.choice([18 * 60 + 40, 19 * 60 + 15, 18 * 60 + 30, 17 * 60 + 50, 19 * 60, 18 * 60 + 20])
        t = r.choice([20, 25, 30, 35, 40])
        e = r.choice([10, 15, 20])
        ans = S - t - e
        sc = (f"W: The movie starts at {tw(S)}.\nM: It takes about {nw(t)} minutes to get to the theater from here.\n"
              f"W: And I want to get there {nw(e)} minutes early to buy snacks.\nM: OK. Let's leave just in time, then.")
        q = "What time should they leave?"
        fmt = hm
        f_ok = f"{hm(S)} − {t}分（移動）− {e}分（早めに着く）＝ {hm(ans)}"
        wr = [(S - t, f"早めに着きたい{e}分を引き忘れている。", "条件の聞き落とし", f"{hm(S)} − {t}分"),
              (S - e, f"移動の{t}分を引き忘れている。", "条件の聞き落とし", f"{hm(S)} − {e}分"),
              (S - t + e, f"早めに着く{e}分を足している。到着を早めるには出発をさらに早くする（引く）。", "時間の計算の向きの誤り", f"{hm(S)} − {t}分 ＋ {e}分")]
        chk = (f"{S}-{t}-{e}", str(ans))
    elif kind == "price":
        p = r.choice([1200, 1500, 1800, 2000])
        d = r.choice([200, 300, 500])
        n, a = r.randint(2, 4), r.randint(1, 2)
        ans = n * (p - d) + a * p
        sc = (f"M: How much are the tickets for the aquarium?\nW: They're {p:,} yen each, but students get {d} yen off.\n"
              f"M: There are {nw(n)} of us students, and {'one parent is' if a == 1 else 'two parents are'} coming too.\nW: OK, I'll buy all the tickets together.")
        q = "How much will they pay in total?"
        fmt = yen
        f_ok = f"学生 ({p}−{d})×{n} ＋ 大人 {p}×{a} ＝ {ans:,}円"
        wr = [((n + a) * (p - d), "割引は学生だけで、保護者は正規料金である。", "割引の対象の取り違え", f"({p}−{d})×{n + a}"),
              ((n + a) * p, "学生の割引を忘れている。", "条件の聞き落とし", f"{p}×{n + a}"),
              ((n + a) * p - d, "割引は学生1人ごとにかかる（students get … off）。1回だけ引いている。", "割引の回数の誤り", f"{p}×{n + a} − {d}")]
        chk = (f"{n}*({p}-{d})+{a}*{p}", str(ans))
    elif kind == "arrive":
        X = r.choice([9 * 60 + 10, 10 * 60 + 25, 13 * 60 + 40, 15 * 60 + 5, 8 * 60 + 50])
        Y = r.choice([35, 45, 50, 55])
        Z = r.choice([10, 15, 20])
        ans = X + Y + Z
        sc = (f"M: Our train leaves at {tw(X)}, and the trip usually takes {nw(Y)} minutes.\n"
              f"W: I just heard an announcement. The train is running {nw(Z)} minutes late.\nM: Oh no. I'll tell my aunt that we'll be late.")
        q = "What time will they probably arrive?"
        fmt = hm
        f_ok = f"{hm(X)} ＋ {Y}分（所要時間）＋ {Z}分（遅れ）＝ {hm(ans)}"
        wr = [(X + Y, f"{Z}分の遅れを足し忘れている。", "条件の聞き落とし", f"{hm(X)} ＋ {Y}分"),
              (X + Z, "所要時間を足し忘れ、遅れだけを足している。", "条件の聞き落とし", f"{hm(X)} ＋ {Z}分"),
              (X + Y - Z, "遅れ（late）は到着を遅くするので、足す。", "時間の計算の向きの誤り", f"{hm(X)} ＋ {Y}分 − {Z}分")]
        chk = (f"{X}+{Y}+{Z}", str(ans))
    else:
        p = r.choice([150, 180, 200, 250])
        k = r.choice([3, 4, 5])
        d = r.choice([20, 30, 50])
        n = k + r.randint(0, 2)
        bill = 1000 if n * p <= 1000 else 2000
        ans = bill - n * (p - d)
        sc = (f"W: I'd like {nw(n)} of these notebooks, please.\nM: They're {p} yen each, but if you buy {nw(k)} or more, each one is {d} yen cheaper.\n"
              f"W: Great. Here's a {bill:,}-yen bill.")
        q = "How much change will the woman get?"
        fmt = yen
        f_ok = f"代金 ({p}−{d})×{n}＝{n * (p - d):,}円、おつり {bill:,}−{n * (p - d):,}＝{ans:,}円"
        wr = [(bill - n * p, f"{k}冊以上で1冊{d}円安くなる条件を使っていない。", "条件の聞き落とし", f"{bill}−{p}×{n}"),
              (n * (p - d), "おつりではなく代金を答えている。", "問いの取り違え", f"({p}−{d})×{n}"),
              (bill - (n * p - d), "割引は1冊ごとにかかる。1回だけ引いている。", "割引の回数の誤り", f"{bill}−({p}×{n}−{d})")]
        chk = (f"{bill}-{n}*({p}-{d})", str(ans))
    if kind == "change":
        wr.append((bill - (n - 1) * (p - d), f"買う冊数（{n}冊）を1冊少なく数えている。", "数の聞き取りの誤り", f"{bill}−({p}−{d})×{n - 1}"))
        wr.append((n * p, "おつりではなく、割引前の代金を答えている。", "問いの取り違え", f"{p}×{n}"))
    step = 5 if fmt is hm else 100
    k = 1
    seen, ws = {ans}, []
    for w in wr:
        if w[0] not in seen and w[0] > 0:
            seen.add(w[0])
            ws.append(w)
    while len(ws) < 3:
        v = ans + step * k
        k += 1
        if v not in seen:
            seen.add(v)
            ws.append((v, "聞き取った数の一部を取り違えて計算している。", "数の聞き取りの誤り", "数の一部を取り違えた式"))
    return dict(kind=kind, script=sc, q=q, ans=ans, fmt=fmt, f_ok=f_ok, wrongs=ws, chk=chk)


# ======================================================================
# 授業プリント
# ======================================================================

EX_TIME = DIALOGS[1]

LESSON = lesson(
    goals=["対話を聞く前に設問と選択肢を先読みし、「最終的に何に決まったか」「数値の計算に必要な条件は何か」をとらえられる。",
           "講義を聞きながらワークシートの枠組み（原因・利点・対策など）に沿ってメモを取り、図表と結びつけて内容を判断できる。",
           "複数の話し手の意見について、賛否・理由・条件を整理し、条件に合う選択肢や共通点・相違点を判断できる。"],
    duration=50,
    readiness=["中学で学んだ時刻・数・金額の英語表現（six forty、fifteen / fifty など）を聞いて理解できる。",
               "提案・依頼・応答の表現（How about ～? / Why don't we ～? / Would you mind ～?）の意味を知っている。",
               "ディスコースマーカー（first / second / however / so）の働きを知っている（HS-ENG-U09）。"],
    flow=[("導入：聞く前に勝負が決まる", 5, "先読みの効果を体験させ、共通テストのリスニングでは1回しか読まれない問題もあることを確認する"),
          ("短い対話", 12, "最初の案が変更される対話（例題1）と、言外の意味・応答の選び方を練習する"),
          ("講義と図表", 15, "ワークシートの枠組みでメモを取り、図表と照合する（例題2）"),
          ("複数の意見の比較", 12, "条件表を作って話し手の説明を照合し（例題3）、賛否と条件つき賛成を区別する"),
          ("まとめと確認", 6, "確認問題3問、スクリプトを使った復習（音読・ディクテーション）の方法を指示")],
    sections=[
        intro("in1", "リスニングは「聞く前の準備」と「聞きながらの整理」で決まる",
              "共通テストの英語リスニングでは、短い対話、図やイラストを使った問題、講義とワークシート、複数の話し手の意見など、さまざまな形式の英語を聞く。問題によっては英語が1回しか読まれないため、聞きながら必要な情報を選び取る力が求められる。この授業では音声の代わりに、教師がスクリプトを読み上げる。音声がないときはスクリプトを読んで答えるが、その場合も「1回通して読んだら本文に戻らない」など、聞き取りに近い条件で取り組むこと。",
              bullets=["聞く前：設問・選択肢・図表を先読みし、何を聞き取るか（時刻・場所・理由・賛否）を決める。",
                       "聞きながら：最初の案がそのまま答えになるとは限らない。Actually / But / How about ～? の後で決定が変わる。",
                       "聞いた後：選択肢は言いかえで作られる。聞こえた単語を含む選択肢ほど疑う。"],
              points=[tp("先読みなしで1回聞かせた後、先読みしてからもう1回聞かせ、正答率の違いを挙げさせる。", ask="先読みをすると、聞くときに何が変わったか。",
                         expect="聞き取るべき情報（時刻・場所など）が決まり、そこに集中できた。", timing="導入の冒頭"),
                      tp("読み上げは自然な速さで行い、2回読む問題と1回だけの問題を区別して伝える。", caution="教師がゆっくり読みすぎると、本番の速さとの差が大きくなる。")]),
        definition("df1", "聞き取りの3つの型と、注目する表現",
                   "短い対話では「最終的な決定・相手の意図」、講義では「話の枠組み（原因・利点・対策）と数値」、複数の意見では「賛否・理由・条件」を聞き取る。それぞれの型で、決定や構成を知らせる表現が決まっている。",
                   bullets=["決定が変わる合図：Actually, ～ ／ I was going to ～, but … ／ How about ～? ／ Why don't we ～? ／ Then let's ～.",
                            "講義の構成の合図：First / Second / Third / Finally ／ However ／ So ／ The most effective step is ～.",
                            "賛否の合図：I'm for it ／ I agree with ～ ／ I'm against it ／ I disagree ／ I see why you think that, but …（反対）",
                            "条件つきの意見：I'm for it, but ～ ／ as long as ～（～ならば賛成）"],
                   conditions=["I see why you think that, but … は相手に理解を示してから反対する言い方で、賛成ではない。",
                               "I'm for it, but … は条件つきの賛成で、賛成の人数に数える。"],
                   points=[tp("合図の表現を「決定変更」「構成」「賛否」に分けてカードにし、スクリプトの中で見つけたら手を挙げさせる。", ask="I see why you think that, but I'm against it. は賛成か反対か。",
                              expect="反対。前半は相手への理解を示しているだけ。")]),
        theorem("th1", "リスニングの誤りの選択肢の4類型",
                "① 最初に出た案（後で変更・却下された情報）　② 聞こえた語の組み合わせ（対話に出た単語を別の意味でつなげたもの）　③ 数値の処理もれ（遅れ・割引・早めの到着などの条件を使っていない値）　④ 話し手の取り違え（別の人物の意見・行動）",
                ["正解は、決定の合図の後の内容や、話し手の意図を言いかえたものであることが多い。",
                 "聞こえた単語がそのまま入った選択肢は、②の可能性を疑う。",
                 "数値の問題は、聞いた数をメモし、条件を当てはめて計算してから選択肢を見る。"],
                body="共通テストのリスニングの選択肢は、聞き手が陥りやすい誤りに合わせて作られている。誤りの型を知っていれば、聞き取れた情報が断片的でも、根拠をもって選択肢を絞れる。",
                points=[tp("例題1のスクリプトで、各選択肢が4類型のどれに当たるかを生徒に分類させる。", ask="6:30 はどの型の誤りか。", expect="①最初に出た案。")]),
        derivation("dv1", "講義のメモの取り方（なぜワークシートの枠組みを先に読むのか）",
                   ["① 講義の前に、ワークシートの見出し（Cause / Benefit / Problem / Measure など）と空欄の位置を確認する。",
                    "② 見出しから、講義の構成（原因 → 対策、利点 → 問題点 など）を予測する。",
                    "③ 聞きながら、First / Second / However などの合図が出たら、どの見出しの話に移ったかを判断する。",
                    "④ メモは英語の文ではなく、キーワードと記号（↑増加、↓減少、→結果、×問題点）で取る。",
                    "⑤ 講義の後に示される図表は、メモのどの見出しと対応するかを確認してから読み取る。図表で確かめられることと、確かめられないことを区別する。"],
                   body="1回しか読まれない講義をすべて覚えることはできない。ワークシートの枠組みは「何を聞けばよいか」を示した地図である。先に地図を見ておけば、聞こえた情報をどこに書けばよいかが決まり、聞き取りの負担が大きく減る。",
                   points=[tp("同じ講義を、ワークシートを見ずに聞いた場合と見てから聞いた場合で、メモの量と正確さを比べさせる。", timing="例題2の前"),
                           tp("記号メモの例を板書し、英語の文で書こうとしないよう指導する。", caution="1文ずつ書き取ろうとすると、次の情報を聞き逃す。")]),
        example("ex1", "例題1　最初の案が変わる対話",
                f"対話を聞き、問いに答えなさい。\n{EX_TIME[1]}\n{EX_TIME[2]}\n(a) 6:30　(b) 6:15　(c) 6:20　(d) 7:00",
                ["女性が最初に 6:30 を提案する（最初の案）。", "男性が just in case で 6:15 に早めることを提案する。",
                 "女性が Actually, I finish work at six. と言って 6:20 を提案し、男性が Sure と同意する。", "7:00 はコンサートの開始時刻。"],
                "(c) 6:20",
                thinking="Actually の後で決定が変わる。最後に相手が同意した案が答え。",
                points=[tp("対話の中で出た時刻をすべてメモさせ、どれが最終決定かを Actually と Sure を手がかりに判断させる。", ask="最後に男性が同意した時刻はどれか。",
                           expect="6:20（Sure, no problem.）")],
                misconceptions=[("最初に聞こえた 6:30 を答える。", "最初の案は Actually の後で変更されている。最後に合意した時刻を答える")]),
        example("ex2", "例題2　講義とワークシート・図表",
                f"講義“{LBY['TREE']['title']}”を聞き、ワークシートの Problem 2 の欄に入る内容を選びなさい。\n{LBY['TREE']['text']}\n(a) Shade that keeps the ground cooler　(b) Roots can break sidewalks　(c) Trees make the streets noisier　(d) Homes for birds and insects",
                ["ワークシートの見出しから、講義は「利点 → 問題点」の順に進むと予測する。", "However, street trees also cause some problems. で問題点の話に移る。",
                 "問題点は、落ち葉の清掃（Problem 1）、根が歩道を壊す（Problem 2）、手入れの費用（Problem 3）の順。", "(a)(d) は利点、(c) は講義で述べられていない。"],
                "(b)",
                thinking="However が「利点から問題点へ」の切りかえの合図。問題点の2つ目を聞き取る。",
                points=[tp("講義の後に示す地面の温度の表（架空の資料）を使い、表が裏づけるのは利点1だけで、問題点は表からは確かめられないことを確認する。",
                           ask="この表で、手入れに費用がかかることは確かめられるか。", expect="確かめられない。表には温度しかない。")]),
        example("ex3", "例題3　条件に合うものを選ぶ（複数の話し手）",
                "あなたは夏休みのプログラムを選んでいる。条件は「A. 期間は3日以内」「B. 参加費は無料」「D. 英語を使う機会がある」である。4人の説明を聞き、条件に合うものを選びなさい。\n"
                + "\n".join(f"Speaker {i + 1}: {PROGRAMS[j][1]}" for i, j in enumerate([0, 1, 4, 2]))
                + "\n(a) Science Camp　(b) Beach Clean-Up Week　(c) Library Reading Volunteers　(d) Museum Guide Training",
                ["条件表（A・B・D × 4つのプログラム）を作ってから聞く。", "Science Camp：4日間・6,000円・日本語 → A×、B×、D×。",
                 "Beach Clean-Up Week：3日間・無料・英語を使う → すべて〇。", "Library Reading Volunteers：3日間・無料・日本語 → D×。", "Museum Guide Training：2日間・3,000円・英語 → B×。"],
                "(b)",
                thinking="条件を表の列にして、聞きながら〇×を記入する。1つでも×があれば消去する。",
                points=[tp("〇×の表をあらかじめ配り、聞きながら記入させる。全部の欄を埋めようとせず、×が1つ出たらその行は次へ進んでよいことを伝える。")]),
        board("bd1", "板書案",
              [("① 短い対話", ["先読み：何を聞くか決める", "Actually / How about ～? で変更", "最後に合意した案が答え", "言外の意味：断り・遠回しの評価"]),
               ("② 講義と図表", ["ワークシートの見出しを先に読む", "First / However / So で区切る", "メモは記号（↑↓→×）", "図表で確かめられること／られないこと"]),
               ("③ 複数の意見", ["条件表を作って〇×", "I'm for it, but ～ ＝条件つき賛成", "I see why …, but ＝反対", "誤り：最初の案・語の組み合わせ・計算もれ・人違い"])],
              points=[tp("③の条件表は、例題3の表をそのまま板書し、生徒の記入と照らし合わせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("スクリプトを使う場合も、最初は見せずに読み上げ、答えを確認した後でスクリプトを配って聞き取れなかった箇所に線を引かせる。", timing="各例題の後"),
               tp("数値の問題では、聞いた数を必ずメモさせ、計算してから選択肢を見る。", caution="選択肢を先に見ると、条件を1つ使い忘れた値を選びやすい。"),
               tp("議論の問題では、話し手ごとに「賛成／反対／条件つき賛成」と理由を1語でメモさせる。", ask="Hiro は賛成か反対か。", expect="条件つきの賛成（as long as ～）。"),
               tp("講義の図表問題では、「図表から言えること」と「言えないこと」を区別させる。図表にない情報を推測で補う誤りが多い。"),
               tp("復習では、スクリプトの音読とディクテーションを組み合わせる。聞き取れなかった原因（語を知らない・音の連結・速さ）を分類させる。")],
              misconceptions=[("対話で最初に聞こえた案を答える。", "Actually / How about ～? の後で決定が変わる。最後に合意した案を答える"),
                              ("聞こえた単語を含む選択肢を選ぶ。", "正解は言いかえで作られることが多い。聞こえた語の組み合わせは誤りの典型"),
                              ("I see why you think that, but … を賛成とする。", "相手に理解を示した後に反対している")]),
        summary("sm1", "まとめ",
                ["聞く前に先読みし、何を聞き取るかを決める。最初の案ではなく、最後に合意した内容が答え。",
                 "講義はワークシートの枠組みを地図にして、合図の表現で区切りながら記号でメモする。図表で確かめられることを区別する。",
                 "複数の意見は、条件表と「賛成／反対／条件つき」のメモで整理する。誤りの4類型で選択肢を絞る。"]),
        check("ck1", "確認問題",
              [("“I'm for it, as long as teachers give us a little extra work.” の話し手の立場は何か。", "条件つきの賛成"),
               ("“Would you mind if I opened the window?” に許可を与える応答を英語で答えなさい。", "Not at all. / Of course not. など（No の向きで答える）"),
               ("電車の出発が 9:10、所要時間が 45 分、15 分遅れているとき、到着は何時ごろか。", "10:10")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["concept", "common_error"])
def a_dialog_final(r):
    did, sc, q, ok, wrongs = r.choice(DIALOGS)
    return mc(f"短い対話を聞き、問いの答えとして最も適切なものを選びなさい。（場面 {did}）\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　対話の途中で案が変わり、最後に合意した内容が答えになる。", d=2, stim=lstim(f"DL-{did}", sc, "短い対話"),
              ap="設問を先読みして聞き取る情報（時刻・場所・物）を決め、Actually / How about ～? / Then let's ～ などの決定が変わる合図に注意する。",
              steps=["設問を先読みし、何を聞き取るかを決める。", "対話に出てきた候補をすべてメモする。", "却下された候補（理由つき）に×をつける。", f"最後に合意した内容：{ok}"],
              alt=["選んだ答えのあとに、相手が同意する表現（OK / Sure / Sounds good / That works）があるかを確かめる。"],
              pc=[("候補と却下の理由を聞き取っている", 1), ("最終的な決定を選んでいる", 1)],
              pit=["最初に聞こえた案をそのまま答える。"], why={w: (why, "最初の案・聞こえた語への引きずられ") for w, why in wrongs})


@gen("basic_check", 5, ["concept", "application"])
def a_inference(r):
    sc, q, ok, wrongs = r.choice(INFER)
    return mc(f"短い対話を聞き、話し手の意図として最も適切なものを選びなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　直接 yes / no を言わずに、理由や状況を述べることで答えを伝えている。", d=2, stim=lstim(f"IF-{zlib.crc32(sc.encode()) % 100000}", sc, "短い対話"),
              ap="最初の発話が誘い・依頼・質問のどれかを確認し、それに対する応答が「受け入れ」か「断り」かを、理由の内容から判断する。",
              steps=["最初の発話の種類（誘い・依頼・提案・質問）を確認する。", "応答の文が、その発話に対して何を伝えているか（できない理由・状態）を考える。", f"意図：{ok}"],
              alt=["応答を yes / no で言いかえるとどちらになるかを考え、選んだ選択肢と一致するか確かめる。"],
              pc=[("最初の発話の種類をとらえている", 1), ("応答の意図を選んでいる", 1)],
              pit=["応答の中の単語だけを手がかりに、聞こえた語を含む選択肢を選ぶ。"], why={w: (why, "言外の意味の取り違え") for w, why in wrongs})


@gen("basic_check", 5, ["concept", "condition_check"])
def a_response(r):
    line, ok, wrongs = r.choice(RESP)
    return mc(f"対話の最後の発話を聞き、それに続く応答として最も適切なものを選びなさい。\n{line}", [ok] + [w for w, _ in wrongs],
              f"{ok}　発話の種類（依頼・質問・お礼・報告）と、疑問詞・時制に合った応答を選ぶ。", d=2,
              ap="最後の発話が「何を求めているか」（情報・許可・同情・お礼への返事）を判断し、疑問詞や時制に合う応答を選ぶ。",
              steps=["発話の種類と、疑問詞（How long / Which / What time）や時制を確認する。", "その種類に合わない応答（話題のずれ・時制の不一致）を消す。", f"適切な応答：{ok}"],
              alt=["選んだ応答を続けて読み、対話として自然につながるかを確かめる。"],
              pc=[("発話の種類・疑問詞をとらえている", 1), ("適切な応答を選んでいる", 1)],
              pit=["発話の中の単語と同じ語を含む応答を選ぶ。"], why={w: (why, "応答の条件（疑問詞・時制・場面）の不一致") for w, why in wrongs})


@gen("basic_check", 5, ["computation", "condition_check"])
def a_number_calc(r):
    c = calc_dialog(r)
    ws = c["wrongs"][:3]
    f = c["fmt"]
    return mc(f"対話を聞き、問いの答えとして最も適切なものを選びなさい。\n{c['q']}", [f(c["ans"])] + [f(w[0]) for w in ws],
              f"{f(c['ans'])}。{c['f_ok']}。", d=2, stim=lstim(f"NC-{c['kind']}", c["script"], "数値を含む対話"),
              ap="聞こえた数（時刻・所要時間・料金・割引）をすべてメモし、計算に使う条件（遅れ・早めに着く・割引の対象）を確認してから計算する。",
              steps=["聞こえた数をメモする。", "条件（足すのか引くのか、だれに割引がかかるのか）を確認する。", f"計算する：{c['f_ok']}。", "選択肢と照合する。"],
              alt=["答えから逆算して、対話の条件（到着時刻・合計など）がすべて満たされるかを確かめる。"],
              pc=[("必要な数と条件を聞き取っている", 1), ("正しく計算している", 1)],
              pit=["聞こえた時刻や金額をそのまま選ぶ。", "条件を1つ使い忘れる。"], why={f(w[0]): (w[1], w[2]) for w in ws},
              chk=(c["chk"][0], c["chk"][1], None, "intermediate"))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["concept", "computation"])
def b_lecture_blank(r):
    lc = r.choice(LECTURES)
    i = r.randrange(len(lc["rows"]))
    lab, ok = lc["rows"][i]
    others = [(j, v) for j, (_, v) in enumerate(lc["rows"]) if j != i]
    picks = r.sample(others, 2)
    fake = r.choice(lc["fake"])
    why = {v: (f"講義では {lc['rows'][j][0]} の内容として述べられており、{lab} ではない。", "メモの見出しの取り違え") for j, v in picks}
    why[fake] = ("講義で述べられていない内容である。", "聞こえた語からの推測")
    return mc(f"講義“{lc['title']}”を聞き、ワークシートの空欄①（{lab}）に入る内容として最も適切なものを選びなさい。", [ok] + [v for _, v in picks] + [fake],
              f"{ok}　{lab} の話は、講義の構成の合図（First / Second / However など）の後で述べられている。", d=3, stim=lect_stim(lc), tbl=worksheet(lc, blank=i),
              ap="ワークシートの見出しの順番から講義の構成を予測し、空欄の見出しの話が始まる合図（First / Second / However / So など）を待って聞く。",
              steps=["ワークシートの見出しと空欄の位置を確認する。", "講義の構成（原因 → 対策、利点 → 問題点など）を予測する。", f"{lab} に当たる部分を聞き取る。", f"答え：{ok}"],
              alt=["ほかの欄の内容を順に確認し、残りの選択肢がどの欄の内容かを特定して消去する。"],
              pc=[("講義の構成をとらえている", 2), ("空欄の内容を選んでいる", 2)],
              pit=["別の見出しの内容を、聞こえた順番だけで選ぶ。"], why=why)


@gen("standard_practice", 5, ["concept", "application"])
def b_lecture_content(r):
    lc = r.choice(LECTURES)
    if r.random() < 0.5:
        return mc(f"講義“{lc['title']}”を聞き、講師が最も伝えたいこととして最も適切なものを選びなさい。", [lc["main"]] + [w for w, _ in lc["main_wrong"]],
                  f"{lc['main']}　講義の最後の段落（So / I think / The most effective step is）を中心に、However の前後をまとめる。", d=3, stim=lect_stim(lc),
                  ap="講義の最後の部分（結論）と、However で示される限界・問題点の両方を含む選択肢を探す。",
                  steps=["講義の話題（最初の文）を確認する。", "First / Second などで挙げられた要点をメモする。", "However の後の限界・問題点を確認する。", "結論の文を確認し、全体を含む選択肢を選ぶ。"],
                  alt=["選んだ選択肢が、講義の一部（具体例）だけになっていないか、言いすぎ（only / completely）になっていないかを確かめる。"],
                  pc=[("講義の構成と結論をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
                  pit=["印象に残った具体例や数値を主旨として選ぶ。"], why={w: (why, "主旨と部分・譲歩の混同") for w, why in lc["main_wrong"]})
    ok = r.choice(lc["trues"])
    return mc(f"講義“{lc['title']}”を聞き、講義の内容と一致するものを選びなさい。", [ok] + [w for w, _ in lc["falses"]],
              f"{ok}　講義の該当箇所の言いかえになっている。", d=3, stim=lect_stim(lc),
              ap="選択肢を先読みし、それぞれに含まれるキーワード（数・比較・否定）を講義で確かめる。",
              steps=["選択肢のキーワードを先読みする。", "講義の該当箇所を聞き取る。", "逆・言いすぎ・書かれていないものを消去する。", f"一致するのは：{ok}"],
              alt=["誤りの選択肢について、講義のどの部分と食い違うかをスクリプトで確かめる。"],
              pc=[("該当箇所を聞き取っている", 2), ("一致する選択肢を選んでいる", 2)],
              pit=["all / never / only などの強い語を聞き落とす。"], why={w: (why, "講義との照合不足") for w, why in lc["falses"]})


@gen("standard_practice", 5, ["condition_check", "computation"])
def b_condition_fit(r):
    for _ in range(300):
        tgt = r.choice(PROGRAMS)
        name, _, days, fee, place, en = tgt
        kinds = ["days", "fee", "place"] + (["en"] if en else [])
        ks = r.sample(kinds, 3)
        cond = {}
        for k in ks:
            if k == "days":
                cond["days"] = days if r.random() < 0.6 else days + 1
            elif k == "fee":
                cond["fee"] = fee if fee == 0 else r.choice([fee, ((fee + 999) // 1000) * 1000])
            elif k == "place":
                cond["place"] = place
            else:
                cond["en"] = True
        others = [p for p in PROGRAMS if p is not tgt and prog_fail(p, cond)]
        if len(others) >= 3 and not prog_fail(tgt, cond):
            break
    picks = r.sample(others, 3)
    shown = picks + [tgt]
    r.shuffle(shown)
    script = "\n".join(f"Speaker {i + 1}: {p[1]}" for i, p in enumerate(shown))
    ct = "／".join(cond_text(cond))
    why = {p[0]: ("；".join(prog_fail(p, cond)) + "。", "条件の照合もれ") for p in picks}
    return mc(f"あなたは夏休みのプログラムを1つ選ぼうとしている。条件は「{ct}」である。4人の説明を聞き、条件にすべて合うものを選びなさい。",
              [name] + [p[0] for p in picks],
              f"{name}（{days}日間・{'無料' if fee == 0 else f'{fee:,}円'}・{'屋内' if place == 'indoors' else '屋外'}・{'英語を使う' if en else '日本語のみ'}）だけがすべての条件を満たす。", d=3,
              stim=lstim(f"PG-{zlib.crc32(script.encode()) % 100000}", script, "4人の説明"),
              ap="条件を列にした〇×の表を作ってから聞き、各プログラムについて条件ごとに〇×を記入する。×が1つでもあれば消去する。",
              steps=[f"条件を確認する：{ct}。", "話し手ごとに、期間・参加費・場所・使う言語をメモする。", "条件に合わない項目に×をつける。", f"すべて〇なのは {name}。"],
              alt=["正解のプログラムについて、条件ごとに講義（説明）のどの語句が根拠になるかを確かめる。"],
              pc=[("条件ごとに照合している", 2), ("条件に合うものを選んでいる", 2)],
              pit=["条件の1つだけ（無料など）で判断し、ほかの条件を確かめない。", "It's free を聞き落とし、参加費の条件で消去してしまう。"], why=why)


@gen("standard_practice", 5, ["concept", "common_error"])
def b_discussion(r):
    ds = r.choice(DISCUSSIONS)
    mode = r.choice(["count", "closest", "who"])
    st = disc_stim(ds)
    sp = ds["sp"]
    if mode == "count":
        n = sum(1 for s in sp if s[1])
        cands = [x for x in range(1, 5) if x != n]
        wrongs = r.sample(cands, 3)
        why = {}
        for w in wrongs:
            if w < n:
                why[COUNT_EN[w]] = ("条件つきの賛成（I'm for it, but ～ / as long as ～）も賛成に数える。", "条件つき賛成の見落とし")
            else:
                why[COUNT_EN[w]] = ("I disagree / I'm against it / I see why …, but I'm against it などの反対の発言者まで数えている。", "反対の言い方の聞き落とし")
        names = "、".join(s[0] for s in sp if s[1])
        return mc(f"「{ds['jtopic']}」についての4人の話し合いを聞き、提案に賛成している人の数として最も適切なものを選びなさい。", [COUNT_EN[n]] + [COUNT_EN[w] for w in wrongs],
                  f"{COUNT_EN[n]}（{names}）。条件つきの賛成も賛成に数える。", d=3, stim=st,
                  ap="話し手ごとに「賛成・反対・条件つき賛成」を1語でメモしながら聞く。",
                  steps=["話し手ごとに立場をメモする。", "I'm for it, but ～ / as long as ～ は条件つき賛成として賛成に数える。", "I see why …, but I'm against it は反対。", f"賛成は {names} の {n} 人。"],
                  alt=["反対の人数を数え、4から引いて確かめる。"],
                  pc=[("各話し手の立場を聞き取っている", 2), ("人数を正しく答えている", 2)],
                  pit=["条件つき賛成を反対に数える。", "相手に理解を示す前置き（I see why you think that）を賛成と取り違える。"], why=why)
    if mode == "closest":
        i = r.randrange(4)
        name, _, _, jr, para = sp[i]
        others = [s for j, s in enumerate(sp) if j != i]
        why = {s[4]: (f"{s[0]} の意見である（{s[3]}）。", "話し手の取り違え") for s in others}
        return mc(f"「{ds['jtopic']}」についての4人の話し合いを聞き、{name} の意見に最も近いものを選びなさい。", [para] + [s[4] for s in others],
                  f"{para}　{name} は「{jr}」と述べている。", d=3, stim=st,
                  ap="話し手の名前と、その人の立場・理由をセットでメモする。選択肢はほかの話し手の意見の言いかえで作られている。",
                  steps=[f"{name} の発言を聞き取る。", f"理由を確認する：{jr}。", "各選択肢がだれの意見の言いかえかを判断する。", f"{name} の意見：{para}"],
                  alt=["ほかの3つの選択肢が、それぞれだれの意見かを特定して消去する。"],
                  pc=[("話し手の立場と理由を聞き取っている", 2), ("正しい選択肢を選んでいる", 2)],
                  pit=["別の話し手の意見を選ぶ（人違い）。"], why=why)
    i = r.randrange(4)
    name, _, _, jr, para = sp[i]
    others = [s[0] for j, s in enumerate(sp) if j != i]
    return mc(f"「{ds['jtopic']}」についての4人の話し合いを聞き、「{jr}」という趣旨の発言をした人を選びなさい。", [name] + others,
              f"{name}。{name} は「{jr}」と述べている。", d=3, stim=st,
              ap="理由の内容（日本語）を先読みし、それに当たる英語の表現を待って聞く。",
              steps=["設問の理由の内容を先読みする。", "話し手ごとの理由をメモする。", f"その理由を述べたのは {name}。"],
              alt=["ほかの3人の理由をそれぞれ確認し、設問の内容と違うことを確かめる。"],
              pc=[("話し手ごとの理由を聞き取っている", 2), ("正しい人物を選んでいる", 2)],
              pit=["同じ立場の別の話し手と取り違える。"],
              why={s[0]: (f"{s[0]} は「{s[3]}」と述べている。", "話し手の取り違え") for j, s in enumerate(sp) if j != i})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_lecture_summary(r):
    lc = r.choice(LECTURES)
    lim = r.choice([90, 100, 110])
    return desc(f"講義“{lc['title']}”を聞き、講義の要点を日本語{lim}字以内でまとめなさい。", lc["summary"],
                "講義の構成（話題 → 要点（First / Second …）→ 限界・問題点（However）→ 結論）に沿って、具体例や数値を除いてまとめる。",
                lc["skeys"], d=4, p=8, grid=lim, stim=lect_stim(lc),
                ap="メモした見出し（原因・利点・問題点・対策など）を順につなぎ、最後に講師の結論を書く。",
                steps=["話題と、First / Second などで挙げられた要点を確認する。", "However の後の限界・問題点を確認する。", "結論（So / I think / The most effective step）を確認する。", "要点 → 問題点 → 結論の順に、字数内でまとめる。"],
                alt=["まず英語で講師の結論を1文で書き、それを日本語にしてから要点を加える方法もある。"],
                pc=[(k, v) for k, v in lc["skeys"]],
                pit=["数値や具体例を並べて字数を使い、結論を書き落とす。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["CT-ENG-U01", "HS-ENG-U10"])
def c_compare_opinions(r):
    ds = r.choice(DISCUSSIONS)
    fors = [s for s in ds["sp"] if s[1]]
    agn = [s for s in ds["sp"] if not s[1]]
    a, b = r.choice(fors), r.choice(agn)
    st = disc_stim(ds)
    if r.random() < 0.5:
        return desc(f"「{ds['jtopic']}」についての4人の話し合いを聞き、{a[0]} と {b[0]} の意見を比べて、それぞれの立場と理由を日本語で説明しなさい。さらに、2人の意見の対立点を1文で述べなさい。",
                    f"{a[0]}：賛成。{a[3]}。{b[0]}：反対。{b[3]}。対立点：提案を実施することの利点（{a[3]}）と、それにともなう問題（{b[3]}）のどちらを重く見るかで意見が分かれている。",
                    "複数の話し手の意見は、立場（賛成・反対・条件つき）と理由をセットで整理し、何についての評価が違うのかを対立点としてまとめる。",
                    [(f"{a[0]} の立場と理由を正しく説明している", 3), (f"{b[0]} の立場と理由を正しく説明している", 3), ("対立点を的確にまとめている", 2)], d=4, p=8, lines=6, stim=st,
                    ap="話し手ごとに「立場・理由」をメモし、2人の理由が提案のどの側面（利点・問題）に注目しているかを比べる。",
                    steps=[f"{a[0]} の立場と理由をメモする。", f"{b[0]} の立場と理由をメモする。", "2人の理由が注目している点（利点か問題か）を比べる。", "立場・理由・対立点の順に答案を書く。"],
                    alt=["表（話し手 × 立場・理由・条件）を作ってから文章にする。"],
                    pc=[(f"{a[0]} の説明", 3), (f"{b[0]} の説明", 3), ("対立点", 2)],
                    pit=["2人の理由を入れ違えて書く。", "条件つき賛成の条件を書き落とす。"])
    return desc(f"「{ds['jtopic']}」についての4人の話し合いを聞き、あなた自身の意見を英語で書きなさい。話し合いに出た意見のうち1人の意見に触れ（I agree / disagree with ～）、理由を1つ以上含めて30語程度とする。",
                f"（解答例）I agree with {a[0]}. {a[4]} I also think it would be good for our school, because it gives students a new experience.",
                "話し合いの中の意見に触れて自分の立場を示し、自分の経験や具体例で理由を加える。",
                [("話し合いの意見に触れて立場を明確にしている", 3), ("理由を具体的に述べている", 3), ("文法・語法が正しく、語数が適切である", 2)], d=4, p=8, lines=6, stim=st,
                ap="I agree with ～ / I disagree with ～ で始め、because や For example で理由を加える。話し手の英文をそのまま写さず、自分の言葉で書く。",
                steps=["4人の立場と理由をメモする。", "自分の立場を決め、触れる話し手を選ぶ。", "理由を1つ以上、自分の経験や具体例で考える。", "立場 → 理由 → 具体例の順に30語程度で書く。"],
                alt=["条件つきで賛成する書き方（I agree with ～, as long as …）もできる。"],
                pc=[("立場の明示", 3), ("理由の具体性", 3), ("文法・語数", 2)],
                pit=["話し手の英文をそのまま写す。", "だれの意見に触れているかを書かない。"])


@gen("thinking_writing", 3, ["written_reasoning", "application"])
def c_chart_reason(r):
    lc = r.choice(LECTURES)
    if r.random() < 0.6:
        return desc(f"講義“{lc['title']}”を聞きなさい。{lc['chart_q']}", lc["chart_a"],
                    "図表の数値を具体的に引用し、講義のどの説明と結びつくか（また、図表だけでは何が言えないか）を区別して説明する。",
                    [("図表の数値を正しく引用している", 3), ("講義の内容と正しく結びつけている", 3), ("図表で言えること・言えないことを区別している", 2)], d=5, p=8, lines=6,
                    stim=lect_stim(lc), tbl=lc["chart"],
                    ap="まず図表が何を比べているか（項目・単位・期間）を確認し、講義のメモのどの見出しと対応するかを探す。",
                    steps=["図表の項目と単位を確認する。", "数値の大小・変化を読み取る。", "講義のどの説明と対応するかを判断する。", "図表にないデータが必要な主張は「言えない」とする。"],
                    alt=["講義の主張を1つずつ挙げ、それぞれ図表で確かめられるかを〇×で整理してから書く。"],
                    pc=[("数値の引用", 3), ("講義との対応", 3), ("言えること・言えないことの区別", 2)],
                    pit=["図表にないデータ（費用・原因など）まで図表から言えると考える。", "数値を引用せずに「増えている」とだけ書く。"])
    return desc(f"講義“{lc['title']}”を聞き、講師の主張を英語1文で書きなさい。また、その主張を支える講義中の根拠を2つ、日本語で挙げなさい。",
                f"主張：{lc['main']}　根拠（例）：{lc['evid']}。",
                "講師の主張は講義の結論部分にある。根拠はワークシートの見出しにまとめた要点から選ぶ。",
                [("講師の主張を英語1文で正しく書いている", 3), ("根拠を2つ、講義に即して挙げている", 3), ("文法・語法が正しい", 2)], d=4, p=8, lines=6, stim=lect_stim(lc),
                ap="結論部分（So / I think / The most effective step）を主張とし、First / Second などで挙げられた要点を根拠にする。",
                steps=["講義の結論部分を聞き取り、主張を英語1文にする。", "ワークシートの見出しの要点から、主張を支えるものを2つ選ぶ。", "根拠を日本語で書く。"],
                alt=["主張の文を書いた後、根拠の2つを because でつないだ英文にできるかを確かめる。"],
                pc=[("主張の英文", 3), ("根拠2つ", 3), ("文法", 2)],
                pit=["講義の具体例の1つを主張として書く。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "written_reasoning"])
def d_first_info(r):
    did, sc, q, ok, wrongs = r.choice(DIALOGS)
    wrong, why = wrongs[0]
    sol = f"{q} → {wrong}"
    return desc(f"次の短い対話を聞き、問い “{q}” に答える問題で、ある生徒は “{wrong}” と答えた。\n［ある生徒の解答］\n{sol}\nこの解答の誤りの原因を説明し、正しい答えを英語で書きなさい。",
                f"誤りの原因：{why}　正しい答え：{ok}",
                "対話の最初に出た案は、Actually / But / How about ～? などの後で変更・却下されることが多い。最後に合意した内容を答える。",
                [("誤りの原因（最初の案が変更されたこと）を説明している", 2), ("変更の根拠となる発言に触れている", 2), ("正しい答えを書いている", 2)], d=3, p=6, lines=5,
                stim=lstim(f"DL-{did}", sc, "短い対話"),
                ap="生徒の答えが対話のどの時点で出た情報かを確かめ、その後にそれを変更・却下する発言がないかを探す。",
                steps=[f"生徒の答え “{wrong}” が対話のどこに出てくるかを確かめる。", f"その後の発言で変更・却下されている：{why}", f"最後に合意した内容：{ok}"],
                alt=["対話に出てきた候補をすべて書き出し、却下の理由を横に書いてから最後に残ったものを確かめる。"],
                pc=[("原因の説明", 2), ("根拠の発言", 2), ("正しい答え", 2)],
                pit=["最初の発話だけで答えを決め、後半を聞かない。"],
                err=dict(sol=sol, step="最初に出た案を答えにした", type="interpretation", tempt="最初に聞こえた具体的な情報は記憶に残りやすく、その後の変更を聞き落としやすい。", fix=ok))


@gen("error_correction", 3, ["common_error", "computation"])
def d_calc_err(r):
    c = calc_dialog(r)
    f = c["fmt"]
    w = r.choice(c["wrongs"])
    sol = f"{w[3]} として、{f(w[0])} と答えた。"
    return desc(f"次の対話を聞き、問い “{c['q']}” に答える問題で、ある生徒は次のように解いた。\n［ある生徒の解答］\n{sol}\nこの解答の誤りを指摘し、正しい答えを求めなさい。",
                f"誤り：{w[1]}　正しい計算：{c['f_ok']}。答え {f(c['ans'])}",
                "対話の数値を問う問題では、聞こえた数をすべてメモし、足すか引くか・何回かけるかなどの条件を確認してから計算する。",
                [("誤りの箇所と理由を指摘している", 2), ("条件を使った正しい計算を示している", 3), ("正しい答えを書いている", 1)], d=3, p=6, lines=5,
                stim=lstim(f"NC-{c['kind']}", c["script"], "数値を含む対話"),
                ap="生徒の式と対話の条件（遅れ・早めに着く・割引の対象と回数）を1つずつ照らし合わせる。",
                steps=["対話に出てきた数と条件をすべて書き出す。", f"生徒の式の誤り：{w[1]}", f"正しい計算：{c['f_ok']}。", f"答え：{f(c['ans'])}"],
                alt=["正しい答えから逆算して、対話の条件をすべて満たすかを確かめる。"],
                pc=[("誤りの指摘", 2), ("正しい計算", 3), ("正しい答え", 1)],
                pit=["聞こえた数を使う順番だけを気にして、条件の意味（足す・引く）を考えない。"],
                err=dict(sol=sol, step="条件の当てはめ", type="calculation" if "向き" in w[2] else "condition", tempt=f"{w[2]}。数をメモすることに集中すると、条件を表す語（late / early / off / each）を聞き落としやすい。",
                         fix=f"{c['f_ok']}。答え {f(c['ans'])}"),
                chk=(c["chk"][0], c["chk"][1], None, "intermediate"))


@gen("error_correction", 3, ["common_error", "concept"])
def d_worksheet_err(r):
    lc = r.choice(LECTURES)
    i, j = r.sample(range(len(lc["rows"])), 2)
    lab, ok = lc["rows"][i]
    wrong_val = lc["rows"][j][1]
    sol = f"{lab}：{wrong_val}"
    return desc(f"講義“{lc['title']}”を聞いてワークシートを完成させる課題で、ある生徒は次のように書いた。\n［ある生徒の解答（一部）］\n{sol}\nこのメモの誤りを指摘し、正しい内容を英語で書きなさい。",
                f"誤り：“{wrong_val}” は講義では {lc['rows'][j][0]} の内容である。正しい内容：{ok}",
                "講義の構成の合図（First / Second / However など）で、どの見出しの話に移ったかを判断してメモする。",
                [("誤りの内容がどの見出しのものかを指摘している", 2), ("正しい内容を書いている", 3), ("構成の合図に触れて説明している", 1)], d=3, p=6, lines=5,
                stim=lect_stim(lc), tbl=worksheet(lc, filled={i: wrong_val}),
                ap="生徒が書いた内容が講義のどの部分で述べられたかを確かめ、見出しとの対応を合図の表現で判断する。",
                steps=[f"“{wrong_val}” が講義のどこで述べられたかを確かめる（{lc['rows'][j][0]} の内容）。", f"{lab} に当たる部分を講義で探す。", f"正しい内容：{ok}"],
                alt=["ワークシートのすべての欄を講義の順番どおりに埋め直し、同じ内容が2つの欄に入っていないかを確かめる。"],
                pc=[("誤りの指摘", 2), ("正しい内容", 3), ("合図への言及", 1)],
                pit=["聞こえた順番だけで欄を埋め、合図の表現で区切らない。"],
                err=dict(sol=sol, step=f"{lab} の欄", type="interpretation", tempt="講義の要点はどれも似た長さの句なので、合図を聞き落とすと別の見出しの内容を書きやすい。", fix=f"{lab}：{ok}"))


GENERATORS = [a_dialog_final, a_inference, a_response, a_number_calc,
              b_lecture_blank, b_lecture_content, b_condition_fit, b_discussion,
              c_lecture_summary, c_compare_opinions, c_chart_reason,
              d_first_info, d_calc_err, d_worksheet_err]
