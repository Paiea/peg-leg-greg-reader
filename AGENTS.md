# PEG-LEG GREG — REPOSITORY WORKER INSTRUCTIONS

This repository is the durable continuity spine for Peg-Leg Greg. A chat, Codex session, or other agent should be able to start fresh, orient from GitHub, work in one lane, leave durable state, and hand off to another fresh worker without relying on the original conversation.

## Authority

Use this order when sources disagree:

1. current authoritative manuscript prose
2. `state/MANUSCRIPT_STATE.md` for current endpoint and explicit production continuity
3. explicit canon in `project_brain/canon/`
4. other `project_brain/` state
5. handoffs and exploratory notes
6. chat memory

Never restore an older whole-file manuscript over newer authority.

## Start every substantial task

1. Inspect current `main` / repository HEAD.
2. Read `state/MANUSCRIPT_STATE.md`.
3. Read `project_brain/README.md` and `project_brain/CHAT_ROUTER.md` when present.
4. Read only the project-brain files relevant to the lane.
5. Verify manuscript authority before canon-dependent claims.
6. Work on a dedicated branch when other lanes may be active.

## Lanes

Manuscript: prose authority first. Update state after writing.

Story / Writers' Room: explore freely in chat; write only durable residue to GitHub.

Character / Worldbuilding: distinguish ESTABLISHED, STRONG INFERENCE, POSSIBILITY, and OPEN QUESTION.

Reader / UI / Art: do not alter manuscript prose as a presentation side effect.

Publishing: validate endpoint, ordering, links, art references, and unintended rewrites before shipping.

## Durable-memory rule

GitHub stores compact reusable state, not transcripts and not private reasoning. Save:

- established facts
- current relationship and arc state
- continuity constraints
- unresolved pressures
- decisions
- evidence status
- next executable edge

Prune obsolete information instead of endlessly appending.

## Handoff rule

At the end of substantial work:

1. update the relevant `project_brain/` file(s)
2. update `project_brain/PROJECT_STATUS.md` if endpoint, active lane, or major project state changed
3. leave a compact handoff using `project_brain/handoffs/HANDOFF_TEMPLATE.md` when another worker needs a bridge
4. include a copyable re-prompt for a fresh worker when continuation is useful

A re-prompt should tell the next worker to read GitHub first. It should not try to reproduce the whole project in chat.

## Concurrency

Assume another worker may be changing the repository.

- refresh before writing
- isolate lanes by branch
- avoid force pushes
- avoid touching manuscript-authority files from UI/art/worldbuilding lanes
- prefer small commits with one purpose
- open a PR for side-lane work
- if `main` moves, re-check authority before merging

The target workflow is RANDOM WORKER -> READ REPO -> DO ONE LANE -> UPDATE DURABLE STATE -> HANDOFF -> RANDOM NEXT WORKER.