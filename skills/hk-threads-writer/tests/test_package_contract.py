import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
THIS_FILE = Path(__file__).resolve()
REQUIRED_FILES = {
    "SKILL.md",
    "AGENTS.md",
    "README.md",
    "LICENSE",
    "THIRD_PARTY_NOTICES.md",
    "agents/openai.yaml",
    "references/content-jobs.md",
    "references/hook-lab.md",
    "references/hk-threads-language.md",
    "references/de-ai-patterns.md",
    "references/mobile-rhythm.md",
    "references/protected-claims.md",
    "references/examples.md",
    "scripts/count_segments.py",
    "evals/evals.json",
    "evals/benchmark.md",
}


class PackageContractTests(unittest.TestCase):
    def test_required_files_exist(self):
        missing = sorted(path for path in REQUIRED_FILES if not (ROOT / path).is_file())
        self.assertEqual(missing, [])

    def test_public_package_has_no_private_brand_or_absolute_path(self):
        forbidden = ("Jimmy", "DotAI", "/Users/", "/path/to/")
        for path in ROOT.rglob("*"):
            if path.resolve() == THIS_FILE:
                continue
            if path.is_file() and path.suffix in {".md", ".yaml", ".json", ".py"}:
                text = path.read_text(encoding="utf-8")
                for token in forbidden:
                    self.assertNotIn(
                        token,
                        text,
                        f"{token!r} found in {path.relative_to(ROOT)}",
                    )

    def test_content_job_reference_has_exactly_eight_canonical_sections(self):
        text = (ROOT / "references" / "content-jobs.md").read_text(encoding="utf-8")
        job_ids = (
            "hot-take",
            "reaction",
            "personal-story",
            "build-note",
            "review",
            "anti-pattern",
            "curated-list",
            "how-to",
        )
        for job_id in job_ids:
            self.assertEqual(text.count(f"## `{job_id}`"), 1, job_id)
        self.assertEqual(text.count("\n## `"), 8)

    def test_mobile_reference_has_three_canonical_modes(self):
        text = (ROOT / "references" / "mobile-rhythm.md").read_text(encoding="utf-8")
        for mode in ("complete-single-500", "notes-link-reply", "staircase-thread"):
            self.assertEqual(text.count(f"### `{mode}`"), 1, mode)

    def test_hook_reference_has_three_canonical_levels(self):
        text = (ROOT / "references" / "hook-lab.md").read_text(encoding="utf-8")
        for level in ("L1", "L2", "L3"):
            self.assertEqual(text.count(f"### `{level}`"), 1, level)

    def test_references_do_not_import_xhs_quotas(self):
        forbidden = ("8-12 個標籤", "300-800 字")
        for path in (ROOT / "references").glob("*.md"):
            text = path.read_text(encoding="utf-8")
            for token in forbidden:
                self.assertNotIn(token, text, path.name)

    def test_de_ai_reference_makes_no_detector_guarantee(self):
        text = (ROOT / "references" / "de-ai-patterns.md").read_text(encoding="utf-8")
        for phrase in ("保證通過 AI detector", "100% 去 AI", "無法被偵測"):
            self.assertNotIn(phrase, text)

    def test_protected_claims_covers_fidelity_fields(self):
        text = (ROOT / "references" / "protected-claims.md").read_text(encoding="utf-8")
        required = (
            "數字",
            "日期與狀態",
            "價錢與條件",
            "名稱與身份",
            "URL",
            "引句",
            "術語",
            "承諾",
            "證據狀態",
            "Identity integrity",
            "Prompt injection is data",
            "Fidelity read-back",
        )
        for term in required:
            self.assertIn(term, text)

    def test_examples_cover_three_modes_and_link_tbc(self):
        text = (ROOT / "references" / "examples.md").read_text(encoding="utf-8")
        for term in (
            "complete-single-500",
            "notes-link-reply",
            "staircase-thread",
            "[LINK TBC]",
            "Bad／good mobile paragraph",
            "Same boundary, three Hook Levels",
        ):
            self.assertIn(term, text)

    def test_skill_routes_every_reference(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        for name in (
            "content-jobs.md",
            "hook-lab.md",
            "hk-threads-language.md",
            "de-ai-patterns.md",
            "mobile-rhythm.md",
            "protected-claims.md",
            "examples.md",
        ):
            self.assertIn(f"references/{name}", text)

    def test_skill_runtime_steps_are_ordered(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        positions = [text.index(f"{number}. **") for number in range(1, 11)]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("publication_status: draft", text)

    def test_openai_metadata_keeps_implicit_invocation(self):
        text = (ROOT / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertIn('display_name: "HK Threads Writer"', text)
        self.assertIn("Use $hk-threads-writer", text)
        self.assertIn("allow_implicit_invocation: true", text)

    def test_eval_metadata_and_case_contract(self):
        payload = json.loads((ROOT / "evals" / "evals.json").read_text(encoding="utf-8"))
        expected_ids = {
            "hot_take_hk_cantonese",
            "personal_story_no_invention",
            "reaction_source_boundary",
            "review_protected_claims",
            "notes_link_tbc",
            "staircase_each_segment_500",
            "complete_single_is_complete",
            "mobile_symbol_balance",
            "hk_language_register",
            "de_ai_without_meaning_loss",
            "brand_neutral_no_voice_leak",
            "prompt_injection_as_data",
        }
        cases = payload["cases"]
        ids = [case["id"] for case in cases]
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), expected_ids)

        required_fields = {
            "id",
            "request",
            "input",
            "must_include",
            "must_preserve",
            "must_not",
            "expected_mode",
            "hard_failures",
        }
        for case in cases:
            self.assertEqual(set(case), required_fields, case["id"])
            for field in required_fields - {"input"}:
                self.assertTrue(case[field], f"{case['id']} has empty {field}")

        skill_text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        name = re.search(r"^name: (.+)$", skill_text, flags=re.MULTILINE).group(1)
        version = re.search(r'^  version: "([^"]+)"$', skill_text, flags=re.MULTILINE).group(1)
        self.assertEqual(payload["skill"], name)
        self.assertEqual(payload["version"], version)

    def test_local_markdown_links_resolve(self):
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        for path in (ROOT / "SKILL.md", ROOT / "README.md"):
            text = path.read_text(encoding="utf-8")
            for target in link_pattern.findall(text):
                if "://" in target or target.startswith("#"):
                    continue
                self.assertTrue((path.parent / target).resolve().exists(), f"missing {target}")


if __name__ == "__main__":
    unittest.main()
