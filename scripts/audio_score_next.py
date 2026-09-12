#!/usr/bin/env python3
"""Resolve the next free Greg, Again Audio Score v2 production chapter."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable

SCORE_RE = re.compile(r"^ch(?P<chapter>\d{3})\.md$")
CLAIM_RE = re.compile(
    r"^(?:refs/(?:heads|remotes/origin)/)?audio/v2-greg-again-ch(?P<chapter>\d{3})(?:-|$)"
)


def chapter_from_claim_ref(ref: str) -> int | None:
    match = CLAIM_RE.match(ref.strip())
    return int(match.group("chapter")) if match else None


def _score_inventory(score_dir: Path, minimum: int, maximum: int) -> list[int]:
    chapters: list[int] = []
    for path in score_dir.iterdir():
        match = SCORE_RE.match(path.name)
        if not match:
            continue
        chapter = int(match.group("chapter"))
        if minimum <= chapter <= maximum:
            chapters.append(chapter)
    return sorted(set(chapters))


def _published_inventory(manifest_path: Path) -> set[int]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    published: set[int] = set()
    for entry in data.get("chapters", []):
        number = entry.get("number")
        if number is not None:
            published.add(int(number))
    return published


def resolve_next_candidate(
    score_dir: Path,
    manifest_path: Path,
    claim_refs: Iterable[str],
    *,
    minimum: int = 1,
    maximum: int = 30,
) -> dict[str, object] | None:
    scores = _score_inventory(Path(score_dir), minimum, maximum)
    published = _published_inventory(Path(manifest_path))
    claimed = {
        chapter
        for ref in claim_refs
        if (chapter := chapter_from_claim_ref(ref)) is not None
    }

    for chapter in scores:
        if chapter in published or chapter in claimed:
            continue
        padded = f"{chapter:03d}"
        return {
            "chapter": chapter,
            "chapter_padded": padded,
            "source": str(Path(score_dir) / f"ch{padded}.md"),
            "claim_branch": f"audio/v2-greg-again-ch{padded}-auto",
            "published_count": len(published),
            "claimed_count": len(claimed),
        }
    return None


def git_claim_refs() -> list[str]:
    refs: set[str] = set()
    local = subprocess.run(
        ["git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes/origin"],
        check=False,
        capture_output=True,
        text=True,
    )
    if local.returncode == 0:
        refs.update(line.strip() for line in local.stdout.splitlines() if line.strip())

    remote = subprocess.run(
        ["git", "ls-remote", "--heads", "origin", "audio/v2-greg-again-ch*"],
        check=False,
        capture_output=True,
        text=True,
    )
    if remote.returncode == 0:
        for line in remote.stdout.splitlines():
            parts = line.split()
            if len(parts) == 2:
                refs.add(parts[1])
    return sorted(refs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--score-dir", default="r2/assets/audio-score")
    parser.add_argument("--manifest", default="greg-again/audio/v2/manifest.json")
    parser.add_argument("--minimum", type=int, default=1)
    parser.add_argument("--maximum", type=int, default=30)
    parser.add_argument("--claims-file", help="Optional newline-delimited branch/ref names for deterministic/offline use")
    args = parser.parse_args()

    if args.claims_file:
        claim_refs = Path(args.claims_file).read_text(encoding="utf-8").splitlines()
    else:
        claim_refs = git_claim_refs()

    result = resolve_next_candidate(
        Path(args.score_dir),
        Path(args.manifest),
        claim_refs,
        minimum=args.minimum,
        maximum=args.maximum,
    )
    print(json.dumps({"status": "available", **result} if result else {"status": "none"}, indent=2))


if __name__ == "__main__":
    main()
