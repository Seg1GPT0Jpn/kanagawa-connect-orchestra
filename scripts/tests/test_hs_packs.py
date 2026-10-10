"""高校 単元パックの作問ライブラリと各パックの問題数・段階・観点のテスト。"""
import importlib
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import hs_pack_lib as hl  # noqa: E402
import generate_highschool_unit as ghu  # noqa: E402

REQUIRED = {"computation", "condition_check", "cross_unit", "written_reasoning", "common_error"}


class AllocateTest(unittest.TestCase):
    def test_exact_total(self):
        gens = [hl.Gen(fn=None, level="basic_check", n=n, ps=[]) for n in (6, 4, 5, 3, 2)]
        for total in (50, 60, 77, 100):
            self.assertEqual(sum(hl.allocate(gens, total)), total)


class PackTest(unittest.TestCase):
    def test_each_pack_has_50_questions_with_all_levels_and_perspectives(self):
        for uid, mod_name in ghu.list_packs().items():
            mod = importlib.import_module(f"hs_packs.{mod_name}")
            out = hl.run_generators(uid, mod.GENERATORS, 50)
            with self.subTest(unit=uid):
                self.assertEqual(sum(len(v) for v in out.values()), 50)
                self.assertTrue(all(out[lv] for lv in hl.LEVELS))
                ps = {p for v in out.values() for it in v for p in it["ps"]}
                self.assertLessEqual(REQUIRED, ps)
                self.assertIn("sections", mod.LESSON)


if __name__ == "__main__":
    unittest.main()
