#!/usr/bin/env python3
"""Atomically claim the next free Greg, Again Audio Score chapter.

Resolution is read-only. Claiming is successful only when this process creates the
remote single-chapter branch. An existing/up-to-date branch never counts as a win.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from scripts import audio_score_next


def push_created_branch(output: str, branch: str) -> bool:
    target = f"refs/heads/{branch}"
    for raw in output.splitlines():
        line = raw.strip()
        if not line.startswith("*"):
            continue
        if target in line and "[new branch]" in line:
            return True
    return False


def remote_branch_exists(remote: str, branch: str) -> bool:
    result = subprocess.run(
        ["git", "ls-remote", "--heads", remote, f"refs/heads/{branch}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def create_only_branch(remote: str, branch: str, base_ref: str = "origin/main") -> dict[str, object]:
    base = subprocess.run(
        ["git", "rev-parse", base_ref],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    result = subprocess.run(
        ["git", "push", "--porcelain", remote, f"{base}:refs/heads/{branch}"],
        check=False,
        capture_output=True,
        text=True,
    )
    output = "\n".join(part for part in (result.stdout, result.stderr) if part)
    if result.returncode == 0 and push_created_branch(output, branch):
        return {"created": True, "branch": branch, "base_sha": base}
    if remote_branch_exists(remote, branch):
        return {"created": False, "collision": True, "branch": branch, "base_sha": base}
    raise RuntimeError(f"claim push failed without a competing branch:\n{output.strip()}")


def claim_next(
    score_dir: Path,
    manifest_path: Path,
    *,
    generation: str = "v2",
    minimum: int = 1,
    maximum: int = 30,
    remote: str = "origin",
    base_branch: str = "main",
) -> dict[str, object]:
    audio_score_next.generation_config(generation)
    fetch = subprocess.run(
        ["git", "fetch", remote, base_branch],
        check=False,
        capture_output=True,
        text=True,
    )
    if fetch.returncode != 0:
        raise RuntimeError(f"could not refresh {remote}/{base_branch}:\n{fetch.stderr.strip()}")

    base_ref = f"{remote}/{base_branch}"
    while True:
        candidate = audio_score_next.resolve_next_candidate(
            score_dir,
            manifest_path,
            audio_score_next.git_claim_refs(generation, remote),
            generation=generation,
            minimum=minimum,
            maximum=maximum,
        )
        if candidate is None:
            return {"status": "none", "generation": generation}
        claim = create_only_branch(remote, str(candidate["claim_branch"]), base_ref=base_ref)
        if claim.get("created"):
            return {"status": "claimed", **candidate, **claim}
        # Another worker won this chapter between resolution and mutation.
        # Re-resolve from remote authority and try the next free candidate.


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--generation", choices=sorted(audio_score_next.GENERATION_CONFIG), default="v2")
    parser.add_argument("--score-dir")
    parser.add_argument("--manifest")
    parser.add_argument("--minimum", type=int, default=1)
    parser.add_argument("--maximum", type=int, default=30)
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--base-branch", default="main")
    args = parser.parse_args()
    config = audio_score_next.generation_config(args.generation)
    result = claim_next(
        Path(args.score_dir or config["score_dir"]),
        Path(args.manifest or config["manifest"]),
        generation=args.generation,
        minimum=args.minimum,
        maximum=args.maximum,
        remote=args.remote,
        base_branch=args.base_branch,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
