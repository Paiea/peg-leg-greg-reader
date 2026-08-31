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

- `current` — all Chapter 220+ prose materialized in the permanent running manuscript.
- `N-N` — bounded exact range such as `156-219` or `100-155`.

Generated namespace:

- `light/index.html` — range-organized Light TOC.
- `light/NNN.html` — direct static Light chapter pages.
- `light/manifest.json` — generated chapter metadata and current endpoint.
- `latest.html` — regenerated from the newest exact chapter available to the generator.

Legacy `light.html?chapter=N` remains a compatibility router. If a requested chapter has a static Light page it redirects there; otherwise the existing dynamic exact-text reader remains available during staged backfill.

## CURRENT STATIC EDGE

Current-first generation is verified through Chapter 231 — **THE MAGISTRATE** from live manuscript authority.

Do not treat 231 as a permanent endpoint. `current` must derive the newest chapter from current manuscript authority whenever it runs.

## AUTOMATION

`.github/workflows/light-edition.yml` tests reader tooling, regenerates the current Light range, keeps `latest.html` current, and surfaces the Light edition from the homepage.

Future forward-manuscript commits should therefore be cheap to publish in Light mode without waiting for illustrations or old-range backfill.

## PRESENTATION RULES

Light should read like an intentional novel edition, not an internal manuscript utility.

- no chapter images
- no GitHub/manuscript-authority jargon in ordinary reader-facing copy
- clear HOME / ILLUSTRATED / LIGHT / LATEST / ART navigation
- previous / chapters / next on chapter pages
- comfortable text measure and mobile margins
- range-oriented TOC rather than one undifferentiated 230+ chapter wall
- preserve direct links
- preserve illustrated reader rather than replacing it

## BACKFILL ORDER

Current priority:

1. CURRENT / Chapter 220+ — architecture established and generated first.
2. Chapters 156–219 — next static backfill from recovered exact authority.
3. Chapters 100–155 — then backfill from exact illustrated chapter prose.
4. Chapters 83–99 and 1–82 later if useful.

Current content must never wait for old-range completion.

## SAFETY

- Do not edit manuscript prose from the Light lane.
- Do not make generated Light HTML a competing manuscript.
- Do not regenerate or destructively alter illustrations as part of Light backfill.
- Do not delete the compatibility reader until static coverage is proven sufficient.
- Run tests before generation.
- Keep generated chapter number/title/prose aligned to exact source authority.

## RE-PROMPT [READER]

Continue the Peg-Leg Greg Light edition from current GitHub authority. Read `AGENTS.md`, `state/MANUSCRIPT_STATE.md`, `state/LIGHT_EDITION_STATE.md`, and relevant reader files. Re-verify the current manuscript endpoint first. Preserve the current-first static Light architecture, compatibility routing, homepage access, and illustrated reader. Next recommended bounded pass: generate and verify static Light Chapters 156–219 from `state/manuscript/Peg_Leg_Greg_Recovered_Ch156-219_EXACT.md`; polish any compatibility-only reader language that becomes obsolete; do not edit prose or art. Keep `latest.html` derived from the actual current endpoint. Before ending, visibly provide the next copyable reader prompt.
