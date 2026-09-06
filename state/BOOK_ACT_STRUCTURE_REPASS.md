# PEG-LEG GREG — BOOK / ACT STRUCTURE REPASS

Status: WIP structural authority proposal on `editor/book-act-structure-repass`.

Purpose: Re-fit Books and Acts to the manuscript as it actually developed. Chapter numbering, old reader grouping, and existing role-card art are advisory production state only. Structural boundaries follow governing story movement.

## Approved update 1 — retain the Book III / Book IV boundary at 320 / 321

Keep **BOOK III — Chapters 181–320**.

Reason:
- Chapter 320, **THE PORTRAIT**, works retrospectively as an ending image for the phase: Greg is seen externally as the accumulated person he has become, without rank, mythic framing, or old-life iconography.
- Chapter 321 begins the next operating condition and the 321–330 run immediately foregrounds price, choice, risk, ownership, and what Greg can now elect to do with money, tools, and opportunity.
- The boundary is earned by a change in operating condition, not by chapter-count symmetry.

Do not move the Book III ending merely to make Books similar lengths.

## Approved update 2 — close Book IV at Chapter 440

Set **BOOK IV — Chapters 321–440**.

Book IV becomes the movement where Greg's useful life pushes beyond familiar Carrow routines and where paid work, travel, body adaptation, field systems, regional routes, and widening agency become ordinary enough to sustain him outside home.

The old 321–467 Book IV range is retired as a reader-era grouping that outlived the manuscript movement.

## Approved update 3 — split Book IV into three actual Acts

### ACT I — WHAT THINGS COST — Chapters 321–330

Keep the existing title and range.

Function: money, tools, risk, and opportunity become choices Greg can increasingly make for himself.

### ACT II — BEYOND THE DOOR — Chapters 331–388

Start with Chapter 331, **THE MARKER FIELD**.

Function: paid outside-city work becomes repeatable life rather than exception. Greg's usefulness begins traveling through survey, routes, field systems, jobs, people, and increasingly portable competence.

Close at Chapter 388 so the Merecross / expedition transition does not remain buried inside one giant 137-chapter Act.

### ACT III — THE FARTHER ROAD — Chapters 389–440

Start with Chapter 389, **THE TRAVELER**.

Function: Greg stops merely taking jobs beyond Carrow and begins inhabiting a genuinely wider regional life. Merecross, field-crew movement, North Reach, Duskport, Lerrin, body/tool adaptation, curiosity, paid work, and the pull between home and outward movement coexist without canceling one another.

Chapter 400's explicit home/outward pull is representative of this movement: Carrow has become home strongly enough that leaving no longer threatens belonging.

End at Chapter 440, **THE LOOKOUT**, immediately before Greg chooses sea travel as an elective next direction.

## Approved update 4 — open Book V at Chapter 441

Set **BOOK V — Chapters 441–current**.

Chapter 441, **THE SAILOR**, is the Book boundary.

Why it earns Book status rather than only a new Act:
- Greg is offered the known cheaper road and deliberately chooses the boat because he wants the sea.
- Dask continues separately, so the wider movement is no longer simply one shared travel assignment.
- Greg's body, money, routes, and reputation are developed enough that curiosity itself can legitimately steer action.
- The following run expands into islands, regional markets, capital allocation, paid introductions, sourcing, brokerage, logistics, and leverage at a scale larger than Greg's purse.
- By Chapter 474 Greg can coordinate a silver-scale transaction without owning silver-scale inventory. This is a materially new operating condition from early Book IV.

### BOOK V ACT I — THE LONGER REACH — Chapters 441–current

Working Act title: **THE LONGER REACH**.

Governing concern: What happens when Greg's accumulated competence, money, relationships, and freedom of movement let him reach farther than the structures that originally contained his second life?

Do not pre-plan the Act endpoint. Re-audit when another governing question genuinely replaces it.

## Approved update 5 — Book V role-card brief + structural drift guardrail

### Book V role-card target

Preferred role-card chapter: **Chapter 446 — THE INVESTOR**.

Reason:
- It visually and thematically represents the new Book better than selecting the current latest chapter.
- Greg is deciding whether money is only a survival reserve or something he can intentionally deploy into a wider life.
- The sea / ferry / route choice distinguishes Book V visually from Carrow, theatre, and inland survey imagery.

Preferred composition:
- Greg above waist / medium framing by default.
- Notebook or fare board visible as the immediate decision object.
- Ferry / harbor / water context behind or beside him.
- Thoughtful, practical decision rather than heroic pose.
- Do not require lower-body visibility or trial-limb detail unless the exact final composition materially needs it.
- Shared SKETCH + INK + PAINT visual language.
- Preserve established Greg facial continuity using the strongest current accepted references selected by the visual pipeline.

Generation status: **HOLD** while `state/visual/PRODUCTION_HOLD.json` remains active. The brief may be packet-ready, but no new Book V image should be generated or promoted until structural compression / reconciliation clears the hold.

### Structural drift guardrail

Future reader / state tooling should flag structural review rather than silently stretching old groupings when either condition occurs:
- an active Act exceeds roughly 60 chapters without an explicit structural review, or
- an active Book grows roughly 100+ chapters beyond its last structural review while the manuscript's governing question has materially changed.

These are review triggers, not automatic cut rules. Never manufacture a boundary to satisfy a threshold.

## Approved update 6 — do not force a Book V Act break at Chapter 461

Chapter 461, **THE SURVIVOR**, is a meaningful escalation but not yet a governing-question change.

The self-directed expedition, route failure, emergency magic use, and physical danger deepen the same Book V concern rather than replacing it. Greg is still testing what happens when accumulated competence and freedom of movement let him choose farther work and farther risk.

Treat 461 as a review marker / internal inflection, not an Act boundary. Reconsider only if later chapters retrospectively reveal that the expedition or its consequences permanently change the Book's operating condition.

## Approved update 7 — keep Book V Act I open through current authority

Do **not** split **THE LONGER REACH** merely because Chapters 461–474 become more adventurous or more economic.

The later run remains structurally coherent:
- 461 proves self-directed travel now carries real physical consequence;
- 467–468 make curiosity itself a legitimate reason to enter an unknown route;
- 470 explicitly reframes progression around body, magic, money, tools, information, people, credential, reputation, and capital;
- 474 turns that accumulation into silver-scale brokerage leverage without requiring silver-scale ownership.

That is development inside one governing concern, not four separate Acts.

## Approved update 8 — distinguish Book opening chapter from Book role-card chapter

A Book boundary does not require its role-card art to come from the first chapter.

For Book V:
- narrative opening remains Chapter 441, **THE SAILOR**;
- visual identity remains targeted at Chapter 446, **THE INVESTOR**.

This should become a reusable reader rule. Choose Book art for representativeness, not boundary adjacency. Do not replace strong existing Book I–IV role cards merely because structure was repassed.

Current preservation decision:
- Book III keeps `book-iii-magistrate-231.webp` unless a later art-quality review independently finds a materially better card;
- Book IV keeps `book-iv-surveyor-331.webp`; Chapter 331 remains an excellent visual statement of Book IV's portable field-work identity.

## Approved update 9 — active Book / Act ranges must be live, not fake-closed

State should express active structure as **441–current**, not guess a future ending.

Reader generation may render the actual currently published numeric edge for navigation, but it must preserve active/open semantics in source metadata so a static generated range is not mistaken for a closed Book or Act.

Do not hard-code a false structural endpoint merely because the reader currently has fewer chapter files than manuscript authority.

## Approved update 10 — retire the hand-maintained chapter index as endpoint authority

`state/MANUSCRIPT_CHAPTER_INDEX.md` is currently frozen at Chapter 248 while exact manuscript authority is far beyond it. It must not continue masquerading as a current endpoint/index authority.

Integration should either:
1. regenerate the chapter index deterministically from current authoritative chapter/checkpoint metadata, or
2. explicitly mark the file as legacy / non-authoritative and replace its engine-routing role with a generated current index.

Preferred direction: generated index. Chapter titles and structural groupings already exist in machine-readable / checkpoint sources; maintaining another manual 400+ line ledger invites silent drift.

The generated index should validate:
- contiguous chapter numbers;
- title presence;
- current exact endpoint agreement with `MANUSCRIPT_STATE.md`;
- Book / Act membership from structural metadata;
- no chapter assigned to two Books/Acts;
- no closed Book/Act ending beyond existing exact prose.

## Current approved map

- **BOOK I — 1–82**
- **BOOK II — 83–180**
- **BOOK III — 181–320**
  - Act I — 181–219 — THE WORKING COMPANY
  - Act II — 220–280 — THE PRICE OF ATTENTION
  - Act III — 281–320 — THE WIDER LIFE
- **BOOK IV — 321–440**
  - Act I — 321–330 — WHAT THINGS COST
  - Act II — 331–388 — BEYOND THE DOOR
  - Act III — 389–440 — THE FARTHER ROAD
- **BOOK V — 441–current**
  - Act I — 441–current — THE LONGER REACH

## Integration order after structural compression settles

1. Reconcile this map against any chapter merges / cuts / renumbering from the active compression pass.
2. Update project structural state and reader Book/Act metadata from the reconciled map.
3. Replace or regenerate stale chapter-index authority from the reconciled exact chapter set.
4. Extend reader coverage from its current edge through current manuscript authority without inventing a closed Book V endpoint.
5. Run illustration reconciliation against changed Book/Act/chapter placement.
6. Preserve validated Book III / IV role cards; add Book V role-card packet only after structure stabilizes.
7. Clear visual production hold only after anchors and reader structure are stable, then generate/review the Book V role card.

Do not let existing role-card art force a story boundary. Preserve good art when the Book survives; remap or replace when the story structure changes.