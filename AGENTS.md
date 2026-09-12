# PEG-LEG GREG - WORKER ROUTER

This file is a map, not the project brain.

Keep context cold until the task needs it. Read the smallest authoritative surface that can safely answer the current task.

## Universal rules

1. Inspect current GitHub authority before substantial work.
2. Exact source files outrank summaries, chat history, branch names, and stale handoffs.
3. Preserve newer GitHub-authoritative work. Never restore a stale whole-file copy over newer state.
4. CHAT is disposable thinking. BRANCH is durable WIP for broad/risky work. MAIN is accepted authority and small atomic completed work.
5. Reuse existing tools, components, state, and workflows before inventing parallel systems.
6. Prefer deterministic repository tools for lookup, validation, reconciliation, and mechanical work before model reasoning.
7. Do not preload unrelated specialist brains. Follow the route for the task, then open deeper files only when a real dependency appears.
8. When authority or lane ownership is genuinely ambiguous, consult `state/PROJECT_STATE.md` and current branches/PRs rather than guessing.
9. Exact manuscript prose remains story authority. Showcase visibility never changes canon.
10. For substantial cross-worker handoff, follow `state/HANDSHAKE_PROTOCOL.md` and leave a compact durable trailhead.

## Codex execution

For Codex implementation/campaign work, read:

- `state/editorial/CODEX_EXECUTION_POLICY.md`
- `state/CODEX_TASK_PACKET.md`

Default posture: one strong primary agent, one bounded target, deterministic tools first, verify, stop, return control to Chat/Mana.

Do not spawn subagents unless the task packet explicitly authorizes parallelism. A bounded target may still require multi-file edits, debugging, tests, and iteration; Codex owns that work inside the approved boundary.

Project Codex concurrency is guarded by `.codex/config.toml`.

## Route by task

### 01 - Manuscript Engine
Read:
- `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`
- `state/MANUSCRIPT_WORKFLOW.md`
- `state/MANUSCRIPT_STATE.md`
- `state/OPEN_THREADS.md`
- exact recent manuscript authority

Use `state/STORY_NORTH_STAR.md` for durable artistic direction. Consult specialist brains only when the chapter/task needs them.

### 02 - Writers' Room
Read current manuscript/state plus:
- `state/WRITERS_ROOM_STATE.md`
- `state/DEVELOPMENT_CYCLE.md`
- `state/RESEARCH_LEDGER.md` when research is relevant

Explore; do not silently canonize possibilities.

### 03 - Story Control
Read current manuscript/state plus:
- `state/STORY_CONTROL_STATE.md`
- `state/DEVELOPMENT_CYCLE.md`
- `state/PLOT_CONTROL.md`
- `state/OPEN_THREADS.md`

Pressure-test and classify. Graduate only useful durable residue.

### 04 - Prose / editorial
Read actual prose plus:
- `state/PROSE_PLAYBOOK.md`
- `state/STORY_NORTH_STAR.md`

Inspect current PRs/branches only when the requested specialty suggests a narrower active owner. Do not preload unrelated editorial history.

### Character / setting / plot / research
Open only the matching specialist surface as needed:
- `state/CHARACTER_BIBLE.md`
- `state/SETTING_BIBLE.md`
- `state/PLOT_CONTROL.md`
- `state/RESEARCH_LEDGER.md`

Exact manuscript evidence outranks all specialist summaries.

### Visual production
Read:
- `state/VISUAL_BIBLE.md`
- `state/IMAGE_PRODUCTION.md`
- exact manuscript scenes / current reader coverage

If binary transport matters, also read `state/IMAGE_BINARY_HANDOFF.md`.

### Reader / UI
Read:
- `state/READER_DESIGN_LAB.md`
- current reader files
- visual guidance only when relevant

Preserve prose authority. When showcase curation matters, use `publishing/showcase_chapters.json` for public ordering while preserving canonical IDs and file paths.

### Greg, Again / R2 audio
Read:
- `r2/PIPELINE.md`
- `r2/AUDIO_PRODUCTION.md`
- the exact current source surface for the target chapter/work

When Codex is the worker, also read `r2/CODEX_AUDIO_EFFICIENCY.md`.

For Audio Score v2 work, additionally read the relevant current audio-score production docs, including `r2/AUDIO_SCORE.md`, `r2/AUDIO_SCORE_PRODUCTION.md`, and `r2/AUDIO_PRONUNCIATION.md` when synthesis/pronunciation is involved.

Do not read unrelated manuscript/editorial brains merely because the repository contains them.

### Publishing / repository integration
Read the exact files being integrated plus their owning lane docs. Reconcile in favor of newer authority. Prefer small legible commits and validated deterministic checks.

## Repository tools

AI-facing operations live in `scripts/plg_ai_tools.py`; the optional MCP adapter is `scripts/plg_mcp_server.py`.

When existing tools can compile, resolve, query, reduce, validate, or execute state, use them instead of rediscovering layout manually.

Compiled brain output is disposable routing and never outranks repository source authority.

## GitHub-first handoff

Normal continuation:

`READ CURRENT GITHUB -> WORK -> VALIDATE -> UPDATE RELEVANT DURABLE STATE -> COMMIT / MERGE -> VERIFY -> LEAVE COMPACT TRAILHEAD`

Do not create giant replacement-chat prompts when the repository already contains the operating rules and trailhead.
