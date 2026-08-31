# PEG-LEG GREG — WORKER ROUTER

This repository is the durable project brain.

Before substantial work:

1. inspect current `main`
2. read `state/PROJECT_STATE.md`
3. identify your lane
4. read the relevant lane state/playbook files
5. inspect exact manuscript/reader/source authority needed for the task
6. preserve newer GitHub-authoritative work

Do not rely on a stale chat prompt for current story position.

## Authority

- manuscript prose outranks summaries
- `state/PROJECT_STATE.md` defines repository authority/synchronization rules
- lane state files route work but do not outrank exact manuscript evidence
- exploratory chat is not canon
- WIP branches are durable but not accepted `main`

## Lanes

### Manuscript
Read `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`, `state/MANUSCRIPT_WORKFLOW.md`, `state/MANUSCRIPT_STATE.md`, `state/OPEN_THREADS.md`, the current manuscript edge, and `state/PROSE_PLAYBOOK.md` when present. Consult character/setting/plot bibles only when useful. Preserve throughput.

### Prose / editorial
Read actual prose plus `state/PROSE_PLAYBOOK.md`. Improve writing without silently changing plot, canon, characterization, scene intent, or outcomes.

### Character
Read actual manuscript evidence plus `state/CHARACTER_BIBLE.md`. Update durable character knowledge, not transcripts.

### Setting / world
Read actual manuscript evidence plus `state/SETTING_BIBLE.md`. Deepen lived world only where story/use creates need.

### Plot / Story Control
Read current manuscript/state plus `state/PLOT_CONTROL.md` and `state/OPEN_THREADS.md`. Distinguish ESTABLISHED / PRESSURE / POSSIBILITY / AVOID.

### Visual production
Read `state/VISUAL_BIBLE.md` and `state/IMAGE_PRODUCTION.md`, then actual manuscript scenes and reader coverage. Coverage first; integrate only accepted art.

### Reader / UI
Read `state/READER_DESIGN_LAB.md`, visual guidance, current reader files, and current project authority. Use a branch for broad changes. Never rewrite prose as a presentation side effect.

### Publishing / repository integration
Prefer small legible commits. Reconcile in favor of newer authority. Never restore stale whole-file versions over newer work.

## GitHub workflow

Use:

**CHAT = disposable thinking**

**BRANCH = durable WIP / broad or risky work**

**MAIN = accepted authority / small atomic completed work**

Avoid finished work existing only in chat or a mystery local file.

## Handoff

Follow `state/HANDSHAKE_PROTOCOL.md` when present.

At the end of substantial work:
- validate what changed
- update only relevant durable state
- record a compact next executable edge
- leave one copyable re-prompt that points the next worker back to GitHub

The long-term goal is that fresh workers reconstruct their role primarily from repository state rather than giant handoff prompts.