# Forward REHEARSAL Writing Loop Design

## Status

Approved by the author for Peg-Leg Greg forward production beginning after Chapter 492.

## Goal

Move REHEARSAL from a retrospective prose-editing experiment into a lightweight pre-prose story-discovery layer that improves scene choice and character behavior before a chapter is rendered.

## Core shift

Previous retrospective shape:

`canon prose -> REHEARSAL -> possible prose return`

Forward production shape:

`current story memory -> competing possibilities -> REHEARSAL -> PERFORMANCE when warranted -> surviving discoveries -> prose -> updated story memory`

Canon prose remains story authority. REHEARSAL and PERFORMANCE remain derived working evidence.

## Authority

For every forward chapter:

1. newest exact manuscript prose;
2. explicit current author decisions;
3. `MANUSCRIPT_STATE.md` and other current durable story-control state;
4. converged REHEARSAL memory;
5. current chapter REHEARSAL discoveries;
6. developmental speculation.

A rehearsal discovery cannot overrule canon, silently promote protected uncertainty, or become durable character truth merely because it played well.

## Inputs to forward REHEARSAL

Use the lightest packet that can represent the chapter pressure:

- current exact story edge;
- current executable trailhead;
- only the live story memory relevant to the proposed scene;
- recent 3-6 chapter rhythm/function window;
- active character or relationship memory relevant to the scene;
- scene pressure: who wants what, what is concealed or unknown, what constrains action, and what result would materially change story state;
- hard locks: facts, knowledge ceilings, body state, money, chronology, geography, relationship state, magic evidence ceilings, and ownership boundaries.

Do not load every specialist state file merely because it exists.

## Competing possibilities

Before prose, generate multiple plausible scene solutions at story-beat scale. They are not chapter drafts.

Default exploration:

- one conservative possibility that follows the most obvious live claim;
- one higher-pressure possibility that changes scene grammar, ownership, or consequence without violating canon;
- one lateral possibility that advances a different live pressure or lets another character/system own more of the chapter.

More possibilities are allowed only when uncertainty genuinely warrants them. A simple chapter may need two. A complex chapter may need four or five. Do not create option quotas for their own sake.

For each possibility, ask:

- what new pressure does this create?
- who owns the decisive action or knowledge?
- what would Greg be tempted to overclaim or over-own?
- what observable behavior would distinguish the characters?
- what residue would remain after the scene?
- is this functionally different from recent chapters, or only new nouns?

## REHEARSAL output

REHEARSAL returns discoveries and a recommendation, not prose.

Useful outputs include:

- preferred scene pressure;
- character behavior under conditions;
- relationship behavior;
- ownership boundaries;
- staging or environmental opportunities;
- silence, interruption, object, route, or timing discoveries;
- protected uncertainties that must remain protected;
- rejected alternatives and why they lost;
- whether the source trailhead itself is already stronger than the explored alternatives.

The selected scene can combine compatible discoveries from more than one possibility, but must not become a maximalist collage.

## PERFORMANCE escalation rule

PERFORMANCE is optional and expensive.

Use PERFORMANCE only when high-fidelity embodied behavior is materially uncertain or important, such as:

- a relationship confrontation where timing, silence, interruption, or physical distance carries the scene;
- theatre/performance scenes where actual playable behavior matters;
- action, danger, rescue, pursuit, or physical training where body and environment determine plausibility;
- disability/access scenes where movement geometry changes outcome;
- a scene whose main uncertainty is not what happens but how these particular people physically behave while it happens.

Do not invoke PERFORMANCE merely because named actors are present, because dialogue exists, or because a scene is emotionally important in the abstract.

If ordinary REHEARSAL already resolves the story choice, render prose.

## Prose boundary

The Manuscript Engine renders one complete chapter from the selected scene/discovery packet.

The prose renderer may still discover sentence-level and beat-level solutions while writing. It is not required to literalize every rehearsal beat. The chapter must feel like a novel chapter, not an execution trace.

After drafting, run the normal light pass and validation. If prose reveals a stronger story truth than the rehearsal packet anticipated, canon prose wins and state is updated from the actual chapter.

## Story Sync after prose

After a chapter ships:

- update `MANUSCRIPT_STATE.md` from what actually happened;
- update `OPEN_THREADS.md` only when a live unresolved pressure materially changes;
- update the chapter index compactly;
- record which rehearsal discoveries survived, changed, or were rejected by prose;
- promote durable behavioral memory only when supported by canon, not by rehearsal alone.

The next chapter starts from the new GitHub authority, not from chat memory or the prior rehearsal packet.

## State-spine repair

Before the proving run, repair stale forward routing:

- `MANUSCRIPT_STATE.md` remains the exact current edge and executable trailhead owner;
- `OPEN_THREADS.md` becomes a compact list of genuinely live unresolved pressures, not a historical chapter-by-chapter cache;
- `MANUSCRIPT_CHAPTER_INDEX.md` becomes a routing/title-history aid and must not advertise a stale endpoint. It does not need a full retroactive title transcription when exact checkpoint headers already exist.

## Proving run 493-500

Chapters 493-500 are the bounded proving ground.

Each chapter ships one at a time with normal durability discipline. Do not force every engine into every chapter. Rehearsal heat and PERFORMANCE use vary by actual scene uncertainty.

For each chapter record:

- current pressure;
- possibilities explored;
- selected discovery set;
- PERFORMANCE decision and reason;
- what prose actually kept;
- any surprise introduced by characters or environment;
- whether protagonist gravity increased or decreased;
- whether story memory materially helped selection;
- next trailhead.

## Evaluation at Chapter 500

Evaluate the system, not only chapter prose.

Questions:

1. Did REHEARSAL improve scene choice before drafting?
2. Did it produce character-specific surprises without breaking canon?
3. Did it reduce generic protagonist gravity or merely add procedure?
4. Did PERFORMANCE earn its cost when invoked?
5. Did converged story memory materially improve the next chapter?
6. Did the workflow preserve throughput and one-chapter durability?
7. Were rejected alternatives useful evidence, or mostly noise?
8. Did story state stay cleaner than the old stale-thread system?

If the run is positive, graduate this contract into the permanent Manuscript Workflow. If not, keep the useful parts and simplify the rest.

## Non-goals

- no automatic meta-router;
- no requirement that every chapter use PERFORMANCE;
- no quota for visible prose changes or dramatic escalation;
- no giant trait bible;
- no replacement for the Manuscript Engine;
- no retroactive rewrite campaign;
- no use of rehearsal-only private motives as canon;
- no second story authority beside exact prose.
