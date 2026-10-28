"""単元パック：中学1年 英語 名詞の複数形と代名詞（可算名詞の複数形・人称代名詞の格・所有代名詞）。"""
import random

from banks._common import desc, mc, order, sa
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem,
                         tp)

UNIT_ID = "JH-ENG-G1-U02"

PREREQUISITES = [
    ("JH-ENG-G1-U01", "主語が3人称単数か複数かによって be 動詞（is / are）や一般動詞の形（plays / play）が変わること。名詞を複数形にしたり代名詞に置きかえたりすると、動詞の形も合わせて変える必要がある。"),
    ("JH-JPN-G1-U03", "名詞・動詞などの品詞の区別。代名詞は「名詞の代わりをする語」であり、文の中で名詞と同じ位置（主語・目的語）に置かれることを理解する土台になる。"),
]
EXTENSIONS = [
    ("JH-ENG-G1-U03", "How many＋複数形 ～? や Whose ～ is this? ― It's mine. のように、複数形と所有代名詞は疑問詞を使った疑問文と答えの中で使われる。"),
    ("JH-ENG-G2-U03", "There is＋単数 / There are＋複数 のように、後ろの名詞が単数か複数かで be 動詞を使い分ける。"),
    ("JH-ENG-G3-U03", "関係代名詞 who / which / that にも主格・目的格の区別があり、この単元の「格」の考え方がそのまま使われる。"),
    ("HS-ENG-U06", "高校の関係詞では、所有格の関係代名詞 whose や、名詞を受ける代名詞の働きをさらに深く学ぶ。"),
]

# 名詞：(単数, 複数, 意味, 規則, 冠詞, 助数詞, まちがいやすいつづり)
R_S = "ふつうはそのまま s をつける"
R_ES = "s・x・sh・ch で終わる語には es をつける"
R_IES = "子音字＋y で終わる語は、y を i にかえて es をつける"
R_YS = "母音字（a・i・u・e・o）＋y で終わる語は、そのまま s をつける"
R_VES = "f・fe で終わる語の多くは、f・fe を v にかえて es をつける"
R_OES = "o で終わる語のうち、tomato・potato・hero などは es をつける"
R_OS = "o で終わる語でも、piano・photo などは s だけをつける"
R_IRR = "不規則に変化する"
R_SAME = "単数と複数が同じ形"
NOUNS = [
    ("book", "books", "本", R_S, "a", "冊", "bookes"), ("pen", "pens", "ペン", R_S, "a", "本", "penes"),
    ("cat", "cats", "ねこ", R_S, "a", "匹", "cates"), ("desk", "desks", "机", R_S, "a", "つ", "deskes"),
    ("egg", "eggs", "卵", R_S, "an", "個", "egges"), ("bag", "bags", "かばん", R_S, "a", "つ", "bages"),
    ("box", "boxes", "箱", R_ES, "a", "つ", "boxs"), ("bus", "buses", "バス", R_ES, "a", "台", "buss"),
    ("dish", "dishes", "皿", R_ES, "a", "枚", "dishs"), ("watch", "watches", "腕時計", R_ES, "a", "つ", "watchs"),
    ("class", "classes", "授業", R_ES, "a", "つ", "classs"), ("bench", "benches", "ベンチ", R_ES, "a", "つ", "benchs"),
    ("city", "cities", "都市", R_IES, "a", "つ", "citys"), ("country", "countries", "国", R_IES, "a", "か国", "countrys"),
    ("baby", "babies", "赤ちゃん", R_IES, "a", "人", "babys"), ("story", "stories", "物語", R_IES, "a", "つ", "storys"),
    ("dictionary", "dictionaries", "辞書", R_IES, "a", "冊", "dictionarys"), ("library", "libraries", "図書館", R_IES, "a", "つ", "librarys"),
    ("boy", "boys", "男の子", R_YS, "a", "人", "boies"), ("key", "keys", "かぎ", R_YS, "a", "つ", "keies"),
    ("toy", "toys", "おもちゃ", R_YS, "a", "つ", "toies"), ("day", "days", "日", R_YS, "a", "日", "daies"),
    ("leaf", "leaves", "葉", R_VES, "a", "枚", "leafs"), ("knife", "knives", "ナイフ", R_VES, "a", "本", "knifes"),
    ("tomato", "tomatoes", "トマト", R_OES, "a", "個", "tomatos"), ("potato", "potatoes", "じゃがいも", R_OES, "a", "個", "potatos"),
    ("piano", "pianos", "ピアノ", R_OS, "a", "台", "pianoes"), ("photo", "photos", "写真", R_OS, "a", "枚", "photoes"),
    ("child", "children", "子ども", R_IRR, "a", "人", "childs"), ("man", "men", "男性", R_IRR, "a", "人", "mans"),
    ("woman", "women", "女性", R_IRR, "a", "人", "womans"), ("foot", "feet", "足", R_IRR, "a", "本", "foots"),
    ("tooth", "teeth", "歯", R_IRR, "a", "本", "tooths"), ("mouse", "mice", "ねずみ", R_IRR, "a", "匹", "mouses"),
    ("sheep", "sheep", "羊", R_SAME, "a", "匹", "sheeps"),
]
# 「持っている」の文に使いやすい名詞
HAVE_NOUNS = [n for n in NOUNS if n[0] in ("book", "pen", "cat", "bag", "box", "dish", "watch", "dictionary", "key", "toy", "knife", "photo", "egg", "tomato", "potato")]
NUMS = [("two", 2), ("three", 3), ("four", 4), ("five", 5)]

# 人称代名詞：(主格, 所有格, 目的格, 所有代名詞, 日本語)
PRON = {
    "I": ("I", "my", "me", "mine", "私"),
    "you": ("you", "your", "you", "yours", "あなた"),
    "he": ("he", "his", "him", "his", "彼"),
    "she": ("she", "her", "her", "hers", "彼女"),
    "it": ("it", "its", "it", None, "それ"),
    "we": ("we", "our", "us", "ours", "私たち"),
    "they": ("they", "their", "them", "theirs", "彼ら"),
}
CASES = ["主格", "所有格", "目的格", "所有代名詞"]
CASE_USE = {"主格": "文の主語になる形（～は・～が）", "所有格": "後ろに名詞を続けて「～の」を表す形",
            "目的格": "動詞や前置詞の後ろに置く形（～を・～に）", "所有代名詞": "1語で「～のもの」を表す形（所有格＋名詞の代わり）"}
FILLER = {"you": "you're", "he": "he's", "she": "she's", "it": "it's"}
FILLER_WHY = {"you're": "you're は you are の短縮形で、代名詞の格の形ではない", "he's": "he's は he is の短縮形で、代名詞の格の形ではない",
              "she's": "she's は she is の短縮形で、代名詞の格の形ではない", "it's": "it's は it is の短縮形。「それの」は its（アポストロフィなし）"}


def be_for(p):
    return {"I": "am", "he": "is", "she": "is", "it": "is"}.get(p, "are")


def cap(s):
    return s[0].upper() + s[1:]


def local(key):
    return random.Random(key)


# ======================================================================
# 授業プリント
# ======================================================================

LESSON = lesson(
    goals=["数えられる名詞の複数形を、つづりの規則（s / es / ies / ves・不規則変化）にしたがって正しく書ける。",
           "人称代名詞の主格・所有格・目的格・所有代名詞を、文の中の位置から判断して使い分けられる。",
           "名詞を複数形や代名詞に置きかえたとき、be 動詞・一般動詞の形もあわせて正しく直せる。"],
    duration=50,
    readiness=["小学校の外国語で、I・you・he・she などを使った簡単な表現（He is ～. / She is ～.）を聞いたり話したりした経験がある。",
               "a dog / two dogs のように、ものの数を英語で言った経験がある。",
               "be 動詞（am / are / is）と3単現の s の使い分けができる（前の単元）。"],
    flow=[("導入：1つと2つ以上", 5, "I have a cat. と I have two cats. を比べ、英語では数えられる名詞の数を必ず形で表すことに気づかせる"),
          ("複数形のつくり方", 13, "s / es / ies / ves と不規則変化を、語の終わりのつづりで整理する（例題1）"),
          ("人称代名詞の格", 17, "主格・所有格・目的格・所有代名詞の表を完成させ、文の中の位置で形が決まることを確かめる（例題2）"),
          ("置きかえと動詞の一致", 8, "名詞を代名詞や複数形にしたときの be 動詞・一般動詞の変化を練習する（例題3）"),
          ("まとめと確認", 7, "確認問題3問、問題プリントA の課題指示")],
    sections=[
        intro("in1", "英語は「いくつあるか」を名詞の形で表す",
              "日本語では「ねこを飼っています」と言えば、1匹でも2匹でも同じ形です。英語では、数えられる名詞が1つのときは a cat、2つ以上のときは cats のように、名詞の形そのものを変えます。また、同じ人を何度も名前で呼ぶ代わりに he や she などの代名詞を使いますが、代名詞は文の中のどの位置に置くかによって he / his / him のように形が変わります。この単元では、この2つの「形の変化」を学びます。",
              bullets=["I have a cat.（1匹）／ I have two cats.（2匹以上）", "Ken is my friend. I like him.（him は Ken を受ける）",
                       "名詞や代名詞の形が変わると、be 動詞や一般動詞の形も変わることがある。"],
              points=[tp("I have a cat. と I have two cats. を板書し、日本語訳がどちらも「ねこを飼っている」になることを確認してから、英語の違いに注目させる。",
                         ask="2つの英文で違うところはどこか。", expect="a があるかないか、cat に s がつくかどうか。", timing="導入の冒頭")]),
        definition("df1", "数えられる名詞と複数形",
                   "1つ、2つと数えられる名詞（可算名詞）は、2つ以上のとき複数形にします。1つのときは a / an をつけ、複数形には a / an をつけません。",
                   bullets=["ふつうは s：book → books、egg → eggs", "s・x・sh・ch で終わる語は es：box → boxes、dish → dishes、watch → watches",
                            "子音字＋y は y を i にかえて es：city → cities、母音字＋y は s：boy → boys", "f・fe の多くは ves：leaf → leaves、knife → knives",
                            "o で終わる語：tomato → tomatoes、potato → potatoes（piano → pianos、photo → photos は s）",
                            "不規則変化：child → children、man → men、woman → women、foot → feet、tooth → teeth、mouse → mice、sheep → sheep（同じ形）"],
                   conditions=["water・milk・money・music・rice などの数えられない名詞は、a / an をつけず、複数形にもしない。",
                               "two・three・many・some（いくつかの）や these・those の後ろの数えられる名詞は複数形にする。"],
                   points=[tp("つづりの規則は「語の終わりの文字」を見ることから始めさせ、ノートに規則ごとの表を作らせる。",
                              caution="sheep のように単数と複数が同じ形の語や、children のような不規則変化は、まとめて覚える時間をとる。")]),
        theorem("th1", "人称代名詞の格（主格・所有格・目的格・所有代名詞）",
                "I-my-me-mine／you-your-you-yours／he-his-him-his／she-her-her-hers／it-its-it／we-our-us-ours／they-their-them-theirs",
                ["主格：文の主語（～は・～が）。動詞の前に置く。", "所有格：「～の」。必ず後ろに名詞が続く（my bag, her brother）。",
                 "目的格：「～を・～に」。動詞や前置詞（with, to, for, at など）の後ろに置く。", "所有代名詞：「～のもの」。1語で「所有格＋名詞」の代わりをし、後ろに名詞は続かない（This bag is mine.）。",
                 "人の名前の所有格は 's をつける（Ken's bag）。Ken's は「ケンのもの」の意味にもなる（This bag is Ken's.）。"],
                body="her は所有格と目的格が同じ形、his は所有格と所有代名詞が同じ形、you は主格と目的格が同じ形です。同じつづりでも、文の中での働きは位置で決まります。",
                points=[tp("表は「縦に読む（I-my-me-mine）」練習と「横に読む（my-your-his-her…）」練習の両方をさせて、声に出して定着させる。",
                           ask="her が「彼女の」か「彼女を」かは、どうすればわかるか。", expect="後ろに名詞があれば所有格、なければ目的格。"),
                        tp("its と it's を混同しないよう、「it's は it is の短縮形」と板書で区別する。", caution="it's を「それの」の意味で書く誤りは高校生にも多い。")]),
        derivation("dv1", "代名詞の形を決める手順（なぜその形になるのか）",
                   ["① 代名詞が指す人やものを確かめる。1人の男性 → he、1人の女性 → she、もの1つ → it、2人・2つ以上 → they、自分をふくむ2人以上 → we。",
                    "② 空所が文のどの位置にあるかを見る。動詞の前（主語の位置）なら主格。",
                    "③ 空所の後ろに名詞が続いていれば、「～の」を表す所有格。",
                    "④ 動詞や前置詞の直後で、後ろに名詞が続かなければ目的格。",
                    "⑤ 「～のもの」の意味で、後ろに名詞が続かず、主語や be 動詞の後ろにあれば所有代名詞。",
                    "⑥ 主語を代名詞や複数形にかえたときは、前の単元の規則で be 動詞・一般動詞の形も合わせる（Ken plays → They play など）。"],
                   body="英語は語順で意味が決まる言語なので、代名詞の形も「どの位置に置かれたか」で決まります。日本語の「は・の・を」にあたる働きを、英語では形の変化で表していると考えるとよいでしょう。",
                   points=[tp("手順②〜⑤を「前に動詞なし→主格／後ろに名詞→所有格／動詞・前置詞の後ろ→目的格／～のもの→所有代名詞」と短くまとめて板書する。", timing="例題2の前")]),
        example("ex1", "例題1　複数形をつくる",
                "（　）内の名詞を正しい形にしなさい。(1) I have three (box).　(2) Ms. Green has two (child).　(3) I know many (city) in Japan.",
                ["(1) three の後ろなので複数形。box は x で終わるので es → boxes。", "(2) two の後ろなので複数形。child は不規則変化 → children。",
                 "(3) many の後ろなので複数形。city は子音字＋y なので y を i にかえて es → cities。"],
                "(1) boxes　(2) children　(3) cities",
                thinking="数を表す語（two・three・many など）の後ろは複数形。つづりは語の終わりで決める。",
                points=[tp("答え合わせでは、boxes・cities の語尾の発音（ズ／イズ）も確認し、つづりと音を結びつける。")],
                misconceptions=[("three boxs", "x で終わる語には es をつける。boxes。"), ("two childs", "child は不規則変化。children。")]),
        example("ex2", "例題2　代名詞の格を選ぶ",
                "（　）内から正しい語を選びなさい。(1) This is Aya. (She / Her) is my classmate.　(2) I like (she / her) songs.　(3) Do you know (they / them)?　(4) This umbrella is (my / mine).",
                ["(1) 動詞 is の前で主語の位置 → 主格 She。", "(2) 後ろに名詞 songs が続く → 所有格 her。",
                 "(3) 動詞 know の後ろで、後ろに名詞がない → 目的格 them。", "(4) 「私のもの」の意味で後ろに名詞がない → 所有代名詞 mine。"],
                "(1) She　(2) her　(3) them　(4) mine",
                thinking="空所の前後を見て、主語の位置か、後ろに名詞があるか、動詞・前置詞の後ろかを確かめる。",
                points=[tp("(2) と「I like her.」を並べ、同じ her でも後ろに名詞があるかで所有格・目的格が分かれることを確認する。",
                           ask="I like her. の her は何格か。", expect="後ろに名詞がないので目的格。")]),
        example("ex3", "例題3　置きかえると動詞も変わる",
                "下線部を代名詞にかえ、さらに全文を「友だちが2人いる」場合の文に書きかえなさい。This is my friend. [[u:My friend]] plays the piano.",
                ["My friend を代名詞にすると He / She。", "2人の場合：This is → These are、friend → friends。", "主語が They になるので、plays → play（3単現の s をとる）。"],
                "These are my friends. They play the piano.",
                thinking="名詞を複数にすると、this → these、be 動詞、代名詞、一般動詞の s まで連動して変わる。",
                points=[tp("変わった語に下線を引かせ、「なぜ変わったか」を1つずつ言わせる。")],
                misconceptions=[("These are my friends. They plays the piano.", "主語 They は複数なので s はつけない。")]),
        board("bd1", "板書案",
              [("① 複数形", ["ふつう＋s：books", "s・x・sh・ch＋es：boxes", "子音字＋y → ies：cities", "f・fe → ves：knives", "不規則：children・men・feet"]),
               ("② 代名詞の格", ["主格（～は）I he she they", "所有格（～の）＋名詞 my his her their", "目的格（～を）動詞・前置詞の後 me him her them", "所有代名詞（～のもの）mine his hers theirs", "its（それの）≠ it's（it is）"]),
               ("③ 置きかえと一致", ["this → these／that → those", "is → are", "he / she → they", "plays → play", "a / an は複数形につけない"])],
              points=[tp("②の列は表の形で書き、生徒に空欄を埋めさせながら完成させる。③は例題3の答えと対応させる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("複数形の規則は、発音とセットで練習させる（boxes・dishes・watches は語尾が「イズ」になる）。"),
               tp("代名詞の格は、空所の「前後」を見る習慣をつけさせる。", ask="I play tennis with (he / him). の空所の前には何があるか。", expect="前置詞 with。だから目的格 him。"),
               tp("所有代名詞を使う文では、後ろに名詞を置かないことを強調する（This is mine bag. は誤り）。", caution="mine を my と同じように使う誤りが多い。"),
               tp("Ken and I（主語）／Ken and me（目的語）のように、and でつないでも格の規則は同じことを補足する。", timing="例題2の後"),
               tp("問題プリント D では「つづりの誤り」「数の一致の誤り」「格の誤り」の3種類に分けて整理させる。")],
              misconceptions=[("I have two boxs.", "x で終わる語は es。two boxes。"),
                              ("I often play with he.", "前置詞 with の後ろは目的格。with him。"),
                              ("This pen is her's.", "所有代名詞にアポストロフィはつかない。hers。")]),
        summary("sm1", "まとめ",
                ["数えられる名詞は、2つ以上のとき複数形にする。つづりは語の終わりで決まり、不規則変化は覚える。",
                 "代名詞は位置で形が決まる：主語→主格、名詞の前→所有格、動詞・前置詞の後→目的格、「～のもの」→所有代名詞。",
                 "名詞を複数形や代名詞にしたら、be 動詞・一般動詞の形もあわせて直す。"]),
        check("ck1", "確認問題",
              [("knife と tooth の複数形を書きなさい。", "knives、teeth"),
               ("I know (he / his / him) brother. の（　）に入る語を選びなさい。", "his（後ろに名詞 brother が続くので所有格）"),
               ("This is our classroom. を、ours を使ってほぼ同じ意味の文にしなさい。", "This classroom is ours.")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

def bad_plural(n):
    return n[6]


@gen("basic_check", 4, ["computation"])
def plural_spell(r):
    sg, pl, m, rule, *_ = r.choice(NOUNS)
    return sa(f"次の名詞の複数形を書きなさい。\n{sg}（{m}）", pl, f"{rule}ので {pl}。", d=1,
              ap="語の終わりのつづりを見て、s・es・ies・ves のどれになるか、または不規則変化かを判断する。",
              steps=[f"語の終わりを確認する：{sg}。", f"規則を当てはめる：{rule}。", f"答え：{pl}"],
              alt=[f"two {pl} のように数といっしょに声に出して、発音とつづりが合っているかを確かめる。"],
              pc=[("規則を正しく選んでいる", 1), ("正しいつづりで書いている", 1)],
              pit=["どの語にも s だけをつけてしまう（boxs, citys など）。", "不規則変化の語に s をつけてしまう（childs, mans など）。"])


PFRAMES = [
    # (英文の型, 格, 日本語の型, 使える代名詞)
    ("(　) {be} in the gym now.", "主格", "{X}は今、体育館にいます。", ["I", "you", "he", "she", "we", "they"]),
    ("(　) {be} good at singing.", "主格", "{X}は歌が得意です。", ["I", "you", "he", "she", "we", "they"]),
    ("This is (　) bike.", "所有格", "これは{X}の自転車です。", ["I", "you", "he", "she", "we", "they"]),
    ("(　) mother is a nurse.", "所有格", "{X}のお母さんは看護師です。", ["I", "you", "he", "she", "we", "they"]),
    ("Ken knows (　) brother well.", "所有格", "ケンは{X}のお兄さんをよく知っています。", ["I", "you", "he", "she", "we", "they"]),
    ("Look at the dog. (　) name is Pochi.", "所有格", "あの犬を見て。それの名前はポチです。", ["it"]),
    ("Ms. Green knows (　) well.", "目的格", "グリーン先生は{X}をよく知っています。", ["I", "you", "he", "she", "we", "they"]),
    ("Ken often plays with (　).", "目的格", "ケンはよく{X}と遊びます。", ["I", "you", "he", "she", "we", "they"]),
    ("Please help (　).", "目的格", "{X}を手伝ってください。", ["I", "he", "she", "we", "they"]),
    ("I have a cat. I love (　) very much.", "目的格", "私はねこを飼っています。私はそれが大好きです。", ["it"]),
    ("This notebook is (　).", "所有代名詞", "このノートは{X}のものです。", ["I", "you", "he", "she", "we", "they"]),
    ("Those bikes are (　).", "所有代名詞", "あれらの自転車は{X}のものです。", ["I", "you", "he", "she", "we", "they"]),
]


@gen("basic_check", 4, ["condition_check", "concept"])
def pron_case(r):
    fr, case, jpt, allowed = r.choice(PFRAMES)
    p = r.choice(allowed)
    forms = PRON[p]
    ok = forms[CASES.index(case)]
    s = fr.replace("{be}", be_for(p))
    capf = s.startswith("(　)") or ". (　)" in s
    if capf:
        ok = cap(ok)
    uniq = []
    for f in forms[:4]:
        if f and f != forms[CASES.index(case)] and f not in uniq:
            uniq.append(f)
    if len(uniq) < 3:
        uniq.append(FILLER[p])
    if p == "it":
        uniq.append({"所有格": "their", "目的格": "them"}[case])
    wrongs = [cap(w) if capf else w for w in uniq]
    why = {}
    for w in wrongs:
        lw = w.lower() if w != "I" else w
        if p == "it" and lw in ("their", "them"):
            why[w] = (f"{lw} は they の形で、2つ以上のものを指す。ここで指しているのは1匹（1つ）なので it の仲間を使う。", "単数・複数の代名詞の混同")
        elif lw in FILLER_WHY:
            why[w] = (FILLER_WHY[lw] + "。", "短縮形と代名詞の格の混同")
        else:
            c = [CASES[i] for i, f in enumerate(forms[:4]) if f == lw and CASES[i] != case][0]
            why[w] = (f"{w} は{c}で、{CASE_USE[c]}。この空所は{CASE_USE[case]}が必要な位置。", f"{c}と{case}の混同")
    J = jpt.replace("{X}", forms[4])
    return mc(f"日本語の意味を表すように、（　）に入る最も適切な語を選びなさい。\n{J}\n{s}", [ok] + wrongs,
              f"この空所は{CASE_USE[case]}が入る位置なので、{forms[4]}（{p}）の{case} {ok} を使う。", d=2,
              ap="空所の位置を見る。動詞の前なら主格、後ろに名詞があれば所有格、動詞・前置詞の後ろなら目的格、「～のもの」なら所有代名詞。",
              steps=["空所の前後に何があるかを確かめる。", f"空所の働きを判断する：{CASE_USE[case]}。", f"{p} の{case}は {forms[CASES.index(case)]}。答え：{ok}"],
              alt=[f"{p} の4つの形（{'・'.join(f for f in forms[:4] if f)}）を順に入れて読み、日本語の意味に合うものを確かめる。"],
              pc=[("空所の働き（格）を正しく判断している", 1), ("正しい形を選んでいる", 1)],
              pit=["日本語の「～を」「～の」だけで判断し、空所の後ろに名詞があるかを確かめない。", "her・his のように同じ形の格を取り違える。"], why=why)


SG_FRAMES = [("I have {art} (　).", "私は{m}を1{c}持っています。"), ("This is my (　).", "これは私の{m}です。"), ("Is that your (　)?", "あれはあなたの{m}ですか。")]
PL_FRAMES = [("I have {num} (　).", "私は{m}を{n}{c}持っています。"), ("These are my (　).", "これらは私の{m}です。"),
             ("Ken has many (　).", "ケンは{m}をたくさん持っています。"), ("Are those your (　)?", "あれらはあなたの{m}ですか。")]


@gen("basic_check", 4, ["common_error", "condition_check"])
def noun_form(r):
    n = r.choice(HAVE_NOUNS)
    sg, pl, m, rule, art, c, bad = n
    if r.random() < 0.6:
        fr, jpt = r.choice(PL_FRAMES)
        num, k = r.choice(NUMS)
        s = fr.replace("{num}", num)
        J = jpt.replace("{m}", m).replace("{n}", str(k)).replace("{c}", c)
        ok = pl
        need = "数えられる名詞が2つ以上なので複数形"
        why = {sg: (f"{sg} は単数形。{need}にする。", "単数・複数の判断の誤り"),
               bad: (f"{bad} というつづりはない。{rule}ので {pl}。", "複数形のつづりの規則の誤り"),
               f"{sg}'s": (f"{sg}'s は「～の」を表す所有の形で、複数形ではない。", "所有を表す 's と複数形の s の混同")}
    else:
        fr, jpt = r.choice(SG_FRAMES)
        s = fr.replace("{art}", art)
        J = jpt.replace("{m}", m).replace("{c}", c)
        ok = sg
        need = "a / an や this・that（is）があるので単数形"
        why = {pl: (f"{pl} は複数形。{need}にする。", "単数・複数の判断の誤り"),
               bad: (f"{bad} は複数形のつもりの誤ったつづりで、しかもこの文には単数形が必要。", "複数形のつづりの規則の誤り"),
               f"{sg}'s": (f"{sg}'s は「～の」を表す所有の形で、後ろに名詞が必要。", "所有を表す 's と名詞の形の混同")}
    return mc(f"日本語の意味を表すように、（　）に入る最も適切なものを選びなさい。\n{J}\n{s}", [ok] + list(why),
              f"{need}。答えは {ok}。", d=2,
              ap="（　）の前に a / an・this・that があれば単数、two・many・these・those があれば複数と考える。複数ならつづりの規則も確かめる。",
              steps=["（　）の前にある語（a / an、数、these など）を確かめる。", "単数形か複数形かを決める。", f"つづりを確かめて {ok} を選ぶ。"],
              alt=["日本語の意味（1つか、2つ以上か）からも、単数か複数かを確かめる。"],
              pc=[("単数・複数を正しく判断している", 1), ("正しいつづりの語を選んでいる", 1)],
              pit=["数を表す語があるのに単数形のままにする。", "所有の 's と複数形の s を混同する。"], why=why)


@gen("basic_check", 4, ["computation", "concept"])
def pron_table(r):
    p = r.choice(list(PRON))
    forms = PRON[p]
    idx = [i for i in (1, 2, 3) if forms[i]]
    i = r.choice(idx)
    case = CASES[i]
    ans = forms[i]
    return sa(f"人称代名詞の表を完成させます。{p}（{forms[4]}は）の{case}を書きなさい。（{case}：{CASE_USE[case]}）", ans,
              f"{p} の変化は {'－'.join(f for f in forms[:4] if f)}。{case}は {ans}。", d=1,
              ap="主格→所有格→目的格→所有代名詞の順に、声に出して表を言ってみる。",
              steps=[f"{p} の変化を順に言う：{'－'.join(f for f in forms[:4] if f)}。", f"{case}にあたる形を選ぶ：{ans}。"],
              alt=[f"{case}を使った短い文（例：{ {'所有格': f'This is {forms[1]} bag.', '目的格': f'Ken likes {forms[2]}.', '所有代名詞': f'This bag is {forms[3]}.'}[case] }）を作って確かめる。"],
              pc=[("正しい格を選んでいる", 1), ("正しいつづりで書いている", 1)],
              pit=["her と hers、its と it's を取り違える。", "所有代名詞にアポストロフィをつける（her's など）。"])


@gen("basic_check", 4, ["concept", "condition_check"])
def this_these(r):
    n = r.choice(HAVE_NOUNS)
    sg, pl, m = n[0], n[1], n[2]
    near = r.random() < 0.5
    plural = r.random() < 0.5
    if plural:
        ok = "These are" if near else "Those are"
        noun = pl
        J = f"{'これら' if near else 'あれら'}は私の{m}です。"
        cands = [ok, "This is" if near else "That is", "These is" if near else "Those is", "This are" if near else "That are"]
    else:
        ok = "This is" if near else "That is"
        noun = sg
        J = f"{'これ' if near else 'あれ'}は私の{m}です。"
        cands = [ok, "These are" if near else "Those are", "These is" if near else "Those is", "This are" if near else "That are"]
    word = ok.split()[0]
    why = {}
    for w in cands[1:]:
        a, b = w.split()
        if a in ("These", "Those") and b == "is":
            why[w] = (f"{a} は複数を指すので、be 動詞は are にする。", "主語の数と be 動詞の一致の誤り")
        elif a in ("This", "That") and b == "are":
            why[w] = (f"{a} は1つのものを指すので、be 動詞は is にする。", "主語の数と be 動詞の一致の誤り")
        else:
            why[w] = (f"後ろの名詞 {noun} は{'複数形' if plural else '単数形'}なので、{'These / Those' if plural else 'This / That'} を使う。{w} では数が合わない。", "this / these の使い分けの誤り")
    return mc(f"日本語の意味を表すように、（　）に入る最も適切なものを選びなさい。\n{J}\n(　) my {noun}.", [ok] + cands[1:],
              f"後ろの名詞 {noun} は{'複数形なので These / Those、be 動詞は are' if plural else '単数形なので This / That、be 動詞は is'}。近くのものは this / these、遠くのものは that / those。答えは {ok}。", d=2,
              ap="後ろの名詞が単数形か複数形かを見て、this / these（that / those）と be 動詞を同時に決める。",
              steps=[f"後ろの名詞 {noun} が{'複数形' if plural else '単数形'}であることを確かめる。", f"{'近く' if near else '遠く'}のものなので {word} を使う。", f"be 動詞を合わせて {ok}。"],
              alt=["日本語の「これ・これら・あれ・あれら」から、近いか遠いか・1つか2つ以上かを確かめる。"],
              pc=[("this / these などを正しく選んでいる", 1), ("be 動詞を正しく合わせている", 1)],
              pit=["These の後ろに is を使う。", "複数形の名詞に This を使う。"], why=why)


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "condition_check"])
def to_plural(r):
    n = r.choice(HAVE_NOUNS)
    sg, pl, m, rule, art = n[:5]
    typ = r.choice(["this", "that", "have", "q"])
    num, k = r.choice(NUMS)
    if typ == "this":
        src, ans, how = f"This is my {sg}.", f"These are my {pl}.", f"This is → These are、{sg} → {pl}"
        inst = "下線部を These にかえて"
        src = f"[[u:This]] is my {sg}."
    elif typ == "that":
        src, ans, how = f"[[u:That]] is {art} {sg}.", f"Those are {pl}.", f"That is → Those are、{art} を取り、{sg} → {pl}"
        inst = "下線部を Those にかえて"
    elif typ == "have":
        S = r.choice([("I", "have"), ("Ken", "has"), ("We", "have"), ("My sister", "has")])
        src, ans, how = f"{S[0]} {S[1]} [[u:{art}]] {sg}.", f"{S[0]} {S[1]} {num} {pl}.", f"{art} → {num}、{sg} → {pl}"
        inst = f"下線部を {num} にかえて"
    else:
        src, ans, how = f"Is [[u:this]] your {sg}?", f"Are these your {pl}?", f"Is this → Are these、{sg} → {pl}"
        inst = "下線部を these にかえて"
    return sa(f"{inst}、全文を書きかえなさい。\n{src}", ans, f"{how}。{rule}ので {pl}。", d=2,
              ap="名詞が複数になると、名詞の形だけでなく、this → these、is → are、a / an の削除など、まわりの語も変わる。",
              steps=["下線部をかえると名詞が複数になることを確かめる。", f"まわりの語を直す：{how}。", f"答え：{ans}"],
              alt=["書きかえた文を日本語に訳し、「2つ以上」の意味になっているか、be 動詞と名詞の数が合っているかを確かめる。"],
              pc=[("名詞を正しい複数形にしている", 2), ("be 動詞・this / these・a / an を正しく直している", 2)],
              pit=["名詞だけ複数形にして、is や a を残す。", "複数形のつづりを誤る。"])


PEOPLE = [("Ms. Green", "she", "グリーン先生"), ("Mr. Sato", "he", "佐藤先生"), ("Ken", "he", "ケン"), ("Aya", "she", "アヤ"),
          ("my mother", "she", "私の母"), ("my father", "he", "私の父"), ("Tom and Emi", "they", "トムとエミ"), ("my parents", "they", "私の両親"),
          ("Ken and I", "we", "ケンと私")]
RFRAMES = [
    ("{N} {be} in the library now.", "主格"),
    ("{N} {be} from Canada.", "主格"),
    ("Do you know {N}?", "目的格"),
    ("I often talk with {N}.", "目的格"),
    ("Mr. Brown teaches {N} English.", "目的格"),
    ("{N}'s house is near the park.", "所有格"),
    ("I sometimes use {N}'s computer.", "所有格"),
]


@gen("standard_practice", 4, ["computation", "concept"])
def to_pronoun(r):
    fr, case = r.choice(RFRAMES)
    cands = [p for p in PEOPLE if not (case == "所有格" and p[1] in ("they", "we"))]
    if case == "目的格":
        cands = [p for p in cands if p[0] != "Ken and I"]  # 目的語の位置なら Ken and me になるため除く
    N, p, jn = r.choice(cands)
    be = "are" if p in ("they", "we") else "is"
    src0 = fr.replace("{be}", be)
    if fr.startswith("{N}"):
        Nshow = N[0].upper() + N[1:]
        src = src0.replace("{N}'s" if case == "所有格" else "{N}", f"[[u:{Nshow}{chr(39) + 's' if case == '所有格' else ''}]]", 1)
    else:
        src = src0.replace("{N}'s" if case == "所有格" else "{N}", f"[[u:{N}{chr(39) + 's' if case == '所有格' else ''}]]", 1)
    word = PRON[p][CASES.index(case)]
    ans = src0.replace("{N}'s" if case == "所有格" else "{N}", word, 1)
    ans = cap(ans) if fr.startswith("{N}") else ans
    num = {"she": "女性1人", "he": "男性1人", "they": "2人", "we": "自分をふくむ2人"}[p]
    return sa(f"下線部を適切な代名詞1語に置きかえて、英文全体を書き直しなさい。\n{src}", ans,
              f"{jn}は{num}なので {p} の仲間。下線部は{CASE_USE[case]}の位置なので{case} {word}。", d=2,
              ap="①下線部が何人（いくつ）で、男性か女性か（自分をふくむか）、②文の中でどの位置にあるか、の2点で代名詞を決める。",
              steps=[f"下線部 {N} を受ける代名詞の仲間を決める：{p}（{num}）。", f"位置から格を決める：{case}（{CASE_USE[case]}）。", f"答え：{ans}"],
              alt=["書き直した文の代名詞をもとの語句にもどして読み、意味が変わっていないかを確かめる。"],
              pc=[("正しい代名詞の仲間（人称・数・性別）を選んでいる", 2), ("位置に合う格の形にしている", 2)],
              pit=["Ken and I を they にする（自分をふくむので we / us）。", "Ken's を he's にする（所有格は his）。"])


OWNERS = [("my", "mine", "私"), ("your", "yours", "あなた"), ("his", "his", "彼"), ("her", "hers", "彼女"), ("our", "ours", "私たち"),
          ("their", "theirs", "彼ら"), ("Ken's", "Ken's", "ケン"), ("Aya's", "Aya's", "アヤ")]
THINGS = [("bag", "bags"), ("umbrella", "umbrellas"), ("bike", "bikes"), ("notebook", "notebooks"), ("racket", "rackets"), ("cap", "caps"), ("dictionary", "dictionaries")]


@gen("standard_practice", 4, ["application", "condition_check"])
def possessive_rewrite(r):
    poss, pp, who = r.choice(OWNERS)
    sg, pl = r.choice(THINGS)
    typ = r.choice(["this", "that", "these", "q"])
    plural = typ == "these"
    noun = pl if plural else sg
    if typ == "q":
        a, b = f"Is this {poss} {noun}?", f"Is this {noun} {pp}?"
    else:
        dem = {"this": "This", "that": "That", "these": "These"}[typ]
        bev = "are" if plural else "is"
        a, b = f"{dem} is {poss} {noun}.".replace("These is", "These are"), f"{dem} {noun} {bev} {pp}."
    rev = r.random() < 0.35
    src, ans = (b, a) if rev else (a, b)
    if poss.endswith("'s"):
        tgt = f"{poss}（～の）" if rev else f"{pp}（～のもの）"
    else:
        tgt = f"所有格 {poss}" if rev else f"所有代名詞 {pp}"
    return sa(f"次の英文を、{tgt} を使ってほぼ同じ意味の文に書きかえなさい。\n{src}", ans,
              f"「{who}の{noun}」＝「{who}のもの」。{poss} {noun} と {pp} が同じ意味になる。所有代名詞の後ろには名詞を置かない。", d=3,
              ap="所有格＋名詞（my bag）と所有代名詞（mine）は同じ内容を表す。名詞をどこに置くかを入れかえる。",
              steps=[f"「{poss} {noun}」と「{pp}」の対応を確かめる。", "名詞を主語の this / that / these の後ろに移す（または be 動詞の後ろにもどす）。", f"答え：{ans}"],
              alt=["書きかえた文を日本語に訳し、もとの文と同じ意味になるかを確かめる。"],
              pc=[("所有格・所有代名詞を正しく使っている", 2), ("語順（名詞の位置）が正しい", 2)],
              pit=["This is mine bag. のように、所有代名詞の後ろに名詞を置く。", "hers・theirs にアポストロフィをつける。"])


ORDERS = [
    ("私は彼女のお兄さんをよく知っています。", ["I", "know", "her", "brother", "well"]),
    ("これらの写真は私たちのものです。", ["these", "photos", "are", "ours"]),
    ("彼らの子どもたちはとても親切です。", ["their", "children", "are", "very", "kind"]),
    ("ケンはよく彼といっしょにテニスをします。", ["Ken", "often", "plays", "tennis", "with", "him"]),
    ("あれらの箱はあなたのものですか。", ["are", "those", "boxes", "yours"]),
    ("私の姉は辞書を3冊持っています。", ["my", "sister", "has", "three", "dictionaries"]),
    ("私たちは彼らをよく手伝います。", ["we", "often", "help", "them"]),
    ("あの女性たちは私の先生です。", ["those", "women", "are", "my", "teachers"]),
    ("私の兄は自分の部屋でよく本を読みます。", ["my", "brother", "often", "reads", "books", "in", "his", "room"]),
    ("（飼っている犬について）その犬の名前はコロです。", ["its", "name", "is", "Koro"]),
    ("グリーン先生は私たちに英語を教えています。", ["Ms. Green", "teaches", "us", "English"]),
    ("このかさは彼のものではありません。", ["this", "umbrella", "is", "not", "his"]),
    ("私の父はナイフを2本持っています。", ["my", "father", "has", "two", "knives"]),
    ("あなたは彼女たちを知っていますか。", ["do", "you", "know", "them"]),
]


@gen("standard_practice", 4, ["application", "computation"])
def build_order(r):
    jp, parts = r.choice(ORDERS)
    sent = " ".join(parts)
    q = parts[0] in ("are", "do")
    sent = cap(sent) + ("?" if q else ".")
    return order(f"日本語の意味を表す英文になるように、次の語を正しい順に並べなさい。文の最初にくる語も小文字で示してある。\n{jp}", parts,
                 f"{sent}　代名詞は位置で形が決まり（主語→主格、名詞の前→所有格、動詞・前置詞の後→目的格）、2つ以上のものは複数形で表す。", d=3, p=4,
                 ap="まず主語と動詞を決め、代名詞が「主語・名詞の前・動詞や前置詞の後ろ」のどこに入るかを考える。",
                 steps=["主語と動詞（be 動詞・一般動詞）を見つけて先頭に置く。", "所有格は名詞の直前、目的格は動詞・前置詞の直後に置く。", f"完成文：{sent}"],
                 alt=["完成した英文を日本語に訳し直して、問題の日本語と一致するかを確かめる。"],
                 pc=[("主語・動詞の位置が正しい", 2), ("代名詞・名詞の位置が正しい", 2)],
                 pit=["所有格を名詞から離して置く。", "疑問文で be 動詞や do を文頭に置かない。"])


def make_error(kind, r):
    """よくある誤り：dict(wrong, fix, jp, where, type, rule, tempt, label)"""
    if kind == "spell":
        n = r.choice(HAVE_NOUNS)
        num, k = r.choice(NUMS)
        S = r.choice([("I", "have", "私は"), ("My brother", "has", "私の兄は"), ("We", "have", "私たちは")])
        return dict(wrong=f"{S[0]} {S[1]} {num} {n[6]}.", fix=f"{S[0]} {S[1]} {num} {n[1]}.", jp=f"{S[2]}{n[2]}を{k}{n[5]}持っています。",
                    where=n[6], type="notation", rule=f"{n[3]}ので、{n[0]} の複数形は {n[1]}",
                    tempt="複数形は「s をつける」とだけ覚えていて、語の終わりのつづりによる変化を確かめなかった。", label="複数形のつづりの誤り")
    if kind == "no_pl":
        n = r.choice(HAVE_NOUNS)
        num, k = r.choice(NUMS)
        return dict(wrong=f"Ken has {num} {n[0]}.", fix=f"Ken has {num} {n[1]}.", jp=f"ケンは{n[2]}を{k}{n[5]}持っています。",
                    where=f"{num} {n[0]}", type="condition", rule=f"{num} の後ろの数えられる名詞は複数形にするので {n[1]}",
                    tempt="日本語では「3冊の本」でも「本」の形が変わらないので、英語でも名詞をそのままにした。", label="複数形にし忘れる誤り")
    if kind == "a_pl":
        n = r.choice(HAVE_NOUNS)
        return dict(wrong=f"I have {n[4]} {n[1]}.", fix=f"I have {n[4]} {n[0]}.", jp=f"私は{n[2]}を1{n[5]}持っています。",
                    where=f"{n[4]} {n[1]}", type="condition", rule=f"a / an は1つのものにつけるので、後ろは単数形 {n[0]}",
                    tempt="名詞にはいつも s をつけるものだと思い込み、a / an との組み合わせを確かめなかった。", label="a / an と複数形を組み合わせる誤り")
    if kind == "these_sg":
        n = r.choice(HAVE_NOUNS)
        return dict(wrong=f"These are my {n[0]}.", fix=f"These are my {n[1]}.", jp=f"これらは私の{n[2]}です。",
                    where=n[0], type="condition", rule=f"These は2つ以上のものを指すので、名詞も複数形 {n[1]} にする",
                    tempt="These are にしたことで複数を表せたと考え、名詞の形を直さなかった。", label="these と単数形を組み合わせる誤り")
    if kind == "uncount":
        w, f, j = r.choice([("I drink milks every morning.", "I drink milk every morning.", "私は毎朝牛乳を飲みます。"),
                            ("We need waters.", "We need water.", "私たちは水が必要です。"),
                            ("I don't have moneys now.", "I don't have money now.", "私は今、お金を持っていません。"),
                            ("My father likes breads.", "My father likes bread.", "私の父はパンが好きです。"),
                            ("We eat rices every day.", "We eat rice every day.", "私たちは毎日ごはんを食べます。"),
                            ("Ken listens to musics after dinner.", "Ken listens to music after dinner.", "ケンは夕食後に音楽を聞きます。")])
        word = [x for x in w.split() if x.rstrip(".") not in f.split() and x not in f.split()][0].rstrip(".")
        return dict(wrong=w, fix=f, jp=j, where=word, type="concept", rule=f"{word[:-1]} は数えられない名詞なので、複数形にしない",
                    tempt="「たくさんある」「ふだん～する」という意味から、名詞を複数形にしたほうがよいと考えた。", label="数えられない名詞を複数形にする誤り")
    if kind == "subj_case":
        nm, p, jn = r.choice([("Aya", "she", "アヤ"), ("Ken", "he", "ケン"), ("Tom", "he", "トム"), ("Lucy", "she", "ルーシー")])
        wrongf = PRON[p][2] if r.random() < 0.6 else PRON[p][1]
        tail, tj = r.choice([("lives in Kobe", "神戸に住んでいます"), ("plays the guitar", "ギターをひきます"), ("is from Canada", "カナダ出身です"), ("likes animals", "動物が好きです")])
        return dict(wrong=f"This is my friend {nm}. {cap(wrongf)} {tail}.", fix=f"This is my friend {nm}. {cap(p)} {tail}.",
                    jp=f"こちらは友だちの{jn}です。{'彼女' if p == 'she' else '彼'}は{tj}。", where=cap(wrongf), type="concept",
                    rule=f"動詞の前の主語の位置には主格を使うので {cap(p)}",
                    tempt="日本語の「彼女は」「彼は」にあたる形を、目的格や所有格と区別せずに覚えていた。", label="主語に主格以外を使う誤り")
    if kind == "obj_case":
        p = r.choice(["he", "she", "they", "we", "I"])
        fr, fj = r.choice([("Ken often plays with {X}.", "ケンはよく{J}と遊びます。"), ("Do you know {X}?", "あなたは{J}を知っていますか。"),
                           ("Ms. Green helps {X} every day.", "グリーン先生は毎日{J}を手伝います。"), ("Please look at {X}.", "{J}を見てください。")])
        if p == "I" and "look" in fr:
            p = "he"
        wrong = fr.replace("{X}", PRON[p][0])
        fix = fr.replace("{X}", PRON[p][2])
        return dict(wrong=wrong, fix=fix, jp=fj.replace("{J}", PRON[p][4]), where=PRON[p][0], type="concept",
                    rule=f"動詞や前置詞の後ろには目的格を使うので {PRON[p][2]}",
                    tempt="代名詞はいつも主格（he, she など）の形で使えると思い込み、位置による形の変化を確かめなかった。", label="動詞・前置詞の後ろに主格を使う誤り")
    if kind == "poss_case":
        p = r.choice(["I", "he", "she", "we", "they"])
        bad = PRON[p][2] if r.random() < 0.5 else PRON[p][0]
        n, nj = r.choice([("bike", "自転車"), ("bag", "かばん"), ("house", "家"), ("dog", "犬"), ("room", "部屋")])
        return dict(wrong=f"This is {bad} {n}.", fix=f"This is {PRON[p][1]} {n}.", jp=f"これは{PRON[p][4]}の{nj}です。",
                    where=bad, type="concept", rule=f"後ろに名詞 {n} が続く「～の」の位置には所有格を使うので {PRON[p][1]}",
                    tempt="「～の」を表す形（所有格）と、主格・目的格の区別があいまいだった。", label="名詞の前に所有格以外を使う誤り")
    if kind == "mine_noun":
        p = r.choice(["I", "you", "she", "we", "they"])
        n, nj = r.choice([("bike", "自転車"), ("bag", "かばん"), ("umbrella", "かさ"), ("notebook", "ノート")])
        if r.random() < 0.5:
            return dict(wrong=f"This is {PRON[p][3]} {n}.", fix=f"This is {PRON[p][1]} {n}.", jp=f"これは{PRON[p][4]}の{nj}です。",
                        where=PRON[p][3], type="concept", rule=f"後ろに名詞が続くときは所有格 {PRON[p][1]}。所有代名詞 {PRON[p][3]} は1語で「～のもの」を表し、後ろに名詞を置かない",
                        tempt="mine・yours も「～の」と訳すことがあるので、所有格と同じように名詞の前に置いた。", label="所有代名詞の後ろに名詞を置く誤り")
        return dict(wrong=f"This {n} is {PRON[p][1]}.", fix=f"This {n} is {PRON[p][3]}.", jp=f"この{nj}は{PRON[p][4]}のものです。",
                    where=PRON[p][1], type="concept", rule=f"「～のもの」は所有代名詞 {PRON[p][3]}。所有格 {PRON[p][1]} は後ろに名詞が必要",
                    tempt="「～の」と「～のもの」の区別をせず、所有格で文を終えた。", label="「～のもの」に所有格を使う誤り")
    # apostrophe
    p = r.choice(["she", "you", "we", "they"])
    n, nj = r.choice([("pen", "ペン"), ("cap", "帽子"), ("racket", "ラケット"), ("watch", "腕時計")])
    bad = PRON[p][1] + "'s"
    return dict(wrong=f"That {n} is {bad}.", fix=f"That {n} is {PRON[p][3]}.", jp=f"あの{nj}は{PRON[p][4]}のものです。",
                where=bad, type="notation", rule=f"所有代名詞は {PRON[p][3]} で、アポストロフィ（'）はつけない",
                tempt="Ken's（ケンのもの）と同じように、所有を表す 's をつければよいと考えた。", label="所有代名詞にアポストロフィをつける誤り")


NOUN_ERRS = ["spell", "no_pl", "a_pl", "these_sg", "uncount"]
PRON_ERRS = ["subj_case", "obj_case", "poss_case", "mine_noun", "apos"]


@gen("standard_practice", 4, ["common_error", "concept"])
def correct_sentence(r):
    kinds = r.sample(NOUN_ERRS, 2) + r.sample(PRON_ERRS, 2)
    r.shuffle(kinds)
    okk = kinds[0]
    ok = make_error(okk, r)["fix"]
    errs = [(k, make_error(k, r)) for k in kinds[1:]]
    texts = [e["wrong"] for _, e in errs]
    if len(set(texts + [ok])) < 4:
        errs = [(k, make_error(k, local(ok + k))) for k in kinds[1:]]
        texts = [e["wrong"] for _, e in errs]
    why = {e["wrong"]: (f"{e['rule']}。正しくは {e['fix']}", e["label"]) for _, e in errs}
    return mc("次の英文のうち、文法的に正しいものを1つ選びなさい。", [ok] + texts,
              f"{ok} が正しい。ほかの3つは、" + "／".join(e["label"] for _, e in errs) + " をふくんでいる。", d=3,
              ap="名詞は「単数か複数か・つづり」、代名詞は「位置に合った格か」を、選択肢ごとに確かめる。",
              steps=["各選択肢の名詞に、数を表す語（a / two / these など）との組み合わせの誤りがないかを確かめる。",
                     "代名詞が主語・名詞の前・動詞や前置詞の後ろのどこにあるかを見て、格が合っているかを確かめる。", f"誤りのない {ok} を選ぶ。"],
              alt=["誤りだと思った選択肢を正しく直してみる。直す箇所がはっきり言えれば、その選択肢は誤りだと確信できる。"],
              pc=[("誤りの選択肢の誤りを見抜いている", 2), ("正しい文を選んでいる", 2)],
              pit=["文の意味が通じるかどうかだけで判断し、名詞や代名詞の形を確かめない。"], why=why)


# ======================================================================
# C 思考力・記述応用
# ======================================================================

CFR = [
    # (英文, 下線の語, 格, 日本語訳, 判断の根拠)
    ("I like [[u:{p}]] songs very much.", "所有格", "私は{J}の歌が大好きです。", "後ろに名詞 songs が続き、「{J}の」という意味になる"),
    ("Do you know [[u:{p}]] sister?", "所有格", "あなたは{J}のお姉さんを知っていますか。", "後ろに名詞 sister が続き、「{J}の」という意味になる"),
    ("I like [[u:{p}]] very much.", "目的格", "私は{J}が大好きです。", "動詞 like の後ろにあり、後ろに名詞が続かない（like の目的語）"),
    ("Ken often goes to the library with [[u:{p}]].", "目的格", "ケンはよく{J}といっしょに図書館に行きます。", "前置詞 with の後ろにあり、後ろに名詞が続かない"),
    ("This racket is [[u:{p}]].", "所有代名詞", "このラケットは{J}のものです。", "be 動詞 is の後ろで、後ろに名詞がなく、1語で「{J}のもの」（＝{poss} racket）を表す"),
    ("[[u:{p}]] room is very clean.", "所有格", "{J}の部屋はとてもきれいです。", "後ろに名詞 room が続き、「{J}の」という意味になる"),
    ("Ken sometimes uses [[u:{p}]] computer.", "所有格", "ケンはときどき{J}のコンピュータを使います。", "後ろに名詞 computer が続き、「{J}の」という意味になる"),
    ("Please give this letter to [[u:{p}]].", "目的格", "この手紙を{J}に渡してください。", "前置詞 to の後ろにあり、後ろに名詞が続かない"),
    ("We know [[u:{p}]] well.", "目的格", "私たちは{J}をよく知っています。", "動詞 know の後ろにあり、後ろに名詞が続かない（know の目的語）"),
    ("Is this cap [[u:{p}]]?", "所有代名詞", "この帽子は{J}のものですか。", "be 動詞 is と主語 this cap の後ろで、後ろに名詞がなく、1語で「{J}のもの」（＝{poss} cap）を表す"),
]


@gen("thinking_writing", 4, ["written_reasoning", "condition_check"])
def explain_case(r):
    fr, case, jt, reason = r.choice(CFR)
    # her（所有格・目的格が同形）、his（所有格・所有代名詞が同形）を中心に出題
    p = r.choice(["she", "he"]) if case != "所有代名詞" else "he"
    if case == "目的格":
        p = "she"
    word = PRON[p][CASES.index(case)]
    J = PRON[p][4]
    s = fr.replace("{p}", cap(word) if fr.startswith("[[u:") else word)
    rs = reason.replace("{J}", J).replace("{poss}", PRON[p][1])
    tr = jt.replace("{J}", J)
    same = {"she": "her は所有格と目的格が同じ形", "he": "his は所有格と所有代名詞が同じ形"}[p]
    model = f"{case}。{rs}から。{same}なので、つづりではなく位置で判断する。訳：{tr}"
    return desc(f"次の英文の下線部の語は、主格・所有格・目的格・所有代名詞のどれにあたるか答えなさい。また、そう判断した理由を、下線部の前後の語に注目して説明し、文全体を日本語に訳しなさい。\n{s}",
                model, f"{same}。同じつづりの語の働きは、前後の語（後ろに名詞があるか、動詞・前置詞の後ろか）で見分ける。",
                [("格を正しく答えている", 2), ("前後の語に注目した根拠を説明している", 4), ("和訳が正しい", 2)], d=4, p=8, lines=5,
                ap="下線部の直後に名詞があるか、直前に動詞・前置詞・be 動詞があるかを確かめる。",
                steps=["下線部の直前・直後の語を確認する。", f"位置から働きを判断する：{rs}。", f"格を決める：{case}。", f"和訳：{tr}"],
                alt=[f"下線部を別の代名詞（例：they の形 {PRON['they'][CASES.index(case)]}）に置きかえて読むと、どの格か確かめやすい（they は4つの形がすべて異なる）。"],
                pc=[("格", 2), ("根拠の説明", 4), ("和訳", 2)],
                pit=["「her＝彼女の」とだけ覚えていて、目的格の her を所有格と答える。", "his を見ると必ず所有格と答える。"])


PERSONS = [("friend", "friends", "友だち"), ("classmate", "classmates", "クラスメート"), ("cousin", "cousins", "いとこ")]
PVERBS = [("plays", "play", "tennis"), ("lives", "live", "in Kobe"), ("likes", "like", "music"), ("has", "have", "a big dog"),
          ("studies", "study", "science every day"), ("goes", "go", "to Minami Junior High School"), ("speaks", "speak", "English well")]


@gen("thinking_writing", 3, ["cross_unit", "written_reasoning"], rel=["JH-ENG-G1-U01"])
def plural_rewrite(r):
    sg, pl, m = r.choice(PERSONS)
    p = r.choice(["he", "she"])
    v3, v, rest = r.choice(PVERBS)
    near = r.random() < 0.6
    d1, d2 = ("This", "These") if near else ("That", "Those")
    src = f"{d1} is my {sg}. {cap(p)} {v3} {rest}."
    ans = f"{d2} are my {pl}. They {v} {rest}."
    model = (f"{ans}　変えた語：{d1} → {d2}（2人を指す）、is → are（主語が複数）、{sg} → {pl}（2人以上なので複数形）、"
             f"{cap(p)} → They（2人を受ける代名詞）、{v3} → {v}（主語 They は3人称単数ではないので、3単現の s をつけない）。")
    return desc(f"次の英文を、自分の{m}が2人いて、その2人を紹介する文に書きかえなさい（{d1} は {d2} にかえる）。また、ほかに形を変えた語をすべて挙げ、それぞれ変えた理由を説明しなさい。\n{src}",
                model, "名詞を複数にすると、指示語・be 動詞・代名詞・一般動詞の s まで連動して変わる。",
                [("正しい英文に書きかえている", 3), ("be 動詞・名詞の変化の理由を説明している", 2), ("代名詞と一般動詞の変化の理由を説明している", 3)], d=4, p=8, lines=6,
                ap="1人 → 2人になると、主語が複数になる。主語に合わせて形が変わる語（be 動詞・代名詞・3単現の s）を順に探す。",
                steps=[f"{d1} is → {d2} are、{sg} → {pl} にする。", f"{cap(p)} を2人を受ける They にする。", f"主語が They になったので {v3} → {v}。", f"答え：{ans}"],
                alt=["書きかえた文の They を he / she にもどしたとき、動詞に s が必要になることを確かめると、変化の理由を説明しやすい。"],
                pc=[("英文", 3), ("be 動詞・名詞の理由", 2), ("代名詞・一般動詞の理由", 3)],
                pit=[f"They {v3} のように、3単現の s を残す。", f"my {sg}s のつづり以外の変化（is → are など）を見落とす。"])


DIALOG_PEOPLE = [("Mr. Sato", "he", "佐藤先生", "neighbor"), ("Ms. Green", "she", "グリーン先生", "neighbor"), ("Ken", "he", "ケン", "cousin"),
                 ("Aya", "she", "アヤ", "cousin"), ("Tom and Emi", "they", "トムとエミ", "cousins"), ("Mr. and Mrs. Brown", "they", "ブラウン夫妻", "neighbors")]


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-ENG-G1-U01"])
def dialogue_fill(r):
    nm, p, jn, rel = r.choice(DIALOG_PEOPLE)
    sub, pos, obj = PRON[p][0], PRON[p][1], PRON[p][2]
    be = "are" if p == "they" else "is"
    v = "live" if p == "they" else "lives"
    typ = r.choice(["A", "B"])
    if typ == "A":
        s = f"A: Do you know {nm}?\nB: Yes. I know (　①　) well. (　②　) {be} my {rel}. I often go to (　③　) house."
        a = (obj, cap(sub), pos)
        why = (f"①は動詞 know の後ろなので目的格 {obj}", f"②は動詞 {be} の前の主語の位置なので主格 {cap(sub)}", f"③は後ろに名詞 house が続くので所有格 {pos}")
    else:
        s = f"A: Is this {nm}'s umbrella?\nB: Yes, it's (　①　). (　②　) {v} near my house. I see (　③　) every morning."
        a = (PRON[p][3], cap(sub), obj)
        why = (f"①は「{jn}のもの」の意味で後ろに名詞がないので所有代名詞 {PRON[p][3]}", f"②は動詞 {v} の前の主語の位置なので主格 {cap(sub)}",
               f"③は動詞 see の後ろなので目的格 {obj}")
    head = f"{nm} は{'2人' if p == 'they' else ('男性1人' if p == 'he' else '女性1人')}なので {p} の仲間を使う。"
    model = f"①{a[0]}　②{a[1]}　③{a[2]}。{head}" + "。".join(why) + "。"
    if p == "they":
        model += f"②の後ろの動詞が {be if typ == 'A' else v} になっているのも、主語が複数であることと合っている。"
    return desc(f"次の対話文の（①）〜（③）に、{nm} を指す代名詞を適切な形にして1語ずつ入れなさい。また、それぞれの形を選んだ理由を説明しなさい。\n{s}",
                model, f"{head}代名詞の形は位置で決まる。主語の位置→主格、名詞の前→所有格、動詞・前置詞の後ろ→目的格、「～のもの」→所有代名詞。",
                [("①が正しい", 2), ("②が正しい", 2), ("③が正しい", 2), ("位置に注目して理由を説明している", 2)], d=4, p=8, lines=6,
                ap=f"まず {nm} を受ける代名詞の仲間（he / she / they）を決め、次に空所ごとに位置を見て形を選ぶ。",
                steps=[head, why[0] + "。", why[1] + "。", why[2] + "。"],
                alt=[f"空所に {nm} をそのまま入れて読み（{nm}'s のように所有の形が必要な所はどこか）、その形に対応する代名詞を選ぶ。"],
                pc=[("①", 2), ("②", 2), ("③", 2), ("理由", 2)],
                pit=["空所の位置を見ずに、すべて同じ形（he など）を入れる。", "2人を指しているのに he / she を使う。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(e, ap, alt, pit, d=3):
    return desc(f"次の日本語を英語に直しなさい。\n{e['jp']}\n［ある生徒の解答］\n{e['wrong']}\n上の解答の誤りを指摘し、正しい英文に書き直しなさい。", e["fix"],
                f"「{e['where']}」の部分が誤り。{e['rule']}。正しくは {e['fix']}",
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい英文に直している", 3), ("規則を説明している", 1)], d=d, p=6, lines=5,
                ap=ap, steps=["誤りがありそうな名詞・代名詞を見つける。", "名詞なら数とつづり、代名詞なら位置と格を確かめる。",
                              f"「{e['where']}」を直す：{e['rule']}。", f"正しい英文：{e['fix']}"],
                alt=alt, pc=[("誤りの指摘", 2), ("正しい英文", 3), ("規則の説明", 1)], pit=pit,
                err=dict(sol=e["wrong"], step=f"「{e['where']}」の部分", type=e["type"], tempt=e["tempt"], fix=e["fix"]))


@gen("error_correction", 5, ["common_error", "computation"])
def err_noun(r):
    e = make_error(r.choice(NOUN_ERRS), r)
    return err_item(e, "名詞の前に a / an、数、these などがあるかを見て単数か複数かを決め、複数ならつづりの規則を確かめる。数えられない名詞は複数形にしない。",
                    ["直した英文の名詞を日本語に訳し、1つか2つ以上か（または数えられないものか）が日本語と合っているかを確かめる。"],
                    ["複数形のつづりの規則や不規則変化を確かめない。", "数えられない名詞に s をつける。"])


@gen("error_correction", 5, ["common_error", "condition_check"])
def err_pronoun(r):
    e = make_error(r.choice(PRON_ERRS), r)
    return err_item(e, "代名詞は位置で形が決まる。主語の位置→主格、名詞の前→所有格、動詞・前置詞の後ろ→目的格、「～のもの」→所有代名詞。",
                    ["人称代名詞の表（I-my-me-mine など）を書き出し、直した形が位置に合っているかを照合する。"],
                    ["日本語の「は・の・を」だけで形を決め、英文の中の位置を確かめない。", "所有代名詞にアポストロフィをつける。"])


GENERATORS = [plural_spell, pron_case, noun_form, pron_table, this_these,
              to_plural, to_pronoun, possessive_rewrite, build_order, correct_sentence,
              explain_case, plural_rewrite, dialogue_fill,
              err_noun, err_pronoun]
