from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.illustration_state import load_scene_candidates

CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"
OUTPUT_DIR = ROOT / "state" / "visual" / "prompt-packs"


def prompt_pack_filename(candidate: dict) -> str:
    return f"{candidate['id']}.md"


def _continuity_lines(candidate: dict) -> list[str]:
    names = {name.strip().lower() for name in candidate.get("characters", [])}
    lines = ["- Preserve manuscript-established age, body, clothing, props, and setting details."]
    if "greg" in names:
        lines.append("- Greg is nineteen, with a permanent LEFT BKA, knee preserved, right leg intact, and two crutches.")
    if "lyssa" in names:
        lines.append("- Lyssa is a Black woman, tall relative to Greg, thin/lithe, with natural Afro-textured hair.")
    return lines


def render_prompt_pack(candidate: dict) -> str:
    anchor = candidate.get("paragraph_anchor") or "No paragraph anchor recorded yet."
    characters = ", ".join(candidate.get("characters", [])) or "No required named character"
    location = candidate.get("location") or "Use manuscript-supported environment only"
    mood = candidate.get("mood") or "Match manuscript scene tone"
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
        "### SUBJECT + ACTION",
        f"Characters: {characters}. Show them doing the physical action implied by the scene rather than posing for a portrait.",
        "",
        "### CAMERA",
        "Choose a composition that avoids default centered eye-level two-person staging. Rotate wide/medium/close and camera height to suit the scene.",
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
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    wanted = {
        prompt_pack_filename(candidate): render_prompt_pack(candidate)
        for candidate in candidates
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
