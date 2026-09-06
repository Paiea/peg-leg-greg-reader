# PEG-LEG GREG — BOOK / ACT STRUCTURE IMPLEMENTATION QUEUE

Status: approved implementation follow-through for `state/BOOK_ACT_STRUCTURE_REPASS.md` on `editor/book-act-structure-repass`.

This file does not create new story structure. It translates the approved editorial map into durable backend rules so reader/state tooling cannot silently drift away again.

## Approved update 11 — one machine-readable structural source

Make one canonical machine-readable Book/Act manifest the source for:
- Book numeral / slug
- start chapter
- closed end chapter or `null` for active/open
- Act numeral / title / deck
- role-card chapter / asset metadata
- optional structural-review marker metadata

Preferred shape: a small JSON state file under `state/`, loaded by `scripts/reader_sections.py` rather than maintaining the `BOOKS` tuple as another hand-edited authority.

`reader_sections.py` should remain the renderer/model layer, not the canonical editorial database.

The approved current values remain:
- Book I 1–82
- Book II 83–180
- Book III 181–320
- Book IV 321–440 with Acts 321–330, 331–388, 389–440
- Book V 441–current with Act I 441–current

## Approved update 12 — preserve open/closed semantics separately from rendered numeric ranges

The current `ReaderBook.end: int | None` and `ReaderAct.end: int | None` behavior is useful and should be preserved.

Do not replace `None` / open structure with a guessed ending. The rendered reader may display `Chapters 441–474` when 474 is the current published frontier, while the structural source still says `end: null`.

Add explicit helpers/metadata where useful so code can distinguish:
- structural end = open
- current manuscript frontier
- current published Illustrated frontier

Those are three different facts and should never be collapsed into one integer.

## Approved update 13 — make reader-frontier verification structure-driven

`scripts/verify_reader_frontier.py` currently hard-codes:
- `BOOK IV`
- `Chapters 321–latest`
- `ACT II · Chapters 331–latest`

That validator is now structurally stale by construction.

Replace those assumptions with checks derived from the structural manifest / `reader_sections` model.

It should verify:
- the current published chapter belongs to exactly one Book and one Act;
- the rendered Book range matches the structural Book plus current published frontier;
- the rendered Act range matches the structural Act plus current published frontier;
- closed Books/Acts render their true closed end;
- active Book/Act ranges render through the published frontier without becoming structurally closed;
- the current Book/Act labels and titles are present in both Illustrated and Text indexes.

## Approved update 14 — stop using the stale handwritten index as reader-generation input

`scripts/update_home_contents.py` currently parses `state/MANUSCRIPT_CHAPTER_INDEX.md` and then overlays `light/manifest.json` because the handwritten index historically lagged.

Retire that fallback once the generated chapter index replacement is in place.

Preferred source chain:
1. exact manuscript-derived/generated chapter manifest owns chapter number + title;
2. structural manifest owns Book/Act membership;
3. reader generation joins them.

Reader generation should fail loudly on missing chapter/title data rather than quietly preserving an old handwritten prefix forever.

This removes a second authority path that can preserve stale structure after the manuscript has moved on.

## Approved update 15 — add structural checks to the normal project check/audit

Extend `scripts/project_check.py` or its successor with a `structure` check.

Required errors:
- overlapping Book ranges;
- overlapping Act ranges;
- gap between closed structural ranges;
- Act outside its parent Book;
- chapter assigned to zero or multiple Books/Acts;
- closed end beyond exact manuscript authority;
- active Book/Act beginning beyond exact authority;
- role-card chapter outside its Book;
- missing role-card asset for a closed Book that declares one.

Required warnings / review triggers:
- active Act exceeds ~60 chapters since last structural review;
- active Book exceeds ~100 chapters since last structural review;
- role-card target exists but asset is intentionally absent because visual production hold is active;
- reader published frontier trails manuscript authority.

The 60/100 thresholds are review alarms only. They must never automatically create a Book or Act boundary.

## Integration note

Do not duplicate this logic into separate Illustrated/Text implementations. `reader_sections.py` is already shared infrastructure and should remain the common rendering path. The fix is to move editorial structure below it into data, then make generation and validation consume the same data.

## Next implementation order

1. add structural manifest;
2. teach `reader_sections.py` to load/validate it;
3. make `verify_reader_frontier.py` structure-driven;
4. remove handwritten chapter-index dependency from home-content generation after generated chapter metadata is authoritative;
5. add `project_check.py structure` and CI/test coverage.

Preserve the active visual production hold. Backend structural work may proceed while new Book V image generation remains blocked.