# Mana -> Codex Task Packet

Use this packet when Chat/Mana has already decided what Codex should implement.

The packet is intentionally small. It should contain only enough project context to let one strong Codex agent solve the selected target safely.

## Default

`PARALLELISM: NO`

One primary Codex agent owns the task. Do not spawn subagents unless this field is explicitly changed to `YES` and the packet explains what independent work may be delegated.

## Template

```text
TARGET
<One concrete user-visible or system-visible outcome.>

WHY THIS TARGET
<Why this is currently the highest-leverage implementation change. Keep short.>

AUTHORITY
<Exact repo ref/files/docs/behavior that own the task. Do not list unrelated project context.>

REUSE
<Existing components, scripts, libraries, patterns, APIs, or external conventions to reuse.>

BOUNDARY
<What must not be redesigned, refactored, or expanded into.>

IMPLEMENT
<Give the primary agent freedom to inspect/edit/debug/test whatever is required inside the boundary. State any non-negotiable behavior.>

VERIFY
<Concrete evidence proving the target works: tests, build, screenshots, routes, state checks, deployment behavior, etc.>

PARALLELISM
NO

STOP
<When VERIFY passes, stop. Return evidence and newly discovered constraints to Chat/Mana. Do not continue into adjacent improvements.>
```

## Parallelism exception

When `PARALLELISM: YES`, add:

```text
PARALLEL WORK
<Enumerate independent sidecar tasks and their ownership boundaries.>

INTEGRATION
<State how results are reconciled and which writes must remain serialized.>
```

Do not authorize parallelism for one coherent investigation, overlapping edits, architecture discovery, or product/design uncertainty.

## Quality bar

A good packet makes Codex's question narrow while leaving Codex's technical execution strong.

Bad:

`Make R2 better.`

Good:

`Fix only the R2 mobile hero cropping and hierarchy. Preserve navigation, audio player, reader architecture, and chapter behavior. Reuse the current component/style system. Verify representative mobile and desktop widths. Stop after the hero.`

The goal is not microscopic tasks. The goal is one coherent battlefield at a time.
