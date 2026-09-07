from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import load_scene_candidates

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
BOUNDED_APPROVALS_PATH = ROOT / "state" / "visual" / "BOUNDED_GENERATION_APPROVALS.json"
OUTPUT_DIR = ROOT / "state" / "visual" / "prompt-packs"


def prompt_pack_filename(candidate: dict) -> str:
    return f"{candidate['id']}.md"


def _bounded_candidates(path: Path = BOUNDED_APPROVALS_PATH) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("bounded generation approvals must be a JSON object")
    if data.get("generation_approved") is not True:
        return []
    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("bounded generation approvals require an items list")
    result: list[dict] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("bounded generation approval items must be JSON objects")
        candidate_id = item.get("id")
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("bounded generation approval item requires id")
        if candidate_id in seen:
            raise ValueError(f"duplicate bounded generation approval: {candidate_id}")
        seen.add(candidate_id)
        result.append(dict(item))
    return result


def _continuity_lines(candidate: dict) -> list[str]:
    names = {name.strip().lower() for name in candidate.get("characters", [])}
    lines = ["- Preserve manuscript-established age, body, clothing, props, and setting details."]
    explicit = candidate.get("continuity_notes")
    if isinstance(explicit, str) and explicit.strip():
        lines.append(f"- {explicit.strip()}")
        return lines
    if "greg" in names:
        lines.append("- Greg is nineteen, with a permanent LEFT BKA, knee preserved, right leg intact, and two crutches.")
        lines.append("- Default to above-waist / chest-up / medium framing unless this exact scene materially requires lower-body visibility.")
    if "lyssa" in names:
        lines.append("- Lyssa is a Black woman, tall relative to Greg, thin/lithe, with natural Afro-textured hair.")
    return lines


def _generation_metadata(candidate: dict) -> dict:
    names = {name.strip().lower() for name in candidate.get("characters", [])}
    framing = candidate.get("framing_preference") or ("above_waist" if "greg" in names else "scene_appropriate")
    view_angle = candidate.get("view_angle") or candidate.get("camera_angle") or "choose_non_repetitive_scene_angle"
    pose_family = candidate.get("pose_family") or "physical_scene_action"
    scene_tags = [str(tag).strip() for tag in candidate.get("scene_tags", []) if str(tag).strip()]
    return {
        "framing": framing,
        "view_angle": view_angle,
        "pose_family": pose_family,
        "scene_tags": scene_tags,
    }


def render_prompt_pack(candidate: dict) -> str:
    anchor = candidate.get("paragraph_anchor") or "No paragraph anchor recorded yet."
    characters = ", ".join(candidate.get("characters", [])) or "No required named character"
    location = candidate.get("location") or "Use manuscript-supported environment only"
    mood = candidate.get("mood") or "Match manuscript scene tone"
    metadata = _generation_metadata(candidate)
    tags = ", ".join(metadata["scene_tags"]) if metadata["scene_tags"] else "derive only from manuscript-supported scene context"
    lines = [
        f"# Illustration Prompt Pack — {candidate['id']}",
        "",
        f"**Chapter:** {candidate['chapter']} — {candidate['chapter_title']}",
        f"**Kind:** `{candidate['kind']}`",
        f"**Fit target:** `{candidate['fit_target']}`",
        f"**Spoiler level:** `{candidate['spoiler_level']}`",
        f"**Paragraph anchor:** {anchor}",
        "",
        "## Scene brief",
        "",
        candidate["scene_summary"],
        "",
        "## Visual hook",
        "",
        candidate["visual_hook"],
        "",
        "## Prompt construction",
        "",
        "### GENERATION METADATA",
        f"- Framing: `{metadata['framing']}`",
        f"- View angle: `{metadata['view_angle']}`",
        f"- Pose family: `{metadata['pose_family']}`",
        f"- Scene tags: {tags}",
        "- Preserve these metadata values into the generation queue and registry when the generated asset is intaked. They are continuity/diversity guidance, not permission to contradict the manuscript.",
        "",
        "### SUBJECT + ACTION",
        f"Characters: {characters}. Show them doing the physical action implied by the scene rather than posing for a portrait.",
        "",
        "### CAMERA",
        "Choose a composition that avoids default centered eye-level two-person staging. Rotate wide/medium/close and camera height to suit the scene while honoring the declared framing/view-angle guidance above.",
        "",
        "### FOREGROUND",
        "Use a meaningful prop, doorway, furniture edge, fabric, stage object, cart, hand, crutch, or other manuscript-supported foreground shape when useful.",
        "",
        "### ENVIRONMENTAL MOVEMENT",
        f"Location: {location}. Mood: {mood}. Use posture, clothing, traffic, weather, smoke, fabric, doors, sightlines, or work activity to create directional energy.",
        "",
        "### EYE PATH",
        "Design where the eye enters, how motion carries it, and where it lands. Quiet scenes should still have directional flow unless deliberate stillness is the point.",
        "",
        "### MANUSCRIPT DETAILS",
        f"Stay inside this scene summary and hook. Do not invent plot facts beyond the candidate. Visual hook: {candidate['visual_hook']}",
        "",
        "### CONTINUITY",
    ]
    lines.extend(_continuity_lines(candidate))
    lines.extend(
        [
            "",
            "### STYLE",
            "**SKETCH + INK + PAINT.** Illustrated-novel energy, not glossy concept-art sameness. Mixed fidelity is allowed. Preserve movement and visual flow.",
            "",
            "## Output target",
            "",
            f"- Prompt pack: `state/visual/prompt-packs/{prompt_pack_filename(candidate)}`",
            f"- Suggested asset id: `{candidate['id']}-v1`",
            f"- Suggested live chapter folder: `visual/chapter_art/{candidate['chapter']:03d}/`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    candidates = load_scene_candidates(CANDIDATES_PATH)
    merged = {
        candidate["id"]: dict(candidate)
        for candidate in candidates
        if isinstance(candidate, dict) and isinstance(candidate.get("id"), str)
    }
    for candidate in _bounded_candidates():
        merged[candidate["id"]] = candidate
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    wanted = {
        prompt_pack_filename(candidate): render_prompt_pack(candidate)
        for candidate in merged.values()
        if candidate.get("status") in {"candidate", "prompt_ready"}
    }

    changed = 0
    for filename, text in sorted(wanted.items()):
        path = OUTPUT_DIR / filename
        previous = path.read_text(encoding="utf-8") if path.exists() else None
        if previous != text:
            path.write_text(text, encoding="utf-8")
            changed += 1

    print(f"prompt packs: {len(wanted)} desired, {changed} changed")


if __name__ == "__main__":
    main()
