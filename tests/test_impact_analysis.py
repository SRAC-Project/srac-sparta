"""Regression tests for complete per-use retrieval and saved reports."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("impact_analysis", ROOT / "impact-analysis.py")
impact = importlib.util.module_from_spec(spec)
spec.loader.exec_module(impact)


class RetrievalTests(unittest.TestCase):
    def test_shared_component_report_retains_both_functions_and_evidence(self):
        with tempfile.TemporaryDirectory() as temp:
            path, output = impact.analyze("CVE-2026-1234", output_dir=temp)
            self.assertEqual(path.read_text(encoding="utf-8"), output)
            self.assertEqual(output.count("Mission Function:"), 2)
            for value in ("AUTH-CMD-001", "UPD-VER-002", "REQ-101", "HAZ-22", "TEST-15", "REQ-201", "TEST-201"):
                self.assertIn(value, output)
            self.assertEqual(len(list(Path(temp).glob("*.txt"))), 1)

    def test_direct_component_and_cve_return_same_assertions(self):
        self.assertEqual(impact.find_assertions("OpenSSL"), impact.find_assertions("cve-2026-1234"))

    def test_per_use_relationships_match_slide_13(self):
        _, rows = impact.find_assertions("OpenSSL")
        self.assertEqual([(r["missionFunctionId"], r["relationshipType"], r["requiresReview"]) for r in rows],
                         [("AUTH-CMD-001", "PROTECTS", True), ("UPD-VER-002", "SUPPORTS", True)])
        _, rows = impact.find_assertions("NASA CryptoLib")
        self.assertEqual((rows[0]["missionFunctionId"], rows[0]["relationshipType"], rows[0]["requiresReview"]),
                         ("UPD-VER-002", "PROTECTS", False))

    def test_unknown_component_creates_no_report(self):
        with tempfile.TemporaryDirectory() as temp:
            path, output = impact.analyze("Unknown Component", output_dir=temp)
            self.assertIsNone(path)
            self.assertIn("No SRAC relationship", output)
            self.assertEqual(list(Path(temp).iterdir()), [])

    def test_new_unmapped_version_does_not_inherit_assertion(self):
        self.assertEqual(impact.find_assertions("OpenSSL 99.0")[1], [])

    def test_missing_review_flag_does_not_mean_no_review(self):
        row = dict(impact.find_assertions("OpenSSL")[1][0])
        del row["requiresReview"]
        self.assertIn("Recorded Review Status: UNDETERMINED", impact.format_assertion(row))

    def test_cli_runs_outside_repository_and_accepts_multiword_name(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(ROOT / "impact-analysis.py"), "NASA CryptoLib", "--output-dir", temp],
                                    cwd=temp, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("UPD-VER-002", result.stdout)
            self.assertTrue((Path(temp) / "NASA_CryptoLib-impact.txt").exists())

    def test_unknown_cve_returns_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            result = subprocess.run([sys.executable, str(ROOT / "impact-analysis.py"), "CVE-UNKNOWN", "--output-dir", temp],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertEqual(list(Path(temp).iterdir()), [])


if __name__ == "__main__":
    unittest.main()
