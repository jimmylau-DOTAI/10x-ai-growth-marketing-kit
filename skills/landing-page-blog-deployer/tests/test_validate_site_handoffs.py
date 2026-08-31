import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_site_handoffs.py"
SPEC = importlib.util.spec_from_file_location("validate_site_handoffs", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


class HandoffValidatorTests(unittest.TestCase):
    def write_json(self, directory: Path, name: str, payload: dict) -> Path:
        path = directory / name
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def landing_payload(self) -> dict:
        return {
            "schema_version": "1.0",
            "handoff_type": "landing-site",
            "approval_status": "APPROVED_FOR_ASSEMBLY",
            "source_artifact": "landing.md",
            "route": "/",
            "primary_cta": {"label": "Join", "intent": "lead-capture", "target": "#lead-form", "status": "VERIFIED"},
            "form": {"anchor": "lead-form", "fields": [], "consent_status": "VERIFIED", "success_action": "Thanks", "endpoint_status": "DISCONNECTED"},
            "tracking": {"utm_fields": ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"], "first_touch_required": True, "registry_path": "utm-registry.csv"},
            "qa": {"design_status": "DESIGN_QA_PASSED", "operations_status": "NOT_IN_SCOPE", "mobile_evidence": "mobile.png"},
            "open_items": [],
        }

    def blog_payload(self) -> dict:
        return {
            "schema_version": "1.0",
            "handoff_type": "blog-publish",
            "approval_status": "APPROVED_FOR_ASSEMBLY",
            "source_artifact": "article-output.md",
            "slug": "ai-learning-path",
            "title": "AI Learning Path",
            "meta_title": "AI Learning Path",
            "meta_description": "A practical learning path.",
            "canonical_path": "/blog/ai-learning-path",
            "content_source": "article.md",
            "language": "zh-Hant",
            "internal_links": [],
            "cta": {"label": "Join", "target": "/#lead-form", "status": "VERIFIED"},
            "schema": {"article": True, "faq": False, "visible_content_match": "VERIFIED"},
            "image_rights_status": "VERIFIED",
            "open_items": [],
        }

    def test_valid_handoffs_pass(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            landing = self.write_json(directory, "landing.json", self.landing_payload())
            blog = self.write_json(directory, "blog.json", self.blog_payload())
            self.assertEqual(MODULE.validate_landing(landing), [])
            self.assertEqual(MODULE.validate_blog(blog), [])

    def test_approved_handoff_with_open_items_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            payload = self.blog_payload()
            payload["open_items"] = ["CTA not confirmed"]
            blog = self.write_json(directory, "blog.json", payload)
            self.assertTrue(any("cannot contain open_items" in error for error in MODULE.validate_blog(blog)))

    def test_missing_utm_field_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            payload = self.landing_payload()
            payload["tracking"]["utm_fields"].remove("utm_term")
            landing = self.write_json(directory, "landing.json", payload)
            self.assertTrue(any("five standard UTM fields" in error for error in MODULE.validate_landing(landing)))

    def test_slug_and_canonical_must_match(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            payload = self.blog_payload()
            payload["slug"] = "Bad Slug"
            blog = self.write_json(directory, "blog.json", payload)
            errors = MODULE.validate_blog(blog)
            self.assertTrue(any("kebab-case" in error for error in errors))
            self.assertTrue(any("canonical_path" in error for error in errors))

    def test_cli_validates_real_json_files(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            landing = self.write_json(directory, "landing.json", self.landing_payload())
            blog = self.write_json(directory, "blog.json", self.blog_payload())
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--landing", str(landing), "--blog", str(blog)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("HANDOFF_VALIDATION_PASSED landing=1 blogs=1", result.stdout)


if __name__ == "__main__":
    unittest.main()
