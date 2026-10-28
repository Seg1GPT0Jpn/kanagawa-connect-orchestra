"""単元パック：中学1年 空間図形（神奈川県公立高校入試形式）。"""
import re
import unicodedata
from fractions import Fraction as Fr

from banks._common import figure, mc, num, shape
from hs_pack_lib import (board, check, definition, derivation, example, gen, guide, intro, lesson, summary, theorem, tp)

UNIT_ID = "JH-MATH-G1-U06"

PREREQUISITES = [
    ("JH-MATH-G1-U05", "おうぎ形の弧の長さと面積を求められること。円錐の展開図（側面のおうぎ形）に使う。"),
    ("JH-MATH-G1-U02", "数量を文字式で表せること。体積・表面積の公式を文字で表して使う。"),
    ("JH-MATH-G1-U03", "一次方程式を解けること。体積や表面積から長さを逆算するときに使う。"),
]
EXTENSIONS = [
    ("JH-MATH-G3-U07", "三平方の定理を使い、円錐の高さや直方体の対角線など、空間図形の長さを求める。"),
    ("JH-MATH-G3-U05", "相似な立体の表面積の比・体積の比へ発展する。"),
    ("HS-MATH1-U04", "高校の図形と計量で、三角比を使って空間図形の長さ・角を求める。"),
]


# ----------------------------------------------------------------------
# 共通ヘルパー
# ----------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))


def MC(stem, right, cands, e, k=3, **kw):
    seen, ws = {_norm(right)}, []
    for t, why, mis in cands:
        if _norm(t) in seen:
            continue
        seen.add(_norm(t))
        ws.append((t, why, mis))
        if len(ws) == k:
            break
    assert len(ws) == k, (stem, right, cands)
    return mc(stem, [right] + [w[0] for w in ws], e, why={w[0]: (w[1], w[2]) for w in ws}, **kw)


def ftex(v):
    v = Fr(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def fpy(v):
    v = Fr(v)
    return str(v.numerator) if v.denominator == 1 else f"Rational({v.numerator},{v.denominator})"


def pitex(k):
    k = Fr(k)
    return "\\pi" if k == 1 else f"{ftex(k)}\\pi"


def cmu(k, u):
    return f"${pitex(k)}$ {u}"


def MARK(stem, v, e, expr, **kw):
    v = Fr(v)
    assert v >= 0
    if v.denominator == 1:
        n = int(v)
        return num(stem, str(n), e, mark=("int", n), chk=(expr, str(n), None, "answer"), **kw)
    p, q = v.numerator, v.denominator
    return num(stem, f"${ftex(v)}$", e, mark=("frac", p, q), chk=(expr, f"Rational({p},{q})", None, "answer"), **kw)


SEL4 = "次の1〜4の中から1つ選び，その番号を答えなさい。"
PI = "ただし，円周率は $\\pi$ とする。"


# ----------------------------------------------------------------------
# 立体の座標と見取図
# ----------------------------------------------------------------------

SOLIDS = {
    "直方体 ABCD−EFGH": dict(
        P={"A": (0, 0, 2), "B": (3, 0, 2), "C": (3, 2, 2), "D": (0, 2, 2), "E": (0, 0, 0), "F": (3, 0, 0), "G": (3, 2, 0), "H": (0, 2, 0)},
        E=["AB", "BC", "CD", "DA", "EF", "FG", "GH", "HE", "AE", "BF", "CG", "DH"],
        F=["ABCD", "EFGH", "ABFE", "BCGF", "CDHG", "DAEH"], hidden="H"),
    "三角柱 ABC−DEF": dict(
        P={"A": (0, 0, 2), "B": (3, 0, 2), "C": (1, 2, 2), "D": (0, 0, 0), "E": (3, 0, 0), "F": (1, 2, 0)},
        E=["AB", "BC", "CA", "DE", "EF", "FD", "AD", "BE", "CF"],
        F=["ABC", "DEF", "ABED", "BCFE", "CADF"], hidden="F"),
    "四角錐 O−ABCD": dict(
        P={"O": (1.5, 1, 2.5), "A": (0, 0, 0), "B": (3, 0, 0), "C": (3, 2, 0), "D": (0, 2, 0)},
        E=["OA", "OB", "OC", "OD", "AB", "BC", "CD", "DA"],
        F=["ABCD", "OAB", "OBC", "OCD", "ODA"], hidden="D"),
}


def _sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _iszero(v):
    return all(abs(x) < 1e-9 for x in v)


def edge_rel(S, e1, e2):
    P = S["P"]
    a, b, c, d = P[e1[0]], P[e1[1]], P[e2[0]], P[e2[1]]
    u, v = _sub(b, a), _sub(d, c)
    if _iszero(_cross(u, v)):
        return "平行"
    if abs(_dot(_cross(u, v), _sub(c, a))) < 1e-9:
        return "交わる"
    return "ねじれ"


def edge_face(S, e, f):
    P = S["P"]
    a, b = P[e[0]], P[e[1]]
    p0, p1, p2 = P[f[0]], P[f[1]], P[f[2]]
    n = _cross(_sub(p1, p0), _sub(p2, p0))
    u = _sub(b, a)
    if _iszero(_cross(u, n)):
        return "垂直"
    if abs(_dot(u, n)) < 1e-9:
        if abs(_dot(_sub(a, p0), n)) < 1e-9:
            return "含まれる"
        return "平行"
    return "交わる"


def solid_svg(name):
    S = SOLIDS[name]
    pts = {k: (x + 0.55 * y, z + 0.4 * y) for k, (x, y, z) in S["P"].items()}
    h = S["hidden"]
    solid = [(e[0], e[1]) for e in S["E"] if h not in e]
    dashed = [(e[0], e[1]) for e in S["E"] if h in e]
    return shape(pts, segments=solid, dashed=dashed, scale=34)


def solid_fig(name):
    return figure(f"{name} の見取図", solid_svg(name))


# ----------------------------------------------------------------------
# 授業プリント
# ----------------------------------------------------------------------

LESSON = lesson(
    goals=["空間における2直線・直線と平面・2平面の位置関係を見取図から判断し、「ねじれの位置」を説明できる。",
           "立体を、平面図形の運動（平行に動かす・回転させる）や投影図・展開図としてとらえられる。",
           "角柱・円柱・角錐・円錐・球の体積と表面積を求め、円錐の側面積をおうぎ形の考えから導ける。"],
    duration=100,
    readiness=["小学校で学んだ角柱・円柱の体積（底面積×高さ）を求められる。",
               "小学校で学んだ見取図・展開図から、立体の面・辺・頂点の数を数えられる。",
               "おうぎ形の弧の長さと面積を求められる（平面図形の単元）。"],
    flow=[("導入：いろいろな立体", 10, "立体模型を分類し、多面体・正多面体・回転体の用語を確認する"),
          ("直線や平面の位置関係", 20, "直方体の辺どうし・辺と面の関係を調べ、ねじれの位置を定義する（例題1）"),
          ("立体の見方", 15, "面の平行移動・回転による立体、投影図（立面図・平面図）"),
          ("体積", 20, "柱体と錐体の体積の関係（1/3）を実験で確かめ、公式を使う"),
          ("表面積と円錐の展開図", 25, "円錐の側面のおうぎ形の中心角と面積を導く（例題2・3）"),
          ("まとめと確認", 10, "確認問題と問題プリントの指示")],
    sections=[
        intro("in1", "立体を分類する",
              "平面だけで囲まれた立体を多面体という。角柱・角錐は多面体である。円柱・円錐・球のように曲面をもつ立体は多面体ではない。すべての面が合同な正多角形で、どの頂点にも面が同じ数だけ集まる、へこみのない多面体を正多面体といい、正四面体・正六面体（立方体）・正八面体・正十二面体・正二十面体の5種類しかない。",
              bullets=["角柱・円柱は底面が2つあり、角錐・円錐は底面が1つで頂点がある。", "立体は「面が動いた跡」や「平面図形を回転させた跡」として見ることもできる。"],
              points=[tp("立体模型を手に取らせ、底面の形と側面の形で分類させる。", ask="三角柱と三角錐はどこが同じで、どこが違うか。", expect="底面が三角形なのは同じ。三角柱は底面が2つで側面が長方形、三角錐は底面が1つで側面が三角形。", timing="導入の最初"),
                      tp("正多面体の面・頂点・辺の数を表にまとめさせると、規則性に気づかせやすい。", caution="正八面体の頂点の数（6）と面の数（8）を取り違える生徒が多い。")]),
        definition("df1", "空間における直線や平面の位置関係",
                   "空間にある2直線の位置関係には、(1) 交わる、(2) 平行である、(3) ねじれの位置にある、の3つの場合がある。平行でなく、交わらない2直線は「ねじれの位置にある」という。",
                   conditions=["同じ平面上にある2直線は、交わるか平行かのどちらかである。ねじれの位置にある2直線は同じ平面上にない。",
                               "直線と平面の位置関係：直線が平面に含まれる／1点で交わる／平行である（交わらない）。",
                               "直線 $\\ell$ が平面 P と点 O で交わり、O を通る P 上の2直線に垂直なとき、$\\ell$ と P は垂直であるという。",
                               "2平面の位置関係：交わる（交わりは直線）か平行である。"],
                   points=[tp("教室の天井と壁の境目、床と壁の境目などの「線」を使って、ねじれの位置の具体例を探させる。", ask="黒板の上の辺と、ねじれの位置にある教室の辺はどれか。", expect="床と反対側の壁の境目の縦の辺など、平行でも交わってもいない辺。")]),
        definition("df2", "回転体と投影図",
                   "1つの平面図形を、その平面上の直線 $\\ell$ を軸として1回転させてできる立体を回転体という。$\\ell$ を回転の軸、側面をつくる線分を母線という。また、立体を正面から見た図を立面図、真上から見た図を平面図といい、これらを組にして表したものを投影図という。",
                   conditions=["長方形を1辺を軸として回転 → 円柱。直角三角形を直角をはさむ1辺を軸として回転 → 円錐。半円を直径を軸として回転 → 球。",
                               "回転体を回転の軸をふくむ平面で切ると、切り口は軸について線対称な図形になる。回転の軸に垂直な平面で切ると、切り口は円になる。"],
                   points=[tp("厚紙の長方形・直角三角形に竹ぐしをつけて回転させ、円柱・円錐ができることを実際に見せる。")]),
        theorem("th1", "体積の公式",
                "$$\\text{柱体：}V=Sh\\qquad \\text{錐体：}V=\\dfrac{1}{3}Sh\\qquad \\text{球：}V=\\dfrac{4}{3}\\pi r^3$$",
                ["$S$：底面積、$h$：高さ、$r$：半径", "円柱は $V=\\pi r^2h$、円錐は $V=\\dfrac{1}{3}\\pi r^2h$。", "円錐の高さは、頂点から底面に垂直にひいた線分の長さであり、母線の長さではない。"],
                body="角錐・円錐の体積が、底面が合同で高さが等しい角柱・円柱の体積の $\\dfrac{1}{3}$ になることは、水や砂を使った実験で確かめられる。球の体積は、球がちょうど入る円柱の体積の $\\dfrac{2}{3}$ になる。",
                points=[tp("円錐の容器に水を入れて同じ底面・高さの円柱に移し、ちょうど3杯で満たされることを演示する。", ask="何杯でいっぱいになると思うか。", expect="2杯、3杯などの予想が出る。実際は3杯。", timing="体積の導入")]),
        derivation("dv1", "円錐の展開図と側面積を導く",
                   ["底面の半径を $r$、母線の長さを $\\ell$ とする。円錐の展開図で、側面は半径 $\\ell$ のおうぎ形になる。",
                    "おうぎ形の弧の長さは、底面の円周に等しいので $2\\pi r$。",
                    "おうぎ形は半径 $\\ell$ の円の $\\dfrac{2\\pi r}{2\\pi\\ell}=\\dfrac{r}{\\ell}$ にあたるので、中心角は $360^\\circ\\times\\dfrac{r}{\\ell}$。",
                    "側面積は $\\pi\\ell^2\\times\\dfrac{r}{\\ell}=\\pi r\\ell$。（平面図形の単元の $S=\\dfrac{1}{2}\\times\\text{弧}\\times\\text{半径}=\\dfrac{1}{2}\\times2\\pi r\\times\\ell$ からも同じ結果になる。）",
                    "表面積 $=$ 側面積 $+$ 底面積 $=\\pi r\\ell+\\pi r^2$。"],
                   points=[tp("「おうぎ形の弧＝底面の円周」という対応を、展開図を組み立てて確認させる。", ask="側面のおうぎ形の弧は、組み立てるとどこになるか。", expect="底面の円のまわり。"),
                           tp("中心角は $360^\\circ\\times\\dfrac{r}{\\ell}$（半径の比）で求められることを強調する。", caution="$\\dfrac{\\ell}{r}$ と逆にする誤りが多い。答えが $360^\\circ$ をこえたら見直す。")]),
        theorem("th2", "表面積",
                "$$\\text{表面積}=\\text{側面積}+\\text{底面積（すべての底面）}$$",
                ["角柱・円柱：側面積は（底面の周の長さ）×（高さ）、底面は2つ。", "円錐：側面積 $\\pi r\\ell$、底面は1つ。", "球：表面積 $S=4\\pi r^2$。"],
                points=[tp("展開図をかかせてから表面積を求めさせると、底面の数え忘れが減る。")]),
        example("ex1", "例題1　ねじれの位置",
                "直方体 ABCD−EFGH で、辺 AB とねじれの位置にある辺をすべて答えなさい。",
                ["辺 AB と平行な辺：DC、EF、HG。", "辺 AB と交わる辺：AD、BC、AE、BF。", "残りの辺 CG、DH、EH、FG がねじれの位置にある。"],
                "辺 CG、DH、EH、FG",
                thinking="12本の辺を「平行」「交わる」に分けると、残りがねじれの位置になる。",
                figure=solid_fig("直方体 ABCD−EFGH"),
                points=[tp("辺を3つのグループに分ける表をつくり、合計が11本（AB 以外）になることを確認させる。")],
                misconceptions=[("辺 CD はねじれの位置にある", "CD は AB と平行（面 ABCD 上にある）")]),
        example("ex2", "例題2　円錐の展開図と表面積",
                "底面の半径が $3$ cm、母線の長さが $8$ cm の円錐の、側面のおうぎ形の中心角と、表面積を求めなさい。ただし、円周率は $\\pi$ とする。",
                ["中心角 $=360^\\circ\\times\\dfrac{3}{8}=135^\\circ$。", "側面積 $=\\pi\\times3\\times8=24\\pi$（cm²）。", "底面積 $=\\pi\\times3^2=9\\pi$（cm²）。", "表面積 $=24\\pi+9\\pi=33\\pi$（cm²）。"],
                "中心角 $135^\\circ$、表面積 $33\\pi$ cm²",
                thinking="側面のおうぎ形の弧の長さは底面の円周と等しい。",
                points=[tp("側面積をおうぎ形の公式（$\\pi\\ell^2\\times\\dfrac{a}{360}$）でも計算させ、$\\pi r\\ell$ と一致することを確かめさせる。")]),
        example("ex3", "例題3　回転体の体積",
                "直角をはさむ2辺の長さが $4$ cm、$6$ cm の直角三角形を、長さ $6$ cm の辺を軸として1回転させてできる立体の体積を求めなさい。ただし、円周率は $\\pi$ とする。",
                ["できる立体は、底面の半径 $4$ cm、高さ $6$ cm の円錐。", "$V=\\dfrac{1}{3}\\times\\pi\\times4^2\\times6=32\\pi$（cm³）。"],
                "$32\\pi$ cm³",
                thinking="軸になる辺が高さ、軸に垂直な辺が底面の半径になる。",
                points=[tp("どちらの辺を軸にするかで体積が変わることを、軸を入れかえた場合と比べさせる。", ask="長さ 4 cm の辺を軸にすると体積はどうなるか。", expect="$\\dfrac{1}{3}\\pi\\times6^2\\times4=48\\pi$ cm³ で、大きくなる。")]),
        board("bd1", "板書案",
              [("① 位置関係", ["2直線：交わる／平行／ねじれ", "ねじれ＝平行でなく交わらない", "直方体の AB：平行3・交わる4・ねじれ4", "直線と平面の垂直"]),
               ("② 立体の見方", ["回転体：長方形→円柱", "直角三角形→円錐、半円→球", "投影図＝立面図＋平面図", "多面体・正多面体（5種類）"]),
               ("③ 体積・表面積", ["柱体 $V=Sh$、錐体 $V=\\dfrac{1}{3}Sh$", "球 $V=\\dfrac{4}{3}\\pi r^3$、$S=4\\pi r^2$", "円錐：中心角 $360^\\circ\\times\\dfrac{r}{\\ell}$", "側面積 $\\pi r\\ell$"])],
              points=[tp("③の円錐の公式は、展開図の図と並べて板書し、弧と円周の対応を矢印で示す。")]),
        guide("gd1", "指導ガイド（口頭で補う要点）",
              [tp("ねじれの位置の判定では、まず「平行」「交わる（延長して交わるものもふくむ）」を除き、残りをねじれとする手順を徹底する。", caution="辺の延長が交わる場合（四角錐の辺など）を見落としやすい。"),
               tp("錐体の体積では $\\dfrac{1}{3}$ を、表面積では底面の数を、毎回声に出して確認させる。"),
               tp("円錐の体積で母線の長さを高さに使う誤りが多い。高さは底面に垂直な線分であることを図で示す。", ask="円錐の高さと母線はどう違うか。", expect="高さは頂点から底面への垂線、母線は頂点と底面の円周上の点を結ぶ線分。"),
               tp("回転体の問題では、回転の軸の位置を確認させ、見取図をかかせてから計算させる。", timing="回転体の演習前")],
              misconceptions=[("円錐の体積を $\\pi r^2h$ とする", "錐体は $\\dfrac{1}{3}\\pi r^2h$"),
                              ("円錐の側面のおうぎ形の中心角を $360^\\circ\\times\\dfrac{\\ell}{r}$ とする", "$360^\\circ\\times\\dfrac{r}{\\ell}$（底面の半径÷母線）"),
                              ("交わらない2直線はすべて平行である", "空間では、交わらず平行でもない「ねじれの位置」がある")]),
        summary("sm1", "まとめ",
                ["空間の2直線：交わる・平行・ねじれの位置。", "回転体と投影図で立体をとらえる。",
                 "柱体 $V=Sh$、錐体 $V=\\dfrac{1}{3}Sh$、球 $V=\\dfrac{4}{3}\\pi r^3$、$S=4\\pi r^2$。", "円錐の側面：中心角 $360^\\circ\\times\\dfrac{r}{\\ell}$、側面積 $\\pi r\\ell$。"]),
        check("ck1", "確認問題",
              [("三角柱 ABC−DEF で、辺 AB とねじれの位置にある辺をすべて答えなさい。", "辺 CF、DF、EF"),
               ("半径 $3$ cm の球の表面積を求めなさい。", "$4\\pi\\times3^2=36\\pi$ cm²"),
               ("底面の半径 $2$ cm、高さ $6$ cm の円錐の体積を求めなさい。", "$\\dfrac{1}{3}\\pi\\times2^2\\times6=8\\pi$ cm³")]),
    ])


# ======================================================================
# A 基本確認
# ======================================================================

REL_WORD = {"平行": "平行な", "交わる": "交わる", "ねじれ": "ねじれの位置にある"}
FACE_WORD = {"平行": "平行な", "垂直": "垂直な"}


@gen("basic_check", 5, ["condition_check", "concept"])
def a_relation(r):
    name = r.choice(list(SOLIDS))
    S = SOLIDS[name]
    kind = r.choice(["edge", "edge", "face"] if not name.startswith("四角錐") else ["edge"])
    e = r.choice(S["E"])
    if kind == "edge":
        rel = r.choice(["平行", "交わる", "ねじれ"])
        hits = [f for f in S["E"] if f != e and edge_rel(S, e, f) == rel]
        if not hits and rel == "平行":
            rel = "ねじれ"
            hits = [f for f in S["E"] if f != e and edge_rel(S, e, f) == rel]
        groups = {k: [f for f in S["E"] if f != e and edge_rel(S, e, f) == k] for k in ("平行", "交わる", "ねじれ")}
        stem = f"右の図の{name}で，辺 {e} と{REL_WORD[rel]}辺は何本あるか求めなさい。"
        st = [f"辺 {e} と平行な辺：{'，'.join(groups['平行']) or 'なし'}。", f"辺 {e} と交わる辺：{'，'.join(groups['交わる'])}。", f"残りがねじれの位置にある辺：{'，'.join(groups['ねじれ']) or 'なし'}。"]
        e_txt = f"辺 {e} と{REL_WORD[rel]}辺は {'，'.join(hits)} の {len(hits)} 本。"
        pit = ["延長すると交わる辺（同じ平面上にある辺）をねじれの位置と数えてしまう。", "平行な辺を数えもらす。"]
    else:
        rel = r.choice(["平行", "垂直"])
        hits = [f for f in S["F"] if edge_face(S, e, f) == rel]
        if not hits:
            rel = "垂直" if rel == "平行" else "平行"
            hits = [f for f in S["F"] if edge_face(S, e, f) == rel]
        stem = f"右の図の{name}で，辺 {e} と{FACE_WORD[rel]}面は何個あるか求めなさい。"
        st = ["それぞれの面について，辺がその面に含まれるか・交わるか・平行かを調べる。", f"辺 {e} と{FACE_WORD[rel]}面：{'，'.join('面 ' + f for f in hits)}。"]
        e_txt = f"辺 {e} と{FACE_WORD[rel]}面は {'，'.join('面 ' + f for f in hits)} の {len(hits)} 個。"
        pit = ["辺を含む面を「平行な面」と数えてしまう。"]
    return MARK(stem, len(hits), e_txt, f"{len(hits)}", d=2, fig=solid_fig(name),
                ap="すべての辺（面）を「平行」「交わる」などのグループに分けて数える。ねじれの位置は「平行でなく，交わらない」ものである。",
                steps=st, alt=["見取図の辺に印をつけながら，グループごとの本数の合計がもれなく全体の数になるかを確かめる。"],
                pc=[("位置関係を正しく判断している", 1), ("正しい数を答えている", 1)], pit=pit)


@gen("basic_check", 5, ["computation"])
def a_volume(r):
    kind = r.choice(["prism", "pyramid", "cylinder", "cone"])
    if kind == "prism":
        a, b, h = r.randint(2, 9), r.randint(2, 9), r.randint(2, 12)
        tri = r.choice([True, False])
        S = Fr(a * b, 2) if tri else Fr(a * b)
        if tri and S.denominator != 1:
            a += 1
            S = Fr(a * b, 2)
        base = f"直角をはさむ2辺が ${a}$ cm，${b}$ cm の直角三角形" if tri else f"縦 ${a}$ cm，横 ${b}$ cm の長方形"
        V = S * h
        return MARK(f"底面が{base}で，高さが ${h}$ cm の角柱の体積は何 cm³ か求めなさい。", V,
                    f"底面積 ${ftex(S)}$ cm²，体積 $={ftex(S)}\\times{h}={ftex(V)}$（cm³）。", f"{fpy(S)}*{h}", d=1,
                    ap="角柱の体積は（底面積）×（高さ）。まず底面積を求める。",
                    steps=[f"底面積：{'$\\dfrac{1}{2}\\times' + str(a) + '\\times' + str(b) + '$' if tri else '$' + str(a) + '\\times' + str(b) + '$'}$={ftex(S)}$。", f"体積：${ftex(S)}\\times{h}={ftex(V)}$。"],
                    alt=["同じ底面の直方体の体積を考え，三角柱ならその半分として確かめる。" if tri else "1 cm³ の立方体が何個並ぶかを考えて確かめる。"],
                    pc=[("底面積を正しく求めている", 1), ("体積を正しく求めている", 1)],
                    pit=["三角形の面積で $\\dfrac{1}{2}$ をかけ忘れる。"])
    if kind == "pyramid":
        a = r.randint(2, 9)
        h = r.choice([x for x in range(3, 16) if (a * a * x) % 3 == 0])
        V = Fr(a * a * h, 3)
        return MARK(f"底面が1辺 ${a}$ cm の正方形で，高さが ${h}$ cm の正四角錐の体積は何 cm³ か求めなさい。", V,
                    f"$\\dfrac{{1}}{{3}}\\times{a}^2\\times{h}={ftex(V)}$（cm³）。", f"Rational(1,3)*{a}**2*{h}", d=1,
                    ap="角錐の体積は $\\dfrac{1}{3}\\times$（底面積）×（高さ）。",
                    steps=[f"底面積：${a}^2={a * a}$。", f"体積：$\\dfrac{{1}}{{3}}\\times{a * a}\\times{h}={ftex(V)}$。"],
                    alt=[f"底面と高さが同じ四角柱の体積 ${a * a * h}$ cm³ の $\\dfrac{{1}}{{3}}$ と考えてもよい。"],
                    pc=[("錐体の公式を使っている", 1), ("正しく計算している", 1)],
                    pit=["$\\dfrac{1}{3}$ をかけ忘れる。"])
    rad = r.randint(2, 9)
    h = r.choice([x for x in range(2, 13) if x != rad])
    if kind == "cylinder":
        V = Fr(rad * rad * h)
        right = cmu(V, "cm³")
        cands = [(cmu(Fr(rad * rad * h, 3), "cm³"), "円柱なのに錐体の公式（$\\dfrac{1}{3}$ をかける）を使っている。", "柱体と錐体の公式の混同"),
                 (cmu(4 * rad * rad * h, "cm³"), "半径の代わりに直径を使っている。", "半径と直径の混同"),
                 (cmu(2 * rad * h, "cm³"), "底面積の代わりに円周 $2\\pi r$ を使っている。", "円周と面積の混同"),
                 (cmu(rad * h * h, "cm³"), "半径と高さを取り違えている。", "半径と高さの混同")]
        e = f"$\\pi\\times{rad}^2\\times{h}={pitex(V)}$（cm³）。"
        nm = "円柱"
        expr, exp = f"pi*{rad}**2*{h}", f"{fpy(V)}*pi"
    else:
        V = Fr(rad * rad * h, 3)
        right = cmu(V, "cm³")
        cands = [(cmu(rad * rad * h, "cm³"), "$\\dfrac{1}{3}$ をかけ忘れている。円錐は錐体である。", "柱体と錐体の公式の混同"),
                 (cmu(Fr(4 * rad * rad * h, 3), "cm³"), "半径の代わりに直径を使っている。", "半径と直径の混同"),
                 (cmu(Fr(2 * rad * h, 3), "cm³"), "底面積の代わりに円周 $2\\pi r$ を使っている。", "円周と面積の混同"),
                 (cmu(Fr(rad * h * h, 3), "cm³"), "半径と高さを取り違えている。", "半径と高さの混同")]
        e = f"$\\dfrac{{1}}{{3}}\\times\\pi\\times{rad}^2\\times{h}={pitex(V)}$（cm³）。"
        nm = "円錐"
        expr, exp = f"pi*{rad}**2*{h}/3", f"{fpy(V)}*pi"
    return MC(f"底面の半径が ${rad}$ cm，高さが ${h}$ cm の{nm}の体積として正しいものを，" + SEL4 + PI, right, cands, e, d=1,
              ap=f"{nm}は{'柱体' if nm == '円柱' else '錐体'}なので，体積は {'（底面積）×（高さ）' if nm == '円柱' else '$\\dfrac{1}{3}\\times$（底面積）×（高さ）'}。",
              steps=[f"底面積：$\\pi\\times{rad}^2={rad * rad}\\pi$。", e],
              alt=["底面積と高さを先に書き出し，公式に当てはめる前に何をかけるかを確認する。"],
              pc=[("公式を正しく選んでいる", 1), ("正しい値を選んでいる", 1)],
              pit=["円錐で $\\dfrac{1}{3}$ をかけ忘れる。", "半径と直径を取り違える。"],
              chk=(expr, exp, None, "intermediate"))


ROT = [
    ("長方形を，その1辺を軸として1回転させる", "円柱"),
    ("直角三角形を，直角をはさむ1辺を軸として1回転させる", "円錐"),
    ("半円を，その直径を軸として1回転させる", "球"),
    ("直角三角形を，斜辺を軸として1回転させる", "2つの円錐を底面で合わせた立体"),
    ("上底と下底に垂直な辺をもつ台形を，その辺を軸として1回転させる", "円錐から，頂点をふくむ小さい円錐を切り取った立体"),
    ("長方形を，1辺と平行で長方形から離れた直線を軸として1回転させる", "円柱から，中心部分の円柱をくりぬいた立体"),
]
ROT_DESC = {"円柱": "円柱は長方形を1辺を軸として回転させてできる。", "円錐": "円錐は直角三角形を直角をはさむ1辺を軸として回転させてできる。",
            "球": "球は半円を直径を軸として回転させてできる。", "2つの円錐を底面で合わせた立体": "直角三角形を斜辺を軸として回転させたときにできる立体である。",
            "円錐から，頂点をふくむ小さい円錐を切り取った立体": "台形を回転させたときにできる立体である。", "円柱から，中心部分の円柱をくりぬいた立体": "長方形を離れた軸のまわりに回転させたときにできる立体である。",
            "三角柱": "三角柱は回転体ではない（側面が平面）。", "四角錐": "四角錐は回転体ではない。"}


@gen("basic_check", 5, ["concept"])
def a_rotation(r):
    i = r.randrange(len(ROT))
    fig_txt, solid = ROT[i]
    rev = r.choice([False, True])
    if not rev:
        others = [ROT[(i + k) % len(ROT)][1] for k in (1, 2, 3)]
        if i < 3:
            others = [x for x in ["円柱", "円錐", "球", "三角柱", "四角錐"] if x != solid][:3]
        return MC(f"{fig_txt}と，どんな立体ができるか。最も適するものを，" + SEL4, solid,
                  [(o, ROT_DESC.get(o, "") or "この問題の図形の回転ではできない。", "回転体の形のとらえ違い") for o in others],
                  f"{fig_txt}と，{solid}ができる。", d=1,
                  ap="回転の軸からの距離が一定の部分は円柱の側面，軸に近づく斜めの辺は円錐の側面になる。見取図をかいて考える。",
                  steps=["回転の軸を決め，図形の各辺が回転してできる面を考える。", "軸に平行な辺 → 円柱の側面，斜めの辺 → 円錐の側面，半円の弧 → 球面。", f"答えは{solid}。"],
                  alt=["厚紙で図形をつくり，軸のまわりに回して確かめる。"],
                  pc=[("回転の軸と図形の位置関係をとらえている", 1), ("正しい立体を選んでいる", 1)],
                  pit=["軸の位置を変えるとできる立体が変わることを見落とす。"])
    others = [ROT[(i + k) % len(ROT)][0] for k in (1, 2, 3)]
    return MC(f"{solid}は，どのような平面図形を1回転させてできる回転体か。最も適するものを，" + SEL4, fig_txt,
              [(o, f"この回転では{dict((a, b) for a, b in ROT)[o]}ができる。", "回転体の形のとらえ違い") for o in others],
              f"{solid}は，{fig_txt}とできる。", d=2,
              ap="立体を回転の軸をふくむ平面で切った切り口の半分が，回転させた平面図形になる。",
              steps=["立体の回転の軸を考える。", "軸をふくむ平面で切った切り口を考え，軸の片側の部分を取り出す。", f"その図形は「{fig_txt}」の図形。"],
              alt=["選択肢の図形をそれぞれ回転させた立体を見取図にかいて比べる。"],
              pc=[("切り口の形から元の図形を考えている", 1), ("正しいものを選んでいる", 1)],
              pit=["回転の軸がどこにあるかを考えずに選ぶ。"])


POLY = [("正四面体", 4, 4, 6, 3, "正三角形"), ("正六面体", 6, 8, 12, 3, "正方形"), ("正八面体", 8, 6, 12, 4, "正三角形"),
        ("正十二面体", 12, 20, 30, 3, "正五角形"), ("正二十面体", 20, 12, 30, 5, "正三角形")]


@gen("basic_check", 5, ["concept", "computation"])
def a_polyhedra(r):
    name, F, V, E, k, face = r.choice(POLY)
    what = r.choice(["頂点", "辺", "1つの頂点に集まる面", "面"])
    if what == "面" and r.random() < 0.6:
        what = "辺"
    val = {"頂点": V, "辺": E, "1つの頂点に集まる面": k, "面": F}[what]
    unit = "本" if what == "辺" else "個"
    how = {"頂点": f"{face}が {F} 個あり，頂点は全部で $3$ 以上の面で共有される。{face}の頂点の数の合計 ${F}\\times{len(face) and {'正三角形': 3, '正方形': 4, '正五角形': 5}[face]}={F * {'正三角形': 3, '正方形': 4, '正五角形': 5}[face]}$ を，1つの頂点に集まる面の数 ${k}$ でわって ${V}$",
           "辺": f"{face}の辺の数の合計 ${F}\\times{ {'正三角形': 3, '正方形': 4, '正五角形': 5}[face]}={F * {'正三角形': 3, '正方形': 4, '正五角形': 5}[face]}$ を，1本の辺を共有する面の数 $2$ でわって ${E}$",
           "1つの頂点に集まる面": f"{name}は，どの頂点にも{face}が ${k}$ 個ずつ集まっている",
           "面": f"{name}は，名前のとおり面が ${F}$ 個ある"}[what]
    n = {"正三角形": 3, "正方形": 4, "正五角形": 5}[face]
    expr = {"頂点": f"{F}*{n}/{k}", "辺": f"{F}*{n}/2", "1つの頂点に集まる面": str(k), "面": str(F)}[what]
    return MARK(f"{name}の{what}の数は何{unit}か求めなさい。", val, f"{how}。", expr, d=2,
                ap="正多面体は，すべての面が合同な正多角形で，どの頂点にも同じ数の面が集まっている。面の数と面の形から，辺や頂点の数を計算できる。",
                steps=[f"{name}の面は{face}で ${F}$ 個。", f"1つの頂点に集まる面は ${k}$ 個。", f"{what}の数：{how}。"],
                alt=["オイラーの多面体定理（頂点の数 − 辺の数 + 面の数 $=2$）で確かめることもできる：" + f"${V}-{E}+{F}=2$。"],
                pc=[("正多面体の面の形と数を正しくとらえている", 1), ("正しい数を求めている", 1)],
                pit=["辺や頂点を，面ごとに数えたまま重複を除かない。", "正八面体と正六面体の頂点の数を取り違える。"])


# ======================================================================
# B 標準演習
# ======================================================================

@gen("standard_practice", 4, ["computation", "cross_unit"], rel=["JH-MATH-G1-U05"])
def b_cone(r):
    rad = r.randint(1, 9)
    L = r.choice([x for x in range(rad + 1, 19) if (360 * rad) % x == 0])
    kind = r.choice(["angle", "lateral", "total"])
    ang = Fr(360 * rad, L)
    if kind == "angle":
        return MARK(f"Kさんは，底面の半径が ${rad}$ cm，母線の長さが ${L}$ cm の円錐の展開図をかいた。側面になるおうぎ形の中心角の大きさを求めなさい。", ang,
                    f"おうぎ形の弧の長さは底面の円周 ${2 * rad}\\pi$ cm に等しい。半径 ${L}$ cm の円周 ${2 * L}\\pi$ cm に対する割合は $\\dfrac{{{rad}}}{{{L}}}$ なので，中心角は $360\\times\\dfrac{{{rad}}}{{{L}}}={ftex(ang)}^\\circ$。",
                    f"360*Rational({rad},{L})", d=3, p=4, unit="度",
                    ap="側面のおうぎ形の弧の長さ＝底面の円周。おうぎ形の弧の長さは中心角に比例する（平面図形の単元とのつながり）。",
                    steps=[f"弧の長さ＝底面の円周：$2\\pi\\times{rad}={2 * rad}\\pi$。", f"半径 ${L}$ の円の円周：${2 * L}\\pi$。", f"割合 $\\dfrac{{{2 * rad}\\pi}}{{{2 * L}\\pi}}={ftex(Fr(rad, L))}$，中心角 $360\\times{ftex(Fr(rad, L))}={ftex(ang)}^\\circ$。"],
                    alt=[f"中心角を $a^\\circ$ として $2\\pi\\times{L}\\times\\dfrac{{a}}{{360}}=2\\pi\\times{rad}$ の方程式を解いてもよい。"],
                    pc=[("弧の長さと底面の円周が等しいことを使っている", 2), ("中心角を正しく求めている", 2)],
                    pit=["割合を $\\dfrac{\\ell}{r}$ と逆にする（答えが $360^\\circ$ をこえる）。"])
    lat = Fr(rad * L)
    if kind == "lateral":
        right = cmu(lat, "cm²")
        cands = [(cmu(lat + rad * rad, "cm²"), "底面積までふくめた表面積を答えている。", "側面積と表面積の混同"),
                 (cmu(2 * rad * L, "cm²"), "側面積を $2\\pi r\\ell$ としている。$\\dfrac{1}{2}\\times2\\pi r\\times\\ell=\\pi r\\ell$ である。", "おうぎ形の面積の公式の誤り"),
                 (cmu(L * L, "cm²"), "半径 $\\ell$ の円全体の面積を答えている。側面は円の一部（おうぎ形）である。", "割合のかけ忘れ"),
                 (cmu(rad * rad, "cm²"), "底面積を答えている。", "求める面の取り違え")]
        stem = f"底面の半径が ${rad}$ cm，母線の長さが ${L}$ cm の円錐の側面積として正しいものを，" + SEL4 + PI
        e = f"側面積 $=\\pi r\\ell=\\pi\\times{rad}\\times{L}={pitex(lat)}$（cm²）。"
        expr, exp = f"pi*{rad}*{L}", f"{rad * L}*pi"
    else:
        tot = lat + rad * rad
        right = cmu(tot, "cm²")
        cands = [(cmu(lat, "cm²"), "底面積を加え忘れている。", "底面の数え忘れ"),
                 (cmu(lat + 2 * rad * rad, "cm²"), "底面を2つ加えている。円錐の底面は1つである。", "柱体と錐体の混同"),
                 (cmu(2 * rad * L + rad * rad, "cm²"), "側面積を $2\\pi r\\ell$ としている。", "おうぎ形の面積の公式の誤り"),
                 (cmu(L * L + rad * rad, "cm²"), "側面を半径 $\\ell$ の円全体としている。", "割合のかけ忘れ")]
        stem = f"底面の半径が ${rad}$ cm，母線の長さが ${L}$ cm の円錐の表面積として正しいものを，" + SEL4 + PI
        e = f"側面積 ${pitex(lat)}$ と底面積 ${pitex(rad * rad)}$ の和で ${pitex(tot)}$（cm²）。"
        expr, exp = f"pi*{rad}*{L}+pi*{rad}**2", f"{fpy(tot)}*pi"
    return MC(stem, right, cands, e, d=3, p=4,
              ap="側面は半径 $\\ell$（母線）のおうぎ形で，その弧の長さは底面の円周 $2\\pi r$ に等しい。おうぎ形の面積 $S=\\dfrac{1}{2}\\times$ 弧 $\\times$ 半径（平面図形の単元）を使う。",
              steps=[f"側面のおうぎ形：弧 ${2 * rad}\\pi$，半径 ${L}$。", f"側面積 $=\\dfrac{{1}}{{2}}\\times{2 * rad}\\pi\\times{L}={pitex(lat)}$。", e],
              alt=[f"中心角 ${ftex(ang)}^\\circ$ を求め，$\\pi\\times{L}^2\\times\\dfrac{{{ftex(ang)}}}{{360}}$ で側面積を計算しても同じ。"],
              pc=[("側面のおうぎ形の弧と底面の円周の関係を使っている", 2), ("正しい値を選んでいる", 2)],
              pit=["底面積の加え忘れ。", "側面積を $2\\pi r\\ell$ とする。"],
              chk=(expr, exp, None, "intermediate"))


@gen("standard_practice", 4, ["computation", "condition_check"])
def b_sphere(r):
    kind = r.choice(["V", "S", "half"])
    if kind == "V":
        rad = r.choice([3, 6, 9, 2, 4, 5, 1, 12])
        V = Fr(4 * rad ** 3, 3)
        right = cmu(V, "cm³")
        cands = [(cmu(4 * rad * rad, "cm³"), "表面積の式 $4\\pi r^2$ を使っている。", "体積と表面積の公式の混同"),
                 (cmu(4 * rad ** 3, "cm³"), "$\\dfrac{4}{3}$ ではなく $4$ をかけている。", "公式の係数の誤り"),
                 (cmu(Fr(32 * rad ** 3, 3), "cm³"), "半径の代わりに直径を使っている。", "半径と直径の混同"),
                 (cmu(Fr(2 * rad ** 3, 3), "cm³"), "半球の体積を答えている。", "球と半球の混同")]
        stem = f"半径 ${rad}$ cm の球の体積として正しいものを，" + SEL4 + PI
        e = f"$\\dfrac{{4}}{{3}}\\pi\\times{rad}^3={pitex(V)}$（cm³）。"
        expr, exp = f"Rational(4,3)*pi*{rad}**3", f"{fpy(V)}*pi"
    elif kind == "S":
        rad = r.randint(1, 12)
        S = Fr(4 * rad * rad)
        right = cmu(S, "cm²")
        cands = [(cmu(Fr(4 * rad ** 3, 3), "cm²"), "体積の式を使っている。", "体積と表面積の公式の混同"),
                 (cmu(rad * rad, "cm²"), "半径 $r$ の円の面積を答えている。球の表面積はその4倍。", "公式の係数の誤り"),
                 (cmu(16 * rad * rad, "cm²"), "半径の代わりに直径を使っている。", "半径と直径の混同"),
                 (cmu(2 * rad * rad, "cm²"), "半球の曲面の面積を答えている。", "球と半球の混同")]
        stem = f"半径 ${rad}$ cm の球の表面積として正しいものを，" + SEL4 + PI
        e = f"$4\\pi\\times{rad}^2={pitex(S)}$（cm²）。"
        expr, exp = f"4*pi*{rad}**2", f"{fpy(S)}*pi"
    else:
        rad = r.randint(1, 12)
        S = Fr(3 * rad * rad)
        right = cmu(S, "cm²")
        cands = [(cmu(2 * rad * rad, "cm²"), "曲面の部分だけで，切り口の円の面積を加え忘れている。", "切り口の面の見落とし"),
                 (cmu(4 * rad * rad, "cm²"), "球全体の表面積を答えている。", "球と半球の混同"),
                 (cmu(5 * rad * rad, "cm²"), "球全体の表面積に切り口の円を加えている。", "球と半球の混同"),
                 (cmu(rad * rad, "cm²"), "切り口の円の面積だけを答えている。", "曲面の見落とし")]
        stem = f"半径 ${rad}$ cm の球を，中心を通る平面で切ってできる半球の表面積として正しいものを，" + SEL4 + PI
        e = f"曲面 $\\dfrac{{1}}{{2}}\\times4\\pi\\times{rad}^2={pitex(2 * rad * rad)}$ と切り口の円 ${pitex(rad * rad)}$ の和で ${pitex(S)}$（cm²）。"
        expr, exp = f"2*pi*{rad}**2+pi*{rad}**2", f"{fpy(S)}*pi"
    return MC(stem, right, cands, e, d=3, p=4,
              ap="球の体積は $\\dfrac{4}{3}\\pi r^3$，表面積は $4\\pi r^2$。半球では切り口の円の面も表面にふくまれることに注意する。",
              steps=["何を求めるか（体積か表面積か，球か半球か）を確認する。", "公式に半径を代入する。", e],
              alt=["体積は「球がちょうど入る円柱の $\\dfrac{2}{3}$」，表面積は「半径 $r$ の円の面積の4倍」と考えて確かめる。"],
              pc=[("適切な公式を選んでいる", 2), ("正しい値を選んでいる", 2)],
              pit=["半球の表面積で切り口の円を加え忘れる。", "$r^3$ と $r^2$ を取り違える。"],
              chk=(expr, exp, None, "intermediate"))


@gen("standard_practice", 4, ["application", "computation"])
def b_rot_volume(r):
    kind = r.choice(["rect", "tri"])
    a, b = r.sample(range(2, 10), 2)
    if kind == "rect":
        V = Fr(b * b * a)
        right = cmu(V, "cm³")
        cands = [(cmu(a * a * b, "cm³"), "回転の軸を取り違え，半径と高さを逆にしている。", "回転の軸の取り違え"),
                 (cmu(Fr(b * b * a, 3), "cm³"), "円柱なのに $\\dfrac{1}{3}$ をかけている。", "柱体と錐体の混同"),
                 (cmu(4 * b * b * a, "cm³"), "軸から辺までの距離（半径）を2倍にしている。", "半径と直径の混同"),
                 (cmu(2 * a * b, "cm³"), "底面積の代わりに長方形の面積の2倍を使っている。", "回転体の体積のとらえ違い")]
        stem = f"縦 ${a}$ cm，横 ${b}$ cm の長方形を，縦の辺を軸として1回転させてできる立体の体積として正しいものを，" + SEL4 + PI
        e = f"底面の半径 ${b}$ cm，高さ ${a}$ cm の円柱ができる。$\\pi\\times{b}^2\\times{a}={pitex(V)}$（cm³）。"
        expr, exp = f"pi*{b}**2*{a}", f"{fpy(V)}*pi"
        solid = "円柱"
    else:
        V = Fr(b * b * a, 3)
        right = cmu(V, "cm³")
        cands = [(cmu(Fr(a * a * b, 3), "cm³"), "回転の軸を取り違え，半径と高さを逆にしている。", "回転の軸の取り違え"),
                 (cmu(b * b * a, "cm³"), "$\\dfrac{1}{3}$ をかけ忘れている（円柱の体積になっている）。", "柱体と錐体の混同"),
                 (cmu(Fr(4 * b * b * a, 3), "cm³"), "半径を2倍にしている。", "半径と直径の混同"),
                 (cmu(Fr(a * b, 2), "cm³"), "三角形の面積に $\\pi$ をかけただけである。", "回転体の体積のとらえ違い")]
        stem = f"直角をはさむ2辺の長さが ${a}$ cm，${b}$ cm の直角三角形を，長さ ${a}$ cm の辺を軸として1回転させてできる立体の体積として正しいものを，" + SEL4 + PI
        e = f"底面の半径 ${b}$ cm，高さ ${a}$ cm の円錐ができる。$\\dfrac{{1}}{{3}}\\times\\pi\\times{b}^2\\times{a}={pitex(V)}$（cm³）。"
        expr, exp = f"pi*{b}**2*{a}/3", f"{fpy(V)}*pi"
        solid = "円錐"
    return MC(stem, right, cands, e, d=3, p=4,
              ap="回転の軸になる辺が高さ，軸に垂直な辺が底面の半径になる。見取図をかいてから公式に当てはめる。",
              steps=[f"できる立体は{solid}。", f"高さ（軸の辺）${a}$ cm，底面の半径 ${b}$ cm。", e],
              alt=[f"軸を入れかえた場合の体積も計算して比べると，半径の2乗が効くので結果が大きく変わることがわかる。"],
              pc=[("できる立体と半径・高さを正しくとらえている", 2), ("正しい体積を選んでいる", 2)],
              pit=["軸の辺を半径と取り違える。"],
              chk=(expr, exp, None, "intermediate"))


PROJ = [("長方形", "円", "円柱"), ("二等辺三角形", "円（中心に点がある）", "円錐"), ("円", "円", "球"),
        ("二等辺三角形", "正方形（対角線がかかれている）", "正四角錐"), ("長方形", "三角形", "三角柱"),
        ("長方形", "正方形", "正四角柱"), ("二等辺三角形", "正三角形（頂点と中心を結ぶ線がかかれている）", "正三角錐")]


@gen("standard_practice", 4, ["concept"])
def b_projection(r):
    i = r.randrange(len(PROJ))
    el, pl, solid = PROJ[i]
    rev = r.choice([False, True])
    if not rev:
        others = [p[2] for p in PROJ if p[2] != solid]
        same_el = [p[2] for p in PROJ if p[0] == el and p[2] != solid]
        cand = same_el + [o for o in others if o not in same_el]
        return MC(f"ある立体を投影図で表したところ，立面図が{el}，平面図が{pl}になった。この立体として最も適するものを，" + SEL4, solid,
                  [(o, f"{o}の投影図は，立面図が{[p for p in PROJ if p[2] == o][0][0]}，平面図が{[p for p in PROJ if p[2] == o][0][1]}になる。", "立面図・平面図の読み取りの誤り") for o in cand],
                  f"立面図が{el}，平面図が{pl}になるのは{solid}。", d=2, p=4,
                  ap="立面図（正面から見た形）と平面図（真上から見た形）の両方に合う立体を考える。どちらか一方だけでは決まらないことが多い。",
                  steps=[f"立面図が{el}になる立体を挙げる。", f"そのうち，平面図が{pl}になるものを選ぶ。", f"答えは{solid}。"],
                  alt=["選択肢の立体をそれぞれ正面と真上から見た形を想像し，見取図にかいて比べる。"],
                  pc=[("立面図から候補をしぼっている", 2), ("平面図と合わせて正しく判断している", 2)],
                  pit=["立面図だけを見て判断し，平面図を確かめない。"])
    others = [p for p in PROJ if p[2] != solid and p[1] != pl]
    return MC(f"{solid}を投影図で表したとき，平面図（真上から見た図）の形として最も適するものを，" + SEL4, pl,
              [(o[1], f"平面図が{o[1]}になるのは{o[2]}である。", "平面図のとらえ違い") for o in others],
              f"{solid}を真上から見ると{pl}に見える。", d=2, p=4,
              ap="真上から見たとき，底面の形や頂点の位置がどう見えるかを考える。",
              steps=[f"{solid}の底面の形を確認する。", "真上から見たとき，側面の辺や頂点がどこに見えるかを考える。", f"平面図は{pl}。"],
              alt=["身のまわりの物（缶・コーンなど）を真上から見て確かめる。"],
              pc=[("立体を真上から見た形をとらえている", 2), ("正しい形を選んでいる", 2)],
              pit=["立面図と平面図を取り違える。"])


@gen("standard_practice", 4, ["computation"])
def b_surface(r):
    kind = r.choice(["box", "tri", "cyl"])
    if kind == "box":
        a, b, c = r.randint(2, 9), r.randint(2, 9), r.randint(2, 12)
        S = 2 * (a * b + b * c + c * a)
        return MARK(f"縦 ${a}$ cm，横 ${b}$ cm，高さ ${c}$ cm の直方体の表面積は何 cm² か求めなさい。", S,
                    f"$2\\times({a}\\times{b}+{b}\\times{c}+{c}\\times{a})={S}$（cm²）。", f"2*({a}*{b}+{b}*{c}+{c}*{a})", d=2, p=4,
                    ap="直方体の面は，合同な長方形が2つずつ3組ある。展開図をかいて面を数える。",
                    steps=[f"3種類の面：${a * b}$，${b * c}$，${c * a}$（cm²）。", f"それぞれ2つずつあるので合計 ${S}$ cm²。"],
                    alt=[f"側面積（底面の周 ${2 * (a + b)}$ × 高さ ${c}$）$={2 * (a + b) * c}$ と底面積 $2\\times{a * b}$ の和としても求められる。"],
                    pc=[("面の種類と数を正しくとらえている", 2), ("表面積を正しく求めている", 2)],
                    pit=["同じ形の面を1つずつしか数えない。"])
    if kind == "tri":
        k = r.randint(1, 3)
        p, q, hyp = 3 * k, 4 * k, 5 * k
        h = r.randint(2, 12)
        base = p * q // 2
        S = 2 * base + (p + q + hyp) * h
        return MARK(f"底面が，3辺の長さが ${p}$ cm，${q}$ cm，${hyp}$ cm で，長さ ${hyp}$ cm の辺に向かい合う角が直角である三角形の三角柱がある。高さが ${h}$ cm のとき，この三角柱の表面積は何 cm² か求めなさい。", S,
                    f"底面積 $\\dfrac{{1}}{{2}}\\times{p}\\times{q}={base}$ が2つ，側面積 $({p}+{q}+{hyp})\\times{h}={(p + q + hyp) * h}$。合計 ${S}$ cm²。",
                    f"2*Rational(1,2)*{p}*{q}+({p}+{q}+{hyp})*{h}", d=3, p=4,
                    ap="角柱の表面積＝側面積＋底面積×2。側面を展開すると，横が底面の周の長さ，縦が高さの長方形になる。",
                    steps=[f"底面は直角をはさむ2辺が ${p}$，${q}$ の直角三角形：面積 ${base}$。", f"側面積：底面の周 ${p + q + hyp}$ × 高さ ${h}$ $={(p + q + hyp) * h}$。", f"表面積：${base}\\times2+{(p + q + hyp) * h}={S}$。"],
                    alt=["側面の3つの長方形の面積を別々に求めて加えてもよい。"],
                    pc=[("側面積を正しく求めている", 2), ("底面2つを加えて表面積を求めている", 2)],
                    pit=["底面の三角形で $\\dfrac{1}{2}$ をかけ忘れる。", "底面を1つしか加えない。"])
    rad, h = r.randint(1, 9), r.randint(2, 12)
    S = Fr(2 * rad * h + 2 * rad * rad)
    right = cmu(S, "cm²")
    cands = [(cmu(2 * rad * h + rad * rad, "cm²"), "底面を1つしか加えていない。円柱の底面は2つある。", "底面の数え落とし"),
             (cmu(2 * rad * h, "cm²"), "側面積だけを答えている。", "底面の加え忘れ"),
             (cmu(rad * rad * h, "cm²"), "体積を答えている。", "体積と表面積の混同"),
             (cmu(rad * h + 2 * rad * rad, "cm²"), "側面の長方形の横の長さを $\\pi r$ としている。正しくは円周 $2\\pi r$。", "円周の公式の誤り")]
    return MC(f"底面の半径が ${rad}$ cm，高さが ${h}$ cm の円柱の表面積として正しいものを，" + SEL4 + PI, right, cands,
              f"側面積 $2\\pi\\times{rad}\\times{h}={pitex(2 * rad * h)}$，底面積 $\\pi\\times{rad}^2\\times2={pitex(2 * rad * rad)}$。合計 ${pitex(S)}$（cm²）。", d=3, p=4,
              ap="円柱の側面を展開すると，横が底面の円周，縦が高さの長方形になる。底面は2つ。",
              steps=[f"側面：横 ${2 * rad}\\pi$，縦 ${h}$ の長方形で ${pitex(2 * rad * h)}$。", f"底面：${pitex(rad * rad)}$ が2つで ${pitex(2 * rad * rad)}$。", f"表面積 ${pitex(S)}$ cm²。"],
              alt=["展開図をかき，各部分の長さを書きこんでから計算する。"],
              pc=[("側面の長方形の横の長さを円周としている", 2), ("底面2つを加えている", 2)],
              pit=["底面を1つしか加えない。"],
              chk=(f"2*pi*{rad}*{h}+2*pi*{rad}**2", f"{fpy(S)}*pi", None, "intermediate"))


# ======================================================================
# C 思考力・記述応用
# ======================================================================

@gen("thinking_writing", 4, ["multiple_solutions", "computation"])
def c_ratio(r):
    kind = r.choice(["cone_cyl", "sphere_cyl", "cube_cut", "free"])
    if kind == "cone_cyl":
        rad, h = r.randint(2, 9), r.randint(2, 12)
        a, b = 1, 3
        stem = f"底面の半径が ${rad}$ cm，高さが ${h}$ cm の円錐 P と，底面の半径が ${rad}$ cm，高さが ${h}$ cm の円柱 Q がある。P と Q の体積の比を最も簡単な整数の比で表しなさい。"
        e = f"P は $\\dfrac{{1}}{{3}}\\pi\\times{rad}^2\\times{h}$，Q は $\\pi\\times{rad}^2\\times{h}$ なので，P：Q $=1:3$。"
        expr = f"(pi*{rad}**2*{h}/3)/(pi*{rad}**2*{h})"
        st = [f"P の体積：${pitex(Fr(rad * rad * h, 3))}$。", f"Q の体積：${pitex(rad * rad * h)}$。", "比：$1:3$。"]
        alt = ["底面と高さが等しい錐体の体積は柱体の $\\dfrac{1}{3}$ であることから，計算しなくても $1:3$ とわかる。"]
    elif kind == "sphere_cyl":
        rad = r.randint(1, 9)
        what = r.choice(["体積", "表面積と円柱の側面積"])
        if what == "体積":
            a, b = 2, 3
            stem = f"半径 ${rad}$ cm の球と，その球がちょうど入る円柱（底面の半径 ${rad}$ cm，高さ ${2 * rad}$ cm）がある。球と円柱の体積の比を最も簡単な整数の比で表しなさい。"
            e = f"球 $\\dfrac{{4}}{{3}}\\pi\\times{rad}^3={pitex(Fr(4 * rad ** 3, 3))}$，円柱 $\\pi\\times{rad}^2\\times{2 * rad}={pitex(2 * rad ** 3)}$ なので $2:3$。"
            expr = f"(Rational(4,3)*pi*{rad}**3)/(pi*{rad}**2*{2 * rad})"
            st = [f"球：${pitex(Fr(4 * rad ** 3, 3))}$。", f"円柱：${pitex(2 * rad ** 3)}$。", "比：$\\dfrac{4}{3}:2=4:6=2:3$。"]
        else:
            a, b = 1, 1
            stem = f"半径 ${rad}$ cm の球と，その球がちょうど入る円柱（底面の半径 ${rad}$ cm，高さ ${2 * rad}$ cm）がある。球の表面積と円柱の側面積の比を最も簡単な整数の比で表しなさい。"
            e = f"球の表面積 $4\\pi\\times{rad}^2={pitex(4 * rad * rad)}$，円柱の側面積 $2\\pi\\times{rad}\\times{2 * rad}={pitex(4 * rad * rad)}$ で等しいので $1:1$。"
            expr = f"(4*pi*{rad}**2)/(2*pi*{rad}*{2 * rad})"
            st = [f"球の表面積：${pitex(4 * rad * rad)}$。", f"円柱の側面積：${pitex(4 * rad * rad)}$。", "比：$1:1$。"]
        alt = ["半径を $r$ として文字で計算すると，$r$ の値に関係なく同じ比になることがわかる。"]
    elif kind == "cube_cut":
        s = r.randint(2, 9)
        a, b = 5, 1
        stem = f"1辺が ${s}$ cm の立方体 ABCD−EFGH を，3点 B，D，E を通る平面で切り，2つの立体に分けた。頂点 A をふくむ三角錐の体積を V，もう一方の立体の体積を W とするとき，W：V を最も簡単な整数の比で表しなさい。"
        e = f"V $=\\dfrac{{1}}{{3}}\\times\\dfrac{{1}}{{2}}\\times{s}\\times{s}\\times{s}={ftex(Fr(s ** 3, 6))}$，W $={s ** 3}-{ftex(Fr(s ** 3, 6))}={ftex(Fr(5 * s ** 3, 6))}$ なので W：V$=5:1$。"
        expr = f"({s}**3-Rational(1,6)*{s}**3)/(Rational(1,6)*{s}**3)"
        st = [f"三角錐 A−BDE は，底面 $\\triangle$ABD（直角二等辺三角形，面積 ${ftex(Fr(s * s, 2))}$），高さ AE$={s}$。", f"V $=\\dfrac{{1}}{{3}}\\times{ftex(Fr(s * s, 2))}\\times{s}={ftex(Fr(s ** 3, 6))}$。", f"W $={s ** 3}-{ftex(Fr(s ** 3, 6))}={ftex(Fr(5 * s ** 3, 6))}$。", "W：V$=5:1$。"]
        alt = ["V は立方体の $\\dfrac{1}{2}\\times\\dfrac{1}{3}=\\dfrac{1}{6}$ なので，W は $\\dfrac{5}{6}$。1辺の長さに関係なく $5:1$。"]
    else:
        r1, h1, r2, h2 = r.randint(1, 6), r.randint(2, 9), r.randint(1, 6), r.randint(2, 9)
        num_, den = Fr(r1 * r1 * h1, 3), Fr(r2 * r2 * h2)
        q = num_ / den
        if q == 1:
            h2 += 1
            den = Fr(r2 * r2 * h2)
            q = num_ / den
        a, b = q.numerator, q.denominator
        stem = f"底面の半径が ${r1}$ cm，高さが ${h1}$ cm の円錐 P と，底面の半径が ${r2}$ cm，高さが ${h2}$ cm の円柱 Q がある。P と Q の体積の比を最も簡単な整数の比で表しなさい。"
        e = f"P $=\\dfrac{{1}}{{3}}\\pi\\times{r1}^2\\times{h1}={pitex(num_)}$，Q $=\\pi\\times{r2}^2\\times{h2}={pitex(den)}$。P：Q$={a}:{b}$。"
        expr = f"(pi*{r1}**2*{h1}/3)/(pi*{r2}**2*{h2})"
        st = [f"P の体積：${pitex(num_)}$。", f"Q の体積：${pitex(den)}$。", f"$\\pi$ は共通なので約して，${ftex(num_)}:{ftex(den)}={a}:{b}$。"]
        alt = ["$\\pi$ を最初から省いて計算し，比を簡単にしてもよい。"]
    return num(stem, f"${a}:{b}$", e, d=4, p=8, mark=("ratio", a, b), chk=(expr, f"Rational({a},{b})", None, "intermediate"),
               ap="それぞれの体積（面積）を同じ文字や数で表し，比をとる。$\\pi$ や共通の因数は約すことができる。",
               steps=st, alt=alt,
               pc=[("それぞれの量を正しく式に表している", 4), ("比を最も簡単な整数の比にしている", 4)],
               pit=["錐体の $\\dfrac{1}{3}$ をかけ忘れる。", "比を最も簡単な整数の比にしない。"])


@gen("thinking_writing", 3, ["cross_unit", "application"], rel=["JH-MATH-G1-U05"])
def c_cone_roll(r):
    kind = r.choice(["turns", "slant", "angle_back"])
    if kind == "turns":
        rad = r.randint(1, 6)
        n = r.randint(2, 6)
        L = rad * n
        return MARK(f"底面の半径が ${rad}$ cm，母線の長さが ${L}$ cm の円錐を，平面上で頂点 O を中心としてすべらないように転がしたところ，円錐は点 O を中心とする円をえがいて元の位置にもどった。元の位置にもどるまでに，円錐は何回転したか求めなさい。",
                    n, f"えがく円の円周は $2\\pi\\times{L}={2 * L}\\pi$，底面の円周は ${2 * rad}\\pi$。${2 * L}\\pi\\div{2 * rad}\\pi={n}$ 回転。",
                    f"(2*pi*{L})/(2*pi*{rad})", d=4, p=8,
                    ap="円錐が転がるとき，底面の円周が平面上の円（半径＝母線）の上を転がる。2つの円周の長さを比べる。",
                    steps=[f"平面上にえがく円の半径は母線の長さ ${L}$ cm，円周 ${2 * L}\\pi$ cm。", f"1回転で進む長さは底面の円周 ${2 * rad}\\pi$ cm。", f"${2 * L}\\pi\\div{2 * rad}\\pi={n}$。"],
                    alt=[f"側面のおうぎ形の中心角 $360\\times\\dfrac{{{rad}}}{{{L}}}={360 * rad // L}^\\circ$ を求め，$360\\div{360 * rad // L}={n}$ としても求められる（平面図形のおうぎ形とのつながり）。"],
                    pc=[("えがく円の半径が母線の長さであることに気づいている", 3), ("円周の比で回転数を求めている", 3), ("正しい答え", 2)],
                    pit=["えがく円の半径を底面の半径と取り違える。"])
    if kind == "slant":
        rad = r.randint(1, 8)
        ang = r.choice([a for a in (30, 40, 45, 60, 72, 80, 90, 100, 120, 135, 144, 150, 160, 180, 200, 216, 240, 270) if (360 * rad) % a == 0 and 360 * rad // a > rad])
        L = 360 * rad // ang
        return MARK(f"円錐の展開図で，側面のおうぎ形の中心角が ${ang}^\\circ$，底面の円の半径が ${rad}$ cm であった。この円錐の母線の長さは何 cm か求めなさい。",
                    L, f"$2\\pi\\times\\ell\\times\\dfrac{{{ang}}}{{360}}=2\\pi\\times{rad}$ を解いて $\\ell={L}$。", f"360*{rad}/{ang}", d=4, p=8,
                    ap="側面のおうぎ形の弧の長さは底面の円周に等しい。母線の長さを $\\ell$ とおいて方程式をつくる（平面図形のおうぎ形の公式を使う）。",
                    steps=[f"おうぎ形の弧：$2\\pi\\ell\\times\\dfrac{{{ang}}}{{360}}$。", f"底面の円周：${2 * rad}\\pi$。", f"等しいとおいて $\\ell\\times{ftex(Fr(ang, 360))}={rad}$，$\\ell={L}$。"],
                    alt=[f"中心角 $=360\\times\\dfrac{{r}}{{\\ell}}$ の関係から $\\dfrac{{{rad}}}{{\\ell}}={ftex(Fr(ang, 360))}$ として求めてもよい。"],
                    pc=[("弧の長さ＝底面の円周の関係を使っている", 3), ("方程式を正しく立てている", 3), ("正しい答え", 2)],
                    pit=["割合を逆にして $\\ell$ を小さく求めてしまう（母線は底面の半径より長いはず）。"])
    L = r.choice([x for x in range(3, 19) if any((360 * y) % x == 0 for y in range(1, x))])
    rad = r.choice([x for x in range(1, L) if (360 * x) % L == 0])
    ang = 360 * rad // L
    S = Fr(rad * L)
    return MARK(f"母線の長さが ${L}$ cm，底面の半径が ${rad}$ cm の円錐がある。この円錐の側面積は $a\\pi$ cm² と表される。$a$ の値を求めなさい。", S,
                f"側面のおうぎ形の中心角は $360\\times\\dfrac{{{rad}}}{{{L}}}={ang}^\\circ$。側面積は $\\pi\\times{L}^2\\times\\dfrac{{{ang}}}{{360}}={pitex(S)}$ なので $a={ftex(S)}$。",
                f"{L}**2*Rational({ang},360)", d=4, p=8,
                ap="側面は半径 $\\ell$ のおうぎ形。中心角を求めておうぎ形の面積の公式（平面図形）に当てはめる。",
                steps=[f"中心角：$360\\times\\dfrac{{{rad}}}{{{L}}}={ang}^\\circ$。", f"側面積：$\\pi\\times{L}^2\\times\\dfrac{{{ang}}}{{360}}={pitex(S)}$。", f"$a={ftex(S)}$。"],
                alt=[f"$\\pi r\\ell=\\pi\\times{rad}\\times{L}={pitex(S)}$ の公式で求めて確かめる。"],
                pc=[("中心角を正しく求めている", 3), ("おうぎ形の面積として側面積を求めている", 3), ("正しい答え", 2)],
                pit=["おうぎ形の半径を底面の半径としてしまう。"])


SPACE = [
    ("1つの平面に垂直な2直線は平行である。", True, "同じ平面に垂直な2直線は平行になる。"),
    ("1つの直線に垂直な2平面は平行である。", True, "同じ直線に垂直な2平面は平行になる。"),
    ("平行な2平面に別の平面が交わるとき，2つの交線は平行である。", True, "2つの交線は同じ平面上にあって交わらないので平行である。"),
    ("1つの直線に垂直な2直線は平行である。", False, "空間では，1つの直線に垂直な2直線が交わったり，ねじれの位置にあったりすることがある（直方体の辺 AB に垂直な辺 AD と AE は交わる）。"),
    ("交わらない2直線は平行である。", False, "空間では，交わらず平行でもない「ねじれの位置」の場合がある。"),
    ("1つの平面に平行な2直線は平行である。", False, "1つの平面に平行な2直線が交わることもある（直方体の上の面の2辺 AB，AD はどちらも下の面に平行だが交わる）。"),
    ("1つの平面に垂直な2平面は平行である。", False, "1つの平面に垂直な2平面が交わることもある（直方体の隣り合う2つの側面はどちらも底面に垂直だが交わる）。"),
    ("ねじれの位置にある2直線は，同じ平面上にない。", True, "同じ平面上にある2直線は，交わるか平行かのどちらかである。"),
]


@gen("thinking_writing", 3, ["condition_check", "written_reasoning"])
def c_space(r):
    while True:
        tx, ty = r.choice([True, False]), r.choice([True, False])
        px = [s for s in SPACE if s[1] == tx]
        py_ = [s for s in SPACE if s[1] == ty]
        x = r.choice(px)
        y = r.choice([s for s in py_ if s is not x] or py_)
        if x is not y:
            break
    XY = ["X：正　Y：正", "X：正　Y：誤", "X：誤　Y：正", "X：誤　Y：誤"]
    ans = XY[(0 if tx else 2) + (0 if ty else 1)]
    why = {}
    for c in XY:
        if c == ans:
            continue
        cx, cy = c.startswith("X：正"), c.endswith("Y：正")
        rs = []
        if cx != tx:
            rs.append(f"X は{'正しい' if tx else '誤り'}。{x[2]}")
        if cy != ty:
            rs.append(f"Y は{'正しい' if ty else '誤り'}。{y[2]}")
        why[c] = (" ".join(rs), "平面上の性質を空間にそのまま当てはめる誤り")
    return mc(f"空間における直線や平面の位置関係について述べた次の X，Y の文の正誤の組み合わせとして最も適するものを，" + SEL4 + f"\nX　{x[0]}\nY　{y[0]}",
              [ans] + [c for c in XY if c != ans], f"X：{x[2]}　Y：{y[2]}", d=4, p=8, why=why,
              ap="直方体の辺や面を使って，文に当てはまる例・当てはまらない例（反例）を探す。1つでも反例があれば誤り。",
              steps=["直方体 ABCD−EFGH を思いうかべる。", f"X：{x[2]}", f"Y：{y[2]}", f"よって {ans}。"],
              alt=["教室の壁・床・天井や柱を使って，文の内容を実際に確かめる。"],
              pc=[("X の正誤を根拠をもって判断している", 4), ("Y の正誤を根拠をもって判断している", 4)],
              pit=["平面上で成り立つ性質（垂直な2直線は平行など）を空間でもそのまま成り立つと考える。"])


# ======================================================================
# D 典型誤答訂正
# ======================================================================

def _err_mc(stem, sol, right, cands, e, err, **kw):
    return MC(f"{stem}\n〔Kさんの解答〕\n{sol}\nKさんの解答の誤りを説明したものとして最も適するものを，" + SEL4, right, cands, e, err=err, **kw)


TRIPLES = [(3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (4, 3, 5), (8, 6, 10), (12, 5, 13), (12, 9, 15), (15, 8, 17)]


@gen("error_correction", 4, ["common_error", "concept"])
def d_cone(r):
    rad, h, L = r.choice(TRIPLES)
    kind = r.choice(["third", "slant"])
    V = Fr(rad * rad * h, 3)
    if kind == "third":
        sol = f"$\\pi\\times{rad}^2\\times{h}={pitex(rad * rad * h)}$　答え ${pitex(rad * rad * h)}$ cm³"
        right = "円錐は錐体なので，体積は（底面積）×（高さ）に $\\dfrac{1}{3}$ をかけなければならないのに，かけ忘れている。"
        step, etype, tempt = "体積の公式（$\\dfrac{1}{3}$ のかけ忘れ）", "formula", "円柱の体積の公式と形が似ているため，$\\dfrac{1}{3}$ を忘れやすい。"
        c4 = ("高さの代わりに母線の長さを使うべきである。", "体積には底面に垂直な高さを使う。母線の長さは使わない。", "高さと母線の混同")
    else:
        sol = f"$\\dfrac{{1}}{{3}}\\times\\pi\\times{rad}^2\\times{L}={pitex(Fr(rad * rad * L, 3))}$　答え ${pitex(Fr(rad * rad * L, 3))}$ cm³"
        right = f"円錐の体積には頂点から底面に垂直にひいた高さ ${h}$ cm を使うべきなのに，母線の長さ ${L}$ cm を使っている。"
        step, etype, tempt = "高さとして母線の長さを使った部分", "concept", "見取図で母線が目立つため，母線を高さと思いこみやすい。"
        c4 = ("$\\dfrac{1}{3}$ をかける必要はない。", "円錐は錐体なので $\\dfrac{1}{3}$ をかけるのが正しい。", "柱体と錐体の混同")
    fix = f"$\\dfrac{{1}}{{3}}\\times\\pi\\times{rad}^2\\times{h}={pitex(V)}$ cm³"
    cands = [("半径の代わりに直径を使うべきである。", "公式に使うのは底面の半径である。", "半径と直径の混同"), c4,
             ("$\\pi$ を $3.14$ にして計算すべきである。", "円周率は $\\pi$ とすると指定されているので，$\\pi$ のまま答える。", "答え方の誤解"),
             ("Kさんの解答に誤りはない。", "Kさんの答えは正しい体積になっていない。", "公式の確認不足")]
    return _err_mc(f"〔問題〕底面の半径が ${rad}$ cm，高さが ${h}$ cm，母線の長さが ${L}$ cm の円錐の体積を求めなさい。" + PI, sol, right, cands,
                   f"正しくは {fix}。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="円錐の体積の公式 $V=\\dfrac{1}{3}\\pi r^2h$ の各文字が何を表すかを確認し，Kさんの式と比べる。",
                   steps=["円錐は錐体なので $V=\\dfrac{1}{3}\\times$ 底面積 $\\times$ 高さ。", f"高さは頂点から底面への垂線の長さで ${h}$ cm（母線 ${L}$ cm ではない）。", f"正しくは {fix}。"],
                   alt=[f"同じ底面・高さの円柱 ${pitex(rad * rad * h)}$ cm³ の $\\dfrac{{1}}{{3}}$ になっているかで確かめる。"],
                   pc=[("誤りの箇所を正しく指摘している", 3), ("正しい体積を求めている", 3)],
                   pit=["高さと母線の区別がつかない。", "$\\dfrac{1}{3}$ を忘れる。"],
                   chk=(f"pi*{rad}**2*{h}/3", f"{fpy(V)}*pi", None, "intermediate"))


@gen("error_correction", 3, ["common_error", "computation"])
def d_angle(r):
    rad = r.randint(1, 8)
    L = r.choice([x for x in range(rad + 1, 19) if (360 * rad) % x == 0])
    ang = Fr(360 * rad, L)
    kind = r.choice(["inv", "dia"])
    if kind == "inv":
        w = Fr(360 * L, rad)
        sol = f"中心角 $=360\\times\\dfrac{{{L}}}{{{rad}}}={ftex(w)}^\\circ$"
        right = "中心角は $360^\\circ\\times\\dfrac{\\text{底面の半径}}{\\text{母線の長さ}}$ で求めるのに，分数の分子と分母を逆にしている。"
        step, etype, tempt = "割合の分子と分母", "formula", "「母線」「半径」の2つの長さのどちらを分母にするかを，意味を考えずに式に入れている。"
    else:
        w = Fr(360 * 2 * rad, L)
        sol = f"中心角 $=360\\times\\dfrac{{{2 * rad}}}{{{L}}}={ftex(w)}^\\circ$"
        right = "底面の半径を使うべきところを，直径を使っている。おうぎ形の弧の長さ $2\\pi r$ と，半径 $\\ell$ の円周 $2\\pi\\ell$ の比は $\\dfrac{r}{\\ell}$ である。"
        step, etype, tempt = "割合の分子（直径を使った部分）", "concept", "「$2\\pi r$」の $2r$（直径）を分子にそのまま残してしまう。"
    fix = f"中心角 $=360\\times\\dfrac{{{rad}}}{{{L}}}={ftex(ang)}^\\circ$"
    cands = [("$360$ ではなく $180$ をかけるべきである。", "円全体の中心角は $360^\\circ$ なので，$360$ に割合をかける。", "中心角の全体の誤解"),
             ("中心角は底面の半径と母線の長さの和から求めるべきである。", "中心角は長さの比（割合）から求める。和は使わない。", "割合の考え方の誤解"),
             ("Kさんの解答に誤りはない。", f"Kさんの答え ${ftex(w)}^\\circ$ では，弧の長さが底面の円周と等しくならない。", "検算不足")]
    if kind == "inv":
        cands.insert(0, ("底面の半径の代わりに直径を使うべきである。", "比は半径どうし（$r:\\ell$）で考える。", "半径と直径の混同"))
    else:
        cands.insert(0, ("割合は $\\dfrac{\\text{母線の長さ}}{\\text{底面の半径}}$ とすべきである。", "それでは中心角が $360^\\circ$ をこえてしまう。", "割合の向きの誤解"))
    return _err_mc(f"〔問題〕底面の半径が ${rad}$ cm，母線の長さが ${L}$ cm の円錐の展開図で，側面のおうぎ形の中心角を求めなさい。", sol, right, cands,
                   f"正しくは {fix}。", dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix), d=3, p=6,
                   ap="側面のおうぎ形の弧の長さ＝底面の円周，から割合を正しく立てる。答えが $0^\\circ$ より大きく $360^\\circ$ より小さいかも確かめる。",
                   steps=[f"弧の長さ（底面の円周）：${2 * rad}\\pi$。", f"半径 ${L}$ の円周：${2 * L}\\pi$。", f"割合：${ftex(Fr(rad, L))}$。{fix}。"],
                   alt=[f"求めた中心角で弧の長さ $2\\pi\\times{L}\\times\\dfrac{{a}}{{360}}$ を計算し，底面の円周 ${2 * rad}\\pi$ と一致するかを確かめる。"],
                   pc=[("誤りの原因を正しく指摘している", 3), ("正しい中心角を求めている", 3)],
                   pit=["答えが $360^\\circ$ をこえても見直さない。"],
                   chk=(f"360*Rational({rad},{L})", fpy(ang), None, "intermediate"))


@gen("error_correction", 3, ["common_error", "condition_check"])
def d_cyl(r):
    rad, h = r.randint(1, 9), r.randint(2, 12)
    where = r.choice([0, 1, 2])
    lat, base = 2 * rad * h, rad * rad
    l1 = f"側面の長方形の横の長さは $2\\pi\\times{rad}={2 * rad}\\pi$"
    l2 = f"側面積は ${2 * rad}\\pi\\times{h}={pitex(lat)}$"
    l3 = f"底面積は $\\pi\\times{rad}^2={pitex(base)}$ で，底面は2つ"
    l4 = f"表面積は ${pitex(lat)}+{pitex(base)}\\times2={pitex(lat + 2 * base)}$"
    if where == 0:
        l1 = f"側面の長方形の横の長さは $\\pi\\times{rad}={pitex(rad)}$"
        l2 = f"側面積は ${pitex(rad)}\\times{h}={pitex(rad * h)}$"
        l4 = f"表面積は ${pitex(rad * h)}+{pitex(base)}\\times2={pitex(rad * h + 2 * base)}$"
        step, etype, tempt = "1行目（円周を $\\pi r$ とした）", "formula", "円周の公式 $2\\pi r$ と円の面積の公式 $\\pi r^2$ を混同しやすい。"
    elif where == 1:
        l2 = f"側面積は ${2 * rad}\\pi\\times{h}\\div2={pitex(rad * h)}$"
        l4 = f"表面積は ${pitex(rad * h)}+{pitex(base)}\\times2={pitex(rad * h + 2 * base)}$"
        step, etype, tempt = "2行目（長方形の面積を2でわった）", "calculation", "三角形の面積の公式と混同して，不要な $\\div2$ をしている。"
    else:
        l3 = f"底面積は $\\pi\\times{rad}^2={pitex(base)}$ で，底面は1つ"
        l4 = f"表面積は ${pitex(lat)}+{pitex(base)}={pitex(lat + base)}$"
        step, etype, tempt = "3行目（底面を1つとした）", "condition", "円錐の表面積（底面1つ）と混同しやすい。"
    sol = "\n".join(f"{i + 1}行目　{t}" for i, t in enumerate([l1, l2, l3, l4]))
    LINES4 = ["1行目", "2行目", "3行目", "4行目"]
    ok = {0: "1行目は正しい。側面の長方形の横の長さは底面の円周 $2\\pi r$ である。", 1: "2行目は，1行目の長さに高さをかけて正しく計算している。",
          2: "3行目は正しい。円柱の底面は2つある。", 3: "4行目は，それまでの値を正しく加えている。"}
    why = {LINES4[i]: (ok[i], "誤りの箇所の見落とし") for i in range(4) if i != where}
    S = lat + 2 * base
    fix = f"側面積 ${pitex(lat)}$，底面積 ${pitex(base)}\\times2$，表面積 ${pitex(S)}$ cm²"
    return mc(f"〔問題〕底面の半径が ${rad}$ cm，高さが ${h}$ cm の円柱の表面積を求めなさい。" + PI + f"\n〔Kさんの解答〕\n{sol}\nKさんの解答で，誤りが最初に生じた行として最も適するものを，" + SEL4,
              LINES4, f"誤りが最初に生じたのは{LINES4[where]}。正しくは {fix}。", d=3, p=6, keep=True, ai=where, why=why,
              err=dict(sol=sol, step=step, type=etype, tempt=tempt, fix=fix),
              ap="展開図をかき，側面の長方形の縦・横と底面の数を確認しながら，1行ずつ自分で計算し直す。",
              steps=[f"側面の横の長さ＝底面の円周 ${2 * rad}\\pi$。", f"側面積 ${2 * rad}\\pi\\times{h}={pitex(lat)}$。", f"底面 ${pitex(base)}$ が2つ。", f"表面積 ${pitex(S)}$ cm²。"],
              alt=["展開図に各部分の長さを書きこみ，面積を1つずつ求めて加える。"],
              pc=[("誤りの行を正しく指摘している", 3), ("正しい表面積を求めている", 3)],
              pit=["底面の数を確かめない。", "円周と面積の公式を混同する。"],
              chk=(f"2*pi*{rad}*{h}+2*pi*{rad}**2", f"{S}*pi", None, "intermediate"))


GENERATORS = [a_relation, a_volume, a_rotation, a_polyhedra,
              b_cone, b_sphere, b_rot_volume, b_projection, b_surface,
              c_ratio, c_cone_roll, c_space,
              d_cone, d_angle, d_cyl]


def _robust(g):
    """選択肢が重複して誤答が足りないパラメータのときは、同じ乱数列から別のパラメータを引き直す。"""
    import random as _random
    fn = g.fn

    def wrapped(r):
        for _ in range(50):
            try:
                return fn(r)
            except AssertionError:
                r = _random.Random(r.random())
        return fn(r)
    wrapped.__name__ = fn.__name__
    g.fn = wrapped
    return g


GENERATORS = [_robust(g) for g in GENERATORS]
