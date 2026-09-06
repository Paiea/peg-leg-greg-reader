# PEG-LEG GREG — STRUCTURAL COMPRESSION WORKFLOW

Operational workflow for executing structural manuscript compression safely.

This file answers HOW compression work runs. Editorial judgment belongs in `state/COMPRESSION_ENGINE.md`.

## Preconditions

Structural compression may begin only when:
- the author explicitly requests a compression pass;
- the target range has a stable current manuscript authority;
- any active dialogue/voice/prose pass on that same range has completed or established a frozen checkpoint;
- current GitHub authority has been re-read before work begins.

Do not compress from memory, chat summaries, or stale state.

## Recommended batch size

Default working batch: approximately **10-25 chapters**.

Use smaller batches when:
- chapters are unusually long;
- continuity is dense;
- the range contains major relationship transitions;
- many later callbacks originate there;
- structural repetition is uncertain rather than obvious.

Do not run an unattended structural rewrite across hundreds of chapters in one transaction.

## Phase 0: Preflight

Before mapping:

1. Read current authoritative prose for the target batch.
2. Read at least the preceding and following chapter.
3. Read current chapter index/state material relevant to the historical range.
4. Read relevant prose/voice guidance.
5. Identify likely high-risk continuity categories: money, magic, injuries, purchases, jobs, promises, relationship changes, nicknames, recurring jokes, object provenance, location introductions, reputation events.
6. Search later manuscript when a candidate beat appears likely to have downstream residue.

Historical summaries can help locate dependencies but never outrank exact prose.

## Phase 1: Structural map only

**Do not rewrite manuscript prose during Phase 1.**

For every chapter in the target range, produce a map entry with:

- chapter number and title;
- one-sentence primary function;
- unique surviving value;
- redundant function(s), if any;
- known downstream dependencies/callbacks;
- recommendation: KEEP / TIGHTEN / SUMMARIZE-IN-SCENE / MERGE / CUT;
- destination for surviving beats if the chapter is merged/cut;
- confidence level: HIGH / MEDIUM / LOW;
- risk note.

Then produce:
- proposed compressed chapter sequence;
- likely chapter-count change, if any;
- rough word-density gain without treating percentage as a target;
- high-risk merges/cuts;
- author-judgment items;
- explicit list of chapters that should remain quiet/full despite low plot movement.

## Functional comparison across chapters

Do not map chapters independently.

Compare neighboring and nearby chapters for repeated dramatic function.

Useful questions:
- Does this chapter move a relationship or merely restate it?
- Does this work scene create a new role/consequence or simply prove competence again?
- Does this money scene change a decision or merely recompute a known constraint?
- Does this magic scene change the evidence state or replay the protocol?
- Does this threat scene create new pressure or reannounce danger?
- Does this quiet scene provide unique social texture, intimacy, leisure, belonging, atmosphere, or world behavior?
- If removed, would a later callback still feel earned?
- If merged, what exact concrete beat must survive so time still feels lived?

## Dependency searches

Before recommending CUT or a high-impact MERGE, search later manuscript for likely dependencies.

Search by combinations of:
- unusual names;
- object names/marks;
- memorable phrases/jokes;
- promises and quoted language;
- jobs/referrers;
- purchases/prices;
- injuries/body changes;
- magic result terms/counts;
- nicknames;
- location names;
- event-specific language.

Record relevant dependencies in the map.

Do not assume absence of a search hit proves absence of narrative value. Human judgment still applies.

## Approval gate

After Phase 1, STOP.

Present the structural map and proposed sequence to the author.

Do not:
- rewrite chapters;
- delete prose;
- merge exact manuscript files;
- renumber chapters;
- update public reader numbering;
- alter canonical outcomes.

Execution begins only after author approval of the map or explicit modifications to it.

## Phase 2: Execute approved map

Work from the frozen approved map.

For each approved change:

### KEEP
Apply only the requested prose/editor treatment.

### TIGHTEN
Remove redundant internal explanation/setup while preserving all structural beats and outcome.

### SUMMARIZE-IN-SCENE
Choose a surviving neighboring chapter and preserve at least one concrete lived detail from the compressed material. Bridge only what must remain legible.

### MERGE
Build one stronger scene/chapter from approved sources. Preserve:
- unique relationship movement;
- causal facts;
- necessary time progression;
- strongest concrete detail;
- later callback foundations;
- money/magic/body/object continuity.

### CUT
Delete only after all approved surviving facts have been relocated or proven unnecessary.

If execution reveals a dependency or structural surprise not represented in the approved map, stop that local change and revise the map instead of improvising a larger cut.

## Prose pass after structure

Once the structural shape is stable, apply current:
- `state/PROSE_PLAYBOOK.md`;
- `state/DIALOGUE_VARIANCE_ENGINE.md`;
- relevant voice files;
- attribution/voice-compression rules.

Do not polish a scene at full length immediately before deleting it.

## Renumber safety

Renumbering is a separate finalization step, not something done while deciding structure.

Do not renumber until:
- the full batch structure is frozen;
- merged/cut prose is accepted;
- later references/dependencies are accounted for;
- the chapter index can be updated consistently;
- any reader/site/illustration references affected by numbering are identified.

When renumbering is required:
1. create/freeze an old-to-new chapter map;
2. update manuscript files/index/state consistently;
3. update internal chapter references when they truly use chapter numbers;
4. inspect public-reader and illustration metadata references;
5. verify no chapter is duplicated or skipped;
6. verify titles remain attached to correct prose;
7. keep the map durable for audit/history.

Do not casually renumber during ordinary prose editing.

## Cross-boundary continuity QA

After executing a batch, read:
- the final surviving chapter before the edited range;
- the compressed range in sequence;
- the first surviving chapter after the edited range.

Check for:
- time jumps that now feel accidental;
- repeated introductions no longer needed;
- characters remembering scenes that no longer exist in lived form;
- money jumps;
- unexplained object possession;
- magic-count discontinuity;
- injuries appearing/disappearing;
- relationship intimacy jumping without bridge;
- callbacks whose setup was weakened;
- locations treated as familiar before surviving introduction;
- jokes/nicknames appearing before their surviving origin.

## Density QA

Ask after every executed batch:

**PACE:** Is movement easier to feel?

**LIFE:** Did concrete human/social texture survive?

**CAUSALITY:** Are later facts still earned?

**VOICE:** Does it still sound like PLG rather than an efficient summary?

**ORDINARY LIFE:** Did we remove repetition without accidentally treating leisure/intimacy/belonging as filler?

**MUNDANE NOVELTY:** Are the surviving ordinary scenes more distinct now?

**RELATIONSHIPS:** Did accumulated familiarity survive or did people reset?

**BODY:** Does Greg's physical progression still occur at believable speed?

**MONEY:** Do purchases, debts, income, and constraints still produce coherent choices?

**MAGIC:** Are exact evidence/count changes intact?

**OBJECTS:** Are provenance, ownership, repairs, and later use still supported?

**WORLD:** Does the world feel denser rather than thinner?

## Calibration wave

The first real compression wave after the current editor pass should be a known repetitive 10-25 chapter range rather than the entire 150-350 span.

A Bren/extortion-related range is a strong candidate if the final edited authority still shows repeated scene function there.

The calibration pass should answer:
- Is MODERATE strong enough to matter?
- Does the map protect too much?
- Does it cut too aggressively?
- Does the result still feel lived in?
- Are later callbacks preserved?

Adjust the engine only after evaluating an actual compressed sample.

## Completion receipt

A completed compression batch should report:
- original range;
- original and resulting chapter sequence;
- classifications executed;
- chapters/scenes merged or removed;
- important preserved dependencies;
- whether renumbering occurred;
- validation results;
- resulting GitHub commit/branch authority.

Never claim a compression batch is complete until the durable manuscript and indexes/state agree with the accepted structure.
