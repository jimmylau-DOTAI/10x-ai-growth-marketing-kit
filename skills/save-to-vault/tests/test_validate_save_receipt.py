#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SKILL_ROOT / "scripts" / "validate_save_receipt.py"


def receipt_text(*, owner: str = "Jimmy", status: str = "saved", extra: str = "") -> str:
    return f"""---
title: Save to Vault Receipt
type: save_to_vault_receipt
status: {status}
created: 2026-09-01
updated: 2026-09-01
owner: {owner}
source_kind: chatroom
source_ref: current-chatroom
privacy: internal
human_review: not_required
canonical_changes: none
---

# Save to Vault Receipt

## Scope

Current chatroom.

## Active record

One owner decision.

## Writes

- path: 30-learning/receipt.md
  action: created
  read_back: pass

## Exclusions

Transient conversation.

## Review and next step

No open items.
{extra}
"""


class ReceiptValidatorTests(unittest.TestCase):
    def run_validator(self, vault: Path, receipt: str = "30-learning/receipt.md") -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), "--vault", str(vault), "--receipt", receipt],
            capture_output=True, text=True, check=False,
        )

    def make_vault(self, root: Path, content: str) -> Path:
        (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
        (root / "INDEX.md").write_text("# Index\n", encoding="utf-8")
        receipt = root / "30-learning" / "receipt.md"
        receipt.parent.mkdir()
        receipt.write_text(content, encoding="utf-8")
        return receipt

    def test_valid_receipt_passes_and_checks_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp)
            self.make_vault(vault, receipt_text())
            result = self.run_validator(vault)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "SAVE_RECEIPT_PASS")
            self.assertEqual(payload["write_targets_checked"], 1)

    def test_saved_receipt_rejects_unknown_owner(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp)
            self.make_vault(vault, receipt_text(owner="TBC"))
            result = self.run_validator(vault)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("owner is TBC", result.stderr)

    def test_secret_like_token_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp)
            self.make_vault(vault, receipt_text(extra="sk-1234567890abcdefghijklmnop"))
            result = self.run_validator(vault)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("possible secret", result.stderr)

    def test_receipt_path_cannot_escape_vault(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            vault = Path(temp)
            self.make_vault(vault, receipt_text())
            result = self.run_validator(vault, "../outside.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("safe path relative", result.stderr)

    def test_receipt_symlink_cannot_escape_vault(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            vault = root / "vault"
            vault.mkdir()
            (vault / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")
            (vault / "INDEX.md").write_text("# Index\n", encoding="utf-8")
            outside = root / "outside.md"
            outside.write_text(receipt_text(), encoding="utf-8")
            (vault / "receipt.md").symlink_to(outside)
            result = self.run_validator(vault, "receipt.md")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("resolves outside", result.stderr)


if __name__ == "__main__":
    unittest.main()
