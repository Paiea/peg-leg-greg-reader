# Greg, Again — Audio Pronunciation Authority

This file is the durable pronunciation and inconsistency watchlist for R2 / Greg, Again audio production.

Written prose remains authoritative for displayed text. This file controls provider-facing synthesis spelling only. Never flow phonetic spellings back into the written chapter unless the prose itself is separately edited.

## Two classes of pronunciation knowledge

### 1. Hard provider aliases

Use these provider-facing spellings by default whenever the written token appears in newly synthesized audio. These are settled pronunciation rules, not prose edits.

| Written token | Preferred provider spelling | Intended sound | Historical repair | Notes |
| --- | --- | --- | --- | --- |
| `mana` / `Mana` | `ma-na` / `Ma-na` | Hawaiian-context `MAH-nah` | Yes, where a published spoken occurrence is confirmed wrong | Listener QA on 2026-09-08 showed that literal `mah-nah` can make the `deep` voice audibly pronounce the written H. `ma-na` produced the more reliable target sound in the approved second-pass repairs. Written spelling remains `mana`. |

#### Historical `mah-nah` evidence

`mah-nah` was the first provider spelling tested and can sound correct in some contexts, so successful existing clips do not need regeneration solely to normalize spelling. However, it is **not** the forward default because listener QA caught multiple renders where Deep vocalized the H or otherwise sounded unnatural.

When generating a new take or regenerating a rejected repair, prefer `ma-na` first. Preserve an already-generated `mah-nah` clip when the listener-facing pronunciation is already acceptable.

### 2. Instability watchlist

These words have produced at least one inconsistent provider reading. Prefer the safer provider spelling in future synthesis when it preserves the intended pronunciation, but do **not** automatically regenerate already-published audio that sounds correct.

| Written token | Preferred provider spelling | Intended sound | Historical repair policy | Known evidence |
| --- | --- | --- | --- | --- |
| `Vale` | `Vayle` | rhymes with `veil` | Patch only confirmed bad occurrences | Chapter 5, Take 07, listener timestamp about 08:08: `Vale expected money tomorrow.` was read approximately `Val`. Other published `Vale` readings are generally acceptable. |
| `sparring` | `spar-ring` | normal English `sparring` | Patch only confirmed bad occurrences | Chapter 4, Take 01, listener timestamp about 00:44 previously sounded approximately `spare-ing`. |

## Production behavior

Before sending a take or micro-repair to the voice provider:

1. preserve the exact written/spoken wording as the semantic authority
2. apply hard provider aliases to provider-facing text
3. for written `mana`, prefer provider-facing `ma-na`
4. check the instability watchlist for names or terms present in the take
5. use the preferred provider spelling when it is a safe phonetic equivalent
6. record any provider-facing substitution in the take / repair evidence
7. never treat a phonetic provider spelling as a prose edit

For already-published audio:

- do not mass-regenerate merely because a word appears on the instability watchlist
- preserve acceptable historical readings, including acceptable earlier `mah-nah` renders
- repair only confirmed bad occurrences, using the smallest sentence-local or take-local patch that preserves surrounding performance
- if an ultra-short repair such as `No mana.` is swallowed or produces silence, include the smallest neighboring spoken context needed for a reliable provider performance, then splice only the target listener-facing region
- when a new listener-caught inconsistency appears, add it here so future workers inherit the knowledge

## Why this exists

Voice synthesis can be nondeterministic about names, fantasy terms, homographs, phonetic respellings, and uncommon words. A term can sound correct in ten takes and fail in the eleventh. Listener QA should therefore accumulate into durable production knowledge instead of remaining trapped in chat history.

The goal is not to phoneticize the book. The goal is to make future provider calls more reliable while keeping written authority clean.
