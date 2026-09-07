#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts import rehearsal_engine

DEFAULT_MANIFEST = Path("state/editorial/rehearsal/campaigns/canon-001-020-character-discovery-returns.json")
DEFAULT_REPORT = Path("state/editorial/rehearsal/campaigns/canon-001-020-character-discovery-report.json")


def apply_patch_to_text(
    text: str,
    patch: dict,
    *,
    target_branch: str,
    policy_mode: str = "production",
) -> tuple[str, dict]:
    policy = rehearsal_engine.editorial_return_policy(policy_mode)
    before = patch.get("before")
    after = patch.get("after")
    if not isinstance(before, str) or not before:
        raise ValueError("patch before text is required")
    if not isinstance(after, str) or not after:
        raise ValueError("patch after text is required")

    count = text.count(before)
    if count != 1:
        raise ValueError(f"exact source match required for {patch.get('id')}: found {count}")

    candidate = {
        "actor_prefers": patch.get("actor_prefers") is True,
        "dramatic_lock_status": patch.get("dramatic_lock_status"),
        "reader_check": patch.get("reader_check"),
        "source_match": True,
        "target_branch": target_branch,
        "changed_surfaces": copy.deepcopy(patch.get("changed_surfaces", [])),
    }
    if not rehearsal_engine.can_auto_apply_rehearsal_candidate(candidate, policy):
        raise ValueError(f"write gate rejected {patch.get('id')}")

    interpretation = patch.get("performed_interpretation")
    if interpretation is not None:
        if not isinstance(interpretation, dict):
            raise ValueError("performed_interpretation must be an object")
        if interpretation.get("authority") not in {"rehearsal_hypothesis", "supported"}:
            raise ValueError("performed_interpretation authority must be rehearsal_hypothesis or supported")
        if not isinstance(interpretation.get("summary"), str) or not interpretation["summary"].strip():
            raise ValueError("performed_interpretation summary is required")

    updated = text.replace(before, after, 1)
    record = {
        "patch_id": patch.get("id"),
        "chapter": patch.get("chapter"),
        "actor": patch.get("actor"),
        "role": patch.get("role"),
        "take_id": patch.get("take_id"),
        "variance_group_id": patch.get("variance_group_id"),
        "supporting_actors": copy.deepcopy(patch.get("supporting_actors", [])),
        "changed_surfaces": copy.deepcopy(patch.get("changed_surfaces", [])),
        "reason": patch.get("reason"),
        "performed_interpretation": copy.deepcopy(interpretation),
        "dramatic_lock_status": "preserved",
        "reader_check": "pass",
        "source_match": True,
        "policy_mode": policy["mode"],
        "policy_scope": policy["max_local_scope"],
    }
    return updated, record


def apply_manifest(root: str | Path, manifest: dict, *, write: bool = False) -> dict:
    root = Path(root)
    if manifest.get("mode") != "free_production":
        raise ValueError("manifest mode must be free_production")
    target_branch = manifest.get("target_branch")
    if not isinstance(target_branch, str) or not target_branch:
        raise ValueError("manifest target_branch is required")
    patches = manifest.get("patches")
    if not isinstance(patches, list):
        raise ValueError("manifest patches must be a list")

    by_chapter: dict[int, list[dict]] = {}
    for patch in patches:
        if not isinstance(patch, dict):
            raise ValueError("manifest patches must be objects")
        chapter = patch.get("chapter")
        if not isinstance(chapter, int) or chapter < 1:
            raise ValueError("patch chapter must be a positive integer")
        by_chapter.setdefault(chapter, []).append(patch)

    records: list[dict] = []
    changed_chapters: list[int] = []
    for chapter, chapter_patches in sorted(by_chapter.items()):
        path = root / "chapters" / f"{chapter:03d}.html"
        text = path.read_text(encoding="utf-8")
        updated = text
        for patch in chapter_patches:
            updated, record = apply_patch_to_text(
                updated,
                patch,
                target_branch=target_branch,
                policy_mode="production",
            )
            records.append(record)
        if updated != text:
            changed_chapters.append(chapter)
            if write:
                path.write_text(updated, encoding="utf-8")

    return {
        "schema": "rehearsal_free_returns_report/v1",
        "mode": "free_production",
        "target_branch": target_branch,
        "patches_ready": len(records),
        "patches_applied": len(records) if write else 0,
        "changed_chapters": changed_chapters,
        "records": records,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply validated FREE REHEARSAL prose returns with exact-source gates.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    manifest_path = root / args.manifest
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    report = apply_manifest(root, manifest, write=args.write)
    report_path = root / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "patches_ready": report["patches_ready"],
        "patches_applied": report["patches_applied"],
        "changed_chapters": report["changed_chapters"],
        "report": str(report_path.relative_to(root)),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
