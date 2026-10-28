"""神奈川県公立高校入試形式 オリジナル模試（第2回） 英語。

令和5年度の問題冊子と同じ大問構成（問1〜問8・解答形式・選択肢の数と形式）にならったオリジナル問題。
本文・資料・図・選択肢はすべてオリジナルで、グラフ・表の数値は架空のもの。
問4 は実際の解答用紙と同じく「3番目」「5番目」の二つの番号を答える形にするため、
小問ごとに「3番目」「5番目」の2つのマーク欄（それぞれ1〜6）に分けている。
"""
from ._common import desc, figure, mc, stim, table

PHASE = 6

U = "EX-KNG-MOCK-ENG"
L, V, G, W, R, D = ["listening"], ["vocabulary"], ["grammar"], ["writing"], ["reading"], ["reading", "data_interpretation"]


def tag(sec, items):
    out = []
    for no, it in items:
        it["u"] = U
        it["sec"] = sec
        it["no"] = no
        out.append(it)
    return out


# ============================================================================
# 図（SVG）
# ============================================================================

def _t(x, y, s, size=9, anchor="start", weight="normal", halo=False, style=""):
    bg = ""
    if halo:  # 数値の背後に白い下地（ハッチングの上でも読めるように）
        w = 0.56 * size * len(str(s)) + 2
        x0 = x - w / 2 if anchor == "middle" else (x - w if anchor == "end" else x - 1)
        bg = f'<rect x="{x0:.1f}" y="{y - size * 0.8:.1f}" width="{w:.1f}" height="{size * 0.95:.1f}" fill="#fff"/>'
    return (bg + f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}"'
            f'{(" " + style) if style else ""}>{s}</text>')


_PAT = ('<defs>'
        '<pattern id="pHatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
        '<rect width="5" height="5" fill="#fff"/><line x1="0" y1="0" x2="0" y2="5" stroke="#000" stroke-width="1"/></pattern>'
        '<pattern id="pDot" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="4" fill="#fff"/><circle cx="2" cy="2" r="0.8" fill="#000"/></pattern>'
        '</defs>')
_FILLS = ["#ffffff", "url(#pHatch)", "url(#pDot)", "#b5b5b5"]
_CATS = ["Clothes", "Bicycles", "Toys", "Others"]


def _stack_panel(ox, oy, data, num):
    """積み上げ棒グラフ1枚（230×190）。data=[(年, [Clothes, Bicycles, Toys, Others]), ...]"""
    base, left, k = oy + 160, ox + 40, 0.52
    o = [_t(ox + 4, oy + 14, f"{num}．", 12, weight="bold"), _t(left - 4, oy + 18, "(件)", 8, "end")]
    o.append(f'<line x1="{left}" y1="{base}" x2="{left}" y2="{base - 140}" stroke="#000" stroke-width="0.8"/>')
    o.append(f'<line x1="{left}" y1="{base}" x2="{ox + 225}" y2="{base}" stroke="#000" stroke-width="0.8"/>')
    for v in (0, 100, 200):
        y = base - v * k
        o.append(f'<line x1="{left - 3}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#000" stroke-width="0.8"/>')
        o.append(_t(left - 5, y + 3, str(v), 8, "end"))
    for i, (year, vals) in enumerate(data):
        x, w, y = left + 16 + i * 60, 34, base
        for v, f in zip(vals, _FILLS):
            h = v * k
            o.append(f'<rect x="{x}" y="{y - h:.1f}" width="{w}" height="{h:.1f}" fill="{f}" stroke="#000" stroke-width="0.8"/>')
            if h >= 10:
                o.append(_t(x + w / 2, y - h / 2 + 3, str(v), 8, "middle", halo=True))
            else:
                o.append(_t(x + w + 2, y - h / 2 + 3, str(v), 7.5))
            y -= h
        o.append(_t(x + w / 2, y - 3, f"total {sum(vals)}", 7.5, "middle"))
        o.append(_t(x + w / 2, base + 12, str(year), 9, "middle"))
    return "".join(o)


def _stack_figure():
    panels = {
        1: [(2021, [110, 50, 50, 30]), (2022, [80, 40, 30, 30]), (2023, [60, 30, 10, 20])],   # 年の順が逆
        2: [(2021, [60, 10, 30, 20]), (2022, [80, 30, 40, 30]), (2023, [110, 50, 50, 30])],   # Bicycles と Toys を入れかえ
        3: [(2021, [60, 30, 10, 20]), (2022, [30, 40, 30, 80]), (2023, [110, 50, 50, 30])],   # 2022年の Clothes と Others を入れかえ
        4: [(2021, [60, 30, 10, 20]), (2022, [80, 40, 30, 30]), (2023, [110, 50, 50, 30])],   # 正解
    }
    W, H = 470, 410
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W * 0.8:.0f}" height="{H * 0.8:.0f}" font-family="serif">', _PAT]
    for n, (px, py) in zip(range(1, 5), [(0, 0), (235, 0), (0, 190), (235, 190)]):
        o.append(_stack_panel(px, py, panels[n], n))
    lx = 40
    for c, f in zip(_CATS, _FILLS):
        o.append(f'<rect x="{lx}" y="{H - 22}" width="14" height="10" fill="{f}" stroke="#000" stroke-width="0.8"/>')
        o.append(_t(lx + 18, H - 13, c, 9))
        lx += 100
    o.append("</svg>")
    return "".join(o)


def _line_panel(ox, oy, vals, lab):
    """折れ線グラフ1枚（200×150）。2015〜2025年。"""
    left, base, dx, k = ox + 34, oy + 120, 14.5, 2.1
    o = [_t(ox + 6, oy + 14, lab, 12, weight="bold"), _t(left - 3, oy + 22, "(個)", 8, "end")]
    o.append(f'<line x1="{left}" y1="{base}" x2="{left}" y2="{base - 100}" stroke="#000" stroke-width="0.8"/>')
    o.append(f'<line x1="{left}" y1="{base}" x2="{left + 158}" y2="{base}" stroke="#000" stroke-width="0.8"/>')
    for v in (0, 20, 40):
        y = base - v * k
        o.append(f'<line x1="{left - 3}" y1="{y:.1f}" x2="{left}" y2="{y:.1f}" stroke="#000" stroke-width="0.8"/>')
        o.append(_t(left - 5, y + 3, str(v), 8, "end"))
    pts = [(left + 6 + i * dx, base - v * k) for i, v in enumerate(vals)]
    o.append('<polyline points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '" fill="none" stroke="#000" stroke-width="1.2"/>')
    m = vals.index(min(vals))
    for i, (x, y) in enumerate(pts):
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.8" fill="#000"/>')
        if i in (0, m, len(vals) - 1):
            o.append(_t(x, y - 5 if i != m else y + 11, str(vals[i]), 8, "middle", halo=True))
    for i, yr in ((0, 2015), (5, 2020), (10, 2025)):
        o.append(_t(pts[i][0], base + 12, str(yr), 8, "middle"))
    return "".join(o)


def _hbars(ox, oy, title, vals, k):
    o = [_t(ox, oy, title, 8.5, weight="bold")]
    for j, (c, v) in enumerate(zip(["Yes", "No", "Not sure"], vals)):
        y = oy + 8 + j * 17
        o.append(_t(ox + 38, y + 9, c, 8, "end"))
        o.append(f'<rect x="{ox + 42}" y="{y}" width="{v * k:.1f}" height="11" fill="#b5b5b5" stroke="#000" stroke-width="0.7"/>')
        o.append(_t(ox + 45 + v * k, y + 9, str(v), 8))
    return "".join(o)


def _pair_panel(ox, oy, owners, customers, lab):
    o = [_t(ox + 4, oy + 14, lab, 12, weight="bold")]
    o.append(_hbars(ox + 18, oy + 32, "Shop owners", owners, 3.6))
    o.append(_hbars(ox + 18, oy + 98, "Customers", customers, 1.05))
    return "".join(o)


def _swallow_figure():
    lines = {"A": [40, 35, 29, 22, 17, 12, 12, 13, 11, 12, 12],   # 2020年以降ほぼ横ばい
             "B": [40, 35, 29, 22, 17, 12, 15, 21, 28, 34, 39],   # 正解
             "C": [40, 31, 22, 12, 16, 20, 24, 28, 32, 36, 39]}   # 2018年が最少
    pairs = {"X": ([5, 12, 3], [40, 2, 8]),     # 店主の Yes と No が逆
             "Y": ([12, 5, 3], [40, 8, 2]),     # 客の No と Not sure が逆
             "Z": ([12, 5, 3], [40, 2, 8])}     # 正解
    W, H = 620, 340
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif">']
    o.append(_t(4, 14, "ア群", 10, weight="bold"))
    for i, (lab, v) in enumerate(lines.items()):
        o.append(_line_panel(10 + i * 205, 16, v, lab))
    o.append(_t(4, 180, "イ群", 10, weight="bold"))
    for i, (lab, (a, b)) in enumerate(pairs.items()):
        o.append(f'<rect x="{12 + i * 205}" y="186" width="190" height="150" fill="none" stroke="#000" stroke-width="0.6"/>')
        o.append(_pair_panel(14 + i * 205, 186, a, b, lab))
    o.append("</svg>")
    return "".join(o)


def _person(x, y, s=1.0, arm_up=False):
    """簡単な人物（頭の中心 x, y）。"""
    o = [f'<circle cx="{x}" cy="{y}" r="{9 * s}" fill="#fff" stroke="#000" stroke-width="1.1"/>',
         f'<line x1="{x}" y1="{y + 9 * s}" x2="{x}" y2="{y + 38 * s}" stroke="#000" stroke-width="1.3"/>',
         f'<line x1="{x}" y1="{y + 38 * s}" x2="{x - 9 * s}" y2="{y + 58 * s}" stroke="#000" stroke-width="1.3"/>',
         f'<line x1="{x}" y1="{y + 38 * s}" x2="{x + 9 * s}" y2="{y + 58 * s}" stroke="#000" stroke-width="1.3"/>',
         f'<line x1="{x}" y1="{y + 18 * s}" x2="{x - 12 * s}" y2="{y + 32 * s}" stroke="#000" stroke-width="1.3"/>']
    if arm_up:
        o.append(f'<line x1="{x}" y1="{y + 18 * s}" x2="{x + 13 * s}" y2="{y + 2 * s}" stroke="#000" stroke-width="1.3"/>')
    else:
        o.append(f'<line x1="{x}" y1="{y + 18 * s}" x2="{x + 12 * s}" y2="{y + 32 * s}" stroke="#000" stroke-width="1.3"/>')
    return "".join(o)


def _story_figure():
    W, H = 600, 390
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="serif">']
    for i, lab in enumerate("ABC"):
        y0 = 6 + i * 128
        o.append(_t(2, y0 + 16, lab, 13, weight="bold"))
        o.append(f'<rect x="20" y="{y0}" width="200" height="118" rx="4" fill="#fff" stroke="#000" stroke-width="1"/>')
    # A：駅のポスターを見る Sota
    y0 = 6
    o.append(_person(60, y0 + 34))
    o.append(_t(60, y0 + 112, "Sota", 8.5, "middle"))
    o.append(_t(80, y0 + 28, "!", 14, weight="bold"))
    o.append(f'<rect x="100" y="{y0 + 10}" width="108" height="98" fill="#fff" stroke="#000" stroke-width="1"/>')
    o.append(_t(154, y0 + 24, "Hikari Aquarium", 9, "middle", weight="bold"))
    o.append(_t(154, y0 + 38, "NEW! Penguin Area", 8.5, "middle"))
    o.append(f'<ellipse cx="154" cy="{y0 + 66}" rx="15" ry="20" fill="#222"/>')
    o.append(f'<ellipse cx="154" cy="{y0 + 70}" rx="9" ry="14" fill="#fff"/>')
    o.append(f'<circle cx="149" cy="{y0 + 54}" r="1.6" fill="#fff"/><circle cx="159" cy="{y0 + 54}" r="1.6" fill="#fff"/>')
    o.append(f'<polygon points="151,{y0 + 59} 157,{y0 + 59} 154,{y0 + 63}" fill="#e0a000"/>')
    o.append(_t(154, y0 + 102, "Opens on April 29!", 8.5, "middle"))
    # B：Sota が Tom に話しかける
    y0 = 134
    o.append(_person(80, y0 + 34))
    o.append(_person(160, y0 + 34))
    o.append(_t(80, y0 + 112, "Sota", 8.5, "middle"))
    o.append(_t(160, y0 + 112, "Tom", 8.5, "middle"))
    o.append(f'<ellipse cx="112" cy="{y0 + 16}" rx="18" ry="10" fill="#fff" stroke="#000" stroke-width="0.8"/>')
    o.append(_t(112, y0 + 20, "…", 10, "middle"))
    # C：Tom が喜んで答える
    y0 = 262
    o.append(_person(80, y0 + 34))
    o.append(_person(160, y0 + 34, arm_up=True))
    o.append(_t(80, y0 + 112, "Sota", 8.5, "middle"))
    o.append(_t(160, y0 + 112, "Tom", 8.5, "middle"))
    # 右側の英文
    o.append(_t(240, 165, "Sota: Hi, Tom.", 12))
    o.append(f'<rect x="322" y="150" width="262" height="24" fill="#fff" stroke="#000" stroke-width="1.1"/>')
    o.append(_t(240, 200, "Do you want to go there with me?", 12))
    o.append(_t(240, 300, "Tom: Sure! I love penguins.", 12))
    o.append(_t(240, 322, "How about next Sunday?", 12))
    o.append("</svg>")
    return "".join(o)


# ============================================================================
# 資料（放送文・本文）
# ============================================================================

STIMULI = [
    # ---------------- 問1 リスニング ----------------
    stim("E2-L1",
         "Ms. Baker: Haruto, you look happy. What happened?\n"
         "Haruto: My sister started working in Osaka, so I'm going to visit her during the winter vacation.\n"
         "Ms. Baker: That's nice. How are you going to get there?\n"
         "Haruto: (チャイム)",
         "listening_script", "問1(ア) No.1"),
    stim("E2-L2",
         "Haruto: Mom, have you seen my blue notebook? I need it for my science class today.\n"
         "Mother: I saw a blue notebook on the table in the living room this morning.\n"
         "Haruto: I looked there, but it wasn't there.\n"
         "Mother: Then maybe your brother took it by mistake. He has a blue notebook, too.\n"
         "Haruto: (チャイム)",
         "listening_script", "問1(ア) No.2"),
    stim("E2-L3",
         "Yui: Haruto, the school festival is next Friday. Have you finished making the poster for our class?\n"
         "Haruto: Not yet. I've drawn the picture, but I haven't written the words.\n"
         "Yui: Can I help you? I'm good at writing big letters.\n"
         "Haruto: (チャイム)",
         "listening_script", "問1(ア) No.3"),
    stim("E2-L4",
         "Mei: Sota, did you watch the soccer game on TV last night?\n"
         "Sota: No, I couldn't. I had to finish my homework. Who won?\n"
         "Mei: Japan did. The score was 2 to 1. Japan got the winning goal in the last five minutes.\n"
         "Sota: Wow! I wish I had watched it.\n"
         "Mei: My father recorded the game. You can watch it at my house this Saturday if you want.\n"
         "Sota: Really? Thanks! I'll come at ten.\n"
         "Question: What can we say about Sota?",
         "listening_script", "問1(イ) No.1"),
    stim("E2-L5",
         "Clerk: Hello. May I help you?\n"
         "Ms. Baker: Yes. I'm looking for a T-shirt for my son. He's ten years old.\n"
         "Clerk: How about this one? It's popular among children. We have it in blue and green.\n"
         "Ms. Baker: He likes green, but this one looks a little big for him.\n"
         "Clerk: Then how about this smaller green one? It's 1,500 yen.\n"
         "Ms. Baker: Perfect. I'll take it.\n"
         "Question: What can we say about Ms. Baker?",
         "listening_script", "問1(イ) No.2"),
    stim("E2-L6",
         "Hello, everyone. I'm Mr. Hill. Today I'm going to tell you about the English Camp this summer. "
         "The camp will be held for three days, from August 7 to August 9, at Hikari Lake Youth House. "
         "About thirty students from five junior high schools will join it.\n"
         "On the first day, you will make groups and cook dinner together. "
         "On the second day, you will climb a mountain with teachers from five countries and talk about nature in English. "
         "On the last day, each group will make a short play in English and show it to everyone.\n"
         "When I was a student, I was afraid of making mistakes, so I didn't speak much in English class. "
         "But at a camp like this one, I found that people listened to me even when my English was not perfect. "
         "Mistakes are a part of learning. So please don't worry, and try to speak a lot. "
         "If you want to join the camp, please give the form to your English teacher by July 10. Thank you.",
         "listening_script", "問1(ウ)"),

    # ---------------- 問6 スピーチ ----------------
    stim("E2-SPEECH",
         "Hello, everyone. Do you have something at home that you don't use because it is broken? "
         "Last spring, the *zipper of my favorite bag broke. I thought, \"I have to buy a new one.\" "
         "But my grandmother said, \"Why don't you take it to the Repair Café?\" I had never heard of that place.\n\n"
         "The Repair Café is held at the community center in our city on the second Sunday of every month. "
         "People bring broken things there, and volunteers help them repair the things. "
         "The volunteers are not *professionals; many of them are *retired people who like making or fixing things. "
         "( ① ) When I visited the café, a man named Mr. Kato showed me how to change the zipper. "
         "It took about an hour, and my bag looked like new. I was so happy that I decided to join the café as a volunteer.\n\n"
         "Now, please look at [[u:this graph]]. It shows the number of things people brought to the Repair Café in the last three years. "
         "In 2021, 120 things were brought. Since then, the number has increased every year, and in 2023, it was twice as large as in 2021. "
         "Clothes were the biggest part every year. I was surprised that the number of toys grew so much. "
         "In 2021, toys were the smallest part, but in 2023, the number became five times larger, and it was the same as the number of bicycles. "
         "Mr. Kato told me that many parents come with their children now. ( ② )\n\n"
         "Why do more people come to the café? I asked some visitors. One woman said, \"My jacket was a present from my mother, "
         "so I want to wear it for a long time.\" A high school student said, \"I want to learn how to repair things by myself.\" "
         "I think people are starting to feel that things have stories, and that throwing them away is a *waste.\n\n"
         "Of course, not everything can be repaired at the café. Last month, a boy brought a video game machine, "
         "but we couldn't fix it because we didn't have the *parts. He looked very sad. ( ③ ) "
         "Now the volunteers are making a list of shops that can repair *electronic things, so that we can tell visitors where to go.\n\n"
         "Through this activity, I learned two things. First, repairing takes time, but the time makes us love our things more. "
         "Second, when we repair things together, we can talk with people of different ages. "
         "Before, I didn't talk with older people very much, but now Mr. Kato is one of my best teachers.\n\n"
         "Next time something breaks, please don't throw it away soon. Think about repairing it first. "
         "You may find a new story with it. Thank you.",
         "passage",
         glossary=[("zipper", "ファスナー"), ("professional", "専門家"), ("retired", "退職した"), ("waste", "むだ"),
                   ("parts", "部品"), ("electronic", "電子の")]),

    # ---------------- 問7 資料 ----------------
    stim("E2-CHAT",
         "（ア）Yui and Sota are classmates. Their ALT, Mr. Lopez, is going back to his country next month. "
         "They want to buy a present for him. They are sending messages to each other on Friday night.\n\n"
         "Yui (19:02)：Mr. Lopez loves cooking, so let's buy a cooking tool for him. Can you go shopping with me tomorrow?\n"
         "Sota (19:05)：Sure. I found a list of shops near Hikari Station. Look at the List below.\n"
         "Yui (19:08)：Thanks. I want to take enough time to choose a good one, so let's stay at the shop for one hour.\n"
         "Sota (19:10)：OK. I have basketball practice at school until 1:00 tomorrow, and it takes 30 minutes from school to the station. "
         "I want to have lunch at home after practice, so let's meet as late as possible.\n"
         "Yui (19:12)：All right. I have a piano lesson at 4:30, so I need to be back at the station by 4:00.\n"
         "Sota (19:14)：Then let's go to a shop that sells cooking tools and is open tomorrow afternoon. "
         "We'll walk from the station. Let's meet at the station at [[blank:　　]].\n"
         "Yui (19:15)：OK. See you tomorrow!",
         "data",
         tbl=table([["Green Kitchen", "cooking tools", "10:00 – 14:00", "10 minutes"],
                    ["Hikari Mall", "cooking tools, clothes", "10:00 – 20:00", "20 minutes"],
                    ["Maple Books", "cookbooks", "closed", "5 minutes"],
                    ["Wood House", "tables, chairs", "11:00 – 18:00", "15 minutes"]],
                   header=["Shop", "Things they sell", "Open (Saturday)", "Walking time from the station"],
                   caption="List：Shops near Hikari Station")),
    stim("E2-POSTER",
         "（イ）Kaho and Daiki are junior high school students. They are talking with Mr. Hill, their English teacher, "
         "about a video contest.\n\n"
         "Mr. Hill：Kaho, Daiki, you want to join this contest, right?\n"
         "Kaho：Yes. We want to make a video about Hikari River. It's our favorite place in our town.\n"
         "Daiki：Let's start taking videos of the river this weekend!\n"
         "Kaho：Wait, Daiki. Look at the poster. In Round 1, we only send a plan. If we don't pass it, we can't send a video.\n"
         "Daiki：You're right. But we have to decide which part of the river we'll show before we write the plan. There are many good places.\n"
         "Mr. Hill：That's true. After you write the plan, bring it to me. I'll check your English before you send it.\n"
         "Kaho：Thank you. If we pass Round 1, we want to take videos of the fireworks festival by the river on July 5.\n"
         "Daiki：Then we'll *edit the video after the festival and send it before the deadline.\n"
         "Mr. Hill：Good plan. And if you are chosen for the final, you'll need to practice your speech.",
         "data",
         tbl=table([["Round 1", "Send a plan for your video (in English, about 100 words).", "May 31"],
                    ["Round 2", "Teams that pass Round 1 (results: June 20) send a 3-minute video.", "July 15"],
                    ["Final", "Show your video and make a speech at Hikari City Hall.", "August 2"]],
                   header=["", "What to do", "Deadline"],
                   caption="Poster：Hikari City Video Contest ― \"The Best Place in Our Town\""),
         glossary=[("edit", "編集する")]),

    # ---------------- 問8 対話文 ----------------
    stim("E2-DIALOGUE",
         "（Riku and Mei are junior high school students in Hikari City. They are talking with Ms. Baker, "
         "their English teacher from Australia, after school.）\n\n"
         "Ms. Baker：Hi, Riku and Mei. What are you working on?\n\n"
         "Riku：Hi, Ms. Baker. We are making a report for the Hikari City Nature Contest. Our topic is *swallows.\n\n"
         "Ms. Baker：Swallows? The small birds that fly very fast?\n\n"
         "Mei：Yes. They come to Japan from southern countries in spring and make their *nests under the roofs of houses and shops. "
         "On the shopping street near our school, you can see many nests every year.\n\n"
         "Ms. Baker：Interesting. In my town in Australia, I didn't see birds' nests on shops.\n\n"
         "Riku：Look at this graph. It shows [[mark:①:the number of swallows' nests on the shopping street]] from 2015 to 2025. "
         "From 2015, the number went down for five years. In 2020, there were only twelve nests.\n\n"
         "Mei：But in 2021, the shop owners started a project called \"Swallow Guard.\" Since then, the number has gone up again, "
         "and last year it was almost the same as in 2015.\n\n"
         "Ms. Baker：That's great. What did the shop owners do?\n\n"
         "Riku：They put small boards under the nests. The boards catch the swallows' *droppings, so the street stays clean. "
         "Before the project, some owners *removed nests because customers didn't like the dirt.\n\n"
         "Ms. Baker：I see. So the boards solved the problem.\n\n"
         "Mei：We think so, but we are not sure. We want to know how people on the street feel about swallows now.\n\n"
         "Ms. Baker：Then why don't you ask them? [[blank:　　　　　　]]\n\n"
         "Riku：That's a good idea. We'll make some questions and visit the street this weekend.\n\n"
         "（A week later, Riku and Mei are talking with Ms. Baker again.）\n\n"
         "Ms. Baker：How was your *survey?\n\n"
         "Mei：We asked 20 shop owners and 50 customers, \"Are you happy that swallows come to the street?\" "
         "Here are [[mark:②:the results]].\n\n"
         "Riku：Twelve of the twenty shop owners said \"Yes.\" That's more than half. But five owners said \"No.\"\n\n"
         "Mei：On the other hand, forty of the fifty customers said \"Yes,\" and only two said \"No.\" "
         "Many customers told us that they enjoy watching the baby birds. "
         "One woman said she comes to the street with her son every week to see them.\n\n"
         "Ms. Baker：So the swallows bring people to the street. That may be good news for the shops, too.\n\n"
         "Riku：Yes! That's our idea. We also asked the owners who said \"No\" about their reasons. "
         "Most of them said, \"I like swallows, but I'm too busy to clean the boards.\"\n\n"
         "Mei：So we want to ask the volunteer club at our school to help them. "
         "If the club members clean the boards once a week, the owners don't have to do it by themselves.\n\n"
         "Ms. Baker：Wonderful. Your report is not only about birds. It's about how people and nature can live together.\n\n"
         "Riku：Thank you, Ms. Baker. We'll write that in the last part of our report.",
         "dialogue",
         glossary=[("swallow", "ツバメ"), ("nest", "巣"), ("droppings", "ふん"), ("remove ～", "～を取り除く"),
                   ("survey", "調査")]),
]


# ============================================================================
# 問題
# ============================================================================

items = []

# ---------------- 問1 リスニングテスト ----------------
LA = "（ア）は、対話の最後の発言に続くものとして最も適するものを、次の1～4の中から一つずつ選び、その番号を答えなさい。"
items += tag("Q1", [
    ("問1(ア)No.1", mc(LA,
                       ["By train. It takes about three hours.", "For five days in December.",
                        "She works at a hotel there.", "I visited Osaka last summer."],
                       "最後に How are you going to get there?（そこへどうやって行くのか）と交通手段をたずねているので、"
                       "By train.（電車で）と答えている1が適切。",
                       why={"For five days in December.": "滞在期間を答えており、交通手段の質問に合わない。",
                            "She works at a hotel there.": "姉の仕事についての発言で、質問に答えていない。",
                            "I visited Osaka last summer.": "過去の経験を述べているだけで、これからの交通手段を答えていない。"},
                       d=2, k=L, p=3, st="E2-L1")),
    ("問1(ア)No.2", mc("放送される対話を聞いて答えなさい。",
                       ["Oh, I'll look for it on his desk.", "Yes, it's on the table now.",
                        "No, I don't have science class today.", "Sure, you can use my notebook."],
                       "母親が「弟（兄）がまちがえて持っていったのかもしれない」と言っているので、"
                       "「彼の机の上を探してみる」と答える1が自然な流れ。",
                       why={"Yes, it's on the table now.": "Haruto はテーブルを探したがなかったと言っており、矛盾する。",
                            "No, I don't have science class today.": "最初に今日理科の授業で必要だと言っており、矛盾する。",
                            "Sure, you can use my notebook.": "ノートを探しているのは Haruto 自身なので、応答として不自然。"},
                       d=2, k=L, p=3, st="E2-L2")),
    ("問1(ア)No.3", mc("放送される対話を聞いて、Haruto の最後の発言として最も適するものを選びなさい。",
                       ["Thank you. Can you come to the art room after school?", "Sorry, I've never been to the festival.",
                        "Yes, I drew the picture last week.", "No, the festival was last Friday."],
                       "Yui が Can I help you?（手伝おうか）と申し出ているので、お礼を言って放課後に来てくれるよう頼む1が適切。",
                       why={"Sorry, I've never been to the festival.": "手伝いの申し出への応答になっていない。",
                            "Yes, I drew the picture last week.": "絵をかいたことはすでに話しており、申し出への応答になっていない。",
                            "No, the festival was last Friday.": "文化祭は「来週の金曜日」なので内容に合わない。"},
                       d=2, k=L, p=3, st="E2-L3")),
    ("問1(イ)No.1", mc("（イ）は、対話を聞いて、それぞれの質問の答えとして最も適するものを、次の1～4の中から一つずつ選び、その番号を答えなさい。\n"
                       "質問：What can we say about Sota?",
                       ["He is going to watch the game at Mei's house on Saturday.", "He watched the game with his father last night.",
                        "He got a goal in the last five minutes of the game.", "He finished his homework at Mei's house."],
                       "Mei が「父が試合を録画した。土曜日にうちで見られるよ」と言い、Sota は I'll come at ten. と答えているので1が適切。",
                       why={"He watched the game with his father last night.": "Sota は宿題があって試合を見られなかった。録画したのは Mei の父。",
                            "He got a goal in the last five minutes of the game.": "最後の5分で決勝点を取ったのは日本代表で、Sota ではない。",
                            "He finished his homework at Mei's house.": "宿題をした場所は述べられておらず、Mei の家に行くのは土曜日に試合を見るため。"},
                       d=3, k=L, p=4, st="E2-L4")),
    ("問1(イ)No.2", mc("質問：What can we say about Ms. Baker?",
                       ["She is going to buy a smaller green T-shirt for her son.", "She is going to buy a blue T-shirt for herself.",
                        "She thinks the T-shirt is too expensive.", "She wants a bigger T-shirt because her son is tall."],
                       "息子は緑が好きだが最初のシャツは少し大きいと言い、店員がすすめた小さいサイズの緑のシャツを I'll take it. と買うことにしたので1が適切。",
                       why={"She is going to buy a blue T-shirt for herself.": "色は緑で、10歳の息子のためのもの。",
                            "She thinks the T-shirt is too expensive.": "値段について不満は言っておらず、Perfect. と答えている。",
                            "She wants a bigger T-shirt because her son is tall.": "最初のシャツは「少し大きい」と言っており、小さいものを選んでいる。"},
                       d=3, k=L, p=4, st="E2-L5")),
    ("問1(ウ)No.1", mc("（ウ）は、英語の先生の Mr. Hill が、サマーキャンプについて生徒に話しています。次の＜ワークシート＞は、生徒の Aoi が話を聞きながら書いたものです。\n"
                       "＜ワークシート＞\n"
                       "　English Camp（August 7 – August 9）\n"
                       "　・About thirty students from （ ① ） junior high schools will join.\n"
                       "　・On the second day, we will （ ② ）.\n"
                       "　・We have to give the form to our English teacher by （ ③ ）.\n"
                       "　・Mr. Hill's message：（ ④ ）\n\n"
                       "＜ワークシート＞の（ ① ）～（ ③ ）の中に入れるものとして最も適するものをそれぞれＡ～Ｃの中から一つずつ選んだときの組み合わせとして最も適するものを、あとの1～9の中から一つ選び、その番号を答えなさい。\n"
                       "①　A. five　　B. thirty　　C. three\n"
                       "②　A. cook dinner together　　B. make a short play　　C. climb a mountain\n"
                       "③　A. July 10　　B. August 7　　C. August 9",
                       ["①-A ②-A ③-B", "①-A ②-B ③-C", "①-A ②-C ③-A", "①-B ②-A ③-A", "①-B ②-B ③-B",
                        "①-B ②-C ③-C", "①-C ②-A ③-C", "①-C ②-B ③-A", "①-C ②-C ③-B"],
                       "① about thirty students from five junior high schools より five（A）。② On the second day, you will climb a mountain より（C）。"
                       "③ give the form to your English teacher by July 10 より（A）。よって ①-A ②-C ③-A。",
                       why={"①-A ②-A ③-B": "夕食作りは1日目、8月7日はキャンプの初日で申込みの締め切りではない。",
                            "①-A ②-B ③-C": "劇を作るのは最終日、8月9日はキャンプの最終日。",
                            "①-B ②-A ③-A": "30は参加する生徒の人数で、学校の数は5。夕食作りは1日目。",
                            "①-B ②-B ③-B": "30は生徒の人数。劇は最終日、8月7日はキャンプの初日。",
                            "①-B ②-C ③-C": "30は生徒の人数。8月9日はキャンプの最終日。",
                            "①-C ②-A ③-C": "学校の数は5（three ではない）。夕食作りは1日目、8月9日は最終日。",
                            "①-C ②-B ③-A": "学校の数は5。劇を作るのは最終日。",
                            "①-C ②-C ③-B": "学校の数は5。8月7日はキャンプの初日。"},
                       d=3, k=L, p=4, st="E2-L6", keep=True, ai=2)),
    ("問1(ウ)No.2", mc("＜ワークシート＞の（ ④ ）の中に入れるものとして最も適するものを、次の1～4の中から一つ選び、その番号を答えなさい。",
                       ["Don't be afraid of making mistakes, and try to speak a lot.",
                        "Practice English hard before the camp so that you won't make mistakes.",
                        "Make a short play in English with your family.",
                        "Speak English only when you are sure your English is perfect."],
                       "Mr. Hill は Mistakes are a part of learning. So please don't worry, and try to speak a lot. と伝えている。"
                       "自分の経験（まちがいを恐れて話さなかった）も話の中心なので1が適切。",
                       why={"Practice English hard before the camp so that you won't make mistakes.": "「まちがいをしないように」ではなく「まちがいは学習の一部」と言っている。",
                            "Make a short play in English with your family.": "劇はキャンプ最終日にグループで作るもので、家族と作るという話ではない。",
                            "Speak English only when you are sure your English is perfect.": "完璧でなくても聞いてもらえたと話しており、メッセージと正反対。"},
                       d=3, k=L, p=4, st="E2-L6")),
])

# ---------------- 問2 語彙 ----------------
items += tag("Q2", [
    ("問2(ア)", mc("This bag is too (　　　) for me to carry. Can you help me?",
                  ["heavy", "quiet", "polite", "empty"],
                  "too ～ for … to ―「…が―するには～すぎる」。運ぶのを手伝ってほしいのだから heavy（重い）が適切。",
                  why={"quiet": "「静かな」。かばんを運べない理由にならない。",
                       "polite": "「礼儀正しい」。人について使う語で文意に合わない。",
                       "empty": "「空の」。空なら軽くて運べるので、手伝いを頼む流れに合わない。"},
                  d=1, k=V, p=2)),
    ("問2(イ)", mc("There is a big (　　　) near my house. I often go there to borrow books.",
                  ["library", "kitchen", "stadium", "hospital"],
                  "本を借りに行く場所なので library（図書館）が適切。",
                  why={"kitchen": "「台所」。家の近くにあって本を借りに行く場所ではない。",
                       "stadium": "「競技場」。本を借りる場所ではない。",
                       "hospital": "「病院」。本を借りる場所ではない。"},
                  d=1, k=V, p=2)),
    ("問2(ウ)", mc("I couldn't (　　　) the answer to the last question, so I asked my teacher about it.",
                  ["find", "wear", "spend", "lose"],
                  "find the answer で「答えを見つける」。答えがわからなかったので先生に聞いた、という流れ。",
                  why={"wear": "「身につける」。answer を目的語にとれない。",
                       "spend": "「（時間・お金を）使う」。answer を目的語にとれない。",
                       "lose": "「失う」。答えを失ったから先生に聞く、では意味が通らない。"},
                  d=2, k=V, p=2)),
])

# ---------------- 問3 文法 ----------------
items += tag("Q3", [
    ("問3(ア)", mc("A：How long have you lived in Hikari City?\nB：I (　　　) here since I was five.",
                  ["have lived", "lived", "am living", "was living"],
                  "since I was five（5歳のときから）と、過去から現在まで続く状態を表しているので現在完了 have lived が適切。",
                  why={"lived": "過去形では「今も住んでいる」ことを表せず、since とも合わない。",
                       "am living": "現在進行形は since ～ と組み合わせて継続を表せない。",
                       "was living": "過去進行形では現在までの継続を表せない。"},
                  d=2, k=G, p=2)),
    ("問3(イ)", mc("A：Which do you want to drink, tea or coffee?\nB：(　　　) is fine. I like both of them.",
                  ["Either", "Neither", "Each", "Nothing"],
                  "二つのうち「どちらでも」は either。I like both of them. とあるので「どちらでもいい」となる Either が適切。",
                  why={"Neither": "「どちらも～ない」となり、両方好きだという文と合わない。",
                       "Each": "「それぞれ」。どちらにするかの答えとして不自然。",
                       "Nothing": "「何も～ない」。二つから選ぶ問いの答えにならない。"},
                  d=2, k=G, p=2)),
    ("問3(ウ)", mc("A：Do you know (　　　) the next bus will come?\nB：In ten minutes, I think.",
                  ["when", "where", "who", "which"],
                  "間接疑問。B が In ten minutes（10分後に）と時を答えているので when が適切。",
                  why={"where": "場所をたずねる語。B は時を答えている。",
                       "who": "人をたずねる語。B の答えと合わない。",
                       "which": "「どちら（の）」。B の答えと合わない。"},
                  d=2, k=G, p=2)),
    ("問3(エ)", mc("A：Thank you for (　　　) me with my homework.\nB：You're welcome.",
                  ["helping", "help", "helped", "to help"],
                  "前置詞 for の後ろに動詞を置くときは動名詞（～ing）にする。Thank you for helping me. で「手伝ってくれてありがとう」。",
                  why={"help": "前置詞の後ろに動詞の原形は置けない。",
                       "helped": "前置詞の後ろに過去形は置けない。",
                       "to help": "前置詞の後ろに to 不定詞は置けない。"},
                  d=2, k=G, p=2)),
])

# ---------------- 問4 語順整序（3番目・5番目） ----------------


def _ord(sub, dialogue, words, sentence, third, fifth, e3, e5, unused):
    """問4の小問1つを「3番目」「5番目」の2つのマーク欄にする。words は番号順（1～6）。"""
    def why2(correct, pos):
        out = {}
        tokens = sentence.rstrip(".?!").split()
        for w in words:
            if w == correct:
                continue
            if w == unused:
                out[w] = f"不要な語。{w} は使わない。"
            else:
                out[w] = f"{w} は（　）内の{tokens.index(w) + 1}番目にくる語で、{pos}番目ではない。"
        return out

    numbered = "　".join(f"{i}. {w}" for i, w in enumerate(words, 1))
    stem3 = f"{dialogue.replace('＿', f'（　{numbered}　）')}\n▶（{sub}）の（　）内で3番目にくる語"
    stem5 = f"▶（{sub}）の（　）内で5番目にくる語"
    tokens = sentence.rstrip(".?!").split()
    assert tokens[2] == third and tokens[4] == fifth and unused not in tokens and len(tokens) == 5, sub
    exp = f"正しい順：{' '.join(tokens)}（不要な語：{unused}）。"
    return [
        (f"問4({sub})3番目", mc(stem3, words, exp + e3, why=why2(third, 3), d=3, k=G, p=2, keep=True, ai=words.index(third))),
        (f"問4({sub})5番目", mc(stem5, words, exp + e5, why=why2(fifth, 5), d=3, k=G, p=2, keep=True, ai=words.index(fifth))),
    ]


items += tag("Q4",
             _ord("ア", "A：This cake is delicious! Did you make it?\nB：Yes. My grandmother ＿ it.",
                  ["how", "make", "taught", "what", "to", "me"], "taught me how to make",
                  "how", "make",
                  "teach ＋人＋how to ～ で「（人）に～のしかたを教える」。3番目は how。",
                  "how to make it で「それの作り方」。5番目は make。", "what")
             + _ord("イ", "A：Whose umbrella is this?\nB：I think it belongs to ＿ with Ms. Baker over there.",
                    ["girl", "is", "the", "talking", "who", "which"], "the girl who is talking",
                    "who", "talking",
                    "人を説明する主格の関係代名詞は who。the girl who is talking で「話している女の子」。3番目は who。",
                    "who の後ろは is talking（現在進行形）。5番目は talking。which は人以外に使うので不要。", "which")
             + _ord("ウ", "A：Have you finished your report for the English class?\nB：No. It's ＿ in English.",
                    ["write", "of", "difficult", "to", "me", "for"], "difficult for me to write",
                    "me", "write",
                    "It is ～ for ＋人＋ to … で「（人）にとって…することは～だ」。difficult for me と続くので3番目は me。",
                    "to の後ろは動詞の原形 write。5番目は write。of は It is kind of you のように人の性質を表す形容詞のときに使うので不要。", "of")
             + _ord("エ", "A：What did you think of the movie?\nB：It was the ＿ seen.",
                    ["ever", "movie", "exciting", "I've", "most", "more"], "most exciting movie I've ever",
                    "movie", "ever",
                    "the most ＋形容詞＋名詞 で最上級。the most exciting movie と続くので3番目は movie。",
                    "movie を I've ever seen（今までに見た）が後ろから説明する。5番目は ever。more は比較級で the とは使わないので不要。", "more"))

# ---------------- 問5 条件英作文 ----------------
items += tag("Q5", [
    ("問5", desc("次のＡ～Ｃの絵と英文は、中学生の Sota と、カナダからの留学生の Tom の間の出来事を表しています。"
                "Ｂの場面で、Sota は何と言ったと考えられますか。あとの＜条件＞にしたがって、[[blank:　　]]の中に入れるのに適する英文を書きなさい。\n\n"
                "＜最初の英文＞\n"
                "Sota found a poster at Hikari Station. It was about Hikari Aquarium.\n\n"
                "＜条件＞\n"
                "①　aquarium, new, opens の3語を必ず用いること。\n"
                "②　[[blank:　　]]内を7語以上の1文で書くこと。\n"
                "③　[[blank:　　]]のあとに続く Do you want to go there with me? につながる内容にすること。\n"
                "※　短縮形（I'm など）は1語と数え、符号（, など）は語数に含めません。",
                "A new penguin area opens at Hikari Aquarium on April 29.",
                "ポスター（Ａ）には「新しいペンギンエリアが4月29日にオープンする」とある。Ｃで Tom が I love penguins. と答えているので、"
                "Ｂでは新しいペンギンのエリアができることを伝え、そのあとの Do you want to go there with me? につなげる。"
                "opens は主語が3人称単数の現在形（決まった予定を表す）なので、主語は A new ～ area のように単数にする。"
                "別解例：Hikari Aquarium opens a new area for penguins this month.（10語）など。",
                [("aquarium, new, opens の3語を用い、7語以上の1文になっている", 2),
                 ("ポスターの内容（新しいペンギンのエリアがオープンすること）を伝え、あとの英文につながっている", 2),
                 ("文法・つづりの誤りがない（主語と opens の一致など）", 1)],
                d=4, k=W, p=5, lines=2,
                fig=figure("問5の絵：Ａ 駅でポスター（Hikari Aquarium・NEW! Penguin Area・Opens on April 29!）を見る Sota。"
                           "Ｂ Sota が Tom に話しかける場面（Sota: Hi, Tom. ［空欄］ Do you want to go there with me?）。"
                           "Ｃ Tom が喜んで答える場面（Tom: Sure! I love penguins. How about next Sunday?）。",
                           svg=_story_figure()))),
])

# ---------------- 問6 スピーチ ----------------
PAIRS8 = ["aとc", "aとe", "bとd", "bとf", "cとd", "cとf", "dとe", "eとf"]
items += tag("Q6", [
    ("問6(ア)", mc("本文中の――線部 this graph の内容を表したものとして最も適するものを、次の1～4の中から一つ選び、その番号を答えなさい。",
                  ["1のグラフ", "2のグラフ", "3のグラフ", "4のグラフ"],
                  "本文の内容は「2021年は120件、その後毎年増え、2023年は2021年の2倍（240件）」「Clothes が毎年最も多い」"
                  "「Toys は2021年に最も少なかったが、2023年には5倍（10→50）になり、Bicycles と同じ数」。すべてに合うのは4のグラフ。",
                  why={"1のグラフ": "年の並びが逆で、2021年が240件、2023年が120件になっている（毎年増えたという内容に合わない）。",
                       "2のグラフ": "2021年は Bicycles が最も少なく、Toys（30）は最も少ない部分ではない。Toys も5倍になっていない。",
                       "3のグラフ": "2022年は Others（80）が最も多く、「Clothes が毎年最も多い」に合わない。"},
                  d=3, k=D, p=5, keep=True, ai=3,
                  fig=figure("Repair Café に持ちこまれた物の数（2021～2023年）を表す積み上げ棒グラフ4つ（Clothes・Bicycles・Toys・Others、架空の資料）",
                             svg=_stack_figure(), caption="（架空の資料）"))),
    ("問6(イ)", mc("本文中の（ ① ）～（ ③ ）の中に、次のＡ～Ｃを意味が通るように入れるとき、その組み合わせとして最も適するものを、あとの1～6の中から一つ選び、その番号を答えなさい。\n"
                  "A. Children can see how their toys are repaired, and some of them try to use the tools by themselves.\n"
                  "B. They are always happy to teach visitors, so you don't have to be good at repairing.\n"
                  "C. I learned that we sometimes need help from people who have special skills.",
                  ["①-A ②-B ③-C", "①-A ②-C ③-B", "①-B ②-A ③-C", "①-B ②-C ③-A", "①-C ②-A ③-B", "①-C ②-B ③-A"],
                  "① 直前でボランティアについて説明しているので、They（＝ボランティア）を主語にした B。"
                  "② 直前で「親が子どもと来る」とあるので、子どもについての A。"
                  "③ 部品がなくゲーム機を直せなかった話のあと、専門店のリストを作っていると続くので、専門の技術をもつ人の助けが必要だという C。",
                  why={"①-A ②-B ③-C": "①の段階ではまだ子どもの話が出ておらず、②の直前の「親が子どもと来る」に B はつながらない。",
                       "①-A ②-C ③-B": "①に子どもの話は合わず、③の直前の「直せなかった」話に「ボランティアは喜んで教える」はつながらない。",
                       "①-B ②-C ③-A": "②の直前は子ども連れの話なので C は合わず、③の直前の「直せなかった」話に A は合わない。",
                       "①-C ②-A ③-B": "①の直前はボランティアの説明で、専門的な技術の話（C）はつながらない。",
                       "①-C ②-B ③-A": "①に C、③に A はどちらも前後の内容とつながらない。"},
                  d=3, k=R, p=5, keep=True, ai=2)),
    ("問6(ウ)", mc("次のａ～ｆの中から、本文の内容に合うものを二つ選んだときの組み合わせとして最も適するものを、あとの1～8の中から一つ選び、その番号を答えなさい。\n"
                  "a. Nana's grandmother told her about the Repair Café when her bag was broken.\n"
                  "b. The volunteers at the Repair Café are people who repair things as their job.\n"
                  "c. Nana repaired the zipper of her bag by herself without any help.\n"
                  "d. More than half of the things brought to the café in 2023 were toys.\n"
                  "e. The volunteers couldn't repair a video game machine because they didn't have the parts.\n"
                  "f. Nana thinks repairing things is a fast way to save money.",
                  PAIRS8,
                  "a：かばんのファスナーが壊れたとき、祖母が Repair Café をすすめた（正）。"
                  "e：部品がなかったのでゲーム機は直せなかった（正）。"
                  "b はボランティアは専門家ではない、c は Mr. Kato が教えてくれた、d は2023年の Toys は240件中50件、"
                  "f は「修理には時間がかかる」と述べており、いずれも誤り。",
                  why={"aとc": "c は誤り。Mr. Kato がファスナーの替え方を教えてくれた。",
                       "bとd": "b はボランティアは専門家ではないので誤り。d は Toys は240件中50件なので誤り。",
                       "bとf": "b・f ともに誤り。修理は時間がかかると述べている。",
                       "cとd": "c・d ともに誤り。",
                       "cとf": "c・f ともに誤り。",
                       "dとe": "d は誤り。2023年の Toys は240件中50件で半分に満たない。",
                       "eとf": "f は誤り。Nana は修理は時間がかかるが物を大切に思えるようになると述べており、早くお金を節約する方法とは言っていない。"},
                  d=3, k=R, p=5, keep=True, ai=1)),
])

# ---------------- 問7 資料の読み取り ----------------
items += tag("Q7", [
    ("問7(ア)", mc("（ア）の英文中の[[blank:　　]]の中に入れるのに最も適するものを、次の1～5の中から一つ選び、その番号を答えなさい。",
                  ["2:20", "1:30", "2:00", "2:40", "3:00"],
                  "土曜日の午後に開いていて料理道具を売っているのは Hikari Mall（Green Kitchen は14時に閉店）。"
                  "駅から店まで歩いて20分、店に1時間、店から駅まで20分の合計1時間40分かかる。4:00までに駅に戻るには、"
                  "4:00の1時間40分前の 2:20 に会えばよい。Sota は「できるだけ遅く会いたい」と言っているので 2:20。",
                  why={"1:30": "Sota が駅に着ける最も早い時刻。Sota はできるだけ遅く会いたいと言っている。",
                       "2:00": "4:00までに戻れるが、まだ遅くできるので「できるだけ遅く」に合わない。",
                       "2:40": "店で1時間過ごし、往復40分歩くと駅に戻るのが4:20になり、ピアノのレッスンに間に合わない。",
                       "3:00": "店までの往復の時間や店にいる時間を考えると、4:00までに駅に戻れない。"},
                  d=4, k=D, p=5, st="E2-CHAT")),
    ("問7(イ)", mc("（イ）の英文と Poster を読み、Kaho たちの＜To-Do List＞の ① ～ ⑤ に、あとの(ア)～(オ)を入れるとき、その組み合わせとして最も適するものを、あとの1～5の中から一つ選び、その番号を答えなさい。\n"
                  "＜To-Do List＞\n"
                  "　① → ② → ③ → Send the plan（by May 31）→ ④ → Send the video（by July 15）→ ⑤\n"
                  "(ア) Take videos of the fireworks festival.\n"
                  "(イ) Ask Mr. Hill to check the plan.\n"
                  "(ウ) Choose the place on Hikari River for the video.\n"
                  "(エ) Practice the speech for the final.\n"
                  "(オ) Write the plan in English.",
                  ["①-(ウ) ②-(オ) ③-(イ) ④-(ア) ⑤-(エ)", "①-(オ) ②-(ウ) ③-(イ) ④-(ア) ⑤-(エ)",
                   "①-(ウ) ②-(イ) ③-(オ) ④-(ア) ⑤-(エ)", "①-(ア) ②-(ウ) ③-(オ) ④-(イ) ⑤-(エ)",
                   "①-(ウ) ②-(オ) ③-(イ) ④-(エ) ⑤-(ア)"],
                  "計画を書く前に川のどこを見せるか決め（ウ）、計画を英語で書き（オ）、送る前に Mr. Hill に確認してもらう（イ）。"
                  "Round 1 を通過したら7月5日の花火大会を撮影し（ア）、7月15日までに動画を送る。決勝に選ばれたらスピーチを練習する（エ）。",
                  why={"①-(オ) ②-(ウ) ③-(イ) ④-(ア) ⑤-(エ)": "Daiki が「計画を書く前に、どの場所を見せるか決めなければならない」と言っている。",
                       "①-(ウ) ②-(イ) ③-(オ) ④-(ア) ⑤-(エ)": "Mr. Hill は計画を書いたあとに持ってくるよう言っており、書く前には確認できない。",
                       "①-(ア) ②-(ウ) ③-(オ) ④-(イ) ⑤-(エ)": "花火大会は7月5日で、Round 1 の計画の締め切り（5月31日）より後。また Mr. Hill の確認は計画を送る前。",
                       "①-(ウ) ②-(オ) ③-(イ) ④-(エ) ⑤-(ア)": "花火大会の撮影は動画を送る（7月15日）前にしなければならない。スピーチの練習は決勝に選ばれてから。"},
                  d=4, k=D, p=5, st="E2-POSTER")),
])

# ---------------- 問8 対話文 ----------------
COMB9 = [f"①：{a}　②：{b}" for a in "ABC" for b in "XYZ"]
items += tag("Q8", [
    ("問8(ア)", mc("本文中の――線①、②が表す内容を、①はア群、②はイ群の中からそれぞれ選んだときの組み合わせとして最も適するものを、あとの1～9の中から一つ選び、その番号を答えなさい。",
                  COMB9,
                  "① 本文では「2015年から5年間減り続け、2020年は12個」「2021年から再び増え、昨年（2025年）は2015年とほぼ同じ」と述べているので B。"
                  "A は2020年以降増えておらず、C は2018年が最も少ない。"
                  "② 店主20人のうち Yes 12人・No 5人、客50人のうち Yes 40人・No 2人なので Z。X は店主の Yes と No が逆、Y は客の No と Not sure が逆。",
                  why={c: r for c, r in zip(COMB9, [
                      "① A は2020年以降ほとんど増えていない。② X は店主の Yes と No が逆。",
                      "① A は2020年以降ほとんど増えていない。② Y は客の No が8人になっている。",
                      "① A は2020年以降ほとんど増えておらず、「昨年は2015年とほぼ同じ」に合わない。",
                      "② X は店主の Yes が5人、No が12人で、本文と逆。",
                      "② Y は客の No が8人で、「No は2人だけ」に合わない。",
                      None,
                      "① C は2018年に12個で最も少なく、「2020年は12個」「5年間減り続けた」に合わない。② X も誤り。",
                      "① C は5年間減り続けていない。② Y も誤り。",
                      "① C は2018年が最も少なく、本文と合わない。"]) if r},
                  d=4, k=D, p=5, keep=True, ai=5,
                  fig=figure("ア群：ツバメの巣の数（2015～2025年）の折れ線グラフ A・B・C。イ群：店主20人と客50人の回答（Yes・No・Not sure）を表す棒グラフの組 X・Y・Z（架空の資料）",
                             svg=_swallow_figure(), caption="（架空の資料）"))),
    ("問8(イ)", mc("本文中の[[blank:　　　]]の中に入れるのに最も適するものを、次の1～4の中から一つ選び、その番号を答えなさい。",
                  ["You can learn what they really think by talking with them.",
                   "You should stop writing the report about swallows.",
                   "You can find the answer in the graph you made.",
                   "You don't need to visit the shopping street again."],
                  "Mei が「通りの人々がツバメをどう思っているか知りたい」と言い、Ms. Baker が「聞いてみたら？」とすすめている。"
                  "そのあと Riku が質問を作って通りを訪ねると答えているので、話を聞けば本当の気持ちがわかるという1が適切。",
                  why={"You should stop writing the report about swallows.": "Ms. Baker はレポート作りを応援しており、やめるよう言う流れではない。",
                       "You can find the answer in the graph you made.": "グラフは巣の数を示すだけで、人々の気持ちはわからない。直前の「聞いてみたら」にもつながらない。",
                       "You don't need to visit the shopping street again.": "直後に Riku が「今週末に通りを訪ねる」と答えており、つながらない。"},
                  d=3, k=R, p=5)),
    ("問8(ウ)", mc("次のａ～ｆの中から、本文の内容に合うものを二つ選んだときの組み合わせとして最も適するものを、あとの1～8の中から一つ選び、その番号を答えなさい。\n"
                  "a. Ms. Baker often saw swallows' nests on shops in her town in Australia.\n"
                  "b. The number of nests on the shopping street in 2020 was smaller than in 2015.\n"
                  "c. The shop owners started to put boards under the nests before 2015.\n"
                  "d. Riku and Mei asked more customers than shop owners in their survey.\n"
                  "e. Most of the customers said that they were not happy about swallows.\n"
                  "f. Riku and Mei are going to ask the shop owners to clean the boards every day.",
                  ["bとd", "aとc", "aとe", "bとf", "cとd", "cとf", "dとe", "eとf"],
                  "b：2015年から5年間減り、2020年は12個（正）。d：店主20人、客50人に聞いた（正）。"
                  "a は Ms. Baker の町では見なかった、c は板を置き始めたのは2021年、e は客50人中40人が Yes、"
                  "f は店主ではなく学校のボランティア部に週1回の掃除を頼みたいと言っているので、いずれも誤り。",
                  why={"aとc": "a・c ともに誤り。Ms. Baker の町では見なかった。板は2021年から。",
                       "aとe": "a・e ともに誤り。客の多く（40人）は Yes と答えた。",
                       "bとf": "f は誤り。掃除を頼みたいのは学校のボランティア部で、週1回。",
                       "cとd": "c は誤り。Swallow Guard は2021年に始まった。",
                       "cとf": "c・f ともに誤り。",
                       "dとe": "e は誤り。客50人中40人が Yes と答えた。",
                       "eとf": "e・f ともに誤り。"},
                  d=3, k=R, p=5, keep=False)),
])

SECTIONS = [
    {"id": "Q1", "title": "問1",
     "instructions": "リスニングテスト（放送の指示にしたがって答えなさい。放送を聞きながらメモをとってもかまいません。）"},
    {"id": "Q2", "title": "問2", "page_break": True,
     "instructions": "次の英文の（　）の中に入れるのに最も適するものを、あとの1～4の中からそれぞれ一つずつ選び、その番号を答えなさい。"},
    {"id": "Q3", "title": "問3",
     "instructions": "次の英文の（　）の中に入れるのに最も適するものを、あとの1～4の中からそれぞれ一つずつ選び、その番号を答えなさい。"},
    {"id": "Q4", "title": "問4", "page_break": True,
     "instructions": "次の(ア)～(エ)の対話が成り立つように、（　）内の六つの語の中から五つを選んで正しい順番に並べたとき、"
                     "その（　）内で3番目と5番目にくる語の番号をそれぞれ答えなさい。（それぞれ一つずつ不要な語があるので、その語は使用しないこと。）"},
    {"id": "Q5", "title": "問5", "page_break": True},
    {"id": "Q6", "title": "問6", "page_break": True,
     "instructions": "次の英文は、中学生の Nana が英語の授業で行ったスピーチの原稿です。英文を読んで、あとの各問いに答えなさい。",
     "stimulus_refs": ["E2-SPEECH"]},
    {"id": "Q7", "title": "問7", "page_break": True,
     "instructions": "次の(ア)の英文と List、(イ)の英文と Poster について、それぞれあとの問いに答えなさい。"},
    {"id": "Q8", "title": "問8", "page_break": True,
     "instructions": "次の英文を読んで、あとの各問いに答えなさい。",
     "stimulus_refs": ["E2-DIALOGUE"]},
]

SETS = [{
    "set_id": "KNG-MOCK-R8-02-ENG",
    "track": "mock_exam",
    "stage": "junior_high",
    "subject": "english",
    "grade": "JH3",
    "unit_ids": [U],
    "title": "神奈川県公立高校入試形式　オリジナル模試（第2回）　英語",
    "subtitle": "50分・100点",
    "time_limit_minutes": 50,
    "total_points": 100,
    "labels": "num",
    "exam_format": "kanagawa",
    "exam_spec": {
        "name": "神奈川県公立高校入試形式　オリジナル模試（第2回）　英語",
        "reference": "神奈川県公立高校入試（共通選抜）の問題冊子の構成を参考に作成したオリジナル問題",
        "answer_format": "mixed",
        "notes": "問1～問8の大問構成と解答形式（マークシート中心、問5のみ英文記述）は実際の問題冊子にならったが、"
                 "本文・資料・設問はすべてオリジナルで、グラフ・表の数値は架空のもの。配点はこの模試独自の配分であり、実際の入試の配点とは異なる。"
                 "問4は解答用紙に合わせて3番目・5番目を別々のマーク欄（各2点）とした。問1の放送文は解答・解説冊子に掲載。",
    },
    "sections": SECTIONS,
    "stimuli": STIMULI,
    "build": {"show_points": True, "show_difficulty": False},
    "out": "data/mock_exam/kng_mock_r8_02_eng.json",
    "items": items,
}]
