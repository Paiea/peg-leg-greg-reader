# Peg-Leg Greg Manuscript Compression Engine Design

## Purpose

Build a durable structural-compression layer for Peg-Leg Greg that can be invoked after the current dialogue/prose editor pass finishes. The system should make long stretches of manuscript more efficient without flattening the book's defining strengths: ordinary life, social accumulation, material continuity, money, body, work, humor, recurring relationships, and lived-in world texture.

The goal is not fewer chapters for their own sake.

The goal is **fewer repeated dramatic functions**.

A quiet chapter may stay. A busy chapter may shrink. Six chapters may remain six if each changes something meaningfully. Six may become three if they repeatedly prove the same thing with different props.

## Core editorial principle

**CUT REPETITION, NOT QUIETNESS.**

The compression engine must preserve the book's accumulated life while removing repeated explanation, repeated procedure, repeated emotional conclusions, repeated evidence demonstrations, repeated threat pressure, and neighboring scenes that perform materially the same movement.

The target is **more life per word**, not a summarized or plot-only version of PLG.

## Why a dedicated subsystem

Existing prose guidance already supports tightening, repetition removal, and selective structural compression. That is not enough for a deliberate 150-350 style pass because a real structural pass may need to:

- merge neighboring chapters;
- delete a redundant scene;
- preserve one scene and bridge over repeated time;
- convert repeated full scenes into a short lived-in montage;
- relocate a surviving beat into a stronger neighboring chapter;
- reduce repeated setup while preserving the changed variable;
- renumber only after a frozen structural map is approved.

Ordinary forward drafting and ordinary prose editing must not gain permission to casually delete or merge canon. Structural compression remains a dedicated mode.

## Scope

Initial intended use is historical manuscript compression, especially ranges where the book spent longer than necessary proving already-established qualities. Likely high-value territory includes roughly Chapters 150-350, but exact ranges must be determined by manuscript evidence rather than the chapter number itself.

This subsystem is not required for every chapter and should not run unattended across hundreds of chapters in one transaction.

## Editorial classification

Every chapter or substantial scene in a compression batch receives one primary recommendation:

### KEEP

The material performs a distinct function that still earns full scene space.

Typical reasons:
- first occurrence of an important relationship state;
- unique social memory or belonging beat;
- distinct world behavior;
- important economic decision;
- first or meaningful change in body/mobility;
- consequential magic evidence;
- meaningful character choice unavailable earlier;
- setup that later pays off;
- unique comedy or intimacy that would be lost in summary;
- new role, workplace, route, object, person, or institution becoming socially legible.

KEEP does not mean prose is untouchable. It may still receive the active prose/editor pass.

### TIGHTEN

The scene earns its existence but contains redundant explanation, repeated setup, repeated body checks, repeated procedure, excessive inference restatement, or cadence bloat.

Preferred action: preserve scene outcome and emotional/social function while reducing internal repetition.

### SUMMARIZE-IN-SCENE

The underlying time/event matters, but full dramatization no longer earns its length.

Preferred action: preserve one concrete lived detail and compress the rest into a brief bridge, montage, remembered line, work rhythm, or transition inside a surviving chapter.

Do not turn this into encyclopedia summary.

### MERGE

Two or more neighboring chapters/scenes perform overlapping dramatic functions and can become one stronger unit without losing distinct residue.

The merged result should preserve the best concrete moments from each source while eliminating duplicated setup, duplicated conclusion, and repeated scene architecture.

### CUT

The material performs no unique surviving function after neighboring material is considered, or its function is already better performed elsewhere.

CUT requires dependency checks before deletion.

## Functional-value test

Before recommending compression, ask what new function the material contributes.

A scene may earn space through any of the following:
- relationship change;
- social memory;
- new joke/history that later persists;
- new information;
- changed evidence state;
- changed money/material state;
- changed body state;
- changed magic state;
- changed role or reputation;
- changed world understanding;
- changed emotional language;
- changed obligation;
- changed choice architecture;
- distinct atmosphere or leisure that deepens belonging;
- distinct ordinary-life texture that has not already been shown;
- setup/payoff dependency;
- an irreversible or memorable event.

If the answer is only "this again demonstrates that Greg is careful / poor / analytical / physically limited / attracted to useful junk / increasingly accepted / under threat," the scene is a compression candidate unless it adds a new consequence or relationship state.

## Repetition targets

The compression engine should aggressively hunt for:

- repeated procedural setup after the procedure is established;
- repeated magic setup where only the changed variable matters;
- repeated ledgers or purse arithmetic that do not alter a decision;
- repeated "Greg does not overclaim" demonstrations after restraint is already visible;
- repeated shopping deliberations with the same outcome and same emotional function;
- repeated body inventories where nothing materially changed;
- repeated threat warnings with no new consequence;
- repeated work scenes that prove the same competence in the same way;
- repeated explanations of relationship states the reader already understands;
- dialogue followed by narration explaining the dialogue;
- multiple chapters ending on the same emotional realization in slightly different words;
- repeated reminders that Greg is not an expert in a field;
- repeated reminders that quiet life matters;
- repeated setup for a payoff that already happened;
- arcs that use five or six scenes where three would produce the same causal and emotional result.

## Protected material

Compression must be conservative around:

- first meaningful scenes between recurring characters;
- relationship transitions;
- later callbacks and running jokes;
- exact magic evidence/count changes;
- money/debt changes that affect later choices;
- purchases, losses, repairs, and object provenance that matter later;
- injuries and recovery that affect later physical behavior;
- disability-specific functional changes;
- location introductions that establish later shorthand;
- promises, obligations, referrals, contracts, debts, favors, and permissions;
- reputation events that later travel;
- theatre history that creates later group memory;
- emotional scenes whose power depends on being lived rather than summarized;
- Greg choices that demonstrate a changed self rather than a repeated trait.

## Anti-summary-sludge rule

Compression must not turn PLG into plot synopsis.

Bad compression:

> Over the next few weeks Greg worked more at the theatre, grew closer to everyone, and improved at backstage tasks.

Preferred compression preserves at least one concrete human detail:

> By the third week, nobody asked who had the prop-room key anymore. They asked Greg, which was how he learned he had apparently become the person with the prop-room key.

The exact wording above is illustrative only. The rule is durable: **keep lived evidence of accumulated time**.

## Scene-survival hierarchy

When several scenes perform the same broad function, prefer preserving the scene that has the most of the following:

1. strongest character interaction;
2. most future residue;
3. most distinctive physical/world texture;
4. funniest or most emotionally specific beat;
5. clearest causal consequence;
6. best setup/payoff connection;
7. most representative ordinary-life detail;
8. strongest prose/voice potential after editing.

Do not automatically preserve the earliest or latest scene.

## Structural-map-first workflow

Compression is a two-phase operation.

### Phase 1: Map only

Read a bounded manuscript range plus enough surrounding context to understand dependencies.

Recommended working batch: approximately 10-25 chapters. Smaller when chapters are unusually long, continuity-dense, or structurally tangled.

Produce a structural map containing, for every chapter:
- chapter number/title;
- one-sentence primary function;
- unique surviving value;
- redundant function(s), if any;
- downstream dependencies/callbacks;
- recommendation: KEEP / TIGHTEN / SUMMARIZE-IN-SCENE / MERGE / CUT;
- proposed destination for any surviving beats if merged/cut;
- confidence / risk note.

Then produce the proposed new chapter sequence for the batch.

**Do not rewrite manuscript prose during the mapping phase.**

### Phase 2: Execute approved map

Only after the map is approved:
- edit/merge/cut according to the frozen map;
- preserve exact canon and dependencies;
- add only minimal bridging prose required for continuity;
- run the active prose/voice/attribution guidance on surviving text;
- validate cross-boundary continuity;
- renumber only if the approved map requires it and the renumber-safety workflow is active.

If execution reveals a structural surprise, stop that local change and revise the map rather than improvising broad new deletions.

## Range boundaries

A batch must read enough before and after the target range to avoid deleting setup or payoff that lives across the boundary.

At minimum inspect:
- the preceding chapter;
- the following chapter;
- current state/index summaries relevant to the range;
- later callback/search hits for names, objects, jokes, promises, injuries, purchases, magic results, and unusual phrases that appear likely to matter.

For high-risk cuts, search later manuscript for the event/object/person before deletion.

## Dependency protection

Before CUT or MERGE, check for:

- later dialogue referring to the event;
- callback jokes;
- relationship memory;
- object ownership/provenance;
- money balance changes;
- magic evidence/counts;
- injury/fatigue state;
- job/referral consequences;
- promises or obligations;
- route/location familiarity;
- later reputation;
- chapter-title/act references;
- illustration references or published-reader links if applicable.

A later dependency does not automatically mean the whole original scene must survive. Preserve the causal fact in the strongest remaining form.

## Compression-strength levels

The prompt may accept one of three levels:

### CONSERVATIVE
Mostly TIGHTEN. Merge/cut only obvious duplicate functions.

### MODERATE
Default. Will merge repeated scene functions and summarize repeated process while protecting lived-in texture.

### AGGRESSIVE
Used only with explicit author request. May substantially reduce scene/chapter count when long stretches repeatedly perform the same movement. Still cannot alter canon outcomes, relationships, or later causal facts without explicit authorization.

Default is MODERATE.

## Success criteria

A successful compressed range should:

- move faster without feeling hurried;
- preserve Greg's voice;
- preserve social accumulation;
- preserve enough ordinary life that later home/adventure contrast still works;
- make unique mundane scenes more visible because repeated ones are gone;
- preserve causal continuity and later callbacks;
- reduce repeated explanation and procedural reenactment;
- make chapter-to-chapter movement easier to feel;
- sound like PLG, not a synopsis of PLG;
- retain moments a reader would actually miss if removed.

A useful test is:

**Does the compressed version make the world feel denser, not thinner?**

## Failure modes

Reject compression that:

- removes quiet scenes merely because they are quiet;
- preserves only plot-critical scenes;
- summarizes intimacy or belonging into abstract statements;
- erases minor recurring people who make places socially legible;
- deletes the first occurrence but keeps weaker callbacks;
- makes Greg's economic or physical progression appear to jump;
- causes later jokes/relationships to feel unearned;
- compresses every work scene into the same montage voice;
- converts uncertainty into certainty;
- changes money, magic, injuries, promises, or outcomes for convenience;
- flattens distinct characters into generic functional dialogue;
- makes the manuscript feel like an outline;
- optimizes solely for word count or chapter count.

## Reusable engine prompt

The following prompt is the intended human-facing trigger after the current editor pass is complete.

```text
Run the Peg-Leg Greg Manuscript Compression Engine from current GitHub authority on Chapters [START]-[END].

This is a structural compression pass, not a plot rewrite.

Use the current authoritative manuscript, PROSE_PLAYBOOK, dialogue/voice guidance, and COMPRESSION_ENGINE rules. Read enough surrounding and later continuity to protect callbacks and dependencies.

First produce a structural map only. For each chapter identify its primary function, unique surviving value, redundant function, downstream dependencies, and recommend KEEP, TIGHTEN, SUMMARIZE-IN-SCENE, MERGE, or CUT.

Default compression strength: MODERATE.

Optimize for fewer repeated dramatic functions, not fewer chapters. Preserve mundane novelty, social accumulation, relationship memory, money/material continuity, disability/body continuity, magic evidence, object provenance, humor, later callbacks, and the lived-in feeling of the world.

Do not turn quiet material into synopsis. Preserve concrete human evidence of accumulated time. Prefer more life per word.

Do not edit prose or renumber chapters until the structural map is complete and approved.

When the map is ready, stop and present the proposed compressed sequence, expected gains, high-risk cuts/merges, and anything that requires author judgment.
```

## Short restart prompt

After this subsystem is implemented, a convenient invocation may be:

`Run PLG compression map for Chapters [START]-[END] at moderate strength from current GitHub authority.`

The engine must expand that shorthand into the full safeguards above.

## Integration plan

After this design is approved and implementation begins, create:

1. `state/COMPRESSION_ENGINE.md`
   - durable editorial logic from this design;
   - classification system;
   - preservation rules;
   - failure modes;
   - strength levels.

2. `state/STRUCTURAL_COMPRESSION_WORKFLOW.md`
   - map-first procedure;
   - batch sizing;
   - dependency search;
   - approval gate;
   - execution and renumber safety;
   - QA requirements.

3. `prompts/MANUSCRIPT_COMPRESSION_PASS.md`
   - reusable full prompt and shorthand invocation;
   - parameter placeholders for range/strength;
   - explicit stop-after-map behavior.

4. Integrate minimal references into:
   - `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
   - `state/PROSE_PLAYBOOK.md`

The integration should point to the dedicated subsystem instead of duplicating the entire ruleset.

## Interaction with current editor pass

Do not run structural compression on ranges currently being actively rewritten by the dialogue/voice-compression editor.

The current editor pass should complete or establish a clear frozen checkpoint first. Structural compression then operates from that edited authority.

This ordering avoids wasting prose-level work on scenes later deleted and avoids structural merging across chapters whose voice/attribution authority is still changing.

## Recommended first real compression wave

Do not begin with Chapters 150-350 all at once.

Choose a 10-25 chapter sample from a known repetitive area, preferably one where the author already remembers functional repetition. Use that batch to calibrate whether MODERATE is preserving enough life.

The Bren/extortion-related sequence is a strong calibration candidate if its exact edited range is identified after the current editor pass, because it has already been flagged as potentially using more full scenes than the dramatic function requires.

After one successful sample, expand batch by batch.

## Final principle

PLG earned its scale through accumulation.

Compression should make that accumulation easier to feel, not erase the evidence that it happened.
