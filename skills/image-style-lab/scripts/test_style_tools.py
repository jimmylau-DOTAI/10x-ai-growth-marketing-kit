#!/usr/bin/env python3
"""Behavior tests for the public Image Style Lab helper scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = ROOT / "assets" / "templates"
VALIDATOR = ROOT / "scripts" / "validate_style_pack.py"
PILOT_VALIDATOR = ROOT / "scripts" / "validate_pilot_job.py"
ROUTE_VALIDATOR = ROOT / "scripts" / "validate_platform_route.py"
AUTO_ROUTE_VALIDATOR = ROOT / "scripts" / "validate_auto_route.py"
SAVER = ROOT / "scripts" / "save_style_pack.py"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        check=False,
        text=True,
        capture_output=True,
    )


def build_pack(root: Path, leakage: bool = False) -> Path:
    experiment = root / "experiment"
    style = experiment / "styles" / "student-style"
    style.mkdir(parents=True)
    reference_assets = style / "assets" / "reference-images"
    reference_assets.mkdir(parents=True)
    (reference_assets / "R01.png").write_bytes(b"portable-reference-image")
    for name in ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md"):
        text = (TEMPLATES / name).read_text(encoding="utf-8")
        if name == "STYLE.md":
            text = text.replace("style_id: TBC", "style_id: student-style")
            text = text.replace("design_id: unassigned", "design_id: unassigned")
            text = text.replace("palette_mode: TBC", "palette_mode: adaptive")
            text = text.replace("proof_modality: TBC", "proof_modality: authentic-ui-screenshot")
            text = text.replace("proof_authenticity: TBC", "proof_authenticity: authentic-required")
            text = text.replace("visible_attribution_default: TBC", "visible_attribution_default: forbidden")
        if name == "DESIGN.md":
            text = text.replace("style_id: TBC", "style_id: student-style")
            text = text.replace("design_id: unassigned", "design_id: unassigned")
            text = text.replace("format: TBC", "format: portrait-social")
            text = text.replace("default_treatment: TBC", "default_treatment: adaptive")
            text = text.replace("proof_asset_policy: TBC", "proof_asset_policy: authentic-required")
            text = text.replace("visible_attribution: TBC", "visible_attribution: forbidden")
            if leakage:
                text += "\nC01 source:@copiedcreator\n"
        (style / name).write_text(text, encoding="utf-8")
    return experiment


def build_platform_route(experiment: Path) -> Path:
    style_folder = experiment / "styles" / "student-style"
    for name in ("STYLE.md", "DESIGN.md"):
        path = style_folder / name
        text = path.read_text(encoding="utf-8")
        text = text.replace("design_id: unassigned", "design_id: IG-C-011")
        text = text.replace("platform_scope: portable", "platform_scope: instagram-carousel")
        path.write_text(text, encoding="utf-8")

    vault = experiment.parent / "vault"
    style_index = vault / "platform" / "Styles" / "INDEX.md"
    style_index.parent.mkdir(parents=True)
    style_index.write_text("# Style selector\n", encoding="utf-8")
    reference_root = vault / "Reference-Library" / "visual-assets" / "instagram-carousel"
    reference_root.mkdir(parents=True)
    style_destination = style_index.parent / "IG-C-011-student-style"
    reference_destination = reference_root / "IG-C-011-student-style"

    route = style_folder / "PLATFORM-ROUTE.md"
    text = (TEMPLATES / "PLATFORM-ROUTE.md").read_text(encoding="utf-8")
    replacements = {
        "style_id: TBC": "style_id: student-style",
        "platform: TBC": "platform: instagram",
        "format: TBC": "format: carousel",
        "design_id_namespace: TBC": "design_id_namespace: IG-C",
        "proposed_design_id: TBC": "proposed_design_id: IG-C-011",
        "style_index: TBC": f"style_index: {style_index}",
        "style_destination: TBC": f"style_destination: {style_destination}",
        "reference_destination: TBC": f"reference_destination: {reference_destination}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    route.write_text(text, encoding="utf-8")
    return route


class StyleToolTests(unittest.TestCase):
    def write_auto_route(
        self,
        root: Path,
        *,
        target: str = "ig-carousel",
        outputs: str = "style,tone,skill",
        save_target: str = "none",
        save_authorized: str = "false",
    ) -> Path:
        route = root / "AUTO-ROUTE.md"
        route.write_text(
            f"""---
route_mode: auto
target_use: {target}
detected_outputs: {outputs}
save_target: {save_target}
save_authorized: {save_authorized}
---

# Auto route

## Student request

## Sources received

## Why these outputs

## Save boundary
""",
            encoding="utf-8",
        )
        return route

    def test_auto_route_accepts_all_three_candidate_layers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            route = self.write_auto_route(Path(tmp))
            result = run(str(AUTO_ROUTE_VALIDATOR), str(route))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["detected_outputs"], ["skill", "style", "tone"])
            self.assertFalse(payload["save_authorized"])

    def test_auto_route_accepts_each_student_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for target in ("portable", "seo-banner", "ig-carousel", "ig-single-image"):
                route = self.write_auto_route(Path(tmp), target=target, outputs="style")
                result = run(str(AUTO_ROUTE_VALIDATOR), str(route))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["target_use"], target)

    def test_auto_route_rejects_unknown_layer(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            route = self.write_auto_route(Path(tmp), outputs="style,classroom")
            result = run(str(AUTO_ROUTE_VALIDATOR), str(route))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(any("unknown" in item for item in json.loads(result.stdout)["errors"]))

    def test_auto_route_requires_explicit_save_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            route = self.write_auto_route(
                Path(tmp), save_target="style", save_authorized="false"
            )
            result = run(str(AUTO_ROUTE_VALIDATOR), str(route))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(any("explicit save" in item for item in json.loads(result.stdout)["errors"]))

    def test_auto_route_accepts_each_explicit_candidate_save_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for save_target in ("style", "tone", "skill"):
                route = self.write_auto_route(
                    Path(tmp), save_target=save_target, save_authorized="true"
                )
                result = run(str(AUTO_ROUTE_VALIDATOR), str(route))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["save_target"], save_target)

    def test_auto_route_checks_detected_candidate_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = Path(tmp)
            route = self.write_auto_route(experiment)
            style = experiment / "styles" / "student-style"
            style.mkdir(parents=True)
            (style / "STYLE.md").write_text("# Style\n", encoding="utf-8")
            (style / "DESIGN.md").write_text("# Design\n", encoding="utf-8")
            tone = experiment / "tones" / "student-tone"
            tone.mkdir(parents=True)
            (tone / "TONE.md").write_text("# Tone\n", encoding="utf-8")
            skill = experiment / "skill-candidates" / "student-skill"
            (skill / "evals").mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Skill\n", encoding="utf-8")
            (skill / "evals" / "evals.json").write_text("{}\n", encoding="utf-8")

            result = run(str(AUTO_ROUTE_VALIDATOR), str(route), "--check-outputs")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

            (tone / "TONE.md").unlink()
            invalid = run(str(AUTO_ROUTE_VALIDATOR), str(route), "--check-outputs")
            self.assertNotEqual(invalid.returncode, 0)
            self.assertTrue(any("tone" in item for item in json.loads(invalid.stdout)["errors"]))

    def test_valid_pack_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp))
            result = run(str(VALIDATOR), str(experiment))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_campaign_leakage_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp), leakage=True)
            result = run(str(VALIDATOR), str(experiment))
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(json.loads(result.stdout)["ok"])

    def test_reference_images_must_live_in_declared_reference_asset_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp))
            style = experiment / "styles" / "student-style"
            original = style / "assets" / "reference-images" / "R01.png"
            misplaced = style / "R01.png"
            original.rename(misplaced)
            reference = style / "REFERENCE.md"
            reference.write_text(
                reference.read_text(encoding="utf-8").replace(
                    "assets/reference-images/R01.png", "R01.png"
                ),
                encoding="utf-8",
            )
            result = run(str(VALIDATOR), str(experiment))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(
                any(
                    "reference asset root" in item
                    for item in json.loads(result.stdout)["errors"]
                )
            )

    def test_style_and_design_design_id_must_match(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp))
            design = experiment / "styles" / "student-style" / "DESIGN.md"
            design.write_text(
                design.read_text(encoding="utf-8").replace(
                    "design_id: unassigned", "design_id: IG-C-999"
                ),
                encoding="utf-8",
            )
            result = run(str(VALIDATOR), str(experiment))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(
                any("design_id must match" in item for item in json.loads(result.stdout)["errors"])
            )

    def test_managed_platform_route_has_design_id_and_reference_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp))
            route = build_platform_route(experiment)
            result = run(str(ROUTE_VALIDATOR), str(experiment), str(route))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["ok"])
            self.assertEqual(payload["proposed_design_id"], "IG-C-011")

            route_text = route.read_text(encoding="utf-8")
            style_destination = next(
                line.split(":", 1)[1].strip()
                for line in route_text.splitlines()
                if line.startswith("style_destination:")
            )
            route.write_text(
                "\n".join(
                    f"reference_destination: {style_destination}"
                    if line.startswith("reference_destination:")
                    else line
                    for line in route_text.splitlines()
                )
                + "\n",
                encoding="utf-8",
            )
            invalid = run(str(ROUTE_VALIDATOR), str(experiment), str(route))
            self.assertNotEqual(invalid.returncode, 0)
            self.assertTrue(
                any(
                    "reference_destination" in item
                    for item in json.loads(invalid.stdout)["errors"]
                )
            )

    def test_managed_platform_route_requires_an_existing_style_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            experiment = build_pack(Path(tmp))
            route = build_platform_route(experiment)
            text = route.read_text(encoding="utf-8")
            text = "\n".join(
                "style_index: /missing/platform/Styles/INDEX.md"
                if line.startswith("style_index:")
                else line
                for line in text.splitlines()
            ) + "\n"
            route.write_text(text, encoding="utf-8")
            result = run(str(ROUTE_VALIDATOR), str(experiment), str(route))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(
                any("style_index" in item for item in json.loads(result.stdout)["errors"])
            )

    def test_image_led_html_only_cannot_pass_pilot_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "CONTENT-JOB.md"
            job.write_text(
                """---
job_id: pilot-01
style_id: student-style
status: PILOT_REVIEW_STOP
visual_intent: image-led
pilot_medium: deterministic-layout
production_skill: local-html-renderer
html_role: final-render
fallback_policy: stop
proof_modality: generated-metaphor
proof_authenticity: generated-allowed
proof_asset_path: none
proof_asset_sha256: none
visible_attribution: forbidden
visible_source_text: none
internal_provenance: required
image_model_calls: 0
output_path: pilot.png
output_sha256: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
native_dimensions: 1080x1350
final_dimensions: 1080x1350
postprocess: none
---
""",
                encoding="utf-8",
            )
            result = run(str(PILOT_VALIDATOR), str(job))
            self.assertNotEqual(result.returncode, 0)
            errors = json.loads(result.stdout)["errors"]
            self.assertTrue(any("image-model call" in item for item in errors))
            self.assertTrue(any("HTML as final-render" in item for item in errors))

    def test_image_led_handoff_can_be_route_ready(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "CONTENT-JOB.md"
            job.write_text(
                """---
job_id: pilot-01
style_id: student-style
status: PRODUCTION_HANDOFF_READY
visual_intent: image-led
pilot_medium: image-generation
production_skill: available-complete-image-skill
html_role: layout-reference-only
fallback_policy: stop
proof_modality: generated-metaphor
proof_authenticity: generated-allowed
proof_asset_path: none
proof_asset_sha256: none
visible_attribution: forbidden
visible_source_text: none
internal_provenance: required
image_model_calls: 0
output_path: TBC
output_sha256: TBC
native_dimensions: TBC
final_dimensions: TBC
postprocess: TBC
---
""",
                encoding="utf-8",
            )
            result = run(str(PILOT_VALIDATOR), str(job))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_image_led_generated_pilot_can_reach_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "CONTENT-JOB.md"
            job.write_text(
                """---
job_id: pilot-01
style_id: student-style
status: PILOT_REVIEW_STOP
visual_intent: image-led
pilot_medium: hybrid
production_skill: available-complete-image-skill
html_role: layout-reference-only
fallback_policy: stop
proof_modality: generated-metaphor
proof_authenticity: generated-allowed
proof_asset_path: none
proof_asset_sha256: none
visible_attribution: forbidden
visible_source_text: none
internal_provenance: required
image_model_calls: 1
output_path: pilot.png
output_sha256: bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
native_dimensions: 1024x1280
final_dimensions: 1080x1350
postprocess: exact-size-normalization-and-logo-lock
---
""",
                encoding="utf-8",
            )
            result = run(str(PILOT_VALIDATOR), str(job))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_authentic_required_handoff_needs_real_asset_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "CONTENT-JOB.md"
            job.write_text(
                """---
job_id: pilot-02
style_id: student-style
status: PRODUCTION_HANDOFF_READY
visual_intent: hybrid
pilot_medium: hybrid
production_skill: available-complete-image-skill
html_role: layout-reference-only
fallback_policy: stop
proof_modality: authentic-dashboard-screenshot
proof_authenticity: authentic-required
proof_asset_path: TBC
proof_asset_sha256: TBC
visible_attribution: forbidden
visible_source_text: none
internal_provenance: required
image_model_calls: 0
output_path: TBC
output_sha256: TBC
native_dimensions: TBC
final_dimensions: TBC
postprocess: TBC
---
""",
                encoding="utf-8",
            )
            result = run(str(PILOT_VALIDATOR), str(job))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(any("authentic-required" in item for item in json.loads(result.stdout)["errors"]))

    def test_forbidden_visible_attribution_rejects_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            job = Path(tmp) / "CONTENT-JOB.md"
            job.write_text(
                """---
job_id: pilot-03
style_id: student-style
status: draft
visual_intent: image-led
pilot_medium: image-generation
production_skill: available-complete-image-skill
html_role: none
fallback_policy: stop
proof_modality: generated-metaphor
proof_authenticity: generated-allowed
proof_asset_path: none
proof_asset_sha256: none
visible_attribution: forbidden
visible_source_text: Sources line
internal_provenance: required
image_model_calls: 0
output_path: TBC
output_sha256: TBC
native_dimensions: TBC
final_dimensions: TBC
postprocess: TBC
---
""",
                encoding="utf-8",
            )
            result = run(str(PILOT_VALIDATOR), str(job))
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(any("visible_source_text" in item for item in json.loads(result.stdout)["errors"]))

    def test_save_is_dry_run_then_read_back(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            experiment = build_pack(base)
            vault = base / "vault"
            vault.mkdir()

            dry = run(str(SAVER), str(experiment), "--vault", str(vault))
            self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
            dry_payload = json.loads(dry.stdout)
            self.assertEqual(dry_payload["status"], "STYLE_SAVE_REVIEW_STOP")
            self.assertFalse((vault / "Visual-Styles" / "student-style").exists())

            applied = run(str(SAVER), str(experiment), "--vault", str(vault), "--apply")
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            payload = json.loads(applied.stdout)
            self.assertEqual(payload["status"], "STYLE_SAVED")
            self.assertEqual(
                [item["sha256"] for item in payload["files"]],
                [item["sha256"] for item in payload["read_back"]],
            )
            self.assertTrue(
                (vault / "Visual-Styles" / "student-style" / "assets" / "reference-images" / "R01.png").is_file()
            )
            self.assertTrue((vault / "Visual-Styles" / "INDEX.md").is_file())

            duplicate = run(str(SAVER), str(experiment), "--vault", str(vault), "--apply")
            self.assertNotEqual(duplicate.returncode, 0)
            self.assertIn("refusing to overwrite", duplicate.stderr)

    def test_save_refuses_pack_without_portable_reference_images(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            experiment = build_pack(base)
            image = (
                experiment
                / "styles"
                / "student-style"
                / "assets"
                / "reference-images"
                / "R01.png"
            )
            image.unlink()
            vault = base / "vault"
            vault.mkdir()
            result = run(str(SAVER), str(experiment), "--vault", str(vault))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reference image", result.stderr)


if __name__ == "__main__":
    unittest.main()
