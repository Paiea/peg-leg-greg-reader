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
- `state/voices/` is focused craft authority for recurring-character dialogue and does not outrank exact prose
- `state/DIALOGUE_VARIANCE_ENGINE.md` is project-wide runtime guidance for relationship-, state-, pressure-, and variance-driven speech modulation
- external research informs development but is not canon
- exploratory chat is not canon

## Shared development architecture

For narrative development, read `state/DEVELOPMENT_CYCLE.md`.

Primary loop:

**02 Writers' Room: EXPLORE -> RESEARCH -> SYNTHESIZE**

**03 Story Control: INTEGRATE -> PRESSURE-TEST -> CLASSIFY**

Then repeat while 01 continues forward manuscript production.

Reusable external research belongs in `state/RESEARCH_LEDGER.md`, with sources, limits, story translation, and canon status kept separate.

`state/STORY_ANTI_PATTERNS.md` is the compact negative-knowledge guardrail for recurring narrative/editorial failure modes. Consult it when relevant; it is not canon and is not mandatory every-chapter boot reading.

## Lanes

### Manuscript / 01
Read `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`, `state/MANUSCRIPT_WORKFLOW.md`, `state/MANUSCRIPT_STATE.md`, `state/OPEN_THREADS.md`, the current manuscript edge, and `state/PROSE_PLAYBOOK.md` when present. Use `state/STORY_NORTH_STAR.md` as durable artistic direction. Consult `state/STORY_ANTI_PATTERNS.md` when a chapter choice risks a known recurring failure mode. For substantial dialogue involving a recurring character, consult that character's page under `state/voices/`; when the scene depends on mood, relationship, social status, or speech variation, also consult `state/DIALOGUE_VARIANCE_ENGINE.md`. Do not read the whole voice folder every chapter. Consult character/setting/plot/development files only when useful. Preserve throughput.

01 is intentionally chat-independent. Previous chat history may help but is never required authority. A fresh worker must reconstruct the current endpoint and next executable chapter from current GitHub state. For normal accepted forward production, treat one complete chapter as one durable transaction: draft, validate, update the permanent manuscript and relevant living state, store the next trailhead in `MANUSCRIPT_STATE.md`, commit, verify current `main`, then advance.

If chat history or a prompt claims a chapter exists but GitHub ends earlier, stop forward numbering and recover exact durable prose first if it exists. Never fabricate a missing chapter from summaries or chat residue.

### Writers' Room / 02
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/WRITERS_ROOM_STATE.md`, and relevant specialist brains. Consult `state/STORY_ANTI_PATTERNS.md` when an exploration risks a known recurring failure mode. Explore alternatives, research real practice when useful, translate research into behavior/social/work possibilities, update durable residue, and hand developed possibilities to 03. Do not canonize exploration.

### Story Control / 03
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/STORY_CONTROL_STATE.md`, `state/WRITERS_ROOM_STATE.md`, `state/PLOT_CONTROL.md`, `state/OPEN_THREADS.md`, and relevant research/bibles. Consult `state/STORY_ANTI_PATTERNS.md` when pressure-testing a direction that risks a known recurring failure mode. Pressure-test possibilities against canon/rhythm/long-range direction, classify them, graduate only useful durable residue, and send focused research edges back to 02.

### Prose / editorial / 04
Read actual prose plus `state/PROSE_PLAYBOOK.md`, `state/EDITOR_STATE.md`, and `state/STORY_NORTH_STAR.md`. Consult `state/STORY_ANTI_PATTERNS.md` when an edit risks flattening voice, relationships, evidence discipline, or serial texture. For substantial recurring-character dialogue, read the relevant page under `state/voices/` plus exact manuscript context. When shaping dialogue, also use `state/DIALOGUE_VARIANCE_ENGINE.md` so baseline voice is modulated by relationship, current state, scene pressure, and controlled human variance instead of becoming a fixed gimmick. Improve writing and longitudinal social texture without silently changing plot, canon, characterization, scene intent, or outcomes except when an explicitly authorized structural pass permits chapter merge/cut/renumbering under a frozen structural map.

Dialogue clarity is part of prose quality. Use simple tags freely. In multi-speaker scenes, do not make the reader perform speaker bookkeeping merely because the voices are intended to be distinct.

### Character
Read actual manuscript evidence plus `state/CHARACTER_BIBLE.md`, `state/STORY_NORTH_STAR.md`, and `state/voices/INDEX.md` when dialogue/voice work is involved. Update durable character knowledge, relationships, offscreen causality, and anti-flattening constraints, not transcripts. Update an individual voice page when repeated manuscript evidence changes how that recurring person speaks or processes the world. Use `state/DIALOGUE_VARIANCE_ENGINE.md` to distinguish stable speech center from relationship- and state-dependent performance.

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

Broad prose compression, chapter merging/deletion, renumbering, and manuscript-wide voice surgery belong on a branch first.

### GitHub-first handoff

When current project authority is already in GitHub, do not create or request a full repository ZIP merely to move work between chats or agents.

Normal handoff:

**READ CURRENT GITHUB -> WORK -> VALIDATE -> UPDATE DURABLE STATE -> COMMIT / MERGE -> VERIFY -> LEAVE COMPACT TRAILHEAD**

Use a small targeted attachment only when required work is intentionally absent from GitHub, such as the living heavy-edit manuscript, a genuinely unique source asset, an exact recovery block, or a user-requested offline archive. Full-project ZIPs are exceptional recovery artifacts, not routine checkpoints.

## Handoff

Follow `state/HANDSHAKE_PROTOCOL.md` when present.

At the end of substantial work:
- validate what changed
- update only relevant durable state
- record a compact next executable edge
- store the durable lane re-prompt / trailhead in the relevant state or playbook when that lane uses one
- show a compact copyable restart prompt visibly in the user-facing response unless the user asked for no next-step prompt

For Manuscript / 01 specifically, detailed chapter steering belongs in `MANUSCRIPT_STATE.md`. Do not duplicate a giant chapter-specific prompt in chat when the durable trailhead already contains the necessary information.

The long-term goal is that fresh workers reconstruct their role primarily from repository state rather than giant handoff prompts.

Minimal fresh-chat starters are intentionally valid:

- `Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.`
- `Continue Peg-Leg Greg Writers' Room from current GitHub authority.`
- `Continue Peg-Leg Greg Story Control from current GitHub authority.`
- `Continue Peg-Leg Greg as 04 — Heavy Prose Editor from current GitHub authority.`
- `Continue Peg-Leg Greg as 05 — Visual Production / Image Lab from current GitHub authority.`
- `Continue Peg-Leg Greg as 06 — Manuscript Polish / General Editor from current GitHub authority.`
- `Continue Peg-Leg Greg Reader / UI from current GitHub authority.`

Do not paste a giant lane prompt into every replacement chat unless a genuinely new requirement is not yet represented in GitHub. When a lane's operating rules are durable in repo state, the short starter is preferred.