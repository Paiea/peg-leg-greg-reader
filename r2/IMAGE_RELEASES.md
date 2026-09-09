# R2 IMAGE RELEASES

This file governs consolidation of approved R2 image binaries from ChatGPT Library into large manual handoff releases.

Chapter workers produce small transactions. Release workers package big batches.

## Shared Library source

```text
/Peg-Leg Greg Image Integration/R2/
  00 Canon/
  01 Incoming/
  02 Approved/
  03 Releases/
  04 Released/
```

GitHub remains authority for story, claims, manifests, intended repository paths, and integration state. Library is the binary warehouse.

## Release trigger

Create a release when Keoni asks or when enough approved unreleased art has accumulated that a large handoff is useful.

A normal target is roughly **50 to 100 approved images**, but this is a convenience target, not a quota. Package fewer when a coherent milestone is ready.

## Release-worker lifecycle

A release worker is a separate disposable transaction. It does not claim a chapter and does not generate new chapter art unless the release itself exposes a packaging defect that requires regeneration.

### 1. INVENTORY

- fresh-read current `main`
- read `IMAGE_SYSTEM.md`
- inspect Library `02 Approved/`
- exclude anything already represented in `04 Released/` or a prior release manifest
- confirm each selected asset has a deterministic image ID and intended repository destination

### 2. MATERIALIZE

Gather the selected approved binaries from Library.

Do not silently substitute similarly named files. Use the exact Library file records selected for the release.

### 3. PACKAGE

Create one release archive:

```text
r2-image-release-NNN.zip
```

Recommended internal shape:

```text
r2-image-release-NNN/
  README.md
  manifest.json
  release-map.json
  r2/
    assets/
      images/
        site/
        continuity/
        chapters/
          chNNN/
```

The `r2/` subtree must mirror final repository-relative destinations so Keoni can perform one large manual drop with minimal renaming or routing.

Only approved production assets belong in the ZIP. Do not include rejects, scratch generations, or unrelated Library files.

### 4. VERIFY THE ZIP

Before calling the release ready:

- every manifest member exists in the archive
- archive paths match deterministic repository destinations
- image files decode
- filenames are unique
- no image is duplicated from a prior release unless explicitly replacing an earlier asset
- manifest count matches packaged image count

### 5. STORE THE RELEASE

Store the completed ZIP and its release manifest under:

```text
/Peg-Leg Greg Image Integration/R2/03 Releases/
```

Only after the release ZIP is successfully stored should the included source binaries move from `02 Approved/` to `04 Released/`.

This move is the Library queue transition that prevents the next release worker from packaging the same approved assets again.

### 6. HANDOFF TO KEONI

Give Keoni the single release ZIP.

The expected human action is intentionally small:

1. download one large release
2. copy/drop its repo-mirrored `r2/` subtree into the repository
3. tell a verification/integration worker the drop is complete

### 7. REPOSITORY VERIFICATION

After the manual drop, a repository worker verifies actual files before chapter manifests or live reader references are changed:

- expected path exists
- binary decodes
- pixels are plausible and match the approved asset
- dimensions/aspect ratio are plausible
- replacement relationships are honored
- manifest/gallery integration points at verified files only

## Default user starter

A fresh packager chat may be started with:

```text
Continue R2 image release packaging from current GitHub and ChatGPT Library authority. Package the current approved unreleased R2 image assets into the next repo-ready release ZIP, store the release in the R2 Library release shelf, update release membership, and stop. Do not generate new chapter art.
```

## Stop rule

One release worker packages one release transaction and then stops.
