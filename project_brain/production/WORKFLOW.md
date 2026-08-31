# PEG-LEG GREG — PRODUCTION WORKFLOW

The repository is the durable passoff layer between chats and agents.

## Core loop

REFRESH -> READ AUTHORITY -> PICK ONE LANE -> WORK -> VALIDATE -> UPDATE DURABLE STATE -> HANDOFF -> FRESH WORKER CAN CONTINUE

## Before work

1. Check current `main` and recent commits.
2. Read `AGENTS.md`.
3. Read `state/MANUSCRIPT_STATE.md`.
4. Read `project_brain/PROJECT_STATUS.md`.
5. Read lane-specific project-brain files.
6. Verify whether another lane is likely touching the same files.
7. Use a dedicated branch for side-lane work.

## During work

- Manuscript changes own manuscript authority.
- Reader/UI work owns presentation files, not prose.
- Story/world/character exploration may read broadly but should write compact memory.
- Visual work should not casually rewrite chapter text.
- Publishing/integration should synchronize from newer authority, never from stale range-stamped backups.

## After substantial work

Update only what changed:

- canon if a hard fact changed
- story state if current pressure or trajectory changed
- relationships if relationship state changed
- world/magic if a reusable rule was established or disproven
- reader visual state if presentation/art workflow changed
- project status if endpoint, active lane, or major next step changed

Then leave a handoff if another worker will plausibly continue.

## Fresh-worker handoff philosophy

The handoff is a pointer and bridge, not a backup of the entire project.

A fresh worker should be told:

- where authority lives
- what lane just changed
- what to read
- what is unresolved
- what next action is recommended

The repository itself should carry the rest.

## Commit discipline

Prefer commits that answer one sentence:

- `Advance manuscript to Chapter N`
- `Seed project brain from Chapter N state`
- `Clean up reader presentation`
- `Synchronize reader through Chapter N`
- `Integrate visual coverage batch N`

Avoid giant mixed commits unless the changes are inseparable.

## Validation

Before publishing or merging:

- inspect diff for accidental large rewrites
- verify chapter endpoint and numbering where relevant
- verify links/navigation where relevant
- verify image references where relevant
- verify no stale `Lysa` use where it means canonical Lyssa
- verify no secrets/temp junk
- confirm manuscript prose was not changed by UI/art work

## Re-prompt requirement

For long-running lanes, finish with a full copyable fresh-worker re-prompt in chat or handoff. It should begin by telling the next worker to read current GitHub authority, because the next worker may have zero conversation context.

Dedicated agent identities are optional. Durable roles live in files, not in the survival of one chat.