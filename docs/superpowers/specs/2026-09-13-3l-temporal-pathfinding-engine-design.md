# 3L Temporal Pathfinding Engine Design

## Status

Approved design direction for extending **The Third Leg** beyond Record 010 while preserving the prose and narrative form established in Records 001-010.

This document defines development architecture. It does not make Records 011-300 canon, does not overwrite manuscript authority, and does not require the future story to follow any provisional trajectory that fails rehearsal.

## Goal

Create a lightweight temporal pathfinding engine that can explore a provisional horizon of roughly 300 Records across Greg's Second Life, while preserving the freedom for later prose to diverge whenever lived scenes discover a better path.

The engine should help answer two questions at the same time:

1. What future becomes plausible because of what Greg has already lived?
2. What earlier conditions would need to become true for a compelling later future to exist?

The engine is a development tool, not a plot authority.

## Core scope

3L has a bounded long-life architecture that differs from PLG and R2.

- First Life contributes roughly forty-two years of remembered history, including Greg's path to S-class.
- Second Life contributes roughly forty years of primary on-page lived history from age nineteen to roughly fifty-nine.
- The frame present begins with fifty-nine-year-old Greg reaching Ithar during a kingdom-scale Line crisis.

Life Two remains the primary dramatic spine.

Life One is not a second equal manuscript. It functions as remembered pressure, comparison, missing relationships, techniques, warnings, mistaken assumptions, alternate causal history, and occasional dramatized material when the First-Life event itself must be lived rather than summarized.

## Prose lock

Records 001-010 establish the current prose baseline. Do not reopen them merely because the temporal engine changes long-range planning.

### Greg voice is locked

Greg remains practical, compressed, embodied, observant, dry, materially minded, and willing to under-explain what he considers obvious.

He notices work, bodies, money, tools, discomfort, capability, relationships, immediate consequence, and the difference between remembered competence and current reality.

Do not rebuild Greg's voice for later eras.

### Ithar voice is locked

Ithar remains expansive where Greg compresses.

His age appears through scale of attention, history, causality, time, patience, comparison, and material observation rather than archaic vocabulary or generic fantasy grandeur.

Dragon verbosity remains interest-dependent.

Ithar notices and tests. He is not omniscient and must not become an author-mouthpiece.

### Narrative form is locked

**Young Greg owns perception. Old Greg owns selection.**

A remembered scene may contain only what Greg at that age could perceive, believe, infer, want, misunderstand, or physically experience.

Older Greg may select, omit, compress, emphasize, or frame that memory.

The temporal engine may know much more about later consequences than young Greg does. That future knowledge must not leak into young Greg's perception as deterministic foreshadowing or authorial winking.

### Worldbuilding method is locked

Worldbuilding should continue to emerge through lived activity.

Jobs, contracts, maintenance, licensing, wages, property, travel, institutions, meals, tools, law, training, insurance, ranker work, family obligations, bureaucracy, infrastructure, and ordinary dependence should reveal the setting because Greg is doing something inside it.

Avoid encyclopedia-first development in manuscript prose.

### Record length is flexible

The earlier roughly 2,500-word target remains a useful production reference, not a target that every Record must hit.

A Record gets the space necessary to produce one meaningful change in Greg's lived position.

Some Records may cover a narrow scene in several thousand words. Some may compress months or years in substantially less. The quality measure is life per word, not uniform chapter length.

## 300-Record map status

A provisional 300-Record title-and-one-sentence map is useful as search space.

It is not prophecy.

Records 001-010 remain manuscript authority.

Records 011-300 are hypotheses until individually discovered, rehearsed, selected, written, and accepted through normal story authority.

The map may diverge aggressively when nearer prose creates better people, jobs, institutions, relationships, losses, discoveries, geographies, or causal mechanisms.

Do not preserve a future event merely because the map contains a title for it.

Preserve pressures, possibilities, and useful discoveries when an event itself dies.

## Embodied-role rule

Record titles should often identify what Greg is actually being in that part of his life rather than merely naming an external plot event.

Examples include worker, contractor, witness, husband, employer, teacher, debtor, landlord, mourner, hunter, veteran, builder, adviser, organizer, specialist, petitioner, and other socially or materially embodied positions.

Roles are story generators because each role creates contact with different setting machinery.

A role should imply pressures, obligations, people, institutions, resources, limits, and consequences.

Useful causal grammar:

**ROLE creates CONTACT -> SETTING creates PRESSURE -> GREG chooses -> CONSEQUENCE alters POSITION -> new POSITION creates new ROLE or PRESSURE.**

## Elastic time rule

Do not map chapter count mechanically to calendar time.

Time density should vary with lived pressure.

- Ten Records may cover several weeks when a relationship or crisis is changing quickly.
- One Record may compress a year or more when Greg's life is stable but materially accumulating.
- Major turning periods may expand again around love, loss, revenge, rebuilding, disability, institutional change, or Line collapse.

Temporal compression should preserve material state transitions so later chapters know what changed during skipped time.

## Temporal pathfinding architecture

Adapt the strongest parts of the earlier distributed temporal prose experiment, but use them first for cheap trajectory search rather than speculative full prose.

### Shared seed

All temporal windows begin from one compact `seed.md` built from current accepted authority.

The seed contains:

- exact accepted manuscript frontier
- current age and approximate calendar position
- material state
- money, work, body, rank, and skill position
- relationship state
- geography and social range
- unresolved obligations
- protected uncertainties
- important objects and resources
- active pressures
- already-earned possibilities
- known First-Life comparison pressure
- anti-railroad constraints
- current frame-present obligations to Ithar and the Line crisis

The seed should be compact enough that all four windows can actually hold it in working context.

### Four simultaneous windows

A, B, C, and D are independent temporal perspectives.

They do not wait for one another during first-pass generation.

For a 300-Record pathfinding horizon beginning after Record 010, use broad overlapping territories rather than the earlier fourteen-chapter windows.

Initial proposed territories:

- **A: Records 011-090**
- **B: Records 081-170**
- **C: Records 161-250**
- **D: Records 241-300 plus backward obligations into the earlier timeline**

Each overlap is intentional.

A/B overlap at 081-090.

B/C overlap at 161-170.

C/D overlap at 241-250.

These are convergence tests, not duplicates to be averaged.

### Authority gradient

The windows do not have equal confidence.

**A: high speculative confidence**

Closest to Record 010. Should behave most like ordinary forward story development and remain strongly constrained by current canon.

**B: moderate speculative confidence**

May extrapolate institutions, relationships, role accumulation, career position, and consequences, while preserving uncertainty about exact events.

**C: low speculative confidence**

May explore mature-life structures, loss, revenge, rebuilding, disability, institutional leverage, and wider Line implications. It must remain willing to discover that its specific trajectory is wrong.

**D: reconnaissance and backward-obligation window**

D owns the approach to the known ending. It may explore Line collapse, the mature Greg who reaches Ithar, the contradiction around replaceable civilizations and replaceable lives, and the conditions necessary for that ending to feel earned.

D must also push requirements backward without dictating exact earlier events.

Example:

> Late Greg needs a distributed reporting network he trusts.

This may create an earlier obligation such as:

> Some earlier era should plausibly teach Greg why centralized reporting fails.

It must not automatically dictate:

> Greg definitely founds a named reporting guild in Record 143.

### Window output

The first engine pass does not write complete prose.

Each window produces:

- Record number
- provisional embodied-role title
- one sentence describing the primary lived change, pressure, or consequence
- approximate age or time range when useful
- STATE IN summary for the first Record in the window
- STATE OUT summary for the last Record in the window
- a short list of obligations pushed forward
- a short list of obligations pushed backward
- protected uncertainties and viable forks discovered in the window

This creates enough structure for long-range cognition without spending full-chapter generation on trajectories that may die in rehearsal.

## Seam analysis

After A-D produce independent first passes, preserve their outputs unchanged.

Evaluate each overlap for:

- world state
- relationship state
- money and property
- body and disability
- rank and skill
- work and institutional position
- geography and travel range
- reputation
- objects and resources
- independent character action
- Line knowledge and Line condition
- First-Life comparison pressure
- emotional state
- chronology

Classify each seam:

- **CONVERGED**: substantially compatible causal state
- **MINOR DIVERGENCE**: same broad trajectory with repairable details
- **MAJOR DIVERGENCE**: important causal state differs
- **FORK**: multiple futures remain genuinely viable

Do not average a fork.

Determine why the paths diverged and preserve the useful pressure from both when possible.

## Connected rehearsal

After seam analysis, construct the strongest contiguous candidate trajectory from Record 011 toward Record 300.

Rehearse the full path for:

- causal continuity
- chronology
- money and property
- body and disability progression
- skill and rank progression
- work obligations
- reputation
- independent character motion
- relationship development
- world movement
- Line development
- repeated Record grammar
- protagonist gravity
- escalation pressure
- accidental predetermined plotting
- unnatural foreshadowing
- whether ordinary life remains alive rather than becoming connective tissue between planned payoffs
- whether later outcomes have enough earlier material support without becoming mechanically planted

The rehearsal may delete, move, merge, retitle, split, or replace provisional Records.

The map survives only to the extent that the connected life survives.

## Story Sync boundary

Temporal pathfinding cannot directly change canon prose.

Story Sync is the promotion boundary between speculative development and accepted story direction.

Story Sync may promote:

- a pressure
- a relationship direction
- an institution
- a role
- a world mechanism
- a temporal obligation
- a candidate Record title
- a candidate event
- an entire short run

Promotion should be explicit.

Anything not promoted remains experimental evidence.

When Record prose later contradicts promoted development because the prose discovered a better path, manuscript prose wins and the temporal map must be recomputed.

## First-Life handling

First Life should remain underneath Life Two rather than becoming a second parallel 300-Record map.

A temporal window may introduce First-Life material when it materially changes Greg's present choice, grief, expectation, skill use, relationship interpretation, or understanding of what diverged.

The farther the Second Life diverges, the less First-Life memory should function as reliable future prediction.

Memory remains leverage, not perfect causal understanding.

## Ithar frame handling

Do not mechanically end every Record with cave commentary.

Use the frame when Ithar:

- catches meaningful compression
- challenges Greg's interpretation
- notices contradiction or changed emphasis
- materially advances the bargain
- reveals relationship movement between Greg and Ithar
- exposes a causal pattern Greg cannot see
- is surprised, corrected, annoyed, or taught something
- creates pressure that changes how Greg tells the next part

The frame should remain alive and unpredictable rather than becoming a chapter-ending template.

## Experimental repo shape

Keep the engine lightweight and isolated under 3L development material.

Proposed structure:

```text
3l/development/temporal-pathfinding/
  README.md
  PROSE_LOCK.md
  seed.md
  map-300.md
  windows/
    a.md
    b.md
    c.md
    d.md
  seams/
    a-b.md
    b-c.md
    c-d.md
  rehearsal.md
  story-sync.md
  receipt.md
```

No database, service, workflow engine, or permanent agent hierarchy is required for the first run.

Markdown is sufficient.

## Anti-railroad constraints

The engine must not:

- treat the 300-map as canon
- preserve a title because it already exists
- force every available thread to pay off
- make every Record exist to prepare a later Record
- leak later knowledge into young Greg's perception
- escalate stakes merely because chapter numbers increase
- make the world wait for Greg
- turn independent characters into functions of Greg's arc
- erase ordinary life because the ending is known
- convert First Life into deterministic prophecy
- automatically choose one fork because it is easier to outline
- let farther windows quietly overwrite nearer evidence

## Success criteria for the first run

The first temporal pathfinding run is useful if it produces:

1. a coherent but revisable 011-300 candidate trajectory
2. explicit A/B/C/D STATE IN and STATE OUT conditions
3. meaningful seam tests rather than four sequential outlines
4. at least several genuine causal discoveries that were not already obvious from the opening design
5. visible forks where uncertainty is real
6. a stronger near-future runway for writing Record 011 without locking distant prose
7. a list of backward obligations that enrich early setting and relationship development
8. no change to accepted 001-010 manuscript prose unless a separate editorial decision later earns it

## Starting rule

Do not begin by writing Record 011.

First create the shared seed, install the provisional 300-map as experimental evidence, run A-D independently, analyze seams, and rehearse the connected path.

After Story Sync identifies a strong near-future runway, normal manuscript writing may resume from Record 011.
