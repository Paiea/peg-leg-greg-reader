from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "state" / "visual" / "CHARACTER_VISUAL_REFERENCES.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"
OUTPUT_PATH = ROOT / "state" / "visual" / "CHARACTER_REFERENCE_AUDIT.md"


def audit_character_references(
    catalog: dict[str, dict],
    registry: list[dict],
    available_assets: set[str] | None = None,
) -> list[dict]:
    registry_by_id = {
        record.get("id"): record
        for record in registry
        if isinstance(record.get("id"), str)
    }
    issues: list[dict] = []

    for character, character_record in catalog.items():
        seen: set[str] = set()
        references: list[tuple[str, dict | None]] = []
        for asset in character_record.get("reference_assets", []):
            if isinstance(asset, str) and asset.strip():
                references.append((asset.strip(), None))
        for reference in character_record.get("references", []):
            if isinstance(reference, dict):
                asset = reference.get("asset")
                if isinstance(asset, str) and asset.strip():
                    references.append((asset.strip(), reference))

        for asset, reference in references:
            if asset in seen:
                issues.append({"character": character, "asset": asset, "code": "duplicate_asset"})
            seen.add(asset)

            exists = asset in available_assets if available_assets is not None else (ROOT / asset).exists()
            if not exists:
                issues.append({"character": character, "asset": asset, "code": "missing_asset"})

            if reference:
                registry_id = reference.get("registry_id")
                if registry_id:
                    registry_record = registry_by_id.get(registry_id)
                    if registry_record is None:
                        issues.append({"character": character, "asset": asset, "code": "stale_registry_reference"})
                    elif registry_record.get("status") not in {"approved", "live"}:
                        issues.append({"character": character, "asset": asset, "code": "bad_registry_status"})

                tags = {str(tag) for tag in reference.get("tags", [])}
                if character == "Greg" and tags & {"full_body", "lower_body_visible"} and "above_waist" not in tags:
                    issues.append({"character": character, "asset": asset, "code": "greg_lower_body_risk"})

        notes = character_record.get("appearance_notes", "")
        if not isinstance(notes, str) or not notes.strip():
            issues.append({"character": character, "asset": "", "code": "missing_appearance_notes"})

    return issues


def render_audit_report(issues: list[dict]) -> str:
    lines = ["# PEG-LEG GREG — CHARACTER REFERENCE AUDIT", ""]
    if not issues:
        lines.append("No character reference issues detected.")
        lines.append("")
        return "\n".join(lines)
    lines.append(f"Issues: {len(issues)}")
    lines.append("")
    for issue in issues:
        lines.append(
            f"- `{issue['code']}` — {issue.get('character', '')}: {issue.get('asset', '')}".rstrip()
        )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8")) if CATALOG_PATH.exists() else {}
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else []
    issues = audit_character_references(catalog, registry)
    text = render_audit_report(issues)
    previous = OUTPUT_PATH.read_text(encoding="utf-8") if OUTPUT_PATH.exists() else None
    if previous == text:
        print(f"character reference audit already current: {len(issues)} issues")
        return
    OUTPUT_PATH.write_text(text, encoding="utf-8")
    print(f"wrote character reference audit: {len(issues)} issues")


if __name__ == "__main__":
    main()
