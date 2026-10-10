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


def choice_cols(choices) -> int:
    m = max((visual_len(c.get("text", "")) for c in choices), default=0)
    if m <= 8 and len(choices) in (4, 8):
        return 4
    if m <= 19:
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

def prepare(data: dict) -> tuple[list, list]:
    stimuli = {s["id"]: s for s in data.get("stimuli", [])}
    sections = {s["id"]: s for s in data.get("sections", [])}
    groups: list[dict] = []
    shown: set[str] = set()
    cur_key = object()
    for i, q in enumerate(data["questions"]):
        q = dict(q)
        q["_number"] = q.get("number") or f"{i + 1}"
        q["_long"] = len(q.get("stem", "")) > 500 or (q.get("answer_space") or {}).get("lines", 0) > 10 or \
            (q.get("answer_space") or {}).get("char_grid", 0) > 200 or bool(q.get("stimulus") and len(q["stimulus"].get("content", "")) > 600)
        q["_long_exp"] = len(q.get("explanation", "")) > 700
        sec_id = q.get("section")
        if sec_id != cur_key:
            sec = sections.get(sec_id) if sec_id else None
            groups.append({"section": sec, "items": [], "page_break": bool(sec and sec.get("page_break"))})
            cur_key = sec_id
            if sec:
                for ref in sec.get("stimulus_refs", []):
                    if ref in stimuli and ref not in shown:
                        groups[-1]["items"].append({"kind": "stimulus", "stimulus": stimuli[ref]})
                        shown.add(ref)
        ref = q.get("stimulus_ref")
        if ref and ref in stimuli and ref not in shown:
            groups[-1]["items"].append({"kind": "stimulus", "stimulus": stimuli[ref]})
            shown.add(ref)
        groups[-1]["items"].append({"kind": "question", "question": q})
    if groups:
        groups[0]["page_break"] = False  # 表紙の直後では改ページしない
    units = [UNITS[u] for u in data.get("unit_ids", []) if u in UNITS]
    return groups, units


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
        "choice_cols": choice_cols,
        "num": num,
        "answer_display": answer_display,
        "truncate_plain": truncate_plain,
        "grade_label": lambda c: MASTERS["grade"].get(c, c),
        "subject_label": lambda c: MASTERS["subject"].get(c, c),
        "skill_label": lambda c: MASTERS["skill"].get(c, c),
        "aspect_label": lambda c: MASTERS["aspect"].get(c, c),
        "difficulty_label": lambda c: MASTERS["difficulty"].get(c, c),
        "status_label": lambda c: MASTERS["status"].get(c, c),
        "track_label": lambda c: MASTERS["track"].get(c, c),
    })
    return env


def render_html(env, data: dict, kind: str, paper: str) -> str:
    w, h, (mt, mr, mb, ml), fs = PAPERS[paper]
    groups, units = prepare(data)
    build = data.get("build", {})
    tpl = env.get_template("question_template.html" if kind == "questions" else "answer_template.html")
    page_css = f"@page {{ size: {w}mm {h}mm; }}\n:root {{ --fs: {fs}; }}"
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
        doc_title=f"{data['title']}（{'問題' if kind == 'questions' else '解答・解説'}）",
        show_points=build.get("show_points", True),
        show_difficulty=build.get("show_difficulty", data.get("track") not in ("mock_exam",)),
        answer_sheet=data.get("track") == "mock_exam",
    )


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
                pdf_path = output_path(f, kind, paper, out_dir)
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
                    page.pdf(
                        path=str(pdf_path),
                        width=f"{w}mm", height=f"{h}mm",
                        margin={"top": f"{mt}mm", "right": f"{mr}mm", "bottom": f"{mb}mm", "left": f"{ml}mm"},
                        print_background=True,
                        display_header_footer=True,
                        header_template=(
                            '<div style="width:100%;font-size:7px;color:#888;padding:0 '
                            f'{ml}mm;text-align:right;font-family:\'IPAGothic\',\'Noto Sans CJK JP\',sans-serif;">'
                            f'{title_short}{"（解答・解説）" if kind == "answers" else ""}</div>'
                        ),
                        footer_template=(
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
