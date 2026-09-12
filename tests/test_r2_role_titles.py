import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
R2 = ROOT / "r2"
AUDIT = R2 / "TITLE_ROLE_AUDIT.md"
POLICY = R2 / "TITLE_POLICY.md"
AUDIO_MANIFEST = ROOT / "greg-again" / "audio" / "manifest.json"
HEADING_RE = re.compile(r"^# (?P<prefix>.+?): (?P<title>.+)$")
AUDIT_LINE_RE = re.compile(r"^(?P<number>\d{3})\s+(?P<title>.+)$")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def approved_titles() -> dict[int, str]:
    if not AUDIT.exists():
        raise AssertionError("r2/TITLE_ROLE_AUDIT.md is required role-title authority")

    text = AUDIT.read_text(encoding="utf-8")
    marker = "## Approved title map"
    if marker not in text:
        raise AssertionError(f"{AUDIT}: missing {marker!r}")

    section = text.split(marker, 1)[1]
    in_block = False
    titles: dict[int, str] = {}
    for raw_line in section.splitlines():
        line = raw_line.strip()
        if line.startswith("```"):
            if in_block:
                break
            in_block = True
            continue
        if not in_block or not line:
            continue
        match = AUDIT_LINE_RE.fullmatch(line)
        if match is None:
            raise AssertionError(f"invalid approved title-map line: {raw_line!r}")
        number = int(match.group("number"))
        if number in titles:
            raise AssertionError(f"duplicate approved title for Chapter {number}")
        titles[number] = match.group("title").strip()

    if not titles:
        raise AssertionError("approved R2 title map is empty")
    return titles


def public_numbers() -> list[int]:
    project = read_json(R2 / "data" / "project.json")
    return [int(chapter_id.rsplit("ch", 1)[1]) for chapter_id in project["chapters"]]


def selected_heading_title(number: int) -> str:
    path = R2 / "assets" / "written" / f"ch{number:03d}.md"
    first_line = path.read_text(encoding="utf-8").splitlines()[0]
    match = HEADING_RE.fullmatch(first_line)
    if match is None:
        raise AssertionError(f"{path}: invalid selected chapter heading {first_line!r}")
    return match.group("title")


class R2RoleTitleAuthorityTests(unittest.TestCase):
    def test_approved_map_covers_the_exact_public_frontier(self):
        numbers = public_numbers()
        self.assertEqual(numbers, list(range(1, 119)))
        self.assertEqual(sorted(approved_titles()), numbers)

    def test_selected_written_headings_match_approved_role_titles(self):
        titles = approved_titles()
        for number in public_numbers():
            self.assertEqual(selected_heading_title(number), titles[number], f"Chapter {number}")

    def test_public_manifests_match_role_titles_without_identity_changes(self):
        titles = approved_titles()
        for number in public_numbers():
            path = R2 / "data" / "chapters" / f"ch{number:03d}.json"
            chapter = read_json(path)
            self.assertEqual(chapter["chapter_id"], f"r2-ch{number:03d}")
            self.assertEqual(chapter["display_number"], number)
            self.assertEqual(chapter["title"], titles[number], f"Chapter {number}")
            self.assertEqual(chapter["written"]["path"], f"assets/written/ch{number:03d}.md")

    def test_partial_registry_never_overrides_selected_title_authority(self):
        titles = approved_titles()
        registry = read_json(R2 / "data" / "chapter-registry.json")
        for chapter_id, chapter in registry.get("chapters", {}).items():
            match = re.fullmatch(r"r2-ch(?P<number>\d{3})", chapter_id)
            if match is None:
                continue
            number = int(match.group("number"))
            if number not in titles:
                continue
            self.assertEqual(chapter["display_number"], number)
            self.assertEqual(chapter["title"], titles[number], chapter_id)

    def test_audio_title_metadata_follows_r2_by_stable_number(self):
        titles = approved_titles()
        if not AUDIO_MANIFEST.exists():
            self.skipTest("Greg, Again audio manifest is not present")
        manifest = read_json(AUDIO_MANIFEST)
        for chapter in manifest.get("chapters", []):
            number = chapter.get("number")
            if number not in titles:
                continue
            self.assertEqual(chapter["chapter_id"], f"ga-{number:03d}")
            self.assertEqual(chapter["title"], titles[number], f"ga-{number:03d}")

    def test_policy_names_the_semantic_gate_and_identity_boundary(self):
        policy = POLICY.read_text(encoding="utf-8")
        self.assertIn("Who is Greg in this chapter?", policy)
        self.assertIn("Title wording never owns chapter identity.", policy)
        self.assertIn("Does this title name who Greg is being", policy)
        self.assertIn("The public chapter manifest is the site-facing display surface.", policy)
        self.assertIn("A title-only change must not imply that existing audio is missing", policy)


if __name__ == "__main__":
    unittest.main()
