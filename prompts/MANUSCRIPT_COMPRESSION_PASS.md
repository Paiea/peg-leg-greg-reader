# PEG-LEG GREG — MANUSCRIPT COMPRESSION PASS PROMPT

Use this after the active dialogue/voice/prose editor has finished or frozen the target range.

## Full prompt

```text
Run the Peg-Leg Greg Manuscript Compression Engine from current GitHub authority on Chapters [START]-[END].

Compression strength: [CONSERVATIVE | MODERATE | AGGRESSIVE]. Default to MODERATE if omitted.

This is a structural compression pass, not a plot rewrite and not a generic prose-shortening pass.

Before doing anything:
1. Re-read current GitHub authority for the target range.
2. Read `state/COMPRESSION_ENGINE.md`.
3. Read `state/STRUCTURAL_COMPRESSION_WORKFLOW.md`.
4. Read current relevant manuscript/index/state authority.
5. Read `state/PROSE_PLAYBOOK.md`, `state/DIALOGUE_VARIANCE_ENGINE.md`, and relevant recurring-character voice files when needed.
6. Confirm the target range is not still being actively rewritten by another editor pass. If it is, stop and report the conflict rather than compressing stale prose.

PHASE 1 IS MAP ONLY.

Do not rewrite manuscript prose, delete chapters, merge exact manuscript files, renumber chapters, or update the public reader during Phase 1.

For every chapter in the target range, produce a structural map entry containing:
- chapter number and title;
- one-sentence primary function;
- unique surviving value;
- redundant function(s), if any;
- downstream dependencies/callbacks;
- recommendation: KEEP, TIGHTEN, SUMMARIZE-IN-SCENE, MERGE, or CUT;
- proposed destination for any surviving beats if merged/cut;
- confidence: HIGH, MEDIUM, or LOW;
- risk note.

Compare chapters against neighboring chapters rather than judging them in isolation.

Optimize for FEWER REPEATED DRAMATIC FUNCTIONS, not fewer chapters and not an arbitrary percentage cut.

Preserve:
- mundane novelty;
- social accumulation and group memory;
- relationship transitions and intimacy;
- money/debt/material continuity;
- disability/body continuity;
- exact magic evidence and count changes;
- purchases, repairs, object provenance, and later use;
- promises, obligations, referrals, permissions, and reputation;
- humor and recurring jokes that later pay;
- first meaningful occurrences;
- location/social introductions that create later shorthand;
- scenes whose power depends on being lived rather than summarized.

Quietness is not a defect.

Hunt aggressively for:
- repeated procedure after the procedure is established;
- repeated magic setup when only one changed variable matters;
- repeated purse/debt arithmetic that changes no decision;
- repeated demonstrations that Greg is careful, analytical, restrained, poor, physically limited, or not an expert after those traits are already earned;
- repeated shopping scenes with the same decision architecture;
- repeated body inventories with no changed state;
- repeated threat warnings with no new consequence;
- repeated work scenes that prove the same competence in the same way;
- repeated emotional conclusions;
- dialogue followed by narration explaining the same implication;
- multi-scene arcs where fewer scenes would create the same causal and emotional result.

ANTI-SUMMARY RULE:
Do not turn PLG into plot synopsis. When compressing repeated time, preserve at least one concrete human detail, recurring habit, physical action, joke, object, work rhythm, or social shorthand that makes the accumulation feel lived.

Before recommending CUT or high-impact MERGE, search later manuscript for likely dependencies using names, objects, prices, injuries, magic terms/counts, jobs, promises, jokes, nicknames, locations, and memorable phrases.

After mapping all chapters, present:
1. the proposed compressed chapter sequence;
2. which chapters remain fully intact and why;
3. likely merges/cuts/summarized material;
4. expected pace/density gain without treating a percentage as a target;
5. high-risk dependency decisions;
6. anything requiring author judgment;
7. a short statement answering: `Will this make the world feel denser or thinner, and why?`

Then STOP.

Do not execute the structural edits until the author approves or modifies the map.

After approval, follow Phase 2 in `state/STRUCTURAL_COMPRESSION_WORKFLOW.md` exactly. If a new dependency appears during execution, stop that local structural change and revise the map rather than improvising a larger cut.
```

## Short invocation

```text
Run PLG compression map for Chapters [START]-[END] at [STRENGTH] strength from current GitHub authority.
```

If `[STRENGTH]` is omitted, use MODERATE.

The short invocation inherits every safeguard in the full prompt.

## First calibration recommendation

After the current editor pass is complete, start with one known repetitive range of roughly 10-25 chapters.

Prefer a range where the author already suspects repeated dramatic function, such as the final edited Bren/extortion sequence if it still shows the same issue.

Do not start by compressing Chapters 150-350 as one transaction.
