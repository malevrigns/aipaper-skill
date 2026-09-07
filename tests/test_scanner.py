import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "ai_paper_check.py"
spec = importlib.util.spec_from_file_location("scan", SCRIPT)
scan = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scan)
SENTENCE = "We use recent local traffic observations to adjust traversal costs during online planning."


class ScannerTests(unittest.TestCase):
    def codes(self, report):
        return [f["code"] for f in report["findings"]]

    def test_single_file_cross_section_positions(self):
        r = scan.analyze({"p.md": "## Introduction\n\n" + SENTENCE + "\n\n## Method\n\n" + SENTENCE})
        f = next(f for f in r["findings"] if f["code"] == "B2_REPETITION")
        self.assertEqual([e["line"] for e in f["evidence"]], [3, 7])
        self.assertTrue(f["cross_section"])
        self.assertNotIn("ai_flavor_score", r)

    def test_chinese_repetition(self):
        sentence = "该方法根据机器人近期的局部交通观测动态调整路径搜索中的通行代价。"
        r = scan.analyze({"p.md": "## 引言\n" + sentence + "\n\n## 方法\n" + sentence})
        self.assertIn("B2_REPETITION", self.codes(r))

    def test_legitimate_uncertainty_is_not_a_finding(self):
        text = ("## Results\nAccuracy increased by 2.1 percentage points (95% CI [0.4, 3.8]). "
                "It may vary in another setting.\n\nNo statistically significant difference was found "
                "in the stress test; equivalence remains unresolved.")
        r = scan.analyze({"p.md": text})
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["observations"]["inconclusive_sentence_mentions"], 1)

    def test_table_stats_are_not_body_stats(self):
        text = "| Method | p-value | Accuracy |\n| --- | --- | --- |\n| A | 0.04 | 92.10 |\n| B | 0.0012 | 93.20 |\n| C | 0.000013 | 94.30 |\n| D | 0.0000005 | 95.40 |"
        r = scan.analyze({"p.md": text})
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["observations"].get("statistic_mentions_in_prose", 0), 0)

    def test_precision_compared_within_column(self):
        text = "| Method | Accuracy | Runtime |\n| --- | --- | --- |\n| A | 92.10 | 8.2 |\n| B | 93.20 | 8.7 |"
        self.assertEqual(scan.analyze({"p.md": text})["findings"], [])
        r = scan.analyze({"p.md": text.replace("93.20", "93.200000")})
        self.assertEqual(self.codes(r), ["C1_TABLE_PRECISION"])
        self.assertEqual(r["findings"][0]["evidence"][1]["line"], 4)

    def test_reference_code_latex_and_appendix_exclusion(self):
        text = "## Introduction\n" + SENTENCE + "\n\n"
        text += "~~~text\nTODO\n" + SENTENCE + "\n~~~\n"
        text += "\\begin{tabular}{l}\nTODO p=0.01 p=0.02 p=0.03 p=0.04\n\\end{tabular}\n"
        text += "## References\n" + SENTENCE + "\nTODO\n## Appendix\nTODO"
        self.assertEqual(scan.analyze({"p.md": text})["findings"], [])
        r = scan.analyze({"p.md": text}, include_appendix=True)
        self.assertEqual(self.codes(r), ["E1_PLACEHOLDER"])

    def test_paragraph_wraps_are_not_new_paragraphs(self):
        text = "It is worth noting that this is limited\nin some cases. We do not claim universality."
        r = scan.analyze({"p.txt": text})
        self.assertEqual(self.codes(r), ["B1_DEFENSE_CLUSTER"])
        self.assertEqual(r["coverage"]["prose_blocks"], 1)

    def test_last_shingle_and_minimum_boundary(self):
        tokens = "one two three four five".split()
        self.assertEqual(scan.shingles(tokens), {tuple(tokens)})
        self.assertEqual(len(scan.shingles(tokens + ["six"])), 2)

    def test_same_stem_paths_and_cli_success(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            a, b, out = root / "method_1.txt", root / "method_2.txt", root / "out.json"
            a.write_text(SENTENCE, encoding="utf-8")
            b.write_text(SENTENCE, encoding="utf-8")
            command = [sys.executable, str(SCRIPT), "--sections", str(a), str(b), "--json", str(out)]
            proc = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            r = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(r["coverage"]["inputs"]), 2)
            self.assertIn("B2_REPETITION", self.codes(r))
            fail = subprocess.run(command + ["--fail-on-findings"], capture_output=True)
            self.assertEqual(fail.returncode, 1)

    def test_invalid_input_and_write_collision(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "p.md"
            p.write_text("Original manuscript.", encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(p), "--json", str(p)],
                                    capture_output=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(p.read_text(), "Original manuscript.")
            p.write_bytes(b"\xff\xff")
            result = subprocess.run([sys.executable, str(SCRIPT), str(p)], capture_output=True)
            self.assertEqual(result.returncode, 2)

    def test_no_experiment_ratio_from_verbs(self):
        r = scan.analyze({"p.md": "Results are inconclusive. Results remain mixed."})
        self.assertEqual(r["observations"]["inconclusive_sentence_mentions"], 2)
        self.assertNotIn("fraction_inconclusive", json.dumps(r))
        self.assertEqual(r["findings"], [])

    def test_latex_heading_and_placeholder_location(self):
        r = scan.analyze({"p.tex": "\\section{Method}\n\nWindow: NEEDS REAL VALUE."})
        e = r["findings"][0]["evidence"][0]
        self.assertEqual((e["section"], e["line"]), ("Method", 3))

    def test_display_math_is_not_prose(self):
        r = scan.analyze({"p.tex": "\\[\nTODO p=0.01 p=0.02 p=0.03 p=0.04\n\\]\n\n## Results\nFine."})
        self.assertEqual(r["findings"], [])


if __name__ == "__main__":
    unittest.main()
