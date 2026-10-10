"""validate_questions.py のテスト（ダミー JSON で検出できることを確認）。

実行: python -m unittest discover -s scripts/tests
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import validate_questions as vq  # noqa: E402

FIX = HERE / "fixtures"


def issues_of(rep, name):
    return [i for f in rep.files if f.path.name == name for i in f.issues]


class ValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rep = vq.validate_paths([str(FIX)])

    def cats(self, name, level="ERROR"):
        return [i.category for i in issues_of(self.rep, name) if i.level == level]

    def test_valid_file_alone_passes(self):
        rep = vq.validate_paths([str(FIX / "valid_set.json")])
        self.assertEqual(sum(f.errors for f in rep.files), 0)
        self.assertEqual(vq.main([str(FIX / "valid_set.json"), "--quiet"]), 0)

    def test_syntax_error_reports_line(self):
        iss = issues_of(self.rep, "syntax_error.json")
        self.assertEqual(iss[0].category, "json_syntax")
        self.assertEqual(iss[0].line, 5)

    def test_missing_required_field(self):
        msgs = [i.message for i in issues_of(self.rep, "invalid_schema.json") if i.category == "required"]
        self.assertTrue(any("解説" in m for m in msgs))
        self.assertTrue(any("正答の値が空" in m for m in msgs))

    def test_schema_and_consistency_errors(self):
        cats = self.cats("invalid_schema.json")
        for c in ("schema", "answer", "curriculum", "calc_check", "duplicate_id", "latex", "scoring"):
            self.assertIn(c, cats, c)

    def test_error_lines_point_into_file(self):
        for i in issues_of(self.rep, "invalid_schema.json"):
            self.assertIsNotNone(i.line, i.format())
            self.assertGreater(i.line, 1)

    def test_exact_duplicate_detected(self):
        self.assertIn("duplicate", self.cats("valid_set.json") + self.cats("duplicate_set.json"))

    def test_near_duplicate_warned(self):
        self.assertIn("similar", self.cats("near_duplicate_set.json", "WARNING") + self.cats("duplicate_set.json", "WARNING"))

    def test_strict_exit_code(self):
        self.assertEqual(vq.main([str(FIX), "--quiet"]), 1)

    def test_calc_check(self):
        self.assertIsNone(vq.run_calc_check({"expression": "solve(x**2-5*x+6, x)", "expected": "[2, 3]", "compare": "set"}))
        self.assertIsNone(vq.run_calc_check({"expression": "sqrt(12)", "expected": "2*sqrt(3)"}))
        self.assertIsNone(vq.run_calc_check({"expression": "solve([x+y-5, x-y-1], [x, y])", "expected": "{x: 3, y: 2}"}))
        self.assertIsNotNone(vq.run_calc_check({"expression": "1/3", "expected": "0.33"}))

    def test_calc_check_is_sandboxed(self):
        for bad in ("__import__('os').system('true')", "open('x')", "(1).__class__", "x.subs(x, 1)"):
            msg = vq.run_calc_check({"expression": bad, "expected": "0"})
            self.assertIsNotNone(msg)
            self.assertIn("評価できません", msg)

    def test_similarity_normalization(self):
        self.assertEqual(vq.normalize_text("Ｘ＋１、 です。"), vq.normalize_text("x+1です"))


if __name__ == "__main__":
    unittest.main()
