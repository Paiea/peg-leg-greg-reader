# R2 Chapter Title Policy

Status: **ACTIVE AUTHORITY ON ACCEPTANCE**

R2 chapter titles are embodied Greg-role titles.

## Core question

Every selected/public R2 chapter title must answer:

> **Who is Greg in this chapter?**

A valid title may name:

- an occupation or paid function
- a social position
- a temporary job or assigned function
- a relational role
- a situational identity
- a clean metaphorical role Greg actually inhabits

A title fails when it mainly names:

- an object
- an event
- a place
- a time span
- an abstraction
- a problem
- a chapter topic
- a role that materially belongs to somebody other than Greg

Duplicate roles are allowed. A broad role is allowed when it is true. Do not invent awkward occupational nouns merely to satisfy the pattern.

The test is semantic, not grammatical. `Ward Hand` is a valid role title even without `The`. `The First Customer` fails when the customer is somebody else.

## Identity boundary

Title wording never owns chapter identity.

Stable identity is:

- `r2-chNNN` for the R2 chapter
- `ga-NNN` for Greg, Again audio
- numeric chapter number for cross-surface reconciliation

A title may change without changing any of those identities.

A title-only change must not imply that existing audio is missing, stale, unowned, or in need of regeneration.

## Selected written authority

Working story-search, rehearsal, or development titles may remain provisional.

Once a chapter is selected for public R2, the first-line selected written heading is the semantic title authority:

```text
# Chapter N: <role title>
```

That selected role title propagates by stable chapter number to:

1. `r2/data/chapters/chNNN.json`
2. `r2/data/chapter-registry.json` when that production-registry entry exists
3. `greg-again/audio/manifest.json` when an audio entry exists
4. Listen / Read chapter lists and future divider-card metadata

The public chapter manifest is the site-facing display surface. The production registry may trail the public frontier and does not get to restore an older title merely because its coverage is partial.

Downstream surfaces do not independently invent competing chapter titles.

## Editorial judgment vs mechanical synchronization

Choosing the role title is editorial judgment. Read the actual selected chapter and decide what Greg materially embodies.

Mechanical tooling only enforces parity after that judgment exists. It must not invent role nouns from chapter text.

Use `r2/TITLE_ROLE_AUDIT.md` for approved decisions and the R2 role-title synchronizer for title parity.

## Change boundary

A role-title migration may change:

- the selected chapter heading
- title metadata on manifests/registries

It may not change merely because of a title update:

- story prose below the heading
- chapter IDs
- numeric chapter numbers
- route paths
- previous/next identity
- MP3 binaries
- take maps
- provider artifacts
- audio ownership
- chapter publication status

## Forward rule

Before a selected chapter is published, ask:

> **Does this title name who Greg is being, rather than merely what happens?**

If not, choose the role before publication.

This is a publication gate, not a request to periodically polish already-valid role titles.