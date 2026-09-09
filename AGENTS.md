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

For substantial work, prefer the PLG Brain Compiler task packet when available. Use `brain_for` from `scripts/plg_ai_tools.py` to select relevant brain pointers, then read the exact referenced authority. Compiled brain output is disposable routing and never outranks repository source files. If routing confidence is low or the task is unknown, fall back to `state/PROJECT_STATE.md` and normal router discovery rather than inventing a specialty.

## Authority

- manuscript prose outranks summaries
- `state/PROJECT_STATE.md` defines repository authority/synchronization rules
- `state/STORY_NORTH_STAR.md` defines durable artistic direction but is not plot canon
- lane state files route work but do not outrank exact manuscript evidence
- external research informs development but is not canon
- exploratory chat is not canon
- WIP branches are durable but not accepted `main`

## Full Canon vs Showcase

Peg-Leg Greg has one story canon and a separate reader-facing curation layer.

- Full canonical manuscript chronology remains story authority even when a chapter is hidden from the public reading sequence.
- `publishing/showcase_chapters.json` controls only whole-chapter showcase visibility. It does not delete, de-canonize, rewrite, merge, or move manuscript events.
- Manuscript, Writers' Room, Story Control, character, setting, continuity, economy, and editorial workers must reason from **Full Canon**, including hidden showcase chapters.
- Reader / UI and publishing workers consume the **Showcase** sequence for public chapter lists, display numbering, and previous/next navigation.
- Canonical chapter IDs, source filenames, art registry references, and continuity references never renumber to match showcase numbering.
- Artwork stays attached to canonical chapter IDs. Hiding a chapter does not retire its art.
- Curation is whole-chapter only. Never add scene, paragraph, or prose-range hiding to the showcase manifest.
- Validate showcase state with `python scripts/project_check.py showcase`.

The showcase may become substantially shorter than Full Canon. That is intentional. Hidden chapters still happened.

## Shared development architecture

For narrative development, read `state/DEVELOPMENT_CYCLE.md`.

Primary loop:

**02 Writers' Room: EXPLORE → RESEARCH → SYNTHESIZE**

**03 Story Control: INTEGRATE → PRESSURE-TEST → CLASSIFY**

Then repeat while 01 continues forward manuscript production.

Reusable external research belongs in `state/RESEARCH_LEDGER.md`, with sources, limits, story translation, and canon status kept separate.

`state/STORY_ANTI_PATTERNS.md` is the compact negative-knowledge guardrail for recurring narrative/editorial failure modes. Consult it when relevant; it is not canon and is not mandatory every-chapter boot reading.

## Lanes

### Manuscript / 01
Read `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`, `state/MANUSCRIPT_WORKFLOW.md`, `state/MANUSCRIPT_STATE.md`, `state/OPEN_THREADS.md`, the current manuscript edge, and `state/PROSE_PLAYBOOK.md` when present. Use `state/STORY_NORTH_STAR.md` as durable artistic direction. Consult `state/STORY_ANTI_PATTERNS.md` when a chapter choice risks a known recurring failure mode. Consult character/setting/plot/development files only when useful. Preserve throughput.

01 is intentionally chat-independent. Previous chat history may help but is never required authority. A fresh worker must reconstruct the current endpoint and next executable chapter from current GitHub state. For normal accepted forward production, treat one complete chapter as one durable transaction: draft, validate, update the permanent manuscript and relevant living state, store the next trailhead in `MANUSCRIPT_STATE.md`, commit, verify current `main`, then advance.

`Queue N Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.` is a valid bounded composition of normal Manuscript Engine transactions. Follow the full queue semantics and limits in `state/MANUSCRIPT_ENGINE_PLAYBOOK.md`: each pass must cross its own durable boundary and re-read the newest GitHub edge before the next pass begins. The queue is disposable execution control, not a second manuscript state system.

If chat history or a prompt claims a chapter exists but GitHub ends earlier, stop forward numbering and recover exact durable prose first if it exists. Never fabricate a missing chapter from summaries or chat residue.

### Writers' Room / 02
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/WRITERS_ROOM_STATE.md`, and relevant specialist brains. Consult `state/STORY_ANTI_PATTERNS.md` when an exploration risks a known recurring failure mode. Explore alternatives, research real practice when useful, translate research into behavior/social/work possibilities, update durable residue, and hand developed possibilities to 03. Do not canonize exploration.

### Story Control / 03
Read current manuscript/state plus `state/STORY_NORTH_STAR.md`, `state/DEVELOPMENT_CYCLE.md`, `state/STORY_CONTROL_STATE.md`, `state/WRITERS_ROOM_STATE.md`, `state/PLOT_CONTROL.md`, `state/OPEN_THREADS.md`, and relevant research/bibles. Consult `state/STORY_ANTI_PATTERNS.md` when pressure-testing a direction that risks a known recurring failure mode. Pressure-test possibilities against canon/rhythm/long-range direction, classify them, graduate only useful durable residue, and send focused research edges back to 02.

### Prose / editorial / 04
Read actual prose plus `state/PROSE_PLAYBOOK.md` and `state/STORY_NORTH_STAR.md`. Consult `state/STORY_ANTI_PATTERNS.md` when an edit risks flattening voice, relationships, evidence discipline, or serial texture. Improve writing and longitudinal social texture without silently changing plot, canon, characterization, scene intent, or outcomes.

Before starting a broad dialogue, attribution, compression, PERFORMANCE, or other specialist editorial pass, cheaply inspect current durable WIP for a narrower live owner: open PRs, named active branches, and explicit specialist trailheads. When task wording matches a live specialist pass, continue or review that owner instead of silently starting a duplicate generic-04 pass. If no narrower live owner exists, 04 remains the default editorial route.

Active specialist WIP does **not** automatically become a permanent root lane or mandatory boot context. Discover it when the task enters its jurisdiction; keep unrelated specialist state cold.

`state/GENERAL_EDITOR_STATE.md` is preserved on demand as **REFERENCE / CASE LAW** for the completed Chapters 1–5 moderate-polish batch, its Level 1–3 craft boundary, continuity repairs, and the Book 1 source-promotion path. It is not a separate active lane or sequential queue. Route current prose/editorial work through 04 unless another current specialist pass explicitly owns the task.

For an explicitly authorized **structural compression pass**, current illustrations, illustration candidates, chapter numbers, and paragraph anchors are advisory production state only. Do not preserve weak/redundant prose, a redundant scene, or an old chapter boundary merely because art exists or is planned there. If a visually strong beat still earns its place, preserve the beat because the story needs it, not because the art system does. Visual candidates are reconciled after the manuscript edit.

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

If `state/visual/PRODUCTION_HOLD.json` says an active `structural_edit_hold`, do **not** generate new art or automatically promote approved art into reader prose. Preserve scene-candidate intent, treat chapter/title/paragraph-anchor placement as provisional, and use `state/visual/ILLUSTRATION_RECONCILIATION_REPORT.md` after the structural edit to explicitly remap, retire, or replace drifted candidates before production resumes.

### Greg, Again Audio
Read `r2/PIPELINE.md` and `r2/AUDIO_PRODUCTION.md`, then resolve current audio publication, written frontier, active audio branches/PRs, and the exact source surface needed for the claimed chapter.

If no chapter was explicitly assigned, auto-claim the earliest available free written/unpublished chapter using `r2/AUDIO_PRODUCTION.md` **before voice synthesis**. Audio ownership is one chapter per worker. Scan past occupied unfinished chapters rather than treating the audio frontier as contiguous. Legacy multi-chapter branch names do not blanket-reserve unstarted sibling chapters; durable chapter-specific WIP does. Preserve already-generated provider work, never steal real chapter-specific work, never claim beyond written authority, and reconcile shared manifests/catalogs against newest GitHub state before publication.

Forward Greg, Again audio production must follow the chapter-tail finishing rule in `r2/AUDIO_PRODUCTION.md`: the final listener-facing chapter should end with about 2 seconds of silence after the last spoken word. Apply that silence at chapter assembly only, not at internal take seams. This is a forward-production default and does not require retroactive repair of already-published chapters unless an ending is actually abrupt or a separate repair is authorized.

### Reader / UI
Read `state/READER_DESIGN_LAB.md`, visual guidance, current reader files, and current project authority. Use a branch for broad changes. Never rewrite prose as a presentation side effect. When showcase curation is active, use `publishing/showcase_chapters.json` and generated showcase numbering for public ordering while preserving canonical file paths and art identity.

### Publishing / repository integration
Prefer small legible commits. Reconcile in favor of newer authority. Never restore stale whole-file versions over newer work. Showcase curation changes public presentation only; never apply a showcase hide decision as a manuscript deletion.

## R2 future survivor evidence

For forward R2 narrative work, `r2/FUTURE_SURVIVOR_PROTOCOL.md` defines how to discover and use surviving temporal experiment material when it exists. Treat survivor branches as optional challenger/rehearsal evidence, never accepted story authority or a mandatory outline. Read current `main` first. If relevant survivor evidence is missing, stale, conflicting, or inaccessible, continue normal R2 production from accepted authority.

## GitHub workflow

Use:

**CHAT = disposable thinking**

**BRANCH = durable WIP / broad or risky work**

**MAIN = accepted authority / small atomic completed work**

Avoid finished work existing only in chat or a mystery local file.

### Chat / Codex execution split

Chat is the preferred surface for creative direction, taste, architecture, and new doctrine.

For an explicitly approved bounded bulk job, Codex campaign mode is an execution policy, not a lane. Read `state/editorial/CODEX_EXECUTION_POLICY.md`, use the existing compiler/index/campaign tools, prefer deterministic and cache-valid work, do not widen scope, keep parallel workers derived-only, serialize canon integration, and halt once the requested durable boundary verifies.

AI-facing PLG operations live in `scripts/plg_ai_tools.py`; the optional MCP adapter is `scripts/plg_mcp_server.py`. Do not rediscover file layout manually when these tools can compile, resolve, query, reduce, or execute the needed state.

### GitHub-first handoff

When current project authority is already in GitHub, do not create or request a full repository ZIP merely to move work between chats or agents.

Normal handoff:

**READ CURRENT GITHUB → WORK → VALIDATE → UPDATE DURABLE STATE → COMMIT / MERGE → VERIFY → LEAVE COMPACT TRAILHEAD**

Use a small targeted attachment only when required work is intentionally absent from GitHub, such as the living heavy-edit manuscript, a genuinely unique source asset, an exact missing recovery block, or a user-requested offline archive. Full-project ZIPs are exceptional recovery artifacts, not routine checkpoints.

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
- `Queue 5 Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.`
- `Continue Peg-Leg Greg Writers' Room from current GitHub authority.`
- `Continue Peg-Leg Greg Story Control from current GitHub authority.`
- `Continue Peg-Leg Greg as 04 — Heavy Prose Editor from current GitHub authority.`
- `Continue Peg-Leg Greg as 05 — Visual Production / Image Lab from current GitHub authority.`
- `Continue Peg-Leg Greg Reader / UI from current GitHub authority.`
- `Continue Greg, Again audio production from current GitHub authority.`

Do not paste a giant lane prompt into every replacement chat unless a genuinely new requirement is not yet represented in GitHub. When a lane's operating rules are durable in repo state, the short starter is preferred.
