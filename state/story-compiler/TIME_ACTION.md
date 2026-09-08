# Long-Form Story Compiler — TIME + ACTION

Status: **active derived contract**

Authority: derived-only. Canon prose remains final story authority.

This layer fixes a structural blind spot in long-form generation: strong continuity can still produce weak felt time, and scenes can contain motion without changing the story.

## Core equations

```text
TIME = OFF-CAMERA CAUSALITY + ELAPSED PRESSURE
ACTION = STATE CHANGE UNDER PRESSURE
```

They are closely related.

A punch may change state in half a second.
A bad decision may change it over a week.
Training may change it over months.
Avoidance may cool a relationship while nobody is looking.
A shop may close, a debt may grow, a body may heal, a joke may become routine, an opportunity may disappear.

Long-form fiction should not require the camera to remain on every day for change to feel earned.

## Time is not a timestamp requirement

Do not solve temporal weight by mechanically writing `three days later` everywhere.

Elapsed time may be proven by changed state:

- supervision is no longer needed
- a route becomes automatic
- a customer now knows a worker's name
- a body heals or fails to heal
- a friendship has cooled
- a price changed
- somebody else took the opportunity
- a repeated task becomes boring or skilled
- a joke has history
- equipment is worn, repaired, replaced, or missing
- a routine now includes or excludes someone

Explicit timestamps remain valid when clarity or dramatic pressure requires them.

## Gap modes

Every bounded story/rendering interval may describe one of four temporal modes:

- `continuous_scene` — no meaningful off-camera gap; live pressure carries forward
- `compressed_repetition` — repeated days/tasks are summarized or sampled rather than fully shown
- `off_camera_gap` — story resumes after elapsed time whose consequences matter
- `deliberate_skip` — time is intentionally withheld/skipped so the changed state itself is part of the reveal

No mode is inherently superior. The failure mode is accidental camera-on-every-day continuity.

## What elapsed time may do

Track candidate effects in both directions.

### Growth

Time may legitimately allow larger progression than one visible scene could earn:

- physical conditioning
- practiced technique
- language fluency
- workplace shorthand
- trust built by repeated ordinary behavior
- business/customer accumulation
- route familiarity
- savings
- reputation

Do not require every incremental repetition to appear on-page.

### Decay / cost

Time is not automatically progression.

It may also cause:

- injury stiffness or incomplete recovery
- debt/interest
- missed opportunities
- someone else improving faster
- social drift
- resentment hardening
- a customer leaving
- a business closing
- political/economic conditions changing
- desire changing
- a once-important goal becoming obsolete

A useful long-form question is:

> What did waiting cost?

## Action is broader than combat

Action is any pressure where behavior changes the next available state.

This includes:

- fighting
- sex / consensual intimacy
- pursuit
- rescue
- work under pressure
- gambling
- negotiation
- argument while doing something else
- physical comedy
- magic with consequence
- moving through crowds
- theft
- injury logistics
- choosing not to act when that closes or preserves options
- thought or speech that changes timing, route, risk, access, trust, or the win condition

Thinking is not the opposite of action. Thinking becomes action when the world keeps moving and the thought changes what happens next.

## Residue rule

Action should usually leave state behind.

Possible residue:

- bodily
- material
- financial
- relational
- reputational
- procedural
- geographic
- informational
- emotional
- opportunity cost

A fight that changes nothing may still be valid, but the system should ask whether it is deliberately transient or simply empty spectacle.

## Changed win conditions

Pressure can invalidate the original objective.

Examples:

- catch thief -> survive knife threat and recover what can safely be recovered
- win argument -> prevent relationship rupture
- finish job -> protect worker after accident
- get stronger -> realize the opportunity requiring that strength is already gone

Do not force the protagonist to keep solving the old problem after the story has created a new one.

## Independent causality

Other people and systems continue while the protagonist thinks, waits, trains, heals, sleeps, or avoids.

During both scenes and gaps ask:

- who acted without the protagonist?
- who adapted?
- who stopped waiting?
- what institution changed procedure?
- what market/resource changed?
- what consequence matured off-page?

This prevents long-form generation from making the whole world pause between protagonist-visible events.

## Operational helper

Use:

`scripts/story_time_action.py`

`compile_time_action_contract(interval)` accepts a bounded interval with optional `time` and `action` objects and returns:

- normalized gap mode
- elapsed-time evidence
- growth / decay / missed-opportunity / routine-change candidates
- pressure sources and physical constraints
- state changes and residue
- changed win conditions
- independent vectors
- warnings for `time_gap_without_state_change`
- warnings for `action_without_residue`
- questions and rendering principles for REHEARSAL / STORY SYNC / PROSE

This helper has **no canon authority**. It exists to expose missing causal pressure before prose smooths it over.

## Long-form acceptance questions

Before treating an interval as healthy, ask:

1. If meaningful time passed, what changed because of it?
2. Did the gap permit larger earned progress, larger cost, or both?
3. Did other people/world systems continue independently?
4. What did the active scene actually change?
5. What residue survives the cool beat?
6. Did the win condition change under pressure?
7. Are we showing this day because it matters, or because the generator is afraid to skip time?

## Anti-rules

Do not:

- insert time jumps on a schedule
- make every gap produce improvement
- summarize scenes that need embodied PERFORMANCE
- inflate every action beat into permanent consequence
- confuse explicit dates with felt time
- keep every training/work repetition on camera to prove it happened
- use action quotas that turn slice-of-life into combat sludge
- let off-camera growth bypass established capability constraints

The target is temporal texture and causal residue, not speed for its own sake.
