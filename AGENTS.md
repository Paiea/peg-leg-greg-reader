# PEG-LEG GREG — WORKER ROUTER

This repository is the durable project brain.

Before substantial work:

1. inspect current `main`
2. read `state/PROJECT_STATE.md`
3. identify your lane
4. read `state/STORY_NORTH_STAR.md` for narrative/development work
5. read the relevant lane state/playbook files
6. inspect exact manuscript/reader/source authority needed for the task
7. preserve newer GitHub-authoritative work

Do not rely on a stale chat prompt for current story position.

## Authority

- manuscript prose outranks summaries
- `state/PROJECT_STATE.md` defines repository authority/synchronization rules
- `state/STORY_NORTH_STAR.md` defines durable artistic direction but is not plot canon
- lane state files route work but do not outrank exact manuscript evidence
- external research informs development but is not canon
- exploratory chat is not canon
- WIP branches are durable but not accepted `main`

## Shared development architecture

For narrative development, read `state/DEVELOPMENT_CYCLE.md`.

Primary loop:

**02 Writers' Room: EXPLORE → RESEARCH → SYNTHESIZE**

**03 Story Control: INTEGRATE → PRESSURE-TEST → CLASSIFY**

Then repeat while 01 continues forward manuscript production.

Reusable external research belongs in `state/RESEARCH_LEDGER.md`, with sources, limits, story translation, and canon status kept separate.

## Lanes

### Manuscript / 01
Read `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`, `state/MANUSCRIPT_WORKFLOW.md`, `state/MANUSCRIPT_STATE.md`, `state/OPEN_THREADS.md`, the current manuscript edge, and `state/PROSE_PLAYBOOK.md` when present. Use `state/STORY_NORTH_STAR.md` as durable artistic direction. Consult character/setting/plot/development files only when useful. Preserve throughput.

### Writers' Room / 02
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/WRITERS_ROOM_STATE.md`, and relevant specialist brains. Explore alternatives, research real practice when useful, translate research into behavior/social/work possibilities, update durable residue, and hand developed possibilities to 03. Do not canonize exploration.

### Story Control / 03
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/STORY_CONTROL_STATE.md`, `state/WRITERS_ROOM_STATE.md`, `state/PLOT_CONTROL.md`, `state/OPEN_THREADS.md`, and relevant research/bibles. Pressure-test possibilities against canon/rhythm/long-range direction, classify them, graduate only useful durable residue, and send focused research edges back to 02.

### Prose / editorial / 04
Read actual prose plus `state/PROSE_PLAYBOOK.md` and `state/STORY_NORTH_STAR.md`. Improve writing and longitudinal social texture without silently changing plot, canon, characterization, scene intent, or outcomes.

### Character
Read actual manuscript evidence plus `state/CHARACTER_BIBLE.md` and `state/STORY_NORTH_STAR.md`. Update durable character knowledge, relationships, offscreen causality, and anti-flattening constraints, not transcripts.

### Setting / world
Read actual manuscript evidence plus `state/SETTING_BIBLE.md`, `state/STORY_NORTH_STAR.md`, and relevant research. Deepen lived world through people, work, routes, objects, institutions, commerce, and repeated use rather than lore dumping.

### Research
Read `state/DEVELOPMENT_CYCLE.md` and `state/RESEARCH_LEDGER.md`. Research focused questions that materially improve story specificity. Prefer strong sources; distinguish supported practice from story translation; never silently convert research into canon.

### Plot / Story Control
Read current manuscript/state plus `state/PLOT_CONTROL.md` and `state/OPEN_THREADS.md`. Distinguish ESTABLISHED / PRESSURE / POSSIBILITY / AVOID / RESEARCH EDGE. Prefer convergence between existing threads over new machinery.

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

### GitHub-first handoff

When current project authority is already in GitHub, do not create or request a
full repository ZIP merely to move work between chats or agents.

Normal handoff:

**READ CURRENT GITHUB -> WORK ON BRANCH -> VALIDATE -> PR / MERGE -> UPDATE
DURABLE STATE -> LEAVE COMPACT RE-PROMPT**

Use a small targeted attachment only when required work is intentionally absent
from GitHub, such as the living heavy-edit manuscript, a genuinely unique source
asset, an exact recovery block, or a user-requested offline archive. Full-project
ZIPs are exceptional recovery artifacts, not routine checkpoints.

## Handoff

Follow `state/HANDSHAKE_PROTOCOL.md` when present.

At the end of substantial work:
- validate what changed
- update only relevant durable state
- record a compact next executable edge
- leave one copyable re-prompt that points the next worker back to GitHub
- store the durable lane re-prompt / trailhead in the relevant state or playbook when that lane uses one
- **also show a copyable next prompt visibly in the user-facing response before ending**

A GitHub-only re-prompt is not a complete human handoff. Do not make the user ask what to do next after a substantial run unless they explicitly asked for no next-step prompt.

The visible prompt should target the worker/lane you actually recommend running next. That may differ from the durable same-lane restart prompt stored in GitHub.

The long-term goal is that fresh workers reconstruct their role primarily from repository state rather than giant handoff prompts.

Minimal fresh-chat starters are intentionally valid:

- `Continue Peg-Leg Greg from current GitHub authority.`
- `Continue Peg-Leg Greg Writers' Room from current GitHub authority.`
- `Continue Peg-Leg Greg Story Control from current GitHub authority.`
