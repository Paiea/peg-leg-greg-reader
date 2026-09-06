from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_character_references import audit_character_references

CATALOG_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "CHARACTER_CONTINUITY_REPORT.md"


def _usage_counts(candidates: list[dict], registry: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in [*candidates, *registry]:
        for character in record.get("characters", []):
            if isinstance(character, str) and character.strip():
                name = character.strip()
                counts[name] = counts.get(name, 0) + 1
    return counts


def _manual_reference_records(record: dict) -> list[dict]:
    metadata = record.get("reference_metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
    output: list[dict] = []
    for asset in record.get("reference_assets", []):
        if not isinstance(asset, str) or not asset.strip():
            continue
        item = metadata.get(asset, {})
        output.append(item if isinstance(item, dict) else {})
    return output


def summarize_character_continuity(
    catalog: dict[str, dict],
    audit_issues: list[dict],
    candidates: list[dict] | None = None,
    registry: list[dict] | None = None,
) -> dict:
    candidates = candidates or []
    registry = registry or []
    usage = _usage_counts(candidates, registry)
    issues_by_character: dict[str, int] = {}
    for issue in audit_issues:
        character = issue.get("character", "")
        if character:
            issues_by_character[character] = issues_by_character.get(character, 0) + 1

    characters: dict[str, dict] = {}
    targets: list[dict] = []
    for character, record in catalog.items():
        manual_assets = [asset for asset in record.get("reference_assets", []) if isinstance(asset, str) and asset.strip()]
        structured = [reference for reference in record.get("references", []) if isinstance(reference, dict) and reference.get("asset")]
        manual_records = _manual_reference_records(record)
        all_records = [*manual_records, *structured]
        tags = [{str(tag) for tag in reference.get("tags", [])} for reference in all_records]
        view_angles = sorted({str(reference.get("view_angle")) for reference in all_records if reference.get("view_angle")})
        pose_families = sorted({str(reference.get("pose_family")) for reference in all_records if reference.get("pose_family")})
        scene_tags = sorted({
            str(tag)
            for reference in all_records
            for tag in reference.get("scene_tags", [])
            if str(tag).strip()
        })
        missing_view = sum(1 for reference in all_records if not reference.get("view_angle"))
        missing_pose = sum(1 for reference in all_records if not reference.get("pose_family"))
        missing_scene = sum(1 for reference in all_records if not reference.get("scene_tags"))
        reference_count = len(manual_assets) + len(structured)
        character_usage = usage.get(character, 0)
        gap_units = missing_view + missing_pose + missing_scene
        if reference_count == 0:
            gap_units += 4
        priority_score = character_usage * 5 + gap_units * 4 + issues_by_character.get(character, 0) * 8
        characters[character] = {
            "total_references": reference_count,
            "manual_references": len(manual_assets),
            "structured_references": len(structured),
            "above_waist_references": sum(1 for tag_set in tags if "above_waist" in tag_set),
            "view_angles": view_angles,
            "pose_families": pose_families,
            "scene_tags": scene_tags,
            "missing_view_angle": missing_view,
            "missing_pose_family": missing_pose,
            "missing_scene_tags": missing_scene,
            "usage_count": character_usage,
            "priority_score": priority_score,
            "audit_issues": issues_by_character.get(character, 0),
            "has_appearance_notes": bool(str(record.get("appearance_notes", "")).strip()),
        }
        targets.append({
            "character": character,
            "priority_score": priority_score,
            "usage_count": character_usage,
            "gap_units": gap_units,
        })

    uncataloged = sorted(
        (
            {"character": character, "usage_count": count}
            for character, count in usage.items()
            if character not in catalog
        ),
        key=lambda item: (-item["usage_count"], item["character"]),
    )
    targets.sort(key=lambda item: (-item["priority_score"], item["character"]))
    return {
        "characters": characters,
        "total_characters": len(characters),
        "total_audit_issues": len(audit_issues),
        "top_metadata_fix_targets": targets[:10],
        "uncataloged_recurring_characters": [item["character"] for item in uncataloged[:10]],
        "uncataloged_recurring_character_usage": uncataloged[:10],
    }


def render_character_continuity_report(summary: dict) -> str:
    lines = [
        "# PEG-LEG GREG — CHARACTER CONTINUITY",
        "",
        f"- Cataloged characters: {summary['total_characters']}",
        f"- Reference audit issues: {summary['total_audit_issues']}",
        "",
        "## Top metadata repair targets",
        "",
    ]
    targets = summary.get("top_metadata_fix_targets", [])
    if targets:
        for target in targets:
            lines.append(
                f"- {target['character']}: priority {target['priority_score']} · usage {target['usage_count']} · gap units {target['gap_units']}"
            )
    else:
        lines.append("- none")
    lines.extend(["", "## Uncataloged recurring characters", ""])
    uncataloged = summary.get("uncataloged_recurring_character_usage", [])
    if uncataloged:
        for item in uncataloged:
            lines.append(f"- {item['character']}: usage {item['usage_count']}")
    else:
        lines.append("- none")
    lines.append("")

    for character, record in summary["characters"].items():
        lines.extend(
            [
                f"## {character}",
                "",
                f"- References: {record['total_references']} ({record['manual_references']} manual, {record['structured_references']} promoted)",
                f"- Usage signals: {record['usage_count']}",
                f"- Repair priority: {record['priority_score']}",
                f"- Above-waist anchors: {record['above_waist_references']}",
                f"- View angles: {', '.join(record['view_angles']) if record['view_angles'] else 'not tagged yet'}",
                f"- Pose families: {', '.join(record['pose_families']) if record['pose_families'] else 'not tagged yet'}",
                f"- Scene tags: {', '.join(record['scene_tags']) if record['scene_tags'] else 'not tagged yet'}",
                f"- Missing view-angle metadata: {record['missing_view_angle']}",
                f"- Missing pose-family metadata: {record['missing_pose_family']}",
                f"- Missing scene-tag metadata: {record['missing_scene_tags']}",
                f"- Appearance notes: {'yes' if record['has_appearance_notes'] else 'missing'}",
                f"- Audit issues: {record['audit_issues']}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    audit_issues = audit_character_references(catalog, registry)
    summary = summarize_character_continuity(catalog, audit_issues, candidates=candidates, registry=registry)
    text = render_character_continuity_report(summary) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print("character continuity report already current")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote character continuity report for {summary['total_characters']} characters")


if __name__ == "__main__":
    main()
