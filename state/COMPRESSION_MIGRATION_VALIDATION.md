# PEG-LEG GREG — COMPRESSION MIGRATION VALIDATION

Purpose: define the final validation layer that must pass before a compressed/renumbered manuscript region can become accepted publishing authority.

## Validation domains

Every structural migration should validate six domains:

1. manuscript structure;
2. continuity;
3. chapter identity;
4. illustrations/assets;
5. public reader/navigation;
6. historical aliases/audit trail.

## Manuscript structure checks

Verify:
- every active chapter appears exactly once in current order;
- no merged source prose is duplicated unintentionally;
- no cut chapter remains as a live canonical chapter;
- titles remain attached to the correct surviving prose;
- chapter boundaries read naturally after merges;
- preceding/following chapter transitions still work;
- act/book placement matches actual story movement.

## Continuity checks

Verify affected ranges for:
- money/debt changes;
- magic evidence/counts;
- injuries/recovery;
- object ownership/provenance;
- promises/contracts/referrals;
- relationship-state progression;
- jokes/nicknames/callbacks;
- location familiarity;
- reputation propagation;
- time passage.

A structurally cleaner manuscript that breaks earned continuity fails validation.

## Identity checks

Verify:
- stable IDs are unique;
- active IDs resolve to one canonical manuscript unit;
- merged/cut IDs retain historical status;
- source relationships are recorded;
- no display number is being used as the only durable foreign key;
- redirects contain no cycles.

## Illustration checks

Verify:
- every public asset resolves to a valid stable placement;
- art from merged/cut chapters has an explicit migration decision;
- character-reference authority remains intact where appropriate;
- no image silently follows a chapter number to the wrong prose;
- illustration order still matches scene order when multiple images exist;
- act/book art remains attached to the intended narrative unit.

## Reader checks

Verify:
- table of contents matches current active order;
- previous/next navigation is complete;
- canonical routes resolve;
- legacy aliases resolve;
- no dead chapter links in generated index;
- no duplicate chapter pages;
- books/acts open at correct chapters;
- illustrated/unillustrated variants resolve the same chapter identity.

## Audit-trail checks

Verify:
- compression manifest exists;
- approval/revision history is recorded;
- old-to-new mapping exists when numbering changed;
- art migration ledger is updated;
- legacy alias table is generated;
- pre-compression Git authority is recoverable by commit.

## Reader-experience smoke test

After mechanical checks, read the compressed span in sequence.

Ask:
- Does time still feel lived?
- Do relationships still feel earned?
- Did a joke appear before its origin?
- Did an object appear without acquisition?
- Did Greg's competence/body/magic jump unnaturally?
- Does a location become familiar too quickly?
- Does compression feel invisible to a new reader?

Mechanical validity is necessary but not sufficient.

## Failure policy

If any high-risk validation fails:
- do not publish the migration;
- keep current accepted reader authority unchanged;
- repair on structural/editor branch;
- rerun validation.

Do not patch live output manually in a way that diverges from registry/manifests.

## Completion standard

A migration is complete only when:

**the manuscript, stable identities, illustrations, reader, redirects, and continuity all describe the same book.**
