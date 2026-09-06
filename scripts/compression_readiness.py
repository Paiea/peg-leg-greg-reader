#!/usr/bin/env python3
"""Classify what is safe, migratable, or blocking before structural compression."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from chapter_dependency_scan import scan_dependencies
from chapter_registry import build_registry


def item(code: str, message: str, **details) -> dict:
    row = {"code": code, "message": message}
    row.update(details)
    return row


def build_readiness_report(registry: dict, dependencies: dict) -> dict:
    diagnostics = registry.get("diagnostics", {})
    chapters = registry.get("chapters", [])
    safe_now: list[dict] = []
    needs_migration: list[dict] = []
    blocked: list[dict] = []

    safe_now.append(item(
        "read_only_audit",
        "Whole-book structural mapping and hotspot audit are safe because they do not mutate prose, numbering, URLs, or art.",
    ))

    if chapters:
        safe_now.append(item(
            "stable_identity_inventory",
            "Stable IDs can be generated for current discovered chapter authority without renumbering the book.",
            chapter_count=len(chapters),
        ))
    else:
        blocked.append(item(
            "no_manuscript_chapters",
            "No manuscript chapters were discovered, so structural editing has no reliable identity base.",
        ))

    gaps = diagnostics.get("manuscript_gaps", []) or []
    if gaps:
        blocked.append(item(
            "manuscript_gaps",
            "Current checkout has gaps in discovered chapter authority that must be resolved before destructive structural editing.",
            chapters=gaps,
        ))

    conflicts = diagnostics.get("authority_conflicts", []) or []
    if conflicts:
        blocked.append(item(
            "authority_conflicts",
            "More than one top-priority source claims the same chapter. Resolve authority before structural editing.",
            conflicts=conflicts,
        ))

    reader_only = diagnostics.get("reader_only_chapters", []) or []
    if reader_only:
        blocked.append(item(
            "reader_only_chapters",
            "Published/generated reader chapters exist without matching discovered manuscript authority.",
            chapters=reader_only,
        ))

    stale_by = diagnostics.get("chapter_index_stale_by")
    if isinstance(stale_by, int) and stale_by > 0:
        needs_migration.append(item(
            "stale_chapter_index",
            "The legacy chapter index trails current manuscript authority and must not drive compression or publication rebuilds.",
            stale_by=stale_by,
            index_endpoint=diagnostics.get("chapter_index_endpoint"),
            manuscript_endpoint=diagnostics.get("manuscript_endpoint"),
        ))

    title_mismatches = diagnostics.get("chapter_index_title_mismatches", []) or []
    if title_mismatches:
        needs_migration.append(item(
            "chapter_index_title_mismatches",
            "Legacy chapter-index titles disagree with higher manuscript authority for some chapters.",
            mismatches=title_mismatches,
        ))

    manuscript_only = diagnostics.get("manuscript_only_chapters", []) or []
    if manuscript_only:
        needs_migration.append(item(
            "manuscript_only_chapters",
            "Current manuscript contains chapters not represented by generated reader pages. This is expected for unpublished/unillustrated edge material but publication rebuilds must account for it.",
            count=len(manuscript_only),
            chapters=manuscript_only,
        ))

    reference_count = int(dependencies.get("reference_count", 0) or 0)
    if reference_count:
        needs_migration.append(item(
            "numeric_dependencies",
            "Chapter numbers remain embedded across repository surfaces and require resolver or migration handling before renumbering.",
            reference_count=reference_count,
            counts_by_kind=dependencies.get("counts_by_kind", {}),
            counts_by_file_category=dependencies.get("counts_by_file_category", {}),
            counts_by_risk=dependencies.get("counts_by_risk", {}),
        ))
    else:
        safe_now.append(item(
            "no_numeric_dependencies",
            "No chapter-number-coupled repository references were detected by the current scanner.",
        ))

    if blocked:
        overall_status = "BLOCKED"
    elif needs_migration:
        overall_status = "NEEDS_MIGRATION"
    else:
        overall_status = "SAFE_NOW"

    return {
        "schema_version": 1,
        "overall_status": overall_status,
        "safe_now": safe_now,
        "needs_migration": needs_migration,
        "blocked_before_structural_editing": blocked,
        "summary": {
            "registry_chapters": len(chapters),
            "manuscript_endpoint": diagnostics.get("manuscript_endpoint"),
            "reader_chapter_count": diagnostics.get("reader_chapter_count"),
            "dependency_references": reference_count,
            "safe_item_count": len(safe_now),
            "migration_item_count": len(needs_migration),
            "blocker_count": len(blocked),
        },
        "interpretation": (
            "SAFE_NOW items may proceed without structural mutation. NEEDS_MIGRATION items do not block read-only audit, "
            "but must be handled before renumber publication. BLOCKED items must be resolved before merge/cut execution."
        ),
    }


def build_current_report(root: Path) -> dict:
    registry = build_registry(root)
    dependencies = scan_dependencies(root)
    return build_readiness_report(registry, dependencies)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path, default=Path("publishing/compression_readiness.json"))
    parser.add_argument("--stdout", action="store_true")
    args = parser.parse_args()
    payload = build_current_report(args.root)
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.stdout:
        print(rendered, end="")
    else:
        output = args.output if args.output.is_absolute() else args.root / args.output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        print(f'wrote compression readiness report ({payload["overall_status"]}) to {output}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
