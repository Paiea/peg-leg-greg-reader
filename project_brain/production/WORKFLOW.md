# PEG-LEG GREG — SHARED WORKFLOW

This repository is the durable coordination layer for manuscript, story development, worldbuilding, editing, visuals, reader/UI, and publishing work.

## Before working

1. Identify your lane.
2. Read `project_brain/README.md`.
3. Read only the project-brain files relevant to the task.
4. Inspect current manuscript/repository authority before changing canon-dependent material.
5. Never assume an old chat handoff is newer than GitHub.

## Lanes

### Manuscript
Primary responsibility: write and integrate canonical chapters.

Read:
- `project_brain/canon/CANON.md`
- `project_brain/story/STORY_STATE.md`
- relevant character/world files

May update:
- manuscript/chapter files
- compact project-brain state that genuinely changed because of new canon

Must not:
- rewrite unrelated reader/UI infrastructure
- canonize exploratory possibilities without manuscript support or explicit approval

### Writers' Room / Story Control
Primary responsibility: explore, pressure-test, connect, and develop future story.

Read:
- current manuscript authority
- `project_brain/story/STORY_STATE.md`
- relevant canon/character/world files

May update:
- durable story tensions
- unresolved questions
- clearly labeled possibilities
- compact character/world implications

Must not:
- edit canonical manuscript prose unless explicitly tasked
- convert brainstorming into canon

### Character / Worldbuilding
Primary responsibility: deepen established people, places, institutions, systems, and constraints.

May update:
- `characters/`
- `world/`
- `canon/` only for explicit canon

Prefer filling gaps when story pressure exposes them. Do not worldbuild merely to complete a taxonomy.

### Prose / Editorial
Primary responsibility: improve prose while preserving plot, characterization, canon, scene intent, and outcomes unless repairing an obvious contradiction.

Read current manuscript first. Do not work from stale exported prose when the repository has newer authority.

### Visual / Reader UI
Primary responsibility: illustration coverage, image integration, presentation, reader behavior.

Do not overwrite manuscript authority. Keep UI commits separable from manuscript commits when practical.

### Publishing / GitHub
Primary responsibility: validation, integration, branch/commit hygiene, release/checkpoint work.

Never replace newer whole files with stale handoff versions. Port forward compatible changes by category.

## Update protocol

At the end of substantial work:

- Update only files whose durable state changed.
- Prefer replacing stale facts over appending endless history.
- Preserve unresolved questions only if they are likely to matter again.
- Do not store chat transcripts.
- Do not store chain-of-thought or hidden reasoning.
- Keep exploratory alternatives labeled as non-canon.
- If a file is becoming hard to scan, split by a real domain boundary, not arbitrary size.

## Concurrency rule

Assume another lane may be working simultaneously.

- Prefer a dedicated branch for structural or cross-cutting changes.
- Avoid editing the same manuscript files as an active manuscript lane unless explicitly coordinated.
- Keep reader/UI, project-brain, and manuscript changes separable when possible.
- Before merging, rebase/refresh against current authority and resolve conflicts in favor of newer manuscript canon.

## Handoff rule

A handoff should contain only:
- what changed
- current authority / endpoint
- unresolved risks
- next executable step

The project-brain files should hold durable memory; handoffs should not become a second competing wiki.
