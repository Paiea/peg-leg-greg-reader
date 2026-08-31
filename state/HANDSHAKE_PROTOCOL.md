# PEG-LEG GREG — HANDSHAKE PROTOCOL

Goal: make workers disposable while continuity survives in GitHub.

## Three states

1. **CHAT / THINKING** — exploratory, disposable, not authority.
2. **GITHUB BRANCH / WIP** — durable and inspectable, but not authoritative main.
3. **MAIN / ACCEPTED AUTHORITY** — finished/accepted project state.

Avoid a fourth category of important finished work trapped only in a chat or mystery local file.

## GitHub-first transfer rule

Do not package or request the full repository as a ZIP for an ordinary
chat-to-chat or agent-to-agent handoff when current authority is already in
GitHub. A later worker should reconstruct its lane from current `main`,
`AGENTS.md`, relevant durable state, exact source authority, and any named
branch or PR.

External transfer remains legitimate for a targeted artifact that GitHub
intentionally does not hold: active editorial work, unique binary/source art,
an exact missing recovery block, or a deliberate offline archive. Transfer only
that artifact, not another copy of the entire project.

## GitHub as re-prompt

GitHub cannot by itself force a random future chat to wake up and continue. But it can make the human prompt extremely small.

Desired handshake:

**WORKER A -> works/validates -> updates GitHub -> leaves NEXT_TASK -> WORKER B reads GitHub -> continues**

The re-prompt should point to repository instructions rather than restating the whole project.

## End-of-run behavior

For substantial work:
1. finish or checkpoint work in GitHub
2. update only relevant durable state
3. verify current branch/main and changed files
4. record unresolved risk or next executable edge
5. store the lane's durable re-prompt / trailhead where that lane uses one
6. provide one compact copyable next prompt visibly in chat

For broad/risky unfinished work, commit to a named branch so another worker can inspect it.

### Visible re-prompt requirement

A GitHub-only re-prompt is not enough for the human handoff.

Unless the user explicitly asks for no next-step prompt, every substantial project run should end with a visible copyable prompt for the work/lane the worker actually recommends next.

If the recommended next lane differs from the current lane:
- keep the current lane's durable restart prompt in GitHub;
- show the cross-lane prompt to the user in chat.

The user should not need to ask `what next?` after a substantial run.

## NEXT_TASK convention

When a lane needs an explicit durable trailhead, add/update a compact `NEXT_TASK` section in that lane's existing state/playbook file rather than creating endless handoff files.

It should answer:
- what is the next useful job?
- what authority must be read first?
- what must not be damaged?
- branch or main?

Current state always outranks an old NEXT_TASK.

## Minimal universal re-prompt

> Continue Peg-Leg Greg from GitHub. Inspect current `main`, read `state/PROJECT_STATE.md` and the relevant lane playbook/state, then execute the current durable NEXT_TASK. Preserve newer authority. Work in GitHub, validate, update durable state, and leave the next handshake.

## Manuscript re-prompt

> Work as the Peg-Leg Greg Manuscript Engine. Inspect current `main`, follow `state/MANUSCRIPT_ENGINE_PLAYBOOK.md` and the manuscript startup sequence, write one chapter from current authority, validate/commit/update state, then leave the next handshake.

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

The worker is responsible for discovering current state from GitHub.

## Limitation

Repository state can preserve and route work, but a normal chat does not autonomously launch another chat merely because a commit exists. The practical solution is tiny deterministic re-prompts. Continuity must not depend on autonomous wake-up.
