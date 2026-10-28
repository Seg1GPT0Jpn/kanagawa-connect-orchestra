#!/usr/bin/env python3
"""問題セット JSON から問題冊子・解答解説冊子の PDF を生成する。

  python scripts/build_pdf.py data/pilot/math_unit01.json
  python scripts/build_pdf.py --unit JH-MATH-G1-U01          # 単元 ID を含むセットをすべて
  python scripts/build_pdf.py data/pilot --paper tablet      # タブレット閲覧用
  python scripts/build_pdf.py data/pilot --kind answers --keep-html

処理の流れ
  1. validate_questions.py で検査（エラーのあるセットはビルドしない。--force で無視）
  2. Jinja2 で templates/question_template.html / answer_template.html に流し込み
  3. Chromium（Playwright）で KaTeX の数式を描画してから PDF 化
  4. レイアウト検査（数式エラー・版面からのはみ出し）と PDF 検査（ページ数・文字化け）

出力: output/<data からの相対パス>_questions.pdf / _answers.pdf
"""
from __future__ import annotations

import argparse
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_questions as vq  # noqa: E402

TEMPLATES = ROOT / "templates"
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

# 用紙設定: (幅mm, 高さmm, 余白 上 右 下 左 mm, 本文サイズ)
PAPERS = {
    "A4": (210, 297, (17, 15, 17, 15), "10.5pt"),
    "B5": (182, 257, (15, 13, 15, 13), "10pt"),
    "tablet": (180, 240, (12, 11, 13, 11), "12pt"),  # 3:4 タブレットで等倍表示しやすい比率
}

JP_FONTS = ["IPAMincho", "IPAexMincho", "IPAGothic", "IPAexGothic", "Noto Serif CJK JP", "Noto Sans CJK JP"]


# --------------------------------------------------------------------------
# マスターの表示名
# --------------------------------------------------------------------------

def _load_masters():
    m = json.loads((ROOT / "schemas" / "curriculum_map.json").read_text(encoding="utf-8"))
    ms = m["masters"]
    lab = lambda key: {x["code"]: x["label"] for x in ms[key]}  # noqa: E731
    return {
        "grade": lab("grades"), "subject": lab("subjects"), "skill": lab("skills"),
        "aspect": lab("evaluation_aspects"), "difficulty": lab("difficulty_levels"),
        "status": lab("verification_statuses"), "track": lab("tracks"),
        "level": {x["code"]: f"{x['letter']}　{x['label']}" for x in ms["exercise_levels"]}, "perspective": lab("perspectives"),
    }, vq.load_curriculum()


MASTERS, UNITS = _load_masters()


# --------------------------------------------------------------------------
# テキスト整形フィルタ
# --------------------------------------------------------------------------

_MARK = re.compile(r"\[\[(u|blank|mark):([^\]]*)\]\]")


def _inline(text: str) -> str:
    """HTML エスケープしたうえで独自記法を変換する（$...$ は KaTeX に任せる）。"""
    s = html.escape(str(text), quote=False)

    def rep(m):
        kind, body = m.group(1), m.group(2)
        if kind == "u":
            return f'<span class="u">{body}</span>'
        if kind == "blank":
            return f'<span class="blank">{body or "　"}</span>'
        label, _, words = body.partition(":")
        return f'<span class="mark"><sup>{label}</sup>{words}</span>'

    return _MARK.sub(rep, s)


def rich_inline(text) -> str:
    from markupsafe import Markup
    return Markup(_inline(text).replace("\n", "<br>"))


def rich_block(text) -> str:
    from markupsafe import Markup
    paras = re.split(r"\n\s*\n", str(text).strip())
    return Markup("".join(f"<p>{_inline(p).replace(chr(10), '<br>')}</p>" for p in paras))


def visual_len(s: str) -> float:
    s = re.sub(r"\\[a-zA-Z]+", "x", s).replace("$", "").replace("{", "").replace("}", "")
    return sum(1.0 if unicodedata.east_asian_width(ch) in "WF" else 0.55 for ch in s)


# 選択肢の段組み（4段にできる最大長, 2段にできる最大長）。用紙幅に応じて変える。
CHOICE_LIMITS = {"A4": (8, 19), "B5": (7, 16), "tablet": (5, 12)}


def choice_cols(choices, paper: str = "A4") -> int:
    four, two = CHOICE_LIMITS[paper]
    m = max((visual_len(c.get("text", "")) for c in choices), default=0)
    if m <= four and len(choices) in (4, 8):
        return 4
    if m <= 6 and len(choices) == 5:
        return 5   # 時刻などの短い5択は1行に並べる（入試の体裁）
    if m <= 13 and len(choices) in (6, 9):
        return 3   # 組み合わせの選択肢は 3×2・3×3 の表に並べる
    if m <= two:
        return 2
    return 1


def num(v) -> str:
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


def answer_display(q: dict) -> str:
    a = q.get("answer", {})
    if a.get("display"):
        return a["display"]
    v = a.get("value")
    labels = {c["label"]: c["text"] for c in q.get("choices", []) or []}
    qt = q.get("question_type")
    if qt in ("multiple_choice", "true_false") and str(v) in labels:
        return f"{v}　{labels[str(v)]}"
    if isinstance(v, list):
        sep = "→" if qt == "ordering" else "，"
        return sep.join(str(x) for x in v)
    out = str(v)
    if a.get("unit"):
        out += f" {a['unit']}"
    if q.get("_mark"):
        out += f"（{mark_text(q)}）"
    return out


def truncate_plain(text: str, n: int) -> str:
    s = _MARK.sub(lambda m: m.group(2).split(":")[-1], str(text)).replace("\n", " ")
    if len(s) <= n:
        return s
    cut = s[:n]
    if cut.count("$") % 2:  # 数式の途中で切らない
        cut = cut[: cut.rfind("$")]
    return cut.rstrip() + "…"


# --------------------------------------------------------------------------
# 組版用データの準備
# --------------------------------------------------------------------------

def prepare(data: dict, paper: str = "A4") -> tuple[list, list]:
    stimuli = {s["id"]: s for s in data.get("stimuli", [])}
    sections = {s["id"]: s for s in data.get("sections", [])}
    groups: list[dict] = []
    shown: set[str] = set()
    cur_key = object()
    prev_stim = None
    for i, q in enumerate(data["questions"]):
        q = dict(q)
        q["_number"] = q.get("number") or f"{i + 1}"
        q["_long"] = len(q.get("stem", "")) > 500 or (q.get("answer_space") or {}).get("lines", 0) > 10 or \
            (q.get("answer_space") or {}).get("char_grid", 0) > 200 or bool(q.get("stimulus") and len(q["stimulus"].get("content", "")) > 600)
        q["_long_exp"] = len(q.get("explanation", "")) > 700
        q["_cols"] = choice_cols(q.get("choices") or [], paper)
        # 問題に直接付いた資料（本文・放送文）は、直前の問題と同じなら繰り返さない
        st = q.get("stimulus")
        q["_stim_show"] = bool(st) and st != prev_stim
        prev_stim = st
        sec_id = q.get("section")
        if sec_id != cur_key:
            sec = sections.get(sec_id) if sec_id else None
            groups.append({"section": sec, "items": [], "page_break": bool(sec and sec.get("page_break"))})
            cur_key = sec_id
            if sec:
                for ref in sec.get("stimulus_refs", []):
                    if ref in stimuli and ref not in shown:
                        groups[-1]["items"].append({"kind": "stimulus", "stimulus": stimuli[ref], "compact": False})
                        shown.add(ref)
        ref = q.get("stimulus_ref")
        if ref and ref in stimuli and ref not in shown:
            st = stimuli[ref]
            # 同じ大問の2つ目以降のリスニング資料は、問題冊子では見出しだけにする
            compact = st.get("type") == "listening_script" and any(
                it["kind"] == "stimulus" and it["stimulus"].get("type") == "listening_script" for it in groups[-1]["items"])
            groups[-1]["items"].append({"kind": "stimulus", "stimulus": st, "compact": compact})
            shown.add(ref)
        groups[-1]["items"].append({"kind": "question", "question": q})
    if groups:
        groups[0]["page_break"] = False  # 表紙の直後では改ページしない
    units = [UNITS[u] for u in data.get("unit_ids", []) if u in UNITS]
    return groups, units


_SVG_SEQ = [0]


def uniq_svg_ids(svg: str) -> str:
    """図ごとに SVG 内の id（clipPath など）を一意にする。同じ id の図が1冊に並ぶと、別の図の切り抜き範囲が使われてしまうため。"""
    if not svg or "id=" not in svg:
        return svg
    _SVG_SEQ[0] += 1
    pre = f"f{_SVG_SEQ[0]}-"
    ids = set(re.findall(r'\bid="([^"]+)"', svg))
    for i in sorted(ids, key=len, reverse=True):
        svg = svg.replace(f'id="{i}"', f'id="{pre}{i}"').replace(f"url(#{i})", f"url(#{pre}{i})").replace(f'href="#{i}"', f'href="#{pre}{i}"')
    return svg


def make_env():
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES)),
        autoescape=select_autoescape(["html"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters.update({
        "rich_inline": rich_inline,
        "rich_block": rich_block,
        "num": num,
        "answer_display": answer_display,
        "uniq_ids": uniq_svg_ids,
        "truncate_plain": truncate_plain,
        "grade_label": lambda c: MASTERS["grade"].get(c, c),
        "subject_label": lambda c: MASTERS["subject"].get(c, c),
        "skill_label": lambda c: MASTERS["skill"].get(c, c),
        "aspect_label": lambda c: MASTERS["aspect"].get(c, c),
        "difficulty_label": lambda c: MASTERS["difficulty"].get(c, c),
        "status_label": lambda c: MASTERS["status"].get(c, c),
        "track_label": lambda c: MASTERS["track"].get(c, c),
        "level_label": lambda c: MASTERS["level"].get(c, c),
        "perspective_label": lambda c: MASTERS["perspective"].get(c, c),
        "lesson_kind": lambda c: LESSON_KINDS.get(c, c),
        "error_type_label": lambda c: ERROR_TYPES.get(c, c),
    })
    return env


LESSON_KINDS = {"intro": "導入", "definition": "定義", "theorem": "定理・公式", "proof": "証明", "derivation": "導出",
                "example": "例題", "figure_explain": "図解", "board_plan": "板書案", "teacher_guide": "指導ガイド", "summary": "まとめ", "check": "確認"}
ERROR_TYPES = {"sign": "符号の誤り", "condition": "条件の見落とし", "formula": "公式の誤用", "concept": "概念の誤解", "calculation": "計算ミス",
               "interpretation": "題意の読み違い", "notation": "表記の誤り", "logic": "論理の誤り", "unit": "単位の誤り"}


def edition_of(data: dict, kind: str) -> str:
    """出力する冊子の種類。授業プリントは questions→生徒用、answers→教師用 に読みかえる。"""
    if data.get("print_type") == "lesson":
        return "student" if kind == "questions" else "teacher"
    return kind


EDITION_TITLES = {"questions": "問題", "answers": "解答・解説", "student": "生徒用", "teacher": "教師用"}


HIRAGANA = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわ"
KG_SUBJECT = {"math": ("数", "数　　学"), "english": ("英", "外国語（英　語）"), "japanese": ("国", "国　　語"),
              "science": ("理", "理　　科"), "social": ("社", "社　　会")}


def is_tate(data: dict) -> bool:
    """国語は実際の入試と同じく縦書き・横長の用紙で組む。"""
    return data.get("exam_format") == "kanagawa" and data.get("subject") == "japanese"


def is_kanagawa(data: dict, kind: str) -> bool:
    return data.get("exam_format") == "kanagawa" and edition_of(data, kind) == "questions"


def kanagawa_context(data: dict, groups: list, units: list) -> dict:
    """神奈川入試形式の表紙・注意事項と、あいう の割り当て（冊子全体で通し）。"""
    tab, title = KG_SUBJECT.get(data.get("subject"), ("", MASTERS["subject"].get(data.get("subject"), "")))
    letters = iter(HIRAGANA * 3)
    has_mark = False
    last_mon = ""
    tate = is_tate(data)
    for g in groups:
        if g.get("section"):
            last_mon = g["section"].get("title", last_mon)
        for it in g["items"]:
            if it["kind"] != "question":
                continue
            q = it["question"]
            qno = q.get("_number", "")
            sub = qno[qno.index("("):] if "(" in qno else ""   # 小問のない問（例：問5）は見出しだけ
            q["_sub"] = sub.replace("(", "（").replace(")", "）") if tate else sub
            ma = q.get("mark_answer")
            if ma:
                has_mark = True
                parts = [[next(letters) for _ in str(v)] for v in ma["values"]]
                q["_mark"] = {"form": ma["form"], "parts": parts, "letters": [l for p in parts for l in p]}
            q["_written"] = not q.get("choices") and not ma
    notes = ["開始の合図があるまで、この問題冊子を開いてはいけません。",
             f"問題は {last_mon} まであります。解答用紙はこの冊子の最後にあります。",
             "解答は、解答用紙の決められた欄に書きなさい。",
             "番号を選んで答える問題は、解答用紙の番号を一つ塗りつぶしなさい。"]
    if has_mark:
        notes += ["「あ」「い」「う」…にあてはまる数字を答える問題は、下の 例 のように、あてはまる数字をそれぞれ 0〜9 の中から一つずつ選びなさい。",
                  "答えに根号が含まれるときは、根号の中を最も小さい自然数にしなさい。",
                  "答えが分数になるときは、約分できる場合は約分しなさい。",
                  "計算は、問題冊子のあいているところを使いなさい。"]
    if data.get("subject") == "english":
        notes.append("英語で書く答えは、活字体でも筆記体でもかまいません。")
    if data.get("subject") == "japanese":
        notes.append("字数制限のある問題は、句読点なども一字に数えなさい。")
    notes.append("終了の合図があったら、すぐに解答をやめなさい。")
    unit = units[0] if units else {}
    grade = MASTERS["grade"].get(data.get("grade"), data.get("grade", ""))
    if data.get("track") == "mock_exam":   # 模試は単元名ではなくセットの題名を表紙に出す
        name = (data.get("exam_spec") or {}).get("name") or "オリジナル模試"
        return {"tab": tab, "subject_title": title, "notes": notes, "has_mark": has_mark, "tate": tate,
                "series": f"{name}　（{data.get('time_limit_minutes', 50)}分・{num(data.get('total_points', 100))}点）",
                "unit_title": ""}
    return {"tab": tab, "subject_title": title, "notes": notes, "has_mark": has_mark, "tate": is_tate(data),
            "series": f"{grade}　単元演習",
            "unit_title": unit.get("title", data.get("title", ""))}


def mark_text(q: dict) -> str:
    """解答解説冊子用：あいう の答え（例 あ＝7　い＝1　う＝2）。"""
    m = q.get("_mark")
    if not m:
        return ""
    digits = "".join(str(v) for v in q["mark_answer"]["values"])
    return "　".join(f"{l}＝{d}" for l, d in zip(m["letters"], digits))


def render_html(env, data: dict, kind: str, paper: str) -> str:
    w, h, (mt, mr, mb, ml), fs = PAPERS[paper]
    groups, units = prepare(data, paper)
    build = data.get("build", {})
    pt = data.get("print_type", "worksheet")
    kind = edition_of(data, kind)
    kg = None
    if data.get("exam_format") == "kanagawa":
        kg = kanagawa_context(data, groups, units)   # 解答解説でも あいう の対応を使う
    if is_kanagawa(data, kind):
        tpl = env.get_template("kanagawa_exam_template.html")
    elif pt == "lesson":
        tpl = env.get_template("lesson_print_template.html")
    elif pt == "exercise":
        tpl = env.get_template("exercise_print_template.html")
    else:
        tpl = env.get_template("question_template.html" if kind == "questions" else "answer_template.html")
    if is_kanagawa(data, kind) and is_tate(data):
        w, h = h, w
    page_css = f"@page {{ size: {w}mm {h}mm; }}\n:root {{ --fs: {fs}; --tpage-w: {w - ml - mr}mm; --tpage-h: {h - mt - mb - 1}mm; }}"
    if paper == "tablet":
        page_css += "\n.choices.cols-4 { grid-template-columns: 1fr 1fr; }"
    return tpl.render(
        qs=data,
        groups=groups,
        units=units,
        kind=kind,
        paper=paper,
        css=(TEMPLATES / "print.css").read_text(encoding="utf-8"),
        page_css=page_css,
        asset_base=TEMPLATES.as_uri() + "/",
        doc_title=f"{data['title']}（{EDITION_TITLES[kind]}）",
        show_points=build.get("show_points", True),
        show_difficulty=build.get("show_difficulty", data.get("track") not in ("mock_exam",)),
        answer_sheet=data.get("track") == "mock_exam",
        subtotals=subtotals(data),
        kg=kg,
    )


def subtotals(data: dict) -> list[dict]:
    """教科（大問に subject がある場合）または大問ごとの配点合計。"""
    secs = {s["id"]: s for s in data.get("sections", [])}
    from_masters = MASTERS["subject"]
    out: dict[str, dict] = {}
    for q in data["questions"]:
        sec = secs.get(q.get("section"))
        if sec and sec.get("subject"):
            key = from_masters.get(sec["subject"], sec["subject"])
        elif sec:
            key = sec["title"]
        else:
            continue
        t = out.setdefault(key, {"title": key, "count": 0, "points": 0})
        t["count"] += 1
        t["points"] += q["scoring"]["points"]
    return list(out.values())


# --------------------------------------------------------------------------
# PDF 化
# --------------------------------------------------------------------------

def find_chromium() -> str | None:
    env = os.environ.get("CHROMIUM_PATH")
    if env and Path(env).exists():
        return env
    bases = [os.environ.get("PLAYWRIGHT_BROWSERS_PATH", ""), "/opt/pw-browsers", str(Path.home() / ".cache/ms-playwright")]
    cands = []
    for b in filter(None, bases):
        cands += glob.glob(f"{b}/chromium-*/chrome-linux*/chrome")
        cands += glob.glob(f"{b}/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium")
    cands.sort(key=lambda p: int(re.search(r"chromium-(\d+)", p).group(1)) if re.search(r"chromium-(\d+)", p) else 0)
    return cands[-1] if cands else None


def check_fonts() -> list[str]:
    """日本語フォントが無いと豆腐（文字化け）になるため事前に確認する。"""
    if not shutil.which("fc-list"):
        return []
    out = subprocess.run(["fc-list", ":lang=ja", "family"], capture_output=True, text=True).stdout
    return [f for f in JP_FONTS if f in out]


LAYOUT_JS = r"""
() => {
  const issues = [];
  const body = document.body.getBoundingClientRect();
  document.querySelectorAll('.katex-error').forEach(e => issues.push(['ERROR', 'KaTeX: ' + (e.getAttribute('title') || e.textContent).slice(0, 120)]));
  (window.__renderErrors || []).forEach(m => issues.push(['ERROR', 'KaTeX: ' + m.slice(0, 120)]));
  const sel = '.question, .stimulus, table, .katex-display, .figure-box svg, .choices li, .answer-box, .char-grid, .exp-item';
  document.querySelectorAll(sel).forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > body.right + 1.5 || r.left < body.left - 1.5) {
      const host = el.closest('[id]');
      issues.push(['ERROR', '版面からはみ出しています: ' + (host ? host.id : el.className) + ' (' + Math.round(r.right - body.right) + 'px)']);
    }
  });
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n; let left = 0;
  while ((n = walker.nextNode())) {
    if (n.parentElement && n.parentElement.closest('script, style, .katex, .no-math')) continue;
    if (/\$/.test(n.nodeValue)) left++;
  }
  if (left) issues.push(['WARNING', '描画されずに残った $ 記号が ' + left + ' か所あります']);
  return issues;
}
"""


@dataclass
class BuildResult:
    source: str
    outputs: list = field(default_factory=list)
    errors: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def output_path(src: Path, kind: str, paper: str, out_dir: Path) -> Path:
    try:
        rel = src.resolve().relative_to(DATA)
    except ValueError:
        rel = Path(src.name)
    suffix = f"_{kind}" + ("" if paper == "A4" else f"_{paper}")
    return out_dir / rel.parent / f"{rel.stem}{suffix}.pdf"


def verify_pdf(pdf: Path, title: str) -> list[tuple[str, str]]:
    issues = []
    try:
        from pypdf import PdfReader
    except ImportError:
        return [("WARNING", "pypdf が無いため PDF 検査を省略しました")]
    r = PdfReader(str(pdf))
    if len(r.pages) == 0:
        return [("ERROR", "PDF にページがありません")]
    text = r.pages[0].extract_text() or ""
    norm = lambda s: re.sub(r"\s+", "", unicodedata.normalize("NFKC", s))  # noqa: E731
    if "�" in text:
        issues.append(("ERROR", "PDF のテキストに置換文字 U+FFFD があります（文字化け）"))
    type3 = set()
    for pg in r.pages:
        fonts = pg.get("/Resources", {}).get("/Font", {})
        for f in fonts.values():
            if f.get_object().get("/Subtype") == "/Type3":
                type3.add(1)
    if type3:
        issues.append(("WARNING", "Type3 フォントが埋め込まれています（IPA フォント等の TrueType フォントの導入を推奨）"))
    if norm(title)[:12] not in norm(text):
        issues.append(("WARNING", "1ページ目のテキスト抽出で表題を確認できません（フォント埋め込み・文字化けを目視確認してください）"))
    return issues


def build(files: list[Path], kinds: list[str], paper: str, out_dir: Path, keep_html: bool,
          force: bool, skip_validate: bool) -> list[BuildResult]:
    from playwright.sync_api import sync_playwright

    results: list[BuildResult] = []
    fonts = check_fonts()
    if shutil.which("fc-list") and not fonts:
        raise SystemExit("ERROR: 日本語フォント（Noto CJK JP または IPA フォント）が見つかりません。文字化けを防ぐためビルドを中止します。")

    valid_map: dict[Path, vq.FileResult] = {}
    if not skip_validate:
        rep = vq.validate_paths([str(f) for f in files])
        valid_map = {fr.path: fr for fr in rep.files}

    env = make_env()
    w, h, (mt, mr, mb, ml), _ = PAPERS[paper]
    with sync_playwright() as p:
        exe = find_chromium()
        browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        page = browser.new_page()
        for f in files:
            res = BuildResult(source=vq.relpath(f))
            results.append(res)
            fr = valid_map.get(f.resolve())
            if fr is not None and fr.errors and not force:
                res.errors.append(f"検査エラー {fr.errors} 件のためビルドしません（validate_questions.py で確認、--force で強制）")
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
            except Exception as e:  # noqa: BLE001
                res.errors.append(f"読み込み失敗: {e}")
                continue
            for kind in kinds:
                html_doc = render_html(env, data, kind, paper)
                pdf_path = output_path(f, edition_of(data, kind), paper, out_dir)
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
                    tmp.write(html_doc)
                    tmp_path = Path(tmp.name)
                try:
                    page.goto(tmp_path.as_uri(), wait_until="load")
                    page.wait_for_function("window.__renderDone === true", timeout=30000)
                    page.emulate_media(media="print")
                    for level, msg in page.evaluate(LAYOUT_JS):
                        (res.errors if level == "ERROR" else res.warnings).append(f"{kind}: {msg}")
                    title_short = html.escape(data["title"][:40])
                    pw, ph = (h, w) if is_kanagawa(data, kind) and is_tate(data) else (w, h)
                    page.pdf(
                        path=str(pdf_path),
                        width=f"{pw}mm", height=f"{ph}mm",
                        margin={"top": f"{mt}mm", "right": f"{mr}mm", "bottom": f"{mb}mm", "left": f"{ml}mm"},
                        print_background=True,
                        display_header_footer=True,
                        header_template='<div></div>' if is_kanagawa(data, kind) else (
                            '<div style="width:100%;font-size:7px;color:#888;padding:0 '
                            f'{ml}mm;text-align:right;font-family:\'IPAGothic\',\'Noto Sans CJK JP\',sans-serif;">'
                            f'{title_short}（{EDITION_TITLES[edition_of(data, kind)]}）</div>'
                        ),
                        footer_template=(
                            '<div style="width:100%;font-size:9px;color:#222;text-align:center;'
                            'font-family:\'IPAMincho\',\'Noto Serif CJK JP\',serif;">'
                            '－ <span class="pageNumber"></span> －</div>'
                        ) if is_kanagawa(data, kind) else (
                            '<div style="width:100%;font-size:8px;color:#666;text-align:center;'
                            'font-family:\'IPAGothic\',\'Noto Sans CJK JP\',sans-serif;">'
                            '<span class="pageNumber"></span> / <span class="totalPages"></span></div>'
                        ),
                    )
                    for level, msg in verify_pdf(pdf_path, data["title"]):
                        (res.errors if level == "ERROR" else res.warnings).append(f"{kind}: {msg}")
                    res.outputs.append(vq.relpath(pdf_path))
                    if keep_html:
                        shutil.copy(tmp_path, pdf_path.with_suffix(".html"))
                except Exception as e:  # noqa: BLE001
                    res.errors.append(f"{kind}: PDF 生成に失敗しました: {type(e).__name__}: {e}")
                finally:
                    tmp_path.unlink(missing_ok=True)
        browser.close()
    return results


def find_by_unit(unit_id: str) -> list[Path]:
    out = []
    for f in sorted(DATA.rglob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        if unit_id in d.get("unit_ids", []):
            out.append(f)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="問題セット JSON から PDF 教材を生成")
    ap.add_argument("paths", nargs="*", help="JSON ファイルまたはディレクトリ")
    ap.add_argument("--unit", action="append", default=[], help="単元 ID（複数指定可）を含むセットを data/ から探してビルド")
    ap.add_argument("--kind", choices=["questions", "answers", "both"], default="both")
    ap.add_argument("--paper", choices=list(PAPERS), default="A4")
    ap.add_argument("--out", default=str(OUTPUT), help="出力先ディレクトリ（既定: output/）")
    ap.add_argument("--keep-html", action="store_true", help="PDF と同じ場所に中間 HTML を残す")
    ap.add_argument("--force", action="store_true", help="検査エラーがあってもビルドする")
    ap.add_argument("--skip-validate", action="store_true", help="ビルド前の検査を省略する")
    ap.add_argument("--strict", action="store_true", help="レイアウト警告もエラーとして扱う")
    args = ap.parse_args(argv)

    files = [Path(p).resolve() for p in vq.collect_files(args.paths)] if args.paths else []
    for u in args.unit:
        found = find_by_unit(u)
        if not found:
            print(f"ERROR: 単元 {u} を含むセットが data/ にありません", file=sys.stderr)
            return 2
        files += [f.resolve() for f in found]
    files = list(dict.fromkeys(files))
    if not files:
        ap.error("ビルド対象を指定してください（パスまたは --unit）")

    kinds = ["questions", "answers"] if args.kind == "both" else [args.kind]
    results = build(files, kinds, args.paper, Path(args.out).resolve(), args.keep_html, args.force, args.skip_validate)

    n_err = n_warn = n_pdf = 0
    for r in results:
        status = "NG" if r.errors else ("△" if r.warnings else "OK")
        print(f"[{status}] {r.source}")
        for o in r.outputs:
            print(f"      → {o}")
        for e in r.errors:
            print(f"      ERROR: {e}")
        for wmsg in r.warnings:
            print(f"      WARNING: {wmsg}")
        n_err += len(r.errors)
        n_warn += len(r.warnings)
        n_pdf += len(r.outputs)
    print(f"PDF {n_pdf} 件生成 / エラー {n_err} 件 / 警告 {n_warn} 件")
    return 1 if n_err or (args.strict and n_warn) else 0


if __name__ == "__main__":
    sys.exit(main())
