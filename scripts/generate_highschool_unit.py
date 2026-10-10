#!/usr/bin/env python3
"""単元パック（授業プリント＋問題プリント）を一括生成する（高校が主対象。中学・入試対策の単元にも使える）。

  python scripts/generate_highschool_unit.py --list                     # 作成済みの単元パック
  python scripts/generate_highschool_unit.py --unit HS-MATH1-U03        # 1単元（既定 60 問）
  python scripts/generate_highschool_unit.py --unit HS-MATH1-U03 --count 100
  python scripts/generate_highschool_unit.py --all --count 80
  python scripts/generate_highschool_unit.py --all --no-pdf --note "レビュー指摘 No.5 対応"

1単元あたり次の2つのセットを data/hs_packs/<単元ID>/（中学の単元は data/jh_packs/<単元ID>/）に書き出す。

  lesson.json    授業プリント（概念導入・定義/定理・証明/導出・例題・板書案・教師の指導ガイド・確認問題）
  exercise.json  問題プリント（A 基本確認／B 標準演習／C 思考力・記述応用／D 典型誤答訂正、50〜100 問以上）

その後、generate_batch.py と同じ流れで、変更履歴の記録 → 自動検査（data/ 全体と照合）→ auto_checked の付与
→ PDF（授業：教師用・生徒用、問題：問題冊子・解答解説冊子）→ カタログ・レポート を行う。
"""
from __future__ import annotations

import argparse
import datetime as dt
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

import generate_batch as gb  # noqa: E402
import hs_pack_lib as hl  # noqa: E402
import validate_questions as vq  # noqa: E402
from banks._common import UNITS  # noqa: E402

PACK_DIR = HERE / "hs_packs"
MIN_COUNT = vq.MIN_PACK_QUESTIONS


def list_packs() -> dict[str, str]:
    """{単元ID: モジュール名}"""
    out = {}
    for f in sorted(PACK_DIR.glob("*.py")):
        if f.name.startswith("_"):
            continue
        m = importlib.import_module(f"hs_packs.{f.stem}")
        out[m.UNIT_ID] = f.stem
    return out


def unit_context(unit: dict, readiness: list, mod=None) -> dict:
    """前提条件・発展への接続。curriculum_map.json の定義を使い、なければパックの PREREQUISITES / EXTENSIONS を使う。"""
    def link(x):
        if isinstance(x, (tuple, list)):
            x = {"unit_id": x[0], "point": x[1]}
        if x["unit_id"] not in UNITS:
            raise SystemExit(f"{unit['unit_id']}: 前提・発展の単元 ID {x['unit_id']} が curriculum_map.json にありません")
        u = UNITS[x["unit_id"]]
        d = {"unit_id": x["unit_id"], "point": x["point"]}
        if u.get("title"):
            d["title"] = u["title"]
        return d
    pre = unit.get("prerequisites") or getattr(mod, "PREREQUISITES", [])
    ext = unit.get("extensions") or getattr(mod, "EXTENSIONS", [])
    ctx = {"prerequisites": [link(x) for x in pre], "extensions": [link(x) for x in ext]}
    if readiness:
        ctx["readiness_check"] = list(readiness)
    return ctx


def build_specs(unit_id: str, mod, count: int) -> tuple[dict, dict]:
    unit = UNITS[unit_id]
    items_by_level = hl.run_generators(unit_id, mod.GENERATORS, max(count, MIN_COUNT))
    pack_id = f"{unit_id}-PACK"
    lesson_id, ex_id = f"{unit_id}-LESSON", f"{unit_id}-EX"
    lesson = dict(mod.LESSON)
    readiness = lesson.pop("readiness", [])
    ctx = unit_context(unit, readiness, mod)
    jh = unit.get("stage") == "junior_high"
    track, root = ("jh_pack", "data/jh_packs") if jh else ("hs_pack", "data/hs_packs")
    common = {
        "track": track, "stage": unit.get("stage", "high_school"), "subject": unit["subject"], "grade": unit["grade"],
        "unit_ids": [unit_id], "default_skills": unit["default_skills"], "pack_id": pack_id, "unit_context": ctx,
        "schema_version": "2.0.0", "labels": "kana",
    }
    if unit.get("course"):
        common["course"] = unit["course"]
    title = getattr(mod, "TITLE", unit["title"])
    lesson_spec = dict(common, set_id=lesson_id, print_type="lesson", pair_set_id=ex_id, title=f"{title}　授業プリント",
                       subtitle=f"{unit['domain']}｜{'・'.join(unit['topics'][:4])}", lesson=lesson, items=[],
                       out=f"{root}/{unit_id.lower()}/lesson.json")
    items, sections, plan = [], [], {}
    for lv, (letter, name, desc) in hl.LEVELS.items():
        lv_items = items_by_level[lv]
        plan[lv] = len(lv_items)
        sections.append({"id": f"LV-{letter}", "title": f"{letter}　{name}", "instructions": desc})
        for k, it in enumerate(lv_items, 1):
            it["sec"] = f"LV-{letter}"
            it["no"] = f"{letter}-{k:02d}"
            items.append(it)
    ex_spec = dict(common, set_id=ex_id, print_type="exercise", pair_set_id=lesson_id, title=f"{title}　問題プリント",
                   subtitle=f"A 基本確認 {plan['basic_check']}問・B 標準演習 {plan['standard_practice']}問・C 思考力・記述 {plan['thinking_writing']}問・D 典型誤答訂正 {plan['error_correction']}問",
                   sections=sections, exercise_plan=plan, items=items,
                   instructions=["A から順に取り組み、B 以降は解答解説冊子の「思考の糸口」を読んでから解き直しましょう。",
                                 "C・D は途中の考え方を答案として書きなさい。部分点の基準は解答解説冊子にあります。",
                                 "答えが分数になるときは既約分数、根号を含むときは根号の中をできるだけ小さい自然数にしなさい。"],
                   out=f"{root}/{unit_id.lower()}/exercise.json")
    return lesson_spec, ex_spec


def run(unit_ids: list[str], count: int, pdf: bool, today: str, note: str | None) -> dict:
    packs = list_packs()
    written: list[Path] = []
    summary = {"new": 0, "updated": 0, "unchanged": 0}
    for uid in unit_ids:
        if uid not in packs:
            raise SystemExit(f"単元パック {uid} はまだ作成されていません（scripts/hs_packs/ にモジュールを追加してください）。作成済み: {', '.join(packs)}")
        mod = importlib.import_module(f"hs_packs.{packs[uid]}")
        for spec in build_specs(uid, mod, count):
            path = (ROOT / spec["out"]).resolve()
            data = gb.expand_set(spec)
            data, state = gb.merge_with_existing(data, path, "HS", today, note, author="generate_highschool_unit.py")
            summary[state] += 1
            gb.write_json(path, data)
            written.append(path)
    print(f"== 単元パック: {len(unit_ids)} 単元 / {len(written)} セット（新規 {summary['new']} / 更新 {summary['updated']} / 変更なし {summary['unchanged']}）")

    rep = vq.validate_paths([str(p) for p in written], corpus=[str(ROOT / "data")])
    errs = sum(f.errors for f in rep.files)
    if errs:
        for f in rep.files:
            for i in f.issues:
                if i.level == "ERROR":
                    print("   " + i.format())
        print(f"   検査: エラー {errs} 件 → PDF ビルドを中止しました")
        return {"ok": False, "errors": errs}
    gb.promote_checked(written, rep, today)
    rep = vq.validate_paths([str(p) for p in written], corpus=[str(ROOT / "data")])
    vq.stamp_files(rep)
    warns = sum(f.warnings for f in rep.files)
    for f in rep.files:
        for i in f.issues:
            print("   " + i.format())
    stats = []
    for p in written:
        d = json.loads(p.read_text(encoding="utf-8"))
        if d.get("print_type") == "exercise":
            ps = sorted({x for q in d["questions"] for x in q.get("perspectives", [])})
            stats.append((d["unit_ids"][0], len(d["questions"]), d["exercise_plan"], ps))
    for uid, n, plan, ps in stats:
        print(f"   {uid}: 問題 {n} 問 {plan} 観点 {len(ps)} 種")
    print(f"   検査: {len(written)} ファイル / エラー 0 件 / 警告 {warns} 件")

    pdf_results = []
    if pdf:
        import build_pdf
        res = build_pdf.build(written, ["questions", "answers"], "A4", build_pdf.OUTPUT, False, False, True)
        for r in res:
            pdf_results.append({"source": r.source, "outputs": r.outputs, "errors": r.errors, "warnings": r.warnings})
            for e in r.errors:
                print(f"   PDF ERROR {r.source}: {e}")
        print(f"   PDF: {sum(len(r['outputs']) for r in pdf_results)} 件生成 / エラー {sum(len(r['errors']) for r in pdf_results)} 件")
    report = {"generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(), "units": unit_ids,
              "files": [vq.relpath(p) for p in written], "warnings": warns,
              "exercise_stats": [{"unit_id": u, "questions": n, "plan": pl, "perspectives": ps} for u, n, pl, ps in stats],
              "pdf": pdf_results, "ok": all(not r["errors"] for r in pdf_results)}
    if pdf:
        rdir = ROOT / "output" / "reports"
        rdir.mkdir(parents=True, exist_ok=True)
        (rdir / "hs_packs_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        gb.write_catalog()
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="高校の単元パック（授業プリント＋問題プリント）を一括生成する")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--unit", nargs="+", help="単元 ID（複数可）")
    g.add_argument("--all", action="store_true", help="作成済みのすべての単元パック")
    g.add_argument("--list", action="store_true", help="作成済みの単元パックを表示")
    ap.add_argument("--count", type=int, default=60, help=f"1単元あたりの問題数の目安（{MIN_COUNT} 以上。既定 60）")
    ap.add_argument("--no-pdf", action="store_true")
    ap.add_argument("--note", help="変更履歴に記録する変更理由")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    args = ap.parse_args(argv)
    packs = list_packs()
    if args.list:
        for uid in packs:
            u = UNITS[uid]
            print(f"{uid}\t{u['title']}")
        return 0
    if args.count < MIN_COUNT:
        ap.error(f"--count は {MIN_COUNT} 以上にしてください")
    ids = list(packs) if args.all else args.unit
    r = run(ids, args.count, not args.no_pdf, args.date, args.note)
    return 0 if r.get("ok", False) or (args.no_pdf and "errors" not in r) else 1


if __name__ == "__main__":
    sys.exit(main())
