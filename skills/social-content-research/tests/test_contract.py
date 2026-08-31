#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_sl_packet.py"
DUE_CHECK = SKILL_ROOT / "scripts" / "check_insight_review.py"


SOURCE = """---
type: social_source_record
status: captured
source_id: SRC-20260831-example
source_ref: https://example.com/post
source_type: post
captured: 2026-08-31
access_state: FULL
media_kind: text-only
caption_state: full
retrieval_method: original-page
content_scope: social-post-research-only
origin_id: example-post
---

## Access receipt

Read.

## Evidence inventory

Observed facts.

## Limitations

No performance data.

## SL route

SL-20260831-example.md
"""


SL = """---
type: social_source_learning
status: queued-for-insight-review
source_id: SRC-20260831-example
source_ref: https://example.com/post
created: 2026-08-31
access_state: FULL
media_kind: text-only
caption_state: full
knowledge_status: source-learning-not-approved-insight
content_scope: social-post-research-only
candidate_count: 1
review_status: queued
---

## 30 秒理解

Summary.

## Coverage

Main claim covered.

## 完整攻略

Complete method.

## Candidate Insight cards

#### Candidate 01

- candidate_key: example-pattern
- 一句見解：Example.
- 點解值得記住：Useful.
- 來源證據：Observed example.
- 邊界／反例：No outcome proof.
- Post relevance：Can explain the method.

## Evidence boundary

Do not claim proven results.
"""


class ContractTests(unittest.TestCase):
    def test_valid_sl_packet_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.md"
            sl = Path(temp) / "sl.md"
            source.write_text(SOURCE, encoding="utf-8")
            sl.write_text(SL, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--source", str(source), "--sl", str(sl)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "SL_PACKET_PASS")

    def test_single_source_cannot_be_marked_approved_insight(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "source.md"
            sl = Path(temp) / "sl.md"
            source.write_text(SOURCE, encoding="utf-8")
            sl.write_text(
                SL.replace(
                    "source-learning-not-approved-insight",
                    "approved-for-post",
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(VALIDATOR), "--source", str(source), "--sl", str(sl)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("knowledge_status", result.stderr)

    def test_due_check_uses_next_review_date(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "TRIAGE-STATE.md"
            state.write_text(
                "---\n"
                "last_review_at: 2026-08-28\n"
                "next_review_due: 2026-08-31\n"
                "review_cadence_days: 3\n"
                "last_status: success\n"
                "---\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(DUE_CHECK),
                    "--state",
                    str(state),
                    "--today",
                    "2026-08-31",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "INSIGHT_REVIEW_DUE")

    def test_blank_initial_state_needs_scheduling_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "TRIAGE-STATE.md"
            state.write_text(
                "---\n"
                "last_review_at:\n"
                "next_review_due:\n"
                "review_cadence_days: 3\n"
                "last_status: never-run\n"
                "---\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(DUE_CHECK),
                    "--state",
                    str(state),
                    "--today",
                    "2026-08-31",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "INSIGHT_REVIEW_NOT_SCHEDULED")
            self.assertEqual(payload["reason"], "no-successful-review")

    def test_skill_keeps_content_only_boundary(self) -> None:
        contract = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("social-post-research-only", contract)
        self.assertIn("單一來源沒有升格成 durable Insight", contract)
        self.assertIn("不可自動批准", contract)


if __name__ == "__main__":
    unittest.main()
