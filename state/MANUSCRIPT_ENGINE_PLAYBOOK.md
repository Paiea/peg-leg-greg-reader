# PEG-LEG GREG — MANUSCRIPT ENGINE PLAYBOOK

This file answers: **How should a fresh Manuscript Engine think and work?**

It does not replace `MANUSCRIPT_STATE.md`, `MANUSCRIPT_WORKFLOW.md`, `OPEN_THREADS.md`, the chapter index, or manuscript prose.

## Core purpose

Protect throughput without sacrificing continuity.

The normal unit of work is **one actual chapter**, not an endless planning session. Read enough durable state to orient, write the chapter, run a focused prose/continuity pass, verify, commit, update compact state, and leave the next worker a trailhead.

## Startup

Before canon-dependent work:

1. read `state/PROJECT_STATE.md`
2. read this playbook
3. read `state/PROSE_PLAYBOOK.md`
4. read `state/MANUSCRIPT_WORKFLOW.md`
5. read `state/MANUSCRIPT_STATE.md`
6. read `state/OPEN_THREADS.md`
7. check `state/MANUSCRIPT_CHAPTER_INDEX.md` when chronology/title history matters
8. read the current manuscript edge
9. consult character/setting/plot bibles only when the chapter needs them

Do not reread the entire project brain every chapter.

## Authority

Manuscript prose outranks summaries. Newer GitHub-authoritative prose outranks stale incoming copies. State files are navigation aids, not permission to contradict exact prose.

If the prompt and repository disagree about current story position, trust the newer repository authority.

## Drafting behavior

- Write one chapter rather than replacing writing with outlining.
- Greg POV.
- Greg is intelligent, observant, practical, and increasingly competent, but not a generic mastermind or action hero.
- Competence should grow through work, repetition, observation, mistakes, correction, and practical problem solving.
- Preserve fallibility. Let Greg misread, miss, hesitate, perform unevenly, or need correction.
- Let other characters own strong moments.
- Do not make every chapter prove Greg is special.
- Let ordinary work, money, bodies, schedules, roads, meals, errands, relationships, and fatigue remain story-bearing material.

## Engine rotation

Do not force every active engine into every chapter.

Major engines include theatre, Lyssa/domestic life, Hessa/magic evidence, work/money/debt, Carrow/world life, external pressure/threat, relationships, and longer mysteries.

Let one or two engines lead while others breathe. A live thread can remain live without appearing on-page every chapter.

## Theatre

Theatre must remain actual theatre:

FUN -> PEOPLE -> WORKPLACE -> ACTING -> STAGECRAFT -> FAILURE -> RECOVERY -> ANOTHER TURN

Greg should rehearse, perform, work, solve mundane problems, screw up, listen, recover, and become more comfortable over time.

Long-range utility is allowed to emerge retrospectively. Do not write theatre as an obvious training montage for a future bluff.

## Evidence discipline

Do not overinterpret evidence merely because the reader or writer suspects a connection.

Separate:
- observed fact
- description match
- inference
- possibility
- established identity/causation

Characters such as Hessa, Rinna, and Lyssa can enforce different forms of evidentiary discipline. Preserve uncertainty when uncertainty is what the manuscript has earned.

## Hessa / magic scenes

Hessa handles mana safety, evidence, supervision, repeatability, apparatus discipline, and narrow claims. She is not Greg's theatrical illusion teacher.

A successful observation does not automatically become a stable capability. Track counts and conditions exactly. Failures and no-responses are useful evidence. Body/fatigue can be part of the apparatus.

Do not widen tests casually into stronger objects, independent practice, generalized telekinesis, range claims, or theatrical applications.

## Threat escalation

Threat should collide with ordinary life rather than replace it.

Prefer pressure that changes costs, information, schedules, suppliers, reputation, choices, or relationships before defaulting to spectacle or violence.

Escalation should produce new information or changed behavior, not merely make the antagonist louder.

Do not promote suspected networks, bosses, identities, territories, or conspiracies into fact without evidence.

## Lyssa

Lyssa has independent work, errands, moods, obligations, competence, and desires. She is not present solely to listen to Greg explain the plot.

Her relationship with Greg should accumulate through ordinary interactions as well as major emotional beats. Preserve her ability to disagree, correct, notice different things, be unavailable, or have her own day.

## Long-range direction

Directional, not scheduled canon:

THEATRE -> PERFORMANCE -> MISDIRECTION -> ILLUSION -> MASKS -> CONTROL OF PERCEPTION -> EVENTUAL DANGEROUS BLUFF

The eventual payoff should ideally converge old-life knowledge, second-life evidence/world understanding, and theatre timing/stagecraft. Do not write toward this as a visible checklist.

## Post-draft pass

After the chapter exists, improve it. Do not let editing become a second unrelated rewrite.

Check:
- prose rhythm and paragraph shape
- Greg POV/voice
- dialogue/action balance
- redundant explanation
- over-cleverness
- evidence inflation
- character flattening
- scene transitions
- physical continuity
- money/magic/count continuity
- NO EM DASHES
- target length

Use `state/PROSE_PLAYBOOK.md` for the craft pass.

## State update

After the chapter is final:

- update the permanent manuscript
- update `MANUSCRIPT_STATE.md`
- update index/open threads only when useful
- update specialized bibles only when durable knowledge genuinely changed
- do not create paperwork for unchanged domains

State should describe what actually happened, not what the previous prompt hoped would happen.

## Re-prompt / handshake

End each substantial manuscript run with a full next-edge re-prompt generated from the new repository state.

The re-prompt is a **handshake**, not the savestate. GitHub is the savestate.

A fresh worker should be able to receive a tiny instruction such as:

> Work as the Peg-Leg Greg Manuscript Engine. Read the repository startup sequence and continue from current authority.

The repository should do most of the teaching.

## Failure recovery

If context is lost, a chat dies, or a different worker takes over:

1. ignore assumptions from the dead session
2. inspect current `main`
3. run the startup sequence
4. inspect any relevant WIP branch if explicitly named
5. continue from GitHub authority

Disposable workers are acceptable. Durable state is the continuity mechanism.