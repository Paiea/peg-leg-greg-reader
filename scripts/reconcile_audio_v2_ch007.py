import json
import subprocess
from pathlib import Path

BASE = "origin/audio-score/chapters-001-010"


def from_base(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{BASE}:{path}"], text=True)


# Rebuild the shared v2 registry from newest authority, then add Chapter 007 only.
v2_path = Path("greg-again/audio/v2/manifest.json")
v2 = json.loads(from_base(str(v2_path)))
chapters = [c for c in v2.get("chapters", []) if c.get("number") != 7 and c.get("chapter_id") != "ga-007"]
chapters.append(
    {
        "chapter_id": "ga-007",
        "number": 7,
        "title": "The Extra Guard",
        "status": "verified_unlistened",
        "source": "r2/assets/audio-score/ch007.md",
        "source_blob_sha": "d179b9621a0903c286171b707264b6256600b99f",
        "voice": "deep",
        "take_count": 31,
        "duration_seconds": 623.448,
        "audio_src": "assets/v2/chapter-007.mp3",
        "verification": "greg-again/audio/v2/verification/007/",
    }
)
chapters.sort(key=lambda c: c.get("number", 10**9))
v2["chapters"] = chapters
v2_path.write_text(json.dumps(v2, indent=2) + "\n")

# Rebuild the public catalog from newest authority, preserving all sibling migrations.
public_path = Path("greg-again/audio/manifest.json")
public = json.loads(from_base(str(public_path)))
matches = [c for c in public["chapters"] if c.get("number") == 7 or c.get("chapter_id") == "ga-007"]
if len(matches) != 1:
    raise SystemExit(f"expected exactly one public Chapter 007 entry, found {len(matches)}")
chapter = matches[0]
chapter["audio_finish"] = "audio-score-v2"
chapter["take_count"] = 31
chapter["duration_seconds"] = 623.448
chapter["audio_src"] = "assets/v2/chapter-007.mp3"
chapter["note"] = (
    "Audio Score v2 Chapter 7 from the exact audio-native score. Thirty-one preview-safe "
    "deep-voice takes preserve moving-action causality, Meral's redirection from stopping to "
    "turning the wagon, and Greg's tiny brace under load. Exact score coverage, ordered capture, "
    "MP3 playability, and the chapter settling tail were mechanically verified; subjective human "
    "listen-back remains separate."
)
public_path.write_text(json.dumps(public, indent=2) + "\n")

# Restore the complete catalog contract from newest authority and teach it mixed v1/v2 routing.
test_path = Path("tests/test_greg_again_audio_catalog.py")
test = from_base(str(test_path))
old = '''        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
'''
new = '''        manifest = json.loads((AUDIO_ROOT / "manifest.json").read_text(encoding="utf-8"))
        v2_manifest = json.loads((AUDIO_ROOT / "v2" / "manifest.json").read_text(encoding="utf-8"))
        verified_v2 = {
            chapter["number"]
            for chapter in v2_manifest.get("chapters", [])
            if chapter.get("status") in {"verified", "verified_unlistened"}
        }
        self.assertIn("chapter_id and number are stable identity", manifest["identity_policy"])
'''
if old not in test:
    raise SystemExit("catalog manifest anchor not found")
test = test.replace(old, new, 1)

old = '            self.assertEqual(f"assets/chapter-{number:03d}.mp3", by_id[chapter_id]["audio_src"])\n'
new = '''            expected_src = (
                f"assets/v2/chapter-{number:03d}.mp3"
                if number in verified_v2
                else f"assets/chapter-{number:03d}.mp3"
            )
            self.assertEqual(expected_src, by_id[chapter_id]["audio_src"])
'''
if old not in test:
    raise SystemExit("catalog audio_src anchor not found")
test = test.replace(old, new, 1)

old = '''        self.assertEqual("processing-space", by_id["ga-007"]["audio_finish"])
        self.assertEqual(14, by_id["ga-007"]["take_count"])
        self.assertEqual(818.136, by_id["ga-007"]["duration_seconds"])
'''
new = '''        self.assertEqual("audio-score-v2", by_id["ga-007"]["audio_finish"])
        self.assertEqual(31, by_id["ga-007"]["take_count"])
        self.assertEqual(623.448, by_id["ga-007"]["duration_seconds"])
'''
if old not in test:
    raise SystemExit("Chapter 007 catalog metadata anchor not found")
test = test.replace(old, new, 1)
test_path.write_text(test)

# Sanity checks before CI.
assert any(c.get("number") == 9 for c in v2["chapters"]), "newer Chapter 009 authority was not preserved"
assert next(c for c in public["chapters"] if c.get("number") == 9)["audio_src"] == "assets/v2/chapter-009.mp3"
assert next(c for c in public["chapters"] if c.get("number") == 7)["audio_src"] == "assets/v2/chapter-007.mp3"
print("reconciled Chapter 007 onto newest Audio Score authority while preserving sibling v2 routes")
