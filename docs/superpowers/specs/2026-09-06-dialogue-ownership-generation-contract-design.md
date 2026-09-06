# Dialogue Ownership Generation Contract

Status: DESIGN
Date: 2026-09-06
Scope: Peg-Leg Greg Manuscript Engine forward scene generation and manuscript validation

## Problem

Peg-Leg Greg has accumulated a recurring readability defect in which one dialogue paragraph visually belongs to one speaker but also contains another character's action, reaction, interior response, or later re-entry by the original speaker.

The editorial cleanup can repair historical prose, but cleanup alone does not prevent recurrence. The durable failure is upstream: the Manuscript Engine currently has chapter-level planning, character voice guidance, a light prose pass, and shipping checks, but it does not require scene beats to have explicit dramatic ownership before prose is rendered.

The project therefore needs a generation contract that makes dialogue ownership part of scene construction rather than a later editorial concern.

## Goals

1. Make one clear dramatic owner per dialogue paragraph a forward-generation invariant.
2. Preserve natural paragraph variety. This is not a one-line-per-paragraph rule.
3. Apply character voice, relationship, current state, and scene pressure to character-owned beats before prose is rendered.
4. Catch clear ownership collisions before a new chapter is shipped.
5. Reuse existing Manuscript Engine and project-check architecture rather than creating a parallel story system.
6. Keep the chapter contract lightweight and disposable. Do not create durable beat-outline files for every chapter.
7. Let ambiguous cases receive human or model review instead of allowing a regex to silently rewrite canon.
8. Work with both straight and smart quotation marks and with the repository's mixed manuscript source architecture.

## Non-goals

This design does not:

- require every spoken line to have its own paragraph;
- require dialogue tags on every turn;
- rewrite historical chapters automatically;
- replace the dialogue-variance system;
- create a durable scene database;
- force scenes into rigid screenplay formatting;
- turn the Manuscript Engine into a heavy prose editor;
- use ownership cleanup as permission to change canon, scene outcome, relationship state, or character intent.

Historical cleanup remains a separate editorial job. This contract prevents new debt.

## Chosen architecture

Use a combined model:

**CHAPTER CONTRACT -> OWNED SCENE BEATS -> CHARACTER VOICE/STATE -> PROSE -> OWNERSHIP SWEEP -> STRICT LATEST-CHAPTER CHECK -> SHIP**

This is preferred over either rules-only or validator-only designs.

Rules-only drift because prose generation can still collapse several semantic beats into one paragraph. Validator-only design catches mistakes after they are written but does not improve the scene representation that produced them. The combined model attacks the cause and keeps a guardrail behind it.

## 1. Pre-prose scene ownership

The existing private light chapter contract gains a small scene-ownership layer.

Before drafting a dialogue-bearing scene, the Manuscript Engine should privately identify the sequence of dramatic owners at the level where ownership changes.

Example internal shape:

- Antonius: asks price
- Greg: gives number and privately judges it
- Jorren: laughs
- Antonius: checks plate and asks about collateral

This is a steering representation, not prose and not a durable outline. It may be only a few mental labels. The engine should not output bracketed owner tags into the manuscript.

### Beat ownership rules

A beat may be owned by:

- a named character;
- Greg as POV/interior owner;
- a clearly identified descriptive actor, such as `the clerk`;
- neutral environment/group action when no character ownership is implied.

A change of dramatic owner is normally a paragraph boundary when dialogue is involved.

The engine must distinguish actual characters. It must not reduce ownership to Greg versus everyone else.

### Same-owner material may stay together

Dialogue, action, thought, or reaction belonging to the same character may share a paragraph when the prose reads naturally.

Example:

`"Fine," Antonius said. He counted the silver and pushed it across the desk.`

This remains one Antonius-owned paragraph.

### Different-owner material normally splits

Example:

Bad:

`"You," I said. She stared. I smiled.`

Preferred ownership:

`"You," I said.`

`She stared.`

`I smiled.`

The rule is ownership, not sentence count.

### Leave-and-return paragraphs split

Bad shape:

`"How much?" Antonius asked. I named the number. Jorren laughed. Antonius looked at my plate. "Collateral?"`

The owner sequence is Antonius -> Greg -> Jorren -> Antonius, so the prose should render as distinct owned beats.

### Greg interiority is an owner change

When another character speaks and Greg then internally judges, remembers, notices, decides, or reacts, that interior response normally belongs to Greg's paragraph rather than remaining visually attached to the other speaker.

### Neutral physical detail

Environmental description does not need artificial ownership. A door opening, rain hitting the shutters, or a cart passing may stand alone or remain where rhythm supports it if it does not make the reader reassign a dialogue paragraph to a different character.

### Crowds and multi-speaker scenes

Crowd scenes should remain messy and alive, but explicit interventions still have owners. The contract should not flatten crowd behavior into a sequence of sterile single-line tags. It should simply prevent one character's spoken paragraph from accumulating several other people's specific reactions.

## 2. Voice and state are applied per owned beat

The existing dialogue-variance runtime remains authoritative:

**SPOKEN MOMENT = BASE VOICE + RELATIONSHIP + CURRENT STATE + SCENE PRESSURE + SMALL HUMAN VARIANCE**

The generation contract changes when that runtime is applied.

Instead of drafting a conversational prose blob and differentiating voices afterward, the Manuscript Engine applies each character's voice/state pressures to that character's owned beat before prose rendering.

This improves both ownership and voice separation:

- Greg can retain the shortest dry reduction when it fits.
- Hessa can own precise methodological beats without inheriting Greg's cadence.
- Antonius can own value/obligation framing.
- Lyssa can refuse Greg's analytical frame rather than simply winning his kind of exchange.
- Marek, Nessa, Rinna, Teren, and other recurring characters can carry their own processing rhythm.

Ownership is not a new voice system. It is the container that lets the existing voice system operate cleanly.

## 3. Drafting contract in durable authority

The reusable rule should graduate into the files every fresh Manuscript Engine worker already reads.

### `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`

Add a compact `Scene beat ownership` subsection to the private chapter contract and drafting behavior:

- identify the owner sequence before dialogue-heavy scenes;
- one owner per dialogue paragraph by default;
- same-owner dialogue/action may stay together;
- different-owner reaction/action/interiority normally starts a new paragraph;
- leave-and-return owner sequences must split;
- do not add tags merely to satisfy a detector;
- do not turn the rule into one-sentence-paragraph spam.

Add an ownership sweep to the light prose pass.

Add a strict latest-chapter ownership check to verification before shipping.

### `state/MANUSCRIPT_WORKFLOW.md`

Add ownership to the normal chapter transaction:

- chapter contract includes owner sequence for dialogue-bearing scenes when useful;
- light drafting pass includes dialogue ownership;
- verification runs the strict latest-chapter ownership validator before commit.

### `state/PROSE_PLAYBOOK.md`

Graduate the craft rule into the Dialogue / Interiority section. This is the detailed human-readable authority for what one dramatic owner means and how it interacts with rhythm, tags, interiority, crowds, and voice variance.

### `state/STORY_ANTI_PATTERNS.md`

Add a compact anti-pattern for `mixed-owner dialogue paragraphs` so Story Control, Manuscript, and editorial workers recognize the failure mode without reading historical cleanup state.

The existing dialogue-variance WIP remains evidence and editorial history. It should not remain the only place where the forward generation rule lives.

## 4. Post-draft ownership sweep

Before the ordinary light prose pass is considered complete, the Manuscript Engine performs a focused read of each dialogue-bearing paragraph.

For each paragraph ask:

1. Who owns the quoted speech?
2. Who owns each action or reaction?
3. Who owns any first-person interior response?
4. Does the paragraph leave one owner, visit another, and return?
5. Would a reader need to mentally reassign the paragraph midstream?

Repair order:

1. split paragraph boundaries;
2. move or rebuild the surrounding action/reaction scaffolding;
3. restore a minimal attribution if speaker clarity still needs it;
4. rewrite only the smallest necessary dialogue fragment if the spoken line itself is the source of ambiguity.

Current dialogue remains the default anchor. Paragraph boundaries have no preservation authority.

This sweep is local. It must not become chapter compression or broad prose rewriting during normal forward production.

## 5. Machine validation

Add a focused ownership checker and integrate it with existing project validation.

### New helper: `scripts/dialogue_ownership_check.py`

Responsibilities:

- load canonical chapter prose through the repository's existing source-resolution/generation helpers rather than inventing a new authority map;
- accept `--chapter N`, `--latest`, and optional audit-range modes;
- understand straight and smart double quotes;
- inspect only dialogue-bearing paragraphs;
- identify high-confidence explicit owner collisions;
- identify ambiguous paragraphs that require review;
- never auto-rewrite manuscript prose;
- print machine-readable findings with chapter number and paragraph excerpt;
- return a nonzero exit code in strict mode when unresolved findings remain.

### High-confidence error classes

Examples that should fail strict validation:

- explicit speaker plus a different named/descriptive actor action in the same paragraph;
- another named speaker or actor between two beats belonging to the original speaker;
- another character's dialogue and Greg's explicit first-person reaction/interiority sharing one paragraph when the owner change is clear;
- two or more explicit owners inside a dialogue paragraph where paragraph splitting is mechanically obvious.

### Review classes

Examples that should be reported carefully rather than guessed:

- ambiguous pronouns;
- malformed or cross-paragraph quotation structure;
- dialogue embedded inside letters, quoted documents, lyrics, or formatted blocks;
- unusual verbs the detector cannot confidently classify;
- crowd descriptions where ownership is intentionally collective.

The forward Manuscript Engine should treat review findings as work to inspect before shipping. The validator itself should not invent speaker identity.

### `scripts/project_check.py`

Extend the `manuscript` result with dialogue-ownership information, while preserving its current role as the single machine-readable project check surface.

Recommended payload additions:

- latest canonical chapter checked;
- ownership error count;
- ownership review count;
- compact findings list.

The existing duplicate chapter, em-dash, and stale-name checks remain unchanged.

## 6. Shipping gate

The normal chapter transaction gains this command before the chapter is called complete:

`python scripts/dialogue_ownership_check.py --latest --strict`

The Manuscript Engine must fix or consciously review every finding before it commits the chapter transaction.

### GitHub Actions backstop

Reuse `.github/workflows/light-edition.yml`, which already triggers on the active running manuscript, recovered manuscript, and exact checkpoint paths.

Add an early step before reader regeneration:

`python scripts/dialogue_ownership_check.py --latest --strict`

This is intentionally a backstop, not the primary editing loop. It turns a newly introduced ownership regression into a visible red workflow immediately instead of allowing the reader refresh to make the problem look accepted.

No second manuscript-quality workflow is needed unless future checks become large enough to justify one.

## 7. Tests

Use test-driven development.

Create `tests/test_dialogue_ownership_check.py` with synthetic and manuscript-derived regressions.

Required regression shapes include:

1. same-owner dialogue plus action stays valid;
2. Greg speaks, another character reacts, Greg acts;
3. Antonius speaks, Greg reacts, Jorren reacts, Antonius speaks again;
4. two named non-Greg characters in one dialogue paragraph;
5. descriptive actor such as `the man with the scar`;
6. smart quotes;
7. Greg interiority after another speaker;
8. ambiguous same-gender pronoun is review, not guessed identity;
9. malformed or cross-paragraph quotes are review/protected;
10. quoted letters or formatted blocks do not create destructive false rewrites;
11. ordinary multi-character narration with no dialogue is ignored;
12. already well-separated rapid dialogue remains valid.

Historical examples found during the current cleanup should be converted into regressions when they reveal a general failure class, not hard-coded chapter exceptions.

## 8. Error handling and false-positive policy

The checker must prefer `review` over a false accusation when identity is unclear.

The prose rules remain stricter than the detector. A green detector means no known machine-detectable collision, not that the prose is automatically good.

The Manuscript Engine still performs the ownership sweep because semantic clarity cannot be delegated completely to regex or static analysis.

Do not create a broad permanent exception list during the first implementation. If a real repeated intentional form cannot be represented without false positives, add a narrowly documented exemption only after an actual example proves it is needed.

## 9. Interaction with historical cleanup

Another worker may continue the historical whole-novel ownership pass in parallel.

This generation contract must not depend on that branch merging first.

Implementation should start from current `main`, preserve newer authority, and avoid modifying historical chapter prose. It changes forward rules, validators, tests, and workflow only.

Once historical cleanup is accepted, the same validator can be run manuscript-wide as an audit. Future chapters use the strict latest-chapter gate immediately.

## 10. Success criteria

The design is successful when:

1. a fresh Manuscript Engine worker reconstructs the one-owner rule from normal boot files without reading old chat or editorial WIP;
2. the private scene contract establishes owner changes before dialogue prose is rendered;
3. the light prose pass explicitly audits ownership;
4. high-confidence mixed-owner examples fail automated tests;
5. smart-quote examples are recognized;
6. ambiguous pronouns are surfaced rather than guessed;
7. `project_check.py manuscript` reports ownership findings;
8. `light-edition.yml` runs the strict latest-chapter ownership backstop before regenerating the reader;
9. normal prose with clear same-owner action is not forced into fragment spam;
10. no historical prose is rewritten as a side effect of installing the generation contract.

## Recommended implementation order

1. Add failing ownership-check tests using known failure classes.
2. Implement the focused checker until tests pass.
3. Integrate findings into `project_check.py manuscript`.
4. Add the strict latest-chapter check to the Light edition workflow.
5. Update Manuscript Engine, workflow, prose, and anti-pattern authorities.
6. Run the full repository test suite and focused project checks.
7. Verify the branch is based on current `main` before merge.

## Design decision

Adopt the combined model.

Do not make future PLG dialogue ownership an editorial cleanup concern. Treat it as part of the Manuscript Engine's scene grammar, with a lightweight pre-prose owner sequence and a strict post-draft latest-chapter validator.