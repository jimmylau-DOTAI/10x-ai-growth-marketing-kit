#!/usr/bin/env python3
"""Behavior tests for the public Image Style Lab helper scripts."""

from __future__ import annotations

import json
import hashlib
import re
from PIL import Image
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
    Image.new("RGB", (64, 80), "#163D35").save(reference_assets / "R01.png")
    for name in ("PREFERENCE.md", "REFERENCE.md", "STYLE.md", "DESIGN.md", "scorecard.md"):
        template = TEMPLATES / ("legacy/STYLE.md" if name == "STYLE.md" else name)
        text = template.read_text(encoding="utf-8")
        if name == "REFERENCE.md":
            digest = hashlib.sha256((reference_assets / "R01.png").read_bytes()).hexdigest()
            text = text.replace("| R01 | TBC | TBC | TBC | style-reference | TBC |",
                                f"| R01 | synthetic fixture | test-owned | {digest} | cover | test |")
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
        text = re.sub(r"(?m)^(## .+)\n", r"\1\n\nSynthetic test fixture: this section is populated only to test validation.\n", text)
        (style / name).write_text(text, encoding="utf-8")
    return experiment


def build_compact_pack(root: Path) -> Path:
    pack = root / "experiment" / "styles" / "student-style"
    assets = pack / "assets" / "reference-images"
    assets.mkdir(parents=True)
    Image.new("RGB", (64, 80), "#163D35").save(assets / "R01.png")
    digest = hashlib.sha256((assets / "R01.png").read_bytes()).hexdigest()
    text = (TEMPLATES / "STYLE.md").read_text(encoding="utf-8")
    replacements = {
        "style_id: TBC": "style_id: student-style",
        "identity_basis: TBC": "identity_basis: synthetic portrait social fixture",
        "proof_modality: TBC": "proof_modality: product-photo-with-explanation",
        "proof_authenticity: TBC": "proof_authenticity: authentic-required",
        "rights_status: TBC": "rights_status: synthetic-test-owned",
        "| assets/reference-images/R01.png | TBC | TBC | TBC | TBC |":
            f"| assets/reference-images/R01.png | synthetic fixture | test-owned | 64x80 | {digest} |",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    (pack / "STYLE.md").write_text(text, encoding="utf-8")

    design = (TEMPLATES / "DESIGN.md").read_text(encoding="utf-8")
    design_replacements = {
        "style_id: TBC": "style_id: student-style",
        "format: TBC": "format: portrait-social",
        "render_contract: choose-per-job": "render_contract: native-ai-visual-plus-real-logo-finish",
        "default_treatment: TBC": "default_treatment: adaptive",
        "proof_asset_policy: TBC": "proof_asset_policy: authentic-required",
        "visible_attribution: TBC": "visible_attribution: job-controlled",
    }
    for old, new in design_replacements.items():
        design = design.replace(old, new)
    design = re.sub(
        r"(?m)^(## .+)\n",
        r"\1\n\nSynthetic test fixture: this section is populated only to test validation.\n",
        design,
    )
    (pack / "DESIGN.md").write_text(design, encoding="utf-8")
    return pack


def build_platform_route(experiment: Path) -> Path:
    style_folder = experiment / "styles" / "student-style"
    for name in ("STYLE.md", "DESIGN.md"):
        path = style_folder / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "design_id:" not in text:
            text = text.replace("pack_version: 2", "pack_version: 2\ndesign_id: unassigned")
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
    if (style_folder / "DESIGN.md").is_file():
        text += "\nLegacy files: `DESIGN.md`, `REFERENCE.md`\n"
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

            dry = run(str(SAVER), str(experiment), "--vault", str(vault), "--style-root", "Visual-Styles")
            self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
            dry_payload = json.loads(dry.stdout)
            self.assertEqual(dry_payload["status"], "STYLE_SAVE_REVIEW_STOP")
            self.assertFalse((vault / "Visual-Styles" / "student-style").exists())

            applied = run(str(SAVER), str(experiment), "--vault", str(vault), "--style-root", "Visual-Styles", "--apply")
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

            duplicate = run(str(SAVER), str(experiment), "--vault", str(vault), "--style-root", "Visual-Styles", "--apply")
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
            result = run(str(SAVER), str(experiment), "--vault", str(vault), "--style-root", "Visual-Styles")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reference image", result.stderr)


    def test_complete_gallery_direct_pack_and_exact_format_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_pack(base) / "styles" / "student-style"
            reference = pack / "REFERENCE.md"
            text = reference.read_text(encoding="utf-8")
            names = ["R01.png"]
            for number in range(2, 11):
                # A filename with spaces exercises real Markdown portability.
                name = f"R{number:02d} ending.png" if number == 10 else f"R{number:02d}.png"
                names.append(name)
                image = pack / "assets" / "reference-images" / name
                Image.new("RGB", (24, 30), (number * 20, 90, 100)).save(image)
                digest = hashlib.sha256(image.read_bytes()).hexdigest()
                text += f"\n![page {number}](<assets/reference-images/{name}>)\n\nSHA-256: {digest}\n"
            reference.write_text(text, encoding="utf-8")
            history = pack / "review"
            history.mkdir()
            (history / "rejected.png").write_bytes(b"not an active image")
            vault = base / "vault"
            library = vault / "platform" / "Carousel" / "Style-Candidates"
            library.mkdir(parents=True)
            (library / "INDEX.md").write_text("# Existing library\n\nKeep this entry.\n", encoding="utf-8")
            result = run(str(SAVER), str(pack), "--vault", str(vault),
                         "--style-root", "platform/Carousel/Style-Candidates", "--apply")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["reference_image_count"], 10)
            self.assertEqual(payload["library_status"], "candidate")
            copied_images = [Path(item["name"]).name for item in payload["files"]
                             if item["name"].startswith("assets/")]
            self.assertEqual(copied_images, names)
            saved = library / "student-style"
            self.assertEqual((saved / "REFERENCE.md").read_text(), text)
            self.assertFalse((saved / "review").exists())
            self.assertFalse((vault / "Visual-Styles").exists())
            index = (library / "INDEX.md").read_text()
            self.assertIn("Keep this entry.", index)
            self.assertIn("[STYLE.md](student-style/STYLE.md)", index)
            self.assertIn("[REFERENCE.md](student-style/REFERENCE.md)", index)
            self.assertIn("![student-style — current preview](student-style/assets/reference-images/R01.png)", index)
            self.assertIn("brand_state: reference-only", (saved / "STYLE.md").read_text())

    def test_bad_images_fail_before_any_save(self) -> None:
        for issue in ("corrupt", "stale-hash", "unembedded"):
            with self.subTest(issue=issue), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                pack = build_pack(base) / "styles" / "student-style"
                image = pack / "assets" / "reference-images" / "R01.png"
                if issue == "corrupt":
                    image.write_bytes(b"not a real PNG")
                elif issue == "stale-hash":
                    Image.new("RGB", (20, 20), "red").save(image)
                else:
                    Image.new("RGB", (20, 20), "blue").save(image.with_name("old.png"))
                vault = base / "vault"
                vault.mkdir()
                result = run(str(SAVER), str(pack), "--vault", str(vault),
                             "--style-root", "Carousel/Style-Candidates", "--apply")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list(vault.iterdir()), [])

    def test_symlink_reference_parent_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_pack(base) / "styles" / "student-style"
            assets = pack / "assets" / "reference-images"
            external = base / "external-images"
            assets.rename(external)
            assets.symlink_to(external, target_is_directory=True)
            result = run(str(VALIDATOR), str(pack))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("symlink", result.stdout)

    def test_save_rejects_symlink_document_and_index(self) -> None:
        for target in ("STYLE.md", "INDEX.md"):
            with self.subTest(target=target), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                pack = build_pack(base) / "styles" / "student-style"
                vault = base / "vault"
                library = vault / "Carousel"
                library.mkdir(parents=True)
                external = base / "external.md"
                if target == "STYLE.md":
                    source = pack / target
                    source.rename(external)
                    source.symlink_to(external)
                else:
                    external.write_text("Leave intact\n", encoding="utf-8")
                    (library / target).symlink_to(external)
                original = external.read_bytes()
                result = run(str(SAVER), str(pack), "--vault", str(vault),
                             "--style-root", "Carousel", "--apply")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(external.read_bytes(), original)
                self.assertFalse((library / "student-style").exists())

    def test_user_selection_is_not_gated_on_multiple_jobs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_pack(Path(tmp)) / "styles" / "student-style"
            style = pack / "STYLE.md"
            style.write_text(style.read_text().replace("status: candidate", "status: user-selected"))
            result = run(str(VALIDATOR), str(pack))
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertIn("no tested_jobs", result.stdout)

    def test_destination_must_be_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            experiment = build_pack(base)
            vault = base / "vault"
            vault.mkdir()
            result = run(str(SAVER), str(experiment), "--vault", str(vault), "--apply")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--style-root", result.stderr)
            self.assertEqual(list(vault.iterdir()), [])

    def test_traversal_and_outside_vault_routes_rejected(self) -> None:
        for route in ("../outside", "linked"):
            with self.subTest(route=route), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                experiment = build_pack(base)
                vault = base / "vault"
                vault.mkdir()
                outside = base / "outside"
                outside.mkdir()
                (vault / "linked").symlink_to(outside, target_is_directory=True)
                result = run(str(SAVER), str(experiment), "--vault", str(vault),
                             "--style-root", route, "--apply")
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(list(outside.iterdir()), [])

    def test_brand_candidate_without_palette_is_allowed(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_pack(Path(tmp)) / "styles" / "student-style"
            result = run(str(VALIDATOR), str(pack))
            self.assertEqual(result.returncode, 0, result.stdout)
            self.assertEqual(json.loads(result.stdout)["brand_state"], "reference-only")

    def test_branded_state_requires_own_brand_and_palette(self):
        for state in ("brand-adapted", "brand-approved"):
            with self.subTest(state=state), tempfile.TemporaryDirectory() as tmp:
                pack = build_pack(Path(tmp)) / "styles" / "student-style"
                style = pack / "STYLE.md"
                style.write_text(style.read_text().replace("brand_state: reference-only", f"brand_state: {state}"))
                result = run(str(VALIDATOR), str(pack))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("brand_source required", result.stdout)
                self.assertIn("brand_palette requires", result.stdout)

    def test_brand_approval_evidence_and_no_logo_requirement(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_pack(Path(tmp)) / "styles" / "student-style"
            style, design = pack / "STYLE.md", pack / "DESIGN.md"
            style.write_text(style.read_text().replace("brand_state: reference-only", "brand_state: brand-approved"))
            text = design.read_text().replace("brand_id: unassigned", "brand_id: fixture-brand")
            text = text.replace("brand_source: unassigned", "brand_source: brand/design-source.md")
            text = text.replace("brand_palette: {}", 'brand_palette: {"primary":"#164A70","background":"#FFF9EF","text":"#192B39"}')
            design.write_text(text)
            pending = run(str(VALIDATOR), str(pack))
            self.assertNotEqual(pending.returncode, 0)
            self.assertIn("brand_review evidence", pending.stdout)
            design.write_text(text.replace("brand_review: unreviewed", "brand_review: PREFERENCE.md#human-review"))
            # This verifies metadata presence only, not genuine approval or palette application.
            approved = run(str(VALIDATOR), str(pack))
            self.assertEqual(approved.returncode, 0, approved.stdout)
            self.assertEqual(json.loads(approved.stdout)["brand_state"], "brand-approved")

    def test_brand_palette_invalid_type_or_color_fails(self):
        for palette in ('[]', '{"primary":"orange","background":"#FFFFFF","text":"#111111"}'):
            with self.subTest(palette=palette), tempfile.TemporaryDirectory() as tmp:
                pack = build_pack(Path(tmp)) / "styles" / "student-style"
                style, design = pack / "STYLE.md", pack / "DESIGN.md"
                style.write_text(style.read_text().replace("brand_state: reference-only", "brand_state: brand-adapted"))
                design.write_text(design.read_text().replace("brand_palette: {}", "brand_palette: " + palette))
                result = run(str(VALIDATOR), str(pack))
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("brand_palette", result.stdout)

    def test_empty_section_cannot_be_saved_as_complete_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_pack(Path(tmp)) / "styles" / "student-style"
            design = pack / "DESIGN.md"
            design.write_text(re.sub(r"(?s)(## Recognition path\n).*?(?=\n## )", r"\1\n", design.read_text()))
            result = run(str(VALIDATOR), str(pack))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("empty section", result.stdout)


class CompactStyleToolTests(unittest.TestCase):
    def validate(self, pack: Path):
        return run(str(VALIDATOR), str(pack))

    def save(self, pack: Path, vault: Path, apply: bool = False):
        return run(str(SAVER), str(pack), "--vault", str(vault),
                   "--style-root", "Carousel/Style-Candidates", *(["--apply"] if apply else []))

    def test_style_design_and_images_validate(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            result = self.validate(pack)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["pack_version"], 2)
            self.assertEqual({f.name for f in pack.glob("*.md")}, {"STYLE.md", "DESIGN.md"})

    def test_missing_design_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            (pack / "DESIGN.md").unlink()
            result = self.validate(pack)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing required file", result.stdout)

    def test_new_pack_is_not_implicitly_legacy_or_unknown_version(self):
        for replacement in ("", "pack_version: 3"):
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as tmp:
                pack = build_compact_pack(Path(tmp))
                path = pack / "STYLE.md"
                path.write_text(path.read_text().replace("pack_version: 2", replacement))
                result = self.validate(pack)
                self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_immutable_style_identity_rejects_revision_in_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            style = pack / "STYLE.md"
            text = style.read_text(encoding="utf-8").replace(
                "style_id: student-style", "style_id: student-style-v2"
            )
            style.write_text(text.replace("student-style/", "student-style-v2/"), encoding="utf-8")
            pack.rename(pack.with_name("student-style-v2"))
            result = self.validate(pack.with_name("student-style-v2"))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not carry a revision suffix", result.stdout)

    def test_immutable_style_identity_rejects_self_predecessor(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            style = pack / "STYLE.md"
            text = style.read_text(encoding="utf-8").replace(
                "predecessor_style_id: none", "predecessor_style_id: student-style"
            )
            style.write_text(text, encoding="utf-8")
            result = self.validate(pack)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("cannot equal style_id", result.stdout)

    def test_dry_run_apply_and_revalidate_with_optional_deconstruction(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_compact_pack(base)
            vault = base / "vault"
            vault.mkdir()
            (pack / "DECONSTRUCTION.md").write_text(
                "# Deconstruction\n\nObserved reference evidence for test only.\n",
                encoding="utf-8",
            )
            # Ignore review history during export.
            (pack / "review").mkdir()
            (pack / "review" / "old.md").write_text("Not active\n")
            dry = self.save(pack, vault)
            self.assertEqual(dry.returncode, 0, dry.stdout + dry.stderr)
            self.assertEqual(list(vault.iterdir()), [])
            applied = self.save(pack, vault, True)
            self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
            payload = json.loads(applied.stdout)
            self.assertTrue(payload["read_back_verified"])
            self.assertEqual(
                {item["name"] for item in payload["files"]},
                {"STYLE.md", "DESIGN.md", "DECONSTRUCTION.md", "assets/reference-images/R01.png"},
            )
            saved = Path(payload["destination"])
            self.assertEqual(self.validate(saved).returncode, 0)
            index = (saved.parent / "INDEX.md").read_text()
            self.assertIn("[STYLE.md]", index)
            self.assertIn("[DESIGN.md]", index)
            for extra in ("REFERENCE.md", "PREFERENCE.md", "scorecard.md", "TONE.md"):
                self.assertNotIn(extra, index)
                self.assertFalse((saved / extra).exists())
            self.assertTrue((saved / "DECONSTRUCTION.md").is_file())
            self.assertIn("student-style/assets/reference-images/R01.png", index)
            self.assertNotEqual(self.save(pack, vault, True).returncode, 0)

    def test_optional_tone_only_on_request_and_survives_save(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_compact_pack(base)
            tone = pack / "TONE.md"
            tone.write_text("# Writing voice\n\nExplain in short direct sentences.\n")
            self.assertNotEqual(self.validate(pack).returncode, 0)
            style = pack / "STYLE.md"
            style.write_text(style.read_text().replace("pack_version: 2", "pack_version: 2\ntone_requested: true"))
            vault = base / "vault"
            vault.mkdir()
            result = self.save(pack, vault, True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            saved = Path(json.loads(result.stdout)["destination"])
            self.assertEqual((saved / "TONE.md").read_bytes(), tone.read_bytes())
            self.assertIn("[TONE.md]", (saved.parent / "INDEX.md").read_text())

    def test_missing_empty_symlink_tone_fails(self):
        for issue in ("missing", "empty", "symlink"):
            with self.subTest(issue=issue), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                pack = build_compact_pack(base)
                style = pack / "STYLE.md"
                style.write_text(style.read_text().replace("pack_version: 2", "pack_version: 2\ntone_requested: true"))
                if issue == "empty":
                    (pack / "TONE.md").write_text("")
                elif issue == "symlink":
                    (pack / "TONE.md").symlink_to(style)
                self.assertNotEqual(self.validate(pack).returncode, 0)

    def test_branded_state_needs_palette_and_approval_stays_in_one_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            path = pack / "STYLE.md"
            design_path = pack / "DESIGN.md"
            text = path.read_text().replace("brand_state: reference-only", "brand_state: brand-adapted")
            path.write_text(text)
            self.assertNotEqual(self.validate(pack).returncode, 0)
            design = design_path.read_text()
            design = design.replace("brand_id: unassigned", "brand_id: fixture")
            design = design.replace("brand_source: unassigned", "brand_source: synthetic-test-brief")
            design = design.replace("brand_palette: {}", 'brand_palette: {"primary":"#123456","background":"#FFFFFF","text":"#222222"}')
            design_path.write_text(design)
            self.assertEqual(self.validate(pack).returncode, 0)
            text = text.replace("brand-adapted", "brand-approved")
            path.write_text(text)
            self.assertNotEqual(self.validate(pack).returncode, 0)
            design = design.replace("brand_review: unreviewed", "brand_review: STYLE.md#確認與測試")
            design_path.write_text(design)
            text += "\nSynthetic approval record, fixture only; no real human approval claimed.\n"
            path.write_text(text)
            result = self.validate(pack)
            self.assertEqual(result.returncode, 0, result.stdout)
            design_path.write_text(design.replace("#確認與測試", "#missing"))
            self.assertNotEqual(self.validate(pack).returncode, 0)

    def test_gallery_order_full_set_and_spaces(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_compact_pack(base)
            path = pack / "STYLE.md"
            text = path.read_text()
            names = []
            for number in range(2, 11):
                relative = f"assets/reference-images/R{number:02d} page.png"
                Image.new("RGB", (30, 40), (number * 20, 10, 10)).save(pack / relative)
                digest = hashlib.sha256((pack / relative).read_bytes()).hexdigest()
                text += f"\n![page](<{relative}>)\n\n| {relative} | synthetic, test-owned | {digest} |\n"
                names.append(relative)
            path.write_text(text)
            vault = base / "vault"
            vault.mkdir()
            result = self.save(pack, vault, True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["reference_image_count"], 10)
            self.assertEqual([item["name"] for item in payload["files"]][3:], names)
            self.assertTrue(payload["preview_image"].endswith("R01.png"))

    def test_corrupt_stale_unembedded_and_misassociated_hash_rejected_before_save(self):
        for issue in ("corrupt", "stale", "unembedded", "wrong-row"):
            with self.subTest(issue=issue), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                pack = build_compact_pack(base)
                picture = pack / "assets/reference-images/R01.png"
                if issue == "corrupt":
                    picture.write_bytes(b"not png")
                elif issue == "stale":
                    Image.new("RGB", (5, 5), "red").save(picture)
                elif issue == "unembedded":
                    Image.new("RGB", (5, 5), "red").save(picture.with_name("old.png"))
                else:
                    path = pack / "STYLE.md"
                    digest = hashlib.sha256(picture.read_bytes()).hexdigest()
                    path.write_text(path.read_text().replace(digest, "wrong-hash") + "\n" + digest)
                vault = base / "vault"
                vault.mkdir()
                self.assertNotEqual(self.save(pack, vault, True).returncode, 0)
                self.assertEqual(list(vault.iterdir()), [])

    def test_provenance_not_misclassified_as_style_instruction(self):
        with tempfile.TemporaryDirectory() as tmp:
            pack = build_compact_pack(Path(tmp))
            path = pack / "STYLE.md"
            text = path.read_text()
            path.write_text(text + "\nSource evidence only: @samplecreator\n")
            self.assertEqual(self.validate(pack).returncode, 0)
            path.write_text(text.replace("## 風格核心", "## 風格核心\n\nCopy @samplecreator"))
            self.assertNotEqual(self.validate(pack).returncode, 0)

    def test_auto_route_and_optional_managed_route_accept_compact_pack(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            pack = build_compact_pack(base)
            experiment = pack.parent.parent
            auto = StyleToolTests().write_auto_route(experiment, outputs="style")
            result = run(str(AUTO_ROUTE_VALIDATOR), str(auto), "--check-outputs")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            route = build_platform_route(experiment)
            result = run(str(ROUTE_VALIDATOR), str(experiment), str(route))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((pack / "DESIGN.md").is_file())


if __name__ == "__main__":
    unittest.main()
