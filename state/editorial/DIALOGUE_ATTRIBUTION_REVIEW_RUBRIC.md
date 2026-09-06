# Dialogue + Attribution Review Rubric

Exact manuscript prose outranks this file.

This rubric extends the existing whole-manuscript dialogue + attribution pass. It does **not** turn the pass into structural compression or a general prose rewrite. `NO CHANGE REQUIRED` remains a successful verdict.

## Hard dialogue-ownership invariant

A paragraph containing spoken dialogue belongs to that speaker for attribution purposes.

When Character A speaks, an independent physical action, expression, observation, reaction, or movement performed by Character B must not remain attached to Character A's dialogue paragraph when doing so can make the reader momentarily assign the dialogue to the wrong person.

Default repair order:
1. **Paragraph break first.** Move Character B's independent beat into a new paragraph without rewriting prose.
2. If Character B immediately speaks, keep Character B's action and dialogue together in Character B's paragraph.
3. Add or simplify a dialogue tag only when the paragraph break alone does not restore clear ownership.
4. Rewrite wording only when paragraph separation and ordinary attribution cannot resolve the ambiguity.

Examples of violations:
- Greg dialogue followed in the same paragraph by `Antonius smiled.`
- Antonius dialogue followed in the same paragraph by `I picked up the coins.`
- Greg dialogue followed in the same paragraph by `She stared.` when `she` is another character.

This is primarily a **readability/correctness repair**, not an invitation to polish the surrounding prose.

During the whole-manuscript pass, also flag stronger attribution failures exposed by this rule, including:
- a dialogue tag naming a character who is not present in the scene;
- a reaction beat whose pronoun resolves to the wrong character;
- a paragraph whose action ownership makes the speaker genuinely ambiguous;
- a stale character name left behind after a scene or dialogue rewrite.

## Five added checks

### 1. Jurisdiction check
Ask not only `Who said this?` but `Why is this character the person thinking or saying it?`

Prefer dialogue ownership that grows from the current problem:
- object custody;
- professional responsibility;
- evidence authority;
- relationship knowledge;
- transaction state;
- physical position;
- downstream consequence.

Flag a line when another character could say it with no meaningful change because the scene has not established why this speaker owns the thought.

### 2. Repeated-function check
Mundane activity is allowed and often desirable. Repetition becomes a concern when a new scene performs the same **narrative function** as recent scenes without changing competence, relationship, pressure, information, choice, or consequence.

Do not flag a scene merely because another chapter also contains shopping, work, rehearsal, food, travel, repair, or household routine.

Flag only when the underlying experience has stopped changing.

This is a diagnostic in the dialogue pass, not permission to merge/delete/renumber chapters. Structural compression remains separate.

### 3. Protagonist-gravity check
Greg should not automatically inherit another person's:
- problem;
- expertise;
- decision;
- customer promise;
- job;
- investigation;
- rescue obligation;
- explanatory authority.

Greg may have strong first-life knowledge. Let that knowledge matter when the exact situation genuinely enters his domain, but do not make local people incompetent so Greg can become useful.

A strong scene can end with Greg understanding that the problem belongs to somebody else.

### 4. Voice-source check
Do not confuse a voice with its surface cadence.

Examples:
- Hessa is not `short sentences`; she protects the distance between observation and claim and controls permission from evidence.
- Lyssa is not `terse`; she protects her own work, relationships, promises, and practical boundaries.
- Teren is not `Again`; he reduces scene/show consequence to the smallest usable next action.
- Nessa is not `commands`; she reads object function, route, placement, and downstream material consequence.
- Rinna is not `businesslike`; she routes bodies, schedule, money, records, and operating consequence.

Shared vocabulary and clipped work speech are allowed. Distinction should come primarily from cognition and jurisdiction, not verbal gimmicks.

### 5. Dialogue-necessity check
Before adding a tag, explanation, or clarifying exchange, ask whether the reader already knows enough from:
- action;
- object custody;
- procedure;
- current task;
- seating/position;
- transaction sequence;
- established relationship;
- downstream consequence.

Do not make dialogue explain information the scene has already made legible.

Add attribution only at a real ownership reset, interruption, domain change, crowded ambiguity, or referent failure.

## Batch verdict discipline
For every batch, record:
1. actual dialogue/attribution patches, if any;
2. narrator/referent/POV repairs, if any;
3. em-dash repairs, if any;
4. structural concerns observed but explicitly parked;
5. one high-value craft finding if the batch teaches something durable.

For the ownership pass specifically, record chapter status as:
- `CLEAN` — no ownership violation found;
- `PATCHED` — clear ownership violation repaired;
- `REVIEW` — likely violation requires wider scene context before changing prose.

Never manufacture a patch to justify the pass.

## Current macro finding
The later Carrow manuscript increasingly uses **jurisdiction as attribution**. Characters can share cultural terseness and work vocabulary while remaining distinct because they own different consequences.

The next-order risk is therefore less `Can I tell who spoke?` and more:
- Is the right person owning the line?
- Is Greg pulling the scene toward himself unnecessarily?
- Is a mundane chapter changing the underlying experience?
- Is dialogue explaining what action already proved?

The reader-discovered early-manuscript risk is now additionally explicit: **paragraph ownership can lie even when every sentence is grammatical.** A wrong-owner action beat can make a reader backtrack before they consciously know why.

Use those questions without broadening this pass into structural editing.
