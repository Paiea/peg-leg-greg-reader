# PEG-LEG GREG — CHAT ROUTER

Use this file to orient any fresh Peg-Leg Greg chat or agent.

## Universal startup prompt

> Work on Peg-Leg Greg from `Paiea/peg-leg-greg-reader`. Treat GitHub as durable shared project memory. First inspect current HEAD, `state/MANUSCRIPT_STATE.md`, `AGENTS.md`, `project_brain/README.md`, and the project-brain files relevant to your lane. The manuscript remains prose authority. Do not rely on old chat memory when GitHub is newer. Work in a dedicated branch when appropriate. After meaningful work, update compact durable state and leave a fresh-worker handoff/re-prompt.

That prompt is intentionally small. The repository should carry the missing context.

## Pick a lane

### Manuscript
Read current manuscript authority, manuscript state, canon, story state, open threads, and relevant character/world files. Write prose first. Update durable state only after the chapter is settled.

### Story / Writers' Room
Read manuscript state plus story/character/world memory. Explore alternatives in chat. Do not promote possibilities to canon. Persist only the useful residue and next edge.

### Character
Read current manuscript evidence plus `characters/`. Track current role, relationship state, competencies, tensions, contradictions, and unresolved pressure.

### Worldbuilding
Read current manuscript evidence plus `world/` and affected story files. Build where story pressure creates a need. Avoid encyclopedia completion for its own sake.

### Reader / UI
Read `production/READER_VISUAL_STATE.md`, current reader files, and only enough manuscript evidence to preserve meaning. Presentation work must not rewrite prose.

### Visual production
Read reader visual state plus relevant manuscript scenes. Coverage first. Keep/retry based on major continuity and anatomy errors rather than perfectionism.

### Publishing / integration
Verify newest manuscript authority before synchronizing derived reader files. Validate endpoint, ordering, links, images, indexes, and unexpected rewrites.

## Fresh-worker passoff

A worker finishing substantial work should leave enough for a RANDOM next worker, not just the same chat.

Update the relevant durable files, then write a compact handoff under `project_brain/handoffs/` when needed. The handoff should contain:

- authority / commit used
- lane completed
- files changed
- durable decisions or discoveries
- unresolved issues
- validation status
- next recommended action
- a copyable re-prompt that starts by reading GitHub

Do not restate the entire story in the re-prompt.

## Re-prompt pattern

> Continue Peg-Leg Greg from the current repository. Read `AGENTS.md`, `state/MANUSCRIPT_STATE.md`, `project_brain/README.md`, and `[lane files]` before acting. Inspect newer commits because another worker may have advanced the project. Your lane is `[LANE]`. Preserve manuscript authority and other active lanes. Continue from `[NEXT EDGE]`. After working, validate, update durable project-brain state, and leave a fresh-worker handoff/re-prompt.

## Why this exists

Dedicated chats are useful but disposable. Continuity should survive chat limits, model changes, separate agents, and forgotten handoffs. The repo is the shared memory bus.