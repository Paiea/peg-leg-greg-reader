from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import FIT_TARGETS, PRESENTATION_ROLES, load_registry, validate_registry

APPROVALS_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_APPROVALS.json"
REGISTRY_PATH = ROOT / "state" / "visual" / "ILLUSTRATION_REGISTRY.json"


def apply_approvals(registry: list[dict], approvals: list[dict]) -> tuple[list[dict], int]:
    updated = [dict(record) for record in registry]
    changed = 0
    seen: set[str] = set()
    for approval in approvals:
        candidate_id = approval.get("candidate_id")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("illustration approval requires candidate_id")
        if candidate_id in seen:
            raise ValueError(f"duplicate illustration approval: {candidate_id}")
        seen.add(candidate_id)
        asset = approval.get("asset")
        if not isinstance(asset, str) or not asset.strip():
            raise ValueError(f"illustration approval {candidate_id} requires asset")

        matches = [record for record in updated if record.get("candidate_id") == candidate_id]
        if not matches:
            raise ValueError(f"illustration approval {candidate_id} has no generated registry record")
        exact = [record for record in matches if record.get("source_asset") == asset]
        if not exact:
            raise ValueError(f"illustration approval {candidate_id} asset does not match generated asset")
        record = exact[0]
        if record.get("status") in {"approved", "live", "rejected"}:
            continue
        if record.get("status") != "generated":
            raise ValueError(f"illustration approval {candidate_id} requires generated status, found {record.get('status')!r}")

        decision = approval.get("decision", "approve")
        if decision == "reject":
            reason = approval.get("reason", "")
            if not isinstance(reason, str) or not reason.strip():
                raise ValueError(f"illustration rejection {candidate_id} requires reason")
            record["status"] = "rejected"
            record["live_asset"] = ""
            record["notes"] = f"Rejected: {reason.strip()}"
            changed += 1
            continue
        if decision != "approve":
            raise ValueError(f"illustration approval {candidate_id} has invalid decision: {decision!r}")

        approved_fit = approval.get("approved_fit")
        if approved_fit not in FIT_TARGETS:
            raise ValueError(f"illustration approval {candidate_id} has invalid approved_fit: {approved_fit!r}")
        alt_text = approval.get("alt_text")
        if not isinstance(alt_text, str) or not alt_text.strip():
            raise ValueError(f"illustration approval {candidate_id} requires alt_text")
        caption = approval.get("caption", "")
        if not isinstance(caption, str):
            raise ValueError(f"illustration approval {candidate_id} caption must be text")

        presentation_role = approval.get("presentation_role")
        if presentation_role is not None and presentation_role not in PRESENTATION_ROLES:
            raise ValueError(f"illustration approval {candidate_id} has invalid presentation_role: {presentation_role!r}")
        editorial_purpose = approval.get("editorial_purpose")
        if editorial_purpose is not None and (not isinstance(editorial_purpose, str) or not editorial_purpose.strip()):
            raise ValueError(f"illustration approval {candidate_id} editorial_purpose must be non-empty text")
        editorial_note = approval.get("editorial_note")
        if editorial_note is not None and not isinstance(editorial_note, str):
            raise ValueError(f"illustration approval {candidate_id} editorial_note must be text")

        record["status"] = "approved"
        record["live_asset"] = asset
        record["approved_fit"] = approved_fit
        record["alt_text"] = alt_text.strip()
        record["caption"] = caption.strip()
        if presentation_role is not None:
            record["presentation_role"] = presentation_role
        if editorial_purpose is not None:
            record["editorial_purpose"] = editorial_purpose.strip()
        if editorial_note is not None:
            record["editorial_note"] = editorial_note.strip()
        changed += 1
    validate_registry(updated)
    return updated, changed


def main() -> None:
    approvals = json.loads(APPROVALS_PATH.read_text(encoding="utf-8")) if APPROVALS_PATH.exists() else []
    if not isinstance(approvals, list):
        raise ValueError("illustration approvals must be a JSON list")
    registry = load_registry(REGISTRY_PATH)
    updated, changed = apply_approvals(registry, approvals)
    if not changed:
        print("no generated illustrations awaiting explicit decisions")
        return
    REGISTRY_PATH.write_text(json.dumps(updated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"applied {changed} illustration approval decisions")


if __name__ == "__main__":
    main()
