from pathlib import Path
import subprocess

path = Path("tests/test_greg_again_audio_catalog.py")
text = path.read_text()
old = '''        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}
        for number in range(1, 15):
            chapter_id = f"ga-{number:03d}"
            self.assertIn(chapter_id, by_id)
            self.assertEqual(number, by_id[chapter_id]["number"])
            self.assertEqual(f"assets/chapter-{number:03d}.mp3", by_id[chapter_id]["audio_src"])
'''
new = '''        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        v2_manifest = json.loads((AUDIO_ROOT / "v2/manifest.json").read_text(encoding="utf-8"))
        v2_numbers = {chapter["number"] for chapter in v2_manifest.get("chapters", [])}
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
        chapters = manifest["chapters"]
        by_id = {chapter["chapter_id"]: chapter for chapter in chapters}
        for number in range(1, 15):
            chapter_id = f"ga-{number:03d}"
            self.assertIn(chapter_id, by_id)
            self.assertEqual(number, by_id[chapter_id]["number"])
            generation = "v2/" if number in v2_numbers else ""
            self.assertEqual(f"assets/{generation}chapter-{number:03d}.mp3", by_id[chapter_id]["audio_src"])
'''
if old not in text:
    raise SystemExit("Expected stable-identity test block not found; refusing broad edit")
path.write_text(text.replace(old, new, 1))
subprocess.run([
    "python", "-m", "unittest",
    "tests.test_greg_again_audio_catalog.GregAgainAudioCatalogTest.test_catalog_uses_stable_chapter_identity",
    "-v",
], check=True)
subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
subprocess.run(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], check=True)
subprocess.run(["git", "add", str(path)], check=True)
subprocess.run(["git", "commit", "-m", "Make audio catalog identity test v2-aware"], check=True)
subprocess.run(["git", "push"], check=True)
