"""Behavior tests use generated local media, with no network or account access."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "verify_video.py"
spec = importlib.util.spec_from_file_location("verify_video", MODULE)
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Requires ffmpeg and ffprobe")
class VideoVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.video = cls.root / "valid.mp4"
        cls.silent = cls.root / "silent.mp4"
        subprocess.run([
            "ffmpeg", "-v", "error", "-f", "lavfi", "-i", "color=size=64x64:rate=10",
            "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=8000", "-t", "1",
            "-c:v", "mpeg4", "-c:a", "aac", str(cls.video)
        ], check=True)
        subprocess.run([
            "ffmpeg", "-v", "error", "-i", str(cls.video), "-an", "-c:v", "copy", str(cls.silent)
        ], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_real_video_passes_without_claiming_source_review(self):
        receipt = verifier.verify(self.video, 1.0, True)
        self.assertEqual(receipt["acquisition_status"], "VERIFIED_LOCAL")
        self.assertTrue(receipt["has_audio"])
        self.assertEqual(len(receipt["sha256"]), 64)
        self.assertEqual(receipt["source_identity_check"], "not_performed_by_verifier")
        self.assertEqual(receipt["reuse_clearance"], "not_confirmed")

    def test_html_named_mp4_is_rejected(self):
        fake = self.root / "error.mp4"
        fake.write_text("<html>Login required</html>")
        with self.assertRaises(subprocess.CalledProcessError):
            verifier.verify(fake)

    def test_duration_mismatch_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duration mismatch"):
            verifier.verify(self.video, 100)

    def test_missing_expected_audio_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "audio stream is missing"):
            verifier.verify(self.silent, require_audio=True)

    def test_silent_source_is_allowed_when_audio_not_expected(self):
        self.assertFalse(verifier.verify(self.silent)["has_audio"])

    def test_missing_or_empty_file_is_rejected(self):
        empty = self.root / "empty.mp4"
        empty.touch()
        for file in (empty, self.root / "missing.mp4"):
            with self.subTest(file=file), self.assertRaises(ValueError):
                verifier.verify(file)

    def test_truncated_container_is_rejected(self):
        truncated = self.root / "truncated.mp4"
        truncated.write_bytes(self.video.read_bytes()[:100])
        with self.assertRaises((ValueError, subprocess.CalledProcessError)):
            verifier.verify(truncated)

    def test_invalid_expected_duration_is_rejected(self):
        for duration in (-1, float("nan"), float("inf")):
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                verifier.verify(self.video, duration)


if __name__ == "__main__":
    unittest.main()
