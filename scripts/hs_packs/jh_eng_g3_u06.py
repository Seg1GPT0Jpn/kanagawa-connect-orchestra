"""単元パック：中学3年 英語 長文読解（対話文・説明文・スピーチ・グラフ・資料の読み取り）。

本文・資料はすべてこのパックのためのオリジナル。グラフ・資料の数値はすべて架空のもの。
"""
from banks._common import desc, mc, num, order, stim, table
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G3-U06"

PREREQUISITES = [
    ("JH-ENG-G2-U03", "接続詞 when / if / because / that の意味。文と文の関係（理由・条件・時）をつかむ読解の土台になる。"),
    ("JH-ENG-G2-U04", "比較級・最上級・as ～ as の意味。グラフや表の内容を英文で読み取るときに必ず使う。"),
    ("JH-ENG-G3-U03", "関係代名詞（who / which / that）で名詞を後ろから説明する形。長い文の主語と動詞を見つけるために必要。"),
    ("JH-ENG-G3-U01", "現在完了形（継続・経験・完了）。スピーチや対話で「ずっと～している」「～したことがある」を読み取る。"),
]
EXTENSIONS = [
    ("JH-ENG-G3-U07", "読んだ内容に対して、自分の意見と理由を条件に合わせて英語で書く活動につながる。"),
    ("HS-ENG-U09", "高校では、パラグラフの構成やディスコースマーカーを手がかりに、より長い論説文の要旨をつかむ読解に発展する。"),
    ("CT-ENG-U01", "共通テストのリーディングでは、複数の資料や長い文章から必要な情報をすばやく探す力が問われる。"),
]

# ======================================================================
# 授業プリント
# ======================================================================

EX1_TEXT = ("Mai: I'm going to visit my uncle in Hokkaido next week.\n"
            "Tom: That's nice. What will you do there?\n"
            "Mai: He has a big farm, and he grows potatoes and corn. I'll help him with his work.\n"
            "Tom: Sounds fun. Can you bring me a picture of them?")

LESSON = lesson(
    goals=["対話文・説明文・スピーチ・グラフや資料という文章の型に合わせて、読む目的をもって英文を読める。",
           "設問の答えの根拠を本文から探し、選択肢が「本文と同じ（言いかえ）」「本文と逆」「本文に書かれていない」のどれかを判断できる。",
           "指示語（it / they / this / that など）やつなぎの言葉（but / so / for example など）を手がかりに、文と文の関係をつかめる。",
           "グラフや表の数値を英文と結びつけ、比較の表現や割合の計算を使って正しく読み取れる。"],
    duration=50,
    readiness=["比較級・最上級（more ～ than, the most ～）の文の意味がわかる（中2）。",
               "接続詞 but / so / because / when の意味がわかる（中2）。",
               "百分率（％）と割合の計算ができる（小学校5年）。",
               "棒グラフ・帯グラフ・表から数値を読み取れる（小学校）。"],
    flow=[("導入：全部訳さなくても答えられる", 5, "短い対話文を見せ、質問を先に読むと、どこを読めばよいかがわかることを体験させる"),
          ("文章の型と設問の型", 10, "対話文・説明文・スピーチ・グラフや資料の読み方のポイントを整理する"),
          ("根拠の見つけ方", 12, "内容一致の3つの分類、指示語とつなぎの言葉の確認（例題1）"),
          ("グラフ・資料の読み取り", 13, "比較の表現と割合の計算で資料を読む（例題2）、スピーチの伝えたいこと（例題3）"),
          ("まとめと確認", 10, "読み方の手順を自分の言葉でまとめ、確認問題3問")],
    sections=[
        intro("in1", "長い英文も「目的をもって」読めばこわくない",
              "長文問題を見ると、「単語が多くて全部は訳せない」と感じるかもしれません。でも、入試や定期テストの長文問題では、すべての文を日本語に訳す必要はありません。大切なのは、①何について書かれた文章かをつかむこと、②設問が何をたずねているかを先に知ること、③答えの根拠になる文を本文から見つけることです。この3つができれば、知らない単語が少しあっても正しく答えられます。",
              bullets=["最初に、タイトル・登場人物・グラフの題名を見て「何の話か」を予想する。",
                       "次に、設問を先に読んで、本文のどこを探せばよいかを決める。",
                       "答えを選んだら、必ず本文の根拠の文に線を引いて確かめる。"],
              points=[tp("例題1の対話文を、設問を見せずに読ませた場合と、設問を先に見せた場合で、答えるまでの時間を比べさせる。",
                         ask="設問を先に読むと、読み方はどう変わったか。", expect="探す場所がわかるので、関係のある文をていねいに読めた。",
                         timing="導入の冒頭")]),
        definition("df1", "4つの文章の型と読み方のポイント",
                   "中学校の長文問題には、大きく分けて4つの型があります。型によって、注目すべきところが少しずつ違います。",
                   bullets=["対話文：だれが話しているかを確かめる。質問と答え、提案と返事の組み合わせに注目する。",
                            "説明文：第1段落で話題をつかみ、最後の段落で筆者の考え（まとめ）を確かめる。For example の後ろは具体例。",
                            "スピーチ：話し手の経験（いつ・何があったか）→ 気持ちの変化 → 伝えたいこと（最後の段落）の順に整理する。",
                            "グラフ・資料：題名・単位（人・％・冊・円）・項目を最初に確認し、英文の比較の表現と数値を照らし合わせる。"],
                   conditions=["筆者や話し手の「伝えたいこと」は、最後の段落に書かれることが多い。",
                               "グラフの数値が「人数」か「割合（％）」かを、必ず先に確かめる。"],
                   points=[tp("4つの型の文章を1つずつ見せ、「最初にどこを見るか」を班で話し合わせる。",
                              caution="グラフ問題で単位（％か人数か）を確かめずに計算する生徒が多い。")]),
        theorem("th1", "答えの根拠は必ず本文にある（内容一致の3つの分類）",
                "選択肢 → ① 本文と同じ内容（言いかえ）＝○　② 本文と逆の内容＝×　③ 本文に書かれていない内容＝×",
                ["正しい選択肢は、本文の語句をそのまま使わずに言いかえていることが多い（help → support、happy → glad など）。",
                 "本文の語句をそのまま使っていても、主語・数字・時・not が入れかわっていれば×になる。",
                 "only / all / never / always のような強く言い切る語を含む選択肢は、本文と照らし合わせて特に注意する。",
                 "自分の常識で「たぶんそうだろう」と考えて選ばない。本文に書いてあることだけが根拠になる。"],
                body="内容一致の問題では、選択肢を1つずつ本文と照らし合わせ、上の3つのどれに当たるかを判断します。×の選択肢には必ず「逆」か「書かれていない」の理由があります。",
                points=[tp("例題の選択肢に「同・逆・無」の記号を書きこませ、×の理由を言わせる。",
                           ask="本文の単語がたくさん入っている選択肢は、正しいと言えるか。",
                           expect="言えない。主語や数字が入れかわっていることがある。")]),
        definition("df2", "指示語とつなぎの言葉",
                   "英語では、同じ語のくり返しをさけるために it / they / them / this / that などの指示語を使います。また、文と文の関係は but / so / for example などのつなぎの言葉で示されます。この2つは、長文を正しく読むための大切な手がかりです。",
                   bullets=["it：単数の物・こと（前の文の内容全体を指すこともある）　they / them：複数の人・物",
                            "he / she：男性・女性の1人　this / that：直前の文の内容を指すことが多い",
                            "but（しかし）：前と反対の内容　so（だから）：前が原因、後ろが結果",
                            "for example（例えば）：前の内容の具体例　also（～もまた）：同じ方向の情報を追加",
                            "first / then（まず／それから）：手順や出来事の順番"],
                   conditions=["指示語の答えは、ふつうその指示語より前の部分にある。",
                               "答えを指示語の位置に入れて読み、意味が通るかを確かめる（単数・複数も合わせる）。"],
                   points=[tp("指示語に〇をつけ、指している語句まで矢印を引かせる。単数か複数かもあわせて確かめさせる。",
                              timing="例題1の前")]),
        derivation("dv1", "長文を読む手順（なぜこの順番がよいのか）",
                   ["① タイトル・登場人物・グラフの題名を見る → 何の話かを予想できるので、知らない単語があっても意味を推測しやすくなる。",
                    "② 設問を先に読み、キーワード（人名・数字・疑問詞）に印をつける → 本文のどこを探せばよいかがわかり、時間を節約できる。",
                    "③ 本文を最初から読む。指示語とつなぎの言葉に印をつける → 文と文の関係がわかり、話の流れを見失わない。",
                    "④ 設問のキーワードが出てきた文の前後をていねいに読み、根拠の文に線を引く → 答えが本文に基づいているかを確かめられる。",
                    "⑤ 選択肢を「同じ（言いかえ）・逆・書かれていない」に分ける → 似た単語にだまされずに正解を選べる。",
                    "⑥ 最後の段落で、筆者・話し手の伝えたいことを確認する → 主題や題名を問う設問に答えられる。"],
                   body="この手順は、「答えの根拠は本文にある」という原則から導かれます。根拠のある場所を早く見つけ、その前後を正確に読むことが、長文読解のいちばんの近道です。",
                   points=[tp("手順②の「設問の先読み」をしない生徒が多い。最初の数回は、設問のキーワードに印をつけるまで本文を読ませないようにする。",
                              ask="設問を先に読むと、どんなよいことがあるか。", expect="何を探せばよいかがわかり、必要なところをていねいに読める。")]),
        example("ex1", "例題1　対話文の指示語",
                f"次の対話文の [[u:them]] が指すものを日本語で答えなさい。\n{EX1_TEXT}",
                ["them は「複数の物」を指す指示語。直前の文から複数のものを探す。",
                 "直前のマイの発言に potatoes and corn（じゃがいもととうもろこし）がある。",
                 "「（おじさんが育てている）じゃがいもととうもろこしの写真を持ってきてくれる？」と入れて読むと意味が通る。",
                 "my uncle は1人（him で受ける）、farm は単数なので them では受けない。"],
                "マイのおじさんが育てているじゃがいもととうもろこし",
                thinking="them は複数の物・人。直前の文から複数のものを探し、置きかえて意味が通るかを確かめる。",
                points=[tp("「おじさんの農場」と答えた生徒に、farm が単数であることと、them が複数を指すことを確認させる。")],
                misconceptions=[("them は my uncle を指す。", "おじさんは1人なので him で受ける。them は potatoes and corn を指す。")]),
        example("ex2", "例題2　グラフ（表）の読み取り",
                "次の表は、ある中学校の生徒100人に好きな季節をたずねた結果（架空の資料）です。表の内容に合う英文を選び、さらに「夏」と答えた生徒は「冬」と答えた生徒の何倍かを答えなさい。\n［表］Spring 35人／Summer 30人／Autumn 20人／Winter 15人\nア Summer is the most popular season.　イ Autumn is more popular than winter.　ウ Winter is as popular as spring.",
                ["ア：最も人気があるのは Spring（35人）なので×。",
                 "イ：Autumn 20人＞Winter 15人なので○。",
                 "ウ：Winter 15人と Spring 35人は同じではないので×。",
                 "30 ÷ 15 ＝ 2 なので、夏と答えた生徒は冬の2倍（twice as many）。"],
                "イ／2倍",
                thinking="英文の比較の表現（the most / more ～ than / as ～ as）を、表の数値の大小に置きかえて確かめる。",
                points=[tp("「Summer の数値が大きいから最も人気」と思いこむ生徒がいる。必ずすべての項目と比べさせる。",
                           ask="the most popular と言えるのは、どの項目と比べたときか。", expect="ほかのすべての項目と比べて最も多いとき。")],
                misconceptions=[("Summer is the most popular season. は正しい。", "最も多いのは Spring（35人）。Summer は2番目。")]),
        example("ex3", "例題3　スピーチの伝えたいこと",
                "次のスピーチで、話し手が最も伝えたいことを日本語で答えなさい。\nI was not good at speaking English. I was afraid of making mistakes. But last month, I talked with a student from India on the Internet. My English was not perfect, but she listened to me with a smile. We talked for an hour! Now I know that we don't have to be perfect. Trying to talk is the most important thing.",
                ["前半：英語を話すのが苦手で、間違いをおそれていた（経験）。",
                 "But の後ろ：インドの生徒と話し、完ぺきでなくても通じた（出来事と気持ちの変化）。",
                 "最後の2文：Now I know ～ / ～ is the most important thing.（伝えたいこと）"],
                "完ぺきでなくてもよいので、話そうとすることがいちばん大切だということ。",
                thinking="スピーチの伝えたいことは、最後の部分（Now I know / I learned / I want to など）に書かれることが多い。",
                points=[tp("「インドの生徒と1時間話した」と答えた生徒には、それは経験（出来事）であり、そこから話し手が何を学んだかを問い返す。")]),
        board("bd1", "板書案",
              [("① 読む手順", ["タイトル・題名を見る", "設問を先に読む", "指示語・つなぎの言葉に印", "根拠の文に線を引く", "最後の段落で伝えたいこと"]),
               ("② 根拠の見つけ方", ["同じ（言いかえ）→ ○", "逆 → ×", "書かれていない → ×", "only / all / never に注意", "it / they は前を見る"]),
               ("③ グラフ・資料", ["題名・単位・項目を確認", "the most＝すべてと比べて1番", "more ～ than / as ～ as", "twice as many ＝ 2倍", "割合（％）×全体 ＝ 人数"])],
              points=[tp("②の3分類は記号（○・×逆・×無）で板書し、問題プリントでも同じ記号を使わせる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("1文ずつ和訳させる授業にならないよう、毎回「何をたずねられているか」を先に確認する習慣をつける。", timing="授業全体"),
               tp("内容一致の誤答の多くは、本文の単語がそのまま入った選択肢を選ぶことによる。主語・数字・not の入れかえに注意させる。",
                  ask="本文の単語が多い選択肢と、言いかえた選択肢では、どちらが正解になりやすいか。", expect="言いかえた選択肢のほうが正解のことが多い。"),
               tp("グラフ問題では、計算の前に単位と全体の人数を確認させる。割合（％）と人数を混同する誤りが多い。",
                  caution="「半分（half）」「2倍（twice）」などの語と、実際の数値を必ず照らし合わせさせる。"),
               tp("スピーチ・説明文では、具体的な出来事と「伝えたいこと」を区別させる。最後の段落に線を引かせるとよい。"),
               tp("問題プリント D の誤答例（指示語の取り違え・数字の読み違い・資料の読み誤り）は、誤りの種類ごとにまとめて振り返らせる。")],
              misconceptions=[("本文に出てくる単語が多い選択肢が正解だ。", "単語が同じでも、主語・数字・時・not が入れかわっていれば×。根拠の文と意味を照らし合わせる。"),
                              ("指示語は、すぐ前にある名詞を指す。", "単数・複数や意味が合うものを探す。文の内容全体を指すこともある。"),
                              ("グラフで数値がいちばん大きく見える項目が the most である。", "すべての項目の数値を比べ、単位も確かめてから判断する。")]),
        summary("sm1", "まとめ",
                ["長文は、タイトル → 設問 → 本文の順に読み、答えの根拠の文に線を引いて確かめる。",
                 "選択肢は「同じ（言いかえ）・逆・書かれていない」に分けて判断する。",
                 "指示語は前の部分から、単数・複数と意味が合うものを探す。つなぎの言葉で文と文の関係をつかむ。",
                 "グラフ・資料は、題名・単位・項目を確認し、比較の表現と数値を照らし合わせる。"]),
        check("ck1", "確認問題",
              [("内容一致の問題で、×になる選択肢の2つの種類を答えなさい。", "本文と逆の内容の選択肢と、本文に書かれていない内容の選択肢。"),
               ("They / them が指すものを探すとき、何に注意すればよいか。", "前の部分から、複数の人・物で、置きかえて意味が通るものを探す。"),
               ("全体200人のうち15％の人数を求めなさい。", "200 × 0.15 ＝ 30（人）")]),
    ])


# ======================================================================
# 本文（オリジナル）
# ======================================================================

KIND_JP = {"dialogue": "対話文", "expl": "説明文", "speech": "スピーチ"}

PASSAGES = [
    # ---------------- 対話文 ----------------
    dict(key="WELC", kind="dialogue", title="A Welcome Party",
         intro="次は、中学生の健太（Kenta）と留学生のエマ（Emma）の対話です。",
         lines=[("Emma", "Hi, Kenta. What are you doing?"),
                ("Kenta", "Hi, Emma. I'm making a poster for the welcome party. Some new students from Australia will arrive next Monday."),
                ("Emma", "That sounds fun. What are you going to do at the party?"),
                ("Kenta", "We're going to sing a Japanese song together and show them some calligraphy. But I'm worried. The song is a little difficult for people who don't know Japanese."),
                ("Emma", "Then why don't you write the words in English letters on a big sheet of paper? When I came to Japan, I couldn't read Japanese, so that kind of help made me happy."),
                ("Kenta", "That's a great idea! I'll ask my classmates to help me write them."),
                ("Emma", "Can I join you? I can tell you which words are hard to read."),
                ("Kenta", "Of course. Thank you, Emma. Let's start after school tomorrow.")],
         details=[("What are Kenta and his classmates going to do at the welcome party?", "They are going to sing a Japanese song and show calligraphy.",
                   [("They are going to make posters with the new students.", "ポスターを作っているのは健太で、パーティーでする活動ではない。"),
                    ("They are going to visit Australia.", "オーストラリアから来るのは新入生で、健太たちが行くのではない。"),
                    ("They are going to teach English to the new students.", "英語を教えるとは書かれていない。")]),
                  ("Why is Kenta worried?", "Because the song is a little difficult for people who don't know Japanese.",
                   [("Because he cannot write calligraphy well.", "書道が苦手だとは言っていない。"),
                    ("Because the new students will not come to the party.", "新入生は来週の月曜日に到着すると述べており、来ないとは言っていない。"),
                    ("Because Emma cannot read Japanese now.", "日本語が読めなかったのはエマが日本に来たときのことで、健太の心配の理由ではない。")]),
                  ("When will Kenta and Emma start working together?", "After school tomorrow.",
                   [("Next Monday.", "来週の月曜日は新入生が到着する日である。"),
                    ("This morning.", "今朝とは言っていない。"),
                    ("After the welcome party.", "パーティーの準備をするのだから、パーティーの後ではない。")])],
         refs=[("I'll ask my classmates to help me write [[u:them]].", "them", "歌の歌詞（エマの発言にある the words）",
                [("オーストラリアから来る新入生", "新入生を「書く」ことはできない。直前のエマの発言の the words（歌の言葉）を指す。"),
                 ("健太のクラスメート", "classmates は同じ文の中に別に出ており、書く対象ではない。"),
                 ("歓迎会のポスター", "ポスターは a poster（単数）なので them では受けない。")]),
               ("When I came to Japan, I couldn't read Japanese, so [[u:that kind of help]] made me happy.", "that kind of help",
                "歌の言葉を英語の文字で大きな紙に書いてくれるような手助け",
                [("日本の歌をいっしょに歌ってくれること", "直前の文でエマが提案した「英語の文字で書くこと」を指しており、歌うことではない。"),
                 ("書道を見せてくれること", "書道はパーティーの出し物で、エマが受けた手助けではない。"),
                 ("歓迎会のポスターを作ってくれること", "ポスターは健太が作っているもので、that kind of help の内容ではない。")])],
         trues=["New students from Australia will arrive next Monday.", "Emma could not read Japanese when she came to Japan.", "Emma offers to help Kenta."],
         falses=[("Kenta is making a poster for a sports festival.", "健太が作っているのは歓迎会のポスターである。"),
                 ("Emma thinks the Japanese song is too easy.", "歌が難しいと心配しているのは健太で、エマは易しいとは言っていない。"),
                 ("Kenta will write the words of the song by himself.", "健太はクラスメートに手伝いを頼むと言っており、エマも加わる。"),
                 ("Emma says she cannot join Kenta.", "エマは Can I join you? と自分から手伝いを申し出ている。")],
         main=("How to help new students enjoy a Japanese song at the welcome party",
               [("How to write calligraphy beautifully", "書道は出し物として一度出てくるだけで、書き方は話題になっていない。", "部分と全体の混同"),
                ("Life in Australia", "オーストラリアでの生活は話題になっていない。", "本文にない情報の読みこみ"),
                ("Why Emma came to Japan", "エマが日本に来た理由は述べられていない。", "本文にない情報の読みこみ")]),
         exq="エマが、歌の言葉を英語の文字で大きな紙に書くことを提案したのはなぜか。本文に即して日本語で説明しなさい。",
         exa="健太が、日本語を知らない人には歌が難しいと心配していたから。また、エマ自身も日本に来たときに日本語が読めず、そのような手助けがうれしかったから。",
         errs=[("Why is Kenta worried?", "Because Emma can't read Japanese.",
                "エマが日本語を読めなかったのは日本に来たときの話で、健太の心配の理由ではない。健太は、歌が日本語を知らない人には難しいことを心配している。",
                "Because the song is a little difficult for people who don't know Japanese."),
               ("Who will help Kenta write the words of the song?", "The new students from Australia will.",
                "新入生はまだ到着していない。健太はクラスメートに頼むと言い、エマも手伝いを申し出ている。",
                "His classmates and Emma will.")],
         opinion=("If a new student from another country came to your class, what would you do for him or her?",
                  "I would show the student around our school because I want the student to feel at home quickly."),
         gaps=[(2, [("When will they arrive?", "到着日は直前で健太が言っており、また次の健太の発言（パーティーでの予定）の答えになっていない。"),
                    ("Did you enjoy the party?", "パーティーはまだ開かれていない。次の健太の発言も予定を答えている。"),
                    ("Where is Australia?", "次の健太の発言は、この質問の答えになっていない。")]),
                (5, [("No, thank you. I don't need any help.", "直後にエマが手伝いを申し出て、健太が Thank you と受け入れている流れに合わない。"),
                     ("I don't think the song is difficult.", "健太自身が歌の難しさを心配していたので、前の発言と矛盾する。"),
                     ("Yes, I came to Japan last year.", "エマの提案への返事になっていない。")])]),
    dict(key="MUSE", kind="dialogue", title="Plans for Saturday",
         intro="次は、中学生の美香（Mika）と留学生のベン（Ben）の対話です。",
         lines=[("Mika", "Hi, Ben. Do you have any plans for Saturday?"),
                ("Ben", "Not yet. Why?"),
                ("Mika", "My family is going to the science museum in the city. My mother said I could bring a friend. Do you want to come with us?"),
                ("Ben", "I'd love to! I've wanted to visit that museum since I came to Japan. What time are you going to leave?"),
                ("Mika", "At nine. We'll take the train from Minami Station. It takes about forty minutes."),
                ("Ben", "OK. Is there anything I should bring?"),
                ("Mika", "You don't need to bring lunch. The museum has a restaurant, but it's a little expensive, so my mother is going to make sandwiches for all of us. Just bring some money for the train."),
                ("Ben", "Wow, that's very kind of her. Then I'll bring some cookies for everyone. I made them with my host mother last week, and they were delicious."),
                ("Mika", "Great! See you at the station at a quarter to nine.")],
         details=[("Where is Mika's family going on Saturday?", "To the science museum in the city.",
                   [("To Ben's host family's house.", "ベンのホストファミリーの家に行くとは書かれていない。"),
                    ("To a restaurant near Minami Station.", "博物館のレストランの話は出るが、そこへ行くのが目的ではない。駅の近くとも書かれていない。"),
                    ("To a cookie shop.", "クッキーはベンが作って持っていくもので、店には行かない。")]),
                  ("Why is Mika's mother going to make sandwiches?", "Because the museum restaurant is a little expensive.",
                   [("Because the museum has no restaurant.", "博物館にはレストランがあると述べている。"),
                    ("Because Ben asked her to make them.", "ベンが頼んだとは書かれていない。"),
                    ("Because Ben does not like sandwiches.", "ベンの好みについては書かれていない。")]),
                  ("What time will Mika and Ben meet at the station?", "At a quarter to nine.",
                   [("At nine.", "9時は出発の時刻。待ち合わせは9時15分前（8時45分）である。"),
                    ("At nine forty.", "40分は電車に乗っている時間で、時刻ではない。"),
                    ("At a quarter past nine.", "a quarter past nine は9時15分。本文は a quarter to nine（8時45分）。")])],
         refs=[("My mother said I could bring a friend. Do you want to come with [[u:us]]?", "us", "美香と美香の家族",
                [("美香とベンの2人", "ベンは誘われている側なので、us には含まれない。"),
                 ("科学博物館の人たち", "博物館の人といっしょに行くのではない。直前の My family を受けている。"),
                 ("ベンのホストファミリー", "ベンのホストファミリーは、この時点ではまだ話に出ていない。")]),
               ("I made [[u:them]] with my host mother last week, and they were delicious.", "them", "クッキー（ベンが持っていくクッキー）",
                [("サンドイッチ", "サンドイッチは美香の母が作るもので、ベンが作ったのではない。"),
                 ("電車代", "お金は「作る」ものではない。直前の文の cookies を指す。"),
                 ("博物館のレストランの料理", "レストランの料理をベンが作ったのではない。")])],
         trues=["Ben has wanted to visit the science museum for some time.", "It takes about forty minutes to get to the city by train.", "Ben is going to bring cookies on Saturday."],
         falses=[("Ben has already visited the science museum many times.", "ベンは日本に来てからずっと行きたかったと言っており、まだ行ったことはない。"),
                 ("Mika's family will go to the museum by car.", "南駅から電車で行くと言っている。"),
                 ("Ben has to bring his own lunch.", "美香の母がサンドイッチを作るので、昼食を持ってくる必要はない。"),
                 ("Mika made the cookies with her mother.", "クッキーを作ったのはベンとホストマザーである。")],
         main=("Mika invites Ben to go to a museum with her family.",
               [("Ben teaches Mika how to make cookies.", "クッキーの作り方は話題になっていない。", "本文にない情報の読みこみ"),
                ("Mika and Ben talk about their favorite restaurant.", "レストランは昼食の相談の中で少し出てくるだけで、中心の話題ではない。", "部分と全体の混同"),
                ("Ben asks Mika the way to Minami Station.", "道をたずねる場面はない。", "本文にない情報の読みこみ")]),
         exq="美香の母がサンドイッチを作ると聞いて、ベンはどう反応し、何をすることにしたか。日本語で説明しなさい。",
         exa="とても親切だと喜び、それなら自分は、先週ホストマザーといっしょに作ったおいしいクッキーを、みんなのために持っていくことにした。",
         errs=[("What time will they leave?", "They will leave at a quarter to nine.",
                "a quarter to nine は駅で待ち合わせる時刻。出発の時刻は At nine. と答えている。",
                "They will leave at nine."),
               ("Does Ben need to bring any money?", "No, he doesn't. Mika's mother will make sandwiches.",
                "昼食は不要だが、Just bring some money for the train. と電車代を持ってくるように言われている。",
                "Yes, he does. He needs some money for the train.")],
         opinion=("Which would you like to visit with your friends, a museum or a zoo?",
                  "I would like to visit a zoo because I love animals and I can enjoy walking outside with my friends."),
         gaps=[(1, [("Yes, I'm going to visit my aunt.", "予定があると答えると、次に美香が誘う流れに合わない。"),
                    ("Yes, I went there last week.", "過去のことを答えており、予定をたずねる質問の答えになっていない。"),
                    ("Because it's Saturday.", "Why への答えの形で、Do you have ～? への返事になっていない。")]),
                (5, [("OK. How long does it take?", "所要時間は直前で美香が説明している。次の美香の発言は持ち物の話である。"),
                     ("OK. Where is the museum?", "次の美香の発言は、博物館の場所の説明になっていない。"),
                     ("OK. What did you eat for lunch?", "過去の昼食をたずねており、次の発言とつながらない。")])]),
    dict(key="BEAC", kind="dialogue", title="After the Beach Clean-up",
         intro="次は、中学生の拓海（Takumi）と ALT のグリーン先生（Ms. Green）の対話です。",
         lines=[("Ms. Green", "Hi, Takumi. You look tired today."),
                ("Takumi", "Hi, Ms. Green. Yesterday I joined a beach clean-up with my brother. We worked for three hours."),
                ("Ms. Green", "That's great. What did you find on the beach?"),
                ("Takumi", "We found a lot of plastic bottles and bags. Some of them came from other countries. I was surprised."),
                ("Ms. Green", "Plastic trash can travel a long way on the sea. Sea animals sometimes eat it because they think it's food."),
                ("Takumi", "That's sad. I want to do something, but I'm just a student. What can I do?"),
                ("Ms. Green", "You can start with small things. For example, you can carry your own bottle instead of buying drinks in plastic bottles."),
                ("Takumi", "That's easy. I'll also tell my classmates about the clean-up. Maybe some of them will join us next time."),
                ("Ms. Green", "Good idea. I'd like to join you, too!")],
         details=[("What did Takumi do yesterday?", "He joined a beach clean-up with his brother.",
                   [("He went swimming in the sea with his brother.", "泳いだとは書かれていない。兄と海岸の清掃活動に参加した。"),
                    ("He bought some drinks at the beach.", "飲み物を買ったとは書かれていない。"),
                    ("He worked at a shop for three hours.", "3時間働いたのは海岸の清掃活動で、店ではない。")]),
                  ("Why do sea animals sometimes eat plastic trash?", "Because they think it is food.",
                   [("Because they like its color.", "色が好きだからとは書かれていない。"),
                    ("Because there is no food in the sea.", "海に食べ物がないとは書かれていない。"),
                    ("Because people give it to them.", "人が与えるとは書かれていない。")]),
                  ("What does Ms. Green say Takumi can do?", "He can carry his own bottle.",
                   [("He can buy more drinks in plastic bottles.", "ペットボトルの飲み物を買う代わりに自分の水筒を持つよう勧めており、逆である。"),
                    ("He can go to other countries to clean beaches.", "外国へ行くとは書かれていない。"),
                    ("He can stop going to the beach.", "海岸へ行かないようにとは言っていない。")])],
         refs=[("Some of [[u:them]] came from other countries.", "them", "海岸で見つけたたくさんのペットボトルや袋",
                [("拓海と兄", "人が外国から来たのではない。直前の文の plastic bottles and bags を指す。"),
                 ("海の生き物", "海の生き物は、このあとのグリーン先生の発言で初めて出てくる。"),
                 ("拓海のクラスメート", "クラスメートは対話の後半に出てくる語で、ここでは関係がない。")]),
               ("Maybe some of [[u:them]] will join us next time.", "them", "拓海のクラスメート",
                [("海の生き物", "海の生き物が清掃活動に参加することはない。"),
                 ("ペットボトルや袋", "物が「参加する」ことはない。直前の文の my classmates を指す。"),
                 ("外国の人々", "外国の人々については話していない。")])],
         trues=["Takumi worked on the beach for three hours.", "Takumi was surprised that some trash came from other countries.", "Ms. Green wants to join the next clean-up."],
         falses=[("Takumi found only a few pieces of trash on the beach.", "たくさんのペットボトルや袋を見つけたと述べている。"),
                 ("Ms. Green says students cannot do anything.", "小さなことから始められると述べている。"),
                 ("Takumi thinks carrying his own bottle is difficult.", "That's easy. と言っている。"),
                 ("Takumi went to the beach with Ms. Green.", "いっしょに行ったのは兄で、グリーン先生は次回参加したいと言っている。")],
         main=("Takumi and Ms. Green talk about plastic trash and what students can do.",
               [("Takumi tells Ms. Green why he likes swimming in the sea.", "泳ぐことは話題になっていない。", "本文にない情報の読みこみ"),
                ("Ms. Green explains how plastic bottles are made.", "ペットボトルの作り方の説明はない。", "本文にない情報の読みこみ"),
                ("Takumi and his brother plan a trip to other countries.", "外国はごみが流れてきた場所として出てくるだけで、旅行の計画はない。", "部分と全体の混同")]),
         exq="拓海が、海のごみについて「自分にできること」として、これからすることを2つ、日本語で書きなさい。",
         exa="①ペットボトルの飲み物を買う代わりに、自分の水筒を持ち歩くこと。②海岸の清掃活動のことをクラスメートに伝えること。",
         errs=[("Who did Takumi go to the beach with yesterday?", "He went there with Ms. Green.",
                "グリーン先生は次の清掃活動に参加したいと言っているだけ。昨日いっしょに行ったのは兄である。",
                "He went there with his brother."),
               ("What will Takumi tell his classmates about?", "He will tell them about plastic bottles from other countries.",
                "I'll also tell my classmates about the clean-up. とあり、伝えるのは清掃活動のことである。",
                "He will tell them about the beach clean-up.")],
         opinion=("What can you do to reduce plastic trash?",
                  "I can bring my own bag when I go shopping because then I don't need plastic bags."),
         gaps=[(2, [("That's great. How did you go there?", "次の拓海の発言は見つけた物の話で、交通手段を答えていない。"),
                    ("That's great. How old is your brother?", "次の拓海の発言は兄の年齢を答えていない。"),
                    ("That's too bad. Did you lose something?", "清掃活動への反応として不自然で、次の発言ともつながらない。")]),
                (5, [("That's sad. I'll never go to the beach again.", "直後に先生ができることを提案する流れに合わない。"),
                     ("That's interesting. I want to eat some fish.", "海の生き物がごみを食べる話への反応として不自然である。"),
                     ("That's sad. Where do sea animals live?", "次の先生の発言は、すむ場所の説明になっていない。")])]),
    # ---------------- 説明文 ----------------
    dict(key="UNIV", kind="expl", title="Design for Everyone",
         intro="次の英文を読んで、あとの問いに答えなさい。",
         paras=["Have you ever seen a shampoo bottle with small raised lines on its side? These lines help people who cannot see well. They can tell the shampoo from the conditioner just by touching the bottle. This is an example of universal design.",
                "Universal design is the idea of making things that are easy for many people to use. It is not only for people with disabilities. For example, a door that opens automatically is useful for people in wheelchairs, but it also helps people who are carrying heavy bags or pushing strollers.",
                "Universal design can be found in many places around us. Some cups have large handles, so children and older people can hold them easily. Some signs use pictures instead of words, so people from other countries can understand them.",
                "When we design something, we should think about many different users. If we do so, we can make a society where everyone can live comfortably."],
         details=[("Why do some shampoo bottles have small raised lines on their sides?", "To help people who cannot see well tell shampoo from conditioner.",
                   [("To make the bottles look beautiful.", "見た目を美しくするためとは書かれていない。"),
                    ("To show the price of the shampoo.", "値段を示すためとは書かれていない。"),
                    ("To make the bottles easy to open.", "開けやすくするためとは書かれていない。")]),
                  ("Who can an automatic door help, according to the passage?", "People in wheelchairs and people carrying heavy bags.",
                   [("Only people in wheelchairs.", "第2段落で、重い荷物を持った人なども助けると述べており、only は誤り。"),
                    ("Only children and older people.", "子どもと高齢者は、大きな取っ手のカップの例で出てくる。"),
                    ("People who cannot read Japanese.", "これは絵を使った標識の例に近い内容で、自動ドアの説明ではない。")]),
                  ("Why do some signs use pictures instead of words?", "So that people from other countries can understand them.",
                   [("Because pictures are cheaper than words.", "費用については書かれていない。"),
                    ("So that children can draw on them.", "標識に絵をかくためではない。"),
                    ("Because words are too difficult for everyone.", "すべての人にとって言葉が難しいとは書かれていない。")])],
         refs=[("[[u:They]] can tell the shampoo from the conditioner just by touching the bottle.", "They", "目がよく見えない人々",
                [("ボトルの側面の線", "線が見分けるのではない。触って見分けるのは人である。"),
                 ("シャンプーを作る会社", "会社は本文に出てこない。"),
                 ("車いすの人々", "車いすの人々は第2段落の自動ドアの例で出てくる。")]),
               ("If we do [[u:so]], we can make a society where everyone can live comfortably.", "so",
                "何かを設計するときに、さまざまな使う人のことを考えること",
                [("シャンプーとリンスを触って見分けること", "第1段落の具体例で、直前の文の内容ではない。"),
                 ("外国の人のために絵の標識を作ること", "第3段落の具体例の1つにすぎず、直前の文の内容を指していない。"),
                 ("重い荷物を運ぶこと", "重い荷物は自動ドアの例で出てくるだけである。")])],
         trues=["Universal design is not only for people with disabilities.", "Cups with large handles are easy for children and older people to hold.",
                "The writer thinks we should think about many different users."],
         falses=[("Universal design is only for people who cannot see well.", "第2段落で、障がいのある人だけのものではないと述べている。"),
                 ("Automatic doors are useful only for people in wheelchairs.", "重い荷物を持つ人などにも役立つと述べている。"),
                 ("Signs with pictures are difficult for people from other countries.", "外国の人にも理解できるように絵を使っていると述べている。"),
                 ("Universal design can be found only in hospitals.", "身の回りの多くの場所で見られると述べている。")],
         main=("Universal design makes things easy for many different people to use.",
               [("Shampoo bottles have small lines on their sides.", "第1段落の具体例にすぎず、文章全体の主張ではない。", "具体例と主張の混同"),
                ("Automatic doors are expensive to build.", "費用は話題になっていない。", "本文にない情報の読みこみ"),
                ("Only people with disabilities need special products.", "障がいのある人だけのものではないという本文の主張と逆である。", "本文と逆の内容")]),
         exq="第2段落で、自動ドアの例は、ユニバーサルデザインのどのような考え方を説明するために挙げられているか。日本語で説明しなさい。",
         exa="ユニバーサルデザインは障がいのある人だけのためのものではなく、多くの人にとって使いやすい物を作るという考え方。自動ドアは車いすの人だけでなく、重い荷物を持つ人やベビーカーを押す人にも役立つから。",
         errs=[("Who is universal design for?", "It is for people with disabilities.",
                "第2段落で It is not only for people with disabilities. と述べており、障がいのある人「だけ」のものではない。",
                "It is for many different people, not only for people with disabilities."),
               ("How can people who cannot see well tell the shampoo from the conditioner?", "They can read the words on the bottle.",
                "目がよく見えない人は文字を読むのではなく、ボトルの線に触れて見分ける。",
                "They can touch the small raised lines on the bottle.")],
         opinion=("Find an example of universal design in your school or town, and explain why it is helpful.",
                  "There is a slope next to the stairs at my school. It is helpful for people in wheelchairs and people with heavy bags.")),
    dict(key="EMOJ", kind="expl", title="Small Pictures, Big Messages",
         intro="次の英文を読んで、あとの問いに答えなさい。",
         paras=["Do you use emoji when you send messages to your friends? Emoji are small pictures such as smiling faces, hearts, and food. They were first made in Japan for mobile phones, and now people all over the world use them. The word \"emoji\" is used in English, too. It comes from two Japanese words: \"e\" means \"picture\" and \"moji\" means \"character.\"",
                "Why are emoji so popular? One reason is that they help us show our feelings. When we talk face to face, we can see each other's faces and hear each other's voices. But in a short text message, it is hard to tell if the writer is happy or angry. A smiling face at the end of a message can show that the writer is friendly.",
                "However, we should be careful when we use emoji. The same picture can have different meanings for different people. For example, some people use a certain face to show that they are laughing, but others think it shows that they are crying.",
                "Emoji are useful tools, but they cannot say everything. When something is important, it is better to use clear words, too."],
         details=[("Where were emoji first made?", "In Japan.",
                   [("In America.", "本文では日本で最初に作られたと述べている。"),
                    ("In many countries at the same time.", "日本で最初に作られ、その後世界中で使われるようになった。"),
                    ("In England.", "英語でも使われる語だが、イギリスで作られたとは書かれていない。")]),
                  ("Why is it hard to understand the writer's feelings in a short text message?", "Because we cannot see the writer's face or hear the writer's voice.",
                   [("Because the message is written in English.", "英語で書かれているからとは書かれていない。"),
                    ("Because there are too many emoji in it.", "絵文字が多すぎるからとは書かれていない。"),
                    ("Because the writer is always angry.", "書き手がいつも怒っているとは書かれていない。")]),
                  ("What does the writer say we should do when something is important?", "Use clear words, too.",
                   [("Use only emoji.", "絵文字だけではすべてを伝えられないと述べており、逆である。"),
                    ("Send no messages.", "メッセージを送らないようにとは書かれていない。"),
                    ("Put a smiling face at the end.", "笑顔の絵文字は友好的な気持ちを示す例で、大事なときの助言ではない。")])],
         refs=[("[[u:They]] were first made in Japan for mobile phones, and now people all over the world use them.", "They", "絵文字",
                [("友だち", "友だちが「作られた」のではない。直前の文の Emoji を指す。"),
                 ("携帯電話", "携帯電話は「～のために」作られた対象で、文の主語ではない。"),
                 ("世界中の人々", "people all over the world は同じ文の後半に出てくる別の主語である。")]),
               ("[[u:It]] comes from two Japanese words: \"e\" means \"picture\" and \"moji\" means \"character.\"", "It", "emoji という語",
                [("英語", "英語という言語が日本語の2語から来たのではない。"),
                 ("笑顔の絵", "笑顔の絵は絵文字の例で、語の由来の話ではない。"),
                 ("携帯電話", "携帯電話の語の由来は述べられていない。")])],
         trues=["People all over the world use emoji now.", "Emoji can help us show our feelings in short messages.", "The same emoji can mean different things to different people."],
         falses=[("The word \"emoji\" is not used in English.", "英語でも使われると述べている。"),
                 ("The writer says emoji can say everything.", "最終段落で、すべてを伝えることはできないと述べている。"),
                 ("In a short message, it is easy to tell if the writer is angry.", "短いメッセージでは難しいと述べている。"),
                 ("\"Moji\" means \"picture\" in Japanese.", "picture の意味は e で、moji は character（文字）である。")],
         main=("Emoji help us show our feelings, but we should use them carefully.",
               [("Emoji were first made for mobile phones in Japan.", "第1段落の情報の一部にすぎず、筆者の主張ではない。", "部分と全体の混同"),
                ("Many people send messages every day.", "本文の話題よりも広すぎる内容で、筆者の主張を表していない。", "話題と主張の混同"),
                ("We should stop using emoji because they cause problems.", "使うのをやめるべきとは言っていない。最終段落で役に立つ道具だと述べている。", "本文と逆の内容")]),
         exq="第3段落で筆者が「絵文字を使うときには注意すべきだ」と述べている理由を、本文の例に触れて日本語で説明しなさい。",
         exa="同じ絵文字でも、人によって意味の受け取り方が違うことがあるから。たとえば、ある顔の絵文字を笑っている意味で使う人もいれば、泣いている意味だと考える人もいる。",
         errs=[("What does \"moji\" mean?", "It means \"picture.\"",
                "e が picture、moji が character（文字）。2つの語と意味の組み合わせを取り違えている。",
                "It means \"character.\""),
               ("Does the writer think emoji are useful?", "No. The writer says we should not use emoji.",
                "However 以降は注意点を述べているだけで、最終段落で Emoji are useful tools と述べている。",
                "Yes. The writer says emoji are useful tools, but they cannot say everything.")],
         opinion=("Do you like to use emoji in your messages?",
                  "Yes, I do. Emoji make my messages friendly, and my friends can understand my feelings easily.")),
    dict(key="BEES", kind="expl", title="Small Workers in Our Food",
         intro="次の英文を読んで、あとの問いに答えなさい。",
         paras=["When you eat an apple or a strawberry, do you think about bees? Bees are small, but they play a big role in making our food.",
                "Bees visit flowers to collect nectar, a sweet liquid, and pollen. While they move from flower to flower, they carry pollen with them. This helps the plants make fruit and seeds. Without this help, many plants, such as apples, strawberries, and melons, cannot produce much fruit.",
                "However, in some parts of the world, the number of bees is going down. There are several reasons. Some places have lost the flowers that bees need, and some chemicals used on farms can hurt bees.",
                "What can we do? We can plant flowers in our gardens or at school. We can also learn more about bees and tell other people how important they are. Protecting bees means protecting our food."],
         details=[("Why do bees visit flowers?", "To collect nectar and pollen.",
                   [("To make seeds for farmers.", "種を作るのは植物で、ハチが花を訪れる目的ではない。"),
                    ("To sleep at night.", "眠るためとは書かれていない。"),
                    ("To find water to drink.", "水を探すためとは書かれていない。")]),
                  ("What happens when bees carry pollen from flower to flower?", "It helps the plants make fruit and seeds.",
                   [("The flowers die soon.", "花がすぐ枯れるとは書かれていない。"),
                    ("The bees become bigger.", "ハチが大きくなるとは書かれていない。"),
                    ("The plants stop making nectar.", "みつを作らなくなるとは書かれていない。")]),
                  ("What is one reason that the number of bees is going down?", "Some places have lost the flowers that bees need.",
                   [("People eat too many strawberries.", "イチゴを食べすぎることは理由として挙げられていない。"),
                    ("Bees eat too much fruit.", "ハチが果物を食べすぎるとは書かれていない。"),
                    ("There are too many gardens at schools.", "学校に花を植えることは、ハチを守る方法として挙げられている。")])],
         refs=[("While [[u:they]] move from flower to flower, they carry pollen with them.", "they", "ミツバチ（ハチ）",
                [("花", "花は移動しない。直前の文の Bees を指す。"),
                 ("果物と野菜", "果物は第2段落の後半で出てくる語で、ここでは関係がない。"),
                 ("花粉", "花粉は運ばれる側で、同じ文の後半に pollen として出てくる。")]),
               ("[[u:This]] helps the plants make fruit and seeds.", "This", "ハチが花から花へ花粉を運ぶこと",
                [("ハチが甘い液体を集めること", "みつを集めることではなく、直前の文の「花粉を運ぶこと」を指す。"),
                 ("人々がリンゴやイチゴを食べること", "第1段落の内容で、直前の文の内容ではない。"),
                 ("農場で化学物質を使うこと", "化学物質は第3段落で、ハチを傷つけるものとして出てくる。")])],
         trues=["Bees carry pollen while they move between flowers.", "Some chemicals used on farms can hurt bees.", "Planting flowers can help bees."],
         falses=[("Bees are not important for making our food.", "第1段落で、ハチは食べ物を作るうえで大きな役割を果たすと述べている。"),
                 ("The number of bees is going up all over the world.", "世界の一部の地域で減っていると述べている。"),
                 ("Apples can produce a lot of fruit without bees.", "ハチの助けがないと多くの実をつけられないと述べている。"),
                 ("The writer says we should not plant flowers at school.", "学校に花を植えることを勧めている。")],
         main=("Bees are important for our food, so we should protect them.",
               [("Bees collect a sweet liquid called nectar.", "第2段落の情報の一部にすぎず、筆者の主張ではない。", "部分と全体の混同"),
                ("Many people like to eat fruit.", "本文の話題よりも広すぎる内容で、筆者の主張を表していない。", "話題と主張の混同"),
                ("Chemicals used on farms are always good for bees.", "化学物質がハチを傷つけることがあると述べており、逆である。", "本文と逆の内容")]),
         exq="最終段落の Protecting bees means protecting our food. とはどういうことか。本文の内容に即して日本語で説明しなさい。",
         exa="ハチが花から花へ花粉を運ぶことで、リンゴやイチゴなど多くの植物が実をつけられるので、ハチを守ることは、私たちの食べ物を守ることにつながるということ。",
         errs=[("Why is the number of bees going down?", "Because people plant too many flowers.",
                "花を植えることはハチを助ける方法として挙げられている。減っている理由は、ハチに必要な花が失われたことや、化学物質がハチを傷つけること。",
                "Because some places have lost the flowers that bees need, and some chemicals can hurt bees."),
               ("What do bees carry from flower to flower?", "They carry fruit and seeds.",
                "運ぶのは花粉（pollen）。実や種は、その結果として植物が作るものである。",
                "They carry pollen.")],
         opinion=("What can students do to protect bees?",
                  "We can plant flowers at school because bees need flowers to collect nectar and pollen.")),
    # ---------------- スピーチ ----------------
    dict(key="BAND", kind="speech", title="What I Learned from the Brass Band",
         intro="次は、中学3年生の綾（Aya）が英語の授業で行ったスピーチです。",
         paras=["Hello, everyone. Today I'd like to talk about my experience in the brass band.",
                "When I joined the band in my first year, I chose the trumpet. I thought it would be easy, but I couldn't make a good sound for a long time. I practiced every day, but the other members played much better than me. I wanted to quit.",
                "One day, our leader, Haruka, said to me, \"Everyone was a beginner at first. Let's practice together after school.\" From that day, she practiced with me for twenty minutes every day. Little by little, my sound got better.",
                "Last summer, we played at a concert in our city hall. When the audience clapped, I felt really happy. I learned that I could improve if I didn't give up. Now I am the leader of the band, and I want to help new members like Haruka helped me. Thank you."],
         details=[("Why did Aya want to quit the brass band?", "Because she could not make a good sound for a long time.",
                   [("Because she did not like the trumpet.", "トランペットが嫌いだとは言っていない。"),
                    ("Because Haruka was not kind to her.", "はるかはいっしょに練習してくれた。逆である。"),
                    ("Because the band had no concerts.", "コンサートがなかったとは書かれていない。")]),
                  ("What did Haruka do for Aya?", "She practiced with Aya for twenty minutes every day.",
                   [("She gave Aya a new trumpet.", "新しいトランペットをあげたとは書かれていない。"),
                    ("She told Aya to quit the band.", "はるかはいっしょに練習しようと言っており、逆である。"),
                    ("She asked Aya to be the leader.", "リーダーになるよう頼んだとは書かれていない。")]),
                  ("How did Aya feel when the audience clapped?", "She felt really happy.",
                   [("She felt very nervous.", "緊張したとは書かれていない。"),
                    ("She felt a little sad.", "悲しかったとは書かれていない。"),
                    ("She felt very tired.", "疲れたとは書かれていない。")])],
         refs=[("From that day, [[u:she]] practiced with me for twenty minutes every day.", "she", "はるか（吹奏楽部のリーダー）",
                [("綾（話し手）", "話し手自身は me で表されている。"),
                 ("トランペットの先生", "トランペットの先生は本文に出てこない。"),
                 ("市民ホールの観客", "観客は第4段落に出てくる語で、ここでは関係がない。")]),
               ("From [[u:that day]], she practiced with me for twenty minutes every day.", "that day",
                "はるかが「みんな最初は初心者だった。放課後いっしょに練習しよう」と言った日",
                [("綾が吹奏楽部に入った日", "入部した日には、はるかの言葉はまだ出てこない。直前の One day を受けている。"),
                 ("市民ホールでコンサートをした日", "コンサートは第4段落の出来事で、そのあとではない。"),
                 ("綾がリーダーになった日", "リーダーになったのは最近のことで、練習を始めた日ではない。")])],
         trues=["Aya chose the trumpet when she joined the band.", "Haruka practiced with Aya for twenty minutes a day.", "Aya is the leader of the band now."],
         falses=[("Playing the trumpet was easy for Aya at first.", "簡単だと思っていたが、長い間よい音が出せなかった。"),
                 ("Aya quit the band before the concert.", "やめずに続け、コンサートで演奏した。"),
                 ("Haruka told Aya to practice alone.", "はるかはいっしょに練習しようと言った。"),
                 ("The concert was held at Aya's school.", "コンサートは市民ホールで開かれた。")],
         main=("If we keep trying without giving up, we can improve.",
               [("The trumpet is the most difficult instrument.", "最上級で言い切っているが、そのようなことは述べていない。", "本文にない情報の読みこみ"),
                ("Concerts at the city hall are exciting.", "コンサートは経験の一部で、伝えたいことそのものではない。", "具体例と主張の混同"),
                ("Beginners should not join the brass band.", "みんな最初は初心者だったと述べており、逆である。", "本文と逆の内容")]),
         exq="綾が、今、新しい部員を助けたいと思っているのはなぜか。本文に即して日本語で説明しなさい。",
         exa="自分がよい音を出せずにやめたいと思っていたとき、リーダーのはるかが毎日いっしょに練習してくれたおかげで上達できたので、今度は自分がはるかのように新しい部員を助けたいと思っているから。",
         errs=[("Who is the leader of the band now?", "Haruka is.",
                "はるかは綾が1年生のときのリーダー。最後の段落で Now I am the leader of the band と述べている。",
                "Aya is."),
               ("How long did Haruka practice with Aya every day?", "For two hours.",
                "本文は for twenty minutes（20分間）。数字を読み違えている。",
                "For twenty minutes.")],
         opinion=("Have you ever wanted to give up something? Write about it and what you did.",
                  "Yes. I wanted to give up swimming because I was slow, but I kept practicing and finally swam 100 meters.")),
    dict(key="HOME", kind="speech", title="My Homestay in Canada",
         intro="次は、中学3年生の陸（Riku）が英語の授業で行ったスピーチです。",
         paras=["Hi, everyone. Last August, I stayed with a host family in Canada for two weeks. I want to tell you about one important thing I learned there.",
                "On the first day, my host mother asked me, \"What do you want to eat for dinner?\" I didn't know what to say, so I just answered, \"Anything is OK.\" She looked a little sad. Later, my host brother told me, \"In our family, we like to hear what you want. Please tell us your ideas.\"",
                "After that, I tried to say my opinions, even with simple English. I told them I wanted to try Canadian food, and they took me to a market. I also cooked miso soup for them. They loved it and asked me how to make it.",
                "Through this experience, I learned that sharing my ideas is the first step to understanding each other. In Japan, I sometimes stay quiet in class, but now I want to say what I think. Thank you for listening."],
         details=[("How long did Riku stay in Canada?", "For two weeks.",
                   [("For two months.", "two weeks（2週間）を two months（2か月）と読み違えている。"),
                    ("For one year.", "1年とは書かれていない。"),
                    ("For two days.", "2日間ではなく2週間である。")]),
                  ("Why did Riku's host mother look a little sad?", "Because Riku only said, \"Anything is OK.\"",
                   [("Because Riku didn't eat dinner.", "夕食を食べなかったとは書かれていない。"),
                    ("Because Riku cooked miso soup.", "みそ汁を作ったのは後のことで、家族はとても喜んだ。"),
                    ("Because Riku couldn't speak English at all.", "簡単な英語で答えており、まったく話せなかったわけではない。")]),
                  ("Where did Riku's host family take him?", "To a market.",
                   [("To a Japanese restaurant.", "日本料理店に行ったとは書かれていない。"),
                    ("To a school.", "学校に連れていったとは書かれていない。"),
                    ("To the airport.", "空港に行ったとは書かれていない。")])],
         refs=[("[[u:She]] looked a little sad.", "She", "陸のホストマザー",
                [("陸（話し手）", "話し手自身は I で表されている。"),
                 ("陸のホストブラザー", "ホストブラザーは男性なので she では受けない。また、この文より後に出てくる。"),
                 ("市場の店員", "市場は第3段落で出てくる語で、ここでは関係がない。")]),
               ("They loved [[u:it]] and asked me how to make it.", "it", "陸が作ったみそ汁",
                [("カナダの料理", "カナダの料理は陸が食べてみたいと言ったもので、作り方をたずねられたものではない。"),
                 ("市場", "市場の作り方をたずねることはない。直前の文の miso soup を指す。"),
                 ("夕食の献立についての質問", "第2段落の内容で、直前の文の内容ではない。")])],
         trues=["Riku stayed with a host family in Canada last August.", "Riku cooked miso soup for his host family.", "Riku wants to say what he thinks in class now."],
         falses=[("Riku's host brother did not want to hear Riku's ideas.", "ホストブラザーは、陸の考えを聞きたいと言った。"),
                 ("Riku's host family did not like his miso soup.", "They loved it と述べている。"),
                 ("Riku stayed in Canada last winter.", "カナダに滞在したのは8月である。"),
                 ("Riku told his host family that he wanted to eat Japanese food.", "カナダの料理を食べてみたいと伝えた。")],
         main=("Sharing our ideas is the first step to understanding each other.",
               [("Miso soup is the most popular food in Canada.", "最上級で言い切っているが、そのようなことは述べていない。", "本文にない情報の読みこみ"),
                ("Many people in Canada go to markets on weekends.", "本文で扱っていない一般的な内容である。", "本文にない情報の読みこみ"),
                ("We should say \"Anything is OK.\" when we stay with a host family.", "Anything is OK. と答えてホストマザーを悲しませた経験から学んだことと逆である。", "本文と逆の内容")]),
         exq="陸は、ホストブラザーの言葉を聞いたあと、どのように行動を変えたか。その結果も含めて日本語で説明しなさい。",
         exa="簡単な英語でも自分の意見を言うようにした。カナダの料理を食べてみたいと伝えると市場に連れていってもらえ、みそ汁を作るとホストファミリーにとても喜ばれ、作り方をたずねられた。",
         errs=[("What did Riku say to his host mother on the first day?", "He said, \"I want to eat miso soup.\"",
                "最初の日は Anything is OK. としか答えなかった。みそ汁は、そのあと陸が自分から作ったものである。",
                "He said, \"Anything is OK.\""),
               ("What did Riku learn through his homestay?", "He learned how to cook Canadian food.",
                "学んだのは、自分の考えを伝えることが理解し合うための第一歩だということ。カナダの料理の作り方を学んだとは書かれていない。",
                "He learned that sharing his ideas is the first step to understanding each other.")],
         opinion=("Do you think it is important to say your opinions in class?",
                  "Yes, I do. If we share our opinions, we can learn different ideas from our classmates.")),
    dict(key="TIME", kind="speech", title="How I Changed My Time",
         intro="次は、中学3年生の健（Ken）が英語の授業で行ったスピーチです。",
         paras=["Hello. Do you know how you use your time? Last year, I didn't think about it at all.",
                "One evening, my father asked me, \"How many hours do you play video games every day?\" I answered, \"Maybe one hour.\" But he told me to write down what I did every day for a week. When I checked my notes, I was shocked. I was playing games for about three hours a day!",
                "I didn't want to stop playing games because they were fun. So I made a rule: I could play only after I finished my homework, and only for one hour. At first, keeping the rule was hard, but soon it became a habit.",
                "Now I have more time to read books and help my family. My grades also got better. Writing down how I used my time helped me see myself clearly. I hope you will try it, too. Thank you."],
         details=[("How many hours was Ken really playing video games every day?", "About three hours.",
                   [("About one hour.", "1時間は健の思いこみで、記録してみると約3時間だった。"),
                    ("About two hours.", "2時間とは書かれていない。"),
                    ("About seven hours.", "7は1週間の日数で、ゲームの時間ではない。")]),
                  ("What did Ken's father tell him to do?", "To write down what he did every day for a week.",
                   [("To stop playing video games.", "父はゲームをやめるようにとは言っていない。"),
                    ("To read more books.", "本を読む時間が増えたのは結果であり、父の指示ではない。"),
                    ("To help the family more.", "家族を手伝うようになったのは結果であり、父の指示ではない。")]),
                  ("What was Ken's rule?", "He could play games only after finishing his homework, and only for one hour.",
                   [("He could never play video games again.", "ゲームはやめたくなかったので、条件つきで遊ぶルールを作った。"),
                    ("He could play games for three hours before his homework.", "宿題の後に1時間だけというルールで、逆である。"),
                    ("He could play games only on weekends.", "週末だけとは書かれていない。")])],
         refs=[("I didn't want to stop playing games because [[u:they]] were fun.", "they", "テレビゲーム",
                [("健の家族", "家族が楽しいから、という意味ではない。同じ文の games を指す。"),
                 ("1週間の記録", "記録は notes で、楽しいものとしては述べられていない。"),
                 ("宿題", "宿題は次の文で出てくる語である。")]),
               ("At first, keeping the rule was hard, but soon [[u:it]] became a habit.", "it",
                "宿題を終えてから1時間だけゲームをするというルールを守ること",
                [("宿題をすること", "宿題そのものではなく、ルールを守ることが習慣になった。"),
                 ("1週間の行動を書き出すこと", "書き出したのは前の段落の内容で、習慣になったとは述べていない。"),
                 ("本を読むこと", "本を読むことは次の段落で、時間が増えた結果として出てくる。")])],
         trues=["Ken wrote down what he did every day for a week.", "Ken made a rule about playing video games.", "Ken's grades got better."],
         falses=[("Ken was right when he said he played games for about one hour.", "記録すると約3時間で、健の答えは間違っていた。"),
                 ("Ken stopped playing video games completely.", "宿題の後に1時間だけ遊ぶルールを作ったのであり、やめてはいない。"),
                 ("Keeping the rule was easy for Ken from the first day.", "At first it was hard と述べている。"),
                 ("Ken has less time to help his family now.", "家族を手伝う時間が増えたと述べている。")],
         main=("Writing down how we use our time can help us change our habits.",
               [("Video games are bad for students.", "ゲームが悪いとは言っていない。健はゲームを楽しんでいる。", "本文と逆の内容"),
                ("Ken's father plays video games, too.", "父がゲームをするとは書かれていない。", "本文にない情報の読みこみ"),
                ("Ken's grades got better last year.", "成績が上がったことは結果の1つで、伝えたいことそのものではない。", "具体例と主張の混同")]),
         exq="健が「時間の使い方を書き出すことで、自分をはっきり見ることができた」と言っているのはどういうことか。日本語で説明しなさい。",
         exa="自分ではゲームは1日1時間くらいだと思っていたが、1週間の行動を書き出してみると実際は約3時間もしていたことに気づき、自分の時間の使い方を正しく知ることができたということ。",
         errs=[("Did Ken stop playing video games?", "Yes, he did. He never played games after that.",
                "ゲームはやめたくなかったので、宿題の後に1時間だけというルールを作った。やめてはいない。",
                "No, he didn't. He played games only for one hour after finishing his homework."),
               ("What happened after Ken made the rule?", "He had less time to read books.",
                "本を読んだり家族を手伝ったりする時間が増えた（more time）と述べている。",
                "He had more time to read books and help his family, and his grades got better.")],
         opinion=("How do you use your free time after school?",
                  "I usually practice the guitar after school because I want to play in a concert someday.")),
]


def ptext(p):
    if p["kind"] == "dialogue":
        return "\n".join(f"{s}: {t}" for s, t in p["lines"])
    return "\n\n".join(p["paras"])


def pstim(p, text=None, sid=None):
    typ = "dialogue" if p["kind"] == "dialogue" else "passage"
    return stim(sid or f"RD-{p['key']}", text or ptext(p), typ, f"{p['intro']}（“{p['title']}”）", source="オリジナル")


def head(p):
    return f"{KIND_JP[p['kind']]}“{p['title']}”について答えなさい。"


# ======================================================================
# グラフ・資料（すべて架空の資料）
# ======================================================================

GRAPHS = [
    dict(key="COMM", title="How Students Come to School",
         intro="次は、ある中学校の生徒200人に通学方法をたずねた結果（架空の資料）と、その説明です。",
         text="This table shows how the students at our school come to school. We asked 200 students. Many students come by bicycle, and walking is the second most popular way.",
         tbl=table([["Bicycle", "45%"], ["Walking", "30%"], ["Bus", "15%"], ["Train", "10%"]], header=["How do you come to school?", "Students (%)"]),
         trues=["Bicycle is the most popular way to come to school.", "Twice as many students walk to school as come by bus.", "Fewer students come by train than by bus."],
         falses=[("More students come by bus than on foot.", "バスは15％で、徒歩の30％より少ない。"),
                 ("Half of the students come to school by bicycle.", "自転車は45％で、半分（50％）ではない。"),
                 ("Train is the second most popular way.", "電車は10％で最も少ない。2番目は徒歩である。"),
                 ("The same number of students come by bus and by train.", "バスは15％、電車は10％で同じではない。")],
         calcs=[("徒歩で通学している生徒は何人か。", 60, "200*30/100", "人", "全体200人の30％：200 × 0.30 ＝ 60"),
                ("自転車で通学している生徒は、バスで通学している生徒より何人多いか。", 60, "200*(45-15)/100", "人", "割合の差は45 − 15 ＝ 30（％）。200 × 0.30 ＝ 60"),
                ("バスか電車で通学している生徒は、合わせて何人か。", 50, "200*(15+10)/100", "人", "15 ＋ 10 ＝ 25（％）。200 × 0.25 ＝ 50")],
         tasks=[("資料からわかることを、比較の表現（比較級・最上級・twice as ～ as など）を使って英語で2文書きなさい。",
                 "（例）Bicycle is the most popular way to come to school. Twice as many students walk to school as come by bus.",
                 [("比較の表現を正しく使っている", 3), ("資料の数値と合っている", 3), ("2文の英文として文法・語法が正しい", 2)]),
                ("あなたの学校で「歩いて通学しよう」と提案する英文を、資料の数値を1つ使って2〜3文で書きなさい。",
                 "（例）Only thirty percent of the students walk to school now. Walking is good for our health. Let's walk to school if we live near it.",
                 [("資料の数値を正しく使っている", 3), ("提案の内容と理由が書けている", 3), ("文法・語法が正しく、2〜3文で書けている", 2)])],
         errs=[("Half of the students come to school by bicycle.", "自転車は45％で、半分（50％）には届かない。数値を確かめずに half を使っている。",
                "Almost half of the students come to school by bicycle."),
               ("Walking is the most popular way to come to school.", "最も多いのは自転車（45％）。徒歩（30％）は2番目である。",
                "Walking is the second most popular way to come to school.")]),
    dict(key="LIBR", title="Books Borrowed from the School Library",
         intro="次は、ある中学校の図書室で4月から7月に借りられた本の冊数（架空の資料）と、伊藤先生（Ms. Ito）の説明です。",
         text="Ms. Ito: Look at this table. It shows how many books our students borrowed from the school library from April to July. In June, many students were busy with their tests, so they borrowed fewer books. In July, we started a reading campaign before summer vacation.",
         tbl=table([["April", "120"], ["May", "150"], ["June", "90"], ["July", "220"]], header=["Month", "Books"]),
         trues=["The students borrowed the most books in July.", "The students borrowed fewer books in June than in April.",
                "In July, the students borrowed more than twice as many books as in June."],
         falses=[("The number of books went up every month.", "6月は5月より減っている（150冊 → 90冊）。"),
                 ("The students borrowed the fewest books in April.", "最も少ないのは6月の90冊である。"),
                 ("The students borrowed the same number of books in May and June.", "5月は150冊、6月は90冊で同じではない。"),
                 ("In July, the students borrowed twice as many books as in May.", "5月150冊の2倍は300冊で、7月の220冊ではない。")],
         calcs=[("4月から7月までに借りられた本は、合計何冊か。", 580, "120+150+90+220", "冊", "120 ＋ 150 ＋ 90 ＋ 220 ＝ 580"),
                ("7月に借りられた本は、6月より何冊多いか。", 130, "220-90", "冊", "220 − 90 ＝ 130"),
                ("4月から7月までの、1か月あたりの平均は何冊か。", 145, "(120+150+90+220)/4", "冊", "合計580 ÷ 4 ＝ 145")],
         tasks=[("4月から7月までの冊数の変化を、英語2文で説明しなさい。",
                 "（例）The students borrowed 150 books in May, but only 90 books in June. In July, the number went up to 220.",
                 [("変化（増減）を正しく説明している", 3), ("資料の数値と合っている", 3), ("文法・語法が正しい", 2)]),
                ("伊藤先生の説明をもとに、6月に借りられた本が少なかった理由と、7月に増えた理由を日本語で説明しなさい。",
                 "6月は多くの生徒がテストで忙しかったから。7月は夏休み前に読書キャンペーンを始めたから。",
                 [("6月の理由を本文に即して書いている", 3), ("7月の理由を本文に即して書いている", 3), ("資料と本文を結びつけている", 2)])],
         errs=[("The number of books went up every month.", "6月は5月の150冊から90冊に減っている。「毎月増えた」とは言えない。",
                "The number of books went down in June, but it went up again in July."),
               ("The students borrowed the most books in May.", "最も多いのは7月の220冊。5月の150冊は2番目である。",
                "The students borrowed the most books in July.")]),
    dict(key="SUMM", title="What Do You Want to Do During Summer Vacation?",
         intro="次は、ある中学校の3年生120人に、夏休みにしたいことをたずねた結果（架空の資料）です。",
         text="We asked 120 third-year students, \"What do you want to do during summer vacation?\" Each student chose one answer.",
         tbl=table([["Travel", "36"], ["Play sports", "30"], ["Read books", "24"], ["Study", "18"], ["Others", "12"]], header=["Answer", "Students"]),
         trues=["Traveling is the most popular answer.", "More students want to play sports than read books.", "Fewer than twenty students want to study."],
         falses=[("Studying is more popular than reading books.", "勉強は18人で、読書の24人より少ない。"),
                 ("Half of the students want to travel.", "旅行は36人で、120人の半分（60人）ではない。"),
                 ("Playing sports is the most popular answer.", "最も多いのは旅行（36人）。スポーツは2番目である。"),
                 ("The same number of students chose sports and reading.", "スポーツは30人、読書は24人で同じではない。")],
         calcs=[("「旅行」と答えた生徒は、全体の何％か。", 30, "36*100/120", "%", "36 ÷ 120 × 100 ＝ 30"),
                ("「スポーツ」と答えた生徒は、「勉強」と答えた生徒より何人多いか。", 12, "30-18", "人", "30 − 18 ＝ 12"),
                ("「読書」と答えた生徒は、全体の何％か。", 20, "24*100/120", "%", "24 ÷ 120 × 100 ＝ 20")],
         tasks=[("資料からわかることを、比較の表現を使って英語で2文書きなさい。",
                 "（例）Traveling is the most popular answer. More students want to play sports than study.",
                 [("比較の表現を正しく使っている", 3), ("資料の数値と合っている", 3), ("2文の英文として文法・語法が正しい", 2)]),
                ("資料の項目から1つを選び、あなたが夏休みにしたいことを、理由とともに英語で2〜3文で書きなさい。",
                 "（例）I want to read books during summer vacation. I have more free time then, so I can read long stories.",
                 [("資料の項目から1つを選んで書いている", 2), ("理由を書いている", 4), ("文法・語法が正しく、2〜3文で書けている", 2)])],
         errs=[("Half of the students want to travel.", "旅行は36人で、120人の30％。半分（60人）ではない。",
                "Thirty percent of the students want to travel."),
               ("Reading books is more popular than playing sports.", "読書は24人、スポーツは30人で、スポーツのほうが多い。",
                "Playing sports is more popular than reading books.")]),
    dict(key="EVNT", title="Midori City Library Summer Events",
         intro="次は、市立図書館の催しのお知らせ（架空の資料）と、涼（Ryo）と留学生のリサ（Lisa）の対話です。",
         text="Ryo: Lisa, look at this poster. The city library has some events this weekend.\nLisa: Nice! I'm interested in science. Can I join the workshop? I'm fourteen.\nRyo: Yes, you can. It's on Saturday afternoon. I'll join the English Talk Club on Sunday.\nLisa: Then let's watch the movie together after your club. It's free!",
         tbl=table([["Picture Book Time", "Saturday", "10:00-10:30", "Children under 7", "Free"],
                    ["English Talk Club", "Sunday", "14:00-15:00", "Junior high school students and older", "200 yen"],
                    ["Science Workshop", "Saturday", "13:00-15:00", "Ages 10-15", "500 yen"],
                    ["Movie Afternoon", "Sunday", "15:30-17:30", "Everyone", "Free"]],
                   header=["Event", "Day", "Time", "For", "Fee"]),
         trues=["Lisa can join the Science Workshop.", "The Movie Afternoon starts after the English Talk Club ends.", "Two of the events are free."],
         falses=[("A twelve-year-old student can join Picture Book Time.", "Picture Book Time は7歳未満の子ども向けである。"),
                 ("The Science Workshop is held on Sunday morning.", "科学ワークショップは土曜日の午後（13:00〜15:00）である。"),
                 ("The English Talk Club is free.", "英語トーク・クラブの参加費は200円である。"),
                 ("The Movie Afternoon is only for children.", "映画会はだれでも（Everyone）参加できる。")],
         calcs=[("リサが科学ワークショップに、涼が英語トーク・クラブに参加すると、2人の参加費は合わせていくらか。", 700, "500+200", "円", "500 ＋ 200 ＝ 700"),
                ("科学ワークショップは何分間行われるか。", 120, "(15-13)*60", "分", "13:00 から 15:00 までの2時間 ＝ 120分"),
                ("英語トーク・クラブが終わってから映画会が始まるまで、何分あるか。", 30, "(15*60+30)-15*60", "分", "15:00 から 15:30 までで30分")],
         tasks=[("友だちを1つの催しに誘うメッセージを、曜日・時刻・参加費のうち2つ以上の情報を入れて、英語で2〜3文で書きなさい。",
                 "（例）Let's go to the Movie Afternoon at the city library. It starts at three thirty on Sunday, and it's free.",
                 [("資料の情報を2つ以上正しく使っている", 4), ("誘う表現を使っている", 2), ("文法・語法が正しい", 2)]),
                ("中学3年生のあなたが、10歳の弟といっしょに土曜日に参加できる催しを選び、その理由を資料の情報を使って日本語で説明しなさい。",
                 "科学ワークショップ。土曜日に行われ、対象が10歳から15歳なので、10歳の弟も中学3年生（14〜15歳）の自分も参加できるから。Picture Book Time は7歳未満が対象なので参加できない。",
                 [("正しい催しを選んでいる", 3), ("曜日と対象年齢の両方を根拠にしている", 3), ("ほかの催しが合わない理由にも触れている", 2)])],
         errs=[("Lisa can't join the Science Workshop because she is fourteen.", "科学ワークショップの対象は10歳から15歳（Ages 10-15）なので、14歳のリサは参加できる。",
                "Lisa can join the Science Workshop because it is for ages 10 to 15."),
               ("The English Talk Club is free.", "英語トーク・クラブの参加費は200円。無料なのは Picture Book Time と Movie Afternoon である。",
                "The English Talk Club costs 200 yen.")]),
]


def gstim(g):
    return stim(f"GR-{g['key']}", g["text"], "data", f"{g['intro']}（“{g['title']}”）", source="オリジナル（架空の資料）", tbl=g["tbl"])


# ======================================================================
# つなぎの言葉・並べかえの資料
# ======================================================================

CONN_DESC = {
    "But": ("逆接", "前の内容と反対・予想に反する内容が続く"),
    "So": ("結果", "前の内容が原因・理由になり、その結果が続く"),
    "For example": ("例示", "前の内容の具体例が続く"),
    "Also": ("追加", "前の内容に同じ方向の情報を付け加える"),
    "Then": ("順序", "前の動作・出来事の次に起こることが続く"),
}
CONN_ALL = list(CONN_DESC)

# (前の文, 正しいつなぎの言葉, 後ろの文, 関係の説明, 誤答から除く語)
CONN = [
    ("I wanted to play tennis after school.", "But", "it started to rain.", "テニスをしたかった ⇔ 雨が降り始めた（思いどおりにならない）", "Then"),
    ("I was very hungry.", "So", "I ate two bowls of rice.", "とてもおなかがすいていた → ご飯を2杯食べた（原因と結果）", "Then"),
    ("There are many things you can do to help the earth.", "For example", "you can use your own bag when you go shopping.", "地球のためにできることがある → 自分の袋を使う（具体例）", "Also"),
    ("My sister can play the piano well.", "Also", "she can sing beautifully.", "ピアノが上手 ＋ 歌も上手（同じ方向の追加）", "But"),
    ("First, wash your hands.", "Then", "cut the vegetables into small pieces.", "手を洗う → 次に野菜を切る（手順の順番）", "Also"),
    ("This bag is very nice.", "But", "it is too expensive for me.", "とてもすてき ⇔ 高すぎる（反対の内容）", "Then"),
    ("The bus did not come for thirty minutes.", "So", "I was late for school.", "バスが30分来なかった → 遅刻した（原因と結果）", "Then"),
    ("My grandfather has many hobbies.", "For example", "he enjoys fishing, cooking, and taking pictures.", "趣味が多い → 釣り・料理・写真（具体例）", "Also"),
    ("Our town is famous for its beautiful beach.", "Also", "it has a lot of delicious seafood.", "海岸が有名 ＋ 海産物もおいしい（よい点の追加）", "For example"),
    ("Put the water in a pot and heat it.", "Then", "add the noodles.", "湯をわかす → 次にめんを入れる（手順の順番）", "Also"),
    ("Tom studied very hard for the test.", "So", "he got a good score.", "一生けんめい勉強した → よい点をとった（原因と結果）", "Then"),
    ("Ken practiced soccer every day.", "But", "his team lost the game.", "毎日練習した ⇔ 試合に負けた（予想に反する結果）", "Then"),
]

# 並べかえ（正しい順）
ORDERS = [
    ("対話", ["A: Excuse me. Could you tell me the way to the station?", "B: Sure. Go down this street and turn left at the second corner.",
             "A: How long does it take from here?", "B: About five minutes."]),
    ("対話", ["A: What are you going to do this weekend?", "B: I'm going to visit my grandmother in Nagano.",
             "A: That sounds nice. How will you get there?", "B: By train with my sister."]),
    ("対話", ["A: You look sad. What's wrong?", "B: I lost my key on the way home.",
             "A: Oh, no. Did you look for it in the park?", "B: Not yet. Can you help me look for it?"]),
    ("対話", ["A: Hello. This is Yuta. May I speak to Sam, please?", "B: Sorry, he's out now. Can I take a message?",
             "A: Yes, please. Please tell him to call me back.", "B: OK. I'll tell him."]),
    ("対話", ["A: Have you finished your homework?", "B: Not yet. The last question is too difficult.",
             "A: Shall I help you?", "B: Thanks. You're so kind."]),
    ("対話", ["A: Which season do you like the best?", "B: I like winter the best.",
             "A: Why do you like it?", "B: Because I can enjoy skiing with my family."]),
    ("文章", ["Last Sunday, I made curry for my family for the first time.", "First, I cut the vegetables and meat.",
             "Then I cooked them in a pot with water for thirty minutes.", "My family said it was delicious, and I was very happy."]),
    ("文章", ["My town has a famous festival every summer.", "During the festival, people carry a large portable shrine along the main street.",
             "Many visitors come to see it, so the town becomes very lively.", "I hope more people will learn about this festival."]),
    ("文章", ["Two years ago, I was in the hospital for a week.", "The nurses there were very kind to me.",
             "They always smiled and listened to my worries.", "That is why I want to be a nurse in the future."]),
    ("文章", ["Yesterday, I found a small dog in the park.", "It looked hungry and tired, so I gave it some water.",
             "Then I took it to the police station near the park.", "Later, its owner came and thanked me."]),
]


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 5, ["computation", "concept"])
def detail(r):
    p = r.choice(PASSAGES)
    q, ok, wrongs = r.choice(p["details"])
    return mc(f"{head(p)}\n次の質問の答えとして最も適切なものを選びなさい。\n{q}", [ok] + [w for w, _ in wrongs],
              f"{ok}　質問のキーワードを本文で探し、その前後の文を根拠にする。", d=2, stim=pstim(p),
              ap="質問の疑問詞（Why / What / When など）とキーワード（人名・語句）を確認し、本文の同じ語句が出てくる文の前後を読む。",
              steps=["質問の疑問詞とキーワードに印をつける。", "本文でキーワードが出てくる文を探す。", "その文と前後の文を読み、質問に合う部分を見つける。", f"答え：{ok}"],
              alt=["誤りの選択肢について、本文のどこと食い違うか（書かれていない・逆・別の場面の話）を1つずつ確かめる。"],
              pc=[("本文の根拠の文を見つけている", 1), ("正しい選択肢を選んでいる", 1)],
              pit=["本文に出てくる単語を含むだけの選択肢を選ぶ。", "疑問詞（When と What time など）が何をたずねているかを確かめない。"],
              why={w: (reason, "本文との照合不足") for w, reason in wrongs})


@gen("basic_check", 5, ["condition_check", "concept"])
def pronoun_ref(r):
    p = r.choice(PASSAGES)
    sent, word, ok, wrongs = r.choice(p["refs"])
    return mc(f"{head(p)}\n次の文の下線部 {word} が指すものとして最も適切なものを選びなさい。\n{sent}", [ok] + [w for w, _ in wrongs],
              f"{ok}。{word} の前の部分から、意味と数（単数・複数）が合うものを探す。", d=2, stim=pstim(p),
              ap="指示語の答えは、ふつうその指示語より前にある。単数か複数か、人か物かを手がかりに候補をしぼる。",
              steps=[f"下線部 {word} が単数・複数のどちらか、人・物・ことのどれを指しうるかを考える。", "直前の文から、条件に合う語句を探す。",
                     f"見つけた語句を {word} の位置に入れて読み、意味が通るかを確かめる。", f"答え：{ok}"],
              alt=["選んだ答えを指示語の位置に入れて日本語に訳し、文全体の意味が自然になるかを確かめる。"],
              pc=[("指示語の前の部分から候補を探している", 1), ("正しいものを選んでいる", 1)],
              pit=["すぐ前にある名詞を、意味や数を確かめずに選ぶ。"],
              why={w: (reason, "指示語の指す内容の取り違え") for w, reason in wrongs})


@gen("basic_check", 5, ["condition_check", "common_error"])
def connector_fill(r):
    a, ok, b, rel, excl = r.choice(CONN)
    pool = [x for x in CONN_ALL if x != ok and x != excl]
    wrongs = r.sample(pool, 3)
    why = {w: (f"{w} は「{CONN_DESC[w][0]}」（{CONN_DESC[w][1]}）を表す。この2文は「{rel}」という関係なので合わない。", "つなぎの言葉の働きの混同") for w in wrongs}
    return mc(f"前の文と後ろの文がどのような関係かを考えて、（　）に入る最も適切な語句を選びなさい。\n{a} (　　), {b}", [ok] + wrongs,
              f"{ok}（{CONN_DESC[ok][0]}）が入る。前後の関係：{rel}。", d=2,
              ap="（　）の前後の文を日本語で考え、「反対」「原因と結果」「具体例」「追加」「順番」のどの関係かを決めてから選ぶ。",
              steps=["前の文と後ろの文の意味を確認する。", f"2文の関係を考える：{rel}。", f"その関係を表すのは {ok}（{CONN_DESC[ok][0]}）。"],
              alt=["選んだ語句を入れて2文を日本語に訳し、「しかし」「だから」「例えば」などのつながりが自然かを確かめる。"],
              pc=[("2文の関係をとらえている", 1), ("正しい語句を選んでいる", 1)],
              pit=["前後の関係を考えずに、よく見る But や So を選ぶ。"], why=why)


@gen("basic_check", 5, ["application", "computation"])
def graph_read(r):
    g = r.choice(GRAPHS)
    ok = r.choice(g["trues"])
    wrongs = r.sample(g["falses"], 3)
    return mc(f"資料“{g['title']}”の内容に合う英文を1つ選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　英文の比較の表現や数を表す語を、資料の数値に置きかえて確かめる。", d=2, stim=gstim(g),
              ap="資料の題名・単位・項目を先に確認し、各英文の比較の表現（the most / more ～ than / twice as ～ as / half など）を数値で確かめる。",
              steps=["資料の単位（人・％・冊・円）と項目を確認する。", "各選択肢の英文から、比べている項目と比較の表現を読み取る。", "資料の数値で大小・倍数を確かめる。", f"答え：{ok}"],
              alt=["誤りの選択肢を、資料に合うように直すと正しい英文になるかを考えて確かめる。"],
              pc=[("資料の数値を正しく読んでいる", 1), ("正しい英文を選んでいる", 1)],
              pit=["half / twice / the most などの語を、数値で確かめずに選ぶ。"],
              why={w: (reason, "資料の数値の読み誤り") for w, reason in wrongs})


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["condition_check", "common_error"])
def true_statement(r):
    p = r.choice(PASSAGES)
    ok = r.choice(p["trues"])
    wrongs = r.sample(p["falses"], 3)
    return mc(f"{head(p)}\n本文の内容に合うものを1つ選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　選択肢ごとに根拠となる本文の箇所を探し、言いかえに注意して照合する。", d=3, stim=pstim(p),
              ap="選択肢ごとに根拠となる本文の文を探し、「同じ内容（言いかえ）」「逆」「書かれていない」のどれかに分ける。",
              steps=["選択肢のキーワード（人名・数字・動詞）に印をつける。", "本文で同じ内容が書かれた文を探す。",
                     "主語・数字・時・not / only などが本文と合っているかを確かめる。", f"本文と一致するのは：{ok}"],
              alt=["誤りの選択肢について、本文のどの語句と食い違うかを書き出し、「逆」か「書かれていない」かを確かめる。"],
              pc=[("根拠となる本文の文を見つけている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["本文の単語が多く入っている選択肢を、意味を確かめずに選ぶ。", "主語（だれがしたか）の入れかわりを見落とす。"],
              why={w: (reason, "本文との照合不足") for w, reason in wrongs})


MAIN_Q = {"dialogue": "この対話の内容を最もよく表しているもの", "expl": "筆者が最も伝えたいこと", "speech": "話し手が最も伝えたいこと"}


@gen("standard_practice", 4, ["concept", "application"])
def main_message(r):
    p = r.choice(PASSAGES)
    ok, wrongs = p["main"]
    what = MAIN_Q[p["kind"]]
    return mc(f"{head(p)}\n{what}として最も適切なものを選びなさい。", [ok] + [w for w, _, _ in wrongs],
              f"{ok}　{'対話全体の流れ（話題 → 問題 → 解決）' if p['kind'] == 'dialogue' else '最後の段落のまとめ'}をもとに判断する。", d=3, stim=pstim(p),
              ap=("対話文では、最初の話題と、最後にどうすることになったかをつなげて考える。" if p["kind"] == "dialogue"
                  else "最初の段落の話題と、最後の段落のまとめ（I learned / I want to / we should など）を中心に考える。具体例だけの選択肢は外す。"),
              steps=["最初の段落（最初の発言）で話題を確認する。", "最後の段落（最後の発言）で、まとめや結論を確認する。",
                     "各選択肢が、一部だけでないか・本文にない内容でないか・逆でないかを点検する。", f"答え：{ok}"],
              alt=["各段落（発言のまとまり）の内容を一言で書き出し、そのすべてを含む選択肢を選ぶ。"],
              pc=[("話題とまとめをとらえている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["印象に残った具体例や出来事を、伝えたいことと思いこむ。"],
              why={w: (reason, mis) for w, reason, mis in wrongs})


@gen("standard_practice", 3, ["application", "concept"])
def dialogue_gap(r):
    p = r.choice([x for x in PASSAGES if x["kind"] == "dialogue"])
    i, wrongs = r.choice(p["gaps"])
    sp, ok = p["lines"][i]
    text = "\n".join(f"{s}: {'(　　　　)' if k == i else t}" for k, (s, t) in enumerate(p["lines"]))
    return mc(f"{head(p)}\n対話の（　　）に入る {sp} の発言として最も適切なものを選びなさい。", [ok] + [w for w, _ in wrongs],
              f"{ok}　空所の直前の発言と直後の発言の両方につながるものを選ぶ。", d=3, stim=pstim(p, text, f"RD-{p['key']}-GAP{i}"),
              ap="空所の「直前の発言への返事」になっているか、「直後の発言が答えになる質問・発言」になっているかの両方を確かめる。",
              steps=["空所の直前の発言を読み、何を言われたかを確認する。", "空所の直後の発言を読み、何に答えているかを確認する。",
                     "前後の両方につながる選択肢を選ぶ。", f"答え：{ok}"],
              alt=["選んだ発言を空所に入れて、前後3つの発言を続けて読み、会話が自然に流れるかを確かめる。"],
              pc=[("前後の発言とのつながりを考えている", 2), ("正しい選択肢を選んでいる", 2)],
              pit=["直前の発言だけを見て選び、直後の発言とつながるかを確かめない。"],
              why={w: (reason, "対話の流れの読み落とし") for w, reason in wrongs})


@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G1-U07"])
def graph_calc(r):
    g = r.choice(GRAPHS)
    q, ans, expr, unit, how = r.choice(g["calcs"])
    return num(f"資料“{g['title']}”をもとに答えなさい。\n{q}", ans, f"{how}（{unit}）", d=3, stim=gstim(g), unit=unit,
               chk=(expr, str(ans)),
               ap="資料の単位（人・％・冊・円・時刻）と、全体の数を先に確認する。割合（％）から人数を出すときは「全体 × 割合」を使う。",
               steps=["資料から必要な項目の数値を読み取る。", "単位と全体の数を確認し、式を立てる。", f"計算する：{how}", f"答え：{ans}{unit}"],
               alt=["求めた答えを資料にもどし、ほかの項目の数値と比べて大きさが自然か（全体を超えていないかなど）を確かめる。"],
               pc=[("必要な数値を正しく読み取っている", 2), ("正しく計算している", 2)],
               pit=["割合（％）の数値をそのまま人数として答える。", "時刻の差を出すときに、60分で1時間になることを忘れる。"],
               ver=f"{expr} ＝ {ans}")


@gen("standard_practice", 4, ["application", "written_reasoning"])
def sentence_order(r):
    kind, sents = r.choice(ORDERS)
    what = "自然な対話" if kind == "対話" else "意味の通る文章"
    return order(f"次の4つの英文を、{what}になるように並べかえなさい。", sents,
                 "　".join(sents) + "　質問と答え、指示語（it / they / there）、つなぎの言葉（First / Then / That is why）が順番の手がかりになる。", d=3, p=4,
                 ap="ほかの文を受ける語（it / they / there / Then / That is why など）を含まない文、または最初の質問を探して先頭に置く。",
                 steps=["ほかの文がなくても意味がわかる文（話題を出す文・最初の質問）を先頭に置く。",
                        "指示語やつなぎの言葉が、どの文を受けているかで次の文を決める。",
                        "質問には答えを、提案には返事を続ける。", "完成した順に通して読み、流れを確かめる。"],
                 alt=["隣り合う2文ごとに「前の文がないと意味が通らないか」を確かめ、つながりを1組ずつ決めていく。"],
                 pc=[("先頭の文を正しく選んでいる", 2), ("残りの文の順序が正しい", 2)],
                 pit=["指示語が何を指すかを確かめずに並べる。", "質問と答えの組み合わせを確かめない。"])


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["written_reasoning", "concept"])
def explain_jp(r):
    p = r.choice(PASSAGES)
    return desc(f"{head(p)}\n{p['exq']}", p["exa"],
                "設問が指す部分を本文で特定し、その前後の文（because / so / but などのつなぎの言葉）から理由や内容をとらえて、本文の言葉を使って説明する。",
                [("設問が指す本文の箇所を正しく特定している", 3), ("本文の内容に即して説明している", 3), ("設問の問い方に合った文末で答えている", 2)],
                d=4, p=8, lines=5, stim=pstim(p),
                ap="設問のキーワードが出てくる本文の箇所を探し、その前後の文に書かれた理由・出来事・気持ちをまとめる。",
                steps=["設問が何をたずねているか（理由・内容・変化など）を確認する。", "本文で該当する箇所を探し、線を引く。",
                       "前後の文から必要な情報を集め、日本語でまとめる。", "「なぜか」なら「～から」、「どういうことか」なら「～ということ」で結ぶ。"],
                alt=["書いた答えを本文の該当箇所と1文ずつ対応させ、抜けている情報や本文にない内容がないかを確かめる。"],
                pc=[("箇所の特定", 3), ("内容の説明", 3), ("文末の形", 2)],
                pit=["本文に書かれていない自分の考えを付け加える。", "「なぜか」と問われているのに「～から」で結ばない。"])


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G3-U07", "HS-ENG-U09"])
def respond_english(r):
    p = r.choice(PASSAGES)
    q, sample = p["opinion"]
    return desc(f"{head(p)}\n本文の内容をふまえて、次の質問にあなた自身の答えを、理由を含めて英語で書きなさい（15語以上）。\n{q}",
                f"（例）{sample}",
                "質問に直接答える文を最初に書き、because や自分の経験で理由を1つ以上加える。本文の内容とつながる考えを書くとよい。",
                [("質問に正しく答えている", 3), ("理由を明確に書いている", 3), ("文法・語法が正しく、語数の条件を満たしている", 2)],
                d=4, p=8, lines=5, stim=pstim(p),
                ap="質問の疑問詞と時制（would / can / do など）をそのまま使って答えの文を作り、続けて because や具体的な経験で理由を書く。",
                steps=["質問が何をたずねているかを確認する（意見・経験・考えなど）。", "質問の形に合わせて、答えの文を1文で書く。",
                       "理由を because や具体的な経験で1〜2文加える。", "語数（15語以上）と、主語・動詞・時制の誤りがないかを確かめる。"],
                alt=["本文の登場人物の考えを例として引き、それに賛成・反対する形で自分の考えを書く方法もある。"],
                pc=[("質問への答え", 3), ("理由", 3), ("文法・語数", 2)],
                pit=["理由を書かずに答えだけで終える。", "質問の時制（would / did など）と答えの時制がずれる。"])


@gen("thinking_writing", 3, ["written_reasoning", "multiple_solutions"])
def graph_explain(r):
    g = r.choice(GRAPHS)
    task, sample, rubric = r.choice(g["tasks"])
    return desc(f"資料“{g['title']}”について答えなさい。\n{task}", sample,
                "資料の数値を正確に読み取り、比較の表現や数を表す語を使って書く。数値の大小や変化を、資料と照らし合わせて確かめる。",
                rubric, d=4, p=8, lines=5, stim=gstim(g),
                ap="まず資料から使う情報（項目・数値・曜日など）を2つ以上選び、それをどの表現（比較級・最上級・理由の because など）で書くかを決める。",
                steps=["資料の題名・単位・項目を確認する。", "条件に合う情報を資料から選ぶ。", "選んだ情報を英文（または日本語）で書く。",
                       "書いた内容を資料の数値ともう一度照らし合わせる。"],
                alt=["別の項目や別の比較の表現を使っても、資料と合っていれば正解になる（解答例は一例）。"],
                pc=[(c, v) for c, v in rubric],
                pit=["資料の数値と合わない比較（half / twice など）を書く。", "条件の文数や情報の数を満たさない。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

@gen("error_correction", 4, ["common_error", "written_reasoning"])
def err_detail(r):
    p = r.choice(PASSAGES)
    q, wrong, why, fix = r.choice(p["errs"])
    return desc(f"{head(p)}\n質問 {q} に、ある生徒は次のように答えた。\n［ある生徒の答え］{wrong}\nこの答えの誤りを本文の根拠を示して指摘し、正しい英語の答えに直しなさい。",
                f"誤り：{why}　正しい答え：{fix}",
                "質問のキーワードが出てくる本文の文をもう一度読み、だれが・いつ・何をしたかを確かめる。",
                [("誤りを本文の根拠とともに指摘している", 3), ("正しい英語の答えを書いている", 3)], d=3, p=6, lines=5, stim=pstim(p),
                ap="生徒の答えに出てくる語句が本文のどこにあるかを探し、それが質問の内容と本当に対応しているか（別の人物・別の場面・別の数字ではないか）を確かめる。",
                steps=["質問のキーワードを本文で探す。", "生徒の答えの内容が、本文のどの部分から来たかを確かめる。",
                       "質問と本文の内容がずれている点を指摘する。", f"正しい答え：{fix}"],
                alt=["生徒の答えを本文にもどして読み、その答えが別の質問への答えになっていないかを考える。"],
                pc=[("誤りの指摘", 3), ("正しい答え", 3)],
                pit=["本文の単語が答えに入っていれば正しいと思いこむ。"],
                err=dict(sol=wrong, step="本文の根拠の選び方", type="interpretation",
                         tempt="質問と似た語句が出てくる別の部分を根拠にしてしまった。", fix=fix))


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_graph(r):
    g = r.choice(GRAPHS)
    wrong, why, fix = r.choice(g["errs"])
    return desc(f"資料“{g['title']}”について、ある生徒が次の英文を書いた。\n［ある生徒の英文］{wrong}\nこの英文の誤りを資料の数値を使って指摘し、資料に合う正しい英文に直しなさい。",
                f"誤り：{why}　正しい英文（例）：{fix}",
                "英文の比較の表現・数を表す語（half / twice / the most / free など）を、資料の数値と1つずつ照らし合わせる。",
                [("誤りを資料の数値を使って指摘している", 3), ("資料に合う正しい英文を書いている", 3)], d=3, p=6, lines=5, stim=gstim(g),
                ap="生徒の英文の中の比較の表現や数を表す語に印をつけ、それが資料のどの数値と対応しているかを確かめる。",
                steps=["生徒の英文が、資料のどの項目について述べているかを確認する。", "資料の数値と照らし合わせ、合わない部分を見つける。",
                       "数値を使って誤りを説明する。", f"正しい英文：{fix}"],
                alt=["直した英文を資料の数値でもう一度確かめ、ほかの項目と比べても正しいかを確認する。"],
                pc=[("誤りの指摘", 3), ("正しい英文", 3)],
                pit=["数値を確かめずに half / the most などの語を使う。"],
                err=dict(sol=wrong, step="資料の数値と英文の照合", type="interpretation",
                         tempt="資料の印象（大きい・多い）だけで判断し、数値を正確に確かめなかった。", fix=fix))


@gen("error_correction", 3, ["common_error", "concept"])
def err_pronoun(r):
    p = r.choice(PASSAGES)
    sent, word, ok, wrongs = r.choice(p["refs"])
    wrong, why = r.choice(wrongs)
    return desc(f"{head(p)}\n次の文の下線部 {word} が指すものを、ある生徒は「{wrong}」と答えた。\n{sent}\nこの答えの誤りを指摘し、正しく答えなさい。",
                f"誤り：{why}　正しい答え：{ok}",
                f"{word} の前の部分から、数（単数・複数）や意味が合うものを探し、指示語の位置に入れて意味が通るかを確かめる。",
                [("誤りの理由を指摘している", 3), ("正しく答えている", 3)], d=3, p=6, lines=4, stim=pstim(p),
                ap="生徒の答えを指示語の位置に入れて読み、意味が通るか、数や人・物の区別が合っているかを確かめる。",
                steps=[f"生徒の答え「{wrong}」を {word} の位置に入れて読む。", "意味が通らない理由（数・人と物・場面の違い）を考える。",
                       "直前の部分から、条件に合う語句を探す。", f"正しい答え：{ok}"],
                alt=["正しい答えを指示語の位置に入れて日本語に訳し、文全体の意味が自然になることを確かめる。"],
                pc=[("誤りの理由", 3), ("正しい答え", 3)],
                pit=["指示語のすぐ前にある名詞を、意味を確かめずに答える。"],
                err=dict(sol=wrong, step=f"{word} が指す語句の特定", type="interpretation",
                         tempt="指示語の近くにある目立つ語句を、意味や数を確かめずに選んだ。", fix=ok))


GENERATORS = [detail, pronoun_ref, connector_fill, graph_read,
              true_statement, main_message, dialogue_gap, graph_calc, sentence_order,
              explain_jp, respond_english, graph_explain,
              err_detail, err_graph, err_pronoun]
