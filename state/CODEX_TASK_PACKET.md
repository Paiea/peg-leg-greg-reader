# Mana -> Codex Task Packet

Use this packet when Chat/Mana has already decided what Codex should implement or audit.

The packet is intentionally small. It should contain only enough project context to let one strong Codex agent solve the selected target safely.

## Default

`PARALLELISM: NO`

`RESIDUE: COMPACT`

One primary Codex agent owns the task. Do not spawn subagents unless `PARALLELISM` is explicitly changed to `YES` and the packet explains what independent work may be delegated.

`RESIDUE` controls how much reusable method the agent leaves behind:

- `NONE` - ordinary obvious implementation; return only evidence.
- `COMPACT` - default; if a transferable method was discovered, return a short recipe.
- `DURABLE` - first-of-kind or strategically reusable work; update the owning lane/playbook with the proven method after verification. Prefer updating an existing doc over creating a new one.

Do not manufacture documentation when the task taught us nothing reusable.

## Template

```text
TARGET
<One concrete user-visible or system-visible outcome, or one bounded audit question.>

WHY THIS TARGET
<Why this is currently the highest-leverage change. Keep short.>

AUTHORITY
<Exact repo ref/files/docs/behavior that own the task. Do not list unrelated project context.>

REUSE
<Existing components, scripts, libraries, patterns, APIs, or external conventions to reuse.>

BOUNDARY
<What must not be redesigned, refactored, or expanded into.>

IMPLEMENT
<Give the primary agent freedom to inspect/edit/debug/test whatever is required inside the boundary. State any non-negotiable behavior. For an audit, analyze and return recommendations rather than mutating code unless implementation is explicitly authorized.>

VERIFY
<Concrete evidence proving the target works or the audit is grounded: tests, build, screenshots, routes, state checks, deployment behavior, exact repository evidence, etc.>

PARALLELISM
NO

RESIDUE
COMPACT

STOP
<When VERIFY passes, stop. Return evidence, reusable residue if earned, and newly discovered constraints to Chat/Mana. Do not continue into adjacent improvements.>
```

## Expert residue

When `RESIDUE` is `COMPACT` or `DURABLE` and the work reveals a genuinely reusable method, leave a small expert handoff that lets Chat/Mana reproduce the pattern later without paying Codex to rediscover it.

Use this shape:

```text
REUSABLE RECIPE
Problem class: <when this pattern applies>
Pattern: <the compact solution>
Use: <exact files / commands / sequence / components worth copying>
Why it worked: <the important mechanism, not a long recap>
Do not use when: <boundary / failure mode>
Next reuse: <where else this could plausibly apply, if obvious>
```

Keep it compact. The goal is transferable method, not a transcript of the agent's reasoning.

For `RESIDUE: DURABLE`, write the proven recipe into the smallest existing authoritative lane/playbook that future workers will naturally read. Do not create a new doctrine file when an existing owner can hold the rule cleanly.

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

## Operating loop

`Mana frames -> Codex audits/builds -> Codex verifies -> Codex leaves compact expert residue -> Mana decides whether the pattern should be reused -> next bounded shot`

This is how Codex becomes an expert we can call for a hard piece, learn from once, and reuse later instead of repeatedly paying for the same discovery.
