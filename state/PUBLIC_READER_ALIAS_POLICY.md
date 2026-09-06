# PEG-LEG GREG — PUBLIC READER ALIAS POLICY

Purpose: keep published chapter links and reader navigation stable when structural editing changes chapter numbering, titles, acts, or book placement.

## Core rule

Public presentation may change. Old reader links should not break casually.

Stable chapter identity should be the source of truth. Display number and slug are generated/current presentation fields.

## Legacy URL behavior

When a published chapter changes number or title:
- preserve its previous public slug as a legacy alias when practical;
- route the alias to the current surviving chapter identity;
- do not create redirect loops;
- keep aliases out of normal chapter navigation and index presentation.

When a chapter is merged:
- legacy URLs for merged source chapters should resolve to the surviving merged chapter when the source scene materially survives there;
- if a source chapter is fully retired and its content does not survive, use an intentional archive/retired behavior rather than silently pointing to unrelated prose.

## Current canonical URL

Each active chapter identity should have one current canonical slug derived from current publication structure.

The canonical slug may include chapter number/title for readability, but identity resolution should not depend exclusively on parsing that number.

## Reader navigation

Previous/next links, book/act lists, chapter counts, progress indicators, and table of contents must be regenerated from current active sequence after structural finalization.

Do not hand-edit hundreds of downstream links after renumbering.

## Bookmarks and external links

Treat legacy aliases as compatibility infrastructure for:
- browser bookmarks;
- shared links;
- search indexing;
- existing illustration notes;
- project documentation;
- old chat/review references.

## Illustration URLs

Do not assume image paths must match current chapter number.

Prefer stable asset identity and manifest-driven placement so renumbering does not require destructive image renames.

## Migration QA

Before shipping a renumbered range:
- old known public slugs resolve as intended;
- current canonical slugs resolve;
- no active chapter has duplicate canonical URLs;
- previous/next sequence matches current order;
- act/book navigation matches current structure;
- illustrated chapter links load the intended art;
- retired chapters are not accidentally listed as active.

## Goal

A reader who bookmarked Chapter 205 before a compression pass should not receive a meaningless 404 simply because the surviving scene became Chapter 188.
