# PEG-LEG GREG — LIGHT EDITION STATE

Durable publishing memory for the text-first reader. Exact manuscript authority outranks this file and compact state.

## PURPOSE

The public reader is one book with two intentional modes:

- **ILLUSTRATED** — existing art-forward static chapter pages.
- **LIGHT** — fast text-first static publishing derivatives with no chapter illustrations.

Light pages are disposable publishing output. They are never prose authority.

## SOURCE AUTHORITY

Generation must preserve these source rules:

- Published illustrated range through Chapter 155: extract exact prose from `chapters/NNN.html` and omit illustrations.
- Chapters 156–219: `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`.
- Chapters 220+: `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md`.

Do not reconstruct missing prose from summaries or compact state.

The current exact running manuscript contains one legacy alternate chapter-heading form at Chapter 232:

`## Chapter 232 — THE COUNTERSIGN`

The Light parser supports that exact combined heading form in addition to the normal `# CHAPTER N` plus `## TITLE` form. The manuscript was not rewritten to satisfy the publisher.

## CURRENT ARCHITECTURE

Generator:

`python scripts/generate_light.py <range>`

Supported range forms:

- `current` — all Chapter 220+ prose actually present in the permanent running manuscript.
- `N-N` — bounded exact range such as `156-219` or `100-155`.

Bounded generation is strict: if any requested chapter is absent from source authority, generation fails instead of silently publishing a partial range.

Generated namespace:

- `light/index.html` — range-organized Light TOC.
- `light/NNN.html` — direct static Light chapter pages.
- `light/manifest.json` — generated chapter metadata and exact current endpoint.
- `latest.html` — regenerated from the newest exact chapter available to the generator.

The generator also prunes numeric Light chapter derivatives whose exact source chapter no longer exists. Withdrawn or corrected forward material must not remain publicly reachable as stale generated HTML.

`python scripts/verify_light.py <range>` verifies generated title, prose body, navigation, Light-only presentation constraints, manifest coverage, latest routing, and absence of orphan numeric Light pages against source authority.

Previous/Next navigation is numerically gap-aware. A missing exact chapter may not be silently skipped in sequential navigation; once the missing exact chapter appears, regeneration restores the normal chain automatically.

Legacy `light.html?chapter=N` remains a compatibility router. If a requested chapter has a static Light page it redirects there. During remaining backfill, compatibility rendering is limited to old published chapter HTML and no longer downloads the recovered or running manuscript into the browser.

## CURRENT STATIC COVERAGE

Verified checkpoint at this handoff:

- Chapters 156–219 — static and verified from recovered exact authority.
- Chapters 220–234 — static and verified from the permanent running manuscript.
- Continuous static Light coverage: Chapters 156–234.
- Current exact Light-publishable endpoint: Chapter 234 — **THE CONDITION**.
- No exact-source chapter gap remains in the 156–234 static range at this checkpoint.

Chapter 232 previously appeared absent to the Light build because its exact prose used the combined heading `## Chapter 232 — THE COUNTERSIGN`. That was a parser-compatibility defect, not missing prose. The reader tooling now recognizes the exact source form without altering manuscript authority.

Re-check exact running prose on every future reader run. `generate_light.py current` should publish new exact forward chapters automatically.

## AUTOMATION

`.github/workflows/light-edition.yml` now:

1. runs the full reader tooling tests;
2. generates Chapters 156–219;
3. regenerates the current exact 220+ range;
4. prunes stale numeric Light derivatives no longer backed by exact source;
5. keeps the homepage Light entry point present;
6. verifies both recovered and current generated prose against authority;
7. verifies the 219 → 220 source seam as ordinary reader navigation;
8. rejects orphan generated chapter pages;
9. keeps `latest.html` current;
10. commits changed publishing derivatives.

Future forward-manuscript commits should therefore be cheap to publish in Light mode without waiting for illustrations or old-range backfill.

## PRESENTATION RULES

Light should read like an intentional novel edition, not an internal manuscript utility.

- no chapter images
- no GitHub/manuscript-authority jargon in ordinary reader-facing copy
- clear HOME / ILLUSTRATED / LIGHT / LATEST / ART navigation
- previous / chapters / next on chapter pages
- comfortable text measure and mobile margins
- range-oriented TOC rather than one undifferentiated chapter wall
- preserve direct links
- preserve illustrated reader rather than replacing it

Current TOC priority remains:

1. CURRENT — open and easiest to reach.
2. Chapters 156–219 — static but collapsed by default.
3. Chapters 100–155 — compatibility until the next backfill.
4. Chapters 83–99.
5. Chapters 1–82.

Do not invent fake Acts or Books merely to organize the reader.

## BACKFILL ORDER

Completed:

1. CURRENT / Chapter 220+ — static current-first architecture established and automated against exact running prose.
2. Chapters 156–219 — static recovered-exact backfill completed and verified.

Next:

3. Chapters 100–155 — generate from exact illustrated chapter prose, stripping only illustrations/presentation markup.

Later if still useful:

4. Chapters 83–99.
5. Chapters 1–82.

Current content must never wait for old-range completion.

## SAFETY

- Do not edit manuscript prose from the Light lane.
- Do not make generated Light HTML a competing manuscript.
- Do not regenerate or destructively alter illustrations as part of Light backfill.
- Do not delete the compatibility router until static coverage is proven sufficient.
- Run tests before generation.
- Keep generated chapter number/title/prose aligned to exact source authority.
- When adding a static range, re-render existing generated neighbors so previous/next links switch cleanly from compatibility URLs to direct static URLs.
- If compact state and exact prose disagree, publish only what exact prose authority supports and record the discrepancy rather than inventing missing text.
- Accept supported exact source heading forms in the publisher; do not rewrite manuscript prose merely to satisfy generated-output tooling.

## RE-PROMPT [READER]

Continue the Peg-Leg Greg Light edition from fresh current GitHub authority. Read `AGENTS.md`, current `state/MANUSCRIPT_STATE.md`, `state/LIGHT_EDITION_STATE.md`, `scripts/generate_light.py`, `scripts/verify_light.py`, `.github/workflows/light-edition.yml`, and the current Light reader files. Re-verify the permanent running manuscript directly before trusting the compact endpoint, then regenerate `current` from whatever exact prose exists. Preserve the established static Light architecture and verified continuous 156→current exact reading path. Next bounded pass: generate and verify static Light Chapters 100–155 from the exact published `chapters/NNN.html` prose, stripping chapter illustrations but not rewriting text. Pressure-test the 155→156 seam, mode-switch links for chapters that now have both editions, and the compatibility reader after its remaining responsibility shrinks to Chapters 1–99. Do not edit prose or art. Keep `latest.html` derived from the actual exact endpoint. Before ending, visibly provide the next copyable reader prompt.
