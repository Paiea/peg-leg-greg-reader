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

## Approved update 16 — keep the structural manifest deliberately skinny

Do not turn the new manifest into a second manuscript index or visual registry.

It should own only facts that are genuinely structural:
- stable Book / Act IDs, numerals, slugs, titles, decks;
- start chapter;
- closed end or `null` when open;
- optional representative role-card chapter / visual identity key;
- structural-review marker metadata.

It should **not** duplicate:
- chapter titles;
- manuscript endpoint;
- chapter prose/checkpoint paths;
- illustration approval state;
- character-reference metadata;
- generated reader frontier.

Those values must be joined from their existing owners at runtime/build time. If another source already owns a fact better, structure references it rather than copying it.

## Approved update 17 — derive chapter catalog from exact manuscript generation, not from structure

The generated chapter catalog should come from the same exact-source loading path used to build the Text reader (`generate_light.load_all_sources()` or a shared extraction beneath it), then emit a deterministic chapter-number/title catalog.

The structural manifest consumes chapter numbers; it never supplies chapter titles.

Required behavior:
- one exact-source discovery path for manuscript-derived chapter number/title data;
- generated catalog is deterministic and overwriteable;
- a missing/duplicate exact chapter is an error before reader structure is rendered;
- `MANUSCRIPT_CHAPTER_INDEX.md` can remain historical/reference material, but must be labeled non-authoritative once replacement is live.

This prevents the new structural system from accidentally inheriting the old manual-index maintenance burden.

## Approved update 18 — role-card structure stores intent, visual pipeline stores asset truth

Structural data should record the representative chapter / semantic role-card target for a Book, but it should not become the authoritative image registry.

Preferred split:
- structure owns `role_card_chapter` and optionally a stable visual-intent/key;
- visual state / accepted asset registry owns actual file path, approval status, reference provenance, and generation metadata;
- reader assembly resolves the accepted asset for that structural key/chapter;
- if no accepted asset exists, reader may render the Book without a plate rather than inventing or silently reusing a wrong one.

For the current map:
- Book III intent remains Chapter 231 / THE MAGISTRATE;
- Book IV intent remains Chapter 331 / THE SURVEYOR;
- Book V intent remains Chapter 446 / THE INVESTOR, with asset unresolved while production hold is active.

This keeps structural editing from mutating visual-production authority and vice versa.

## Approved update 19 — structural review markers are chapter-based, not calendar-based

The drift guardrail should be measured against manuscript growth, not elapsed real-world time.

Each open Book / Act may store a compact review marker such as `reviewed_through_chapter` plus an optional short review note/reason.

Warnings should compare current exact manuscript authority to that reviewed-through chapter:
- Act: review when growth since structural review passes roughly 60 chapters;
- Book: review when growth since structural review passes roughly 100 chapters.

Do not use dates as the primary trigger. PLG can add many chapters in one session or sit unchanged for weeks; chapter growth is the variable that actually creates structural drift.

A review marker means `human/editorial structure was reconsidered through here`, not `a boundary was created here`.

## Approved update 20 — migrate in shadow mode before replacing current reader structure

Do not switch reader production directly from the hard-coded `BOOKS` tuple to the manifest in one blind step.

Migration sequence:
1. add the structural manifest and loader;
2. render/resolve structure from both the legacy tuple and the manifest for the already-stable Books I–III and compare normalized output;
3. confirm the manifest intentionally differs for Book IV/V according to the approved repass;
4. add tests for open-end behavior, membership, role-card intent, and current-frontier rendering;
5. only then remove the hard-coded tuple as authority.

The comparison is a migration guard, not permanent dual authority. Once parity/intended differences are verified, delete the legacy structural definitions rather than keeping two paths forever.

This is especially important because the current renderer abstraction is good. The goal is to swap its data source without unnecessarily rewriting rendering behavior that already works.

## Integration note

Do not duplicate this logic into separate Illustrated/Text implementations. `reader_sections.py` is already shared infrastructure and should remain the common rendering path. The fix is to move editorial structure below it into data, then make generation and validation consume the same data.

## Next implementation order

1. add the skinny structural manifest with chapter-based review markers;
2. add loader/validation and shadow-compare it against the existing `reader_sections.py` definitions;
3. derive a deterministic chapter catalog from exact manuscript source loading;
4. make `reader_sections.py` and `verify_reader_frontier.py` structure-driven;
5. resolve role-card assets through visual authority rather than hard-coding asset truth into structure;
6. remove handwritten chapter-index dependency from home-content generation;
7. add `project_check.py structure` and CI/test coverage;
8. delete legacy hard-coded structural definitions after migration parity/intended-difference checks pass.

Preserve the active visual production hold. Backend structural work may proceed while new Book V image generation remains blocked.