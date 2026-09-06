#!/usr/bin/env python3
"""One-shot branch installer for the approved dialogue generation contract."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected exactly one anchor in {path}: {old[:80]!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


replace_once(
    "state/MANUSCRIPT_ENGINE_PLAYBOOK.md",
    "The contract is a steering interface, not canon, not a scene-by-scene outline, and not a checklist the prose must mechanically satisfy. Do not create a separate durable chapter-contract file unless a specific workflow genuinely needs one.\n\nThen write the chapter rather than continuing to plan it.",
    "The contract is a steering interface, not canon, not a scene-by-scene outline, and not a checklist the prose must mechanically satisfy. Do not create a separate durable chapter-contract file unless a specific workflow genuinely needs one.\n\n### Scene beat ownership\n\nBefore drafting a dialogue-bearing scene, privately identify the dramatic owner sequence wherever ownership changes materially. This can be as light as `Antonius -> Greg -> Jorren -> Antonius`. It is disposable steering, not a screenplay, not manuscript markup, and not a new durable scene-outline system.\n\n**One clear dramatic owner per dialogue paragraph is the default.**\n\n- same-owner dialogue, tags, action, and reaction may stay together when natural;\n- another character's action, reaction, or spoken turn normally starts a new paragraph;\n- Greg's first-person interior response after another character speaks normally starts a Greg-owned paragraph;\n- when a paragraph leaves one owner, visits another, and returns to the first, split the owner sequence;\n- distinguish actual characters rather than treating ownership as Greg versus everyone else;\n- do not add dialogue tags merely to satisfy a detector;\n- do not turn ownership clarity into uniform one-sentence-paragraph spam.\n\nApply the existing dialogue-variance model at the owned-beat level: base voice + relationship + current state + scene pressure + small human variance. Build the exchange from character-owned beats, then render natural prose.\n\nThen write the chapter rather than continuing to plan it."
)

replace_once(
    "state/MANUSCRIPT_ENGINE_PLAYBOOK.md",
    "- do not polish away Greg's voice;\n- do not change story outcomes during a light pass.\n\nFor a requested heavy prose pass, sentence and paragraph restructuring may be much stronger, but canon, characterization, scene intent, and outcomes remain protected unless repairing an obvious contradiction.",
    "- do not polish away Greg's voice;\n- do not change story outcomes during a light pass.\n\nFor every dialogue-bearing paragraph, run an ownership sweep before calling the light pass complete:\n\n1. Who owns the quoted speech?\n2. Who owns each action or reaction?\n3. Who owns any first-person interior response?\n4. Does the paragraph leave one owner, visit another, and return?\n5. Would a reader have to mentally reassign the paragraph while reading it?\n\nRepair the smallest useful layer first: paragraph boundary, then surrounding action/reaction scaffolding, then minimal attribution. Preserve working spoken dialogue as the anchor. Rewrite the smallest necessary dialogue fragment only when the line itself remains ambiguous. This is local clarity work, not permission for chapter compression or unrelated polishing.\n\nFor a requested heavy prose pass, sentence and paragraph restructuring may be much stronger, but canon, characterization, scene intent, and outcomes remain protected unless repairing an obvious contradiction."
)

replace_once(
    "state/MANUSCRIPT_ENGINE_PLAYBOOK.md",
    "- manuscript chapter contains zero em dash characters;\n- title/index endpoint agree;",
    "- manuscript chapter contains zero em dash characters;\n- after the chapter is present in its intended permanent source path, `python scripts/dialogue_ownership_check.py --latest --strict` passes with no unresolved ownership errors or review findings;\n- title/index endpoint agree;"
)

replace_once(
    "state/MANUSCRIPT_WORKFLOW.md",
    "6. Privately identify the light chapter contract, including rhythm intervention, fantasy density, artifact pressure, information gap, market-visible value, economic pull, and **action pressure** when relevant, then write ONE complete chapter.\n7. Give it a LIGHT drafting pass: clarity, repetition, attribution, paragraph rhythm, continuity, obvious weak prose, rhythm repetition, fantasy density, artifact-market logic, economic logic, and action rhythm when applicable.\n8. Validate chapter length, title, no-em-dash rule, numerical continuity, protected uncertainty, economic continuity when relevant, and any chapter-specific constraints.\n9. Append the exact accepted prose to the SAME permanent running manuscript.\n10. Update only the living state/index/open-thread files whose answers materially changed.\n11. Put the next executable chapter trailhead in `MANUSCRIPT_STATE.md`.\n12. Commit the complete chapter transaction to `main` when the author has authorized normal forward shipping.\n13. Re-read current `main` and verify the endpoint before reporting success or drafting the next chapter.",
    "6. Privately identify the light chapter contract, including rhythm intervention, fantasy density, artifact pressure, information gap, market-visible value, economic pull, **action pressure** when relevant, and the dramatic owner sequence for dialogue-bearing scenes where ownership changes. Keep the owner sequence disposable and lightweight, then write ONE complete chapter.\n7. Give it a LIGHT drafting pass: clarity, repetition, attribution, **dialogue paragraph ownership**, paragraph rhythm, continuity, obvious weak prose, rhythm repetition, fantasy density, artifact-market logic, economic logic, and action rhythm when applicable.\n8. Validate chapter length, title, no-em-dash rule, numerical continuity, protected uncertainty, economic continuity when relevant, and any chapter-specific constraints.\n9. Append the exact accepted prose to the SAME permanent running manuscript.\n10. Run `python scripts/dialogue_ownership_check.py --latest --strict`. Inspect and repair every ownership error or review finding before commit. Do not guess ambiguous speaker identity merely to make the checker green.\n11. Update only the living state/index/open-thread files whose answers materially changed.\n12. Put the next executable chapter trailhead in `MANUSCRIPT_STATE.md`.\n13. Commit the complete chapter transaction to `main` when the author has authorized normal forward shipping.\n14. Re-read current `main` and verify the endpoint before reporting success or drafting the next chapter."
)

replace_once(
    "state/PROSE_PLAYBOOK.md",
    "Let other people make the best joke, solve the practical problem, know context Greg missed, or continue talking after his contribution is finished. The world should not behave as though it knows Greg is the protagonist.\n\n### Recurring-character voice separation",
    "Let other people make the best joke, solve the practical problem, know context Greg missed, or continue talking after his contribution is finished. The world should not behave as though it knows Greg is the protagonist.\n\n### Dialogue paragraph ownership\n\nTreat **one clear dramatic owner per dialogue paragraph** as the default scene grammar. The rule is ownership, not sentence count. A character may speak for several sentences, move, hesitate, handle an object, and continue in one paragraph when all of those beats belong to that character.\n\nWhen another character acts, reacts, speaks, or becomes the clear interior owner, normally start a new paragraph. Greg's first-person thought after someone else's line is Greg's beat. If a paragraph begins with Antonius, moves through Greg or Jorren, then returns to Antonius, render those changes as separate owned beats instead of asking the reader to reassign the paragraph midstream.\n\nCurrent spoken dialogue is the default anchor. If an exchange is muddy, first split paragraph boundaries or rebuild nearby tags, actions, reactions, and transitions. Add a minimal attribution only when clarity still needs it. Rewrite the smallest necessary spoken fragment only when the dialogue itself remains the problem.\n\nDo not use this rule to manufacture fragment spam. Neutral environmental description and collective crowd motion may remain where rhythm supports them when they do not steal ownership from a dialogue paragraph. In crowded scenes, preserve mess and overlap while keeping specific character interventions legible.\n\nApply recurring-character voice, relationship, mood, and scene pressure inside each owned beat. Ownership gives different voices clean containers; it does not replace the dialogue-variance system.\n\n### Recurring-character voice separation"
)

replace_once(
    "state/STORY_ANTI_PATTERNS.md",
    "### Mechanical AI cadence\nResist repeated fragment stacks, perfect rhetorical reversals, suspiciously balanced dialogue, everyone being equally witty, and identical chapter architecture. Use intentional variation rather than texture-by-formula.\n\n### Research dump / procedure fetish",
    "### Mechanical AI cadence\nResist repeated fragment stacks, perfect rhetorical reversals, suspiciously balanced dialogue, everyone being equally witty, and identical chapter architecture. Use intentional variation rather than texture-by-formula.\n\n### Mixed-owner dialogue paragraphs\nDo not let one speaker's paragraph silently accumulate another character's action, reaction, interior beat, or intervention before returning to the original speaker. Build dialogue-bearing scenes from character-owned beats and normally split when dramatic ownership changes. Same-owner speech and action may stay together. The target is clear ownership, not one-sentence-paragraph formatting.\n\n### Research dump / procedure fetish"
)

print("installed dialogue ownership generation contract authority")
