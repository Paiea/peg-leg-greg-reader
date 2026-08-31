# PEG-LEG GREG — LIGHT EDITION STATE

Durable publishing memory for the text-first reader. Manuscript authority outranks this file.

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

## CURRENT ARCHITECTURE

Generator:

`python scripts/generate_light.py <range>`

Supported range forms:

- `current` — all Chapter 220+ prose present in the permanent running manuscript.
- `N-N` — bounded exact range such as `156-219` or `100-155`.

Bounded generation is strict: if any requested chapter is absent from source authority, generation fails instead of silently publishing a partial range.

Generated namespace:

- `light/index.html` — range-organized Light TOC.
- `light/NNN.html` — direct static Light chapter pages.
- `light/manifest.json` — generated chapter metadata and current endpoint.
- `latest.html` — regenerated from the newest chapter available to the generator.

`python scripts/verify_light.py <range>` verifies generated title, prose body, navigation, Light-only presentation constraints, manifest coverage, and latest routing against source authority.

Legacy `light.html?chapter=N` remains a compatibility router. If a requested chapter has a static Light page it redirects there. During remaining backfill, compatibility rendering is limited to old published chapter HTML and no longer downloads the recovered or running manuscript into the browser.

## CURRENT STATIC COVERAGE

Static Light coverage is continuous from Chapter 156 through the current forward endpoint.

Verified checkpoint at this handoff:

- Chapters 156–219 — static and verified from recovered exact authority.
- Chapters 220–232 — static and verified from the running manuscript.
- Current checkpoint endpoint: Chapter 232 — **THE MATCHER**.

Do not treat 232 as a permanent endpoint. `current` must derive the newest chapter from current manuscript authority whenever it runs.

## AUTOMATION

`.github/workflows/light-edition.yml` now:

1. runs the reader tooling tests;
2. generates Chapters 156–219;
3. regenerates the current 220+ range;
4. keeps the homepage Light entry point present;
5. verifies both recovered and current generated prose against authority;
6. verifies the 219 → 220 source seam as ordinary reader navigation;
7. keeps `latest.html` current;
8. commits changed publishing derivatives.

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

1. CURRENT / Chapter 220+ — static current-first architecture established and automated.
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

## RE-PROMPT [READER]

Continue the Peg-Leg Greg Light edition from fresh current GitHub authority. Read `AGENTS.md`, current `state/MANUSCRIPT_STATE.md`, `state/LIGHT_EDITION_STATE.md`, `scripts/generate_light.py`, `scripts/verify_light.py`, `.github/workflows/light-edition.yml`, and the current Light reader files. Re-verify the manuscript endpoint first and regenerate `current` if 01 has advanced. Preserve the established static Light architecture and the verified continuous 156→current reading path. Next bounded pass: generate and verify static Light Chapters 100–155 from the exact published `chapters/NNN.html` prose, stripping chapter illustrations but not rewriting text. Pressure-test the 155→156 seam, mode-switch links for chapters that now have both editions, and the compatibility reader after its remaining responsibility shrinks to Chapters 1–99. Do not edit prose or art. Keep `latest.html` derived from the actual current endpoint. Before ending, visibly provide the next copyable reader prompt.
