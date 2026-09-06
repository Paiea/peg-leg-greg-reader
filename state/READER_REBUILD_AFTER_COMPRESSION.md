# PEG-LEG GREG — READER REBUILD AFTER COMPRESSION

Purpose: define how the public reader should be rebuilt after structural compression without breaking navigation, acts, art placement, or legacy links.

## Separation rule

Structural manuscript editing and public-reader migration are separate phases.

Do not update public chapter numbering while the structural map is still changing.

## Reader rebuild inputs

The publication rebuild should consume:
- ordered active stable chapter IDs;
- current titles;
- current book/act assignments;
- current display numbering;
- current slugs;
- legacy aliases;
- illustration bindings;
- compression batch manifests;
- public-reader configuration/manifest files.

## Rebuild sequence

1. Freeze approved structural region.
2. Generate current ordered active chapter IDs.
3. Assign sequential display numbers.
4. Recalculate book/act boundaries only from approved structure.
5. Generate current chapter slugs/routes.
6. Generate previous/next navigation from stable ordering.
7. Resolve illustration bindings through stable chapter IDs.
8. Build legacy alias/redirect table.
9. Rebuild chapter index/table of contents.
10. Validate all public chapter links and asset placements.
11. Preview before publishing.
12. Publish only when validation is clean.

## Legacy links

Old chapter-number URLs should resolve deliberately after renumbering.

Preferred outcomes:
- redirect/alias to same surviving stable chapter;
- redirect to merged destination;
- redirect to nearest canonical destination with explicit migration record when original chapter was cut.

Do not silently send every missing old chapter to the homepage.

## Acts and books

Act/book boundaries are presentation structure and may move during compression, but only after narrative review.

Do not mechanically preserve old boundaries if merged/cut material changed the governing movement.

Do not mechanically regenerate new acts solely because chapter counts changed.

## Reader art

The reader should ask:

`What art currently belongs to this stable chapter/story beat?`

not:

`What files have ch187 in the filename?`

Filename legacy may remain during transition, but resolver logic should own placement.

## Validation gates

Before publishing, verify:
- no duplicate display numbers;
- no skipped active chapter in navigation;
- every previous/next link resolves;
- every book/act index points to active chapters;
- every active public illustration resolves;
- legacy aliases resolve without loops;
- current canonical URLs resolve directly;
- no cut chapter appears as a live table-of-contents entry;
- merged source chapters do not render duplicate prose;
- titles match surviving canonical prose.

## Preview requirement

Major renumber migrations should produce a preview/staging report before live publication.

The report should summarize:
- old -> new number changes;
- merged/cut chapters;
- moved art;
- changed act boundaries;
- legacy aliases;
- unresolved warnings.

## Final principle

The reader is a projection of manuscript authority.

Do not make manuscript structure conform to brittle reader numbering merely because that numbering already exists.
