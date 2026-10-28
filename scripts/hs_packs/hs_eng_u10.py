"""単元パック：論理・表現Ⅰ 英作文（和文英訳・意見文・論理展開）。"""
from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "HS-ENG-U10"


def cap(s):
    return s[0].upper() + s[1:]


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["和文英訳で、日本語を英語にしやすい日本語に言いかえ（和文和訳）、主語と動詞を決めてから英文を組み立てられる。",
           "意見文を「主張 → 理由 → 具体例 → 結論」の構成で、論理のつながりを示す表現を使って書ける。",
           "理由が主張を支えているか、結論が主張と一致しているかを点検し、論理の飛躍を直せる。"],
    duration=50,
    readiness=["中学3年の条件英作文で、I think ～ because … の形で意見と理由を書ける。",
               "5文型・時制・関係詞など、高校1年で学んだ文法事項を使える（HS-ENG-U01〜U08）。",
               "可算名詞・不可算名詞、冠詞 a / the の基本的な使い分けを知っている。"],
    flow=[("導入：直訳の落とし穴", 5, "「この町は多くの人が住んでいる」を直訳した This town lives many people. の誤りを考えさせる"),
          ("和文英訳の手順", 13, "和文和訳 → 主語と動詞の決定 → 文型・時制の確認の手順を示す（例題1）"),
          ("意見文の構成", 12, "主張・理由・具体例・結論の4つの部分と、それぞれで使う表現を整理する（例題2）"),
          ("論理展開の点検", 13, "理由が主張を支えているか、具体例が理由に合っているかを点検する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "英作文は「日本語をそのまま置きかえる」作業ではない",
              "「この町は多くの人が住んでいる」を語順どおりに英語にすると This town lives many people. となるが、これは「この町が多くの人を住まわせている」という意味不明な文になる。日本語の「は」は話題を示すだけで、英語の主語とは限らない。英作文では、まず「誰が・何が、どうする」という英語の骨組みを決め、それに合うように日本語を言いかえる必要がある。また、意見を述べる文章では、英語の読み手は「主張が先、理由が後」という順序を期待している。",
              bullets=["「この町は多くの人が住んでいる」→「多くの人がこの町に住んでいる」→ Many people live in this town.",
                       "英語の意見文：主張（I think …）→ 理由（First, … Second, …）→ 結論（For these reasons, …）",
                       "論理のつながりは、ディスコースマーカーで読み手に示す。"],
              points=[tp("直訳の文を板書し、どこがおかしいかを生徒に指摘させる。", ask="This town lives many people. の主語と動詞は何か。町は「住む」のか。",
                         expect="主語は This town、動詞は lives。住むのは人なので、主語を many people にする。", timing="導入の冒頭"),
                      tp("英作文の採点では「伝わるか」と「文法の正確さ」の両方が見られることを最初に伝える。")]),
        definition("df1", "和文英訳の手順",
                   "和文英訳では、日本語の表現をそのまま英語に置きかえるのではなく、英語にしやすい日本語に言いかえてから訳す。この言いかえを和文和訳という。",
                   bullets=["① 和文和訳：比喩・慣用句・省略を、意味が同じ平易な日本語に直す（「目が回るほど忙しい」→「とても忙しい」）。",
                            "② 主語を決める：日本語の「～は」が主語とは限らない。省略された主語（私・人々）を補う。",
                            "③ 動詞と文型を決める：主語に合う動詞を選び、目的語・補語の形を決める。",
                            "④ 時制・数・冠詞を確認する：過去か現在か、名詞は単数か複数か、a / the / 無冠詞か。",
                            "⑤ 書いた英文を日本語に訳し戻し、元の意味とずれていないかを確かめる。"],
                   conditions=["知らない単語は、知っている単語で言いかえる（「渋滞」→ a lot of cars on the road）。",
                               "日本語の「～こと」は、英語では不定詞・動名詞・that 節のどれかで表す。"],
                   points=[tp("「和文和訳」の練習として、慣用句を含む日本語を平易な日本語に直す活動を2〜3問行う。", caution="難しい単語を探すことに時間をかけすぎ、文の骨組みが崩れる答案が多い。")]),
        theorem("th1", "意見文の基本構成",
                "主張（Introduction）→ 理由1・理由2（Body：理由＋具体例）→ 結論（Conclusion：主張の言いかえ）",
                ["主張は最初の1文で、賛成か反対かをはっきり述べる（I agree / disagree that … ／ I think …）。",
                 "理由は First, / Second, / In addition, などで示し、それぞれに具体例や説明を1文以上つける。",
                 "結論は For these reasons, / In conclusion, などで始め、主張を別の言葉で言いかえる。新しい理由は加えない。"],
                body="反対の意見に触れる場合は、Some people say that …, but … のように一度認めてから、自分の主張に戻る（譲歩）。これにより主張がより説得力をもつ。",
                points=[tp("4つの部分を色分けしたモデル文を示し、各部分で使われている表現に下線を引かせる。",
                           ask="結論の段落に新しい理由を書いてもよいか。", expect="よくない。結論は主張のまとめで、理由は本論で述べる。")]),
        derivation("dv1", "論理展開を組み立てる手順（なぜ主張を最初に書くのか）",
                   ["① テーマに対して賛成か反対かを決める。書きやすい理由が2つ思いつく立場を選ぶ。",
                    "② 理由を2つ、日本語でメモする。2つの理由が同じ内容の言いかえになっていないかを確かめる。",
                    "③ それぞれの理由に、具体例（自分の経験・身近な例）や説明を1つずつ加える。",
                    "④ 主張 → 理由1＋例 → 理由2＋例 → 結論 の順に並べる。読み手は最初に主張を知ることで、後の理由を「主張を支える材料」として読める。",
                    "⑤ 各文のつながりに First / For example / In addition / For these reasons などを入れる。",
                    "⑥ 点検：理由は主張を支えているか、例は理由に合っているか、結論は主張と一致しているか。"],
                   body="日本語の作文では結論を最後に書くことが多いが、英語の論理的な文章では主張を最初に示すのが基本である。主張が先にあれば、読み手は各理由がどの主張を支えているのかを迷わずに理解できる。",
                   points=[tp("手順②で「2つの理由が実は同じこと」になっている例（便利だから／役に立つから）を示し、理由の重なりに気づかせる。",
                              ask="「便利だから」と「役に立つから」は別の理由と言えるか。", expect="ほぼ同じ内容なので、別の観点（費用・健康など）の理由を考える必要がある。", timing="手順②の説明時")]),
        example("ex1", "例題1　和文和訳してから英訳する",
                "次の日本語を英語に直しなさい。「この町は多くの人が住んでいる。」",
                ["和文和訳：「多くの人がこの町に住んでいる」と言いかえる。", "主語：住むのは人なので many people。動詞：live（自動詞）なので場所は in this town。",
                 "時制：現在の状態なので現在形。"],
                "Many people live in this town.（This town has a large population. も可）",
                thinking="日本語の「～は」をそのまま主語にせず、動詞（住む）の動作主を主語にする。",
                points=[tp("別解の This town has a large population. を示し、「町」を主語にするなら動詞を変えればよいことを確認する。")],
                misconceptions=[("This town lives many people.", "live の主語は人。Many people live in this town. とする")]),
        example("ex2", "例題2　意見文の構成",
                "「高校生は毎日新聞を読むべきだ」というテーマについて、主張・理由・具体例・結論の順に、各1文で英文を書きなさい。",
                ["主張：I think high school students should read a newspaper every day.",
                 "理由：First, newspapers help us understand what is happening in society.",
                 "具体例：For example, we can learn about elections and the economy, which we will need to know about as adults.",
                 "結論：For these reasons, I believe reading a newspaper is a good habit for high school students."],
                "I think high school students should read a newspaper every day. First, newspapers help us understand what is happening in society. For example, we can learn about elections and the economy, which we will need to know about as adults. For these reasons, I believe reading a newspaper is a good habit for high school students.",
                thinking="主張は1文目で立場をはっきりさせ、結論は主張を別の言葉で言いかえる。",
                points=[tp("結論の文が主張の単なるくり返しにならないよう、言いかえ（should read → a good habit）を工夫させる。", ask="主張と結論で、言い方はどう変わっているか。",
                           expect="should read every day が is a good habit に言いかえられている。")]),
        example("ex3", "例題3　論理のつながりを点検する",
                "次の意見文の論理的な問題点を指摘しなさい。\nI think students should not use smartphones at school. First, smartphones are very useful for looking up words. For these reasons, smartphones should not be used at school.",
                ["主張は「学校でスマートフォンを使うべきではない」。", "理由は「単語を調べるのにとても便利だ」で、これは使うことに賛成する理由になっている。",
                 "理由が主張を支えておらず、むしろ反対の立場の理由になっている。また理由が1つなのに For these reasons と複数形になっている。"],
                "理由（便利である）が主張（使うべきではない）を支えていない。たとえば First, smartphones can distract students from their lessons. のように、主張を支える理由に直す必要がある。また、理由が1つなら For this reason とする。",
                thinking="各理由の文の前に「なぜなら」をつけて主張とつなげ、意味が通るかを確かめる。",
                points=[tp("「主張＋なぜなら＋理由」と日本語で読み上げさせ、つながらないことを体感させる。")]),
        board("bd1", "板書案",
              [("① 和文英訳の手順", ["和文和訳（易しい日本語に）", "主語を決める（「は」≠主語）", "動詞・文型を決める", "時制・数・冠詞を確認", "訳し戻して確認"]),
               ("② 意見文の構成", ["主張：I think …", "理由：First, / Second,", "具体例：For example,", "結論：For these reasons,", "譲歩：Some people say …, but"]),
               ("③ 論理の点検", ["理由 → 主張を支えるか", "例 → 理由に合うか", "結論 ＝ 主張の言いかえ", "理由どうしが重なっていないか", "結論に新しい理由を書かない"])],
              points=[tp("②は生徒の作文用テンプレートとしてノートに写させ、問題プリントの C の意見文で使わせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("和文英訳では、書き始める前に必ず「主語と動詞」を日本語でメモさせる。", ask="この文で、動作をしているのは誰（何）か。", expect="日本語の「～は」ではなく、動詞の動作主。"),
               tp("名詞の単数・複数と冠詞は、最後の見直しで必ず点検させる。", caution="school uniform is ／ protect environment など、数と冠詞の誤りは減点が積み重なりやすい。"),
               tp("意見文の理由は「自分にとって」ではなく「多くの人に当てはまる」理由にすると説得力が増すことを伝える。", timing="例題2の後"),
               tp("語数の指定がある場合は、主張1文・理由2つ（各2文）・結論1文で約60語になることを目安として示す。"),
               tp("問題プリント D の誤答例を使い、「日本語の直訳による誤り」と「論理のつながりの誤り」の2種類を扱う。")],
              misconceptions=[("This town lives many people.", "日本語の「は」を主語にした誤り。Many people live in this town."),
                              ("Because it rained yesterday. The game was canceled.", "because の節だけでは文にならない。Because it rained yesterday, the game was canceled."),
                              ("結論の段落で新しい理由を加える。", "結論は主張の言いかえ。理由は本論で述べる")]),
        summary("sm1", "まとめ",
                ["和文英訳は、和文和訳 → 主語・動詞の決定 → 時制・数・冠詞の確認 → 訳し戻し、の順で行う。",
                 "意見文は「主張 → 理由（＋具体例）→ 結論」の順で書き、First / For example / For these reasons などでつながりを示す。",
                 "理由が主張を支えているか、例が理由に合っているか、結論が主張と一致しているかを点検する。"]),
        check("ck1", "確認問題",
              [("「目が回るほど忙しい」を英語にしやすい日本語に言いかえなさい。", "「とても忙しい」（I am very busy. など）"),
               ("意見文の結論を始めるときに使う表現を1つ答えなさい。", "For these reasons, ／ In conclusion, ／ To sum up, など"),
               ("意見文の理由を書くときに点検すべきことを1つ答えなさい。", "理由が主張を支えているか（主張と逆の立場の理由になっていないか）。")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

TRANS_MC = [
    ("駅まで歩いて20分かかる。", "It takes twenty minutes to walk to the station.",
     [("It needs twenty minutes to walk to the station.", "時間が「かかる」は it takes ＋時間＋to do で表す。need は主語に必要なものを表し、この形では使わない。"),
      ("It spends twenty minutes to walk to the station.", "spend は人が主語で「（時間）を費やす」。It を主語にして「かかる」の意味にはならない。"),
      ("Walking to the station costs twenty minutes.", "cost は主にお金について使う。時間がかかる意味では take を使う。")]),
    ("この映画は見る価値がある。", "This movie is worth watching.",
     [("This movie is worth to watch.", "worth の後ろは動名詞（worth watching）。to 不定詞は続かない。"),
      ("This movie is worth to be watched.", "worth の後ろは動名詞で、受け身の不定詞は使わない。"),
      ("This movie has worth watching.", "worth は前置詞的に be worth -ing の形で使う。has worth という形にはならない。")]),
    ("その試合が行われるかどうかはわからない。", "I don't know whether the game will be held.",
     [("I don't know that the game will be held.", "that 節は「～ということ」で、「かどうか」の意味を表せない。"),
      ("I don't know if will the game be held.", "if 節の中は平叙文の語順（主語＋動詞）にする。"),
      ("I don't know the game will be held or not.", "「かどうか」を表す whether / if がなく、文が成り立たない。")]),
    ("天気予報によると、明日は雪が降るそうだ。", "According to the weather forecast, it will snow tomorrow.",
     [("According to the weather forecast, it snows tomorrow.", "明日のことなので、ふつう will を使って未来を表す。"),
      ("According to the weather forecast, tomorrow will snow.", "天候を表す文の主語は it。tomorrow は雪を降らせる主語にならない。"),
      ("By the weather forecast, it will snow tomorrow.", "「～によると」は according to で表す。by では情報源の意味にならない。")]),
    ("彼は正直な人だと言われている。", "It is said that he is an honest man.",
     [("It says that he is an honest man.", "It says は「（文書などに）～と書いてある」の意味。「言われている」は It is said that ～。"),
      ("He is said that he is an honest man.", "He を主語にするなら He is said to be an honest man. の形にする。"),
      ("It is said that he is honest man.", "可算名詞 man の前に冠詞 an が必要。")]),
    ("私はこの町に来てから3年になる。", "It has been three years since I came to this town.",
     [("It is three years ago since I came to this town.", "ago は since と一緒に使わない。"),
      ("It has been three years since I have come to this town.", "since の後ろは過去の一時点を表すので、過去形 came を使う。"),
      ("Three years have passed after I came to this town.", "「～してから」の起点を表すときは since を使う。after では期間の起点にならない。")]),
    ("母は私がゲームをしすぎないように注意した。", "My mother told me not to play games too much.",
     [("My mother told me to not playing games too much.", "tell O to do の否定は not to do の形。to の後ろは原形。"),
      ("My mother told to me not to play games too much.", "tell は人を直接目的語にとる（told me）。to は不要。"),
      ("My mother said me not to play games too much.", "say は人を目的語にとらない。tell O to do の形にする。")]),
    ("彼女に会うたびに、彼女は笑顔だ。", "Every time I see her, she is smiling.",
     [("Every time I will see her, she is smiling.", "時を表す副詞節（every time ～）の中では、will を使わず現在形で表す。"),
      ("Every times I see her, she is smiling.", "every の後ろの名詞は単数形（every time）。"),
      ("Each times I see her, she is smiling.", "each の後ろの名詞も単数形。each time なら可能だが、times は誤り。")]),
    ("私はその知らせを聞いて驚いた。", "I was surprised to hear the news.",
     [("I was surprising to hear the news.", "surprising は「（人を）驚かせるような」。人が驚いたときは surprised。"),
      ("I surprised to hear the news.", "surprise は「驚かせる」という他動詞。「驚いた」は be surprised。"),
      ("I was surprised to hear the new.", "「知らせ」は news（不可算名詞）で、the new という形はない。")]),
    ("その本を読むのは簡単だった。", "It was easy to read the book.",
     [("It was easy that I read the book.", "easy は that 節をとらない。It is easy to do の形にする。"),
      ("I was easy to read the book.", "「読むのが簡単」なのは人ではない。人を主語にすると「私は扱いやすい人だった」のような意味になってしまう。"),
      ("It was easy reading of the book.", "名詞句 reading of the book を補語にしても「読むのは簡単だった」という意味にならない。")]),
    ("その問題を解くのに1時間かかった。", "It took me an hour to solve the problem.",
     [("It took me an hour solving the problem.", "it takes ＋人＋時間 の後ろは to 不定詞（to solve）にする。"),
      ("It took an hour me to solve the problem.", "it takes の後ろは「人＋時間」の順（It took me an hour）。"),
      ("It spent me an hour to solve the problem.", "spend は人が主語。It spent me という形はない。")]),
    ("私は英語で日記をつけることにした。", "I decided to keep a diary in English.",
     [("I decided keeping a diary in English.", "decide の後ろは to 不定詞（decide to do）。"),
      ("I decided to write diary in English.", "diary は可算名詞なので a が必要（keep / write a diary）。"),
      ("I decided to keep a diary by English.", "「英語で」は in English。by は手段（by bus）などに使う。")]),
]


@gen("basic_check", 5, ["computation", "common_error"])
def translation_choice(r):
    jp, ok, wrongs = r.choice(TRANS_MC)
    return mc(f"次の日本語の英訳として最も適切なものを選びなさい。\n{jp}", [ok] + [w for w, _ in wrongs],
              f"{ok}　日本語に対応する決まった構文・語法を正確に使う。", d=2,
              ap="日本語の中の決まった表現（～かかる、～の価値がある、～かどうか など）を見つけ、それに対応する英語の構文を思い出す。",
              steps=["日本語の中で、決まった構文が必要な部分を見つける。", "対応する英語の構文・語法を確認する。", "選択肢の文法・語法の誤りを点検する。", f"答え：{ok}"],
              alt=["選んだ英文を日本語に訳し戻して、元の日本語と一致するかを確かめる。"],
              pc=[("対応する構文に気づいている", 1), ("正しい英訳を選んでいる", 1)],
              pit=["日本語の語順や単語をそのまま英語に置きかえる。"], why={w: (reason, "日本語からの直訳による語法の誤り") for w, reason in wrongs})


PARTS = {"claim": "主張", "reason": "理由", "example": "具体例", "conclusion": "結論", "concession": "反対意見への譲歩"}
ESSAY_SENT = [
    ("I think that school uniforms are necessary for high school students.", "claim", "立場（制服は必要）をはっきり述べている"),
    ("I do not agree that students should be allowed to use smartphones in class.", "claim", "賛成・反対の立場を述べている"),
    ("In my opinion, every student should learn how to cook.", "claim", "In my opinion で自分の考えを示している"),
    ("First, reading books helps us learn many new words.", "reason", "First で始まり、主張を支える理由を述べている"),
    ("Second, walking to school is good for our health.", "reason", "Second で始まり、2つ目の理由を述べている"),
    ("This is because living in the countryside is less stressful than living in a big city.", "reason", "This is because で理由を示している"),
    ("For example, my brother learned to swim in a summer program and now enjoys swimming every week.", "example", "For example で始まり、個人の経験を挙げている"),
    ("For instance, many libraries now offer free online lessons.", "example", "For instance で始まり、具体的な事例を挙げている"),
    ("When I visited Kyoto last year, I saw many foreign tourists enjoying traditional food.", "example", "自分の体験という具体的な事例を述べている"),
    ("For these reasons, I believe that high school students should do volunteer work.", "conclusion", "For these reasons で始まり、主張をまとめている"),
    ("In conclusion, learning a foreign language makes our lives richer.", "conclusion", "In conclusion で始まり、全体をまとめている"),
    ("To sum up, I strongly believe that we should use public transportation more.", "conclusion", "To sum up で始まり、主張を言いかえている"),
    ("Some people say that homework is a waste of time, but it helps us review what we learned.", "concession", "反対の意見を一度認めてから、but で自分の考えに戻している"),
    ("It is true that online shopping is convenient, but it can make us spend too much money.", "concession", "It is true that … but で反対の立場の利点を認めている"),
]


@gen("basic_check", 5, ["concept", "condition_check"])
def essay_part(r):
    s, part, why_s = r.choice(ESSAY_SENT)
    others = [k for k in PARTS if k != part]
    wrongs = r.sample(others, 3)
    why = {PARTS[w]: (f"この文は{why_s}ので「{PARTS[part]}」にあたる。「{PARTS[w]}」の文ではない。", "意見文の構成要素の混同") for w in wrongs}
    return mc(f"次の英文は、意見文のどの部分に使うのが最も適切か。選びなさい。\n{s}", [PARTS[part]] + [PARTS[w] for w in wrongs],
              f"「{PARTS[part]}」。この文は{why_s}。", d=1,
              ap="文頭の表現（I think / First / For example / For these reasons / Some people say … but など）と、文の内容が一般的か具体的かに注目する。",
              steps=["文頭の表現を確認する。", "文の内容が、立場・理由・具体例・まとめ・反対意見のどれにあたるかを考える。", f"答えは「{PARTS[part]}」。"],
              alt=["この文の前後にどんな文が来るかを考え、意見文の流れ（主張 → 理由 → 例 → 結論）のどこに入るかを確かめる。"],
              pc=[("文頭の表現や内容に注目している", 1), ("構成要素を正しく選んでいる", 1)],
              pit=["個人の経験（具体例）を理由と混同する。"], why=why)


CONNECT = [
    ("I think students should join a club. (　　), clubs help them make friends from other classes.", "First",
     [("In conclusion", "In conclusion は結論を述べる表現で、最初の理由の前には使わない。"), ("For example", "For example は具体例を示す表現で、ここは主張を支える1つ目の理由である。"),
      ("However", "However は逆接で、主張と同じ方向の理由の前には使わない。")]),
    ("Smartphones make it easy to contact friends. (　　), they let us look up information quickly.", "In addition",
     [("However", "However は逆接だが、後ろの文は前と同じ方向の利点の追加である。"), ("For example", "後ろの文は前の文の具体例ではなく、別の利点である。"),
      ("As a result", "後ろの文は前の文の結果ではない。")]),
    ("Reading books improves our vocabulary. (　　), my sister learned many difficult words from novels.", "For example",
     [("In addition", "後ろの文は新しい理由ではなく、前の文の具体例（姉の経験）である。"), ("On the other hand", "On the other hand は対比で、同じ内容を支える例の前には使わない。"),
      ("In conclusion", "後ろの文は全体のまとめではなく、具体例である。")]),
    ("Walking is good for our health, and it costs nothing. (　　), I think everyone should walk more.", "For these reasons",
     [("For example", "後ろの文は具体例ではなく、2つの理由から導かれる結論である。"), ("However", "後ろの文は前の内容と反対ではない。"),
      ("Second", "Second は2つ目の理由を示す表現で、結論の前には使わない。")]),
    ("(　　) online classes are convenient, but many students still prefer to study at school.", "Some people say that",
     [("For these reasons,", "For these reasons は結論を述べる表現で、but と組み合わせて譲歩を表すことはできない。"), ("For example,", "For example は具体例を示す表現で、but で反論する形にならない。"),
      ("Second,", "Second は2つ目の理由を示す表現で、ここでは反対の意見を一度認める形が必要である。")]),
    ("Public transportation reduces traffic. (　　), it is cheaper than driving a car.", "Moreover",
     [("For instance", "後ろの文は前の文の具体例ではなく、別の利点である。"), ("Nevertheless", "Nevertheless は逆接で、同じ方向の利点の追加には使わない。"),
      ("In conclusion", "後ろの文は全体のまとめではない。")]),
    ("Many people think that living in a big city is exciting. (　　), I prefer living in a small town because it is quiet.", "However",
     [("In addition", "後ろの文は前の内容と反対の自分の考えなので、追加ではない。"), ("For example", "後ろの文は前の文の具体例ではない。"),
      ("Therefore", "後ろの文は前の文から導かれる結果ではない。")]),
    ("I believe that every high school should have a library. (　　), libraries give students a quiet place to study.", "This is because",
     [("In conclusion,", "主張の直後で結論を述べることはできない。後ろの文は主張の理由である。"), ("For example,", "後ろの文は具体例ではなく、主張の理由である。"),
      ("On the other hand,", "後ろの文は主張と対比される内容ではない。")]),
    ("First, cooking at home is healthy. (　　), it helps us save money.", "Second",
     [("First", "すでに First で1つ目の理由を述べているので、2つ目の理由には Second を使う。"), ("For example", "後ろの文は前の文の具体例ではない。"),
      ("In short", "後ろの文はまとめではなく、新しい理由である。")]),
    ("Students can learn teamwork through club activities. (　　), they can learn how to manage their time.", "Also",
     [("For instance", "後ろの文は前の文の具体例ではなく、別の利点である。"), ("However", "後ろの文は前と反対の内容ではない。"),
      ("In conclusion", "後ろの文はまとめではない。")]),
    ("We should reduce plastic waste. (　　), we can bring our own bags when we go shopping.", "For instance",
     [("However", "後ろの文は前の内容と反対ではない。"), ("In conclusion", "後ろの文は全体のまとめではなく、方法の具体例である。"),
      ("Second", "後ろの文は新しい理由ではなく、前の文の具体例である。")]),
]


@gen("basic_check", 5, ["application", "condition_check"])
def connective(r):
    s, ok, wrongs = r.choice(CONNECT)
    full = s.replace("(　　)", ok)
    return mc(f"意見文の流れに合うように、（　）に入る最も適切な表現を選びなさい。\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。完成文：{full}", d=2,
              ap="（　）の前後の文が、主張と理由・理由と理由・理由と例・反対の意見と自分の考え・全体とまとめ、のどの関係かを考える。",
              steps=["（　）の前後の文の内容を確認する。", "2つの文の関係（理由の追加・例・逆接・結論など）を判断する。", f"その関係を示す表現 {ok} を選ぶ。"],
              alt=["選んだ表現を入れた文を日本語に訳し、論理の流れが自然かを確かめる。"],
              pc=[("前後の関係をとらえている", 1), ("適切な表現を選んでいる", 1)],
              pit=["前後の関係を考えずに、知っている表現を入れる。"], why={w: (reason, "論理展開の表現の誤用") for w, reason in wrongs})


WORD = [
    ("毎晩、宿題をする。", "I (　　) my homework every night.", "do", [("make", "「宿題をする」は do one's homework。make は「作る」。"), ("play", "play はスポーツや楽器などに使う。"), ("study", "study は「勉強する」で、homework を目的語にしない。")]),
    ("彼は入学試験に合格した。", "He (　　) the entrance exam.", "passed", [("won", "win は試合や賞に使う。試験に「合格する」は pass。"), ("got", "get the exam では「試験を手に入れる」になってしまう。"), ("succeeded", "succeed は自動詞で、in が必要（succeeded in the exam）。")]),
    ("昨夜はよく眠れなかった。", "I couldn't (　　) well last night.", "sleep", [("sleeping", "couldn't の後ろは原形。"), ("asleep", "asleep は形容詞（眠っている状態）で、助動詞の後ろに置けない。"), ("slept", "couldn't の後ろは原形。")]),
    ("写真を撮ってもいいですか。", "May I (　　) a picture?", "take", [("write", "write a picture という形はない。「写真を撮る」は take a picture。"), ("make", "make a picture は「絵を作る」で、写真を撮る意味にならない。"), ("draw", "draw は「（線で）絵を描く」。")]),
    ("その会議で重要な決定をした。", "We (　　) an important decision at the meeting.", "made", [("did", "「決定をする」は make a decision。do は使わない。"), ("had", "「決定をする」は make a decision。have a decision という言い方はしない。"), ("got", "get a decision では「決定を受け取る」になる。")]),
    ("私は風邪をひいている。", "I (　　) a cold.", "have", [("am", "be 動詞では「風邪をもっている」状態を表せない。"), ("take", "take a cold という形はない。"), ("do", "do a cold という形はない。")]),
    ("この問題について意見を述べたい。", "I'd like to (　　) my opinion about this problem.", "express", [("speak", "speak は言語や話すこと自体に使い、意見を目的語にしない。"), ("talk", "talk は自動詞で目的語をとらない。"), ("tell", "tell は人を目的語にとることが多く、「意見を述べる」は express / give an opinion。")]),
    ("先生は私たちに多くの宿題を出した。", "Our teacher gave us a lot of (　　).", "homework", [("homeworks", "homework は不可算名詞で複数形にしない。"), ("a homework", "homework は不可算名詞で a をつけない。"), ("many homework", "不可算名詞には many ではなく much / a lot of を使う。")]),
    ("この部屋には家具がたくさんある。", "There is a lot of (　　) in this room.", "furniture", [("furnitures", "furniture は不可算名詞で複数形にしない。"), ("a furniture", "furniture は不可算名詞で a をつけない。"), ("furniture's", "furniture's は所有格で、名詞の位置に置いても意味をなさない。")]),
    ("彼は私にいくつか役に立つ情報をくれた。", "He gave me some useful (　　).", "information", [("informations", "information は不可算名詞で複数形にしない。"), ("an information", "information は不可算名詞で an をつけない。"), ("informs", "inform は動詞で、名詞の位置に置けない。")]),
    ("電車で学校に通っている。", "I go to school (　　) train.", "by", [("on", "on the train のように冠詞が必要。手段を表すときは無冠詞の by train。"), ("with", "with は道具を表し、交通手段には使わない。"), ("in", "in the train なら「電車の中で」となり、手段の意味にならない。")]),
    ("その事故の後、彼は運転するのをやめた。", "After the accident, he stopped (　　).", "driving", [("to drive", "stop to do は「～するために立ち止まる」という意味になり、日本語と合わない。"), ("drive", "stop の後ろに動詞の原形は置けない。"), ("drove", "stop の後ろに過去形は置けない。")]),
]


@gen("basic_check", 5, ["computation", "common_error"])
def word_usage(r):
    jp, s, ok, wrongs = r.choice(WORD)
    return mc(f"日本語に合うように、（　）に入る最も適切なものを選びなさい。\n{jp}\n{s}", [ok] + [w for w, _ in wrongs],
              f"{ok} が入る。英語では動詞と名詞の組み合わせ（コロケーション）や、名詞の数え方・冠詞が決まっている。", d=2,
              ap="日本語の動詞を1語ずつ訳すのではなく、英語で決まった組み合わせ（do homework, make a decision など）や名詞の性質（可算・不可算）から考える。",
              steps=["（　）の前後の語句を確認する。", "決まった組み合わせや名詞の性質を思い出す。", f"答えは {ok}。"],
              alt=["選んだ語を入れた英文を音読し、教科書や辞書で見たことのある組み合わせかどうかを確かめる。"],
              pc=[("組み合わせ・名詞の性質に注目している", 1), ("正しい語を選んでいる", 1)],
              pit=["日本語の「する」をいつも do、「作る」をいつも make と訳す。"], why={w: (reason, "語の組み合わせ・名詞の性質の誤り") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

TRANS_SA = [
    ("この町は多くの観光客が訪れる。", "Many tourists visit this town.", ["This town is visited by many tourists."], "「町は」を主語にせず、訪れる動作主の tourists を主語にする（受け身も可）。"),
    ("彼女はクラスで一番速く走れる。", "She can run the fastest in her class.", ["She can run faster than any other student in her class."], "最上級の副詞。比較級＋than any other でも表せる。"),
    ("駅に着いたときには、電車はもう出てしまっていた。", "When I got to the station, the train had already left.", ["When I arrived at the station, the train had already left."], "過去のある時点より前に完了したことは過去完了で表す。"),
    ("もし時間があれば、その博物館を訪れるのに。", "If I had time, I would visit the museum.", [], "現在の事実に反する仮定は仮定法過去。"),
    ("彼が何を言ったのか思い出せない。", "I can't remember what he said.", [], "疑問詞で始まる間接疑問は、主語＋動詞の語順。"),
    ("祖父は私に古い時計をくれた。", "My grandfather gave me an old watch.", ["My grandfather gave an old watch to me."], "SVOO（give 人 物）。第3文型なら to を使う。"),
    ("私たちは窓を開けたままにしておいた。", "We left the window open.", ["We kept the window open."], "SVOC（leave O C「O を C のままにしておく」）。"),
    ("英語を学ぶことは、異なる文化を理解する助けになる。", "Learning English helps us understand different cultures.", ["Learning English helps us to understand different cultures."], "動名詞の主語。help O (to) do の形。"),
    ("私が昨日会った女性は医者だ。", "The woman I met yesterday is a doctor.", ["The woman who I met yesterday is a doctor.", "The woman that I met yesterday is a doctor."], "関係代名詞（目的格）で名詞を後ろから修飾する。"),
    ("早く寝れば寝るほど、早く起きられる。", "The earlier you go to bed, the earlier you can get up.", [], "the 比較級 ～, the 比較級 … の構文。"),
    ("彼は宿題をし終えてからテレビを見た。", "He watched TV after he had finished his homework.", ["He watched TV after he finished his homework.", "After finishing his homework, he watched TV."], "前後関係が after で明らかなので、過去完了でも過去形でもよい。"),
    ("この本は私には難しすぎて読めない。", "This book is too difficult for me to read.", ["This book is so difficult that I can't read it."], "too ～ for 人 to do「～すぎて…できない」。"),
]


@gen("standard_practice", 5, ["computation", "application"])
def translate_sa(r):
    jp, ans, v, point = r.choice(TRANS_SA)
    return sa(f"次の日本語を英語に直しなさい。\n{jp}", ans, f"{point}", d=3, **({"v": v} if v else {}),
              ap="和文和訳をして、主語と動詞を決める。次に、使う文法事項（時制・構文・修飾の形）を決めてから書く。",
              steps=["英語にしやすい日本語に言いかえ、主語と動詞を決める。", f"使う文法事項を決める：{point}", "時制・数・冠詞を確認する。", f"解答例：{ans}"],
              alt=["書いた英文を日本語に訳し戻し、元の日本語の意味とずれていないかを確かめる。"],
              pc=[("主語と動詞・文型が正しい", 2), ("ポイントとなる文法事項を正しく使っている", 2)],
              pit=["日本語の「～は」をそのまま主語にする。", "時制や冠詞を確認しない。"])


ORDERS = [
    ("私はこの町が好きだ。なぜなら公園がたくさんあるからだ。", ["I", "like", "this town", "because", "there", "are", "many parks"], "主張＋because＋理由"),
    ("多くの人が、オンライン学習は便利だと考えている。", ["many people", "think", "that", "online learning", "is", "convenient"], "think that ～（意見の紹介）"),
    ("これらの理由から、私は制服に賛成だ。", ["for these reasons", "I", "am", "in favor of", "school uniforms"], "For these reasons（結論の導入）"),
    ("学生がアルバイトをするのはよい考えだと思う。", ["I", "think", "it", "is", "a good idea", "for students", "to", "work part-time"], "It is ～ for 人 to do"),
    ("確かに車は便利だが、環境に悪い。", ["it", "is true", "that", "cars", "are convenient", "but", "they", "are bad", "for the environment"], "It is true that ～, but …（譲歩）"),
    ("例えば、私の兄は毎朝ジョギングをしている。", ["for example", "my brother", "goes", "jogging", "every", "morning"], "For example（具体例の導入）"),
    ("その結果、私たちは計画を変えなければならなかった。", ["as a result", "we", "had", "to", "change", "our plan"], "As a result（結果）"),
    ("私の意見では、宿題はもっと少なくするべきだ。", ["in my opinion", "we", "should", "have", "less", "homework"], "In my opinion（主張）"),
    ("インターネットのおかげで、私たちは簡単に情報を得られる。", ["thanks to", "the Internet", "we", "can", "get", "information", "easily"], "thanks to ～（原因・理由）"),
    ("その本を読めば、彼の考えがよくわかるだろう。", ["the book", "will", "help", "you", "understand", "his ideas", "well"], "無生物主語 help O do"),
    ("何が起きているのかを理解することが大切だ。", ["it", "is important", "to", "understand", "what", "is happening"], "It is important to do＋間接疑問"),
    ("そう考える人もいるが、私はそうは思わない。", ["some", "people", "think", "so", "but", "I", "don't", "agree"], "譲歩と反論"),
]


@gen("standard_practice", 5, ["application", "computation"])
def build_order(r):
    jp, parts, pat = r.choice(ORDERS)
    sent = cap(" ".join(parts))
    for k in ("For example", "As a result", "In my opinion", "For these reasons", "Thanks to the Internet"):
        if sent.startswith(k):
            sent = sent.replace(k, k + ",", 1)
    for k in (" but ",):
        sent = sent.replace(k, ", but ")
    sent += "."
    return order(f"日本語に合うように、語句を並べかえて英文を完成させなさい。ただし、文頭にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　ポイントは{pat}。", d=3, p=4,
                 ap="まず文全体の骨組み（主語＋動詞）を決め、つなぎの表現（because / but / For example など）の位置を決めてから残りを並べる。",
                 steps=[f"使う表現を確認する：{pat}。", "主語と動詞を決める。", "残りの語句を文型に従って並べる。", f"完成文：{sent}"],
                 alt=["完成した英文を和訳し直して、日本語と一致するかを確かめる。"],
                 pc=[("骨組み（主語・動詞・つなぎの表現）が正しい", 2), ("語順がすべて正しい", 2)],
                 pit=["日本語の語順のまま並べる。", "つなぎの表現の位置を誤る。"])


REWORD = [
    ("彼の話は眉唾ものだ。", "彼の話は信じられない。", "His story is hard to believe.",
     [("彼の話はまゆ毛につばをつけたようだ。", "慣用句を文字どおりに言いかえても、英語では意味が伝わらない。"), ("彼の話は長い。", "元の文の「疑わしい」という意味が失われている。"),
      ("彼の話はおもしろい。", "元の文の意味と違う。")]),
    ("今日は猫の手も借りたいほど忙しい。", "今日はとても忙しい。", "I am very busy today.",
     [("今日は猫を借りたい。", "慣用句を文字どおりに受け取っており、意味が変わってしまう。"), ("今日は猫の世話で忙しい。", "猫は比喩で、実際の猫の話ではない。"),
      ("今日は手が痛い。", "元の文の意味と違う。")]),
    ("彼女は顔が広い。", "彼女には知り合いがたくさんいる。", "She knows a lot of people.",
     [("彼女の顔は大きい。", "慣用句を文字どおりに受け取っている。"), ("彼女は有名な顔をしている。", "元の文の「交際範囲が広い」という意味が伝わらない。"),
      ("彼女は笑顔が多い。", "元の文の意味と違う。")]),
    ("テストの結果を聞いて、肩の荷が下りた。", "テストの結果を聞いて安心した。", "I was relieved to hear the test results.",
     [("テストの結果を聞いて、荷物を下ろした。", "慣用句を文字どおりに受け取っている。"), ("テストの結果を聞いて、肩が痛くなった。", "元の文の意味と違う。"),
      ("テストの結果を聞いて、がっかりした。", "「肩の荷が下りる」は安心する意味で、がっかりするのではない。")]),
    ("この店はいつも閑古鳥が鳴いている。", "この店にはいつも客がほとんどいない。", "This store usually has very few customers.",
     [("この店ではいつも鳥が鳴いている。", "慣用句を文字どおりに受け取っている。"), ("この店はいつも騒がしい。", "閑古鳥が鳴くは客が少なく静かな様子で、逆の意味になる。"),
      ("この店ではいつも鳥を売っている。", "元の文の意味と違う。")]),
    ("彼は口が堅い。", "彼は秘密を他人に話さない。", "He never tells other people's secrets.",
     [("彼の口は硬い。", "慣用句を文字どおりに受け取っている。"), ("彼は話すのが下手だ。", "口が堅いは秘密を守る意味で、話し方の上手下手ではない。"),
      ("彼はあまり食べない。", "元の文の意味と違う。")]),
    ("その知らせを聞いて、私は耳を疑った。", "その知らせを聞いて、私は信じられなかった。", "I couldn't believe the news.",
     [("その知らせを聞いて、私は耳が痛くなった。", "慣用句を文字どおりに受け取っている。"), ("その知らせは聞こえなかった。", "耳を疑うは聞こえなかったのではなく、信じられない意味。"),
      ("その知らせを聞いて、私は耳をふさいだ。", "元の文の意味と違う。")]),
    ("彼女は英語の授業で頭角を現した。", "彼女は英語の授業でほかの生徒より目立って優秀になった。", "She became one of the best students in her English class.",
     [("彼女は英語の授業で頭を上げた。", "慣用句を文字どおりに受け取っている。"), ("彼女は英語の授業で手を挙げた。", "元の文の意味と違う。"),
      ("彼女は英語の授業で頭が痛くなった。", "元の文の意味と違う。")]),
    ("試合の前は、胸がどきどきした。", "試合の前は、とても緊張した。", "I was very nervous before the game.",
     [("試合の前は、胸が痛かった。", "どきどきは緊張を表しており、痛みではない。"), ("試合の前は、走っていた。", "元の文の意味と違う。"),
      ("試合の前は、とても楽しかった。", "どきどきは緊張を表し、楽しさとは限らない。")]),
    ("彼は首を長くしてその手紙を待っていた。", "彼はその手紙をとても楽しみに待っていた。", "He was looking forward to the letter.",
     [("彼は首をのばしてその手紙を読んでいた。", "慣用句を文字どおりに受け取っている。"), ("彼はその手紙を長い間書いていた。", "元の文の意味と違う。"),
      ("彼はその手紙を待つのに疲れていた。", "首を長くするは期待して待つ意味で、疲れた意味ではない。")]),
]


@gen("standard_practice", 5, ["concept", "application"])
def reword(r):
    jp, ok, en, wrongs = r.choice(REWORD)
    return mc(f"次の日本語を英語にするために、意味を変えずに英語にしやすい日本語へ言いかえる（和文和訳する）とき、最も適切なものを選びなさい。\n{jp}", [ok] + [w for w, _ in wrongs],
              f"「{ok}」が適切。英訳例：{en}", d=3,
              ap="慣用句や比喩を、文字どおりではなく「本当に言いたいこと」に置きかえる。そのとき元の意味が変わっていないかを確かめる。",
              steps=["日本語の中の慣用句・比喩を見つける。", "その本当の意味を平易な日本語で考える。", f"意味が同じで、英語にしやすい「{ok}」を選ぶ。", f"英訳例：{en}"],
              alt=["選んだ言いかえを英語に直し、その英語を日本語に戻したときに元の文と同じ意味になるかを確かめる。"],
              pc=[("慣用句・比喩の意味をとらえている", 2), ("意味を変えずに言いかえている", 2)],
              pit=["慣用句を文字どおりに英訳しようとする。"], why={w: (reason, "和文和訳での意味のずれ") for w, reason in wrongs})


LOGIC_ORDER = [
    ("「高校生は運動部に入るべきだ」", ["I think high school students should join a sports club.", "First, playing sports every day keeps them healthy.",
                                        "Second, they can learn how to work as a team.", "For example, my soccer team practices passing together every day.",
                                        "For these reasons, joining a sports club is a good choice."]),
    ("「紙の辞書を使うべきだ」", ["I believe students should use paper dictionaries.", "This is because they can see many related words on the same page.",
                                  "For instance, when I looked up \"happy,\" I also found \"happiness\" and \"happily.\"",
                                  "Therefore, paper dictionaries help us learn more words."]),
    ("「学校に自動販売機は必要か」", ["Some people say that vending machines are useful at school.", "However, I do not think schools need them.",
                                      "First, students may buy too many sweet drinks.", "In addition, students can bring their own water bottles.",
                                      "In conclusion, schools should not have vending machines."]),
    ("「旅行は国内と海外どちらがよいか」", ["I prefer traveling in Japan to traveling abroad.", "One reason is that it costs less money.",
                                           "Another reason is that I can enjoy local food without any language problems.",
                                           "To sum up, traveling in Japan is easier and cheaper for me."]),
    ("「朝食は大切か」", ["In my opinion, eating breakfast is very important.", "Without breakfast, it is hard to concentrate in morning classes.",
                          "For example, when I skipped breakfast last week, I felt sleepy during math class.",
                          "That is why I always eat breakfast before school."]),
    ("「図書館は夜も開くべきだ」", ["I think the city library should stay open later at night.", "Many students have club activities until evening.",
                                    "As a result, they cannot use the library after school.", "If it stayed open until nine, more students could study there.",
                                    "For this reason, longer opening hours would be helpful."]),
    ("「SNS の利用」", ["It is true that social media is a useful way to share information.", "However, it can also cause problems.",
                        "For example, some people spend too many hours on it and lose sleep.", "So we should decide how long to use it each day."]),
    ("「外国語を学ぶ利点」", ["Learning a foreign language has many benefits.", "First, we can communicate with people from other countries.",
                              "Second, we can understand our own language better by comparing the two.", "In short, a new language opens new doors for us."]),
    ("「制服の是非」", ["I am against school uniforms.", "To begin with, students should be free to choose their own clothes.",
                       "Moreover, uniforms are expensive for many families.", "For these reasons, I believe schools should not require uniforms."]),
    ("「早起きの利点」", ["I think getting up early is a good habit.", "When I get up early, I have time to review my lessons.",
                         "In addition, I never have to rush to catch the train.", "For these reasons, I recommend getting up early."]),
]


@gen("standard_practice", 5, ["condition_check", "application"])
def logic_order(r):
    theme, sents = r.choice(LOGIC_ORDER)
    return order(f"テーマ{theme}についての意見文になるように、次の英文を並べかえなさい。", sents,
                 "主張（または譲歩）→ 理由 → 具体例・追加 → 結論の順になる。First / Second / For example / For these reasons などのつなぎの表現が手がかり。", d=3, p=4,
                 ap="まず主張の文（I think / I believe / In my opinion など）と結論の文（For these reasons / Therefore / In conclusion など）を見つけ、最初と最後に置く。",
                 steps=["主張（または譲歩）の文を見つけて先頭に置く。", "結論の文を見つけて最後に置く。", "First / Second / In addition / For example などを手がかりに、理由と例を並べる。", "全体を通して読み、論理の流れを確かめる。"],
                 alt=["各文の文頭の表現に「主張」「理由」「例」「結論」などの役割を書きこみ、役割の順に並べて確かめる。"],
                 pc=[("主張と結論の位置が正しい", 2), ("理由・例の順序が正しい", 2)],
                 pit=["For example の文を、それが説明する理由の前に置く。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

OPINION = [
    ("高校生はアルバイトをするべきではない", "I agree that high school students should not have part-time jobs. First, they need time to study. If they work late at night, they may be too tired to concentrate in class. Second, school life, such as club activities, gives them experiences they cannot get later. For these reasons, I think students should focus on school."),
    ("小学校から英語を教えるのはよいことだ", "I agree that teaching English in elementary school is a good idea. First, young children can learn the sounds of a new language naturally. Second, they become less afraid of speaking with people from other countries. For example, my little sister enjoys talking with her English teacher. For these reasons, I support English lessons in elementary school."),
    ("紙の本より電子書籍のほうがよい", "I disagree that e-books are better than paper books. First, reading on a screen for a long time makes my eyes tired. Second, I can easily write notes in a paper book and find them again later. Some people say e-books are convenient, but I still prefer paper books for studying. For these reasons, I think paper books are better."),
    ("学校の休み時間にスマートフォンを使ってもよい", "I agree that students should be allowed to use smartphones during breaks. First, they can contact their families in an emergency. Second, they can check information such as train delays. However, they should not use them during class. For these reasons, I think using smartphones during breaks should be allowed."),
    ("都会より田舎に住むほうがよい", "I think living in the countryside is better than living in a city. First, the air is clean and there is a lot of nature. Second, people know their neighbors and help one another. For example, my grandparents' neighbors often bring them vegetables. For these reasons, I would like to live in the countryside in the future."),
    ("高校生は毎日運動するべきだ", "I agree that high school students should exercise every day. First, exercise keeps our bodies healthy. Second, it helps us reduce stress. For example, after I go running, I feel refreshed and can study better. For these reasons, I believe daily exercise is important for students."),
    ("学校給食を高校でも実施するべきだ", "I agree that high schools should serve school lunches. First, students can eat healthy meals every day. Second, parents do not have to make lunch boxes early in the morning. Some people say students should choose their own food, but healthy meals are more important. For these reasons, I support school lunches in high school."),
    ("修学旅行は海外に行くほうがよい", "I agree that school trips should go abroad. First, students can experience a different culture with their own eyes. Second, they have a real chance to use the English they learn at school. For example, ordering food in English can give them confidence. For these reasons, I think going abroad is a valuable experience."),
    ("宿題は廃止するべきだ", "I disagree that homework should be abolished. First, homework helps students review what they learned in class. Second, it teaches them to manage their time. It is true that too much homework is stressful, but a reasonable amount is useful. For these reasons, I think homework is necessary."),
    ("オンライン授業は対面授業より効果的だ", "I disagree that online classes are more effective than face-to-face classes. First, in a classroom, students can ask questions and get answers right away. Second, it is easier to concentrate when the teacher and classmates are nearby. For these reasons, I believe face-to-face classes are more effective."),
]


@gen("thinking_writing", 4, ["written_reasoning", "application"])
def opinion_essay(r):
    theme, model = r.choice(OPINION)
    words = r.choice([50, 60, 70])
    return desc(f"「{theme}」という意見について、賛成か反対かを明らかにし、理由を2つ挙げて{words}語程度の英語で書きなさい。",
                f"（解答例・{len(model.split())}語）{model}",
                "主張 → 理由1 → 理由2（具体例や説明）→ 結論 の構成で書く。理由は互いに重ならない観点から選び、結論は主張を言いかえる。",
                [("立場（賛成・反対）が明確である", 2), ("主張を支える理由が2つ、適切な説明とともに書かれている", 3), ("構成（主張・理由・結論）とつなぎの表現が適切である", 2), ("文法・語法が正確で語数が適切である", 1)],
                d=4, p=8, lines=8,
                ap="書き始める前に、立場と理由2つを日本語でメモする。理由は「健康」「お金」「時間」「人間関係」など別々の観点から選ぶと重ならない。",
                steps=["立場を決め、1文目で I agree / I disagree that … と述べる。", "理由を2つ、First, / Second, で示し、それぞれに説明か具体例を加える。",
                       "必要なら反対意見に触れて（Some people say …, but …）主張を強める。", "For these reasons, で始めて主張を言いかえて結ぶ。", f"語数（{words}語程度）と文法を見直す。"],
                alt=["反対の立場で書く場合も、同じ構成（主張 → 理由2つ → 結論）を使う。書きやすい理由が思いつく立場を選んでよい。"],
                pc=[("立場の明確さ", 2), ("理由と説明", 3), ("構成とつなぎ", 2), ("文法・語数", 1)],
                pit=["2つの理由が同じ内容の言いかえになる。", "結論で新しい理由を加える。"])


SURVEY = [
    dict(title="ある高校の1年生200人に聞いた「1日に家庭で勉強する時間」（架空の資料）", unit="人",
         cats=[("1時間未満", "less than one hour"), ("1〜2時間", "one to two hours"), ("2時間以上", "two hours or more")],
),
    dict(title="ある高校の1年生200人に聞いた「通学に使う主な手段」（架空の資料）", unit="人",
         cats=[("自転車", "by bicycle"), ("電車", "by train"), ("徒歩", "on foot")],
),
    dict(title="ある高校の1年生200人に聞いた「休日に最も長く時間を使うこと」（架空の資料）", unit="人",
         cats=[("部活動", "on club activities"), ("勉強", "on studying"), ("動画の視聴", "on watching videos")],
),
]


TRIPLES = [(90, 80, 30), (120, 50, 30), (100, 75, 25), (96, 72, 32), (100, 60, 40), (110, 60, 30), (84, 72, 44), (120, 60, 20), (130, 40, 30), (80, 70, 50)]


@gen("thinking_writing", 3, ["cross_unit", "computation", "written_reasoning"], rel=["HS-ENG-U07", "HS-MATH1-U05"])
def describe_data(r):
    sv = r.choice(SURVEY)
    vals = list(r.choice(TRIPLES))
    order_idx = [0, 1, 2]
    r.shuffle(order_idx)
    cats = [sv["cats"][i] for i in order_idx]
    rows = "、".join(f"{c[0]} {v}{sv['unit']}" for c, v in zip(cats, vals))
    big, small = cats[0], cats[2]
    ratio = vals[0] // vals[2] if vals[0] % vals[2] == 0 else None
    if ratio:
        mult = {2: "twice", 3: "three times", 4: "four times", 6: "six times"}[ratio]
        s1 = f"The number of students who answered \"{big[1]}\" is {mult} as large as the number of students who answered \"{small[1]}.\""
        chk = (f"{vals[0]}/{vals[2]}", str(ratio), None, "intermediate")
    else:
        s1 = f"More students answered \"{big[1]}\" than \"{small[1]}.\""
        chk = (f"{vals[0]}-{vals[2]}", str(vals[0] - vals[2]), None, "intermediate")
    pct = vals[0] * 100 // 200
    s2 = f"The most common answer was \"{big[1]},\" which was given by {pct} percent of the students."
    return desc(f"次の資料（{sv['title']}）を見て、(1)(2) の英文を書きなさい。\n［資料］{rows}\n(1) 最も多い回答と最も少ない回答を、比較の表現を使って比べる英文を1文書きなさい。\n(2) 最も多い回答が全体の何パーセントにあたるかを含めて、資料からわかることを英文1文で書きなさい。",
                f"(1) {s1}　(2) {s2}",
                f"(1) {vals[0]}÷{vals[2]}{'＝' + str(ratio) if ratio else ''} から倍数表現または比較級を使う。(2) {vals[0]}÷200×100＝{pct}（％）。",
                [("(1) 数値を正しく読み取り、比較の表現を正しく使っている", 4), ("(2) 割合を正しく計算し、英文で正しく表している", 4)], d=4, p=8, lines=6,
                ap="まず最大・最小の回答を見つけ、倍率（または差）と割合を計算する。次に、比較の表現（X times as many / more … than）と percent を使って英文にする。",
                steps=[f"最大は {big[0]}（{vals[0]}{sv['unit']}）、最小は {small[0]}（{vals[2]}{sv['unit']}）。",
                       f"倍率または差を計算する：{vals[0]}÷{vals[2]}" + (f"＝{ratio}" if ratio else f"、差は {vals[0] - vals[2]}") + "。",
                       f"割合を計算する：{vals[0]}÷200×100＝{pct}（％）。", "比較の表現と percent を使って英文を書く。"],
                alt=[f"(2) は {pct} percent of the students answered \"{big[1]}.\" のように、割合を主語にして書くこともできる。"],
                pc=[("数値の読み取りと計算", 3), ("比較の表現", 3), ("割合の英語表現", 2)],
                pit=["percent を複数形 percents にする。", "倍数表現で as large を larger にする。"],
                chk=chk)


JPEN = [
    ("日本に来る外国人観光客の数は年々増えている。", "The number of foreign tourists who visit Japan is increasing year by year.",
     "「数は」を主語にするので The number of ～ is（単数扱い）。「来る」は関係代名詞 who で tourists を修飾する。", ["The number of foreign tourists visiting Japan is increasing every year."], ["HS-ENG-U06"]),
    ("何を食べるかを決めるのは、思っていたより難しかった。", "Deciding what to eat was more difficult than I had expected.",
     "主語は動名詞句 Deciding what to eat。「思っていたより」は than I had expected（決める前に予想していたので過去完了）。", ["It was more difficult than I had expected to decide what to eat."], ["HS-ENG-U04", "HS-ENG-U07"]),
    ("その本を読んで、私は環境問題に興味を持つようになった。", "Reading the book made me interested in environmental problems.",
     "無生物主語（Reading the book）＋make O C で「O を C にする」。人を主語にするなら After I read the book, I became interested in ～。", ["After I read the book, I became interested in environmental problems.", "The book made me interested in environmental problems."], ["HS-ENG-U01", "HS-ENG-U04"]),
    ("もっと早く勉強を始めていれば、試験に合格できたかもしれない。", "If I had started studying earlier, I might have passed the exam.",
     "過去の事実に反する仮定なので仮定法過去完了。「かもしれない」は might have＋過去分詞。", ["If I had begun to study earlier, I might have passed the exam."], ["HS-ENG-U08", "HS-ENG-U04"]),
    ("私が生まれた町は、海の近くにある。", "The town where I was born is near the sea.",
     "「私が生まれた」は関係副詞 where で町を修飾する。主語は The town で、動詞は is。", ["The town I was born in is near the sea.", "The town in which I was born is near the sea."], ["HS-ENG-U06"]),
    ("彼女は、自分が間違っていたことに気づいていないようだ。", "She does not seem to realize that she was wrong.",
     "「～ようだ」は seem to do。「気づく」は realize that ～。間違っていたのは過去なので was wrong。", ["It seems that she does not realize that she was wrong."], ["HS-ENG-U04", "HS-ENG-U02"]),
    ("駅で財布をなくしたことに気づいたのは、家に帰ってからだった。", "It was not until I got home that I noticed I had lost my wallet at the station.",
     "「～してはじめて…した」は It was not until ～ that … の強調構文で表せる。なくしたのは気づくより前なので過去完了。", ["I didn't notice that I had lost my wallet at the station until I got home."], ["HS-ENG-U02"]),
    ("宿題を手伝ってくれた友達にお礼を言った。", "I thanked my friend who had helped me with my homework.",
     "「手伝ってくれた」は関係代名詞 who で friend を修飾する。お礼を言うより前なので過去完了（過去形も可）。help 人 with 物 の語法に注意。", ["I thanked my friend who helped me with my homework."], ["HS-ENG-U06", "HS-ENG-U02"]),
]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["HS-ENG-U06", "HS-ENG-U04"])
def translate_explain(r):
    jp, ans, why, v, rel = r.choice(JPEN)
    return desc(f"次の日本語を英語に直しなさい。また、英文の主語と、使った文法事項（時制・構文など）を選んだ理由を日本語で説明しなさい。\n{jp}",
                f"{ans}　（説明：{why}）" + (f"　別解：{' ／ '.join(v)}" if v else ""),
                f"和文英訳では、主語の決定と、時制・修飾の構文の選択が英文の正確さを左右する。{why}",
                [("英文が文法的に正しく、日本語の意味を正確に表している", 4), ("主語の選び方を説明している", 2), ("時制・構文の選択理由を説明している", 2)], d=4, p=8, lines=6,
                ap="日本語を「誰が（何が）・どうする」に分解し、主語と動詞を決める。名詞を修飾する部分は関係詞・分詞、時のずれは完了形で表す。",
                steps=["和文和訳をして、主語と動詞を決める。", "修飾の部分（～する人・～した町など）の表し方を決める。", "時制（特に、過去のある時点より前のことか）を確認する。", f"解答例：{ans}"],
                alt=v[:1] + ["書いた英文を日本語に訳し戻し、元の文と意味がずれていないかを確かめる。"],
                pc=[("英文", 4), ("主語の説明", 2), ("文法事項の説明", 2)],
                pit=["日本語の語順のまま修飾語を前に置く。", "時のずれを無視して過去形だけで書く。"], rel=rel)


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(task, wrong, step, etype, tempt, fix, expl, steps, ap, alt, pit):
    return desc(f"{task}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しく書き直しなさい。", fix, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しく書き直している", 3), ("規則・考え方を説明している", 1)], d=3, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい書き直し", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix))


TR_ERR = [
    ("昨日は雨が降ったので、試合は中止された。", "Because it rained yesterday. The game was canceled.", "Because it rained yesterday, the game was canceled.", "Because it rained yesterday.", "notation",
     "because の節は従属節で、それだけでは文にならない。コンマで主節につなぐ。", "日本語の「～ので。」で文を区切る感覚で、ピリオドを打った。"),
    ("この町には多くの人が住んでいる。", "This town lives many people.", "Many people live in this town.", "This town lives", "concept",
     "live の主語は「住む人」。日本語の「この町には」を主語にしてはいけない。", "日本語の文頭の語句をそのまま主語にした。"),
    ("私の意見では、制服は必要だ。", "In my opinion, school uniform is necessary.", "In my opinion, school uniforms are necessary.", "school uniform is", "notation",
     "uniform は可算名詞。一般論では複数形にし、動詞も are にする。", "日本語には単数・複数の区別がないので、名詞の数を意識しなかった。"),
    ("スマートフォンは便利だが、使いすぎはよくない。", "Smartphones are convenient, but use them too much is not good.", "Smartphones are convenient, but using them too much is not good.", "use them too much is", "formula",
     "主語にするには動名詞（using）か to 不定詞が必要。動詞の原形は主語になれない。", "「使いすぎ」を名詞にする方法を考えず、動詞のまま主語にした。"),
    ("多くの生徒がその意見に賛成した。", "Many students agreed the opinion.", "Many students agreed with the opinion.", "agreed the opinion", "concept",
     "「（意見・人）に賛成する」は agree with ～。", "日本語の「～に賛成」の「に」を英語で表すことを忘れた。"),
    ("私はその知らせを聞いて驚いた。", "I was surprising to hear the news.", "I was surprised to hear the news.", "surprising", "concept",
     "人が驚いたときは過去分詞 surprised。surprising は「（人を）驚かせるような」。", "-ing 形と -ed 形の意味の違いを確かめなかった。"),
    ("私たちは環境を守るべきだ。", "We should protect environment.", "We should protect the environment.", "environment", "notation",
     "「（自然）環境」は the environment と the をつける。", "日本語に冠詞がないので、冠詞を落とした。"),
    ("その問題について話し合うことが大切だ。", "It is important that discuss the problem.", "It is important to discuss the problem.", "that discuss", "formula",
     "It is important の後ろは to 不定詞（to discuss）か、主語のある that 節（that we discuss）にする。", "that の後ろに主語が必要なことを忘れた。"),
    ("将来、私は医者になりたい。", "In the future, I want to become doctor.", "In the future, I want to become a doctor.", "become doctor", "notation",
     "可算名詞の単数形 doctor には a が必要。", "日本語の「医者」に冠詞がないので、そのまま書いた。"),
]


@gen("error_correction", 5, ["common_error", "computation"])
def err_translation(r):
    jp, wrong, fix, where, etype, rule, tempt = r.choice(TR_ERR)
    return err_item(f"次の日本語を英語に直しなさい。\n{jp}", wrong, f"「{where}」の部分", etype, tempt, fix, f"{rule}正しくは {fix}",
                    ["主語と動詞の組み合わせが正しいかを確認する。", f"「{where}」の部分の文法・語法を点検する。", f"正しい英文：{fix}"],
                    "和文英訳の誤りは、①主語と動詞の組み合わせ、②動詞の語法（前置詞・目的語）、③名詞の数と冠詞、④文の区切り、の順に点検する。",
                    ["直した英文を日本語に訳し戻して、元の日本語と一致するかを確かめる。"],
                    ["日本語の語順・助詞をそのまま英語に置きかえる。", "冠詞と名詞の数を確認しない。"])


LOGIC_ERR = [
    ("I think students should not use smartphones at school. First, smartphones are very useful for looking up words. For these reasons, smartphones should not be used at school.",
     "理由（単語を調べるのに便利）が主張（使うべきではない）を支えておらず、反対の立場の理由になっている。また理由が1つなのに For these reasons としている。",
     "I think students should not use smartphones at school. First, smartphones can distract students from their lessons. For this reason, smartphones should not be used at school."),
    ("I agree that high school students should do volunteer work. First, volunteer work is good. Second, it is a nice experience. For these reasons, I agree.",
     "理由が「よい」「すばらしい経験だ」と抽象的で、2つの理由がほぼ同じ内容になっている。具体的で、互いに異なる観点の理由が必要。",
     "I agree that high school students should do volunteer work. First, they can learn how to work with people of different ages. Second, they can find out what kind of job they want in the future. For these reasons, I agree."),
    ("I think living in a city is better than living in the countryside. First, there are many stores and hospitals. For example, my grandparents grow vegetables in their large garden in the countryside. For these reasons, I like city life.",
     "具体例（田舎で野菜を育てる祖父母）が直前の理由（都市には店や病院が多い）を説明しておらず、むしろ田舎のよさを示している。",
     "I think living in a city is better than living in the countryside. First, there are many stores and hospitals. For example, I can buy what I need at any time near my house. For this reason, I like city life."),
    ("I disagree that homework should be abolished. First, homework helps us review our lessons. Second, it teaches us to manage our time. In conclusion, homework should be abolished because it is too stressful.",
     "結論が主張（廃止に反対）と逆になっており、本論で触れていない新しい理由（ストレス）も加えている。",
     "I disagree that homework should be abolished. First, homework helps us review our lessons. Second, it teaches us to manage our time. In conclusion, homework is necessary for students."),
    ("Online classes are better than face-to-face classes. Everyone knows this. So schools should change all classes to online classes.",
     "主張の理由が「誰もが知っている」だけで、根拠になっていない。また「すべて」を変えるべきという結論は、根拠に比べて飛躍している。",
     "I think online classes have some advantages over face-to-face classes. First, students can watch the lessons again to review them. Second, they do not need to spend time traveling to school. For these reasons, schools should use online classes more often."),
    ("I agree that students should wear school uniforms. Some people say uniforms are expensive. For these reasons, I agree with uniforms.",
     "反対意見（制服は高い）を紹介しただけで反論しておらず、主張を支える理由が1つもない。",
     "I agree that students should wear school uniforms. Some people say uniforms are expensive, but students do not need to buy many clothes for school. In addition, uniforms help students feel part of their school. For these reasons, I agree with uniforms."),
    ("I think we should eat breakfast every day. For example, my friend Ken eats rice for breakfast. For this reason, breakfast is important.",
     "具体例（ケンがご飯を食べている）が、朝食が大切である理由になっていない。まず理由を述べ、その理由を説明する例を挙げる必要がある。",
     "I think we should eat breakfast every day. First, breakfast gives us energy for morning classes. For example, when I skip breakfast, I feel sleepy during first period. For this reason, breakfast is important."),
    ("I think reading books is important. First, reading books is important for students. For these reasons, students should read more books.",
     "理由が主張のくり返しになっており（循環論法）、新しい根拠が示されていない。理由も1つしかないのに For these reasons としている。",
     "I think reading books is important. First, reading helps students learn new words and ideas. Second, it helps them understand other people's feelings. For these reasons, students should read more books."),
]


@gen("error_correction", 5, ["common_error", "written_reasoning"])
def err_logic(r):
    wrong, why, fix = r.choice(LOGIC_ERR)
    return err_item("意見文を書く課題で、ある生徒が次の英文を書いた。", wrong, "理由・具体例・結論のつながり", "logic",
                    "主張を書いたことで満足し、各文が主張を支えているかを点検しなかった。", f"（書き直しの例）{fix}",
                    f"問題点：{why}",
                    ["主張を確認する。", "各理由・具体例の前に「なぜなら」をつけて、主張とつながるかを確かめる。", f"問題点を指摘する：{why}", "主張を支える理由・例に書き直し、結論を主張と一致させる。"],
                    "意見文の論理は、①理由が主張を支えているか、②例が理由を説明しているか、③結論が主張と一致しているか、④理由が具体的で重なっていないか、の順に点検する。",
                    ["各文の役割（主張・理由・例・結論）を書き出し、矢印でつないで、つながらない箇所を探す。"],
                    ["理由と主張の立場が逆になる。", "結論で新しい理由を加える。"])


GENERATORS = [translation_choice, essay_part, connective, word_usage,
              translate_sa, build_order, reword, logic_order,
              opinion_essay, describe_data, translate_explain,
              err_translation, err_logic]
