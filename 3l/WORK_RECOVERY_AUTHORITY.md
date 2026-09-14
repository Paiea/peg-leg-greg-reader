# 3L WORK RECOVERY AUTHORITY

Status: CURRENT 3L EXECUTION / RECOVERY AUTHORITY

Purpose: keep 3L moving toward a user-visible result when automation, tools, CI, or a specialist path stalls.

## Priority order

1. Canon prose remains correct and durable.
2. The user can read the current written frontier.
3. Verified audio is published when ready.
4. Automation is improved after the user-facing artifact is available.

A lower priority must never block a higher one.

## Two-strike rule

If the same mechanism fails twice with the same class of failure, stop retrying that mechanism in the current task.

Do one of these instead:

- use the simplest independent fallback that produces the requested artifact
- isolate the failing subsystem and continue the unaffected work
- leave a compact durable failure note and move to the next executable boundary

Do not spend repeated turns proving that a broken path is broken.

## Reader independence

Readable prose must never depend on:

- audio completion
- audio worker manifests
- the audio coordinator
- JavaScript fetching manuscript text at runtime
- a successful audio build
- a full frontier rebuild

Each published record page must contain its prose directly in the HTML generated from canon manuscript authority.

The canonical manuscript link remains available as a fallback.

## Audio independence

Audio workers may finish in any order.

The coordinator must process available worker returns incrementally. It may assemble a record only when that record has every required verified capture. Missing workers or incomplete later records must not prevent verification or publication of an earlier complete record.

## Scope recovery

When a task starts expanding into unrelated failures:

- preserve the requested user-facing result first
- record the unrelated issue separately
- do not turn a bounded fix into repository-wide cleanup unless the user asks

## Evidence states

Use these words precisely:

- SOURCE READY: authoritative source exists in GitHub
- BUILT: derived artifact was generated
- VERIFIED: targeted validation passed
- MERGED: accepted on main
- LIVE: public surface was directly confirmed

Never collapse these into "done" unless the requested boundary actually reached the relevant state.

## Continue behavior

When the user says `Continue`:

- resume from the newest proven durable checkpoint
- do not restart discovery that was already completed
- do not ask for information already present in repo authority
- if the previous path is stalled, switch to the documented fallback rather than repeating it
- surface a usable partial result as soon as one exists

## Tool failure behavior

For tool/API failures:

1. retry once only when the failure appears transient
2. if the retry fails the same way, use another available source or path
3. if no alternate path exists, report the exact blocked boundary and continue all unaffected work

Do not loop on the same endpoint, query shape, or workflow inspection.

## User-facing default

When debugging production machinery and a usable story artifact already exists, give the user the story link/output first. Debugging detail is secondary.

Core rule:

**DELIVER THE STORY. THEN IMPROVE THE MACHINE.**
