import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.count_segments import count_segment, validate_payload


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "count_segments.py"


class CountSegmentTests(unittest.TestCase):
    def test_exactly_500_passes(self):
        result = count_segment("字" * 500)
        self.assertEqual(result, {"count": 500, "remaining": 0, "status": "PASS"})

    def test_501_fails(self):
        result = count_segment("字" * 501)
        self.assertEqual(result, {"count": 501, "remaining": -1, "status": "FAIL"})

    def test_newlines_spaces_symbols_emoji_and_url_use_python_len(self):
        text = "第一段\n\n→ 第二段 👇 https://example.com"
        self.assertEqual(count_segment(text)["count"], len(text))

    def test_non_string_text_fails(self):
        with self.assertRaisesRegex(TypeError, "segment text must be a string"):
            count_segment(None)

    def test_multiple_segments_are_counted_independently(self):
        payload = {
            "segments": [
                {"id": "root", "text": "甲" * 500},
                {"id": "reply-1", "text": "乙" * 501},
            ]
        }
        results, passed = validate_payload(payload)
        self.assertEqual([item["status"] for item in results], ["PASS", "FAIL"])
        self.assertFalse(passed)

    def test_missing_segments_fails(self):
        with self.assertRaisesRegex(ValueError, "segments must be a non-empty list"):
            validate_payload({})

    def test_empty_segments_fails(self):
        with self.assertRaisesRegex(ValueError, "segments must be a non-empty list"):
            validate_payload({"segments": []})

    def test_duplicate_ids_fail(self):
        payload = {
            "segments": [
                {"id": "root", "text": "甲"},
                {"id": "root", "text": "乙"},
            ]
        }
        with self.assertRaisesRegex(ValueError, "duplicate segment id: root"):
            validate_payload(payload)

    def test_non_string_payload_text_fails(self):
        with self.assertRaisesRegex(TypeError, "segment text must be a string"):
            validate_payload({"segments": [{"id": "root", "text": 42}]})

    def run_cli(self, payload):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_path = Path(temp_dir) / "segments.json"
            input_path.write_text(
                json.dumps(payload, ensure_ascii=False),
                encoding="utf-8",
            )
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(input_path)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                check=False,
            )

    def test_cli_returns_zero_when_every_segment_passes(self):
        completed = self.run_cli({"segments": [{"id": "root", "text": "甲" * 500}]})
        self.assertEqual(completed.returncode, 0)
        output = json.loads(completed.stdout)
        self.assertTrue(output["passed"])
        self.assertEqual(output["segments"][0]["count"], 500)

    def test_cli_returns_one_when_a_segment_fails(self):
        completed = self.run_cli({"segments": [{"id": "root", "text": "甲" * 501}]})
        self.assertEqual(completed.returncode, 1)
        output = json.loads(completed.stdout)
        self.assertFalse(output["passed"])

    def test_cli_returns_one_for_invalid_payload(self):
        completed = self.run_cli({"segments": []})
        self.assertEqual(completed.returncode, 1)
        self.assertIn("ERROR: segments must be a non-empty list", completed.stderr)


if __name__ == "__main__":
    unittest.main()
