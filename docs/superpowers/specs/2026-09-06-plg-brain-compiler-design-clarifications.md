# PLG Brain Compiler Design Clarifications

This file is a normative clarification to `2026-09-06-plg-brain-compiler-design.md` produced during spec self-review. It does not widen the approved feature scope.

## Authority inputs

The deterministic compiler must never infer accepted project authority from the currently checked-out feature branch.

`compile_brain(...)` accepts explicit optional `authority_branch` and `authority_sha` inputs.

Defaults:

- `authority_branch` defaults to the registry project's `authority` value, currently `main`.
- `authority_sha` may be omitted. When omitted, output uses `null` and adds a routing warning that the exact accepted authority SHA was not supplied.
- An optional GitHub snapshot may supply `authority_sha`; if both explicit input and snapshot are present and disagree, compilation emits a warning and the Doctor reports a conflict.

The compiler performs no `git` or network call merely to fill an authority SHA.

## Registry relations

Document entries may include:

```json
{
  "dependencies": [
    {"path": "state/STORY_NORTH_STAR.md", "temperature": "conditional"}
  ]
}
```

Allowed dependency temperatures are `hot` and `conditional`. A dependency path must also be a registered document. Circular dependencies are invalid registry state.

Dependencies are routing relationships only. They do not express authority precedence.

## Exclusive workstream ownership

The registry may define:

```json
{
  "exclusive_task_tags": ["dialogue-owner", "manuscript-owner"]
}
```

A workstream may claim ownership tags through:

```json
{
  "owner_tags": ["dialogue-owner"]
}
```

The Doctor reports an `error` when more than one `ACTIVE` durable workstream claims the same tag listed in `exclusive_task_tags`.

Task tags and owner tags are separate concepts. Task tags control relevance. Owner tags control collision detection.

## Unregistered-file discovery

The Doctor must not treat every Markdown file under `state/` as equally likely brain input.

The registry may define:

```json
{
  "discovery": {
    "include_globs": ["state/*.md", "state/editorial/*.md"],
    "ignore_globs": ["state/manuscript/**", "state/editorial/performance-roundtrip/**", "state/editorial/performance-production/**"]
  }
}
```

Unregistered discovery is advisory only. It returns a bounded deterministic list, default maximum 25 paths, sorted lexically.

Binary artifacts, generated campaign/cache outputs, manuscript checkpoint directories, exact prose archives, and other known content stores should be excluded by registry ignore globs rather than individually registered as brain documents.

## HOT ceiling behavior

The hard HOT ceiling remains 12 pointers. If compilation would exceed it, compilation fails closed with an explicit error naming the task and candidate count. The compiler must not silently truncate HOT context because silent truncation could hide required authority.

Conditional/cold display lists may be deterministically truncated to configured presentation limits, with counts included in output.

## Canonical JSON

Determinism tests compare canonical JSON generated with:

```python
json.dumps(packet, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
```

No timestamps, random IDs, filesystem mtimes, or unordered traversal results may appear in packet or Doctor output.
