# PEG-LEG GREG — HANDSHAKE PROTOCOL

Goal: make workers disposable while continuity survives in GitHub.

## Three states

1. **CHAT / THINKING** — exploratory, disposable, not authority.
2. **GITHUB BRANCH / WIP** — durable and inspectable, but not authoritative main.
3. **MAIN / ACCEPTED AUTHORITY** — finished/accepted project state.

Avoid a fourth category of important finished work trapped only in a chat or mystery local file.

## GitHub-first transfer rule

Do not package or request the full repository as a ZIP for an ordinary chat-to-chat or agent-to-agent handoff when current authority is already in GitHub. A later worker should reconstruct its lane from current `main`, `AGENTS.md`, relevant durable state, exact source authority, and any named branch or PR.

External transfer remains legitimate for a targeted artifact that GitHub intentionally does not hold: active editorial work, unique binary/source art, an exact missing recovery block, or a deliberate offline archive. Transfer only that artifact, not another copy of the entire project.

## GitHub as re-prompt

GitHub cannot by itself force a random future chat to wake up and continue. But it can make the human prompt extremely small.

Desired handshake:

**WORKER A → works/validates → updates GitHub → leaves NEXT_TASK/trailhead → WORKER B reads GitHub → continues**

The re-prompt should point to repository instructions rather than restating the whole project.

## End-of-run behavior

For substantial work:
1. finish or checkpoint work in GitHub
2. update only relevant durable state
3. verify current branch/main and changed files
4. record unresolved risk or next executable edge
5. store the lane's durable re-prompt / trailhead where that lane uses one
6. provide one compact copyable restart prompt visibly in chat unless the user asked for no next-step prompt

For broad/risky unfinished work, commit to a named branch so another worker can inspect it.

## Manuscript / 01 special rule

Forward manuscript production is intentionally chat-independent.

For normal accepted production, one complete chapter is one durable transaction. `MANUSCRIPT_STATE.md` carries the chapter-specific next trailhead. After Chapter N is validated, written to the permanent manuscript, state is updated, the transaction is committed, and current `main` is verified, the same chat may immediately continue to N+1. A fresh replacement chat must be able to do the same from GitHub without needing the old conversation.

If chat history says Chapter N happened but GitHub ends at N-1, do not write N+1. Search durable WIP for exact N and recover it if possible. Otherwise report the synchronization gap. Never rebuild missing exact prose from summaries.

A giant chapter-specific prompt in chat is therefore optional when the durable trailhead is complete.

## NEXT_TASK convention

When a lane needs an explicit durable trailhead, add/update a compact `NEXT_TASK` section in that lane's existing state/playbook file rather than creating endless handoff files.

It should answer:
- what is the next useful job?
- what authority must be read first?
- what must not be damaged?
- branch or main?

Current state always outranks an old NEXT_TASK.

For Manuscript / 01, `MANUSCRIPT_STATE.md` is the normal home for the next executable chapter trailhead.

## Minimal universal re-prompt

> Continue Peg-Leg Greg from current GitHub authority. Inspect current `main`, read `state/PROJECT_STATE.md` and the relevant lane playbook/state, then execute the current durable NEXT_TASK. Preserve newer authority. Work in GitHub, validate, update durable state, and leave the next handshake.

## Manuscript re-prompt

> Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.

That compact prompt is intentionally sufficient. The worker must discover the current endpoint, exact prose edge, constraints, and next trailhead from GitHub.

## Reader / UI re-prompt

> Continue Peg-Leg Greg reader work from GitHub. Read project authority plus `state/READER_DESIGN_LAB.md` and visual guidance. Use a branch for broad changes. Preserve manuscript prose and newer art/UI work. Validate, update durable design state, and leave the next handshake.

## Visual re-prompt

> Continue Peg-Leg Greg visual production from GitHub. Read `state/VISUAL_BIBLE.md` and `state/IMAGE_PRODUCTION.md`, inspect actual reader coverage and authoritative manuscript scenes, execute the next coverage batch, integrate accepted art, validate, update durable state, and leave the next handshake.

## Human-light workflow

The human should increasingly be able to say only:
- `continue manuscript`
- `continue reader`
- `continue images`
- `continue story control`
- or simply `continue the highest-value Peg-Leg Greg work`

Within an already-running Manuscript Engine chat, `Continue` or `Next chapter` is enough after the prior chapter has been durably committed and verified.

The worker is responsible for discovering current state from GitHub.

## Limitation

Repository state can preserve and route work, but a normal chat does not autonomously launch another chat merely because a commit exists. The practical solution is tiny deterministic re-prompts. Continuity must not depend on autonomous wake-up.
