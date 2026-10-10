#!/usr/bin/env python3
"""作問バンク（scripts/banks/）から問題マスター JSON を生成し、検査と PDF ビルドまで一括実行する。

  python scripts/generate_batch.py --phase 1            # パイロット
  python scripts/generate_batch.py --phase 2 3 4 5      # 複数フェーズ
  python scripts/generate_batch.py --phase 2 --only JH-MATH-G1-U01-S1
  python scripts/generate_batch.py --phase 1 --tablet   # タブレット版 PDF も作る
  python scripts/generate_batch.py --phase 2 --no-pdf   # PDF を作らない（検査は必ず行う）

各セットについて次を順に行う。
  1. バンクの定義をスキーマ準拠の JSON に展開（ID 採番・選択肢の決定的シャッフル・既定値の補完）
  2. 既存マスターとの差分を取り、内容が変わったときだけ revision_history に版を追加
     （教科担当者のレビュー状態は、その問題の内容が変わっていなければ引き継ぐ）
  3. validate_questions.py で data/ 全体を対象に検査（重複検知は既存データも含めて行う）
  4. エラーが無ければ draft の問題を auto_checked に更新し、検査結果を validation に記録
  5. build_pdf.py で問題冊子・解答解説冊子を output/ に生成
  6. output/reports/phase{N}_report.json に結果を保存
"""
from __future__ import annotations

import argparse
import copy
import datetime as dt
import hashlib
import importlib
import json
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import validate_questions as vq  # noqa: E402
from banks import PHASE_MODULES  # noqa: E402
from banks._common import COPYRIGHT_HOLDER, LICENSE, UNITS  # noqa: E402

SCHEMA_VERSION = "1.0.0"
GENERATOR = "generate_batch.py"
LABELS = {
    "kana": ["ア", "イ", "ウ", "エ", "オ", "カ", "キ", "ク", "ケ", "コ"],
    "num": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "alpha": ["A", "B", "C", "D", "E", "F", "G", "H"],
}
TYPE_MAP = {
    "mc": "multiple_choice", "ms": "multiple_select", "tf": "true_false", "num": "numeric",
    "sa": "short_answer", "fill": "fill_in_blank", "ord": "ordering", "desc": "descriptive",
    "proof": "proof", "essay": "essay",
}
THINKING_SKILLS = {"thinking", "data_interpretation", "writing", "essay", "proof", "experiment"}
REVIEW_STATES = {"self_reviewed", "expert_reviewed", "approved"}


def level_of(score: int) -> str:
    return "basic" if score <= 2 else ("standard" if score == 3 else "advanced")


def _rng(*parts) -> random.Random:
    seed = int(hashlib.sha256("|".join(map(str, parts)).encode()).hexdigest()[:16], 16)
    return random.Random(seed)


def expand_item(spec: dict, item: dict, n: int) -> dict:
    t = item["t"]
    qid = f"{spec['set_id']}-Q{n:03d}"
    unit_id = item.get("u", spec["unit_ids"][0])
    unit = UNITS.get(unit_id, {})
    skills = item.get("k") or spec.get("default_skills") or unit.get("default_skills") or ["knowledge"]
    score = int(item.get("d", 2))
    if "asp" in item:
        aspect = "knowledge_skill" if item["asp"] == "k" else "thinking_judgment_expression"
    else:
        aspect = "thinking_judgment_expression" if (THINKING_SKILLS & set(skills) or score >= 4) else "knowledge_skill"
    labels = LABELS[item.get("labels", spec.get("labels", "kana"))]

    q: dict = {
        "id": qid,
    }
    if item.get("no"):
        q["number"] = str(item["no"])
    if item.get("sec"):
        q["section"] = item["sec"]
    q.update({
        "grade": item.get("grade", unit.get("grade", spec["grade"])),
        "subject": item.get("subj", unit.get("subject", spec["subject"])),
        "unit_id": unit_id,
    })
    if item.get("tp"):
        q["topic"] = item["tp"]
    q.update({
        "skills": list(dict.fromkeys(skills)),
        "evaluation_aspect": aspect,
        "question_type": TYPE_MAP[t],
    })
    if item.get("st"):
        q["stimulus_ref"] = item["st"]
    if item.get("stim"):
        q["stimulus"] = item["stim"]
    q["stem"] = item["s"]
    if item.get("fig"):
        q["figure"] = item["fig"]
    if item.get("tbl"):
        q["table"] = item["tbl"]

    answer: dict
    rng = _rng(spec["set_id"], n, item["s"])
    if t in ("mc", "ms", "ord"):
        texts = item["c"]
        idx = list(range(len(texts)))
        if not item.get("keep"):
            rng.shuffle(idx)
            if t == "ord":
                # 並べ替えで偶然正しい順になったら1回ずらす
                if idx == sorted(idx) and len(idx) > 1:
                    idx = idx[1:] + idx[:1]
        q["choices"] = [{"label": labels[pos], "text": texts[i]} for pos, i in enumerate(idx)]
        label_of = {i: labels[pos] for pos, i in enumerate(idx)}
        if t == "mc":
            correct = item.get("ai", 0)
            answer = {"value": label_of[correct]}
        elif t == "ms":
            answer = {"value": sorted((label_of[i] for i in range(item["n_correct"])), key=labels.index)}
        else:
            answer = {"value": [label_of[i] for i in range(len(texts))]}
    elif t == "tf":
        q["choices"] = [{"label": "○", "text": "正しい"}, {"label": "×", "text": "誤り"}]
        answer = {"value": "○" if item["truth"] else "×"}
    else:
        answer = {"value": item["a"]}
    if item.get("v"):
        answer["accepted"] = list(item["v"])
    if item.get("disp"):
        answer["display"] = item["disp"]
    if item.get("unit"):
        answer["unit"] = item["unit"]
    q["answer"] = answer
    q["explanation"] = item["e"]

    points = item.get("p", spec.get("default_points", 5))
    if t in ("desc", "proof", "essay"):
        rubric = [{"criterion": c, "points": p} for c, p in item["r"]]
        method = "rubric" if abs(sum(r["points"] for r in rubric) - points) < 1e-9 else "partial"
        if "p" not in item and method == "partial":
            points = sum(r["points"] for r in rubric)
            method = "rubric"
        q["scoring"] = {"points": points, "method": method, "rubric": rubric}
    elif t in ("ms", "ord"):
        q["scoring"] = {"points": points, "method": "all_or_nothing", "notes": "完全一致で正解"}
    else:
        q["scoring"] = {"points": points, "method": "exact"}
        if item.get("v"):
            q["scoring"]["notes"] = "別解欄の表記も正解とする"
    q["difficulty"] = {"level": level_of(score), "score": score}

    sp = {}
    if item.get("lines"):
        sp["lines"] = item["lines"]
    if item.get("grid"):
        sp["char_grid"] = item["grid"]
    if item.get("h"):
        sp["height_mm"] = item["h"]
    if sp:
        q["answer_space"] = sp
    if item.get("chk"):
        c = item["chk"]
        q["calc_check"] = {"expression": c[0], "expected": c[1]}
        if len(c) > 2 and c[2]:
            q["calc_check"]["compare"] = c[2]
        if len(c) > 3:
            q["calc_check"]["target"] = c[3]
    # --- 版2.0：問題プリント用の拡張項目 ---
    if item.get("lvl"):
        q["exercise_level"] = item["lvl"]
    if item.get("ps"):
        q["perspectives"] = list(dict.fromkeys(item["ps"]))
    if item.get("vg"):
        q["variant_group"] = item["vg"]
    if item.get("rel"):
        q["related_units"] = list(item["rel"])
    if item.get("ap"):
        ed = {"approach": item["ap"], "steps": list(item.get("steps") or [item["e"]])}
        if item.get("alt"):
            ed["alternatives"] = list(item["alt"])
        if item.get("pc"):
            ed["partial_credit"] = [{"point": a, "points": b} for a, b in item["pc"]]
        if item.get("pit"):
            ed["pitfalls"] = list(item["pit"])
        if item.get("ver"):
            ed["verification"] = item["ver"]
        q["explanation_detail"] = ed
    if item.get("why") and q.get("choices"):
        by_text = {c["text"]: c["label"] for c in q["choices"]}
        correct = q["answer"]["value"] if isinstance(q["answer"]["value"], list) else [q["answer"]["value"]]
        da = []
        for text, reason in item["why"].items():
            lab = by_text.get(text)
            if lab is None:
                raise ValueError(f"{qid}: 誤答分析の選択肢「{text}」が選択肢にありません")
            if lab in correct:
                raise ValueError(f"{qid}: 正答の選択肢に誤答分析が付いています")
            da.append({"label": lab, "why_wrong": reason[0] if isinstance(reason, tuple) else reason}
                      | ({"misconception": reason[1]} if isinstance(reason, tuple) else {}))
        q["distractor_analysis"] = sorted(da, key=lambda x: labels.index(x["label"]) if x["label"] in labels else 99)
    if item.get("err"):
        e = item["err"]
        q["error_analysis"] = {"erroneous_solution": e["sol"], "error_step": e["step"], "error_type": e["type"],
                               "why_tempting": e["tempt"], "correction": e["fix"]}
    if item.get("tags"):
        q["tags"] = list(item["tags"])
    q["verification"] = {"status": "draft"}
    cp = {"status": item.get("cp", "original"), "holder": COPYRIGHT_HOLDER}
    if item.get("src"):
        cp["source"] = item["src"]
    if cp["status"] == "public_domain":
        cp["notes"] = "原文は著作権の保護期間が満了した古典。問題文・設問・解説はオリジナル。"
    q["copyright"] = cp
    return q


def expand_set(spec: dict) -> dict:
    data = {
        "schema_version": spec.get("schema_version", SCHEMA_VERSION),
        "set_id": spec["set_id"],
        "title": spec["title"],
    }
    if spec.get("subtitle"):
        data["subtitle"] = spec["subtitle"]
    if spec.get("description"):
        data["description"] = spec["description"]
    data.update({
        "track": spec["track"],
        "stage": spec["stage"],
        "subject": spec["subject"],
    })
    if spec.get("course"):
        data["course"] = spec["course"]
    data["grade"] = spec["grade"]
    data["unit_ids"] = spec["unit_ids"]
    for key in ("print_type", "pack_id", "pair_set_id", "unit_context", "lesson", "exercise_plan",
                "time_limit_minutes", "instructions", "exam_spec", "sections", "stimuli", "build"):
        if spec.get(key):
            data[key] = copy.deepcopy(spec[key])
    data["questions"] = [expand_item(spec, it, i) for i, it in enumerate(spec["items"], 1)]
    if data["questions"]:
        if spec.get("total_points") and spec["total_points"] is not True:
            data["total_points"] = spec["total_points"]
        else:
            data["total_points"] = sum(q["scoring"]["points"] for q in data["questions"])
    data["copyright"] = {
        "status": spec.get("copyright_status", "original"),
        "holder": COPYRIGHT_HOLDER,
        "license": LICENSE,
    }
    if spec.get("copyright_notes"):
        data["copyright"]["notes"] = spec["copyright_notes"]
    return data


# --------------------------------------------------------------------------
# 版管理
# --------------------------------------------------------------------------

def _q_hash(q: dict) -> str:
    body = {k: v for k, v in q.items() if k != "verification"}
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def set_hash(data: dict) -> str:
    body = {k: v for k, v in data.items() if k not in ("revision_history", "validation")}
    body["questions"] = [_q_hash(q) for q in data["questions"]]
    return hashlib.sha256(json.dumps(body, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def merge_with_existing(new: dict, path: Path, phase, today: str, note: str | None = None, author: str | None = None) -> tuple[dict, str]:
    """既存ファイルと比較して revision_history を更新する。戻り値の第2要素は変更概要。"""
    h = set_hash(new)
    author = author or f"{GENERATOR}（フェーズ{phase}）"
    if not path.exists():
        new["revision_history"] = [{
            "version": "1.0.0", "date": today, "author": author,
            "changes": (f"初版作成（{len(new['questions'])}問）。自動検査（スキーマ・重複・検算）実施予定。" if new["questions"]
                        else "初版作成。自動検査（スキーマ・構成）実施予定。"),
            "content_hash": h,
        }]
        return new, "new"
    old = json.loads(path.read_text(encoding="utf-8"))
    hist = old.get("revision_history") or []
    old_q = {q["id"]: q for q in old.get("questions", [])}
    # 内容が同じ問題はレビュー状態を引き継ぐ
    for q in new["questions"]:
        oq = old_q.get(q["id"])
        if oq and _q_hash(oq) == _q_hash(q):
            q["verification"] = oq.get("verification", q["verification"])
    if hist and hist[-1].get("content_hash") == h:
        new["revision_history"] = hist
        if old.get("validation"):
            new["validation"] = old["validation"]
        return new, "unchanged"
    added = [i for i in (q["id"] for q in new["questions"]) if i not in old_q]
    new_ids = {q["id"] for q in new["questions"]}
    removed = [i for i in old_q if i not in new_ids]
    changed = [q["id"] for q in new["questions"] if q["id"] in old_q and _q_hash(old_q[q["id"]]) != _q_hash(q)]
    parts = []
    if added:
        parts.append(f"追加 {len(added)} 問")
    if removed:
        parts.append(f"削除 {len(removed)} 問")
    if changed:
        parts.append(f"修正 {len(changed)} 問（{', '.join(c.rsplit('-', 1)[-1] for c in changed[:10])}{' 他' if len(changed) > 10 else ''}）")
    if not parts:
        parts.append("セット情報（表題・構成・資料等）の更新")
    last = hist[-1]["version"] if hist else "0.0.0"
    major, minor, patch = (int(x) for x in last.split("."))
    version = f"{major}.{minor + 1}.0" if (added or removed or changed) else f"{major}.{minor}.{patch + 1}"
    for q in new["questions"]:
        if q["id"] in changed and q["verification"].get("status") in REVIEW_STATES:
            q["verification"] = {"status": "draft", "notes": "内容修正のため再レビューが必要"}
    changes = "；".join(parts)
    if note:
        changes = f"{note}：{changes}"
    new["revision_history"] = hist + [{
        "version": version, "date": today, "author": author,
        "changes": changes, "content_hash": h,
    }]
    return new, "updated"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")  # 一時ファイル経由で置き換え（並行実行中の検査が書きかけを読まないように）
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def promote_checked(paths: list[Path], rep: vq.Reporter, today: str) -> None:
    for fr in rep.files:
        if fr.path not in paths or fr.errors:
            continue
        data = json.loads(fr.path.read_text(encoding="utf-8"))
        changed = False
        for q in data["questions"]:
            v = q["verification"]
            if v.get("status") == "draft":
                methods = ["schema", "answer_consistency", "duplicate"] + (["calc_check"] if q.get("calc_check") else [])
                q["verification"] = {
                    "status": "auto_checked",
                    "checked_by": f"validate_questions.py v{vq.VALIDATOR_VERSION}",
                    "checked_at": today,
                    "methods": methods,
                    "notes": "AI による作成。教科担当者による内容レビュー（expert_review）待ち。",
                }
                changed = True
        if changed:
            write_json(fr.path, data)


# --------------------------------------------------------------------------
# 実行
# --------------------------------------------------------------------------

def load_specs(phase: int) -> list[dict]:
    specs = []
    for mod in PHASE_MODULES[phase]:
        if not (HERE / "banks" / f"{mod}.py").exists():
            print(f"   WARNING: 作問バンク banks/{mod}.py がありません（スキップ）")
            continue
        m = importlib.import_module(f"banks.{mod}")
        specs.extend(m.SETS)
    return specs


def run_phase(phase: int, only: set[str] | None, pdf: bool, tablet: bool, today: str, note: str | None = None) -> dict:
    specs = load_specs(phase)
    if only:
        specs = [s for s in specs if s["set_id"] in only]
    print(f"== フェーズ {phase}: {len(specs)} セット ==")
    written: list[Path] = []
    summary = {"new": 0, "updated": 0, "unchanged": 0}
    for spec in specs:
        path = (ROOT / spec["out"]).resolve()
        data = expand_set(spec)
        data, state = merge_with_existing(data, path, phase, today, note)
        summary[state] += 1
        write_json(path, data)
        written.append(path)
    print(f"   生成: 新規 {summary['new']} / 更新 {summary['updated']} / 変更なし {summary['unchanged']}")

    # 検査（重複検知は data/ 全体と比較）
    rep = vq.validate_paths([str(p) for p in written], corpus=[str(ROOT / "data")])
    errs = sum(f.errors for f in rep.files)
    warns = sum(f.warnings for f in rep.files)
    if errs:
        for f in rep.files:
            for i in f.issues:
                if i.level == "ERROR":
                    print("   " + i.format())
        print(f"   検査: エラー {errs} 件 → PDF ビルドを中止しました")
        return {"phase": phase, "sets": len(specs), "errors": errs, "warnings": warns, "pdf": [], "ok": False}
    promote_checked(written, rep, today)
    rep = vq.validate_paths([str(p) for p in written], corpus=[str(ROOT / "data")])
    vq.stamp_files(rep)
    warns = sum(f.warnings for f in rep.files)
    warn_lines = [i.format() for f in rep.files for i in f.issues]
    for line in warn_lines[:50]:
        print("   " + line)
    nq = sum(len(json.loads(p.read_text(encoding="utf-8"))["questions"]) for p in written)
    print(f"   検査: {len(written)} ファイル / {nq} 問 / エラー 0 件 / 警告 {warns} 件")

    pdf_results = []
    build_errors = 0
    if pdf:
        import build_pdf
        papers = ["A4"] + (["tablet"] if tablet else [])
        for paper in papers:
            res = build_pdf.build(written, ["questions", "answers"], paper, build_pdf.OUTPUT, False, False, True)
            for r in res:
                pdf_results.append({"source": r.source, "paper": paper, "outputs": r.outputs, "errors": r.errors, "warnings": r.warnings})
                build_errors += len(r.errors)
                for e in r.errors:
                    print(f"   PDF ERROR {r.source}: {e}")
        print(f"   PDF: {sum(len(r['outputs']) for r in pdf_results)} 件生成 / エラー {build_errors} 件")

    report = {
        "phase": phase,
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "sets": len(specs),
        "questions": nq,
        "files": [vq.relpath(p) for p in written],
        "validation": {"errors": 0, "warnings": warns, "issues": warn_lines},
        "pdf": pdf_results,
        "ok": build_errors == 0,
    }
    rdir = ROOT / "output" / "reports"
    rdir.mkdir(parents=True, exist_ok=True)
    # フェーズ全体を PDF まで処理したときだけ正式なレポートを更新する
    name = f"phase{phase}_report.json" if (pdf and not only) else f"phase{phase}_partial_report.json"
    (rdir / name).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


TRACK_ORDER = ["pilot", "mock_exam", "junior_high", "tokushoku", "high_school", "common_test", "second_stage"]


def write_catalog() -> Path:
    """data/ 以下の全セットの一覧（版・検査結果・PDF へのリンク）を output/CATALOG.md に書き出す。"""
    import build_pdf

    labels = build_pdf.MASTERS["track"]
    rows: dict[str, list] = {}
    totals = {"sets": 0, "questions": 0}
    for f in sorted((ROOT / "data").rglob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(d, dict) or "questions" not in d:
            continue
        status = {}
        for q in d["questions"]:
            st = q.get("verification", {}).get("status", "?")
            status[st] = status.get(st, 0) + 1
        pdfs = []
        for kind, label in (("questions", "問題"), ("answers", "解答"), ("questions_tablet", "問題(タブレット)"), ("answers_tablet", "解答(タブレット)")):
            k, _, paper = kind.partition("_")
            pp = build_pdf.output_path(f, k, paper or "A4", build_pdf.OUTPUT)
            if pp.exists():
                pdfs.append(f"[{label}]({pp.relative_to(build_pdf.OUTPUT).as_posix()})")
        rows.setdefault(d.get("track", "?"), []).append(
            f"| {d['set_id']} | {d['title']} | {d['grade']} | {len(d['questions'])} | {d.get('total_points', '')} | "
            f"{d['revision_history'][-1]['version']} | {d.get('validation', {}).get('result', '未検査')} | "
            f"{'・'.join(f'{k} {v}' for k, v in sorted(status.items()))} | {' '.join(pdfs)} |")
        totals["sets"] += 1
        totals["questions"] += len(d["questions"])
    lines = ["# 教材カタログ", "",
             f"全 {totals['sets']} セット・{totals['questions']} 問（`scripts/generate_batch.py` が自動生成。手で編集しないこと）", "",
             "検証状態 `auto_checked` は自動検査（スキーマ・整合性・重複・検算）に合格した状態です。教科担当者のレビュー（`expert_reviewed`）を経てから配布してください。", ""]
    for tr in TRACK_ORDER + sorted(set(rows) - set(TRACK_ORDER)):
        if tr not in rows:
            continue
        lines += [f"## {labels.get(tr, tr)}（{len(rows[tr])} セット）", "",
                  "| セットID | 表題 | 学年 | 問題数 | 配点 | 版 | 自動検査 | 検証状態 | PDF |", "|---|---|---|---|---|---|---|---|---|"]
        lines += rows[tr] + [""]
    out = build_pdf.OUTPUT / "CATALOG.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="作問バンクから問題マスターを生成し、検査・PDF ビルドを行う")
    ap.add_argument("--phase", type=int, nargs="+", required=True, choices=sorted(PHASE_MODULES))
    ap.add_argument("--only", nargs="*", help="指定した set_id だけを処理")
    ap.add_argument("--no-pdf", action="store_true", help="PDF をビルドしない")
    ap.add_argument("--tablet", action="store_true", help="タブレット版 PDF も生成する")
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="変更履歴に記録する日付（既定: 今日）")
    ap.add_argument("--note", help="変更履歴に記録する変更理由（例: レビュー指摘番号）")
    args = ap.parse_args(argv)
    ok = True
    for ph in args.phase:
        r = run_phase(ph, set(args.only) if args.only else None, not args.no_pdf, args.tablet, args.date, args.note)
        ok = ok and r["ok"]
    print(f"カタログを更新しました: {vq.relpath(write_catalog())}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
