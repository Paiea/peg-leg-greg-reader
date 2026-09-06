# PEG-LEG GREG — ILLUSTRATION STABLE BINDING SPEC

Purpose: bind illustrations to durable story identity rather than fragile display chapter numbers.

## Core rule

Illustrations should bind primarily to:
- stable `chapter_id`;
- optional stable `beat_id` or scene descriptor;
- asset identity.

Display chapter number is presentation metadata only.

## Why

Structural compression may:
- merge chapters;
- cut chapters;
- move a surviving scene;
- renumber hundreds of later chapters;
- change act boundaries.

The art pipeline should not interpret those changes as every downstream image becoming orphaned.

## Recommended art binding record

Each illustration asset should support:
- `asset_id`
- `chapter_id`
- optional `beat_id`
- `scene_summary`
- `characters`
- `status`
- `current_display_number` generated at publish time
- `source_display_number` historical only
- `placement`
- `reference_role`
- `migration_history`

## Placement values

Suggested placement classes:
- `chapter_inline`
- `chapter_lead`
- `act_lead`
- `book_lead`
- `gallery`
- `archive`

## Compression behavior

### Chapter survives
Keep asset bound to same stable chapter ID unless the represented beat moved.

### Chapter merges into another
If the depicted beat survives in destination chapter:
- move the binding to destination chapter ID;
- retain source ID in migration history;
- preserve asset approval/reference quality.

If the depicted beat does not survive:
- assess gallery/archive/replacement;
- do not automatically delete the asset.

### Chapter is cut
Art does not grant chapter immunity.

Choose explicitly:
- rebind to destination containing surviving beat;
- convert to act/book/gallery placement;
- archive;
- regenerate if the new structural scene needs different art.

## Character reference protection

An image may be valuable as character-reference authority even if its original chapter disappears.

Structural compression must not accidentally demote a strong approved character reference merely because the associated chapter was merged/cut.

Keep character-reference registry identity independent from public chapter placement.

## Beat IDs

Future tooling may assign optional stable beat IDs for illustrated moments, especially where art is expensive or heavily referenced.

Example:

`plg-beat-greg-first-stage-bow`

Do not require beat IDs for every scene. Use them where stable scene-level attachment materially reduces migration ambiguity.

## Publication resolution

At build time:
1. resolve asset -> stable chapter ID;
2. resolve chapter ID -> current display number/slug/act;
3. render placement;
4. preserve legacy metadata only for redirects/history.

## Validation

Reject publication when:
- active chapter art references nonexistent chapter ID;
- an asset marked public has no resolvable placement;
- two conflicting migration destinations exist;
- a cut chapter still owns active inline art without an explicit migration decision;
- stable character references were lost through chapter renumbering alone.

## Final principle

**Art belongs to story moments and character continuity, not to a fragile integer.**
