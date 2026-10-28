"""単元パック：共通テスト対策　英語リーディング（情報の検索と要旨把握）。

広告・掲示・論説文はすべてこのパックのためのオリジナル英文。調査の数値などはすべて架空の資料である。
"""
from banks._common import desc, mc, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "CT-ENG-U01"

PREREQUISITES = [
    ("HS-ENG-U09", "パラグラフの構成・ディスコースマーカーを手がかりに、段落の役割と筆者の主張をつかめること"),
    ("JH-ENG-G3-U06", "対話文・説明文・グラフや資料の読み取りの基本（必要な情報を本文から探す習慣）"),
    ("HS-ENG-U07", "比較級・最上級・倍数表現を正しく読み、数量の大小や評価の表現を区別できること"),
]
EXTENSIONS = [
    ("CT-ENG-U02", "同じ「情報の検索・要旨把握・事実と意見の区別」の力を、音声で聞く場面に広げる"),
    ("SS-ENG-U01", "要旨把握の手順を、二次試験の内容説明・下線部和訳の記述答案に生かす"),
    ("HS-ENG-U10", "論説文の「主張＋理由＋譲歩」の構成を、自分の意見文を書くときの型として使う"),
]


def yen(n):
    return f"{n:,} yen"


def jyen(n):
    return f"{n:,}円"


# ======================================================================
# 広告・掲示（オリジナル）
# ======================================================================

# --- 料金計算に使う3つの掲示（掲示文は料金表から組み立てるので、本文と計算が必ず一致する） ---
MU_AD, MU_HS, MU_PL, MU_GROUP = 1200, 700, 300, 10
MUSEUM = ("Greenhill Science Museum — Summer Night Program\n"
          "・Dates: Every Friday and Saturday in August\n"
          "・Hours: 6:00 p.m. – 9:00 p.m. (last entry 8:30 p.m.)\n"
          f"・Admission: Adults {yen(MU_AD)} / High school students {yen(MU_HS)} / Junior high school students and younger: free\n"
          f"・Planetarium show (starts at 7:00 p.m., 30 minutes): {yen(MU_PL)} per person, in addition to admission. Tickets are sold at the entrance only.\n"
          f"・Groups of {MU_GROUP} or more people (including children): 10% off admission. The discount does not apply to planetarium tickets.\n"
          "・Food and drinks are not allowed in the exhibition rooms.")

PO_AD, PO_ST, PO_CH, PO_WE = 600, 400, 200, 100
POOL = ("Riverside City Pool — Opening Notice\n"
        "・Open: July 15 – August 31, 9:00 a.m. – 5:00 p.m. (closed on Mondays)\n"
        f"・Weekday prices: Adults {yen(PO_AD)} / High school and university students {yen(PO_ST)} / Children aged 6 to 15 {yen(PO_CH)} / Children under 6: free\n"
        f"・On Saturdays, Sundays, and national holidays, every price is {PO_WE} yen higher, except for children under 6 (always free).\n"
        "・Children under 10 must be with an adult at all times.\n"
        "・Students must show a student ID card at the ticket counter.")

BK_STD, BK_ELE, BK_STD_DAY, BK_ELE_DAY = 300, 600, 1500, 2500
BIKE = ("Lakeside Bike Rental\n"
        f"・Standard bike: {yen(BK_STD)} per hour / One-day pass {yen(BK_STD_DAY)}\n"
        f"・Electric bike: {yen(BK_ELE)} per hour / One-day pass {yen(BK_ELE_DAY)}\n"
        "・Hourly rental is charged for every hour that has started. (Example: 1 hour and 10 minutes = 2 hours)\n"
        "・One-day passes can be used from 9:00 a.m. until we close at 6:00 p.m.\n"
        "・Helmets are free. Please return bikes to the same shop where you rented them.")

LEAFLET = ("Join the Minato Beach Clean-Up!\n"
           "・When: Sunday, June 8, 8:00 a.m. – 10:00 a.m. (If it rains, the event will be held on June 15.)\n"
           "・Meeting place: In front of the Minato Station north exit at 7:45 a.m.\n"
           "・Bring: Gloves, a hat, and something to drink. Trash bags will be provided.\n"
           "・Sign up by June 1 on our website. High school students need a parent's permission.\n"
           "・Everyone who joins will receive a free towel.")

CLUB = ("English Debate Club — New Members Wanted!\n"
        "・We meet every Tuesday and Thursday from 4:00 p.m. to 5:30 p.m. in Room 204.\n"
        "・No experience is needed. Most of our members started debating in high school.\n"
        "・In November, we take part in the city debate contest. Members who want to join the contest must attend at least one practice a week from September.\n"
        "・Visit us any time in April to watch a practice. Please talk to Ms. Ito if you have any questions.")

NOTICES = {
    "MUSEUM": dict(title="Summer Night Program", text=MUSEUM, qs=[
        ("What is the latest time visitors can enter the museum during the program?", "8:30 p.m.",
         [("9:00 p.m.", "9:00 p.m. は閉館時刻。入館の締め切り（last entry）は 8:30 p.m. である。"),
          ("7:00 p.m.", "7:00 p.m. はプラネタリウムの開始時刻である。"),
          ("6:00 p.m.", "6:00 p.m. は開館時刻である。")]),
        ("Where can visitors buy planetarium tickets?", "At the museum entrance",
         [("On the museum's website", "Tickets are sold at the entrance only とあり、ウェブサイトでは買えない。"),
          ("Inside the planetarium", "入口でのみ販売と書かれている。"),
          ("At any exhibition room", "展示室で買えるとは書かれていない。")]),
        ("Which is true about the group discount?", "It does not apply to planetarium tickets.",
         [("It is for groups of five or more people.", "割引の対象は10人以上の団体である。"),
          ("Children are not counted as group members.", "including children とあり、子どもも人数に含める。"),
          ("It gives 10% off both admission and the planetarium.", "割引は入館料のみで、プラネタリウムには適用されない。")]),
    ]),
    "POOL": dict(title="Riverside City Pool", text=POOL, qs=[
        ("On which day is the pool closed?", "Monday",
         [("Sunday", "日曜日は営業しており、料金が100円高くなる日である。"),
          ("Saturday", "土曜日は営業している。"),
          ("National holidays", "祝日は休みではなく、料金が100円高くなる日である。")]),
        ("What must high school students do to get the student price?", "Show a student ID card",
         [("Come with an adult", "大人の同伴が必要なのは10歳未満の子どもである。"),
          ("Buy a ticket in advance", "前売り券については書かれていない。"),
          ("Visit on a weekday", "平日でも休日でも、学生料金で入るには学生証の提示が必要である。")]),
        ("Who must be with an adult at the pool?", "Children under 10",
         [("Children under 6 only", "6歳未満は料金が無料になる区分で、大人の同伴が必要なのは10歳未満である。"),
          ("All children aged 6 to 15", "15歳までの子ども料金の区分と、同伴が必要な年齢（10歳未満）を混同している。"),
          ("High school students", "高校生の同伴については書かれていない。")]),
    ]),
    "BIKE": dict(title="Lakeside Bike Rental", text=BIKE, qs=[
        ("How much does it cost to rent a standard bike for 1 hour and 10 minutes?", yen(2 * BK_STD),
         [(yen(BK_STD), "始まった1時間ごとに料金がかかるので、1時間10分は2時間分になる。"),
          (yen(BK_STD_DAY), "1日パスより時間料金のほうが安い。"),
          (yen(2 * BK_ELE), "電動自転車の料金と取り違えている。")]),
        ("Which is true about returning a bike?", "It must be returned to the shop where it was rented.",
         [("It can be returned to any shop in the city.", "same shop where you rented them とあり、借りた店に返す必要がある。"),
          ("It can be kept until the next morning with a one-day pass.", "1日パスは閉店の午後6時までである。"),
          ("The helmet must be bought before returning it.", "ヘルメットは無料である。")]),
        ("Until what time can a one-day pass be used?", "6:00 p.m.",
         [("9:00 a.m.", "9:00 a.m. は利用開始の時刻である。"),
          ("9:00 p.m.", "閉店は午後6時と書かれている。"),
          ("Midnight", "閉店時刻（6:00 p.m.）までである。")]),
    ]),
    "LEAFLET": dict(title="Minato Beach Clean-Up", text=LEAFLET, qs=[
        ("What should participants bring?", "Gloves, a hat, and a drink",
         [("Trash bags", "ごみ袋は主催者が用意する（will be provided）。"),
          ("A towel", "タオルは参加者全員がもらえるもので、持参するものではない。"),
          ("A parent's letter and a lunch box", "保護者の許可は申し込みの条件で、昼食の持参は書かれていない。")]),
        ("If it rains on June 8, what will happen?", "The event will be held on June 15.",
         [("The event will be canceled.", "雨の場合は中止ではなく、6月15日に延期される。"),
          ("The event will start at 7:45 a.m.", "7:45 a.m. は集合時刻であり、雨天時の対応ではない。"),
          ("Participants will clean the station instead.", "駅を清掃するとは書かれていない。")]),
        ("What is the deadline for signing up?", "June 1",
         [("June 8", "6月8日は清掃の実施日である。"),
          ("June 15", "6月15日は雨天時の予備日である。"),
          ("The day of the event", "申し込みは6月1日までにウェブサイトで行う。")]),
    ]),
    "CLUB": dict(title="English Debate Club", text=CLUB, qs=[
        ("Which is true about the English Debate Club?", "Students without debate experience can join.",
         [("Members must have debated in junior high school.", "No experience is needed とある。"),
          ("The club meets three times a week.", "活動は火曜と木曜の週2回である。"),
          ("Only members who joined in April can watch practices.", "4月中はいつでも見学できると書かれており、見学に条件はない。")]),
        ("What must members do to take part in the city contest?", "Attend at least one practice a week from September.",
         [("Practice every day in November.", "毎日練習するとは書かれていない。"),
          ("Talk to Ms. Ito before April.", "伊藤先生には質問があれば話すとあるだけで、大会参加の条件ではない。"),
          ("Win a contest at school first.", "校内大会については書かれていない。")]),
        ("Where does the club meet?", "In Room 204",
         [("In the city hall", "市の大会の会場は書かれておらず、活動場所は204教室である。"),
          ("In Ms. Ito's office", "伊藤先生は質問の相談先であり、活動場所ではない。"),
          ("In the library", "図書館は書かれていない。")]),
    ]),
}


def nstim(key):
    n = NOTICES[key]
    return stim(f"NT-{key}", n["text"], "data", "次の掲示（広告）を読んで、あとの問いに答えなさい。", source="オリジナル")


# ======================================================================
# 事実と意見（短い文）— 架空の場面
# ======================================================================

# (場面, 事実[(文)], 意見[(文, 意見を示す手がかり)])
FO = [
    ("部活動の朝練習",
     ["The survey was answered by 240 students at our school.", "The school gate opens at 7:00 a.m.",
      "Morning practice usually lasts 40 minutes.", "About half of the club members practice before classes start."],
     [("Morning practice is the best way to start the day.", "the best way（最上級による評価）"),
      ("Students should be allowed to sleep longer instead of practicing early.", "should（あるべき姿の主張）"),
      ("I think 40 minutes is too short to improve our skills.", "I think と too short（評価）"),
      ("It seems unfair that only some clubs can use the gym in the morning.", "It seems unfair（判断）")]),
    ("シェアサイクル",
     ["There are 35 bike stations around the station area.", "A one-day pass costs 500 yen.",
      "The service was used 12,000 times last month.", "Bikes can be returned to any station."],
     [("The service is a great way for tourists to see the city.", "a great way（評価）"),
      ("The city ought to build more stations near schools.", "ought to（あるべき姿の主張）"),
      ("Riding a shared bike is much more enjoyable than taking a bus.", "more enjoyable（主観的な比較）"),
      ("In my opinion, a one-day pass is a bit expensive.", "In my opinion と expensive（評価）")]),
    ("学校の食堂",
     ["The cafeteria serves about 300 lunches a day.", "The cafeteria is closed on Saturdays.",
      "A vegetarian menu was added last year.", "A set lunch costs 450 yen."],
     [("The new curry is the most delicious dish on the menu.", "the most delicious（主観的な評価）"),
      ("The cafeteria should stay open after school.", "should（あるべき姿の主張）"),
      ("I believe students eat too quickly at lunchtime.", "I believe と too quickly（評価）"),
      ("The vegetarian menu is probably popular because it is healthy.", "probably（推測）")]),
    ("オンライン授業",
     ["In the survey, 62% of the students said they had taken an online class.", "The online lessons were recorded.",
      "Each online lesson lasted 50 minutes.", "The school lent tablets to 120 students."],
     [("Online classes are less effective than face-to-face classes.", "less effective（評価を含む比較）"),
      ("Recorded lessons are a wonderful tool for reviewing.", "wonderful（評価）"),
      ("Schools must keep offering online lessons in the future.", "must（主張）"),
      ("It would be better to mix online and face-to-face lessons.", "It would be better（提案）")]),
    ("町の夏祭り",
     ["More than 5,000 people visited the festival this year.", "The fireworks started at 8:00 p.m.",
      "Volunteers collected 200 bags of trash after the event.", "The festival was held in the park next to the river."],
     [("The fireworks were the most beautiful I have ever seen.", "the most beautiful（主観的な評価）"),
      ("The festival should be held on two days instead of one.", "should（主張）"),
      ("Young people will surely enjoy the new dance contest.", "will surely（予想・推測）"),
      ("The town needs more volunteers to make the event better.", "needs … to make the event better（判断）")]),
    ("レジ袋の有料化",
     ["Since July 2020, stores in Japan have charged customers for plastic shopping bags.", "The store near our school sells a plastic bag for 3 yen.",
      "In our class survey, 28 of the 35 students said they carry their own bags.", "Our school started a bag-sharing box in May."],
     [("Charging for bags is a smart idea.", "smart（評価）"),
      ("Everyone should carry a reusable bag.", "should（主張）"),
      ("Paper bags are better for the environment than plastic ones.", "better（評価を含む比較）"),
      ("I think 3 yen is too cheap to change people's habits.", "I think と too cheap（評価）")]),
]

FACT_WHY = "数値・日時・出来事など、資料や記録で正しいかどうかを確かめられる内容なので事実である。"


def op_why(sig):
    return f"{sig}を含み、書き手の判断・評価を述べている。人によって考えが分かれうるので意見である。"


# ======================================================================
# 論説文（オリジナル・調査はすべて架空）
# ======================================================================

PASSAGES = [
    dict(key="LATE", title="Should Schools Start Later?",
         paras=["Many high school students in our town say they feel sleepy in the morning. In a survey of 400 students at three local high schools, 68% answered that they sleep less than seven hours on school nights. Some people now suggest that schools should start classes 30 minutes later.",
                "Supporters of a later start point out that teenagers tend to become sleepy later at night than adults do. If classes begin later, students can get more sleep without changing their bedtime. One school in the survey tried starting at 9:00 a.m. for one month, and the number of students who arrived late dropped from 25 to 9.",
                "However, a later start also creates problems. Club activities would end later, and some students would have to go home after dark. Parents who drive their children to school might also have trouble because of their work schedules.",
                "In my view, a later start is worth trying, but each school should first talk with students and parents. A small change in the timetable could make a big difference to students' health, as long as everyone's needs are considered."],
         main="A later start could help students sleep more, but schools should discuss it with students and parents first.",
         main_wrong=[("One school had fewer late students after it started classes at 9:00 a.m.", "narrow"),
                     ("Teenagers today face many different problems at school.", "broad"),
                     ("Schools should not change their start time because club activities would end later.", "contra")],
         title_ok="A Later Start: Worth Trying, With Care",
         title_wrong=[("Why Teenagers Love Club Activities", "off"), ("A One-Month Trial at One School", "narrow"), ("Keep the School Day as It Is", "contra")],
         facts=["In the survey, 68% of the students said they sleep less than seven hours on school nights.",
                "At one school, the number of late students went down from 25 to 9 during the trial.",
                "The survey was carried out at three high schools."],
         opinions=["A later start is worth trying.", "Each school should talk with students and parents before changing the timetable.",
                   "A small change in the timetable could make a big difference to students' health."],
         trues=["More than half of the students in the survey sleep less than seven hours on school nights.",
                "The writer wants schools to listen to students and parents before changing the start time.",
                "A later start might cause trouble for some parents who drive their children to school."],
         falses=[("All three schools in the survey started classes at 9:00 a.m.", "9時始業を1か月試したのは1校だけである。"),
                 ("The writer is strongly against a later start.", "第4段落で、試す価値があると述べている。"),
                 ("During the trial, the number of late students increased.", "遅刻者は25人から9人に減っている。"),
                 ("Teenagers usually become sleepy earlier at night than adults.", "第2段落で、大人より遅い時間に眠くなる傾向があると述べている。")],
         summary="始業を遅らせれば生徒は睡眠を増やせるが、部活動の終了が遅くなるなどの問題もある。筆者は試す価値があるとしつつ、まず生徒や保護者と話し合うべきだと考えている。",
         skeys=[("始業を遅らせると睡眠が増えるという利点を述べている", 3), ("部活動・通学などの問題点に触れている", 2), ("生徒・保護者と話し合ったうえで試すべきだという主張でまとめている", 3)],
         wrong_sum=[("ある学校で始業を9時にしたところ、遅刻者が25人から9人に減った。", "第2段落の具体的な試みの結果だけで、筆者の主張（話し合ったうえで試す価値がある）が入っていない。"),
                    ("始業を遅らせると部活動の終了が遅くなり、暗い中で帰宅する生徒も出るので、始業時刻を変えるべきではない。", "第3段落の However 以下の問題点を主張と取り違えており、筆者の結論（試す価値がある）と逆になっている。")]),
    dict(key="CASH", title="Cashless Payment at the School Festival",
         paras=["Last year, our school festival tried something new: visitors could pay at food stands with a smartphone app instead of cash. The student council wanted to know whether this change was a good idea, so it asked 150 visitors and 60 student staff members to answer a short questionnaire.",
                "The results were mostly positive. Of the visitors, 72% said that paying with the app was faster, and the staff no longer had to count coins at the end of the day. One staff member said, \"It saved us at least an hour of work.\"",
                "On the other hand, not everyone was happy. Some older visitors did not have the app, so they had to wait in a separate line to pay in cash. A few stands also had trouble when the Internet connection became slow in the afternoon.",
                "I believe cashless payment should continue at this year's festival, but cash should still be accepted. That way, the festival can become more convenient without leaving anyone out."],
         main="Cashless payment should continue at the festival, but cash should also be accepted so that no one is left out.",
         main_wrong=[("Staff members no longer had to count coins at the end of the day.", "narrow"),
                     ("Smartphones are used for many things in daily life.", "broad"),
                     ("The festival should stop using the app because the Internet connection was slow.", "contra")],
         title_ok="Going Cashless Without Leaving Anyone Out",
         title_wrong=[("How to Make Popular Festival Food", "off"), ("A Slow Internet Connection", "narrow"), ("Why Cash Is Always Better", "contra")],
         facts=["The student council asked 150 visitors to answer a questionnaire.", "72% of the visitors said that paying with the app was faster.",
                "Some older visitors had to wait in a separate line to pay in cash."],
         opinions=["Cashless payment should continue at this year's festival.", "Cash should still be accepted at the festival.",
                   "Accepting both kinds of payment would make the festival convenient for everyone."],
         trues=["The student council asked both visitors and student staff for their views.", "Some visitors could not use the app.",
                "The writer wants the festival to use both the app and cash."],
         falses=[("All of the visitors said that paying with the app was faster.", "app のほうが速いと答えたのは来場者の72%である。"),
                 ("The writer thinks cash should no longer be accepted.", "第4段落で、現金も引き続き受け付けるべきだと述べている。"),
                 ("The Internet connection was slow all day.", "接続が遅くなったのは午後である。"),
                 ("Staff members had to spend more time counting coins.", "第2段落で、硬貨を数える必要がなくなったと述べている。")],
         summary="文化祭でのアプリ決済は会計が速くなり好評だったが、アプリを持たない人や通信の問題もあった。筆者は現金も併用しつつキャッシュレス決済を続けるべきだと考えている。",
         skeys=[("アプリ決済の利点（速さ・作業の軽減）を述べている", 3), ("アプリを使えない人や通信の問題に触れている", 2), ("現金と併用して続けるべきだという主張でまとめている", 3)],
         wrong_sum=[("ある係の生徒は、アプリ決済で少なくとも1時間の作業が省けたと言った。", "第2段落の1人の発言（具体例）だけで、筆者の主張（現金と併用して続けるべきだ）が入っていない。"),
                    ("アプリを持たない人が並ばされ、通信も遅くなったので、キャッシュレス決済はやめるべきだ。", "第3段落の On the other hand 以下の問題点を主張と取り違えており、筆者の結論と逆になっている。")]),
    dict(key="VEGE", title="A Meat-Free Day in the Cafeteria",
         paras=["This spring, our school cafeteria started a \"meat-free day\" every Wednesday. On that day, all the lunch menus are made without meat. The cafeteria staff say they wanted students to try a wider variety of vegetables and beans.",
                "There are good reasons for this idea. Producing meat generally uses more land and water than producing vegetables, so eating less meat can reduce the burden on the environment. The cafeteria also reports that its costs on Wednesdays are about 10% lower.",
                "Not all students are pleased, however. In a class survey, 14 of 32 students said they feel hungry by the afternoon on Wednesdays, and the number of lunches sold on that day fell by about 20% in the first month.",
                "I think the meat-free day is a good start, but the menus need to be improved. If the cafeteria asks students for ideas and offers filling dishes such as bean curry, more students will look forward to Wednesdays."],
         main="The meat-free day is a good idea, but the cafeteria should improve its menus with students' ideas.",
         main_wrong=[("The cafeteria's costs are about 10% lower on Wednesdays.", "narrow"),
                     ("Many people around the world eat meat every day.", "broad"),
                     ("The meat-free day should end because some students feel hungry.", "contra")],
         title_ok="Making Meat-Free Wednesdays Work",
         title_wrong=[("How to Cook Bean Curry at Home", "narrow"), ("Why Students Skip Lunch", "off"), ("The End of Meat-Free Wednesdays", "contra")],
         facts=["The cafeteria started the meat-free day this spring.", "The number of lunches sold on Wednesdays fell by about 20% in the first month.",
                "In a class survey, 14 of 32 students said they feel hungry by the afternoon on Wednesdays."],
         opinions=["The meat-free day is a good start.", "The menus need to be improved.",
                   "More students will look forward to Wednesdays if the menus are better."],
         trues=["On Wednesdays, the cafeteria serves lunches made without meat.", "Fewer lunches were sold on Wednesdays in the first month.",
                "The writer suggests that the cafeteria should ask students for menu ideas."],
         falses=[("The cafeteria serves meat-free lunches every day.", "肉なしの日は毎週水曜日だけである。"),
                 ("Most of the students in the class survey said they feel hungry on Wednesdays.", "32人中14人で、半数に満たない。"),
                 ("The cafeteria's costs on Wednesdays are higher than on other days.", "第2段落で、水曜日の費用は約10%低いと述べている。"),
                 ("The writer wants the cafeteria to stop the meat-free day.", "第4段落で、よい出発点だと述べ、改善を提案している。")],
         summary="食堂の水曜の肉なしの日は、環境への負担や費用を減らせる一方、空腹を訴える生徒や売上の減少もある。筆者は生徒の意見を取り入れて献立を改善すべきだと考えている。",
         skeys=[("肉なしの日の利点（環境・費用）を述べている", 3), ("空腹や売上減少などの問題に触れている", 2), ("生徒の意見を取り入れて献立を改善すべきだという主張でまとめている", 3)],
         wrong_sum=[("水曜日の食堂の費用は、ほかの日より約10%低い。", "第2段落の数値（具体的な根拠）だけで、筆者の主張（献立を改善して続けるべきだ）が入っていない。"),
                    ("水曜日に空腹を感じる生徒が多く、売上も減ったので、肉なしの日はやめるべきだ。", "第3段落の however 以下の問題点を主張と取り違えており、筆者の結論（よい出発点で、改善すべきだ）と逆になっている。")]),
    dict(key="PHON", title="Smartphones as Learning Tools",
         paras=["Until recently, students at our school had to keep their smartphones in their bags during class. Last year, however, the school began allowing students to use their phones in some lessons to look up information and take photos of their work.",
                "Teachers have noticed some benefits. According to a survey of 30 teachers, 21 said that students can now find information more quickly during group work. Students can also record experiments in science class and watch them again later.",
                "Of course, phones can also be a distraction. Some students check messages or play games when they should be studying, and a few teachers say it is hard to see what every student is doing on a small screen.",
                "Therefore, clear rules are necessary. In my opinion, phones should be used only when the teacher says so, and students should help make the rules. Used in the right way, a smartphone can be a useful tool rather than a problem."],
         main="Smartphones can be useful learning tools if clear rules, made with students, are followed.",
         main_wrong=[("Students can record science experiments and watch them later.", "narrow"),
                     ("Technology has changed the way people live and work.", "broad"),
                     ("Phones should be banned in class because some students play games.", "contra")],
         title_ok="Smartphones in Class: Useful, With Clear Rules",
         title_wrong=[("Recording Science Experiments", "narrow"), ("The Best Games for Students", "off"), ("Why Phones Must Stay in Bags", "contra")],
         facts=["The school began allowing phones in some lessons last year.", "In the survey, 21 of the 30 teachers said students find information more quickly.",
                "Some students check messages when they should be studying."],
         opinions=["Clear rules are necessary.", "Phones should be used only when the teacher says so.",
                   "Students should help make the rules."],
         trues=["Before the change, students had to keep their phones in their bags during class.", "More than half of the teachers in the survey noticed that students found information more quickly.",
                "The writer thinks students should take part in making the rules."],
         falses=[("Students can now use their phones whenever they want.", "使えるのは一部の授業で、筆者は教師の指示があるときだけにすべきだと述べている。"),
                 ("All of the teachers in the survey said phones were helpful.", "情報を速く見つけられると答えたのは30人中21人である。"),
                 ("The writer thinks smartphones are only a problem in class.", "第4段落で、正しく使えば役に立つ道具になると述べている。"),
                 ("Teachers find it easy to see what every student is doing on a phone.", "第3段落で、小さな画面では把握が難しいと言う教師がいると述べている。")],
         summary="授業でのスマートフォン利用は情報検索や実験の記録に役立つ一方、気が散る原因にもなる。筆者は生徒も加わって明確なルールを作れば、有用な学習道具になると考えている。",
         skeys=[("スマートフォン利用の利点を述べている", 3), ("気が散るなどの問題に触れている", 2), ("生徒も加わった明確なルールが必要だという主張でまとめている", 3)],
         wrong_sum=[("理科の授業では、スマートフォンで実験を録画してあとで見返すことができる。", "第2段落の具体例だけで、筆者の主張（明確なルールのもとで使えば有用だ）が入っていない。"),
                    ("授業中にゲームをする生徒もいるので、スマートフォンは授業で使わせるべきではない。", "第3段落の Of course 以下で認めた問題点を主張と取り違えており、筆者の結論と逆になっている。")]),
    dict(key="ELDR", title="Learning From Older Neighbors",
         paras=["Many young people today rarely talk with elderly people outside their own families. To change this, our school started an exchange program with a nearby care home two years ago. Once a month, about 20 students visit the home and spend an afternoon with the residents.",
                "The program has had clear results. The students learn traditional games and songs, and the residents often share stories about how the town looked 60 years ago. In a survey after the first year, 90% of the participating students said they wanted to continue.",
                "Still, the program is not easy to run. Students are busy with club activities and tests, so it is sometimes hard to find enough volunteers. Some students also feel nervous because they do not know what to talk about.",
                "I think schools in other areas should also try programs like this. Short guides with conversation topics could help nervous students, and even one visit a month can build a bridge between generations."],
         main="Exchange programs with older people benefit both generations, and other schools should try them too.",
         main_wrong=[("Students learn traditional games at the care home.", "narrow"),
                     ("The number of elderly people is increasing in many countries.", "broad"),
                     ("The program should end because it is hard to find volunteers.", "contra")],
         title_ok="Building Bridges Between Generations",
         title_wrong=[("Traditional Games for Children", "narrow"), ("How to Pass Your Tests", "off"), ("Too Busy to Volunteer", "contra")],
         facts=["The school started the exchange program two years ago.", "About 20 students visit the care home once a month.",
                "In the survey, 90% of the participating students said they wanted to continue."],
         opinions=["Schools in other areas should also try programs like this.", "Short guides with conversation topics could help nervous students.",
                   "Even one visit a month can build a bridge between generations."],
         trues=["Students visit the care home once a month.", "Some students do not know what to talk about with the residents.",
                "The writer suggests making guides to help nervous students."],
         falses=[("The residents teach the students how to use smartphones.", "住民が教えるのは昔の遊びや歌、町の昔の話である。"),
                 ("Fewer than half of the students wanted to continue the program.", "90%が続けたいと答えている。"),
                 ("It is always easy to find enough volunteers.", "第3段落で、ボランティアを集めるのが難しいことがあると述べている。"),
                 ("The writer thinks the program is useful only for students.", "住民も話を伝える機会を得ており、筆者は世代をつなぐ取り組みとして評価している。")],
         summary="高齢者施設との交流で、生徒は昔の遊びや町の歴史を学び、多くが継続を望んでいる。人集めなどの課題はあるが、筆者は他の学校もこうした取り組みを行うべきだと考えている。",
         skeys=[("交流で生徒が得ているもの・成果を述べている", 3), ("人集めや緊張などの課題に触れている", 2), ("他の学校も取り組むべきだという主張でまとめている", 3)],
         wrong_sum=[("生徒は高齢者施設で昔の遊びや歌を教わり、住民からは60年前の町の様子を聞く。", "第2段落の具体的な活動内容だけで、筆者の主張（他の学校も行うべきだ）が入っていない。"),
                    ("生徒は部活動や試験で忙しく、話題に困る生徒もいるので、交流活動は続けにくい。", "第3段落の Still 以下の課題を主張と取り違えており、筆者の結論と逆になっている。")]),
    dict(key="SHOP", title="Bringing Life Back to the Shopping Street",
         paras=["The old shopping street near our station used to be full of people. Today, however, 12 of its 40 shops are closed, and many residents drive to a large shopping mall instead. Some people say the street has no future.",
                "Last year, a group of high school students decided to help. With the shop owners, they held a monthly market where local farmers sell vegetables and students sell handmade goods. They also made a map of the street and shared it online.",
                "The market has brought more visitors. The shop owners counted about 1,500 people at the market in March, compared with about 600 on ordinary weekends. However, the number of visitors on other days has not changed much.",
                "I believe the students' work shows that the street still has value. To keep it alive, the town should support events like the market and help new shops open in the empty buildings."],
         main="The students' market shows the old street still has value, and the town should help keep it alive.",
         main_wrong=[("About 1,500 people came to the market in March.", "narrow"),
                     ("Large shopping malls are popular in many countries.", "broad"),
                     ("The shopping street has no future because visitors did not increase on other days.", "contra")],
         title_ok="A Second Chance for an Old Street",
         title_wrong=[("How to Make Handmade Goods", "narrow"), ("The Largest Mall in Town", "off"), ("A Street With No Future", "contra")],
         facts=["Twelve of the 40 shops on the street are closed.", "About 1,500 people came to the market in March.",
                "The students made a map of the street and shared it online."],
         opinions=["The students' work shows that the street still has value.", "The town should support events like the market.",
                   "The town should help new shops open in the empty buildings."],
         trues=["Some shops on the street are no longer open.", "The market attracted more people than an ordinary weekend.",
                "The writer thinks the town should help new shops open."],
         falses=[("All of the shops on the street are now closed.", "閉まっているのは40店のうち12店である。"),
                 ("The number of visitors increased on every day of the week.", "第3段落で、市の日以外の来訪者はあまり変わっていないと述べている。"),
                 ("The students held the market without the shop owners.", "店主たちと一緒に開いている。"),
                 ("The writer agrees that the street has no future.", "第4段落で、商店街にはまだ価値があると述べている。")],
         summary="さびれた商店街で高校生が店主と月1回の市を開き、来訪者を増やした。ふだんの日の客はあまり増えていないが、筆者は町が催しや新しい店の開業を支援すべきだと考えている。",
         skeys=[("高校生の市の取り組みとその成果を述べている", 3), ("ふだんの日の客が増えていないという限界に触れている", 2), ("町が支援すべきだという主張でまとめている", 3)],
         wrong_sum=[("3月の市には約1,500人が訪れ、ふだんの週末の約600人より多かった。", "第3段落の数値（具体的な根拠）だけで、筆者の主張（町が支援すべきだ）が入っていない。"),
                    ("市の日以外の客は増えていないので、商店街にはやはり将来がない。", "第3段落の However 以下の限界と第1段落の一部の人の見方を主張と取り違えており、筆者の結論と逆になっている。")]),
]
PBY = {p["key"]: p for p in PASSAGES}

MAIN_WHY = {
    "narrow": ("本文の一部（具体例や数値）だけを述べており、文章全体の主旨としては狭すぎる。", "具体例と主旨の混同"),
    "broad": ("本文の話題より広すぎる一般論で、筆者の主張を表していない。", "話題と主旨の混同"),
    "contra": ("本文の主張と逆である。筆者が認めた問題点（譲歩）を主張と取り違えている。", "譲歩と主張の混同"),
    "off": ("本文で扱われていない内容である。", "本文にない情報の読みこみ"),
}


def pstim(p):
    return stim(f"RD-{p['key']}", "\n\n".join(p["paras"]), "passage", f"次の記事（“{p['title']}”）を読んで、あとの問いに答えなさい。", source="オリジナル（調査の数値は架空）")


def head(p):
    return f"記事“{p['title']}”について答えなさい。"


# ======================================================================
# 2人の筆者の意見（複数テクスト）
# ======================================================================

PAIRS = [
    dict(key="HW", topic="週末の宿題",
         a="Writer A: I think teachers should give homework on weekends. If students do not study for two days, they forget what they learned during the week. A small amount of homework, about 30 minutes a day, helps students keep a good study habit.",
         b="Writer B: Weekends should be free from homework. Students need time to rest, spend time with their families, and follow their own interests. Of course, regular study is important, but students can learn to plan it by themselves.",
         pa="週末にも宿題を出すべきだ（2日間学習しないと忘れてしまうので、少量の宿題で学習習慣を保てる）",
         pb="週末は宿題をなくすべきだ（休息・家族との時間・自分の興味のための時間が必要で、学習は自分で計画できる）",
         common="定期的に学習する習慣が大切だという点", opinion="I agree with Writer B. On weekends I study by myself, and I can choose what I need to review."),
    dict(key="UNI", topic="制服と私服",
         a="Writer A: School uniforms are useful. Students do not have to choose what to wear every morning, and families can save money on clothes. Uniforms also help students focus on their studies rather than on fashion.",
         b="Writer B: Students should be allowed to wear their own clothes. Choosing clothes is a way to express yourself, and some uniforms are uncomfortable in hot weather. Uniforms are also expensive to buy at first.",
         pa="制服はよい（毎朝服を選ばずにすみ、学業に集中でき、服の費用も節約できる）",
         pb="私服を認めるべきだ（服選びは自己表現であり、制服は暑さの中で不快で、最初の購入費も高い）",
         common="服にかかる費用を気にしている点（家計への負担を判断の材料にしている点）", opinion="I agree with Writer A because I do not want to spend time choosing clothes every morning."),
    dict(key="ABR", topic="留学の時期",
         a="Writer A: High school is the best time to study abroad. Young students pick up a new language quickly, and living with a host family teaches them a lot about another culture. Even a short stay of a few weeks can change how they see the world.",
         b="Writer B: It is better to study abroad after entering university. Students can choose a program that matches their major, and they are more independent. A high school student may also fall behind in classes at home.",
         pa="高校時代が留学に最適だ（言語を早く身につけ、ホームステイで異文化を学べる）",
         pb="大学に入ってから留学するほうがよい（専攻に合ったプログラムを選べ、自立もしており、高校の授業に遅れる心配もない）",
         common="海外で学ぶ経験そのものには価値があるという点", opinion="I agree with Writer A. A short stay in high school would give me a reason to study English harder."),
    dict(key="AI", topic="英語の宿題での翻訳ツールの利用",
         a="Writer A: Students should be allowed to use translation tools for English homework. These tools show natural expressions, and students can compare them with their own sentences. Learning to use such tools well is also a skill for the future.",
         b="Writer B: Translation tools should not be used for English homework. If students just copy the results, they do not think about grammar or words. Homework is a chance to practice, not to produce perfect sentences.",
         pa="英語の宿題で翻訳ツールを使ってよい（自然な表現を学び、自分の英文と比べられ、道具を使いこなす力も将来役立つ）",
         pb="英語の宿題で翻訳ツールを使うべきではない（結果を写すだけでは文法や語を考えず、宿題は練習の機会だから）",
         common="生徒が自分の英文について考えることが大切だという点", opinion="I agree with Writer A, but only if students write their own sentences first and then compare them."),
]


# ======================================================================
# 講座の予定表（情報検索）
# ======================================================================

WORKSHOPS = [
    ("Pottery for Beginners", "Saturday", 10 * 60, 12 * 60, "Beginners", 1500),
    ("Advanced Pottery", "Saturday", 13 * 60, 16 * 60, "Experienced", 2000),
    ("Bread Baking", "Saturday", 14 * 60, 16 * 60, "Beginners", 1200),
    ("Watercolor Painting", "Sunday", 9 * 60 + 30, 11 * 60 + 30, "Beginners", 1000),
    ("Photography Walk", "Sunday", 13 * 60, 15 * 60 + 30, "All levels", 800),
    ("Guitar Basics", "Sunday", 15 * 60, 17 * 60, "Beginners", 1000),
    ("Advanced Guitar", "Sunday", 10 * 60, 12 * 60, "Experienced", 1500),
]


def hm(m):
    return f"{m // 60}:{m % 60:02d}"


def ws_table():
    return table([[n, d, f"{hm(s)}–{hm(e)}", lv, yen(fee)] for n, d, s, e, lv, fee in WORKSHOPS],
                 header=["Workshop", "Day", "Time", "Level", "Fee"], caption="Hikari Community Center — Weekend Workshops")


def ws_fail(w, day, t0, t1, lv, budget):
    n, d, s, e, wl, fee = w
    out = []
    if d != day:
        out.append(f"{d} の講座で、曜日が合わない")
    elif s < t0 or e > t1:
        out.append(f"時間が {hm(s)}–{hm(e)} で、空いている時間（{hm(t0)}–{hm(t1)}）に収まらない")
    if wl != "All levels" and wl != lv:
        out.append(f"対象が {wl} で、条件に合わない")
    if fee > budget:
        out.append(f"参加費が {yen(fee)} で予算を超える")
    return out


# ======================================================================
# 料金計算のシナリオ（正答と、典型的な誤りの計算）
# ======================================================================

def museum_case(r):
    if r.random() < 0.5:
        a, h, c = r.randint(1, 2), r.randint(8, 12), 0
        who = f"{a} teacher{'s' if a > 1 else ''} and {h} high school students"
    else:
        a, h, c = r.randint(1, 3), r.randint(0, 2), r.randint(1, 3)
        who = f"a family of {a} adult{'s' if a > 1 else ''}, {h} high school student{'s' if h != 1 else ''}, and {c} child{'ren' if c > 1 else ''} in elementary school"
        if h == 0:
            who = f"a family of {a} adult{'s' if a > 1 else ''} and {c} child{'ren' if c > 1 else ''} in elementary school"
    n = a + h + c
    pl_mode = r.choice(["all", "none", "adults"])
    pl = {"all": n, "none": 0, "adults": a}[pl_mode]
    pl_txt = {"all": "All of them will watch the planetarium show.", "none": "None of them will watch the planetarium show.",
              "adults": f"Only the adult{'s' if a > 1 else ''} will watch the planetarium show."}[pl_mode]
    adm = a * MU_AD + h * MU_HS
    disc = n >= MU_GROUP
    adm_pay = adm * 9 // 10 if disc else adm
    total = adm_pay + pl * MU_PL
    story = f"{who[0].upper()}{who[1:]} will visit the Summer Night Program. {pl_txt} How much will they pay in total?"
    f_adm = f"{MU_AD}×{a}" + (f"＋{MU_HS}×{h}" if h else "")
    f_ok = f"入館料（{f_adm}）{'×0.9' if disc else ''}＝{adm_pay}、プラネタリウム {MU_PL}×{pl}＝{pl * MU_PL}、合計 {total}"
    wr = []
    if disc:
        wr.append(((adm + pl * MU_PL) * 9 // 10, "割引をプラネタリウム料金にも適用している。割引は入館料だけである。", "割引の適用範囲の読み落とし",
                   f"（入館料{adm}＋プラネタリウム{pl * MU_PL}）×0.9", "割引をかける範囲", "condition"))
        wr.append((adm + pl * MU_PL, f"{n}人は10人以上なので、入館料は10%引きになる。", "団体割引の条件の見落とし",
                   f"入館料{adm}＋プラネタリウム{pl * MU_PL}（割引なし）", "団体割引の判定", "condition"))
    else:
        if pl:
            wr.append((adm * 9 // 10 + pl * MU_PL, f"{n}人では10人に満たないので、団体割引は使えない。", "団体割引の条件の誤読",
                       f"入館料{adm}×0.9＋プラネタリウム{pl * MU_PL}", "団体割引の判定", "condition"))
    if c:
        adm2 = a * MU_AD + (h + c) * MU_HS
        wr.append(((adm2 * 9 // 10 if disc else adm2) + pl * MU_PL, "中学生以下は入館無料である。小学生に高校生料金をかけている。", "無料の区分の見落とし",
                   f"小学生も{MU_HS}円として入館料{adm2}{'×0.9' if disc else ''}＋プラネタリウム{pl * MU_PL}", "子どもの料金区分", "condition"))
    if pl:
        wr.append((adm_pay, "プラネタリウムは入館料とは別料金（in addition to admission）である。", "追加料金の見落とし",
                   f"入館料{adm_pay}のみ", "プラネタリウム料金の加算", "interpretation"))
    else:
        wr.append((adm_pay + n * MU_PL, "プラネタリウムを見ないので、その料金は不要である。", "条件の読み落とし",
                   f"入館料{adm_pay}＋プラネタリウム{MU_PL}×{n}", "プラネタリウム料金の加算", "interpretation"))
    chk = f"{'(' if disc else ''}{MU_AD}*{a}+{MU_HS}*{h}{')*9/10' if disc else ''}+{MU_PL}*{pl}"
    return dict(key="MUSEUM", story=story, total=total, f_ok=f_ok, wrongs=wr, chk=chk,
                cond="団体（10人以上、子どもも含む）の割引は入館料だけ、中学生以下は入館無料、プラネタリウムは見る人だけ1人300円の別料金")


def pool_case(r):
    a, s = r.randint(1, 2), r.randint(0, 2)
    ages = sorted(r.sample([3, 4, 5, 6, 7, 9, 11, 13, 14], r.randint(1, 3)))
    day = r.choice(["Tuesday", "Thursday", "Saturday", "Sunday"])
    we = day in ("Saturday", "Sunday")
    up = PO_WE if we else 0
    kids = [x for x in ages if x >= 6]
    small = [x for x in ages if x < 6]
    total = a * (PO_AD + up) + s * (PO_ST + up) + len(kids) * (PO_CH + up)
    ages_txt = ' and '.join(map(str, ages)) if len(ages) <= 2 else ', '.join(map(str, ages[:-1])) + ', and ' + str(ages[-1])
    kids_txt = f"{len(ages)} child{'ren' if len(ages) > 1 else ''} aged {ages_txt}"
    if s:
        who = f"{a} adult{'s' if a > 1 else ''}, {s} high school student{'s' if s > 1 else ''}, and {kids_txt}"
    else:
        who = f"{a} adult{'s' if a > 1 else ''} and {kids_txt}"
    story = f"A family of {who} will go to the pool on a {day}. How much will they pay in total?"
    f_ok = (f"大人 {PO_AD + up}×{a}" + (f"＋学生 {PO_ST + up}×{s}" if s else "") + f"＋6〜15歳 {PO_CH + up}×{len(kids)}" +
            (f"＋6歳未満 0×{len(small)}" if small else "") + f"＝{total}")
    wr = []
    if we:
        wr.append((total - up * (a + s + len(kids)), f"{day} は週末なので、6歳未満以外は100円高くなる。", "曜日による料金の違いの見落とし",
                   "平日料金で計算", "曜日の確認", "condition"))
        if small:
            wr.append((total + up * len(small), "6歳未満は週末も無料（always free）である。", "例外の読み落とし",
                       "6歳未満にも100円を加算", "6歳未満の扱い", "condition"))
    else:
        wr.append((total + PO_WE * (a + s + len(kids)), f"{day} は平日なので、100円の加算はない。", "曜日による料金の違いの取り違え",
                   "週末料金で計算", "曜日の確認", "condition"))
    if small:
        wr.append((total + len(small) * (PO_CH + up), "6歳未満の子どもは無料である。", "無料の区分の見落とし",
                   "6歳未満にも子ども料金をかけた", "子どもの年齢区分", "condition"))
    if 6 in ages:
        wr.append((total - (PO_CH + up), "6歳は「6歳から15歳」に含まれるので、子ども料金がかかる。", "境界の年齢の扱いの誤り",
                   "6歳を無料とした", "年齢の境界", "condition"))
    if s:
        wr.append((total + s * (PO_AD - PO_ST), "高校生には学生料金がある（学生証の提示が必要）。", "料金区分の見落とし",
                   "高校生を大人料金で計算", "学生料金の区分", "condition"))
    else:
        wr.append((total + PO_CH, "家族の人数を数え間違えている。区分ごとに人数を確認する。", "人数の数え間違い",
                   "子どもを1人多く数えた", "人数の確認", "calculation"))
    chk = f"{a}*({PO_AD}+{up})+{s}*({PO_ST}+{up})+{len(kids)}*({PO_CH}+{up})"
    return dict(key="POOL", story=story, total=total, f_ok=f_ok, wrongs=wr, chk=chk,
                cond="週末・祝日は100円高い（6歳未満は常に無料）、6〜15歳は子ども料金、高校生は学生料金")


def bike_cost(kind, mins):
    rate, day = (BK_STD, BK_STD_DAY) if kind == "standard" else (BK_ELE, BK_ELE_DAY)
    hours = -(-mins // 60)
    return min(hours * rate, day), hours, rate, day


def bike_case(r):
    ns, ne = r.choice([(2, 0), (0, 2), (1, 1), (2, 1), (1, 2), (3, 0), (0, 3)])
    mins = r.choice([70, 100, 130, 150, 200, 230, 250, 280, 310, 370])
    cs, hrs, _, _ = bike_cost("standard", mins)
    ce, _, _, _ = bike_cost("electric", mins)
    total = ns * cs + ne * ce
    h, m = divmod(mins, 60)
    bikes = " and ".join(x for x in [f"{ns} standard bike{'s' if ns > 1 else ''}" if ns else "", f"{ne} electric bike{'s' if ne > 1 else ''}" if ne else ""] if x)
    story = f"A group of friends will rent {bikes} for {h} hour{'s' if h > 1 else ''} and {m} minutes. They choose the cheapest way to pay for each bike. How much will they pay in total?"
    f_ok = f"利用時間は{hrs}時間分。標準 min({BK_STD}×{hrs}, {BK_STD_DAY})＝{cs}、電動 min({BK_ELE}×{hrs}, {BK_ELE_DAY})＝{ce}。合計 {cs}×{ns}＋{ce}×{ne}＝{total}"
    wr = []
    fl = mins // 60
    v1 = ns * min(fl * BK_STD, BK_STD_DAY) + ne * min(fl * BK_ELE, BK_ELE_DAY)
    wr.append((v1, f"始まった1時間ごとに料金がかかるので、{h}時間{m}分は{hrs}時間分である。", "端数の時間の切り捨て",
               f"{fl}時間分で計算", "時間の数え方", "condition"))
    v2 = ns * hrs * BK_STD + ne * hrs * BK_ELE
    wr.append((v2, "1日パスのほうが安い場合はパスを選ぶ（最も安い方法を選ぶ条件）。", "最安の方法の比較忘れ",
               "すべて時間料金で計算", "料金の比較", "condition"))
    v3 = ns * BK_STD_DAY + ne * BK_ELE_DAY
    wr.append((v3, "時間料金のほうが安い場合もある。自転車の種類ごとに比べる。", "最安の方法の比較忘れ",
               "すべて1日パスで計算", "料金の比較", "condition"))
    v4 = ns * min(hrs * BK_ELE, BK_ELE_DAY) + ne * min(hrs * BK_STD, BK_STD_DAY)
    wr.append((v4, "標準と電動の料金を取り違えている。", "表の行の読み違い",
               "標準と電動の料金を入れかえた", "料金表の読み取り", "interpretation"))
    chk = f"{ns}*Min({BK_STD}*ceiling(Rational({mins},60)),{BK_STD_DAY})+{ne}*Min({BK_ELE}*ceiling(Rational({mins},60)),{BK_ELE_DAY})"
    return dict(key="BIKE", story=story, total=total, f_ok=f_ok, wrongs=wr, chk=chk,
                cond="時間料金は始まった1時間ごと、自転車ごとに時間料金と1日パスの安い方を選ぶ")


CASES = [museum_case, pool_case, bike_case]


def clean_wrongs(case):
    seen, out = {case["total"]}, []
    for w in case["wrongs"]:
        if w[0] not in seen and w[0] > 0:
            seen.add(w[0])
            out.append(w)
    return out


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["広告・掲示・予定表などの資料から、設問に必要な情報だけを素早く探し出し、条件（割引・例外・期限）をもれなく適用できる。",
           "文が事実（fact）か意見（opinion）かを、確かめられるかどうか・判断や評価を表す語の有無から区別できる。",
           "論説文の段落の役割（問題提起・根拠・譲歩・結論）をつかみ、筆者の主張を選択肢や日本語の要旨で正確に表せる。"],
    duration=50,
    readiness=["中学で学んだ時刻・金額・日付の英語表現（a.m. / p.m.、10% off、by June 1 など）を読める。",
               "パラグラフの主題文とディスコースマーカー（however / on the other hand / therefore）の働きを知っている（HS-ENG-U09）。",
               "比較級・最上級（more ～ than、the most ～）を使った文の意味を取れる（HS-ENG-U07）。"],
    flow=[("導入：共通テストの読み方", 5, "全文を訳さず「設問 → 本文の該当箇所」の順に読む方針と、80分の時間配分の考え方を示す"),
          ("情報の検索", 13, "設問の先読みとスキャニング、条件つき料金計算の手順を例題1で練習する"),
          ("事実と意見", 12, "確かめられるかどうかの基準と、意見を示す語のリストを確認し、例題2で判定する"),
          ("要旨と選択肢の吟味", 14, "段落の役割から主張をつかみ、誤りの選択肢の4類型で選択肢を吟味する（例題3）"),
          ("まとめと確認", 6, "確認問題3問、時間配分の目安と問題プリントの取り組み方の指示")],
    sections=[
        intro("in1", "共通テストのリーディングは「速く・正確に・根拠をもって」読む試験",
              "大学入学共通テストの英語リーディングは、試験時間80分のなかで、広告・掲示・ウェブページ・ブログ・記事・論説文など、種類の違う英文を数多く読ませる。すべての英文を日本語に訳していては時間が足りない。設問が求める情報を本文から探す読み方（情報の検索）と、文章全体の主張をつかむ読み方（要旨把握）を、資料の種類に応じて使い分けることが得点の鍵になる。",
              bullets=["短い資料（広告・掲示）：設問を先に読み、必要な数字・条件だけを探す（scanning）。",
                       "論説文：各段落の最初と最後、ディスコースマーカーを手がかりに全体の流れをつかむ（skimming）。",
                       "選択肢は本文の言いかえ（paraphrase）で作られる。同じ語句があるかどうかではなく、意味が同じかどうかで照合する。"],
              points=[tp("「全文を訳してから設問を解く」読み方と「設問を先に読む」読み方で、同じ広告の問題を解く時間を比べさせる。", ask="設問を先に読むと、本文のどこを読めばよいかがどう変わるか。",
                         expect="探す情報（料金・時刻・条件）が決まるので、関係のない部分を読み飛ばせる。", timing="導入の冒頭"),
                      tp("時間配分は「短い資料に時間をかけすぎない」ことが第一。迷った設問には印をつけて先へ進み、最後に戻る習慣をつけさせる。",
                         caution="序盤の広告問題で計算に時間をかけすぎ、後半の長い論説文を読み切れない受験生が多い。")]),
        definition("df1", "情報の検索と、事実・意見の区別",
                   "情報の検索とは、設問が求める情報（数値・日時・条件・人物の行動など）を本文から探し出し、設問の状況に当てはめることである。事実（fact）とは、資料・記録・観察によって正しいかどうかを確かめられる内容であり、意見（opinion）とは、書き手の判断・評価・推測・提案で、人によって考えが分かれうる内容である。",
                   bullets=["事実の手がかり：数値・割合（68%、12,000 times）、日時（since July 2020）、実際に起きた出来事（was held / started）。",
                            "意見の手がかり：I think / I believe / In my opinion、should / must / ought to、評価の形容詞（best, great, smart, delicious）、推測（probably, will surely, seem）。",
                            "注意：数値を含んでいても、too short / too expensive のような評価があれば意見である。"],
                   conditions=["「調査で〇%が～と答えた」は、答えの内容が意見でも、そう答えたという事実を述べた文である。",
                               "意見を示す語がなくても、the most beautiful のように主観的な評価を含む文は意見である。"],
                   points=[tp("事実と意見の判定を「辞書・記録・数えることで確かめられるか」という一つの問いにまとめて言わせる。", ask="“The fireworks started at 8:00 p.m.” は確かめられるか。",
                              expect="記録で確かめられるので事実。"),
                           tp("“I think 40 minutes is too short.” を板書し、数値を含むのに意見であることを示す。", caution="数値があれば事実、と機械的に判断する生徒が多い。")]),
        theorem("th1", "誤りの選択肢の4類型",
                "① 本文と逆（not の有無、増加と減少、賛成と反対の入れかえ）　② 本文に書かれていない（もっともらしいが根拠がない）　③ 言いすぎ（all / always / only / never で範囲を広げる）　④ ずれ（本文の別の箇所の語句を組み合わせる、具体例だけ・一部だけを主旨とする）",
                ["正解の選択肢は、本文の語句を別の表現に言いかえていることが多い。",
                 "本文と同じ語句を多く含む選択肢ほど、④のずれの可能性を疑う。",
                 "主旨を問う設問では、狭すぎる（具体例のみ）・広すぎる（一般論）・逆（譲歩部分）の3つを消去する。"],
                body="共通テストの選択肢は、本文の一部を少しだけ変えて作られる。誤りの型を知っていれば、「なんとなく合っていそう」な選択肢を根拠をもって消去できる。",
                points=[tp("同じ本文から4類型の誤り選択肢を1つずつ生徒に作らせると、出題者の視点が身につく。", ask="“The number of late students dropped.” を「言いすぎ」の誤りに変えるとどうなるか。",
                           expect="“No students arrived late.” など、all / no を使って範囲を広げる。")]),
        derivation("dv1", "条件つきの情報検索の手順（なぜ「条件」を先に書き出すのか）",
                   ["① 設問を読み、求めるもの（合計金額・参加できる講座・期限など）と、登場人物の状況（人数・年齢・曜日・空き時間）を書き出す。",
                    "② 資料の中から、求めるものに関わる行（料金表・時刻表）を探す。",
                    "③ 同じ資料の注意書き（except / only / in addition / does not apply / must など）を探し、①の状況に当てはまる条件を選ぶ。",
                    "④ 条件を当てはめてから計算・判定する。人数は区分ごとに数え、割引をかける範囲を確かめる。",
                    "⑤ 誤りの選択肢は、条件を1つ忘れたときの値で作られている。自分の答えが選択肢にあっても、条件をすべて使ったかを見直す。"],
                   body="共通テストの資料問題では、料金表そのものよりも、その下の小さな注意書きが正誤を分ける。条件を書き出してから計算すれば、「条件を1つ忘れた値」という誤りの選択肢に引っかからない。だから、本文を読む前に状況を整理し、本文では条件を探しに行く。",
                   points=[tp("手順③の「注意書き」を色ペンで囲ませ、料金表の数字と線で結ばせる。", ask="この広告で、計算結果を変える注意書きはいくつあるか。",
                              expect="割引の人数条件、割引の範囲、無料の区分、別料金の4つ。", timing="例題1の前")]),
        example("ex1", "例題1　条件つきの料金計算（広告）",
                f"次の広告を読み、問いに答えなさい。\n{MUSEUM}\nMr. Sato, a teacher, will take 11 high school students to the Summer Night Program. All of them will watch the planetarium show. How much will they pay in total?",
                ["状況：大人1人＋高校生11人＝12人。全員がプラネタリウムを見る。",
                 f"入館料：{MU_AD}×1＋{MU_HS}×11＝8,900円。12人は10人以上なので10%引き：8,900×0.9＝8,010円。",
                 f"プラネタリウム：割引の対象外なので {MU_PL}×12＝3,600円。",
                 "合計：8,010＋3,600＝11,610円。"],
                "11,610 yen",
                thinking="注意書きの「10人以上で10%引き」「割引はプラネタリウムには適用しない」の2つの条件を、計算の前に確認する。",
                points=[tp("割引をプラネタリウムにもかけた値（11,250円）と、割引を忘れた値（12,500円）が誤りの選択肢として並ぶことを示す。",
                           ask="11,250円を選んだ人は、どの条件を読み落としたか。", expect="The discount does not apply to planetarium tickets.")],
                misconceptions=[("割引を合計金額全体にかけて 11,250円とする。", "割引は入館料だけ。プラネタリウムは 300円×12人をそのまま足す")]),
        example("ex2", "例題2　事実と意見の区別",
                "次のうち、意見（opinion）ではなく事実（fact）を述べた文を選びなさい。\n(a) The cafeteria should stay open after school.\n(b) The cafeteria serves about 300 lunches a day.\n(c) The new curry is the most delicious dish on the menu.\n(d) I believe students eat too quickly at lunchtime.",
                ["(a) should はあるべき姿の主張 → 意見。", "(b) 1日の提供数は記録で確かめられる → 事実。",
                 "(c) the most delicious は主観的な評価 → 意見。", "(d) I believe と too quickly → 意見。"],
                "(b)",
                thinking="それぞれの文について「記録や数えることで確かめられるか」を問う。should・最上級の評価・I believe は意見の手がかり。",
                points=[tp("(c) を「最上級だから事実」と考える生徒がいる。最上級でも、何をもって最もおいしいかは人によって違うことを確認する。")]),
        example("ex3", "例題3　論説文の主旨",
                f"次の記事を読み、筆者の主張として最も適切なものを選びなさい。\n{chr(10).join(PBY['LATE']['paras'])}\n(a) {PBY['LATE']['main_wrong'][0][0]}\n(b) {PBY['LATE']['main']}\n(c) {PBY['LATE']['main_wrong'][2][0]}\n(d) {PBY['LATE']['main_wrong'][1][0]}",
                ["第1段落：睡眠不足の調査結果と「始業を遅らせる」という提案（問題提起）。", "第2段落：賛成派の根拠と1校の試み（根拠・具体例）。",
                 "第3段落：However で問題点を示す（譲歩）。", "第4段落：In my view で筆者の主張（試す価値はあるが、まず話し合うべきだ）。",
                 "(a) は具体例だけ（狭すぎる）、(c) は譲歩部分を主張と取り違えた逆の内容、(d) は一般論（広すぎる）。"],
                "(b)",
                thinking="In my view / I believe / I think など筆者の意見を示す表現のある段落が、主張の中心になる。However の段落は筆者が認めた問題点である。",
                points=[tp("(c) を選んだ答案を取り上げ、「筆者は問題点を認めたうえで、結論で何と言っているか」を問い返す。", ask="第3段落と第4段落の関係は何か。",
                           expect="第3段落で問題を認め（譲歩）、第4段落で自分の主張を述べている。")]),
        board("bd1", "板書案",
              [("① 情報の検索", ["設問を先に読む", "状況を書き出す（人数・曜日・年齢）", "注意書きの条件を探す", "except / only / does not apply", "条件を当てはめてから計算"]),
               ("② 事実と意見", ["事実＝確かめられる", "数値・日時・出来事", "意見＝判断・評価・推測", "should / best / I think / probably", "数値＋too ～ は意見"]),
               ("③ 要旨と選択肢", ["段落の役割を書きこむ", "However の段落＝譲歩", "In my view の段落＝主張", "誤り：逆・書いていない・言いすぎ・ずれ", "主旨：狭い・広い・逆を消す"])],
              points=[tp("①の「注意書きの条件」は、例題1の広告から実際に抜き出した英語を板書に残す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("料金計算は、選択肢を見る前に自分で計算させる。選択肢を先に見ると、条件を1つ忘れた値に引きずられる。", caution="計算結果が選択肢にあるだけで安心しないよう指導する。"),
               tp("事実と意見の問題では、選択肢の文の「動詞・助動詞・形容詞」に印をつけさせ、should や評価語の有無を確認させる。", timing="例題2の解説時"),
               tp("内容一致問題では、選択肢ごとに本文の根拠の行番号を書かせる。根拠を示せない選択肢は「書かれていない」として消去する。"),
               tp("論説文の要旨は、譲歩（However / Of course / On the other hand）の段落を主張と取り違える誤りが最も多い。問題プリント D の誤答例で原因を確認する。"),
               tp("時間配分の目安を各自で決めさせ、演習のたびに大問ごとの所要時間を記録させる。", ask="今日の演習で、時間を使いすぎたのはどの資料か。", expect="料金計算の広告、条件の多い予定表など。")],
              misconceptions=[("数値を含む文はすべて事実である。", "too expensive / too short のような評価があれば意見"),
                              ("本文と同じ語句が多い選択肢が正解である。", "正解は言いかえで作られることが多く、同じ語句の多い選択肢は「ずれ」を疑う"),
                              ("However の後ろはいつも筆者の主張である。", "筆者が反対の視点や問題点を認める譲歩の場合もある。結論の段落と合わせて判断する")]),
        summary("sm1", "まとめ",
                ["資料問題：設問 → 状況の書き出し → 注意書きの条件 → 計算・判定の順で、条件をもれなく使う。",
                 "事実は確かめられる内容、意見は判断・評価・推測・提案。should・評価語・I think が手がかり。",
                 "要旨：段落の役割をつかみ、譲歩と主張を区別する。選択肢は「逆・書いていない・言いすぎ・ずれ」で消去する。"]),
        check("ck1", "確認問題",
              [("“Since July 2020, stores in Japan have charged customers for plastic shopping bags.” は事実か意見か。", "事実（時期と出来事は記録で確かめられる）"),
               ("“In my opinion, a one-day pass is a bit expensive.” が意見である手がかりを2つ挙げなさい。", "In my opinion と、評価を表す expensive"),
               ("選択肢に all / always / only が含まれるとき、まず疑うべき誤りの型は何か。", "言いすぎ（本文より範囲を広げている）")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def a_notice_detail(r):
    key = r.choice(list(NOTICES))
    n = NOTICES[key]
    q, ok, wrongs = r.choice(n["qs"])
    return mc(f"掲示“{n['title']}”について答えなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　設問のキーワードに対応する行を掲示から探し、注意書きまで確認する。", d=2, stim=nstim(key),
              ap="設問のキーワード（時刻・場所・条件など）を決めてから、掲示の該当する行だけを読む。",
              steps=["設問が何を求めているか（時刻・場所・条件）を確認する。", "掲示の中からその情報を含む行を探す。", "注意書き（only / except / must など）で答えが変わらないか確かめる。", f"答え：{ok}"],
              alt=["誤りの選択肢が、掲示のどの行の情報を取り違えたものかを確かめて消去する。"],
              pc=[("該当する行を見つけている", 1), ("正しい選択肢を選んでいる", 1)],
              pit=["掲示に出てくる別の時刻・日付（開館時刻・予備日など）を答えてしまう。"], why={w: (why, "資料の別の情報との取り違え") for w, why in wrongs})


@gen("basic_check", 5, ["concept", "condition_check"])
def a_fact_opinion(r):
    scene, facts, ops = r.choice(FO)
    if r.random() < 0.5:
        ok = r.choice(facts)
        wrongs = r.sample(ops, 3)
        why = {s: (op_why(sig), "意見を事実と取り違える") for s, sig in wrongs}
        return mc(f"次の4つの文は、ある高校生が「{scene}」について書いたレポートからとったものである。意見（opinion）ではなく事実（fact）を述べている文を選びなさい。",
                  [ok] + [s for s, _ in wrongs], f"{ok}　{FACT_WHY}", d=2,
                  ap="各文について「記録・資料・数えることで確かめられるか」を問い、should・評価の形容詞・I think などの意見の手がかりを探す。",
                  steps=["各文の動詞・助動詞・形容詞に印をつける。", "should / best / I think / probably などの手がかりがある文を意見として外す。", f"残った文：{ok}"],
                  alt=["正解の文について、どんな資料（記録・調査・時刻表など）で確かめられるかを具体的に言えるかで確認する。"],
                  pc=[("意見の手がかりに気づいている", 1), ("事実の文を選んでいる", 1)],
                  pit=["数値を含む意見文（too short など）を事実と判断する。"], why=why)
    ok, sig = r.choice(ops)
    wrongs = r.sample(facts, 3)
    why = {s: (FACT_WHY + "意見ではない。", "事実を意見と取り違える") for s in wrongs}
    return mc(f"次の4つの文は、ある高校生が「{scene}」について書いたレポートからとったものである。事実（fact）ではなく意見（opinion）を述べている文を選びなさい。",
              [ok] + wrongs, f"{ok}　{op_why(sig)}", d=2,
              ap="判断・評価・推測・提案を表す語（should / best / I think / probably / great など）を探す。",
              steps=["各文の中の評価・判断を表す語を探す。", f"「{sig}」があるのは：{ok}", "ほかの3文は数値・日時・出来事で、確かめられる事実である。"],
              alt=["選んだ文について「人によって考えが分かれるか」を考え、分かれるなら意見と確かめる。"],
              pc=[("意見の手がかりを見つけている", 1), ("意見の文を選んでいる", 1)],
              pit=["数値を含む文をすべて事実として外し、評価語を見落とす。"], why=why)


# 言いかえ：(本文の文, 正しい言いかえ, [(誤り, 理由, 型)])
PARA = [
    ("Tickets are sold at the entrance only.", "You cannot buy tickets anywhere except at the entrance.",
     [("You can buy tickets at the entrance or online.", "only（入口だけ）に反する。", "本文と逆"),
      ("Tickets are free at the entrance.", "無料とは書かれていない。", "本文に書かれていない"),
      ("Everyone must show a ticket at the entrance.", "チケットを入口で見せるという話ではない。", "ずれ")]),
    ("No experience is needed.", "Beginners are welcome.",
     [("Only experienced people can join.", "経験は不要と述べており、逆である。", "本文と逆"),
      ("Experience is helpful but not enough.", "経験が役立つとは書かれていない。", "本文に書かれていない"),
      ("Members will gain a lot of experience.", "経験が得られるという話ではない。", "ずれ")]),
    ("The discount does not apply to planetarium tickets.", "Planetarium tickets are always full price.",
     [("Planetarium tickets are 10% off for groups.", "割引は適用されないので逆である。", "本文と逆"),
      ("Planetarium tickets are not sold to groups.", "団体に売らないとは書かれていない。", "本文に書かれていない"),
      ("Groups get a discount on every ticket.", "every で範囲を広げており、本文より言いすぎである。", "言いすぎ")]),
    ("Trash bags will be provided.", "Participants do not have to bring trash bags.",
     [("Participants must bring their own trash bags.", "主催者が用意するので逆である。", "本文と逆"),
      ("Trash bags will be sold at the event.", "販売するとは書かれていない。", "本文に書かれていない"),
      ("All participants will receive a free towel and bags.", "タオルの情報とごみ袋の情報を組み合わせている。", "ずれ")]),
    ("The number of students who arrived late dropped from 25 to 9.", "Fewer students were late than before.",
     [("More students were late than before.", "dropped（減った）の逆である。", "本文と逆"),
      ("No students were late during the trial.", "9人は遅刻しており、言いすぎである。", "言いすぎ"),
      ("Twenty-five students joined the trial.", "25は遅刻者の数で、参加者数ではない。", "ずれ")]),
    ("Not everyone was happy.", "Some people were not satisfied.",
     [("Nobody was happy.", "not everyone は部分否定で、全員が不満だったわけではない。", "言いすぎ"),
      ("Everyone was happy.", "not everyone の否定を見落としている。", "本文と逆"),
      ("Everyone was too busy to answer.", "忙しくて答えられなかったとは書かれていない。", "本文に書かれていない")]),
    ("It is sometimes hard to find enough volunteers.", "There are times when there are not enough volunteers.",
     [("It is always impossible to find volunteers.", "sometimes を always に変えており、言いすぎである。", "言いすぎ"),
      ("Finding volunteers is never a problem.", "ときどき難しいので逆である。", "本文と逆"),
      ("Volunteers are paid for their work.", "報酬については書かれていない。", "本文に書かれていない")]),
    ("Children under 10 must be with an adult at all times.", "Young children cannot be at the pool alone.",
     [("Children under 10 cannot enter the pool.", "大人と一緒なら入れる。", "本文と逆"),
      ("All children need an adult to buy tickets.", "all children に広げ、チケット購入の話にずれている。", "言いすぎ"),
      ("Adults must swim with children under 15.", "15歳は子ども料金の上限で、同伴の条件ではない。", "ずれ")]),
    ("Producing meat generally uses more land and water than producing vegetables.", "Growing vegetables usually needs less land and water than producing meat.",
     [("Growing vegetables needs more water than producing meat.", "比較の向きが逆である。", "本文と逆"),
      ("Producing meat uses no water at all.", "水を使わないとは書かれていない。", "本文に書かれていない"),
      ("Meat is always more expensive than vegetables.", "値段の比較ではなく、always は言いすぎでもある。", "ずれ")]),
    ("The number of visitors on other days has not changed much.", "On days without the market, the street is about as quiet as before.",
     [("The street is crowded every day now.", "市の日以外は変わっていないので逆である。", "本文と逆"),
      ("No one visits the street on other days.", "来訪者がいないとは書かれておらず、言いすぎである。", "言いすぎ"),
      ("The market is held every day.", "市は月1回である。", "ずれ")]),
]


@gen("basic_check", 5, ["concept", "common_error"])
def a_paraphrase(r):
    src, ok, wrongs = r.choice(PARA)
    return mc(f"次の英文の内容を最も適切に言いかえたものを選びなさい。\n{src}", [ok] + [w for w, _, _ in wrongs],
              f"{ok}　共通テストの正解の選択肢は、本文の語句を別の表現に言いかえて作られる。", d=2,
              ap="本文の文の「肯定・否定」「範囲（only / not everyone / sometimes）」「比較の向き」を確認し、それを保った選択肢を選ぶ。",
              steps=["本文の文の意味を、否定・範囲・比較の向きに注意して確認する。", "各選択肢を、逆・書かれていない・言いすぎ・ずれの4類型で点検する。", f"意味が同じものは：{ok}"],
              alt=["選んだ選択肢を本文の文に戻して置きかえ、同じ状況を表しているかを確かめる。"],
              pc=[("本文の意味（否定・範囲）をとらえている", 1), ("正しい言いかえを選んでいる", 1)],
              pit=["本文と同じ語句を含む選択肢を、意味を確かめずに選ぶ。"], why={w: (f"{why}（{kind}）", kind) for w, why, kind in wrongs})


@gen("basic_check", 5, ["computation", "condition_check"])
def a_schedule(r):
    for _ in range(200):
        tgt = r.choice(WORKSHOPS)
        n, day, s, e, lv, fee = tgt
        t0 = s - r.choice([0, 30, 60])
        t1 = e + r.choice([0, 30, 60])
        plv = "Beginners" if lv in ("Beginners", "All levels") else "Experienced"
        budget = fee + r.choice([0, 200, 500])
        others = [w for w in WORKSHOPS if w != tgt and ws_fail(w, day, t0, t1, plv, budget)]
        if len(others) >= 3:
            break
    picks = r.sample(others, 3)
    name = r.choice(["Mika", "Ken", "Yuna", "Sota", "Aoi", "Riku"])
    he = "She" if name in ("Mika", "Yuna", "Aoi") else "He"
    exp = "has never taken any of these kinds of classes" if plv == "Beginners" else "has several years of experience and wants a class for experienced people"
    stem = (f"次の予定表を読んで答えなさい。\n{name} is free on {day} from {hm(t0)} to {hm(t1)}. {he} {exp}. {he} can spend up to {yen(budget)}. "
            f"Which workshop can {name} join?")
    why = {w[0]: ("；".join(ws_fail(w, day, t0, t1, plv, budget)) + "。", "条件の照合もれ") for w in picks}
    return mc(stem, [n] + [w[0] for w in picks],
              f"{n}（{day} {hm(s)}–{hm(e)}、{lv}、{yen(fee)}）だけが、曜日・時間・対象・予算のすべての条件を満たす。", d=2, tbl=ws_table(),
              ap="人物の条件（曜日・空き時間・経験・予算）を先に書き出し、予定表の行を1行ずつ照合して条件に合わない講座を消していく。",
              steps=[f"条件を書き出す：{day}、{hm(t0)}–{hm(t1)}、{'初心者' if plv == 'Beginners' else '経験者向け希望'}、{yen(budget)}以内。", "曜日の違う講座を消す。",
                     "開始・終了時刻が空き時間に収まらない講座を消す。", "対象レベルと参加費で残りを点検する。", f"すべて満たすのは {n}。"],
              alt=["選んだ講座について、4つの条件を1つずつ「〇」で確認する表を作って見直す。"],
              pc=[("条件をすべて書き出している", 1), ("条件に合う講座を選んでいる", 1)],
              pit=["開始時刻だけを見て、終了時刻が空き時間を超えることを見落とす。", "All levels の講座を初心者が参加できないと考える。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "condition_check"])
def b_price(r):
    case = r.choice(CASES)(r)
    ws = clean_wrongs(case)
    while len(ws) < 3:
        v = case["total"] + 100 * (len(ws) + 1)
        if v not in {w[0] for w in ws}:
            ws.append((v, "人数または単価の数え間違い。区分ごとに人数と単価を確認する。", "計算の誤り", "", "", "calculation"))
    ws = ws[:3]
    return mc(f"掲示“{NOTICES[case['key']]['title']}”について答えなさい。\n{case['story']}", [yen(case["total"])] + [yen(w[0]) for w in ws],
              f"{yen(case['total'])}。{case['f_ok']}（円）。", d=3, stim=nstim(case["key"]),
              ap=f"計算の前に、掲示の注意書きから条件を書き出す（{case['cond']}）。",
              steps=["登場人物を料金区分ごとに数える（曜日・年齢・時間も確認）。", f"注意書きの条件を確認する：{case['cond']}。", f"計算する：{case['f_ok']}。", "選択肢と照合し、条件を1つ忘れた値でないか見直す。"],
              alt=["区分ごとの小計を表にまとめ、合計を足し直して確かめる。"],
              pc=[("料金区分と条件を正しく当てはめている", 2), ("合計金額が正しい", 2)],
              pit=["注意書きの条件を1つ読み落とした値を選ぶ。"], why={yen(w[0]): (w[1], w[2]) for w in ws},
              chk=(case["chk"], str(case["total"]), None, "intermediate"))


@gen("standard_practice", 5, ["concept", "application"])
def b_main_idea(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.5:
        ok, wrongs, what = p["main"], p["main_wrong"], "筆者の主張"
    else:
        ok, wrongs, what = p["title_ok"], p["title_wrong"], "記事の見出し"
    return mc(f"{head(p)}\n{what}として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　筆者の意見を示す最終段落（I believe / In my view / I think）と、問題提起の第1段落を中心に、譲歩の段落と区別して判断する。", d=3, stim=pstim(p),
              ap="各段落の役割（問題提起・根拠・譲歩・結論）を書きこみ、筆者の意見を示す表現のある段落を主張の中心にする。",
              steps=["第1段落で話題と問題提起を確認する。", "譲歩の段落（However / On the other hand / Of course / Still）を見つけ、主張と区別する。",
                     "最終段落の筆者の意見を確認する。", "選択肢を「狭すぎる・広すぎる・逆」で点検する。", f"答え：{ok}"],
              alt=["選んだ選択肢が、第2段落（根拠）と第3段落（問題点）の両方と矛盾しないかを確かめる。"],
              pc=[("段落の役割をとらえている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["印象に残る数値や具体例を主張と考える。", "譲歩の段落の内容を主張と取り違える。"], why={w: MAIN_WHY[k] for w, k in wrongs})


@gen("standard_practice", 5, ["condition_check", "common_error"])
def b_true_false(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.6:
        ok = r.choice(p["trues"])
        wrongs = r.sample(p["falses"], 3)
        return mc(f"{head(p)}\n記事の内容に合うものを1つ選びなさい。", [ok] + [w for w, _ in wrongs],
                  f"{ok}　本文の該当箇所の言いかえになっている。", d=3, stim=pstim(p),
                  ap="選択肢ごとに根拠となる本文の箇所を探し、「一致・逆・書かれていない・言いすぎ」に分ける。",
                  steps=["選択肢のキーワード（数値・人物・行動）を本文で探す。", "数量（all / most / some / more than half）や否定に注意して照合する。", f"本文と一致するのは：{ok}"],
                  alt=["誤りの選択肢について、本文のどの語句と食い違うかを書き出して確かめる。"],
                  pc=[("根拠となる箇所を見つけている", 2), ("正しい選択肢を選んでいる", 2)],
                  pit=["all / always などの強い語を見落とし、言いすぎの選択肢を選ぶ。"], why={w: (why, "本文との照合不足") for w, why in wrongs})
    wrong, why0 = r.choice(p["falses"])
    oks = r.sample(p["trues"], 3)
    return mc(f"{head(p)}\n記事の内容に合わないものを1つ選びなさい。", [wrong] + oks,
              f"{wrong}　{why0}", d=3, stim=pstim(p),
              ap="「合わないもの」を選ぶ設問であることを確認し、本文と一致する3つを根拠つきで消していく。",
              steps=["設問が「合わないもの」を求めていることを確認する。", "各選択肢の根拠を本文で探す。", f"本文と食い違うのは：{wrong}（{why0}）"],
              alt=["選んだ選択肢の誤りの型（逆・言いすぎ・書かれていない）を言えるかで確かめる。"],
              pc=[("根拠となる箇所を見つけている", 2), ("合わない選択肢を選んでいる", 2)],
              pit=["設問の NOT・合わないものを読み落とし、本文と一致する選択肢を選ぶ。"],
              why={t: ("本文の内容と一致するので、「合わないもの」には当たらない。", "設問の条件（合わないもの）の読み落とし") for t in oks})


@gen("standard_practice", 5, ["concept", "condition_check"])
def b_fact_in_passage(r):
    p = r.choice(PASSAGES)
    if r.random() < 0.5:
        ok = r.choice(p["facts"])
        wrongs = r.sample(p["opinions"], 3)
        return mc(f"{head(p)}\n記事で述べられていることのうち、意見（opinion）ではなく事実（fact）であるものを選びなさい。", [ok] + wrongs,
                  f"{ok}　調査の数値や実際に行われたことは、記録で確かめられる事実である。", d=3, stim=pstim(p),
                  ap="筆者の意見は最終段落（I believe / In my view / I think）に集まっている。調査の数値・実施されたことは事実。",
                  steps=["各選択肢が本文のどの段落の内容かを確かめる。", "should / necessary / worth / could make a big difference など、判断・評価・推測の表現を含むものを意見として外す。", f"事実は：{ok}"],
                  alt=["正解の選択肢が、どの調査・記録で確かめられるかを本文から言えるかで確認する。"],
                  pc=[("意見を示す表現に気づいている", 2), ("事実の選択肢を選んでいる", 2)],
                  pit=["筆者の意見を本文に書いてあるから事実だと考える。"],
                  why={w: ("書き手の判断・評価・推測・提案であり、確かめられる事実ではない。本文に書いてあることと事実であることは別である。", "「本文にある」と「事実」の混同") for w in wrongs})
    ok = r.choice(p["opinions"])
    wrongs = r.sample(p["facts"], 3)
    return mc(f"{head(p)}\n記事で述べられていることのうち、事実（fact）ではなく筆者の意見（opinion）であるものを選びなさい。", [ok] + wrongs,
              f"{ok}　筆者の判断・評価・提案を述べている。", d=3, stim=pstim(p),
              ap="判断・評価・推測・提案を表す表現（should / necessary / worth / could など）を探す。",
              steps=["各選択肢の述語部分に注目する。", "数値・日時・実施された出来事は事実として外す。", f"意見は：{ok}"],
              alt=["選んだ文に「人によって考えが分かれるか」を問い、分かれるなら意見と確かめる。"],
              pc=[("事実の選択肢を外せている", 2), ("意見の選択肢を選んでいる", 2)],
              pit=["調査で人々が答えた内容（〇%が～と答えた）を意見と考える。"],
              why={w: ("調査の数値や実際に行われたことで、記録で確かめられる事実である。", "事実を意見と取り違える") for w in wrongs})


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "application"])
def c_summary(r):
    p = r.choice(PASSAGES)
    lim = r.choice([90, 100])
    return desc(f"{head(p)}\n記事の要旨を、筆者の主張がわかるように日本語{lim}字以内でまとめなさい。", p["summary"],
                "問題提起・根拠・譲歩・結論の役割を押さえ、具体的な数値や例を除いて、筆者の主張とその根拠、認めている問題点をまとめる。",
                p["skeys"], d=4, p=8, grid=lim, stim=pstim(p),
                ap="最終段落の筆者の意見を中心にし、第2段落の根拠と第3段落の問題点（譲歩）を短く添える。数値や個人の発言は入れない。",
                steps=["各段落に役割（問題提起・根拠・譲歩・結論）を書きこむ。", "具体的な数値・例・発言を除く。", "「利点 → 問題点 → 筆者の主張」の順に1〜2文でまとめる。", "字数と、本文にない内容がないかを確かめる。"],
                alt=["まず筆者の主張を英語1文で書き（本文の I believe / I think の文を使う）、それを日本語に直して根拠と問題点を加える方法もある。"],
                pc=[(k, v) for k, v in p["skeys"]],
                pit=["譲歩の段落の問題点を主張としてまとめる。", "調査の数値をそのまま要旨に入れて字数を使ってしまう。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U10", "HS-ENG-U09"])
def c_two_texts(r):
    pr = r.choice(PAIRS)
    st = stim(f"TW-{pr['key']}", pr["a"] + "\n\n" + pr["b"], "passage", f"「{pr['topic']}」について、2人の筆者が書いた意見を読んで、あとの問いに答えなさい。", source="オリジナル")
    if r.random() < 0.5:
        return desc(f"「{pr['topic']}」についての2人の筆者の意見を読み、(1) それぞれの筆者の立場と理由、(2) 2人が共通して大切だと考えている点を、日本語で説明しなさい。",
                    f"(1) A：{pr['pa']}。B：{pr['pb']}。(2) {pr['common']}。",
                    "複数のテクストを読む問題では、それぞれの主張と理由を整理したうえで、対立点と共通点を区別する。",
                    [("(1) A の立場と理由を正しく説明している", 3), ("(1) B の立場と理由を正しく説明している", 3), ("(2) 共通点を本文に即して説明している", 2)], d=4, p=8, lines=6, stim=st,
                    ap="それぞれの文章の最初の文（主張）と because / so などの理由を探し、Of course などの譲歩の部分から共通点を見つける。",
                    steps=["A の主張（最初の文）と理由を書き出す。", "B の主張と理由を書き出す。", "譲歩の表現（Of course ～ など）や、両者が前提にしている価値を探し、共通点とする。", "立場の違いと共通点を分けて答案にする。"],
                    alt=["表（A／B × 主張・理由・認めていること）を作ってから文章にすると、もれと混同を防げる。"],
                    pc=[("A の立場と理由", 3), ("B の立場と理由", 3), ("共通点", 2)],
                    pit=["2人の意見を混ぜて書き、どちらの理由かがわからない答案になる。", "共通点として、一方しか述べていない内容を書く。"])
    return desc(f"「{pr['topic']}」についての2人の筆者の意見を読み、どちらの筆者に賛成かを明らかにして、あなたの意見を英語で書きなさい。理由を1つ以上含め、30語程度とする。",
                f"（解答例）{pr['opinion']}",
                "賛成する筆者を明示し、本文の理由をそのまま写すのではなく、自分の経験や具体例で理由を述べる。",
                [("賛成する筆者と自分の立場を明確に述べている", 3), ("理由を具体的に述べている", 3), ("文法・語法が正しく、語数が適切である", 2)], d=4, p=8, lines=6, stim=st,
                ap="I agree with Writer A / B. で始め、because や For example で自分の経験に基づく理由を加える。",
                steps=["2人の主張と理由を確認する。", "どちらに賛成するかを決める。", "理由を1つ以上、自分の経験や具体例で考える。", "主張 → 理由 → 具体例の順に30語程度で書く。"],
                alt=["一方に全面的に賛成せず、条件つきで賛成する（I agree with Writer A, but only if ～）書き方もできる。"],
                pc=[("立場の明示", 3), ("理由の具体性", 3), ("文法・語数", 2)],
                pit=["本文の英文をそのまま写して理由にする。", "どちらに賛成かを書かない。"])


@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def c_best_plan(r):
    kind = r.choice(["standard", "electric"])
    rate, day = (BK_STD, BK_STD_DAY) if kind == "standard" else (BK_ELE, BK_ELE_DAY)
    mins = r.choice([130, 190, 200, 250, 260, 290, 310, 330, 380, 400])
    nb = r.randint(2, 4)
    cost, hrs, _, _ = bike_cost(kind, mins)
    h, m = divmod(mins, 60)
    hourly = hrs * rate
    better = "1日パス" if day < hourly else ("時間料金" if hourly < day else "どちらも同額")
    total = cost * nb
    kj = "標準自転車" if kind == "standard" else "電動自転車"
    ans = (f"利用時間 {h}時間{m}分は、始まった1時間ごとに料金がかかるので {hrs}時間分。時間料金は {rate}×{hrs}＝{hourly}円、1日パスは {day}円なので、"
           f"{'1日パスのほうが安い' if day < hourly else ('時間料金のほうが安い' if hourly < day else '同じ金額になる')}。1台 {cost}円 × {nb}台＝{jyen(total)}。")
    return desc(f"掲示“Lakeside Bike Rental”について答えなさい。\n{nb}人の友人が{kj}を1人1台ずつ借りて、{h}時間{m}分利用する予定である。時間料金と1日パスのどちらで支払うほうが安いかを、計算の過程を示して日本語で説明し、{nb}人分の合計金額を求めなさい。",
                ans, f"結論は「{better}」。端数の時間を1時間に切り上げる条件と、2つの料金の比較がポイント。",
                [("利用時間を切り上げて正しく数えている", 2), ("時間料金と1日パスを計算して比較している", 3), ("合計金額が正しい", 2), ("説明が筋道立っている", 1)], d=4, p=8, lines=6, stim=nstim("BIKE"),
                ap="注意書き「始まった1時間ごとに料金がかかる」を使って時間数を決め、2つの料金を両方計算して比べる。",
                steps=[f"{h}時間{m}分 → {hrs}時間分（切り上げ）。", f"時間料金：{rate}×{hrs}＝{hourly}円。", f"1日パス：{day}円。", f"比べると{better if better == 'どちらも同額' else better + 'のほうが安く'}、1台 {cost}円。", f"{nb}台で {jyen(total)}。"],
                alt=[f"1日パスの料金は時間料金の {day}÷{rate}＝{(f'{day // rate}' if day % rate == 0 else f'約{day / rate:.1f}')} 時間分に当たる。利用時間（{hrs}時間分）がそれより長いか短いかで、計算する前にどちらが安いかの見当をつけられる。"],
                pc=[("時間の切り上げ", 2), ("2つの料金の比較", 3), ("合計金額", 2), ("説明の筋道", 1)],
                pit=["端数の時間を切り捨てて計算する。", "1台分の金額だけを答え、人数分をかけ忘れる。"],
                chk=(f"{nb}*Min({rate}*ceiling(Rational({mins},60)),{day})", str(total), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "condition_check"])
def d_fact_opinion_err(r):
    scene, facts, ops = r.choice(FO)
    fs = r.sample(facts, 2)
    os_ = r.sample(ops, 2)
    rows = [(s, "事実") for s in fs] + [(s, "意見") for s, _ in os_]
    r.shuffle(rows)
    bad = r.randrange(4)
    sent, true_lab = rows[bad]
    shown = [(s, ("意見" if lab == "事実" else "事実") if i == bad else lab) for i, (s, lab) in enumerate(rows)]
    sig = dict(ops).get(sent)
    reason = op_why(sig) if true_lab == "意見" else FACT_WHY
    if true_lab == "意見":
        tempt = "数値や具体的な語を含むので、確かめられる事実のように見えた。" if any(ch.isdigit() for ch in sent) else "断定的な言い方なので、事実のように見えた。"
    else:
        tempt = "レポートの書き手の考えのように見えたが、内容自体は記録で確かめられる。"
    lines_ = "\n".join(f"({k + 1}) {s} → {lab}" for k, (s, lab) in enumerate(shown))
    return desc(f"「{scene}」についてのレポートの4つの文を、ある生徒が事実と意見に分類した。\n［ある生徒の解答］\n{lines_}\n誤って分類されている文を1つ選び、その理由と正しい分類を説明しなさい。",
                f"({bad + 1}) は{true_lab}が正しい。{reason}",
                "事実は資料・記録で確かめられる内容、意見は判断・評価・推測・提案。数値を含むかどうかではなく、評価や判断の語があるかで判断する。",
                [("誤っている文を正しく指摘している", 2), ("正しい分類を示している", 2), ("判断の根拠（評価語・確かめられるか）を説明している", 2)], d=3, p=6, lines=5,
                ap="4つの文それぞれについて「記録で確かめられるか」「判断・評価の語があるか」を確認し、生徒の分類と照らし合わせる。",
                steps=["各文の評価・判断を表す語（should / best / I think / probably / too ～ など）に印をつける。", "確かめられる内容かどうかを判断する。",
                       f"({bad + 1}) の分類が誤り。正しくは{true_lab}。", "理由を根拠となる語とともに書く。"],
                alt=["誤りと判断した文について、「人によって考えが分かれるか」という別の基準でも同じ結論になるか確かめる。"],
                pc=[("誤りの指摘", 2), ("正しい分類", 2), ("根拠の説明", 2)],
                pit=["数値の有無だけで事実・意見を決める。"],
                err=dict(sol=lines_, step=f"({bad + 1}) の分類", type="concept", tempt=tempt, fix=f"({bad + 1}) は{true_lab}。{reason}"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_price_err(r):
    for _ in range(50):
        case = r.choice(CASES)(r)
        ws = [w for w in clean_wrongs(case) if w[3]]
        if ws:
            break
    w = r.choice(ws)
    sol = f"{w[3]} として計算し、{yen(w[0])} と答えた。"
    return desc(f"掲示“{NOTICES[case['key']]['title']}”について答えなさい。\n{case['story']}\n［ある生徒の解答］\n{sol}\nこの解答の誤りを指摘し、正しい金額を求めなさい。",
                f"誤り：{w[1]}　正しい計算：{case['f_ok']}（円）。答え {yen(case['total'])}",
                f"掲示の注意書きの条件（{case['cond']}）をすべて当てはめて計算し直す。",
                [("誤りの箇所と理由を指摘している", 2), ("条件を当てはめた正しい計算を示している", 3), ("正しい金額を答えている", 1)], d=3, p=6, lines=6, stim=nstim(case["key"]),
                ap="生徒の計算が掲示のどの条件を使っていないか（または誤って使っているか）を、注意書きを1行ずつ確認して探す。",
                steps=["生徒の計算の式と、掲示の料金表・注意書きを対応させる。", f"誤りの箇所：{w[4]}。{w[1]}", f"正しい計算：{case['f_ok']}。", f"答え：{yen(case['total'])}。"],
                alt=["区分ごとの人数と単価の表を作り、小計を足し直して確かめる。"],
                pc=[("誤りの指摘", 2), ("正しい計算", 3), ("正しい金額", 1)],
                pit=["料金表の数字だけを見て、表の下の注意書きを読まない。"],
                err=dict(sol=sol, step=w[4], type=w[5], tempt=f"{w[2]}。料金表の数字は目に入りやすいが、注意書きの条件は読み飛ばしやすい。", fix=f"{case['f_ok']}。答え {yen(case['total'])}"),
                chk=(case["chk"], str(case["total"]), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "written_reasoning"])
def d_summary_err(r):
    p = r.choice(PASSAGES)
    wrong, why = r.choice(p["wrong_sum"])
    return desc(f"{head(p)}\n記事の要旨を日本語でまとめる問題に、ある生徒は次のように答えた。\n［ある生徒の解答］\n{wrong}\nこの解答の問題点を指摘し、適切な要旨を書きなさい。",
                f"問題点：{why}　適切な要旨：{p['summary']}",
                "要旨には、具体的な数値や例、譲歩で認めた問題点ではなく、筆者の主張とその根拠を中心に入れる。",
                [("解答の問題点を段落の役割に触れて指摘している", 2), ("筆者の主張を含む要旨を書いている", 3), ("根拠や問題点を適切に添えている", 1)], d=4, p=6, lines=6, stim=pstim(p),
                ap="生徒の解答が本文のどの段落の内容かを特定し、その段落の役割（根拠の具体例・譲歩）を考える。",
                steps=["生徒の解答が対応する段落を本文で探す。", "その段落の役割（具体例・数値・譲歩）を判断し、要旨として不十分な点を指摘する。", "最終段落の筆者の主張を中心に、要旨を書き直す。"],
                alt=["生徒の解答と正しい要旨を並べ、最終段落の筆者の意見が含まれているかどうかで比べる。"],
                pc=[("問題点の指摘", 2), ("主張を含む要旨", 3), ("根拠・問題点の扱い", 1)],
                pit=["印象に残った数値や例を言いかえただけで、主張を書かない。"],
                err=dict(sol=wrong, step="要旨の中心に選んだ段落", type="interpretation", tempt="具体的な数値や、However などの後ろの内容は目立つので、主張だと思いこみやすい。",
                         fix=p["summary"]))


GENERATORS = [a_notice_detail, a_fact_opinion, a_paraphrase, a_schedule,
              b_price, b_main_idea, b_true_false, b_fact_in_passage,
              c_summary, c_two_texts, c_best_plan,
              d_fact_opinion_err, d_price_err, d_summary_err]
