from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES_PATH = ROOT / "state" / "visual" / "SCENE_CANDIDATES.json"

ANCHOR_REPAIRS = {
    "ch158-letter-lyssa": "The paper seller sanded the letter, folded it, tied it, and wrote CARROW on the outside.",
    "ch159-fish-rescue": "We found the fish wedged behind a support where someone had pushed it with a boot.",
}

WAVE = [
    {
        "id": "ch166-firelight-cloth",
        "chapter": 166,
        "chapter_title": "THE ROADHAND",
        "scene_summary": "At the road camp after Kest, Nessa repairs the goat-chewed mounting cloth by firelight while Pell holds the damaged corner and the rest of the company settles into an ordinary no-performance night.",
        "visual_hook": "Nessa working the damaged mounting cloth in warm firelight with Pell holding the corner, road camp and sleeping wagons behind them, while Greg watches from the edge of the work circle.",
        "characters": ["Greg", "Nessa", "Pell"],
        "location": "roadside camp beside the company wagons",
        "mood": "quiet work, dry comedy, road-worn warmth",
        "priority": "high",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "paragraph_anchor": "After dark, Nessa worked on the chewed mounting cloth by firelight until she decided firelight was making the color worse and stopped.",
        "framing_preference": "above_waist",
        "view_angle": "three_quarter",
        "pose_family": "repair_work",
        "scene_tags": ["road_camp", "costume", "repair", "work", "firelight", "travel"],
        "notes": "Keep Greg peripheral/above waist. The image is about accumulated company work and the damaged cloth, not lower-body state.",
    },
    {
        "id": "ch167-dast-arrival-traffic",
        "chapter": 167,
        "chapter_title": "THE APPLICANT",
        "scene_summary": "Before the company can even see Dast properly, the harvest fair announces itself as a traffic problem: fields divided by rope and stakes, temporary signs, packed wagons, and workers redirecting everyone through multiple contradictory easts.",
        "visual_hook": "Greg and the company wagon entering a chaotic fair-routing landscape of rope lanes, painted signs, carts, workers with sticks, livestock, and improvised directions before Dast itself is visible.",
        "characters": ["Greg", "Marek", "Davin"],
        "location": "approach fields outside Dast harvest fair",
        "mood": "busy, comic, overwhelming but practical",
        "priority": "high",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "paragraph_anchor": "Fields on both sides of the road had been divided with rope, stakes, painted boards, and people holding sticks.",
        "framing_preference": "above_waist",
        "camera_angle": "wide_environmental",
        "pose_family": "arrival_observation",
        "scene_tags": ["fair", "traffic", "wagon", "crowd", "arrival", "travel"],
        "notes": "Use Greg as a recognizable foreground anchor while the fair logistics carry the composition.",
    },
    {
        "id": "ch168-cart-through-performance",
        "chapter": 168,
        "chapter_title": "THE PITCHMAN",
        "scene_summary": "During the north-arcade performance, a loading cart forces the actors and audience to break formation and make a lane through the show before the scene resumes as if this is normal.",
        "visual_hook": "A fair cart cutting directly through the improvised performance lane while Marek, Serra, Greg-as-Sword, and the audience peel aside around cheese stalls, columns, wind, and loading traffic.",
        "characters": ["Greg", "Marek", "Serra"],
        "location": "north arcade at Dast fair",
        "mood": "kinetic, comic, improvisational",
        "priority": "high",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "paragraph_anchor": "For several seconds the performance became a crowd making a lane.",
        "framing_preference": "above_waist",
        "view_angle": "side_three_quarter",
        "pose_family": "performance_interruption",
        "scene_tags": ["fair", "performance", "cart", "crowd", "arcade", "comedy", "theatre"],
        "notes": "Frame Greg above waist on/near the Sword board; the cart and crowd geometry sell the scene.",
    },
    {
        "id": "ch169-standby-platform",
        "chapter": 169,
        "chapter_title": "THE STANDBY",
        "scene_summary": "Bellan suddenly gives the company a tiny opening between grain speeches, so Marek walks onto the west platform while the previous speaker is still leaving and the next speaker waits beside the stairs.",
        "visual_hook": "A compressed fair-stage handoff: Marek stepping onto the west platform, Serra and Iven ready behind him, an annoyed grain speaker waiting at the stairs, and Greg off to the side with the collection bowl.",
        "characters": ["Greg", "Marek", "Serra", "Iven"],
        "location": "west platform at Dast fair",
        "mood": "compressed, opportunistic, funny, professional",
        "priority": "high",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "paragraph_anchor": "Marek walked onto the west platform while the fourth speaker was still leaving it.",
        "framing_preference": "above_waist",
        "view_angle": "over_shoulder",
        "pose_family": "stage_handoff",
        "scene_tags": ["fair", "platform", "performance", "standby", "crowd", "theatre"],
        "notes": "Greg can remain above waist at the collection edge; prioritize the stage handoff and cramped schedule joke.",
    },
    {
        "id": "ch170-goat-rope-queue",
        "chapter": 170,
        "chapter_title": "THE CHASER",
        "scene_summary": "While the company waits in a bridge-repair queue, a goat tied behind the next cart repeatedly follows Pell's attempts to move the rear wagon rope out of reach.",
        "visual_hook": "Pell shifting the company wagon rope while a stubborn goat stretches after it again, with Greg watching, wagons queued toward the intact bridge, and repair workers carrying long rail timbers ahead.",
        "characters": ["Greg", "Pell"],
        "location": "wagon queue at a stone bridge under rail repair",
        "mood": "ordinary-road comedy, patient, lived-in",
        "priority": "high",
        "kind": "chapter_illustration",
        "fit_target": "exact",
        "spoiler_level": "low",
        "status": "prompt_ready",
        "paragraph_anchor": "Then a cart with two goats tied behind it joined after us and became our problem because one goat kept trying to eat the rear wagon rope.",
        "framing_preference": "above_waist",
        "view_angle": "three_quarter",
        "pose_family": "roadside_problem_solving",
        "scene_tags": ["bridge", "queue", "wagon", "goat", "road", "work", "comedy", "travel"],
        "notes": "Keep Greg above waist; Pell, the rope, goat, wagons, and bridge-repair activity carry the physical action.",
    },
]


def apply_seed_wave(candidates: list[dict]) -> tuple[list[dict], int]:
    updated = deepcopy(candidates)
    changed = 0
    by_id = {record.get("id"): record for record in updated}

    for candidate_id, anchor in ANCHOR_REPAIRS.items():
        record = by_id.get(candidate_id)
        if record and record.get("paragraph_anchor") != anchor:
            record["paragraph_anchor"] = anchor
            record.pop("anchor_status", None)
            record.pop("anchor_match_count", None)
            record.pop("anchor_quality_status", None)
            record.pop("anchor_quality_score", None)
            record.pop("anchor_blocked", None)
            record["status"] = "prompt_ready"
            changed += 1

    for seeded in WAVE:
        existing = by_id.get(seeded["id"])
        if existing is None:
            updated.append(deepcopy(seeded))
            by_id[seeded["id"]] = updated[-1]
            changed += 1
        else:
            preserved = {key: existing[key] for key in ("anchor_status", "anchor_match_count", "anchor_quality_status", "anchor_quality_score") if key in existing}
            if any(existing.get(key) != value for key, value in seeded.items()):
                existing.clear()
                existing.update(deepcopy(seeded))
                existing.update(preserved)
                changed += 1

    updated.sort(key=lambda record: (record.get("chapter", 999999), record.get("id", "")))
    return updated, changed


def main() -> None:
    candidates = json.loads(CANDIDATES_PATH.read_text(encoding="utf-8")) if CANDIDATES_PATH.exists() else []
    updated, changed = apply_seed_wave(candidates)
    text = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
    if CANDIDATES_PATH.exists() and CANDIDATES_PATH.read_text(encoding="utf-8") == text:
        print("older coverage wave already current")
        return
    CANDIDATES_PATH.write_text(text, encoding="utf-8")
    print(f"seeded/repaired older coverage wave: {changed} candidate records changed")


if __name__ == "__main__":
    main()
