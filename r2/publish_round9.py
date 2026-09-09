from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "r2"
START = 279
END = 304
EXPERIMENT_REF = "origin/experiment/r2-temporal-c-hybrid"
RECON_DIR = "r2/experiments/temporal-writing/c-hybrid/round-09/reconciled"


def git_show(path: str) -> str:
    return subprocess.check_output(["git", "show", f"{EXPERIMENT_REF}:{path}"], cwd=ROOT, text=True)


def title_and_teaser(prose: str, number: int) -> tuple[str, str]:
    lines = prose.splitlines()
    expected = f"# Chapter {number}: "
    if not lines or not lines[0].startswith(expected):
        raise SystemExit(f"bad chapter heading for {number}")
    title = lines[0][len(expected):].strip()
    teaser = ""
    for line in lines[1:]:
        text = line.strip()
        if not text or text == "---":
            continue
        teaser = text
        break
    if not title or not teaser:
        raise SystemExit(f"missing title/teaser for {number}")
    return title, teaser


# Pull exact reconciled experimental authority into public written surfaces.
for number in range(START, END + 1):
    prose = git_show(f"{RECON_DIR}/ch{number:03d}.md")
    if "Status: **EXPERIMENTAL" in prose or "Story search:" in prose:
        raise SystemExit(f"experimental prelude leaked into chapter {number}")
    (R2 / f"assets/written/ch{number:03d}.md").write_text(prose, encoding="utf-8")

# Advance the prior frontier's navigation without disturbing its media state.
prior_path = R2 / f"data/chapters/ch{START - 1:03d}.json"
prior = json.loads(prior_path.read_text(encoding="utf-8"))
prior["navigation"]["next"] = f"r2-ch{START:03d}"
prior_path.write_text(json.dumps(prior, separators=(",", ":")) + "\n", encoding="utf-8")

# Build new chapter manifests from exact prose headings.
for number in range(START, END + 1):
    prose = (R2 / f"assets/written/ch{number:03d}.md").read_text(encoding="utf-8")
    title, teaser = title_and_teaser(prose, number)
    manifest = {
        "chapter_id": f"r2-ch{number:03d}",
        "display_number": number,
        "title": title,
        "status": "published",
        "book": 1,
        "act": 1,
        "teaser": teaser,
        "audio": {"status": "unavailable", "path": None},
        "written": {"status": "published", "path": f"assets/written/ch{number:03d}.md"},
        "images": [],
        "navigation": {
            "previous": f"r2-ch{number - 1:03d}",
            "next": None if number == END else f"r2-ch{number + 1:03d}",
        },
    }
    path = R2 / f"data/chapters/ch{number:03d}.json"
    path.write_text(json.dumps(manifest, separators=(",", ":")) + "\n", encoding="utf-8")

# Project frontier.
project_path = R2 / "data/project.json"
project = json.loads(project_path.read_text(encoding="utf-8"))
project["current_chapter"] = f"r2-ch{END:03d}"
project["chapters"] = [f"r2-ch{i:03d}" for i in range(1, END + 1)]
project_path.write_text(json.dumps(project, indent=2) + "\n", encoding="utf-8")

# Chapter registry: preserve all prior records exactly and add only new written-state entries.
registry_path = R2 / "data/chapter-registry.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
registry["current_chapter"] = f"r2-ch{END:03d}"
for number in range(START, END + 1):
    prose = (R2 / f"assets/written/ch{number:03d}.md").read_text(encoding="utf-8")
    title, _ = title_and_teaser(prose, number)
    registry["chapters"][f"r2-ch{number:03d}"] = {
        "display_number": number,
        "title": title,
        "status": "in_progress",
        "pipeline": {
            "scene_packets": "in_progress",
            "audio": "not_started",
            "written": "published",
            "story_sync": "in_progress",
            "image_plan": "not_started",
            "image_generation": "not_started",
            "image_review": "not_started",
            "image_integration": "not_started",
        },
        "images": {"target_count": 2, "planned": 0, "generated": 0, "approved": 0, "integrated": 0},
        "last_completed_stage": "written",
        "next_action": "publish_audio_and_plan_images",
    }
registry_path.write_text(json.dumps(registry, separators=(",", ":")) + "\n", encoding="utf-8")

# Advance the reader contract deterministically.
test_path = ROOT / "tests/test_r2_site.py"
test = test_path.read_text(encoding="utf-8")
replacements = {
    "range(1, 279)": "range(1, 305)",
    "'r2-ch278'": "'r2-ch304'",
    "test_written_frontier_is_public_through_chapter_two_hundred_seventy_eight": "test_written_frontier_is_public_through_chapter_three_hundred_four",
    "None if number == 278": "None if number == 304",
}
for old, new in replacements.items():
    if old not in test:
        raise SystemExit(f"test frontier anchor not found: {old}")
    test = test.replace(old, new)
test_path.write_text(test, encoding="utf-8")

# Local structural verification before the formal test suite.
assert json.loads(project_path.read_text(encoding="utf-8"))["current_chapter"] == "r2-ch304"
assert json.loads(registry_path.read_text(encoding="utf-8"))["current_chapter"] == "r2-ch304"
for number in range(1, END + 1):
    assert (R2 / f"data/chapters/ch{number:03d}.json").exists(), number
for number in range(START, END + 1):
    chapter = json.loads((R2 / f"data/chapters/ch{number:03d}.json").read_text(encoding="utf-8"))
    assert chapter["written"]["status"] == "published"
    assert chapter["audio"]["status"] == "unavailable"

print("built R2 written publication through Chapter 304")
