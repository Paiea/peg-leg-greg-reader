# Codex Campaign Execution Policy

Codex campaign mode is an execution policy over existing PLG lanes and tools. It is not a new editorial lane.

## Hard usage budget

Codex is an expensive technical intervention, not the default production worker.

Default budget for a new problem is **zero Codex tasks**.

Before invoking Codex, prefer in this order:

1. deterministic repository code and GitHub Actions
2. direct Chat/Mana reasoning and available plugins/connectors
3. existing scripts, recipes, and verified workflows
4. one bounded Codex intervention only when the remaining problem genuinely needs repo-native engineering judgment or implementation

When Codex is justified:

- use one primary agent
- use zero subagents by default
- do not use Best-of-N or duplicate speculative attempts
- allow at most one retry for the same bounded failure, and only after identifying a concrete reason the first attempt failed
- after that retry, stop and return control to Chat/Mana instead of spending more allowance
- a second distinct Codex task requires a fresh Mana decision; never chain adjacent improvements automatically
- recurring production loops must not invoke Codex automatically

Enforce the budget by task count rather than guessed token or allowance percentages when no authoritative live usage meter is available.

Prefer Codex work that either:

- removes Codex from future recurring work by creating or repairing deterministic infrastructure, or
- delivers a high-value one-off technical result that cannot be obtained more cheaply through Chat, plugins, or existing code

## Default behavior

1. Execute the approved bounded job. Do not redesign the project.
2. Use deterministic repository tools before model reasoning.
3. Reuse valid compiler/campaign cache before launching workers.
4. Do not widen chapter scope, task scope, or editorial authority.
5. Do not invent new story doctrine, systems, lanes, or adjacent cleanup work.
6. Parallel workers may produce derived analysis and candidates only when parallelism is explicitly authorized. They do not mutate canon.
7. Canon writes are serialized through the existing validated integration path.
8. Retry ordinary worker failure at most once and only inside the same bounded target.
9. Do not use duplicate attempts or Best-of-N by default.
10. Return schema-bound results instead of long recaps.
11. Escalate material authority/design conflicts instead of improvising around them.
12. Halt when the requested durable boundary is verified.
13. Leave compact reusable operational residue when a first-of-kind technical method was discovered. Preserve the transferable mechanism, not chain-of-thought.

Chat remains the preferred surface for creative direction, taste, architecture, routing, and approval of new doctrine. Creative Codex work is allowed only when the task explicitly authorizes it.

No campaign mechanism may bypass authentication, subscription, quota, credit, sandbox, or permission boundaries.
