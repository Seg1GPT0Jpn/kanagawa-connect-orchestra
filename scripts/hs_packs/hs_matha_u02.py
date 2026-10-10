"""単元パック：数学A 図形の性質。"""
from math import gcd

import sympy as sp

from banks._common import desc, figure, mc, num, sa, shape
from hs_pack_lib import (board, check, definition, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "HS-MATHA-U02"


# ---------------------------------------------------------------------------
# 補助
# ---------------------------------------------------------------------------

def ratio(p, q):
    """p:q を最も簡単な整数の比にした文字列。"""
    g = gcd(p, q)
    return f"{p // g}:{q // g}"


def _meet(p1, p2, p3, p4):
    """直線 p1p2 と直線 p3p4 の交点。"""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p1, p2, p3, p4
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def _on_circle(deg, r=2.0):
    import math
    t = math.radians(deg)
    return (r * math.cos(t), r * math.sin(t))


# チェバの定理の図
_A, _B, _C, _O = (1.2, 3.2), (0.0, 0.0), (4.6, 0.0), (1.8, 1.1)
_D, _E, _F = _meet(_A, _O, _B, _C), _meet(_B, _O, _C, _A), _meet(_C, _O, _A, _B)
CEVA_FIG = figure("三角形ABCと、1点Oで交わる3本の線分AD・BE・CF",
                  shape({"A": _A, "B": _B, "C": _C, "D": _D, "E": _E, "F": _F, "O": _O},
                        segments=[("A", "B"), ("B", "C"), ("C", "A"), ("A", "D"), ("B", "E"), ("C", "F")], scale=40))

# 方べきの定理（円の内部で交わる2弦）の図
_pa, _pb, _pc, _pd = _on_circle(160), _on_circle(-15), _on_circle(105), _on_circle(-80)
_pp = _meet(_pa, _pb, _pc, _pd)
POWER_FIG = figure("円の2つの弦ABとCDが円の内部の点Pで交わる図",
                   shape({"A": _pa, "B": _pb, "C": _pc, "D": _pd, "P": _pp},
                         segments=[("A", "B"), ("C", "D"), ("A", "C"), ("B", "D")], circle=((0, 0), 2), scale=34))

# メネラウスの定理の図（例題2の配置：AR:RB=1:2、Q は AC の中点、P は BC の延長上）
_mA, _mB, _mC = (1.0, 3.0), (0.0, 0.0), (3.0, 0.0)
_mR, _mQ = (2.0 / 3, 2.0), (2.0, 1.5)
_mP = _meet(_mR, _mQ, _mB, _mC)
MENE_FIG = figure("三角形ABCの辺AB上の点R・辺AC上の点Qを通る直線が、辺BCの延長と点Pで交わる図",
                  shape({"A": _mA, "B": _mB, "C": _mC, "P": _mP, "Q": _mQ, "R": _mR},
                        segments=[("A", "B"), ("B", "C"), ("C", "A"), ("C", "P"), ("R", "P")], scale=36))


LESSON = lesson(
    goals=["三角形の五心（重心・内心・外心・垂心・傍心）の定義と基本性質を説明し、長さや角の計算に使える。",
           "角の二等分線と比の定理、チェバの定理、メネラウスの定理を証明の筋道とともに理解し、線分比を求められる。",
           "円に内接する四角形・接弦定理・方べきの定理を、相似な三角形と結びつけて使いこなせる。"],
    duration=100,
    readiness=["平行線と線分の比、三角形の相似条件（中学3年）を使える。", "円周角の定理とその逆（中学3年）を説明できる。",
               "三角形の面積比を「底辺の比」「高さの比」で考えられる。"],
    flow=[("導入：中学の図形からの接続", 8, "三角形の内角の二等分線を3本かくと1点で交わることを作図で確かめ、「なぜ1点で交わるのか」を問う"),
          ("三角形の五心", 17, "五心の定義と性質を表にまとめ、重心が中線を 2:1 に内分すること・角の二等分線と比の定理を証明する"),
          ("チェバ・メネラウスの定理", 30, "面積比によるチェバの定理の証明、平行線によるメネラウスの定理の証明。例題1・例題2"),
          ("円の性質", 15, "円に内接する四角形の性質と接弦定理を、円周角の定理から導く"),
          ("方べきの定理", 20, "相似による証明（交わる2弦・接線と割線）。例題3で長さを求める"),
          ("まとめと確認", 10, "確認問題3問、問題プリントAの課題指示")],
    sections=[
        intro("in1", "三角形の「中心」はひとつではない",
              "三角形の3本の中線は1点で交わり、3本の内角の二等分線も1点で交わる。3本の直線がいつも1点で交わることは当たり前ではなく、それぞれに理由がある。この単元では、三角形の重要な点（五心）と、線分の比を一気に求めるチェバの定理・メネラウスの定理、そして円と直線がつくる図形の性質を、中学で学んだ相似と円周角の定理をもとに証明しながら学ぶ。",
              bullets=["重心・内心・外心・垂心・傍心をまとめて三角形の五心という。", "線分の比の問題は「どの三角形に、どの直線を当てはめるか」を決めることが鍵になる。",
                       "円の問題では、等しい円周角を見つけて相似な三角形をつくるのが基本方針である。"],
              points=[tp("3本の線が1点で交わることを、作図ソフトや紙の作図で実際に確かめさせてから理由を問う。", ask="2本の角の二等分線の交点を I とする。I は3辺からどんな距離にあるか。",
                         expect="2辺ずつから等距離なので、3辺すべてから等距離になる。", timing="導入の冒頭")]),
        definition("df1", "三角形の五心",
                   "三角形 $\\mathrm{ABC}$ について、次の5つの点を三角形の五心という。",
                   bullets=["重心 G：3本の中線の交点。各中線を頂点から $2:1$ に内分する。",
                            "内心 I：3つの内角の二等分線の交点。3辺から等距離にあり、内接円の中心である。",
                            "外心 O：3辺の垂直二等分線の交点。3頂点から等距離にあり、外接円の中心である。",
                            "垂心 H：各頂点から対辺またはその延長に下ろした3本の垂線の交点。",
                            "傍心：1つの内角の二等分線と、他の2つの頂点における外角の二等分線の交点。傍接円の中心で、1つの三角形に3個ある。"],
                   conditions=["外心は、鋭角三角形では内部、直角三角形では斜辺の中点、鈍角三角形では外部にある。", "正三角形では重心・内心・外心・垂心が一致する。"],
                   points=[tp("「何の交点か（定義）」と「何から等距離か（性質）」を区別して表に整理させる。", caution="内心と外心の「等距離」の対象（辺か頂点か）を取り違えやすい。")]),
        theorem("th1", "角の二等分線と線分の比",
                "$$\\triangle\\mathrm{ABC}\\ \\text{で}\\ \\angle\\mathrm{A}\\ \\text{の二等分線と辺 BC の交点を D とすると}\\quad \\mathrm{BD}:\\mathrm{DC}=\\mathrm{AB}:\\mathrm{AC}$$",
                ["D は辺 BC を $\\mathrm{AB}:\\mathrm{AC}$ に内分する。", "外角の二等分線と直線 BC の交点は、辺 BC を $\\mathrm{AB}:\\mathrm{AC}$ に外分する（$\\mathrm{AB}\\neq\\mathrm{AC}$ のとき）。"],
                proof=["C を通り AD に平行な直線と、辺 BA の A を越える延長との交点を E とする。",
                       "$\\mathrm{AD}\\parallel\\mathrm{EC}$ より、$\\angle\\mathrm{ACE}=\\angle\\mathrm{CAD}$（錯角）、$\\angle\\mathrm{AEC}=\\angle\\mathrm{BAD}$（同位角）。",
                       "$\\angle\\mathrm{BAD}=\\angle\\mathrm{CAD}$ なので $\\angle\\mathrm{ACE}=\\angle\\mathrm{AEC}$。よって $\\triangle\\mathrm{ACE}$ は二等辺三角形で $\\mathrm{AE}=\\mathrm{AC}$。",
                       "$\\triangle\\mathrm{BEC}$ で $\\mathrm{AD}\\parallel\\mathrm{EC}$ より $\\mathrm{BD}:\\mathrm{DC}=\\mathrm{BA}:\\mathrm{AE}=\\mathrm{AB}:\\mathrm{AC}$。"],
                points=[tp("補助線「平行線を引いて二等辺三角形をつくる」という発想を、なぜその線を引くのかとともに説明する。", ask="比 $\\mathrm{AB}:\\mathrm{AC}$ を1本の直線上に並べるにはどうすればよいか。")]),
        theorem("th2", "チェバの定理",
                "$$\\dfrac{\\mathrm{AF}}{\\mathrm{FB}}\\cdot\\dfrac{\\mathrm{BD}}{\\mathrm{DC}}\\cdot\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=1$$",
                ["$\\triangle\\mathrm{ABC}$ の3頂点と、三角形の辺上にない点 O を結ぶ直線が、対辺 BC・CA・AB（またはその延長）とそれぞれ D・E・F で交わるとき成り立つ。",
                 "A → F → B → D → C → E → A と、頂点と分点を交互にたどって一周する順に比をかける。"],
                body="O が三角形の内部にある場合を、面積比を使って証明する。",
                proof=["$\\triangle\\mathrm{ABO}$ と $\\triangle\\mathrm{ACO}$ は辺 AO を共有する。B・C から直線 AO までの距離の比は $\\mathrm{BD}:\\mathrm{DC}$ に等しいので、$\\dfrac{\\mathrm{BD}}{\\mathrm{DC}}=\\dfrac{\\triangle\\mathrm{ABO}}{\\triangle\\mathrm{ACO}}$。",
                       "同様に $\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=\\dfrac{\\triangle\\mathrm{BCO}}{\\triangle\\mathrm{BAO}}$、$\\dfrac{\\mathrm{AF}}{\\mathrm{FB}}=\\dfrac{\\triangle\\mathrm{CAO}}{\\triangle\\mathrm{CBO}}$。",
                       "3つの式をかけ合わせると、分子と分母の面積がすべて約分されて $1$ になる。"],
                figure=CEVA_FIG,
                points=[tp("面積比で考えると「高さの比＝底辺上の線分の比」になることを、図に高さをかき入れて確認させる。", caution="比をかける順序を崩すと等式が成り立たない。「頂点→分点→頂点」と一筆書きでたどる。")]),
        theorem("th3", "メネラウスの定理",
                "$$\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}\\cdot\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=1$$",
                ["三角形の頂点を通らない直線 $\\ell$ が、直線 BC・CA・AB とそれぞれ P・Q・R で交わるときに成り立つ。",
                 "線分の長さの比として使う（外分点 P についても $\\mathrm{BP}$、$\\mathrm{PC}$ は長さ）。"],
                proof=["C を通り直線 $\\ell$ に平行な直線を引き、直線 AB との交点を D とする。",
                       "$\\mathrm{PR}\\parallel\\mathrm{CD}$ より $\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}=\\dfrac{\\mathrm{BR}}{\\mathrm{RD}}$、$\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}=\\dfrac{\\mathrm{DR}}{\\mathrm{RA}}$。",
                       "よって $\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}\\cdot\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=\\dfrac{\\mathrm{BR}}{\\mathrm{RD}}\\cdot\\dfrac{\\mathrm{DR}}{\\mathrm{RA}}\\cdot\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=1$。"],
                figure=MENE_FIG,
                points=[tp("チェバとの違いは「1点で交わる3直線」か「1本の直線」か。図を見てどちらを使うかを判断させる。", ask="この図には三角形と直線の組がいくつ見えるか。")]),
        example("ex1", "例題1　チェバの定理",
                "$\\triangle\\mathrm{ABC}$ の内部の点 O について、直線 AO・BO・CO と辺 BC・CA・AB の交点をそれぞれ D・E・F とする。$\\mathrm{AF}:\\mathrm{FB}=2:3$、$\\mathrm{BD}:\\mathrm{DC}=4:1$ のとき、$\\mathrm{CE}:\\mathrm{EA}$ を求めよ。",
                ["チェバの定理より $\\dfrac{2}{3}\\cdot\\dfrac{4}{1}\\cdot\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=1$。", "$\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=\\dfrac{3}{8}$。"],
                "$\\mathrm{CE}:\\mathrm{EA}=3:8$",
                thinking="3本の線分が1点 O で交わっているので、チェバの定理を使う。A から出発して F → B → D → C → E → A の順にたどる。",
                points=[tp("求めた比が図の見た目（E は A 寄りか C 寄りか）と合っているかを確かめさせる。")],
                misconceptions=[("$\\dfrac{2}{3}\\cdot\\dfrac{4}{1}=\\dfrac{8}{3}$ をそのまま $\\mathrm{CE}:\\mathrm{EA}=8:3$ とする", "積が $1$ になるように残りの比を決めるので $\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=\\dfrac{3}{8}$")]),
        example("ex2", "例題2　メネラウスの定理",
                "$\\triangle\\mathrm{ABC}$ の辺 AB を $1:2$ に内分する点を R、辺 AC の中点を Q とし、直線 RQ と直線 BC の交点を P とする。$\\mathrm{BP}:\\mathrm{PC}$ を求めよ。",
                ["直線 PQR と $\\triangle\\mathrm{ABC}$ にメネラウスの定理を用いる：$\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}\\cdot\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=1$。",
                 "$\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}=1$、$\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=\\dfrac{1}{2}$ より $\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}=2$。"],
                "$\\mathrm{BP}:\\mathrm{PC}=2:1$（P は辺 BC の C を越える延長上にあり、C は線分 BP の中点）",
                thinking="三角形 ABC と、それを横切る1本の直線 PQR の組なので、メネラウスの定理を使う。",
                figure=MENE_FIG,
                points=[tp("外分点 P の位置を図で確認し、$\\mathrm{BP}>\\mathrm{PC}$ なので P が C の外側にあることを読み取らせる。")]),
        theorem("th4", "円に内接する四角形と接弦定理",
                "$$\\text{円に内接する四角形 ABCD}\\ \\Longrightarrow\\ \\angle\\mathrm{A}+\\angle\\mathrm{C}=180^\\circ,\\quad \\angle\\mathrm{B}+\\angle\\mathrm{D}=180^\\circ$$",
                ["円に内接する四角形の外角は、それと隣り合う内角の対角に等しい。", "逆に、対角の和が $180^\\circ$ である四角形は円に内接する。",
                 "接弦定理：円の接線と、接点を通る弦のつくる角は、その角の内部にある弧に対する円周角に等しい。"],
                proof=["円の中心を O とすると、弧 BCD に対する中心角と弧 BAD に対する中心角の和は $360^\\circ$。",
                       "円周角は中心角の半分なので、$\\angle\\mathrm{A}+\\angle\\mathrm{C}=\\dfrac{1}{2}\\times360^\\circ=180^\\circ$。",
                       "外角は $180^\\circ-\\angle\\mathrm{C}$ なので $\\angle\\mathrm{A}$ に等しい。"],
                points=[tp("「対角」とは向かい合う角であり、隣り合う角ではないことを図で確認する。", caution="$\\angle\\mathrm{A}+\\angle\\mathrm{B}=180^\\circ$ とする誤りが多い。")]),
        theorem("th5", "方べきの定理",
                "$$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD},\\qquad \\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PT}^2$$",
                ["点 P を通る2直線が円とそれぞれ A, B と C, D で交わるとき（P は円の内部でも外部でもよい）、第1式が成り立つ。",
                 "P が円の外部にあり、P から引いた接線の接点を T とするとき、第2式が成り立つ。",
                 "PA、PB などは、いずれも点 P からの距離である（$\\mathrm{AB}$ ではない）。"],
                proof=["（円の内部で交わる場合）$\\triangle\\mathrm{PAC}$ と $\\triangle\\mathrm{PDB}$ で、$\\angle\\mathrm{APC}=\\angle\\mathrm{DPB}$（対頂角）。",
                       "弧 BC に対する円周角より $\\angle\\mathrm{PAC}=\\angle\\mathrm{PDB}$。よって2組の角がそれぞれ等しく $\\triangle\\mathrm{PAC}\\sim\\triangle\\mathrm{PDB}$。",
                       "対応する辺の比より $\\mathrm{PA}:\\mathrm{PD}=\\mathrm{PC}:\\mathrm{PB}$、すなわち $\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD}$。",
                       "（接線の場合）$\\triangle\\mathrm{PTA}$ と $\\triangle\\mathrm{PBT}$ で $\\angle\\mathrm{P}$ は共通、接弦定理より $\\angle\\mathrm{PTA}=\\angle\\mathrm{PBT}$。よって相似で $\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}$。"],
                figure=POWER_FIG,
                points=[tp("「方べき」は相似の比を積の形に書き直したものだと理解させ、公式を忘れても相似から復元できるようにする。", ask="どの2つの三角形が相似か。等しい角はどれか。")]),
        example("ex3", "例題3　接線と割線",
                "円の外部の点 P から円に接線を引き、接点を T とする。また、P を通る直線が円と2点 A, B で交わり、$\\mathrm{PA}=4$、$\\mathrm{AB}=5$ である。PT の長さを求めよ。",
                ["$\\mathrm{PB}=\\mathrm{PA}+\\mathrm{AB}=9$。", "方べきの定理より $\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}=4\\times9=36$。", "$\\mathrm{PT}>0$ より $\\mathrm{PT}=6$。"],
                "$\\mathrm{PT}=6$",
                thinking="接線と割線があるので $\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}$。PB は P からの距離なので $\\mathrm{PA}+\\mathrm{AB}$。",
                points=[tp("$\\mathrm{PA}\\cdot\\mathrm{AB}$ と計算してしまう誤りを、方べきの意味（P からの距離の積）にもどって正させる。", caution="$\\mathrm{PT}^2=4\\times5$ とする誤りが典型的。")],
                misconceptions=[("$\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{AB}=20$", "$\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}=4\\times9=36$")]),
        board("bd1", "板書案",
              [("① 五心と角の二等分線", ["重心：中線を $2:1$", "内心：3辺から等距離", "外心：3頂点から等距離", "$\\mathrm{BD}:\\mathrm{DC}=\\mathrm{AB}:\\mathrm{AC}$", "（平行線で二等辺三角形）"]),
               ("② チェバ・メネラウス", ["1点で交わる3線 → チェバ", "1本の直線 → メネラウス", "頂点→分点→頂点…と一周", "例1 $\\mathrm{CE}:\\mathrm{EA}=3:8$", "例2 $\\mathrm{BP}:\\mathrm{PC}=2:1$"]),
               ("③ 円の性質と方べき", ["内接四角形：対角の和 $180^\\circ$", "接弦定理", "$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD}$", "$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PT}^2$", "例3 $\\mathrm{PT}=6$"])],
              points=[tp("板書は3列に分け、②③では図を大きくかき、比や長さを図の中に書きこんでから式を立てる。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("チェバ・メネラウスでは、式を書く前に図の上で「出発点の頂点に指を置き、一周する」動作をさせる。", ask="次にたどる点はどれか。"),
               tp("比を求めたら、図の見た目と矛盾しないか（どちら寄りの点か）を必ず確認させる。", timing="例題1・例題2の後"),
               tp("外心の位置は三角形の形（鋭角・直角・鈍角）で変わることを、作図で見せる。", caution="外心はいつも内部にあると思いこんでいる生徒が多い。"),
               tp("方べきの定理は「P からの距離」の積であることを毎回言葉にさせる。", caution="$\\mathrm{PA}\\cdot\\mathrm{AB}$ と弦の長さを使う誤り。"),
               tp("重心の比 $2:1$ は「頂点側が 2」であることを、中線の長さの $\\dfrac{2}{3}$ という形でも確認させる。")],
              misconceptions=[("角の二等分線で $\\mathrm{BD}:\\mathrm{DC}=\\mathrm{AC}:\\mathrm{AB}$ とする", "B 側の線分 BD には B 側の辺 AB が対応する：$\\mathrm{BD}:\\mathrm{DC}=\\mathrm{AB}:\\mathrm{AC}$"),
                              ("円に内接する四角形で隣り合う角の和を $180^\\circ$ とする", "和が $180^\\circ$ になるのは向かい合う角（対角）"),
                              ("重心 G について $\\mathrm{AG}=\\dfrac{1}{3}\\mathrm{AM}$ とする", "頂点側が 2 なので $\\mathrm{AG}=\\dfrac{2}{3}\\mathrm{AM}$")]),
        summary("sm1", "まとめ",
                ["五心は「何の交点か」と「何から等距離か」を区別して覚える。重心は中線を頂点から $2:1$ に内分する。",
                 "角の二等分線は対辺を隣の2辺の比に分ける。1点で交わる3線はチェバ、1本の直線はメネラウス。",
                 "円の問題は等しい円周角から相似を見つける。方べきの定理は P からの距離の積が一定。"]),
        check("ck1", "確認問題",
              [("$\\triangle\\mathrm{ABC}$ の重心を G、辺 BC の中点を M とする。$\\mathrm{AM}=12$ のとき GM を求めよ。", "$\\mathrm{GM}=\\dfrac{1}{3}\\mathrm{AM}=4$"),
               ("$\\mathrm{AB}=8$、$\\mathrm{AC}=6$、$\\mathrm{BC}=7$ の $\\triangle\\mathrm{ABC}$ で、$\\angle\\mathrm{A}$ の二等分線と BC の交点を D とする。BD を求めよ。", "$\\mathrm{BD}:\\mathrm{DC}=4:3$ より $\\mathrm{BD}=4$"),
               ("円の外部の点 P から引いた直線が円と A, B で交わり $\\mathrm{PA}=2,\\ \\mathrm{PB}=8$。P から引いた接線の長さを求めよ。", "$\\mathrm{PT}^2=16$ より $\\mathrm{PT}=4$")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

@gen("basic_check", 4, ["computation", "concept"])
def centroid_ratio(r):
    form = r.choice(["AG", "GM", "AM"])
    if form == "AM":
        g = r.choice(range(2, 31, 2))
        m = g * 3 // 2
        return num(f"$\\triangle\\mathrm{{ABC}}$ の重心を G、辺 BC の中点を M とする。$\\mathrm{{AG}}={g}$ のとき、中線 AM の長さを求めなさい。", str(m),
                   f"G は中線 AM を $2:1$ に内分するので $\\mathrm{{AM}}=\\dfrac{{3}}{{2}}\\mathrm{{AG}}={m}$。", d=1,
                   ap="重心は中線を頂点の側から $2:1$ に内分する。AG は中線全体の $\\dfrac{2}{3}$ にあたる。",
                   steps=["$\\mathrm{AG}:\\mathrm{GM}=2:1$ より $\\mathrm{AG}=\\dfrac{2}{3}\\mathrm{AM}$。", f"$\\mathrm{{AM}}=\\dfrac{{3}}{{2}}\\times{g}={m}$。"],
                   alt=[f"$\\mathrm{{GM}}=\\dfrac{{1}}{{2}}\\mathrm{{AG}}={g // 2}$ を求め、$\\mathrm{{AM}}=\\mathrm{{AG}}+\\mathrm{{GM}}={g}+{g // 2}={m}$ としてもよい。"],
                   pc=[("重心が中線を $2:1$ に内分することを使っている", 1), ("正しい長さを求めている", 1)],
                   pit=["$\\mathrm{AM}=3\\,\\mathrm{AG}$ としてしまう（$1:2$ と逆に覚えている）。"],
                   chk=(f"Rational(3,2)*{g}", str(m)))
    m = r.choice(range(6, 46, 3))
    ans = 2 * m // 3 if form == "AG" else m // 3
    seg = "AG" if form == "AG" else "GM"
    return num(f"$\\triangle\\mathrm{{ABC}}$ の重心を G、辺 BC の中点を M とする。中線 AM の長さが ${m}$ のとき、線分 {seg} の長さを求めなさい。", str(ans),
               f"$\\mathrm{{AG}}:\\mathrm{{GM}}=2:1$ より $\\mathrm{{{seg}}}=\\dfrac{{{2 if form == 'AG' else 1}}}{{3}}\\times{m}={ans}$。", d=1,
               ap="重心は3本の中線の交点で、各中線を頂点の側から $2:1$ に内分する。",
               steps=["$\\mathrm{AG}:\\mathrm{GM}=2:1$。", f"{seg} は中線全体の $\\dfrac{{{2 if form == 'AG' else 1}}}{{3}}$ なので ${ans}$。"],
               alt=[f"$\\mathrm{{AG}}={2 * m // 3}$、$\\mathrm{{GM}}={m // 3}$ を両方求め、和が ${m}$ になることで確かめる。"],
               pc=[("$2:1$ の比を正しく使っている", 1), ("正しい長さを求めている", 1)],
               pit=["頂点側と中点側の比を逆にする（$\\mathrm{AG}:\\mathrm{GM}=1:2$ とする）。"],
               chk=(f"Rational({2 if form == 'AG' else 1},3)*{m}", str(ans)))


@gen("basic_check", 4, ["computation"])
def bisector_ratio(r):
    while True:
        c, b = r.sample(range(3, 13), 2)
        a = r.randint(abs(b - c) + 1, b + c - 1)
        if (a * c) % (b + c) == 0:
            break
    ask = r.choice(["BD", "DC"])
    bd, dc = a * c // (b + c), a * b // (b + c)
    ans = bd if ask == "BD" else dc
    return num(f"$\\mathrm{{AB}}={c}$、$\\mathrm{{BC}}={a}$、$\\mathrm{{CA}}={b}$ の $\\triangle\\mathrm{{ABC}}$ において、$\\angle\\mathrm{{A}}$ の二等分線が辺 BC と交わる点を D とする。線分 {ask} の長さを求めなさい。",
               str(ans), f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AB}}:\\mathrm{{AC}}={c}:{b}$ より $\\mathrm{{{ask}}}={a}\\times\\dfrac{{{c if ask == 'BD' else b}}}{{{b + c}}}={ans}$。", d=2,
               ap="内角の二等分線は、対辺を「隣り合う2辺の比」に内分する。B 側の線分には B 側の辺 AB が対応する。",
               steps=[f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AB}}:\\mathrm{{AC}}={c}:{b}$。", f"$\\mathrm{{{ask}}}={a}\\times\\dfrac{{{c if ask == 'BD' else b}}}{{{c}+{b}}}={ans}$。"],
               alt=[f"$\\mathrm{{BD}}={bd}$、$\\mathrm{{DC}}={dc}$ の和が $\\mathrm{{BC}}={a}$ になり、比が ${ratio(c, b)}$ であることを確かめる。"],
               pc=[("比 $\\mathrm{BD}:\\mathrm{DC}=\\mathrm{AB}:\\mathrm{AC}$ を正しく立てている", 1), ("長さを正しく求めている", 1)],
               pit=["$\\mathrm{BD}:\\mathrm{DC}=\\mathrm{AC}:\\mathrm{AB}$ と対応を逆にする。"],
               chk=(f"Rational({a}*{c if ask == 'BD' else b},{b + c})", str(ans)))


CENTERS = {
    "重心": ("3本の中線", "各中線を頂点の側から $2:1$ に内分する"),
    "内心": ("3つの内角の二等分線", "3辺から等しい距離にある"),
    "外心": ("3辺の垂直二等分線", "3つの頂点から等しい距離にある"),
    "垂心": ("各頂点から対辺またはその延長に下ろした3本の垂線", None),
    "傍心": ("1つの内角の二等分線と、他の2つの頂点における外角の二等分線", None),
}


@gen("basic_check", 3, ["concept"])
def center_name(r):
    form = r.choice(["def", "def", "prop"])
    pool = list(CENTERS) if form == "def" else [k for k, v in CENTERS.items() if v[1]]
    ans = r.choice(pool)
    others = r.sample([k for k in CENTERS if k != ans], 3)
    if form == "def":
        stem = f"$\\triangle\\mathrm{{ABC}}$ において、{CENTERS[ans][0]}は1点で交わる。この交点の名称として正しいものを選びなさい。"
    else:
        stem = f"$\\triangle\\mathrm{{ABC}}$ の五心のうち、「{CENTERS[ans][1]}」という性質をもつ点を選びなさい。"
    why = {o: (f"{o}は{CENTERS[o][0]}の交点である。" + (f"{o}は「{CENTERS[o][1]}」点である。" if CENTERS[o][1] else ""), "五心の定義の取り違え") for o in others}
    return mc(stem, [ans] + others, f"{ans}は{CENTERS[ans][0]}の交点である。" + (f"{ans}は{CENTERS[ans][1]}。" if CENTERS[ans][1] else ""), d=1,
              ap="五心は「何の交点か（定義）」と「何から等距離か（性質）」をセットで覚える。",
              steps=[f"問われているのは「{CENTERS[ans][0] if form == 'def' else CENTERS[ans][1]}」。", f"これは{ans}の{'定義' if form == 'def' else '性質'}である。"],
              alt=["内心は内接円の中心（辺に接する円）、外心は外接円の中心（頂点を通る円）と、円と結びつけて区別するとよい。"],
              pc=[("正しい名称を選んでいる", 2)], why=why)


@gen("basic_check", 4, ["computation", "condition_check"])
def cyclic_quad_angle(r):
    x = r.choice(range(52, 132, 2))
    form = r.choice(["opp", "ext", "oppB"])
    if form == "opp":
        stem = f"四角形 ABCD は円に内接し、$\\angle\\mathrm{{BAD}}={x}^\\circ$ である。$\\angle\\mathrm{{BCD}}$ の大きさを求めなさい。"
        ans, why = 180 - x, "対角の和は $180^\\circ$"
    elif form == "oppB":
        stem = f"円に内接する四角形 ABCD において、$\\angle\\mathrm{{ABC}}={x}^\\circ$ のとき、$\\angle\\mathrm{{ADC}}$ の大きさを求めなさい。"
        ans, why = 180 - x, "対角の和は $180^\\circ$"
    else:
        stem = f"四角形 ABCD は円に内接し、$\\angle\\mathrm{{BAD}}={x}^\\circ$ である。辺 BC の C を越える延長上に点 E をとるとき、$\\angle\\mathrm{{DCE}}$ の大きさを求めなさい。"
        ans, why = x, "外角はその内対角に等しい"
    return num(stem, str(ans), f"円に内接する四角形では{why}ので ${ans}^\\circ$。", d=1, disp=f"${ans}^\\circ$",
               ap="円に内接する四角形では、向かい合う角（対角）の和が $180^\\circ$。外角は隣の内角の対角に等しい。",
               steps=[f"求める角と ${x}^\\circ$ の角の位置関係を確認する（{'向かい合う角' if form != 'ext' else '外角と内対角'}）。", f"{why}より ${ans}^\\circ$。"],
               alt=["対角の和 $180^\\circ$ は、2つの円周角に対する中心角の和が $360^\\circ$ であることから確かめられる。"],
               pc=[("内接四角形の性質を正しく選んでいる", 1), ("角度を正しく求めている", 1)],
               pit=["隣り合う角の和を $180^\\circ$ と考える。", "外角を $180^\\circ$ から引いてしまう。"],
               chk=(f"180-{x}" if form != "ext" else f"{x}", str(ans)))


@gen("basic_check", 5, ["computation"])
def power_chords(r):
    form = r.choice(["in", "out"])
    while True:
        pa, pb, pc = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
        if form == "out" and pa >= pb:
            continue
        if (pa * pb) % pc == 0 and pa * pb // pc != pc and pc not in (pa, pb) and (form == "in" or pa * pb // pc > pc):
            break
    pd = pa * pb // pc
    if form == "in":
        stem = f"円の弦 AB と弦 CD が円の内部の点 P で交わっている。$\\mathrm{{PA}}={pa}$、$\\mathrm{{PB}}={pb}$、$\\mathrm{{PC}}={pc}$ のとき、線分 PD の長さを求めなさい。"
    else:
        stem = f"円の外部の点 P を通る2本の直線が、円とそれぞれ2点 A, B および2点 C, D で交わる（$\\mathrm{{PA}}<\\mathrm{{PB}}$、$\\mathrm{{PC}}<\\mathrm{{PD}}$）。$\\mathrm{{PA}}={pa}$、$\\mathrm{{PB}}={pb}$、$\\mathrm{{PC}}={pc}$ のとき、PD の長さを求めなさい。"
    return num(stem, str(pd), f"方べきの定理より $\\mathrm{{PA}}\\cdot\\mathrm{{PB}}=\\mathrm{{PC}}\\cdot\\mathrm{{PD}}$、${pa}\\times{pb}={pc}\\,\\mathrm{{PD}}$ より $\\mathrm{{PD}}={pd}$。", d=2,
               ap="点 P を通る2直線が円と交わるとき、P から交点までの距離の積は一定（方べきの定理）。P が円の内部でも外部でも同じ式。",
               steps=["$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD}$。", f"${pa * pb}={pc}\\,\\mathrm{{PD}}$。", f"$\\mathrm{{PD}}={pd}$。"],
               alt=["$\\triangle\\mathrm{PAC}\\sim\\triangle\\mathrm{PDB}$ を示し、$\\mathrm{PA}:\\mathrm{PD}=\\mathrm{PC}:\\mathrm{PB}$ から求めてもよい。"],
               pc=[("方べきの定理の式を正しく立てている", 1), ("PD を正しく求めている", 1)],
               pit=["弦の長さ AB や CD を使ってしまう。"],
               chk=(f"Rational({pa}*{pb},{pc})", str(pd)))


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 5, ["computation", "concept"])
def ceva(r):
    while True:
        p, q, s1, s2 = r.randint(1, 6), r.randint(1, 6), r.randint(1, 6), r.randint(1, 6)
        if gcd(p, q) == 1 and gcd(s1, s2) == 1 and (p, q) != (s1, s2) and p != q:
            break
    ask = r.choice(["CE", "AF", "BD"])
    names = {"AF": ("AF", "FB", p, q), "BD": ("BD", "DC", s1, s2)}
    if ask == "CE":
        g1, g2 = names["AF"], names["BD"]
        num_, den = q * s2, p * s1
        tgt = ("CE", "EA")
    elif ask == "AF":
        g1, g2 = names["BD"], ("CE", "EA", p, q)
        num_, den = s2 * q, s1 * p
        tgt = ("AF", "FB")
    else:
        g1, g2 = names["AF"], ("CE", "EA", s1, s2)
        num_, den = q * s2, p * s1
        tgt = ("BD", "DC")
    ans = ratio(num_, den)
    given = f"$\\mathrm{{{g1[0]}}}:\\mathrm{{{g1[1]}}}={g1[2]}:{g1[3]}$、$\\mathrm{{{g2[0]}}}:\\mathrm{{{g2[1]}}}={g2[2]}:{g2[3]}$"
    return sa(f"$\\triangle\\mathrm{{ABC}}$ の内部の点 O について、直線 AO、BO、CO が辺 BC、CA、AB と交わる点をそれぞれ D、E、F とする。{given} のとき、$\\mathrm{{{tgt[0]}}}:\\mathrm{{{tgt[1]}}}$ を最も簡単な整数の比で求めなさい。",
              f"$\\mathrm{{{tgt[0]}}}:\\mathrm{{{tgt[1]}}}={ans}$",
              f"チェバの定理 $\\dfrac{{\\mathrm{{AF}}}}{{\\mathrm{{FB}}}}\\cdot\\dfrac{{\\mathrm{{BD}}}}{{\\mathrm{{DC}}}}\\cdot\\dfrac{{\\mathrm{{CE}}}}{{\\mathrm{{EA}}}}=1$ に代入すると $\\dfrac{{\\mathrm{{{tgt[0]}}}}}{{\\mathrm{{{tgt[1]}}}}}=\\dfrac{{{num_}}}{{{den}}}$。", d=3,
              v=[ans], fig=CEVA_FIG,
              ap="3本の直線が1点 O で交わるので、チェバの定理を使う。A → F → B → D → C → E → A の順に比をかけると $1$ になる。",
              steps=["$\\dfrac{\\mathrm{AF}}{\\mathrm{FB}}\\cdot\\dfrac{\\mathrm{BD}}{\\mathrm{DC}}\\cdot\\dfrac{\\mathrm{CE}}{\\mathrm{EA}}=1$ を書く。",
                     f"分かっている2つの比 $\\dfrac{{{g1[2]}}}{{{g1[3]}}}$、$\\dfrac{{{g2[2]}}}{{{g2[3]}}}$ を代入する。",
                     f"$\\dfrac{{\\mathrm{{{tgt[0]}}}}}{{\\mathrm{{{tgt[1]}}}}}=\\dfrac{{{g1[3]}\\cdot{g2[3]}}}{{{g1[2]}\\cdot{g2[2]}}}=\\dfrac{{{num_}}}{{{den}}}$ より ${ans}$。"],
              alt=["面積比で確かめる：$\\triangle\\mathrm{OAB}$、$\\triangle\\mathrm{OBC}$、$\\triangle\\mathrm{OCA}$ の面積の比を文字でおき、各辺の比を面積比で表すと同じ結果になる。"],
              pc=[("チェバの定理を正しい順序で立てている", 2), ("比を正しく計算し、最も簡単な整数の比にしている", 2)],
              pit=["比をたどる順序を崩して、分子と分母を逆に代入する。", "求めた分数の分子・分母を比の前後に逆に対応させる。"],
              chk=(f"Rational({g1[3]}*{g2[3]},{g1[2]}*{g2[2]})", f"Rational({num_},{den})", None, "intermediate"))


@gen("standard_practice", 5, ["computation", "condition_check"])
def menelaus(r):
    while True:
        a, b, c, d = r.randint(1, 5), r.randint(1, 5), r.randint(1, 5), r.randint(1, 5)
        if gcd(a, b) == 1 and gcd(c, d) == 1 and b * c != a * d:
            break
    num_, den = b * c, a * d
    ans = ratio(num_, den)
    side = "C" if num_ > den else "B"
    return sa(f"$\\triangle\\mathrm{{ABC}}$ の辺 AB を ${a}:{b}$ に内分する点を R、辺 AC を ${c}:{d}$ に内分する点を Q とする。直線 RQ と直線 BC の交点を P とするとき、$\\mathrm{{BP}}:\\mathrm{{PC}}$ を最も簡単な整数の比で求めなさい。",
              f"$\\mathrm{{BP}}:\\mathrm{{PC}}={ans}$",
              f"メネラウスの定理 $\\dfrac{{\\mathrm{{BP}}}}{{\\mathrm{{PC}}}}\\cdot\\dfrac{{\\mathrm{{CQ}}}}{{\\mathrm{{QA}}}}\\cdot\\dfrac{{\\mathrm{{AR}}}}{{\\mathrm{{RB}}}}=1$ より $\\dfrac{{\\mathrm{{BP}}}}{{\\mathrm{{PC}}}}\\cdot\\dfrac{{{d}}}{{{c}}}\\cdot\\dfrac{{{a}}}{{{b}}}=1$。", d=3, v=[ans],
              ap="三角形 ABC を1本の直線 PQR が横切っているので、メネラウスの定理を使う。P は辺 BC の延長上にある。",
              steps=["$\\dfrac{\\mathrm{BP}}{\\mathrm{PC}}\\cdot\\dfrac{\\mathrm{CQ}}{\\mathrm{QA}}\\cdot\\dfrac{\\mathrm{AR}}{\\mathrm{RB}}=1$。",
                     f"$\\dfrac{{\\mathrm{{CQ}}}}{{\\mathrm{{QA}}}}=\\dfrac{{{d}}}{{{c}}}$、$\\dfrac{{\\mathrm{{AR}}}}{{\\mathrm{{RB}}}}=\\dfrac{{{a}}}{{{b}}}$ を代入する。",
                     f"$\\dfrac{{\\mathrm{{BP}}}}{{\\mathrm{{PC}}}}=\\dfrac{{{b}\\cdot{c}}}{{{a}\\cdot{d}}}$ より ${ans}$（P は {'C' if side == 'C' else 'B'} の外側にある）。"],
              alt=["C を通り直線 RQ に平行な直線を引き、平行線と線分の比を2回使っても求められる（メネラウスの定理の証明と同じ考え方）。"],
              pc=[("メネラウスの定理を正しく立てている", 2), ("比を正しく計算している", 2)],
              pit=["CQ:QA を AQ:QC のまま代入してしまう（与えられた比の向きの確認不足）。", "外分点 P を内分点と考える。"],
              chk=(f"Rational({b}*{c},{a}*{d})", f"Rational({num_},{den})", None, "intermediate"))


@gen("standard_practice", 4, ["computation"])
def tangent_secant(r):
    form = r.choice(["PT", "PT", "AB"])
    if form == "PT":
        pa, ab = r.randint(1, 9), r.randint(1, 12)
        pb = pa + ab
        pt = sp.sqrt(pa * pb)
        return sa(f"円の外部の点 P から円に引いた接線の接点を T とする。P を通る別の直線が円と2点 A, B で交わり、$\\mathrm{{PA}}={pa}$、$\\mathrm{{AB}}={ab}$（A は P と B の間）である。線分 PT の長さを求めなさい。",
                  f"${sp.latex(pt)}$", f"$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={pa}\\times{pb}={pa * pb}$。", d=3, v=[str(pt)],
                  ap="接線と割線がある方べきの定理 $\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{PB}$。PB は P からの距離なので $\\mathrm{PA}+\\mathrm{AB}$。",
                  steps=[f"$\\mathrm{{PB}}={pa}+{ab}={pb}$。", f"$\\mathrm{{PT}}^2={pa}\\times{pb}={pa * pb}$。", f"$\\mathrm{{PT}}>0$ より $\\mathrm{{PT}}={sp.latex(pt)}$。"],
                  alt=["$\\triangle\\mathrm{PTA}\\sim\\triangle\\mathrm{PBT}$（接弦定理）から $\\mathrm{PT}:\\mathrm{PB}=\\mathrm{PA}:\\mathrm{PT}$ として求めてもよい。"],
                  pc=[("PB を正しく求めている", 1), ("方べきの定理の式を正しく立てている", 2), ("PT を正しく求めている", 1)],
                  pit=["$\\mathrm{PT}^2=\\mathrm{PA}\\cdot\\mathrm{AB}$ とする。", "根号を簡単にし忘れる。"],
                  chk=(f"sqrt({pa}*({pa}+{ab}))", str(pt), None, "intermediate"))
    pa, pb = r.choice([(x, y) for x in range(1, 13) for y in range(x + 1, 41) if int((x * y) ** 0.5 + 0.5) ** 2 == x * y])
    pt = int((pa * pb) ** 0.5 + 0.5)
    return num(f"円の外部の点 P から円に接線を引き、接点を T とする。P を通る直線が円と2点 A, B で交わり（A は P と B の間）、$\\mathrm{{PT}}={pt}$、$\\mathrm{{PA}}={pa}$ である。弦 AB の長さを求めなさい。",
               str(pb - pa), f"$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{PB}}$ より $\\mathrm{{PB}}={pt * pt}\\div{pa}={pb}$、$\\mathrm{{AB}}={pb}-{pa}={pb - pa}$。", d=3,
               ap="方べきの定理で求まるのは P からの距離 PB。弦 AB は PB から PA を引いて求める。",
               steps=[f"${pt}^2={pa}\\cdot\\mathrm{{PB}}$。", f"$\\mathrm{{PB}}={pb}$。", f"$\\mathrm{{AB}}=\\mathrm{{PB}}-\\mathrm{{PA}}={pb - pa}$。"],
               alt=[f"答えを代入して $\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={pa}\\times{pb}={pa * pb}={pt}^2$ となることを確かめる。"],
               pc=[("方べきの定理の式を正しく立てている", 2), ("PB から AB を正しく求めている", 2)],
               pit=["求めた PB をそのまま AB と答える。"],
               chk=(f"Rational({pt}**2,{pa})-{pa}", str(pb - pa)))


@gen("standard_practice", 3, ["computation", "condition_check"])
def center_angle(r):
    form = r.choice(["I", "O", "Iinv"])
    if form == "I":
        a = r.choice(range(30, 151, 2))
        ans = 90 + a // 2
        stem = f"$\\triangle\\mathrm{{ABC}}$ の内心を I とする。$\\angle\\mathrm{{BAC}}={a}^\\circ$ のとき、$\\angle\\mathrm{{BIC}}$ の大きさを求めなさい。"
        e = f"$\\angle\\mathrm{{IBC}}+\\angle\\mathrm{{ICB}}=\\dfrac{{1}}{{2}}(180^\\circ-{a}^\\circ)={90 - a // 2}^\\circ$ より $\\angle\\mathrm{{BIC}}={ans}^\\circ$。"
        steps = [f"$\\angle\\mathrm{{B}}+\\angle\\mathrm{{C}}=180^\\circ-{a}^\\circ={180 - a}^\\circ$。", f"BI、CI は角の二等分線なので $\\angle\\mathrm{{IBC}}+\\angle\\mathrm{{ICB}}={90 - a // 2}^\\circ$。",
                 f"$\\angle\\mathrm{{BIC}}=180^\\circ-{90 - a // 2}^\\circ={ans}^\\circ$。"]
        expr = f"180-(180-{a})/2"
        ap = "内心は内角の二等分線の交点。$\\triangle\\mathrm{IBC}$ の内角の和を考える。"
    elif form == "Iinv":
        a = r.choice(range(30, 151, 2))
        bic = 90 + a // 2
        ans = a
        stem = f"$\\triangle\\mathrm{{ABC}}$ の内心を I とすると、$\\angle\\mathrm{{BIC}}={bic}^\\circ$ であった。$\\angle\\mathrm{{BAC}}$ の大きさを求めなさい。"
        e = f"$\\angle\\mathrm{{BIC}}=90^\\circ+\\dfrac{{1}}{{2}}\\angle\\mathrm{{A}}$ より $\\angle\\mathrm{{A}}=2({bic}^\\circ-90^\\circ)={a}^\\circ$。"
        steps = [f"$\\angle\\mathrm{{IBC}}+\\angle\\mathrm{{ICB}}=180^\\circ-{bic}^\\circ={180 - bic}^\\circ$。", f"$\\angle\\mathrm{{B}}+\\angle\\mathrm{{C}}=2\\times{180 - bic}^\\circ={2 * (180 - bic)}^\\circ$。",
                 f"$\\angle\\mathrm{{A}}=180^\\circ-{2 * (180 - bic)}^\\circ={a}^\\circ$。"]
        expr = f"180-2*(180-{bic})"
        ap = "内心は内角の二等分線の交点。$\\angle\\mathrm{B}$、$\\angle\\mathrm{C}$ の半分の和を $\\angle\\mathrm{BIC}$ から逆算する。"
    else:
        a = r.choice(range(20, 90, 2))
        ans = 2 * a
        stem = f"鋭角三角形 ABC の外心を O とする。$\\angle\\mathrm{{BAC}}={a}^\\circ$ のとき、$\\angle\\mathrm{{BOC}}$ の大きさを求めなさい。"
        e = f"O は外接円の中心なので、$\\angle\\mathrm{{BOC}}$ は弧 BC に対する中心角で、円周角 $\\angle\\mathrm{{BAC}}$ の2倍。${ans}^\\circ$。"
        steps = ["外心 O は外接円の中心である。", "$\\angle\\mathrm{BOC}$ は弧 BC に対する中心角、$\\angle\\mathrm{BAC}$ は同じ弧に対する円周角。", f"$\\angle\\mathrm{{BOC}}=2\\times{a}^\\circ={ans}^\\circ$。"]
        expr = f"2*{a}"
        ap = "外心は外接円の中心。中心角と円周角の関係（円周角の定理）が使える。"
    return num(stem, str(ans), e, d=3, disp=f"${ans}^\\circ$", ap=ap, steps=steps,
               alt=["$\\angle\\mathrm{BIC}=90^\\circ+\\dfrac{1}{2}\\angle\\mathrm{A}$、$\\angle\\mathrm{BOC}=2\\angle\\mathrm{A}$（A が鋭角のとき）を公式として覚えておき、検算に使う。"],
               pc=[("内心・外心の性質を正しく使っている", 2), ("角度を正しく求めている", 2)],
               pit=["内心と外心の性質を取り違える。", "外心の場合、$\\angle\\mathrm{A}$ が鈍角だと O は BC に関して A と反対側にあり、$\\angle\\mathrm{BOC}=360^\\circ-2\\angle\\mathrm{A}$ となることを見落とす。"],
               chk=(expr, str(ans)))


TANG_TRI = [(a, b, c) for a in range(4, 16) for b in range(4, 16) for c in range(4, 16)
            if a < b + c and b < a + c and c < a + b and (a + b + c) % 2 == 0 and len({a, b, c}) == 3]


@gen("standard_practice", 3, ["computation", "concept"])
def tangent_length(r):
    a, b, c = r.choice(TANG_TRI)
    ask = r.choice(["AF", "BD", "CE"])
    val = {"AF": (b + c - a) // 2, "BD": (a + c - b) // 2, "CE": (a + b - c) // 2}[ask]
    return num(f"$\\mathrm{{BC}}={a}$、$\\mathrm{{CA}}={b}$、$\\mathrm{{AB}}={c}$ の $\\triangle\\mathrm{{ABC}}$ の内接円が、辺 BC、CA、AB に接する点をそれぞれ D、E、F とする。線分 {ask} の長さを求めなさい。",
               str(val), "円外の点から引いた2本の接線の長さは等しいので、$\\mathrm{AF}=\\mathrm{AE}=x$、$\\mathrm{BD}=\\mathrm{BF}=y$、$\\mathrm{CE}=\\mathrm{CD}=z$ とおける。", d=3,
               ap="円の外部の点から引いた2本の接線の長さは等しい。頂点ごとに接線の長さを文字でおき、3辺の長さの式を連立する。",
               steps=["$\\mathrm{AF}=\\mathrm{AE}=x$、$\\mathrm{BD}=\\mathrm{BF}=y$、$\\mathrm{CD}=\\mathrm{CE}=z$ とおく。",
                      f"$x+y={c}$、$y+z={a}$、$z+x={b}$。3式を加えて $x+y+z={(a + b + c) // 2}$。",
                      f"$\\mathrm{{{ask}}}={val}$。"],
               alt=[f"$x=\\dfrac{{b+c-a}}{{2}}$ のように「隣り合う2辺の和から対辺を引いて2で割る」と覚えておくと速い：$\\mathrm{{AF}}={(b + c - a) // 2}$、$\\mathrm{{BD}}={(a + c - b) // 2}$、$\\mathrm{{CE}}={(a + b - c) // 2}$。"],
               pc=[("接線の長さが等しいことを使って式を立てている", 2), ("連立して正しく求めている", 2)],
               pit=["$\\mathrm{AF}=\\dfrac{1}{2}\\mathrm{AB}$ のように、接点を辺の中点と思いこむ。"],
               chk=({"AF": f"({b}+{c}-{a})/2", "BD": f"({a}+{c}-{b})/2", "CE": f"({a}+{b}-{c})/2"}[ask], str(val)))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 3, ["written_reasoning", "computation"])
def menelaus_ceva(r):
    while True:
        m, n, p, q = r.randint(1, 4), r.randint(1, 4), r.randint(1, 4), r.randint(1, 4)
        if gcd(m, n) == 1 and gcd(p, q) == 1 and (m, n, p, q) != (2, 1, 3, 1):
            break
    bo = sp.Rational(n * (p + q), m * q)
    br = sp.Rational(n * p, m * q)
    r1, r2 = ratio(n * (p + q), m * q), ratio(n * p, m * q)
    return desc(f"$\\triangle\\mathrm{{ABC}}$ の辺 AB 上に $\\mathrm{{AP}}:\\mathrm{{PB}}={m}:{n}$ となる点 P を、辺 AC 上に $\\mathrm{{AQ}}:\\mathrm{{QC}}={p}:{q}$ となる点 Q をとり、線分 BQ と線分 CP の交点を O とする。"
                f"さらに、直線 AO と辺 BC の交点を R とする。(1) $\\mathrm{{BO}}:\\mathrm{{OQ}}$、(2) $\\mathrm{{BR}}:\\mathrm{{RC}}$ をそれぞれ求め、用いた定理と三角形・直線を明記して説明しなさい。",
                f"(1) $\\mathrm{{BO}}:\\mathrm{{OQ}}={r1}$　(2) $\\mathrm{{BR}}:\\mathrm{{RC}}={r2}$",
                f"(1) $\\triangle\\mathrm{{ABQ}}$ と直線 PC にメネラウスの定理。(2) $\\triangle\\mathrm{{ABC}}$ と点 O にチェバの定理。",
                [("(1) メネラウスの定理を適用する三角形と直線を正しく選び、式を立てている", 2), ("(1) の比を正しく求めている", 2),
                 ("(2) チェバの定理を正しく立てている", 2), ("(2) の比を正しく求めている", 2)], d=4, p=8, lines=10,
                ap="(1) は「BO:OQ」を含む三角形 ABQ と、それを横切る直線 P-O-C の組を見つける。(2) は3本の線分 AR、BQ、CP が1点 O で交わるのでチェバの定理。",
                steps=[f"(1) $\\triangle\\mathrm{{ABQ}}$ と直線 PC：$\\dfrac{{\\mathrm{{AP}}}}{{\\mathrm{{PB}}}}\\cdot\\dfrac{{\\mathrm{{BO}}}}{{\\mathrm{{OQ}}}}\\cdot\\dfrac{{\\mathrm{{QC}}}}{{\\mathrm{{CA}}}}=1$。",
                       f"$\\dfrac{{{m}}}{{{n}}}\\cdot\\dfrac{{\\mathrm{{BO}}}}{{\\mathrm{{OQ}}}}\\cdot\\dfrac{{{q}}}{{{p + q}}}=1$ より $\\dfrac{{\\mathrm{{BO}}}}{{\\mathrm{{OQ}}}}={sp.latex(bo)}$、$\\mathrm{{BO}}:\\mathrm{{OQ}}={r1}$。",
                       f"(2) $\\triangle\\mathrm{{ABC}}$ と点 O：$\\dfrac{{\\mathrm{{AP}}}}{{\\mathrm{{PB}}}}\\cdot\\dfrac{{\\mathrm{{BR}}}}{{\\mathrm{{RC}}}}\\cdot\\dfrac{{\\mathrm{{CQ}}}}{{\\mathrm{{QA}}}}=1$。",
                       f"$\\dfrac{{{m}}}{{{n}}}\\cdot\\dfrac{{\\mathrm{{BR}}}}{{\\mathrm{{RC}}}}\\cdot\\dfrac{{{q}}}{{{p}}}=1$ より $\\mathrm{{BR}}:\\mathrm{{RC}}={r2}$。"],
                alt=["(1) は面積比でも求められる：$\\mathrm{BO}:\\mathrm{OQ}=\\triangle\\mathrm{BCP}:\\triangle\\mathrm{QCP}$ を、AB・AC 上の比から計算する。"],
                pc=[("(1) の式", 2), ("(1) の答え", 2), ("(2) の式", 2), ("(2) の答え", 2)],
                pit=["(1) で $\\dfrac{\\mathrm{QC}}{\\mathrm{CA}}$ を $\\dfrac{\\mathrm{QC}}{\\mathrm{QA}}$ としてしまう（C は辺 QA の外側の点）。", "どの三角形にどの直線を当てはめたのかを答案に書かない。"],
                chk=(f"[Rational({n},{m})*Rational({p + q},{q}), Rational({n},{m})*Rational({p},{q})]", f"[{bo}, {br}]", None, "intermediate"))


@gen("thinking_writing", 2, ["written_reasoning", "condition_check"])
def concyclic_check(r):
    yes = r.random() < 0.5
    while True:
        pa, pb, pc = r.randint(2, 12), r.randint(2, 12), r.randint(2, 12)
        if (pa * pb) % pc == 0 and pa * pb // pc != pc:
            break
    pd = pa * pb // pc if yes else pa * pb // pc + r.choice([-1, 1])
    if pd <= 0 or pd == pc:
        pd = pa * pb // pc + 2
    prod1, prod2 = pa * pb, pc * pd
    ans = "4点 A, B, C, D は同一円周上にある" if prod1 == prod2 else "4点 A, B, C, D は同一円周上にない"
    return desc(f"線分 AB と線分 CD が点 P で交わり、$\\mathrm{{PA}}={pa}$、$\\mathrm{{PB}}={pb}$、$\\mathrm{{PC}}={pc}$、$\\mathrm{{PD}}={pd}$ である。4点 A, B, C, D が同一円周上にあるかどうかを判定し、その理由を説明しなさい。",
                ans, f"$\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={prod1}$、$\\mathrm{{PC}}\\cdot\\mathrm{{PD}}={prod2}$。" + ("等しいので、方べきの定理の逆より同一円周上にある。" if prod1 == prod2 else "等しくないので、方べきの定理（対偶）より同一円周上にない。"),
                [("2つの積を正しく計算している", 2), ("方べきの定理の逆（または対偶）を根拠として述べている", 4), ("正しい結論を述べている", 2)], d=4, p=8, lines=8,
                ap="方べきの定理には逆が成り立つ。線分 AB、CD が P で交わるとき、$\\mathrm{PA}\\cdot\\mathrm{PB}=\\mathrm{PC}\\cdot\\mathrm{PD}$ ならば4点は同一円周上にある。",
                steps=[f"$\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={pa}\\times{pb}={prod1}$。", f"$\\mathrm{{PC}}\\cdot\\mathrm{{PD}}={pc}\\times{pd}={prod2}$。",
                       ("両者は等しいので、$\\mathrm{PA}:\\mathrm{PD}=\\mathrm{PC}:\\mathrm{PB}$ と対頂角から $\\triangle\\mathrm{PAC}\\sim\\triangle\\mathrm{PDB}$、$\\angle\\mathrm{PAC}=\\angle\\mathrm{PDB}$。円周角の定理の逆より同一円周上にある。"
                        if prod1 == prod2 else "両者は等しくない。もし4点が同一円周上にあれば方べきの定理より積が等しくなるはずなので矛盾。よって同一円周上にない。")],
                alt=["相似の比を直接調べる：$\\mathrm{PA}:\\mathrm{PD}$ と $\\mathrm{PC}:\\mathrm{PB}$ が等しいかどうかで判定してもよい。"],
                pc=[("積の計算", 2), ("定理の逆・対偶による根拠", 4), ("結論", 2)],
                pit=["方べきの定理を「円があること」を前提とせずに使ってよいか（逆が成り立つか）を説明しない。", "積ではなく和 $\\mathrm{PA}+\\mathrm{PB}$ を比べる。"],
                chk=(f"{pa}*{pb}-{pc}*{pd}", str(prod1 - prod2), None, "intermediate"))


TRIS = [(13, 14, 15, 84), (5, 12, 13, 30), (9, 10, 17, 36), (10, 13, 13, 60), (11, 13, 20, 66), (5, 5, 6, 12),
        (5, 5, 8, 12), (13, 20, 21, 126), (7, 15, 20, 42), (6, 25, 29, 60), (6, 8, 10, 24), (3, 4, 5, 6)]


@gen("thinking_writing", 3, ["cross_unit", "application", "written_reasoning"], rel=["HS-MATH1-U04"])
def inradius(r):
    a, b, c, S = r.choice(TRIS)
    a, b, c = r.sample([a, b, c], 3)
    ask = r.choice(["r", "R"])
    s = sp.Rational(a + b + c, 2)
    cosA = sp.Rational(b * b + c * c - a * a, 2 * b * c)
    sinA = sp.sqrt(1 - cosA ** 2)
    assert sp.simplify(sp.Rational(1, 2) * b * c * sinA - S) == 0
    val = sp.Rational(S) / s if ask == "r" else sp.Rational(a * b * c, 4 * S)
    name = "内接円の半径 $r$" if ask == "r" else "外接円の半径 $R$"
    last = (f"$S=\\dfrac{{1}}{{2}}r(a+b+c)$ より $r=\\dfrac{{2S}}{{a+b+c}}=\\dfrac{{{2 * S}}}{{{a + b + c}}}={sp.latex(val)}$。" if ask == "r"
            else f"正弦定理 $\\dfrac{{a}}{{\\sin A}}=2R$ より $R=\\dfrac{{{a}}}{{2\\cdot {sp.latex(sinA)}}}={sp.latex(val)}$。")
    return sa(f"$\\mathrm{{BC}}={a}$、$\\mathrm{{CA}}={b}$、$\\mathrm{{AB}}={c}$ の $\\triangle\\mathrm{{ABC}}$ について、面積 $S$ と{name}を求めなさい。考え方も書きなさい。",
              f"$S={S}$、${ask}={sp.latex(val)}$",
              f"余弦定理で $\\cos A$、そこから $\\sin A$ を求めて $S=\\dfrac{{1}}{{2}}bc\\sin A$。" + ("内心 I で3つの三角形に分けると $S=\\dfrac{1}{2}r(a+b+c)$。" if ask == "r" else "正弦定理で $R$ を求める。"),
              d=4, p=8, v=[f"S={S}, {ask}={val}"],
              ap="面積は「図形と計量」の余弦定理・面積公式で求める。内接円の半径は、内心と3頂点を結んで三角形を3つに分ける考え（内心が3辺から等距離）で面積と結びつく。外接円の半径は正弦定理。",
              steps=[f"余弦定理：$\\cos A=\\dfrac{{{b}^2+{c}^2-{a}^2}}{{2\\cdot{b}\\cdot{c}}}={sp.latex(cosA)}$。",
                     f"$\\sin A=\\sqrt{{1-\\cos^2A}}={sp.latex(sinA)}$（$0^\\circ<A<180^\\circ$ より $\\sin A>0$）。",
                     f"$S=\\dfrac{{1}}{{2}}\\cdot{b}\\cdot{c}\\cdot{sp.latex(sinA)}={S}$。", last],
              alt=["ヘロンの公式 $S=\\sqrt{s(s-a)(s-b)(s-c)}$（$s=\\dfrac{a+b+c}{2}$）を使うと面積を直接求められる。" + ("" if ask == "r" else "また $R=\\dfrac{abc}{4S}$ でも求められる。")],
              pc=[("$\\cos A$、$\\sin A$ を正しく求めている", 2), ("面積を正しく求めている", 2),
                  ("半径を求める関係式（内心で3分割／正弦定理）を正しく立てている", 2), ("半径を正しく求めている", 2)],
              pit=["$\\sin A$ を求めるときに根号の計算を誤る。", "内接円の半径の式で $S=r(a+b+c)$ と $\\dfrac{1}{2}$ を落とす。"],
              chk=(f"[Rational(1,2)*{b}*{c}*sqrt(1-(Rational({b * b + c * c - a * a},{2 * b * c}))**2), {'Rational(2*' + str(S) + ',' + str(a + b + c) + ')' if ask == 'r' else 'Rational(' + str(a * b * c) + ',' + str(4 * S) + ')'}]",
                   f"[{S}, {val}]", None, "intermediate"))


@gen("thinking_writing", 2, ["cross_unit", "application", "condition_check"], rel=["JH-MATH-G3-U07"])
def common_tangent(r):
    kind = r.choice(["ext", "int"])
    while True:
        r1, r2 = r.randint(2, 9), r.randint(1, 8)
        if r1 <= r2:
            continue
        d = r.randint(r1 + r2 + 1, r1 + r2 + 8)
        break
    k = r1 - r2 if kind == "ext" else r1 + r2
    L = sp.sqrt(d * d - k * k)
    nm = "共通外接線" if kind == "ext" else "共通内接線"
    return sa(f"半径 ${r1}$ の円 O と半径 ${r2}$ の円 O' があり、中心間の距離は $\\mathrm{{OO'}}={d}$ である。2つの円の{nm}の1本が円 O、O' に接する点をそれぞれ A、B とするとき、線分 AB の長さを求めなさい。",
              f"${sp.latex(L)}$",
              f"O' から OA（またはその延長）に垂線を引き、直角三角形をつくる。直角をはさむ辺は AB と ${r1}{'-' if kind == 'ext' else '+'}{r2}={k}$、斜辺は ${d}$。",
              d=4, p=8, v=[str(L)],
              ap="接線は接点を通る半径に垂直なので、OA と O'B はともに AB に垂直で平行。O' を通り AB に平行な直線を引くと、三平方の定理が使える直角三角形ができる。",
              steps=[f"$\\mathrm{{OA}}\\perp\\mathrm{{AB}}$、$\\mathrm{{O'B}}\\perp\\mathrm{{AB}}$。O' から直線 OA に垂線 O'H を下ろすと、$\\mathrm{{O'H}}=\\mathrm{{AB}}$。",
                     f"$\\mathrm{{OH}}={'半径の差' if kind == 'ext' else '半径の和'}={k}$（{'A と B が中心線の同じ側' if kind == 'ext' else 'A と B が中心線の反対側'}にあるため）。",
                     f"三平方の定理：$\\mathrm{{AB}}^2={d}^2-{k}^2={d * d - k * k}$。", f"$\\mathrm{{AB}}={sp.latex(L)}$。"],
              alt=[f"公式として、共通外接線の長さは $\\sqrt{{d^2-(r_1-r_2)^2}}$、共通内接線の長さは $\\sqrt{{d^2-(r_1+r_2)^2}}$ とまとめられる（共通内接線は $d>r_1+r_2$ のときに存在する）。"],
              pc=[("接線と半径が垂直であることを使って直角三角形をつくっている", 3), ("直角をはさむ辺が半径の" + ("差" if kind == "ext" else "和") + "であることを示している", 2), ("正しい長さを求めている", 3)],
              pit=["共通外接線で半径の和、共通内接線で半径の差を使ってしまう。", "$\\mathrm{AB}=\\mathrm{OO'}$ と考える。"],
              chk=(f"sqrt({d}**2-({r1}{'-' if kind == 'ext' else '+'}{r2})**2)", str(L), None, "intermediate"))


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def err_item(stem, wrong, step, etype, tempt, fix, ans, expl, steps, ap, alt, pit, chk=None, d=3):
    return desc(f"{stem}\n［ある生徒の解答］\n{wrong}\n上の解答の誤りを指摘し、正しい答えを求めなさい。", ans, expl,
                [("誤りの箇所と理由を正しく指摘している", 2), ("正しい解答を途中式とともに示している", 3), ("最終的な答えが正しい", 1)], d=d, p=6, lines=6,
                ap=ap, steps=steps, alt=alt, pc=[("誤りの指摘", 2), ("正しい途中式", 3), ("正しい答え", 1)], pit=pit,
                err=dict(sol=wrong, step=step, type=etype, tempt=tempt, fix=fix), chk=chk)


@gen("error_correction", 3, ["common_error", "concept"])
def err_bisector(r):
    while True:
        c, b = r.sample(range(3, 13), 2)
        a = r.randint(abs(b - c) + 1, b + c - 1)
        if (a * c) % (b + c) == 0 and b != c:
            break
    bd, wrong_bd = a * c // (b + c), sp.Rational(a * b, b + c)
    wrong = f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AC}}:\\mathrm{{AB}}={b}:{c}$ だから $\\mathrm{{BD}}={a}\\times\\dfrac{{{b}}}{{{b + c}}}={sp.latex(wrong_bd)}$"
    fix = f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AB}}:\\mathrm{{AC}}={c}:{b}$ より $\\mathrm{{BD}}={a}\\times\\dfrac{{{c}}}{{{b + c}}}={bd}$"
    return err_item(f"$\\mathrm{{AB}}={c}$、$\\mathrm{{BC}}={a}$、$\\mathrm{{CA}}={b}$ の $\\triangle\\mathrm{{ABC}}$ で、$\\angle\\mathrm{{A}}$ の二等分線と辺 BC の交点を D とする。BD の長さを求めなさい。",
                    wrong, "比の対応（$\\mathrm{BD}:\\mathrm{DC}$ に対応させた辺の順序）", "concept",
                    "「二等分線と比」は覚えていても、どの線分にどの辺が対応するかを図で確かめずに、辺の名前の並びで機械的に比を書いている。",
                    fix, f"$\\mathrm{{BD}}={bd}$", "B の側の線分 BD には、B の側の辺 AB が対応する。",
                    [f"$\\mathrm{{BD}}:\\mathrm{{DC}}=\\mathrm{{AB}}:\\mathrm{{AC}}={c}:{b}$。", f"$\\mathrm{{BD}}={a}\\times\\dfrac{{{c}}}{{{b + c}}}={bd}$。"],
                    "角の二等分線の定理は「隣り合う辺どうし」が対応する。図に比を書きこむと対応を誤りにくい。",
                    [f"$\\mathrm{{AB}}>\\mathrm{{AC}}$ なら D は C に近いはず、という大小の見通し（{'AB が長いので BD も長い' if c > b else 'AB が短いので BD も短い'}）で答えを確かめる。"],
                    ["比の対応を辺の名前のアルファベット順で決めてしまう。"],
                    chk=(f"Rational({a}*{c},{b + c})", str(bd), None, "intermediate"), d=2)


@gen("error_correction", 3, ["common_error", "condition_check"])
def err_power(r):
    pa, ab = r.randint(2, 9), r.randint(2, 12)
    pb = pa + ab
    pt = sp.sqrt(pa * pb)
    wsq = pa * ab
    wrong = f"方べきの定理より $\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{AB}}={pa}\\times{ab}={wsq}$、よって $\\mathrm{{PT}}={sp.latex(sp.sqrt(wsq))}$"
    fix = f"$\\mathrm{{PB}}={pa}+{ab}={pb}$、$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={pa * pb}$ より $\\mathrm{{PT}}={sp.latex(pt)}$"
    return err_item(f"円の外部の点 P から引いた接線の接点を T とする。P を通る直線が円と点 A, B で交わり（A は P と B の間）、$\\mathrm{{PA}}={pa}$、$\\mathrm{{AB}}={ab}$ である。PT の長さを求めなさい。",
                    wrong, "方べきの定理の式（PB の代わりに AB を使った部分）", "formula",
                    "図に書かれている長さ AB をそのまま使いたくなる。方べきの定理が「点 P からの距離の積」であることを意識していない。",
                    fix, f"$\\mathrm{{PT}}={sp.latex(pt)}$", "方べきの定理の積は、すべて点 P から円との交点までの距離。",
                    [f"$\\mathrm{{PB}}=\\mathrm{{PA}}+\\mathrm{{AB}}={pb}$。", f"$\\mathrm{{PT}}^2=\\mathrm{{PA}}\\cdot\\mathrm{{PB}}={pa}\\times{pb}={pa * pb}$。", f"$\\mathrm{{PT}}={sp.latex(pt)}$。"],
                    "方べきの定理は相似 $\\triangle\\mathrm{PTA}\\sim\\triangle\\mathrm{PBT}$ から出る。相似比の辺はどれも P を端点とする線分である。",
                    ["相似 $\\triangle\\mathrm{PTA}\\sim\\triangle\\mathrm{PBT}$ から $\\mathrm{PT}:\\mathrm{PB}=\\mathrm{PA}:\\mathrm{PT}$ を立てて確かめる。"],
                    ["弦の長さと P からの距離を混同する。"],
                    chk=(f"sqrt({pa}*({pa}+{ab}))", str(pt), None, "intermediate"))


@gen("error_correction", 2, ["common_error", "computation"])
def err_centroid(r):
    m = r.choice(range(9, 61, 3))
    wrong = f"重心は中線を $1:2$ に分けるので $\\mathrm{{AG}}=\\dfrac{{1}}{{3}}\\times{m}={m // 3}$"
    fix = f"重心は中線を頂点の側から $2:1$ に内分するので $\\mathrm{{AG}}=\\dfrac{{2}}{{3}}\\times{m}={2 * m // 3}$"
    return err_item(f"$\\triangle\\mathrm{{ABC}}$ の重心を G、辺 BC の中点を M とする。$\\mathrm{{AM}}={m}$ のとき、AG の長さを求めなさい。",
                    wrong, "重心が中線を分ける比（頂点側と中点側の取り違え）", "concept",
                    "「$2:1$」という数だけを覚えていて、どちら側が 2 なのかをあいまいにしている。",
                    fix, f"$\\mathrm{{AG}}={2 * m // 3}$", "$\\mathrm{AG}:\\mathrm{GM}=2:1$（頂点側が長い）。",
                    ["$\\mathrm{AG}:\\mathrm{GM}=2:1$。", f"$\\mathrm{{AG}}=\\dfrac{{2}}{{3}}\\times{m}={2 * m // 3}$。"],
                    "重心は三角形の「つり合いの点」で、頂点より辺の中点に近い位置にある。図で見通しを立ててから比を使う。",
                    ["座標で確かめる：A$(0,\\,3a)$、B$(-b,\\,0)$、C$(b,\\,0)$ とすると G$(0,\\,a)$、M$(0,\\,0)$ で、$\\mathrm{AG}=2a$、$\\mathrm{GM}=a$。"],
                    ["$\\mathrm{AG}$ と $\\mathrm{GM}$ のどちらが長いかを図で確かめない。"],
                    chk=(f"Rational(2,3)*{m}", str(2 * m // 3), None, "intermediate"), d=2)


@gen("error_correction", 2, ["common_error", "condition_check"])
def err_cyclic(r):
    x = r.choice(range(56, 126, 2))
    y = r.choice([v for v in range(56, 126, 2) if v != x and v != 180 - x])
    wrong = f"内接四角形では $\\angle\\mathrm{{A}}+\\angle\\mathrm{{B}}=180^\\circ$ なので $\\angle\\mathrm{{B}}=180^\\circ-{x}^\\circ={180 - x}^\\circ$"
    fix = f"$\\angle\\mathrm{{B}}$ の対角は $\\angle\\mathrm{{D}}$ なので $\\angle\\mathrm{{B}}=180^\\circ-{y}^\\circ={180 - y}^\\circ$"
    return err_item(f"円に内接する四角形 ABCD で、$\\angle\\mathrm{{A}}={x}^\\circ$、$\\angle\\mathrm{{D}}={y}^\\circ$ である。$\\angle\\mathrm{{B}}$ の大きさを求めなさい。",
                    wrong, "性質の適用（隣り合う角の和を $180^\\circ$ とした部分）", "concept",
                    "「和が $180^\\circ$」という形だけを覚えていて、どの2角の和かを確かめていない。平行四辺形の性質（隣り合う角の和が $180^\\circ$）と混同しやすい。",
                    fix, f"$\\angle\\mathrm{{B}}={180 - y}^\\circ$", "円に内接する四角形で和が $180^\\circ$ になるのは向かい合う角（$\\angle\\mathrm{B}$ と $\\angle\\mathrm{D}$）。",
                    ["$\\angle\\mathrm{B}$ と向かい合う角は $\\angle\\mathrm{D}$。", f"$\\angle\\mathrm{{B}}=180^\\circ-{y}^\\circ={180 - y}^\\circ$。"],
                    "対角の和が $180^\\circ$ になる理由（2つの円周角に対する中心角の和が $360^\\circ$）にもどって確認する。",
                    [f"$\\angle\\mathrm{{C}}=180^\\circ-{x}^\\circ={180 - x}^\\circ$ も求め、4つの角の和が $360^\\circ$ になることを確かめる。"],
                    ["隣り合う角と向かい合う角を取り違える。"],
                    chk=(f"180-{y}", str(180 - y), None, "intermediate"), d=2)


GENERATORS = [centroid_ratio, bisector_ratio, center_name, cyclic_quad_angle, power_chords,
              ceva, menelaus, tangent_secant, center_angle, tangent_length,
              menelaus_ceva, concyclic_check, inradius, common_tangent,
              err_bisector, err_power, err_centroid, err_cyclic]
