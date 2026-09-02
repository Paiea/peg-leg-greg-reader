# Single-Chat Manuscript Engine Design

## Goal

Make 01 / Manuscript Engine fully reconstructible from GitHub so one long-running chat can produce chapter after chapter, while any fresh replacement chat can resume with only a tiny starter prompt.

## Core model

- Chat is disposable execution context, never the project brain.
- `state/manuscript/Peg_Leg_Greg_Running_Manuscript.md` is exact forward prose authority.
- `state/MANUSCRIPT_STATE.md` is the current bookmark: endpoint, durable residue, protected uncertainty, and next executable trailhead.
- `state/MANUSCRIPT_ENGINE_PLAYBOOK.md` defines how 01 thinks and validates.
- `state/MANUSCRIPT_WORKFLOW.md` defines the file/commit loop.
- GitHub `main` is the completion boundary for normal accepted forward chapters.

## Per-chapter transaction

For normal forward production, one chapter is both the writing unit and the durable shipping unit:

1. Re-read current `main` and core 01 files.
2. Read exact recent prose and the current trailhead.
3. Write one complete chapter.
4. Run the light prose/continuity pass.
5. Validate length, em-dash status, title, endpoint, numerical continuity, and protected uncertainties.
6. Append the exact chapter to the permanent running manuscript.
7. Update only living state/index/thread files whose answers actually changed.
8. Write the next executable chapter trailhead into `MANUSCRIPT_STATE.md`.
9. Commit the complete chapter transaction to `main` when authorized.
10. Re-read the resulting `main` endpoint before reporting success.

A draft that exists only in chat is WIP, not a completed chapter.

## Recovery rule

If chat history, a prompt, or a user recollection claims Chapter N exists but current GitHub authority ends at N-1, do not silently draft N+1. Search durable branches/checkpoints for exact N. If exact N exists, integrate/recover it first. If it does not, report the synchronization gap. Never reconstruct missing exact prose from summary residue.

## Fresh-chat behavior

A fresh Manuscript Engine chat must be able to start from:

`Continue Peg-Leg Greg Manuscript Engine from current GitHub authority.`

The worker discovers the current chapter, exact edge, constraints, and next trailhead from GitHub. Previous chat history may help but must not be required.

## Chat handoff

After a successful chapter, the user-facing receipt should be compact: chapter/title, verification result, commit SHA, and confirmation that the next trailhead is durable. A giant chapter-specific re-prompt is optional, not required, when the durable trailhead already contains the steering information.

The generic restart prompt remains visible for human convenience.

## Lane boundaries

This architecture applies to 01 forward manuscript production. Writers' Room, Story Control, editorial, visual, reader/UI, research, and cleanup remain separate lanes with their own state and gates. 01 may consult their accepted durable outputs but must not absorb all lane responsibilities into the writing chat.

## Success criteria

- One Manuscript Engine chat can repeatedly continue chapter production using `Continue` or `Next chapter` after a successful commit.
- A brand-new chat can reconstruct the same next task from GitHub without a giant handoff prompt.
- No completed chapter can be lost merely because a chat dies.
- A mismatch between chat history and GitHub authority stops forward numbering rather than creating invented continuity.
- Normal forward chapters no longer sit uncommitted across a 3-5 chapter batch by default.
