"""パイロット：神奈川県公立高校入試型 5教科オリジナル模試（第1回）。

各教科 100 点・50 分。近年の学力検査の大問構成（マークシート方式中心・一部記述）を参考にした
オリジナル問題。古文は著作権保護期間が満了した『徒然草』を用いる。
"""
from ._common import desc, figure, mc, num, order, plane, sa, shape, stim, table

PHASE = 1

E, M, J, R, S = "EX-KNG-MOCK-ENG", "EX-KNG-MOCK-MATH", "EX-KNG-MOCK-JPN", "EX-KNG-MOCK-SCI", "EX-KNG-MOCK-SOC"


def tag(unit, sec, items, prefix):
    out = []
    for no, it in items:
        it["u"] = unit
        it["sec"] = sec
        it["no"] = f"{prefix} {no}"
        it.setdefault("labels", "num")
        out.append(it)
    return out


# ============================== 英語 ==============================
L = ["listening"]
eng = []
eng += tag(E, "ENG-1", [
    ("問1(ア)No.1", mc("対話を聞いて、最後の発言に対する応答として最も適切なものを選びなさい。",
                     ["It's tomorrow morning.", "I studied at home.", "It was very difficult.", "For three hours."],
                     "最後に When is the test?（テストはいつ？）とたずねているので、時を答える It's tomorrow morning. が適切。", d=2, k=L, p=4, st="E-L1")),
    ("問1(ア)No.2", mc("対話を聞いて、最後の発言に対する応答として最も適切なものを選びなさい。",
                     ["About fifteen minutes.", "It's two hundred yen.", "At the next stop.", "Every ten minutes."],
                     "How long does it take?（どのくらい時間がかかるか）に対しては所要時間を答える。Every ten minutes. はバスの運行間隔なので不適切。", d=2, k=L, p=4, st="E-L2")),
    ("問1(イ)No.1", mc("対話を聞いて、質問に対する答えとして最も適切なものを選びなさい。\nQuestion: What will Ken and Emma do on Saturday afternoon?",
                     ["They will go to the library.", "They will have a piano lesson.", "They will study about space at school.", "They will meet at the library at two."],
                     "ケンが図書館に行こうと誘い、エマが承諾している。2時に会うのは駅（station）なので4は誤り。ピアノのレッスンは土曜日の午前。", d=3, k=L, p=4, st="E-L3")),
    ("問1(イ)No.2", mc("対話を聞いて、質問に対する答えとして最も適切なものを選びなさい。\nQuestion: What will Yuta do tomorrow?",
                     ["He will take his speech to Ms. Brown.", "He will make a speech about his town.", "He will check Ms. Brown's English.", "He will eat lunch with Ms. Brown."],
                     "Yuta は I'll bring it to you tomorrow. と言っている。スピーチをするのは来週。", d=3, k=L, p=4, st="E-L4")),
    ("問1(ウ)", mc("英文を聞いて、その内容に合うものを選びなさい。",
                 ["Visitors can see the baby pandas in the morning.", "Visitors can give food to the pandas at one thirty.", "The zoo opens at ten thirty.", "The zoo closes at five thirty."],
                 "赤ちゃんパンダは午前10時から12時まで見られる。1時30分にえさをあげられるのはゾウ。閉園は5時。", d=3, k=L, p=3, st="E-L5")),
], "英")
eng += tag(E, "ENG-2", [
    ("問2(ア)", mc("（　）に入る最も適切な語を選びなさい。\nI got up at eight this morning, so I was (　　) for school.", ["late", "early", "free", "ready"],
                 "8時に起きたので学校に遅刻した、という流れ。be late for ～ で「～に遅れる」。", d=1, k=["vocabulary"], p=3)),
    ("問2(イ)", mc("（　）に入る最も適切な語を選びなさい。\nPlease (　　) your name on this paper.", ["write", "read", "speak", "listen"],
                 "on this paper（この紙に）とあるので「名前を書く」。", d=1, k=["vocabulary"], p=3)),
    ("問2(ウ)", mc("（　）に入る最も適切な語を選びなさい。\nDecember is the twelfth (　　) of the year.", ["month", "week", "season", "day"],
                 "12月は1年の12番目の月（month）。", d=1, k=["vocabulary"], p=3)),
], "英")
eng += tag(E, "ENG-3", [
    ("問3(ア)", mc("（　）に入る最も適切なものを選びなさい。\nMy brother (　　) soccer every Sunday.", ["plays", "play", "playing", "to play"],
                 "主語 My brother は3人称単数で、every Sunday（毎週日曜日）と習慣を表す現在形なので plays。", d=1, k=["grammar"], p=3)),
    ("問3(イ)", mc("（　）に入る最も適切なものを選びなさい。\nThe letter (　　) by my grandmother was very kind.", ["written", "wrote", "writing", "writes"],
                 "「祖母によって書かれた手紙」なので過去分詞 written が後ろから letter を修飾する。", d=2, k=["grammar"], p=3)),
    ("問3(ウ)", mc("（　）に入る最も適切なものを選びなさい。\nI have (　　) this movie three times.", ["seen", "saw", "see", "seeing"],
                 "have ＋過去分詞の現在完了（経験）。see の過去分詞は seen。", d=2, k=["grammar"], p=3)),
    ("問3(エ)", mc("（　）に入る最も適切なものを選びなさい。\nDo you know (　　) she lives?", ["where", "who", "what", "which"],
                 "間接疑問文。「彼女がどこに住んでいるか知っていますか」。live は自動詞なので what や which は続かない。", d=2, k=["grammar"], p=3)),
], "英")
eng += tag(E, "ENG-4", [
    ("問4(ア)", order("対話が成り立つように、（　）内の語句を並べかえなさい。\nA: What do you want to be in the future?\nB: I want (　　) many sick people.",
                    ["to be", "a doctor", "who", "can help"],
                    "I want to be a doctor who can help many sick people. 主格の関係代名詞 who が a doctor を後ろから説明する。", d=3, k=["grammar"], p=5)),
    ("問4(イ)", order("対話が成り立つように、（　）内の語句を並べかえなさい。\nA: (　　). \nB: Wow, it's beautiful!",
                    ["This is", "a picture", "I took", "in Kyoto"],
                    "This is a picture I took in Kyoto. I took in Kyoto が a picture を後ろから修飾している（目的格の関係代名詞の省略）。", d=3, k=["grammar"], p=5)),
    ("問4(ウ)", order("対話が成り立つように、（　）内の語句を並べかえなさい。\nA: Why do you study English?\nB: Because (　　).",
                    ["it is", "important", "for us", "to learn about", "other cultures"],
                    "Because it is important for us to learn about other cultures. It is ～ for … to ― の構文。", d=4, k=["grammar"], p=5)),
], "英")
eng += tag(E, "ENG-5", [
    ("問5", desc("次の場面で、あなたが留学生のジョン（John）に伝える英文を1文で書きなさい。\n［場面］週末に一緒に映画を見に行かないかと誘う。\n［条件］疑問文で、5語以上の英語で書くこと。",
                 "Would you like to go to see a movie with me this weekend?",
                 "相手を誘う表現には Would you like to ～? / Shall we ～? / Why don't we ～? / Do you want to ～? などがある。this weekend などで時を示すとよい。",
                 [("相手を誘う表現を正しく使っている", 2), ("「週末」「映画」の内容を含み、疑問文・5語以上の条件を満たしている", 2), ("文法・つづりの誤りがない", 1)],
                 d=4, k=["writing"], p=5, lines=2)),
], "英")
eng += tag(E, "ENG-6", [
    ("問6(ア)", mc("Why did the speaker decide to join the event?",
                 ["Because the speaker's mother said it was a good idea to try it.", "Because the speaker's friends were going to join it.",
                  "Because the speaker was very interested in the sea.", "Because the speaker's teacher showed a poster about it."],
                 "母親がポスターを見せ、Why don't you try it? と勧めたことで参加を決めた。最初はあまり興味がなかった（I was not very interested at first）。", d=3, k=["reading"], p=5, st="E-SPEECH")),
    ("問6(イ)", mc("What did the speaker learn at the event?",
                 ["Much of the plastic trash in the sea comes from cities.", "Most of the trash on the beach was big pieces of wood.",
                  "Only children and students joined the event.", "Most of the plastic trash in the sea comes from ships."],
                 "スタッフが much of the plastic trash in the sea comes from cities と教えてくれた。ごみの多くは小さなプラスチック片だった。", d=3, k=["reading"], p=5, st="E-SPEECH")),
    ("問6(ウ)", mc("本文の内容に合うものを選びなさい。",
                 ["The speaker now carries a water bottle.", "About fifty students came to the event.",
                  "The speaker cleaned the beach for five hours.", "The speaker will not join the event again."],
                 "Now I always carry my own water bottle とある。参加者約50人は子どもから高齢者までさまざまで、清掃は2時間。今年も参加したいと述べている。", d=3, k=["reading"], p=5, st="E-SPEECH")),
], "英")
eng += tag(E, "ENG-7", [
    ("問7(ア)", mc("Rina is a junior high school student. She wants to join an event on a Sunday afternoon. Which event can she join?",
                 ["English Conversation Club", "Picture Book Reading", "Book Cover Workshop", "She can't join any event."],
                 "日曜日の午後に開かれ、中高生が参加できるのは English Conversation Club（第1・第3日曜日 14:00–15:30）。", d=3, k=["reading", "data_interpretation"], p=5, st="E-POSTER")),
    ("問7(イ)", mc("ポスターの内容に合うものを選びなさい。",
                 ["People who want to join the workshop must sign up by August 3.", "The Picture Book Reading is for junior high school students.",
                  "The English Conversation Club is free.", "The workshop is held every Saturday."],
                 "Workshop には August 3 までの申し込みが必要と書かれている。読み聞かせは7歳未満対象、英会話クラブは300円、ワークショップは8月10日のみ。", d=3, k=["reading", "data_interpretation"], p=5, st="E-POSTER")),
], "英")
eng += tag(E, "ENG-8", [
    ("問8(ア)", mc("According to the table, how many students chose \"Bring my own bag\"?", ["36", "12", "18", "54"],
                 "表より Bring my own bag は 36 人。", d=2, k=["reading", "data_interpretation"], p=5, st="E-DIALOGUE")),
    ("問8(イ)", mc("What does Aoi want to do?", ["Make a poster about separating trash.", "Ask stores to stop selling plastic bags.",
                                              "Use public transportation every day.", "Turn off the lights in the classroom."],
                 "Aoi は why don't we make a poster that shows how to separate trash? と提案している。", d=3, k=["reading"], p=5, st="E-DIALOGUE")),
    ("問8(ウ)", mc("対話と表の内容に合うものを選びなさい。",
                 ["Less than half of the students chose \"Turn off the lights.\"", "\"Use public transportation\" was the second most popular answer.",
                  "Haruto thinks turning off the lights is difficult.", "Eighteen students bring their own bags."],
                 "Turn off the lights は 120 人中 54 人で半数（60 人）未満。2番目に多いのは Bring my own bag。Haruto は That's easy for everyone. と言っている。", d=4, k=["reading", "data_interpretation"], p=5, st="E-DIALOGUE")),
], "英")

ENG_STIMULI = [
    stim("E-L1", "A: Hi, Mika. You look tired. What did you do last night?\nB: I studied for the math test until midnight.\nA: Oh, really? When is the test?\nB: (チャイム)", "listening_script", "問1(ア) No.1"),
    stim("E-L2", "A: Excuse me. How can I get to Yokohama Station?\nB: Take the bus at that bus stop. It leaves every ten minutes.\nA: How long does it take from here?\nB: (チャイム)", "listening_script", "問1(ア) No.2"),
    stim("E-L3", "Ken: Emma, are you free this Saturday?\nEmma: I have a piano lesson in the morning, but I'm free in the afternoon.\nKen: Great. Shall we go to the library together? I want to borrow some books about space.\nEmma: Sure. Let's meet at the station at two.\nQuestion: What will Ken and Emma do on Saturday afternoon?", "listening_script", "問1(イ) No.1"),
    stim("E-L4", "Yuta: Ms. Brown, I'm going to make a speech about my town next week. Can you check my English?\nMs. Brown: Of course. How long is your speech?\nYuta: It's about three minutes. I'll bring it to you tomorrow.\nMs. Brown: OK. I'm in the teachers' room after lunch.\nQuestion: What will Yuta do tomorrow?", "listening_script", "問1(イ) No.2"),
    stim("E-L5", "Hello, everyone. Welcome to Midori Zoo. Today, you can see the baby pandas from ten to twelve in the morning. At one thirty, you can give food to the elephants. The zoo closes at five, so please leave by then. Enjoy your day!", "listening_script", "問1(ウ)"),
    stim("E-SPEECH",
         "Hello, everyone. Today I'm going to talk about a volunteer activity I joined last summer.\n\n"
         "One day in July, my mother showed me a poster about a beach cleaning event near our town. I was not very interested at first, but she said, \"Why don't you try it? You may find something new.\" So I decided to join.\n\n"
         "On the day of the event, about fifty people came to the beach. There were children, students, and older people. We walked along the beach for two hours and picked up a lot of trash. I was surprised because most of the trash was small pieces of plastic. A staff member told us that much of the plastic trash in the sea comes from cities, not from the beach. Plastic bags and bottles are carried to the sea by rivers and wind.\n\n"
         "After the event, I started to think about my own life. I used many plastic bottles every week. Now I always carry my own water bottle, and I say \"No, thank you\" when a store clerk asks me if I need a plastic bag.\n\n"
         "Small actions by one person may not change the world. But if many people take small actions, the sea will become cleaner. I want to join the event again this year, and I hope some of you will come with me. Thank you.",
         "passage", "問6　次の英文は、中学生がクラスで行ったスピーチである。", source="オリジナル", glossary=[("trash", "ごみ"), ("clerk", "店員")]),
    stim("E-POSTER", "Midori City Library — August Events\nYou need to sign up at the front desk by August 3 for the Book Cover Workshop.", "data", "問7　次のポスターを読んで答えなさい。",
         tbl=table([["Picture Book Reading (children under 7)", "Every Saturday", "10:00–10:30", "Free"],
                    ["English Conversation Club (junior high & high school students)", "1st and 3rd Sunday", "14:00–15:30", "300 yen"],
                    ["Book Cover Workshop (anyone)", "August 10", "13:00–15:00", "500 yen"]],
                   header=["Event", "Day", "Time", "Fee"])),
    stim("E-DIALOGUE",
         "Ms. Green: We asked 120 students in our school, \"What do you do to protect the environment?\" What can you see from the results?\n"
         "Haruto: The most popular answer is \"turning off the lights.\" Fifty-four students do it. That's easy for everyone.\n"
         "Aoi: \"Bringing my own bag\" is second. I think more people started doing it after stores began to charge for plastic bags.\n"
         "Ms. Green: That's a good point. How about \"separating trash\"?\n"
         "Haruto: Only eighteen students chose it. I think many students don't know how to separate trash correctly.\n"
         "Aoi: Then, why don't we make a poster that shows how to separate trash? We can put it near the trash boxes in our classroom.\n"
         "Ms. Green: Great idea! Small changes in our school can make a big difference.",
         "dialogue", "問8　次の対話と表を読んで答えなさい。", source="オリジナル",
         tbl=table([["Turn off the lights when we leave a room", 54], ["Bring my own bag when I go shopping", 36], ["Separate trash for recycling", 18], ["Use public transportation", 12]],
                   header=["What do you do to protect the environment?", "Students"], caption="Survey (120 students)")),
]

# ============================== 数学 ==============================
C = ["calculation"]
math = []
math += tag(M, "MATH-1", [
    ("問1(ア)", mc("$-2-9$ を計算しなさい。", ["$-11$", "$-7$", "$7$", "$11$"], "$-2-9=-(2+9)=-11$。", d=1, k=C, p=3, chk=("-2-9", "-11"))),
    ("問1(イ)", mc("$-\\dfrac{3}{4}+\\dfrac{1}{6}$ を計算しなさい。", ["$-\\dfrac{7}{12}$", "$-\\dfrac{11}{12}$", "$-\\dfrac{1}{5}$", "$\\dfrac{7}{12}$"],
                 "通分して $-\\dfrac{9}{12}+\\dfrac{2}{12}=-\\dfrac{7}{12}$。", d=1, k=C, p=3, chk=("-Rational(3,4)+Rational(1,6)", "-7/12"))),
    ("問1(ウ)", mc("$18x^2y\\div(-3xy)$ を計算しなさい。", ["$-6x$", "$6x$", "$-6xy$", "$-15x$"],
                 "$\\dfrac{18x^2y}{-3xy}=-6x$。", d=1, k=C, p=3, chk=("18*x**2*y/(-3*x*y)", "-6*x"))),
    ("問1(エ)", mc("$\\sqrt{48}-\\sqrt{27}$ を計算しなさい。", ["$\\sqrt{3}$", "$\\sqrt{21}$", "$7\\sqrt{3}$", "$2\\sqrt{3}$"],
                 "$\\sqrt{48}=4\\sqrt{3}$、$\\sqrt{27}=3\\sqrt{3}$ より $4\\sqrt{3}-3\\sqrt{3}=\\sqrt{3}$。", d=2, k=C, p=3, chk=("sqrt(48)-sqrt(27)", "sqrt(3)"))),
    ("問1(オ)", mc("$(x+3)^2-(x+5)(x-5)$ を計算しなさい。", ["$6x+34$", "$6x-16$", "$2x^2+6x-16$", "$6x+9$"],
                 "$(x^2+6x+9)-(x^2-25)=6x+34$。", d=2, k=C, p=3, chk=("expand((x+3)**2-(x+5)*(x-5))", "6*x+34"))),
], "数")
math += tag(M, "MATH-2", [
    ("問2(ア)", mc("連立方程式 $\\begin{cases}2x+3y=1\\\\ x-2y=4\\end{cases}$ を解きなさい。",
                 ["$x=2,\\ y=-1$", "$x=-1,\\ y=1$", "$x=2,\\ y=1$", "$x=4,\\ y=0$"],
                 "第2式より $x=2y+4$。第1式に代入して $2(2y+4)+3y=1$、$7y=-7$、$y=-1$。$x=2$。", d=2, k=C, p=4,
                 chk=("solve([2*x+3*y-1, x-2*y-4], [x, y])", "{x: 2, y: -1}"))),
    ("問2(イ)", mc("二次方程式 $x^2-5x+3=0$ を解きなさい。",
                 ["$x=\\dfrac{5\\pm\\sqrt{13}}{2}$", "$x=\\dfrac{-5\\pm\\sqrt{13}}{2}$", "$x=\\dfrac{5\\pm\\sqrt{37}}{2}$", "$x=5\\pm\\sqrt{13}$"],
                 "解の公式より $x=\\dfrac{5\\pm\\sqrt{25-12}}{2}=\\dfrac{5\\pm\\sqrt{13}}{2}$。", d=2, k=C, p=4,
                 chk=("solve(x**2-5*x+3, x)", "[(5-sqrt(13))/2, (5+sqrt(13))/2]", "set"))),
    ("問2(ウ)", mc("関数 $y=ax^2$ について、$x$ の値が $1$ から $3$ まで増加するときの変化の割合が $8$ であった。$a$ の値を求めなさい。",
                 ["$a=2$", "$a=1$", "$a=4$", "$a=\\dfrac{8}{9}$"],
                 "変化の割合は $\\dfrac{9a-a}{3-1}=4a$。$4a=8$ より $a=2$。", d=3, k=C, p=4, chk=("solve((9*a-a)/(3-1)-8, a)", "[2]"))),
    ("問2(エ)", mc("$\\sqrt{60n}$ が自然数となるような、最も小さい自然数 $n$ を求めなさい。", ["$15$", "$60$", "$5$", "$3$"],
                 "$60=2^2\\times3\\times5$。根号の中が平方数になるには $3\\times5=15$ をかければよい。$\\sqrt{60\\times15}=\\sqrt{900}=30$。", d=3, k=C, p=4, chk=("sqrt(60*15)", "30"))),
    ("問2(オ)", mc("ある中学校の昨年度の生徒数は 500 人であった。今年度は昨年度と比べて男子が 10% 増え、女子が 5% 減ったので、全体で 5 人増えた。今年度の男子の人数を求めなさい。",
                 ["220 人", "200 人", "210 人", "330 人"],
                 "昨年度の男子を $x$ 人、女子を $y$ 人とすると $x+y=500$、$0.1x-0.05y=5$。解くと $x=200,\\ y=300$。今年度の男子は $200\\times1.1=220$（人）。",
                 d=4, k=["calculation", "thinking"], p=4, chk=("solve([x+y-500, x/10-y/20-5], [x, y])[x]*Rational(11,10)", "220"))),
    ("問2(カ)", mc("図のように、円 O の周上に 3 点 A、B、C があり、$\\angle\\mathrm{AOB}=110^\\circ$ である。点 C を含まない側の弧 AB に対する円周角 $\\angle\\mathrm{ACB}$ の大きさを求めなさい。",
                 ["$55^\\circ$", "$110^\\circ$", "$70^\\circ$", "$125^\\circ$"],
                 "同じ弧に対する円周角は中心角の半分なので $110^\\circ\\div2=55^\\circ$。", d=2, k=C, p=4, chk=("110/2", "55"),
                 fig=figure("円Oの周上に点A, B, Cがあり、中心角AOBが110度", shape(
                     {"A": (-1.64, -1.15), "B": (1.64, -1.15), "C": (0.3, 1.98), "O": (0, 0)},
                     segments=[("A", "O"), ("O", "B"), ("A", "C"), ("C", "B")], circle=((0, 0), 2), scale=26)))),
], "数")
math += tag(M, "MATH-3", [
    ("問3(ア)", mc("図のように、$\\mathrm{AB}=\\mathrm{AC}$ の二等辺三角形 ABC の辺 AB 上に点 D、辺 AC 上に点 E を $\\mathrm{BD}=\\mathrm{CE}$ となるようにとる。$\\triangle\\mathrm{DBC}\\equiv\\triangle\\mathrm{ECB}$ を証明するとき、次の［証明］の［　］に入る合同条件として正しいものを選びなさい。\n［証明］$\\triangle\\mathrm{DBC}$ と $\\triangle\\mathrm{ECB}$ において、仮定より $\\mathrm{BD}=\\mathrm{CE}$ …①　共通な辺だから $\\mathrm{BC}=\\mathrm{CB}$ …②　二等辺三角形の底角は等しいから $\\angle\\mathrm{DBC}=\\angle\\mathrm{ECB}$ …③　①、②、③より、［　］から $\\triangle\\mathrm{DBC}\\equiv\\triangle\\mathrm{ECB}$",
                 ["2組の辺とその間の角がそれぞれ等しい", "3組の辺がそれぞれ等しい", "1組の辺とその両端の角がそれぞれ等しい", "直角三角形の斜辺と他の1辺がそれぞれ等しい"],
                 "①②は2組の辺、③はその間の角（辺 BD と BC の間の角、辺 CE と CB の間の角）なので、「2組の辺とその間の角がそれぞれ等しい」。",
                 d=3, k=["proof", "thinking"], p=5,
                 fig=figure("二等辺三角形ABC（AB=AC）、辺AB上の点D、辺AC上の点E、線分DC・EB", shape(
                     {"A": (0, 4), "B": (-2.2, 0), "C": (2.2, 0), "D": (-1.32, 1.6), "E": (1.32, 1.6)},
                     segments=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "C"), ("E", "B")], scale=24)))),
    ("問3(イ)", num("次のデータは、10 人の生徒の小テストの得点である。このデータの四分位範囲を求めなさい。\n3，5，6，6，7，8，8，9，9，10（点）", "3",
                  "データを小さい順に並べると前半 5 個は 3，5，6，6，7 で第1四分位数は 6、後半 5 個は 8，8，9，9，10 で第3四分位数は 9。四分位範囲は $9-6=3$（点）。",
                  d=3, k=["calculation", "data_interpretation"], p=5, unit="点",
                  chk=("quartiles([3,5,6,6,7,8,8,9,9,10])[2]-quartiles([3,5,6,6,7,8,8,9,9,10])[0]", "3"))),
    ("問3(ウ)", num("図の $\\triangle\\mathrm{ABC}$ で、辺 AB 上の点 D と辺 AC 上の点 E について $\\mathrm{DE}\\parallel\\mathrm{BC}$、$\\mathrm{AD}:\\mathrm{DB}=2:3$、$\\mathrm{BC}=10\\,\\mathrm{cm}$ である。線分 DE の長さを求めなさい。", "4",
                  "$\\mathrm{DE}\\parallel\\mathrm{BC}$ より $\\triangle\\mathrm{ADE}\\sim\\triangle\\mathrm{ABC}$ で、相似比は $\\mathrm{AD}:\\mathrm{AB}=2:5$。$\\mathrm{DE}=10\\times\\dfrac{2}{5}=4\\,(\\mathrm{cm})$。",
                  d=3, k=C, p=5, unit="cm", chk=("10*Rational(2,5)", "4"),
                  fig=figure("三角形ABCと、BCに平行な線分DE", shape({"A": (1, 4), "B": (0, 0), "C": (5, 0), "D": (0.6, 2.4), "E": (2.6, 2.4)},
                                                              segments=[("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")], scale=24)))),
    ("問3(エ)", num("$\\mathrm{AB}=\\mathrm{AC}=10\\,\\mathrm{cm}$、$\\mathrm{BC}=12\\,\\mathrm{cm}$ の二等辺三角形 ABC の面積を求めなさい。", "48",
                  "A から BC に垂線 AH をひくと H は BC の中点で $\\mathrm{BH}=6$。三平方の定理より $\\mathrm{AH}=\\sqrt{10^2-6^2}=8$。面積は $\\dfrac{1}{2}\\times12\\times8=48\\,(\\mathrm{cm}^2)$。",
                  d=3, k=C, p=5, unit="cm²", chk=("Rational(1,2)*12*sqrt(10**2-6**2)", "48"))),
], "数")
math += tag(M, "MATH-4", [
    ("問4(ア)", num("図において、曲線①は関数 $y=ax^2$ のグラフである。点 A は曲線①上の点で、座標は $(-2,\\,2)$ である。$a$ の値を求めなさい。", "1/2",
                  "$y=ax^2$ に $x=-2,\\ y=2$ を代入して $2=4a$、$a=\\dfrac{1}{2}$。", d=2, k=C, p=5, disp="$a=\\dfrac{1}{2}$",
                  chk=("solve(a*(-2)**2-2, a)", "[1/2]"),
                  fig=figure("放物線y=1/2x^2上の点A(-2,2)とB(4,8)、直線AB", plane((-4, 6), (-1, 9), unit=14, curves=[(lambda x: x * x / 2, "①")], lines=[(1, 4, "")],
                                                                      points=[(-2, 2, "A"), (4, 8, "B")], segments=[((0, 0), (-2, 2)), ((0, 0), (4, 8))])))),
    ("問4(イ)", sa("曲線①上に $x$ 座標が $4$ である点 B をとる。2点 A、B を通る直線の式を求めなさい。", "$y=x+4$",
                 "B の $y$ 座標は $\\dfrac{1}{2}\\times4^2=8$。直線 AB の傾きは $\\dfrac{8-2}{4-(-2)}=1$。$y=x+b$ に $(4,\\,8)$ を代入して $b=4$。", d=3, k=C, p=5, v=["y=x+4"],
                 chk=("solve([m*(-2)+b-2, m*4+b-8], [m, b])", "{m: 1, b: 4}"))),
    ("問4(ウ)", num("原点を O とするとき、$\\triangle\\mathrm{OAB}$ の面積を求めなさい。ただし、座標の1目もりを $1\\,\\mathrm{cm}$ とする。", "12",
                  "直線 AB と $y$ 軸との交点を C とすると C$(0,\\,4)$。$\\triangle\\mathrm{OAB}=\\triangle\\mathrm{OAC}+\\triangle\\mathrm{OBC}=\\dfrac{1}{2}\\times4\\times2+\\dfrac{1}{2}\\times4\\times4=12\\,(\\mathrm{cm}^2)$。",
                  d=4, k=["calculation", "thinking"], p=6, unit="cm²", chk=("Rational(1,2)*4*(2+4)", "12"))),
], "数")
math += tag(M, "MATH-5", [
    ("問5(ア)", num("大小2つのさいころを同時に1回投げる。出た目の数の和が 5 の倍数になる確率を求めなさい。ただし、どの目が出ることも同様に確からしいものとする。", "7/36",
                  "目の出方は全部で 36 通り。和が 5 になるのは (1,4)(2,3)(3,2)(4,1) の 4 通り、和が 10 になるのは (4,6)(5,5)(6,4) の 3 通り。確率は $\\dfrac{7}{36}$。",
                  d=3, k=C, p=5, disp="$\\dfrac{7}{36}$", chk=("Rational(4+3, 36)", "7/36"))),
    ("問5(イ)", num("大きいさいころの出た目の数を $a$、小さいさいころの出た目の数を $b$ とするとき、$\\dfrac{a}{b}$ が整数になる確率を求めなさい。", "7/18",
                  "$b$ が $a$ の約数になる場合を数える。$b=1$：6 通り、$b=2$：$a=2,4,6$ の 3 通り、$b=3$：$a=3,6$ の 2 通り、$b=4,5,6$：各 1 通り。合計 14 通りで、確率は $\\dfrac{14}{36}=\\dfrac{7}{18}$。",
                  d=4, k=["calculation", "thinking"], p=5, disp="$\\dfrac{7}{18}$", chk=("summation(floor(6/b), (b, 1, 6))/36", "7/18"))),
], "数")
math += tag(M, "MATH-6", [
    ("問6(ア)", num("底面の半径が $3\\,\\mathrm{cm}$、母線の長さが $5\\,\\mathrm{cm}$ の円錐がある。この円錐の高さを求めなさい。", "4",
                  "高さ $h$ は、半径・高さ・母線でできる直角三角形に三平方の定理を使って $h=\\sqrt{5^2-3^2}=4\\,(\\mathrm{cm})$。", d=2, k=C, p=5, unit="cm",
                  chk=("sqrt(5**2-3**2)", "4"),
                  fig=figure("底面の半径3cm、母線5cmの円錐", shape({"P": (0, 4), "L": (-3, 0), "R": (3, 0), "H": (0, 0)},
                                                                segments=[("P", "L"), ("P", "R")], dashed=[("P", "H"), ("L", "R")], labels={"P": "", "L": "", "R": "", "H": ""},
                                                                texts=[(1.7, 2.3, "5cm"), (0.9, -0.5, "3cm")], scale=22)))),
    ("問6(イ)", sa("この円錐の体積を求めなさい。ただし、円周率は $\\pi$ とする。", "$12\\pi\\,\\mathrm{cm}^3$",
                 "$\\dfrac{1}{3}\\times\\pi\\times3^2\\times4=12\\pi\\,(\\mathrm{cm}^3)$。", d=3, k=C, p=5, v=["12π", "12πcm³"],
                 chk=("Rational(1,3)*pi*3**2*4", "12*pi"))),
    ("問6(ウ)", sa("この円錐の表面積を求めなさい。ただし、円周率は $\\pi$ とする。", "$24\\pi\\,\\mathrm{cm}^2$",
                 "側面のおうぎ形の面積は $\\pi\\times5\\times3=15\\pi$（半径×母線×$\\pi$）。底面は $9\\pi$。表面積は $15\\pi+9\\pi=24\\pi\\,(\\mathrm{cm}^2)$。",
                 d=4, k=["calculation", "thinking"], p=5, v=["24π", "24πcm²"], chk=("pi*5*3+pi*3**2", "24*pi"))),
], "数")

# ============================== 国語 ==============================
jpn = []
jpn += tag(J, "JPN-1", [
    ("問一(ア)①", sa("次の――線部の漢字の読みを、ひらがなで書きなさい。\n[[u:穏]]やかな春の日差し。", "おだ", "「穏やか」は「おだやか」と読む。", d=1, k=["vocabulary"], p=2, v=["おだやか"])),
    ("問一(ア)②", sa("次の――線部の漢字の読みを、ひらがなで書きなさい。\n申し出を[[u:拒]]む。", "こば", "「拒む」は「こばむ」と読む。", d=2, k=["vocabulary"], p=2, v=["こばむ"])),
    ("問一(ア)③", sa("次の――線部の漢字の読みを、ひらがなで書きなさい。\n[[u:抑揚]]をつけて朗読する。", "よくよう", "「抑揚」は話すときの声の上げ下げのこと。", d=2, k=["vocabulary"], p=2)),
    ("問一(ア)④", sa("次の――線部の漢字の読みを、ひらがなで書きなさい。\n花の香りが[[u:漂]]う。", "ただよ", "「漂う」は「ただよう」と読む。", d=1, k=["vocabulary"], p=2, v=["ただよう"])),
    ("問一(イ)①", sa("次の――線部のカタカナを漢字に直して書きなさい。\n荷物を駅に[[u:アズ]]ける。", "預", "「預ける」。「頼」「与」との混同に注意。", d=1, k=["vocabulary"], p=2, v=["預ける"])),
    ("問一(イ)②", sa("次の――線部のカタカナを漢字に直して書きなさい。\n[[u:ユウビン]]局で切手を買う。", "郵便", "「郵便」。「便」は「びん」とも「べん」とも読む。", d=1, k=["vocabulary"], p=2)),
    ("問一(イ)③", sa("次の――線部のカタカナを漢字に直して書きなさい。\n事業の[[u:キボ]]を拡大する。", "規模", "「規模」は物事の仕組みや構えの大きさのこと。", d=2, k=["vocabulary"], p=2)),
    ("問一(イ)④", sa("次の――線部のカタカナを漢字に直して書きなさい。\n夕方から雨が[[u:フ]]り出した。", "降", "「降る」。同訓の「振る」と区別する。", d=1, k=["vocabulary"], p=2, v=["降り"])),
    ("問一(ウ)", mc("「腹を割る」の意味として最も適切なものを選びなさい。", ["本心を隠さずに打ち明ける", "ひどく腹を立てる", "我慢できずに笑い出す", "覚悟を決めて取り組む"],
                  "「腹を割って話す」のように、隠しごとをせず本心を打ち明けることをいう。", d=2, k=["vocabulary"], p=2)),
    ("問一(エ)", mc("「登山」と同じ構成の熟語を選びなさい。", ["読書", "岩石", "前後", "国営"],
                  "「登山」は「山に登る」で、下の字が上の字の目的や対象を表す構成。「読書（書を読む）」が同じ。「岩石」は似た意味、「前後」は対になる意味、「国営」は主語・述語の関係。",
                  d=2, k=["vocabulary"], p=2)),
], "国")
jpn += tag(J, "JPN-2", [
    ("問二(ア)", mc("――線①「心憂く覚えて」の意味として最も適切なものを選びなさい。", ["残念に思って", "うれしく思って", "不思議に思って", "恐ろしく思って"],
                  "「心憂し」はつらい・情けないの意。年をとるまで石清水八幡宮に参拝しなかったことを残念に思ったのである。", d=3, k=["classics"], p=4, st="J-KOBUN")),
    ("問二(イ)", mc("――線②「かばかりと心得て帰りにけり」とあるが、法師はどのように思いこんで帰ったのか。最も適切なものを選びなさい。",
                  ["ふもとの極楽寺や高良が石清水八幡宮のすべてだと思いこんだ", "山の上まで登って八幡宮に参拝したと思いこんだ", "参拝する前に日が暮れてしまったと思いこんだ", "連れの者がいなければ参拝できないと思いこんだ"],
                  "法師は山のふもとの極楽寺・高良を拝んで「これだけだ」と思いこみ、山上にある本殿に参らずに帰ってしまった。", d=3, k=["classics", "reading"], p=4, st="J-KOBUN")),
    ("問二(ウ)", mc("――線③「ゆかしかりしかど」の意味として最も適切なものを選びなさい。", ["知りたかったけれど", "行きたくなかったので", "なつかしかったけれど", "おそろしかったので"],
                  "「ゆかし」は「見たい・知りたい・聞きたい」の意。人々が山へ登るのは何があるのかと知りたかったが、という意味。", d=3, k=["classics"], p=4, st="J-KOBUN")),
    ("問二(エ)", mc("この文章で筆者が最も言いたいことはどのようなことか。最も適切なものを選びなさい。",
                  ["ちょっとしたことでも、その道の案内者・指導者はいてほしいものだ", "神仏への参拝は、一人で行うのが最もよい", "年をとってから新しいことを始めるべきではない", "人のうわさは信じないほうがよい"],
                  "最後の一文「少しのことにも、先達はあらまほしき事なり」が筆者の感想・主張。「先達」は案内者・指導者、「あらまほし」はあってほしいの意。", d=3, k=["classics", "reading"], p=4, st="J-KOBUN")),
], "国")
jpn += tag(J, "JPN-3", [
    ("問三(ア)", mc("――線①「マウスピースを付けたまま、しばらく手の中で転がしていた」から読み取れる真帆の様子として最も適切なものを選びなさい。",
                  ["オーディションの結果が心にひっかかり、練習に気持ちが向かない様子", "楽器の手入れに夢中になり、時間を忘れている様子", "楓に会うのが楽しみで、落ち着かない様子", "練習の段取りを考えながら、やる気に満ちている様子"],
                  "直後に昨日のオーディションで後輩が選ばれたことが語られており、楽器を構えずに手の中で転がす動作から、結果を受け止めきれず練習に向かえない心情が読み取れる。",
                  d=3, k=["reading"], p=5, st="J-NOVEL")),
    ("問三(イ)", mc("――線②「胸の奥で固くなっていたものが、少しだけゆるむのを感じた」とあるが、それはなぜか。最も適切なものを選びなさい。",
                  ["自分の演奏が、楓がトランペットを始めるきっかけになっていたと知ったから", "楓がソロを辞退すると言い出したから", "楓の演奏に欠点があることに気づいたから", "顧問の先生がもう一度オーディションをすると言ったから"],
                  "楓が「先輩の音を聴いてトランペットを始めた」と打ち明けたことで、毎朝の練習の音が誰かに届いていたと知り、わだかまりが少しほどけた。", d=3, k=["reading"], p=5, st="J-NOVEL")),
    ("問三(ウ)", mc("――線③「今度は、声がちゃんと出た」の「今度は」という表現からわかることとして最も適切なものを選びなさい。",
                  ["前日は楓を祝う言葉が言えなかったが、今は素直に楓の演奏をたたえられたこと", "前日は風邪で声が出なかったが、今は体調が回復したこと", "前日は大きな声で話せたが、今は小さな声しか出ないこと", "前日は楓に注意したが、今はほめることにしたこと"],
                  "結果を聞いたとき「おめでとう」と言おうとしても声がうまく出なかったことと対比されている。", d=3, k=["reading"], p=5, st="J-NOVEL")),
    ("問三(エ)", desc("――線④「二つの音が、夕方の音楽室に重なっていった」とあるが、この表現は二人の関係がどのように変わったことを表しているか。四十字以内で書きなさい。",
                    "ソロを争う相手だった二人が、互いを認め合い、ともに音楽に向き合う関係になったこと。",
                    "冒頭ではオーディションの結果によって気まずい関係だった二人が、思いを打ち明け、助言し合うことで、一緒に演奏する仲間になったことを、音が「重なる」という表現で象徴的に描いている。",
                    [("競い合う（気まずい）関係だったことにふれている", 3), ("互いを認め合い、ともに演奏する（協力する）関係になったことを書いている", 4)],
                    d=4, k=["reading", "writing"], p=7, grid=40, st="J-NOVEL")),
], "国")
jpn += tag(J, "JPN-4", [
    ("問四(ア)", mc("――線①「隔たり」の意味として最も適切なものを選びなさい。", ["二つのものの間にある差", "二つのものが重なり合う部分", "物事が始まるきっかけ", "物事の順序や段取り"],
                  "「隔たり」は「へだたり」と読み、距離や差・違いを表す。", d=2, k=["vocabulary", "reading"], p=6, st="J-ESSAY")),
    ("問四(イ)", mc("筆者が自転車の乗り方の例を挙げたのはなぜか。最も適切なものを選びなさい。",
                  ["「知っている」ことと「分かっている」ことの違いを、身近な例で具体的に示すため", "自転車に乗る練習には本を読むことが欠かせないと主張するため", "体を動かすことの楽しさを読者に伝えるため", "検索によって情報を得ることの便利さを説明するため"],
                  "説明を読んだだけの状態（知っている）と、実際に乗れるようになった状態（分かった）を対比させて、主張を具体的に示している。", d=3, k=["reading"], p=6, st="J-ESSAY")),
    ("問四(ウ)", mc("――線②「そのことが『分かる』までの過程を省略させてしまう危険もある」とあるが、どのような危険か。最も適切なものを選びなさい。",
                  ["答えを手に入れただけで理解したと思いこみ、自分で考える過程を経なくなる危険", "検索で得た情報がまちがっていて、誤った知識を覚えてしまう危険", "画面を長時間見続けることで、体に悪い影響が出る危険", "多くの情報を一度に手に入れて、覚えきれなくなる危険"],
                  "直後に「答えを手に入れた瞬間に、私たちはそれを理解したような気持ちになる」「自分の中で考えが組み立てられたわけではない」と説明されている。", d=3, k=["reading"], p=6, st="J-ESSAY")),
    ("問四(エ)", mc("本文の内容に合うものとして最も適切なものを選びなさい。",
                  ["他人の知識を借りることは必要だが、それを自分の経験や問いと結びつけ直すことが大切である", "検索で得た情報は信頼できないので、使うべきではない", "すべての知識は、自分で一から確かめなければ身につかない", "つまずくことは理解のさまたげになるので、できるだけ避けるべきである"],
                  "最終段落で、他人の知識を借りることは「欠かせない営み」としたうえで、「借りた知識を、自分の経験や問いと結びつけ直そうとする姿勢」が大切だと述べている。", d=3, k=["reading"], p=6, st="J-ESSAY")),
    ("問四(オ)", desc("筆者は、「知っている」ことが「分かっている」ことへと変わるためには、どのような過程が必要だと考えているか。本文中の言葉を用いて五十字以内で書きなさい。",
                    "自分で問いを立てて試し、つまずいたときにそれまでの理解を組み直すことを繰り返す過程。",
                    "第四段落の「自分で問いを立て、試し、つまずく時間が必要」「この組み直しの繰り返しこそが、知識を自分のものにしていく過程」をまとめる。",
                    [("自分で問いを立てて試す（つまずく）ことにふれている", 3), ("理解を組み直すことを繰り返すことにふれている", 3)],
                    d=4, k=["reading", "writing"], p=6, grid=50, st="J-ESSAY")),
], "国")
jpn += tag(J, "JPN-5", [
    ("問五(ア)", mc("資料から読み取れることとして最も適切なものを選びなさい。",
                  ["学年が上がるにつれて、1か月に1冊も本を読まない生徒の割合が高くなっている", "どの学年でも、1か月に4冊以上読む生徒が最も多い", "3年生は1年生よりも、1か月に4冊以上読む生徒の割合が高い", "1か月に1冊も本を読まない生徒の割合は、どの学年も同じである"],
                  "0冊の割合は1年 15%、2年 22%、3年 30% と学年が上がるほど高くなっている。4冊以上は1年 35%、2年 28%、3年 20% と減っている。", d=3, k=["data_interpretation"], p=6, st="J-DATA")),
    ("問五(イ)", desc("図書委員会では、資料をもとに全校の読書活動を活発にする取り組みを提案することになった。あなたならどのような取り組みを提案するか。資料から読み取れることにふれて、六十字以内で書きなさい。",
                    "学年が上がるほど本を読まない生徒が増えているので、三年生向けに短時間で読める本を紹介する掲示を作る。",
                    "「資料から読み取れること（根拠）」と「具体的な取り組み（提案）」を結びつけて書く。",
                    [("資料から読み取れることを根拠として示している", 3), ("根拠に合った具体的な取り組みを提案している", 3)],
                    d=4, k=["writing", "data_interpretation"], p=6, grid=60, st="J-DATA")),
], "国")

KOBUN = ("仁和寺にある法師、年寄るまで石清水を拝まざりければ、[[mark:①:心憂く覚えて]]、ある時思ひ立ちて、ただひとり、徒歩よりまうでけり。"
         "極楽寺・高良などを拝みて、[[mark:②:かばかりと心得て帰りにけり]]。\n"
         "さて、かたへの人にあひて、「年ごろ思ひつること、果たし侍りぬ。聞きしにも過ぎて尊くこそおはしけれ。そも、参りたる人ごとに山へ登りしは、何事かありけん、[[mark:③:ゆかしかりしかど]]、神へ参るこそ本意なれと思ひて、山までは見ず。」とぞ言ひける。\n"
         "少しのことにも、先達はあらまほしき事なり。")
NOVEL = ("放課後の音楽室には、まだ誰も来ていなかった。真帆はケースからトランペットを取り出したが、[[mark:①:マウスピースを付けたまま、しばらく手の中で転がしていた]]。\n\n"
         "昨日、夏のコンクールのソロを決めるオーディションがあった。選ばれたのは一年生の楓だった。真帆は二年間、毎朝誰よりも早く来て練習してきた。結果を聞いたとき、「おめでとう」と言おうとしたのに、声がうまく出なかった。\n\n"
         "「先輩、早いですね。」\n\n"
         "振り返ると、楓が入り口に立っていた。真帆は思わず楽器をケースの上に置いた。\n\n"
         "「あの、昨日のソロのことなんですけど……。」楓は言いかけて、目を伏せた。「わたし、先輩の音を聴いてトランペットを始めたんです。入学式の日の演奏で。だから、先輩と比べられるのが、ちょっとこわくて。」\n\n"
         "真帆は、[[mark:②:胸の奥で固くなっていたものが、少しだけゆるむのを感じた]]。自分が毎朝吹いていた音を、誰かが聴いていた。そのことを、真帆は考えたことがなかった。\n\n"
         "「楓のソロ、きれいだったよ。」\n\n"
         "[[mark:③:今度は、声がちゃんと出た]]。楓が顔を上げる。\n\n"
         "「でも、最後の高い音、少し急いでた。あそこは、ためてから出したほうがいい。」\n\n"
         "真帆はトランペットを構え、そのフレーズを吹いてみせた。窓から入る風が、楽譜の端をめくった。\n\n"
         "楓はしばらく黙って聴いていたが、やがて自分の楽器を取り出し、真帆の隣に立った。[[mark:④:二つの音が、夕方の音楽室に重なっていった]]。")
ESSAY = ("私たちは、何かを「知っている」ことと「分かっている」ことを、ふだんあまり区別せずに使っている。しかし、この二つの間には大きな[[mark:①:隔たり]]がある。\n\n"
         "たとえば、自転車の乗り方を考えてみよう。ペダルをこぐ力、ハンドルの角度、体重の移動について、言葉で詳しく説明された本を読んだとしても、それだけで自転車に乗れるようになる人はいない。乗れるようになるのは、何度も転びながら、体のどこにどう力を入れればよいかを自分でつかんだときである。説明を読んで得られるのは「知っている」状態であり、実際に乗れるようになったときに初めて「分かった」と言えるのだ。\n\n"
         "現代の私たちは、検索すればたいていの情報をすぐに手に入れることができる。知りたいことの答えが数秒で画面に表示される便利さは、確かに大きな恩恵である。だが、[[mark:②:そのことが「分かる」までの過程を省略させてしまう危険もある]]。答えを手に入れた瞬間に、私たちはそれを理解したような気持ちになる。しかし、それは他人がたどり着いた結論を受け取っただけで、自分の中で考えが組み立てられたわけではない。\n\n"
         "「分かる」ためには、自分で問いを立て、試し、つまずく時間が必要である。つまずいたとき、人はなぜうまくいかないのかを考え、それまでの理解を組み直す。この組み直しの繰り返しこそが、知識を自分のものにしていく過程なのである。\n\n"
         "もちろん、すべてを自分で一から確かめることはできない。他人の知識を借りることは、人間が文化を受け継いでいくうえで欠かせない営みである。大切なのは、借りた知識を、自分の経験や問いと結びつけ直そうとする姿勢だろう。手に入れた答えを出発点として、もう一度自分の頭と体で確かめてみる。そうしたとき、「知っている」ことは、少しずつ「分かっている」ことへと変わっていくのである。")

JPN_STIMULI = [
    stim("J-KOBUN", KOBUN, "classical_text", "問二　次の古文を読んで、あとの問いに答えなさい。", source="兼好法師『徒然草』第五十二段", cp="public_domain",
         glossary=[("仁和寺", "京都にある寺"), ("石清水", "石清水八幡宮。男山の山上にある"), ("極楽寺・高良", "男山のふもとにある寺社"), ("かたへの人", "仲間の人"), ("先達", "案内者・指導者")]),
    stim("J-NOVEL", NOVEL, "passage", "問三　次の文章を読んで、あとの問いに答えなさい。", source="オリジナル"),
    stim("J-ESSAY", ESSAY, "passage", "問四　次の文章を読んで、あとの問いに答えなさい。", source="オリジナル"),
    stim("J-DATA", "図書委員会が全校生徒を対象に行ったアンケートの結果（各学年の生徒数に対する割合）", "data", "問五　次の資料を見て、あとの問いに答えなさい。",
         tbl=table([["1年", "15%", "50%", "35%"], ["2年", "22%", "50%", "28%"], ["3年", "30%", "50%", "20%"]],
                   header=["学年", "0冊", "1〜3冊", "4冊以上"], caption="1か月に読む本の冊数")),
]

# ============================== 理科 ==============================
K = ["knowledge"]
sci = []
sci += tag(R, "SCI-1", [
    ("問1(ア)", mc("焦点距離 $10\\,\\mathrm{cm}$ の凸レンズの前方 $20\\,\\mathrm{cm}$ の位置に物体を置いた。スクリーンにうつる像について正しいものを選びなさい。",
                 ["レンズの後方 20 cm の位置に、物体と同じ大きさの上下左右が逆向きの実像ができる", "レンズの後方 10 cm の位置に、物体より小さい正立の実像ができる",
                  "レンズの後方 40 cm の位置に、物体より大きい倒立の実像ができる", "スクリーンには像はうつらず、レンズを通して虚像が見える"],
                 "物体を焦点距離の2倍の位置に置くと、反対側の焦点距離の2倍の位置に、物体と同じ大きさの倒立の実像ができる。", d=2, k=K, p=3)),
    ("問1(イ)", mc("モノコードの弦をはじいて出る音を高くする方法として正しいものを選びなさい。", ["弦を強く張る", "弦を太いものにかえる", "弦の振動する部分を長くする", "弦を強くはじく"],
                 "弦を強く張る・細くする・振動する部分を短くすると振動数が増え、音は高くなる。強くはじくと振幅が大きくなり、音が大きくなる。", d=2, k=K, p=3)),
    ("問1(ウ)", num("質量 $600\\,\\mathrm{g}$ の直方体の物体を、面積 $20\\,\\mathrm{cm}^2$ の面を下にして水平な床に置いた。床が物体から受ける圧力は何 Pa か。ただし、$100\\,\\mathrm{g}$ の物体にはたらく重力の大きさを $1\\,\\mathrm{N}$ とする。", "3000",
                  "物体にはたらく重力は $6\\,\\mathrm{N}$、面積は $20\\,\\mathrm{cm}^2=0.002\\,\\mathrm{m}^2$。圧力は $6\\div0.002=3000\\,(\\mathrm{Pa})$。", d=3, k=["calculation"], p=3, unit="Pa",
                  chk=("6/(20/10000)", "3000"))),
], "理")
sci += tag(R, "SCI-2", [
    ("問2(ア)", mc("酸化銀を加熱したときに起こる変化として正しいものを選びなさい。", ["銀と酸素に分解する", "銀と二酸化炭素に分解する", "酸化銀がさらに酸化される", "銀と水素に分解する"],
                 "$2\\mathrm{Ag_2O}\\rightarrow4\\mathrm{Ag}+\\mathrm{O_2}$。加熱後に残る白い固体は銀で、発生する気体は酸素である。", d=1, k=K, p=3)),
    ("問2(イ)", num("水 $80\\,\\mathrm{g}$ に食塩 $20\\,\\mathrm{g}$ をとかした食塩水の質量パーセント濃度は何 % か。", "20",
                  "質量パーセント濃度＝溶質の質量÷溶液の質量×100。$20\\div(80+20)\\times100=20\\,(\\%)$。", d=2, k=["calculation"], p=3, unit="%",
                  chk=("20/(80+20)*100", "20"))),
    ("問2(ウ)", mc("うすい塩酸に亜鉛を入れたときに発生する気体の性質として正しいものを選びなさい。", ["火のついたマッチを近づけると、音を立てて燃える", "石灰水を白くにごらせる", "線香の火を近づけると、炎を上げて燃える", "水によくとけ、水溶液はアルカリ性を示す"],
                 "発生する気体は水素。水素は燃えると水ができる。石灰水を白くにごらせるのは二酸化炭素、ものを燃やすはたらきがあるのは酸素、水によくとけアルカリ性を示すのはアンモニア。", d=2, k=K, p=3)),
], "理")
sci += tag(R, "SCI-3", [
    ("問3(ア)", mc("双子葉類の特徴として正しいものを選びなさい。", ["葉脈は網目状で、根は主根と側根からなる", "葉脈は平行で、根はひげ根である", "子葉が1枚で、葉脈は網目状である", "子葉が2枚で、根はひげ根である"],
                 "双子葉類は子葉が2枚、葉脈は網状脈、根は主根と側根。単子葉類は子葉が1枚、葉脈は平行脈、根はひげ根。", d=1, k=K, p=3)),
    ("問3(イ)", mc("だ液に含まれる消化酵素アミラーゼのはたらきとして正しいものを選びなさい。", ["デンプンを分解する", "タンパク質を分解する", "脂肪を分解する", "ブドウ糖を合成する"],
                 "アミラーゼはデンプンを麦芽糖などに分解する。タンパク質はペプシン・トリプシンなど、脂肪はリパーゼが分解する。", d=1, k=K, p=3)),
    ("問3(ウ)", mc("エンドウの種子の形で、丸形が優性（顕性）の形質、しわ形が劣性（潜性）の形質である。遺伝子の組み合わせが Aa の丸形どうしをかけ合わせてできる子の、丸形としわ形の数の比として最も適切なものを選びなさい。",
                 ["丸形：しわ形＝3：1", "丸形：しわ形＝1：1", "丸形：しわ形＝1：3", "すべて丸形"],
                 "子の遺伝子の組み合わせは AA：Aa：aa＝1：2：1。AA と Aa は丸形なので、丸形：しわ形＝3：1。", d=3, k=["knowledge", "thinking"], p=3)),
], "理")
sci += tag(R, "SCI-4", [
    ("問4(ア)", mc("地震の「マグニチュード」について正しいものを選びなさい。", ["地震そのものの規模（エネルギーの大きさ）を表す", "ある地点でのゆれの大きさを表す", "震源からの距離を表す", "地震が起きた深さを表す"],
                 "マグニチュードは地震の規模を表し、1つの地震に1つの値。各地点のゆれの大きさは震度で表す。", d=1, k=K, p=3)),
    ("問4(イ)", mc("寒冷前線が通過した後の天気の変化として最も適切なものを選びなさい。", ["気温が下がり、風向きが北寄りに変わる", "気温が上がり、風向きが南寄りに変わる", "長い時間おだやかな雨が降り続く", "気温も風向きも変化しない"],
                 "寒冷前線が通過すると、強い雨が短時間降った後、寒気におおわれて気温が下がり、風向きは北寄りに変わる。", d=2, k=K, p=3)),
    ("問4(ウ)", mc("明け方、東の空に見える金星について正しいものを選びなさい。", ["「明けの明星」とよばれ、真夜中には見ることができない", "「よいの明星」とよばれ、一晩中見ることができる", "地球の外側を公転しているので、真夜中にも見える", "満ち欠けをせず、いつも同じ形に見える"],
                 "金星は地球より内側を公転するため、明け方の東の空（明けの明星）か夕方の西の空（よいの明星）にしか見えず、真夜中には見えない。また満ち欠けをする。", d=2, k=K, p=3)),
], "理")
sci += tag(R, "SCI-5", [
    ("問5(ア)", num("表は、斜面を下る台車の運動を 1 秒間に 60 回打点する記録タイマーで記録し、6 打点ごとに区切ったテープの長さである。区間 C における台車の平均の速さは何 cm/s か。", "60",
                  "6 打点にかかる時間は $6\\div60=0.1$ 秒。区間 C は 0.1 秒で 6.0 cm 進んでいるので、$6.0\\div0.1=60\\,(\\mathrm{cm/s})$。", d=2, k=["calculation", "experiment"], p=4, unit="cm/s",
                  chk=("6/(Rational(6,60))", "60"),
                  tbl=table([["区間", "A", "B", "C", "D"], ["テープの長さ（cm）", "2.0", "4.0", "6.0", "8.0"]]))),
    ("問5(イ)", mc("この実験で、斜面の傾きを大きくすると、台車の速さの増え方はどうなるか。", ["大きくなる", "小さくなる", "変わらない", "速さが一定になる"],
                 "斜面の傾きを大きくすると、台車にはたらく重力の斜面に沿った分力が大きくなるので、速さの増え方が大きくなる。", d=2, k=["knowledge", "experiment"], p=4)),
    ("問5(ウ)", mc("斜面を下った台車が、摩擦や空気の抵抗がない水平面上を進むときの運動を何というか。", ["等速直線運動", "自由落下運動", "振り子運動", "円運動"],
                 "水平面上では運動の向きに力がはたらかないので、台車は慣性によって一定の速さで一直線に進む（等速直線運動）。", d=2, k=K, p=4)),
    ("問5(エ)", mc("台車が斜面を下るときのエネルギーの変化について正しいものを選びなさい。ただし、摩擦や空気の抵抗は考えないものとする。",
                 ["位置エネルギーが減少し、その分だけ運動エネルギーが増加する", "位置エネルギーも運動エネルギーも増加する", "運動エネルギーが減少し、その分だけ位置エネルギーが増加する", "位置エネルギーと運動エネルギーの和は減少する"],
                 "摩擦がなければ力学的エネルギー（位置エネルギー＋運動エネルギー）は一定に保たれる。下るにつれて位置エネルギーが運動エネルギーに移り変わる。", d=3, k=["knowledge", "thinking"], p=4)),
], "理")
sci += tag(R, "SCI-6", [
    ("問6(ア)", mc("うすい塩酸 $10\\,\\mathrm{cm}^3$ に BTB 溶液を加え、うすい水酸化ナトリウム水溶液を少しずつ加えたところ、$8\\,\\mathrm{cm}^3$ 加えたときに水溶液が緑色になった。このときの水溶液の性質として正しいものを選びなさい。",
                 ["中性", "酸性", "アルカリ性", "酸性とアルカリ性の両方"],
                 "BTB 溶液は酸性で黄色、中性で緑色、アルカリ性で青色を示す。緑色なので中性。", d=1, k=["knowledge", "experiment"], p=4)),
    ("問6(イ)", mc("この中和で、水のほかにできる塩の化学式を選びなさい。", ["$\\mathrm{NaCl}$", "$\\mathrm{NaOH}$", "$\\mathrm{HCl}$", "$\\mathrm{H_2O}$"],
                 "$\\mathrm{HCl}+\\mathrm{NaOH}\\rightarrow\\mathrm{NaCl}+\\mathrm{H_2O}$。塩は塩化ナトリウム。", d=2, k=K, p=4)),
    ("問6(ウ)", mc("水酸化ナトリウム水溶液を加え始めてから緑色になるまでの間、水溶液中の水素イオンの数はどのように変化するか。",
                 ["しだいに減少し、緑色になったときに 0 になる", "しだいに増加する", "変化しない", "しだいに減少し、緑色になった後に増加する"],
                 "加えた水酸化物イオンが水素イオンと結びついて水になるので、水素イオンは減少し、中性になったときに 0 になる。その後も水素イオンは 0 のまま。", d=3, k=["knowledge", "thinking"], p=4)),
    ("問6(エ)", num("同じ濃度の塩酸 $15\\,\\mathrm{cm}^3$ を、同じ濃度の水酸化ナトリウム水溶液で完全に中和するには、水酸化ナトリウム水溶液が何 $\\mathrm{cm}^3$ 必要か。", "12",
                  "塩酸 $10\\,\\mathrm{cm}^3$ に対して $8\\,\\mathrm{cm}^3$ で中和するので、$15\\,\\mathrm{cm}^3$ には $8\\times\\dfrac{15}{10}=12\\,(\\mathrm{cm}^3)$ 必要。", d=3, k=["calculation", "thinking"], p=4, unit="cm³",
                  chk=("8*Rational(15,10)", "12"))),
], "理")
sci += tag(R, "SCI-7", [
    ("問7(ア)", mc("試験管 A がうすい青色に変化したのはなぜか。最も適切なものを選びなさい。", ["オオカナダモが光合成を行い、水中の二酸化炭素が減ったから", "オオカナダモが呼吸を行い、水中の二酸化炭素が増えたから", "光が当たって BTB 溶液が分解されたから", "オオカナダモが酸素を吸収したから"],
                 "光が当たると、オオカナダモは呼吸より光合成をさかんに行い、水中の二酸化炭素を吸収する。二酸化炭素が減ると水溶液は中性から弱アルカリ性になり、BTB 溶液は青色になる。", d=3, k=["experiment", "thinking"], p=4, st="R-EXP")),
    ("問7(イ)", mc("試験管 C を用意したのは何を確かめるためか。最も適切なものを選びなさい。", ["BTB 溶液の色の変化がオオカナダモのはたらきによるものであること", "光の強さによって色の変化が異なること", "オオカナダモが呼吸をしていること", "水温によって色の変化が異なること"],
                 "C はオオカナダモを入れない以外は A と同じ条件にした対照実験。C の色が変わらないことから、A の色の変化がオオカナダモによるものだと確かめられる。", d=3, k=["experiment", "thinking"], p=4, st="R-EXP")),
    ("問7(ウ)", mc("試験管 B が黄色に変化したのはなぜか。最も適切なものを選びなさい。", ["光が当たらず光合成は行われないが、呼吸によって二酸化炭素が出されたから", "光合成によって二酸化炭素が吸収されたから", "暗い所では BTB 溶液が黄色に変化するから", "オオカナダモが酸素を多く出したから"],
                 "暗い所では光合成が行われず、呼吸だけが行われて二酸化炭素が増える。水溶液が酸性になり、BTB 溶液は黄色になる。", d=3, k=["experiment", "thinking"], p=4, st="R-EXP")),
    ("問7(エ)", mc("試験管 A のオオカナダモの葉を取り出して脱色し、ヨウ素液をたらしたところ、葉緑体が青紫色に染まった。このことから、葉緑体で何がつくられたことがわかるか。", ["デンプン", "タンパク質", "脂肪", "ブドウ糖"],
                 "ヨウ素液はデンプンがあると青紫色になる。光合成によって葉緑体でデンプンがつくられた。", d=2, k=["experiment", "knowledge"], p=4, st="R-EXP")),
], "理")
sci += tag(R, "SCI-8", [
    ("問8(ア)", num("気温 $20\\,{}^\\circ\\mathrm{C}$、露点 $10\\,{}^\\circ\\mathrm{C}$ の空気の湿度は何 % か。表を用いて、小数第1位を四捨五入して整数で答えなさい。", "54",
                  "露点 $10\\,{}^\\circ\\mathrm{C}$ より、空気 $1\\,\\mathrm{m^3}$ に含まれる水蒸気量は $9.4\\,\\mathrm{g}$。$20\\,{}^\\circ\\mathrm{C}$ の飽和水蒸気量は $17.3\\,\\mathrm{g/m^3}$。湿度は $9.4\\div17.3\\times100=54.33\\cdots$ より $54\\,\\%$。",
                  d=3, k=["calculation", "data_interpretation"], p=4, unit="%", chk=("floor(Rational(94,173)*100+Rational(1,2))", "54"), st="R-HUM")),
    ("問8(イ)", num("この空気 $1\\,\\mathrm{m^3}$ を $5\\,{}^\\circ\\mathrm{C}$ まで冷やすと、何 g の水滴が生じるか。", "2.6",
                  "$5\\,{}^\\circ\\mathrm{C}$ の飽和水蒸気量は $6.8\\,\\mathrm{g/m^3}$。$9.4-6.8=2.6\\,(\\mathrm{g})$ が水滴になる。", d=3, k=["calculation", "data_interpretation"], p=4, unit="g",
                  chk=("9.4-6.8", "2.6"), st="R-HUM")),
    ("問8(ウ)", mc("雲ができるしくみについて正しいものを選びなさい。", ["空気が上昇すると膨張して温度が下がり、露点に達すると水蒸気が水滴になる", "空気が上昇すると圧縮されて温度が上がり、水蒸気が水滴になる", "空気が下降すると膨張して温度が下がり、水滴ができる", "空気が下降すると温度が上がり、露点に達して水滴ができる"],
                 "上空ほど気圧が低いので、上昇した空気は膨張して温度が下がる。露点以下になると水蒸気が水滴（氷の粒）になり、雲ができる。", d=2, k=K, p=4)),
    ("問8(エ)", num("地表付近で気温 $20\\,{}^\\circ\\mathrm{C}$、露点 $10\\,{}^\\circ\\mathrm{C}$ の空気のかたまりが上昇するとき、雲ができ始めるのは地表から約何 m の高さか。ただし、雲ができるまでは $100\\,\\mathrm{m}$ 上昇するごとに気温が $1\\,{}^\\circ\\mathrm{C}$ 下がり、露点は変化しないものとする。", "1000",
                  "気温が $20\\,{}^\\circ\\mathrm{C}$ から露点 $10\\,{}^\\circ\\mathrm{C}$ まで $10\\,{}^\\circ\\mathrm{C}$ 下がると雲ができ始める。$10\\times100=1000\\,(\\mathrm{m})$。", d=4, k=["calculation", "thinking"], p=4, unit="m",
                  chk=("(20-10)*100", "1000"))),
], "理")

SCI_STIMULI = [
    stim("R-EXP", "試験管 A〜C に、息をふきこんで緑色に調整した BTB 溶液を入れ、A と B にはオオカナダモを入れ、C には何も入れずにゴム栓をした。A と C には光を十分に当て、B はアルミニウムはくで包んで光が当たらないようにした。数時間後、A はうすい青色、B は黄色になり、C は緑色のままだった。",
         "passage", "問7　オオカナダモを用いて次の実験を行った。", source="オリジナル",
         tbl=table([["A", "あり", "当てる", "青色"], ["B", "あり", "当てない", "黄色"], ["C", "なし", "当てる", "緑色"]], header=["試験管", "オオカナダモ", "光", "数時間後の色"])),
    stim("R-HUM", "気温と飽和水蒸気量の関係", "data", "問8　表は、気温と飽和水蒸気量の関係を示したものである。",
         tbl=table([["5", "6.8"], ["10", "9.4"], ["15", "12.8"], ["20", "17.3"], ["25", "23.1"]], header=["気温（℃）", "飽和水蒸気量（g/m³）"])),
]

# ============================== 社会 ==============================
soc = []
soc += tag(S, "SOC-1", [
    ("問1(ア)", mc("経度 0 度の経線（本初子午線）が通る国を選びなさい。", ["イギリス", "フランス", "ドイツ", "アメリカ合衆国"],
                 "本初子午線はイギリスのロンドンにある旧グリニッジ天文台を通る経線である。", d=1, k=K, p=3)),
    ("問1(イ)", mc("東京（東経 135 度の経線で標準時を定める）が 1 月 10 日午前 9 時のとき、ロンドン（経度 0 度）は何月何日の何時か。", ["1 月 10 日午前 0 時", "1 月 10 日午後 6 時", "1 月 9 日午後 9 時", "1 月 10 日午前 6 時"],
                 "経度 15 度で 1 時間の時差。経度差 135 度なので 9 時間。ロンドンは東京より 9 時間遅いので、1 月 10 日午前 0 時。", d=3, k=["knowledge", "calculation"], p=3,
                 chk=("9-135/15", "0"))),
    ("問1(ウ)", mc("一年中気温が高く、降水量が多い熱帯雨林気候に属する都市を選びなさい。", ["シンガポール", "カイロ", "ロンドン", "モスクワ"],
                 "シンガポールは赤道付近にあり、熱帯雨林気候。カイロは砂漠気候、ロンドンは西岸海洋性気候、モスクワは冷帯（亜寒帯）気候。", d=2, k=K, p=3)),
    ("問1(エ)", mc("EU（ヨーロッパ連合）の多くの加盟国で導入されている共通通貨を何というか。", ["ユーロ", "ドル", "ポンド", "フラン"],
                 "EU の多くの加盟国では共通通貨ユーロが使われている。", d=1, k=K, p=3)),
], "社")
soc += tag(S, "SOC-2", [
    ("問2(ア)", mc("日本の最南端の島を選びなさい。", ["沖ノ鳥島", "南鳥島", "与那国島", "択捉島"],
                 "最南端は沖ノ鳥島（東京都）、最東端は南鳥島（東京都）、最西端は与那国島（沖縄県）、最北端は択捉島（北海道）。", d=1, k=K, p=3)),
    ("問2(イ)", mc("縮尺 2 万 5 千分の 1 の地形図上で 4 cm の長さは、実際の距離では何 km か。", ["1 km", "100 m", "10 km", "250 m"],
                 "$4\\times25000=100000\\,(\\mathrm{cm})=1\\,(\\mathrm{km})$。", d=2, k=["knowledge", "calculation"], p=3, chk=("4*25000/100000", "1"))),
    ("問2(ウ)", mc("宮崎平野や高知平野で、冬でも温暖な気候を利用し、ビニールハウスなどで野菜の生長を早めて出荷時期をずらす栽培方法を何というか。", ["促成栽培", "抑制栽培", "近郊農業", "混合農業"],
                 "促成栽培は出荷時期を早める栽培方法。抑制栽培は高原の涼しい気候を利用して出荷時期を遅らせる方法。", d=2, k=K, p=3)),
    ("問2(エ)", mc("伝統的工芸品「南部鉄器」が生産されている県を選びなさい。", ["岩手県", "石川県", "京都府", "佐賀県"],
                 "南部鉄器は岩手県の伝統的工芸品。石川県は輪島塗、京都府は西陣織、佐賀県は有田焼などが知られる。", d=2, k=K, p=3)),
], "社")
soc += tag(S, "SOC-3", [
    ("問3(ア)", mc("聖徳太子（厩戸皇子）が行ったこととして正しいものを選びなさい。", ["冠位十二階の制度を定め、才能や功績のある人物を役人に取り立てた", "墾田永年私財法を出し、開墾した土地の私有を認めた", "平城京に都を移した", "大宝律令を定めた"],
                 "聖徳太子は冠位十二階や十七条の憲法を定め、遣隋使を送った。墾田永年私財法（743年）、平城京遷都（710年）、大宝律令（701年）は奈良時代前後のできごと。", d=2, k=K, p=3)),
    ("問3(イ)", mc("11 世紀前半、娘を天皇のきさきにし、その子を天皇に立てて摂政として権力をふるい、摂関政治の全盛期を築いた人物はだれか。", ["藤原道長", "平清盛", "源頼朝", "菅原道真"],
                 "藤原道長は「この世をば わが世とぞ思ふ」の歌で知られ、子の頼通とともに摂関政治の全盛期を築いた。", d=2, k=K, p=3)),
    ("問3(ウ)", mc("鎌倉幕府における将軍と御家人の関係について正しいものを選びなさい。", ["将軍は御家人の領地を保護し、御家人は戦いのときに命がけで戦った", "御家人は将軍に年貢として米を納め、将軍は御家人に給料を支払った", "将軍と御家人は対等な関係で、主従関係はなかった", "御家人は朝廷に仕え、将軍とは関係がなかった"],
                 "将軍が御家人の領地を保護したり新しい領地を与えたりする「御恩」と、御家人が将軍のために戦う「奉公」による主従関係で結ばれていた。", d=2, k=K, p=3)),
    ("問3(エ)", mc("室町幕府の第 3 代将軍足利義満が始めた、勘合という証明書を用いた貿易の相手国はどこか。", ["明", "宋", "元", "清"],
                 "足利義満は倭寇と区別するため勘合を用いて明との貿易（日明貿易・勘合貿易）を始めた。", d=2, k=K, p=3)),
], "社")
soc += tag(S, "SOC-4", [
    ("問4(ア)", mc("1854 年に結ばれた日米和親条約で開港された港の組み合わせとして正しいものを選びなさい。", ["下田・函館", "横浜・長崎", "神戸・新潟", "下田・横浜"],
                 "日米和親条約で下田と函館が開港された。1858 年の日米修好通商条約では函館・神奈川（横浜）・長崎・新潟・兵庫（神戸）の5港が開港された。", d=2, k=K, p=3)),
    ("問4(イ)", mc("明治政府が 1873 年から行った地租改正の内容として正しいものを選びなさい。", ["土地の所有者に地券を発行し、地価の 3% を現金で納めさせた", "収穫高の 3% を米で納めさせた", "20 歳以上の男子に兵役の義務を課した", "6 歳以上の男女に小学校教育を受けさせた"],
                 "地租改正により、地価の 3%（のちに 2.5%）を土地の所有者が現金で納めることになり、政府の税収が安定した。兵役は徴兵令、小学校は学制。", d=2, k=K, p=3)),
    ("問4(ウ)", mc("1889 年に発布された大日本帝国憲法について正しいものを選びなさい。", ["君主権の強いドイツ（プロイセン）の憲法を参考にし、天皇が国の元首として統治すると定めた", "アメリカ合衆国の憲法を参考にし、国民主権を定めた", "国民が選挙で選んだ議員による国民議会が起草した", "基本的人権を永久の権利として無条件に保障した"],
                 "伊藤博文らが君主権の強いドイツの憲法を参考に草案を作成した。主権は天皇にあり、国民（臣民）の権利は法律の範囲内で認められた。", d=3, k=K, p=3)),
    ("問4(エ)", mc("日清戦争の講和条約である下関条約で日本が得た遼東半島を、ロシア・ドイツ・フランスの要求によって清に返還したできごとを何というか。", ["三国干渉", "三国同盟", "義和団事件", "ポーツマス条約"],
                 "三国干渉の後、ロシアへの対抗心が高まり、のちの日露戦争につながった。", d=2, k=K, p=3)),
], "社")
soc += tag(S, "SOC-5", [
    ("問5(ア)", mc("1925 年に成立した普通選挙法によって選挙権を得た人々として正しいものを選びなさい。", ["満 25 歳以上のすべての男子", "満 20 歳以上のすべての男女", "直接国税 3 円以上を納める満 25 歳以上の男子", "満 18 歳以上のすべての男女"],
                 "1925 年の普通選挙法で納税額による制限が廃止され、満 25 歳以上の男子に選挙権が与えられた。女性の参政権は 1945 年に認められた。", d=2, k=K, p=4)),
    ("問5(イ)", mc("1929 年に始まった世界恐慌に対して、アメリカ合衆国が行った政策を何というか。", ["ニューディール政策", "ブロック経済", "五か年計画", "マーシャル・プラン"],
                 "ローズベルト大統領はニューディール（新規まき直し）政策で大規模な公共事業などを行った。ブロック経済はイギリス・フランス、五か年計画はソ連。", d=2, k=K, p=4)),
    ("問5(ウ)", order("次のできごとを年代の古い順に並べなさい。", ["日中戦争が始まる", "太平洋戦争が始まる", "日本国憲法が施行される", "サンフランシスコ平和条約が結ばれる"],
                    "日中戦争（1937 年）→ 太平洋戦争（1941 年）→ 日本国憲法施行（1947 年）→ サンフランシスコ平和条約（1951 年）。", d=3, k=["knowledge", "thinking"], p=4)),
], "社")
soc += tag(S, "SOC-6", [
    ("問6(ア)", mc("日本国憲法の三つの基本原理の組み合わせとして正しいものを選びなさい。", ["国民主権・基本的人権の尊重・平和主義", "国民主権・三権分立・平和主義", "天皇主権・基本的人権の尊重・平和主義", "国民主権・基本的人権の尊重・地方自治"],
                 "日本国憲法の三大原理は国民主権・基本的人権の尊重・平和主義。", d=1, k=K, p=4)),
    ("問6(イ)", mc("衆議院だけに認められている権限として正しいものを選びなさい。", ["内閣不信任の決議", "法律案の議決", "憲法改正の発議", "国政調査権"],
                 "内閣不信任の決議は衆議院のみが行える。法律案の議決・憲法改正の発議・国政調査権は両院が持つ（憲法改正の発議には各議院の総議員の3分の2以上の賛成が必要）。", d=3, k=K, p=4)),
    ("問6(ウ)", mc("裁判員制度について正しいものを選びなさい。", ["くじで選ばれた国民が、重大な刑事裁判の第一審に参加する", "国民が選挙で裁判官を選ぶ", "裁判員は民事裁判だけに参加する", "裁判員は有罪・無罪のみを判断し、刑の重さは判断しない"],
                 "裁判員制度では、18 歳以上の国民からくじで選ばれた裁判員が、殺人などの重大な刑事事件の第一審に参加し、裁判官とともに有罪・無罪と刑の重さを決める。", d=2, k=K, p=4)),
    ("問6(エ)", mc("地方自治において、住民が条例の制定や改廃を首長に請求するときに必要な署名の数として正しいものを選びなさい。", ["有権者の 50 分の 1 以上", "有権者の 3 分の 1 以上", "有権者の過半数", "有権者の 10 分の 1 以上"],
                 "条例の制定・改廃の請求や監査請求は有権者の 50 分の 1 以上の署名が必要。首長・議員の解職請求や議会の解散請求は原則として 3 分の 1 以上。", d=3, k=K, p=4)),
], "社")
soc += tag(S, "SOC-7", [
    ("問7(ア)", mc("ある商品の需要量が供給量を上回っているとき、一般にその商品の価格はどうなるか。", ["上がる", "下がる", "変わらない", "0 になる"],
                 "買いたい量（需要量）が売りたい量（供給量）より多いと、品不足となって価格は上昇する。", d=1, k=K, p=3)),
    ("問7(イ)", mc("日本銀行の役割として正しいものを選びなさい。", ["紙幣（日本銀行券）を発行する", "企業や個人から直接預金を集めて貸し出す", "税金を集めて国の予算を決める", "株式を発行して資金を集める"],
                 "日本銀行は「発券銀行」「政府の銀行」「銀行の銀行」の役割をもつ。個人や一般企業とは直接取り引きしない。予算は内閣が作成し国会が議決する。", d=2, k=K, p=3)),
    ("問7(ウ)", mc("所得が高い人ほど税率が高くなるしくみを何というか。", ["累進課税", "間接税", "消費税", "地方交付税"],
                 "所得税などで採用されている累進課税は、所得の格差を縮める（所得の再分配）はたらきがある。", d=2, k=K, p=3)),
    ("問7(エ)", mc("日本の社会保障制度のうち、年金保険や医療保険が含まれるものを選びなさい。", ["社会保険", "公的扶助", "社会福祉", "公衆衛生"],
                 "社会保険は加入者が保険料を出し合い、病気・老後などに給付を受けるしくみ。公的扶助は生活保護、社会福祉は高齢者や障がいのある人への支援、公衆衛生は感染症対策など。", d=2, k=K, p=3)),
], "社")
soc += tag(S, "SOC-8", [
    ("問8(ア)", mc("資料から読み取れることとして正しいものを選びなさい。", ["2020 年は 2000 年と比べて、再生可能エネルギーの割合が 8 倍になっている", "2020 年は 2000 年と比べて、原子力の割合が増えている",
                                                      "2020 年は水力の割合が最も高い", "2000 年と 2020 年で火力の割合は変わらない"],
                 "再生可能エネルギー（水力を除く）は 2% から 16% で 8 倍。原子力は 30% から 5% に減少、火力は 60% から 70% に増加している。", d=3, k=["data_interpretation"], p=4, st="S-ENERGY",
                 chk=("16/2", "8"))),
    ("問8(イ)", mc("資料中の「再生可能エネルギー（水力を除く）」にあたる発電方法として適切なものを選びなさい。", ["太陽光発電", "石炭火力発電", "天然ガス火力発電", "原子力発電"],
                 "再生可能エネルギーは太陽光・風力・地熱・バイオマスなど、くり返し使えて枯渇しないエネルギー。", d=1, k=K, p=4, st="S-ENERGY")),
    ("問8(ウ)", desc("資料の国 X で火力発電の割合が高まったことには、どのような課題があると考えられるか。「温室効果ガス」「輸入」の 2 語を使って説明しなさい。",
                    "火力発電は燃料を燃やすときに二酸化炭素などの温室効果ガスを多く排出し、地球温暖化を進めるおそれがある。また、燃料を輸入に頼る場合、国際情勢によって安定して確保できなくなるおそれがある。",
                    "火力発電の課題として、温室効果ガスの排出（環境面）と、化石燃料の輸入依存（エネルギー安全保障・経済面）の2点を挙げる。",
                    [("温室効果ガスの排出と地球温暖化について述べている", 2), ("燃料の輸入に頼ることによる課題（安定確保・価格変動など）を述べている", 2)],
                    d=4, k=["thinking", "data_interpretation"], p=4, lines=4, st="S-ENERGY")),
], "社")

SOC_STIMULI = [
    stim("S-ENERGY", "架空の国 X における発電電力量の割合（%）の変化", "data", "問8　次の資料を見て、あとの問いに答えなさい。",
         tbl=table([["2000年", 60, 30, 8, 2], ["2020年", 70, 5, 9, 16]], header=["年", "火力", "原子力", "水力", "再生可能エネルギー（水力を除く）"])),
]

SECTIONS = [
    {"id": "ENG-1", "title": "英語　問1　リスニング", "subject": "english", "page_break": True, "time_limit_minutes": 50,
     "instructions": "放送を聞いて答えなさい。英文はそれぞれ1回ずつ放送されます（放送文は解答・解説冊子に掲載）。"},
    {"id": "ENG-2", "title": "英語　問2　語彙", "subject": "english"},
    {"id": "ENG-3", "title": "英語　問3　文法", "subject": "english"},
    {"id": "ENG-4", "title": "英語　問4　語順整序", "subject": "english", "instructions": "解答欄には、選択肢の番号を正しい順に書きなさい。"},
    {"id": "ENG-5", "title": "英語　問5　条件英作文", "subject": "english"},
    {"id": "ENG-6", "title": "英語　問6　スピーチの読解", "subject": "english", "stimulus_refs": ["E-SPEECH"]},
    {"id": "ENG-7", "title": "英語　問7　資料の読解", "subject": "english", "stimulus_refs": ["E-POSTER"]},
    {"id": "ENG-8", "title": "英語　問8　対話文と表の読解", "subject": "english", "stimulus_refs": ["E-DIALOGUE"]},
    {"id": "MATH-1", "title": "数学　問1　計算", "subject": "math", "page_break": True, "time_limit_minutes": 50},
    {"id": "MATH-2", "title": "数学　問2　小問集合", "subject": "math"},
    {"id": "MATH-3", "title": "数学　問3　図形・資料の活用", "subject": "math"},
    {"id": "MATH-4", "title": "数学　問4　関数", "subject": "math"},
    {"id": "MATH-5", "title": "数学　問5　確率", "subject": "math"},
    {"id": "MATH-6", "title": "数学　問6　空間図形", "subject": "math"},
    {"id": "JPN-1", "title": "国語　問一　漢字・語句", "subject": "japanese", "page_break": True, "time_limit_minutes": 50},
    {"id": "JPN-2", "title": "国語　問二　古典", "subject": "japanese", "stimulus_refs": ["J-KOBUN"]},
    {"id": "JPN-3", "title": "国語　問三　小説", "subject": "japanese", "stimulus_refs": ["J-NOVEL"]},
    {"id": "JPN-4", "title": "国語　問四　論説文", "subject": "japanese", "stimulus_refs": ["J-ESSAY"]},
    {"id": "JPN-5", "title": "国語　問五　資料の読み取りと提案", "subject": "japanese", "stimulus_refs": ["J-DATA"]},
    {"id": "SCI-1", "title": "理科　問1　物理分野の小問", "subject": "science", "page_break": True, "time_limit_minutes": 50},
    {"id": "SCI-2", "title": "理科　問2　化学分野の小問", "subject": "science"},
    {"id": "SCI-3", "title": "理科　問3　生物分野の小問", "subject": "science"},
    {"id": "SCI-4", "title": "理科　問4　地学分野の小問", "subject": "science"},
    {"id": "SCI-5", "title": "理科　問5　運動とエネルギー", "subject": "science"},
    {"id": "SCI-6", "title": "理科　問6　中和", "subject": "science"},
    {"id": "SCI-7", "title": "理科　問7　光合成と呼吸", "subject": "science", "stimulus_refs": ["R-EXP"]},
    {"id": "SCI-8", "title": "理科　問8　湿度と雲のでき方", "subject": "science", "stimulus_refs": ["R-HUM"]},
    {"id": "SOC-1", "title": "社会　問1　世界の地理", "subject": "social", "page_break": True, "time_limit_minutes": 50},
    {"id": "SOC-2", "title": "社会　問2　日本の地理", "subject": "social"},
    {"id": "SOC-3", "title": "社会　問3　歴史（古代〜中世）", "subject": "social"},
    {"id": "SOC-4", "title": "社会　問4　歴史（近世〜近代）", "subject": "social"},
    {"id": "SOC-5", "title": "社会　問5　歴史（近現代）", "subject": "social"},
    {"id": "SOC-6", "title": "社会　問6　公民（政治）", "subject": "social"},
    {"id": "SOC-7", "title": "社会　問7　公民（経済）", "subject": "social"},
    {"id": "SOC-8", "title": "社会　問8　資料の読み取り", "subject": "social", "stimulus_refs": ["S-ENERGY"]},
]

SETS = [{
    "set_id": "KNG-MOCK-R8-01",
    "track": "mock_exam",
    "title": "神奈川県公立高校入試型　5教科オリジナル模試（第1回）",
    "subtitle": "令和8年度　英語・数学・国語・理科・社会　各100点・各50分",
    "description": "神奈川県公立高等学校入学者選抜の学力検査の近年の出題構成（大問構成・マークシート方式中心）を参考に作成したオリジナル模試。",
    "stage": "junior_high",
    "subject": "integrated",
    "grade": "JH3",
    "unit_ids": [E, M, J, R, S],
    "labels": "num",
    "instructions": [
        "検査時間は各教科 50 分、配点は各教科 100 点です。教科ごとに時間を計って解きなさい。",
        "選択式の問題は、選択肢の番号で答えなさい（解答用紙の該当する番号をぬりつぶす形式を想定しています）。",
        "記述式の問題は、解答用紙の指定された欄に書きなさい。字数制限のある問題は、句読点や「」なども 1 字に数えます。",
        "英語の問1はリスニング問題です。放送文は解答・解説冊子に掲載しています。",
    ],
    "exam_spec": {
        "name": "5教科オリジナル模試（第1回）",
        "reference": "神奈川県公立高校入試（学力検査）の近年の出題構成を参考",
        "answer_format": "mixed",
        "notes": "大問構成・配点は近年の出題傾向をもとにした目安であり、実際の入試の出題内容・配点とは異なる。最新の実施要項は神奈川県教育委員会の公表資料で確認すること。",
    },
    "sections": SECTIONS,
    "stimuli": ENG_STIMULI + JPN_STIMULI + SCI_STIMULI + SOC_STIMULI,
    "total_points": 500,
    "build": {"show_points": True, "show_difficulty": False},
    "out": "data/pilot/kanagawa_mock_r8_01.json",
    "items": eng + math + jpn + sci + soc,
}]
