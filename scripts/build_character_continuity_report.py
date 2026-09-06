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
OUTPUT_PATH = ROOT / "state" / "visual" / "CHARACTER_CONTINUITY_REPORT.md"


def summarize_character_continuity(catalog: dict[str, dict], audit_issues: list[dict]) -> dict:
    issues_by_character: dict[str, int] = {}
    for issue in audit_issues:
        character = issue.get("character", "")
        if character:
            issues_by_character[character] = issues_by_character.get(character, 0) + 1

    characters: dict[str, dict] = {}
    for character, record in catalog.items():
        manual_assets = [asset for asset in record.get("reference_assets", []) if isinstance(asset, str) and asset.strip()]
        structured = [reference for reference in record.get("references", []) if isinstance(reference, dict) and reference.get("asset")]
        tags = [
            {str(tag) for tag in reference.get("tags", [])}
            for reference in structured
        ]
        view_angles = sorted({
            str(reference.get("view_angle"))
            for reference in structured
            if reference.get("view_angle")
        })
        pose_families = sorted({
            str(reference.get("pose_family"))
            for reference in structured
            if reference.get("pose_family")
        })
        scene_tags = sorted({
            str(tag)
            for reference in structured
            for tag in reference.get("scene_tags", [])
            if str(tag).strip()
        })
        characters[character] = {
            "total_references": len(manual_assets) + len(structured),
            "manual_references": len(manual_assets),
            "structured_references": len(structured),
            "above_waist_references": sum(1 for tag_set in tags if "above_waist" in tag_set),
            "view_angles": view_angles,
            "pose_families": pose_families,
            "scene_tags": scene_tags,
            "audit_issues": issues_by_character.get(character, 0),
            "has_appearance_notes": bool(str(record.get("appearance_notes", "")).strip()),
        }
    return {
        "characters": characters,
        "total_characters": len(characters),
        "total_audit_issues": len(audit_issues),
    }


def render_character_continuity_report(summary: dict) -> str:
    lines = [
        "# PEG-LEG GREG — CHARACTER CONTINUITY",
        "",
        f"- Cataloged characters: {summary['total_characters']}",
        f"- Reference audit issues: {summary['total_audit_issues']}",
        "",
    ]
    for character, record in summary["characters"].items():
        lines.extend(
            [
                f"## {character}",
                "",
                f"- References: {record['total_references']} ({record['manual_references']} manual, {record['structured_references']} promoted)",
                f"- Above-waist anchors: {record['above_waist_references']}",
                f"- View angles: {', '.join(record['view_angles']) if record['view_angles'] else 'not tagged yet'}",
                f"- Pose families: {', '.join(record['pose_families']) if record['pose_families'] else 'not tagged yet'}",
                f"- Scene tags: {', '.join(record['scene_tags']) if record['scene_tags'] else 'not tagged yet'}",
                f"- Appearance notes: {'yes' if record['has_appearance_notes'] else 'missing'}",
                f"- Audit issues: {record['audit_issues']}",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    audit_issues = audit_character_references(catalog, registry)
    summary = summarize_character_continuity(catalog, audit_issues)
    text = render_character_continuity_report(summary) + "\n"
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print("character continuity report already current")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote character continuity report for {summary['total_characters']} characters")


if __name__ == "__main__":
    main()
