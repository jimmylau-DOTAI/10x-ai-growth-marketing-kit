"""Regression test for the deterministic text/logo finishing route."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image, ImageDraw

SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "render_social_card.py"


class RenderSocialCardTests(unittest.TestCase):
    def test_creates_exact_canvas_and_uses_source_logo_with_alpha(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            hero = root / "hero.png"
            Image.new("RGB", (800, 1000), "#EAB173").save(hero)
            logo = root / "logo.png"
            mark = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
            ImageDraw.Draw(mark).ellipse((5, 5, 35, 35), fill="#C0604A")
            mark.save(logo)
            spec = {
                "canvas": {"width": 1080, "height": 1350, "background": "#F8F7F3"},
                "images": [{"path": "hero.png", "box": [0, 450, 1080, 900], "fit": "cover", "crop_ok": True}],
                "logo": {"path": "logo.png", "box": [900, 40, 120, 120]},
                "texts": [{"text": "Sample", "box": [60, 80, 700, 160], "font_size": 92, "fill": "#C0604A"}],
            }
            (root / "layout.json").write_text(json.dumps(spec), encoding="utf-8")
            output, receipt = root / "final.png", root / "receipt.json"
            result = subprocess.run([sys.executable, str(SCRIPT), "--spec", str(root / "layout.json"), "--output", str(output), "--receipt", str(receipt)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            with Image.open(output) as rendered:
                self.assertEqual(rendered.size, (1080, 1350))
            data = json.loads(receipt.read_text())
            self.assertEqual(data["logo"]["sha256"], hashlib.sha256(logo.read_bytes()).hexdigest())
            self.assertTrue(data["logo"]["alpha_preserved"])

    def test_cover_without_crop_permission_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            Image.new("RGB", (800, 800), "#EAB173").save(root / "hero.png")
            spec = {"canvas": {"width": 1080, "height": 1350}, "images": [{"path": "hero.png", "box": [0, 0, 1080, 1350], "fit": "cover"}]}
            (root / "layout.json").write_text(json.dumps(spec), encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), "--spec", str(root / "layout.json"), "--output", str(root / "final.png")], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("crop_ok", result.stderr)


if __name__ == "__main__":
    unittest.main()
