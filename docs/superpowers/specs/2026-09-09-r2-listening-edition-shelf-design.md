# R2 Listening Edition Shelf Design

## Goal

Make the Greg, Again audio index the primary public experience for Peg-Leg Greg R2. The page should feel like a finished story product rather than a production surface, with listening as the default action, written chapters as a reference surface, and chapter art as visual storytelling rather than decoration.

## Product hierarchy

The public hierarchy is:

1. R2 Listening Edition hero
2. Start Listening action
3. Compact availability/context strip
4. Illustrated audio chapter shelf
5. Quiet links back to R2 and the written reference

The page must not expose experiment-era or provider-production language. Terms such as experiment, lab, approved render, take count, lens, provider, and production notes remain internal only.

## Visual direction

Use the R2 light-mode visual language as the default: warm cream/paper background, dark ink/brown typography, muted maroon accent, restrained borders, and color supplied primarily by approved art. The interface should feel editorial, warm, book-like, and slightly handmade without becoming faux parchment, pirate branding, a streaming-service clone, or dashboard UI.

The page should be visually richer than the current audio list but simpler than a conventional audiobook application. Native, accessible audio controls remain acceptable and preferred unless they become a concrete usability blocker.

## Hero

The hero is the visual front door to R2 listening.

It contains:

- one large source-grounded R2 hero image
- `R2 Listening Edition` identity
- `Peg-Leg Greg R2` title
- a short listener-oriented description
- one dominant `Start Listening` action

The hero image should depict a real R2 place/relationship and use approved R2 visual continuity. It should not introduce a generic fantasy companion, pirate iconography, or invented canon. The final binary may be uploaded manually to the repository by the project owner. The page must use a stable expected asset path and degrade gracefully if the binary is temporarily absent.

## Availability strip

Immediately below the hero, show a compact product-level status line derived from current public authority, for example the number of playable chapters and the availability of written reference text. This is audience-facing context, not production telemetry.

Do not hard-code a chapter count that will go stale. Derive it from the public audio manifest at render time.

## Chapter shelf

Published audio chapters render as illustrated cards driven by the existing Greg, Again audio manifest. The manifest remains authoritative for stable chapter identity, number, current title metadata, duration, audio source, and publication state.

Desktop uses a two-column card grid when space permits. Mobile uses one column. Cards must remain comfortably playable and readable on touch devices.

Each card contains:

1. chapter number / stable identity context
2. current chapter role/title
3. one short, exact source-grounded quote from that chapter when approved quote metadata exists
4. one approved chapter image when available
5. duration and/or minimal useful listening metadata
6. playable audio controls

Cards must not depend on art or quote availability to remain playable. Missing optional art collapses to a deliberate text-first card state rather than a broken image frame. Missing quote metadata simply removes the quote region.

## Chapter art model

Chapter art is a separate presentation layer keyed by stable audio identity such as `ga-001`, not by mutable chapter title. Audio publication must never depend on image publication.

The initial target is one approved image for each currently published audio chapter. Future chapters can acquire art independently after audio publication.

The visual concept is `Greg's roles illustrated through his footprint`.

The chapter title names the role Greg is playing. The image should usually show evidence of that role in the world rather than defaulting to another portrait of Greg. Examples include a place he changed, an object he borrowed, a work surface, a bargain in progress, another character reacting to his effect, tools, aftermath, or an empty space that implies his action. Greg may appear when his physical action is necessary to make the chapter concept legible, but `Greg absent unless useful` is the default compositional bias.

This rule is a bias, not a prohibition. Source truth and visual interest outrank forced absence.

## Art consistency and variation

All chapter art must remain source-grounded and consistent with current R2 continuity and approved visual references. Do not invent characters, costumes, props, locations, or relationships merely to make a prettier card.

The shelf should deliberately vary visual grammar so it does not become 23 object-on-table images or 23 Greg portraits. Across a run of cards, vary among:

- environments
- objects and tools
- hands/actions
- aftermath
- supporting-character perspective
- work and money evidence
- empty or recently occupied spaces
- Greg-centered action when genuinely useful

Art supplies texture and personality; the UI frame stays consistent.

## Art and quote metadata

Add a small presentation manifest separate from the audio production manifest. It is keyed by stable `ga-NNN` identity and may contain:

- image path
- alt text
- approved exact quote
- optional focal/crop hint if the implementation needs it

Do not duplicate mutable audio title, duration, publication state, or audio source in this presentation manifest. Those remain owned by the existing audio manifest.

The public renderer joins the two sources by stable audio identity.

## Data flow

1. Load the existing public Greg, Again audio manifest.
2. Filter to currently published/playable entries according to existing rules.
3. Load optional listening-shelf presentation metadata.
4. Join presentation metadata by stable `ga-NNN` identity.
5. Render the hero, derived availability count, and chapter cards.
6. If presentation metadata or an individual image is unavailable, preserve audio playback and render a graceful fallback.

A title rename must update automatically from audio/written authority without breaking its art association.

## Homepage relationship

The R2 homepage should continue to feature listening as the dominant route. It may use the same Listening Edition hero language or a compact derivative, but the full chapter shelf belongs on `/greg-again/audio/`.

The homepage should not duplicate the full shelf or create a second independent source of chapter metadata.

## Written reference

Reading remains available but secondary. Public language should frame it naturally as the written chapters or written reference, useful when a listener wants to check a name, line, or detail. Do not diminish the quality of the written surface; only clarify the product hierarchy.

## Error handling and graceful degradation

- Audio manifest unavailable: show a clear temporary listening-unavailable state rather than an empty shelf.
- Presentation manifest unavailable: render the complete playable shelf without art/quotes.
- Individual image unavailable: omit/collapse the image region; never block the player.
- Missing quote: omit it.
- Future published audio without art metadata: automatically appears as a playable text-first card.
- Stale title in presentation data is impossible by design because titles are not duplicated there.

## Accessibility

- Preserve semantic headings and keyboard navigation.
- Images require source-grounded alt text; decorative imagery uses appropriate empty alt text only when genuinely decorative.
- Do not put essential information only inside an image.
- Maintain readable contrast in light mode.
- Keep touch targets comfortable on mobile.
- Audio remains operable through standard accessible controls.
- Respect reduced-motion preferences; no motion is required for this design.

## Testing

Add or update automated site contracts to verify:

- the audio page uses the light Listening Edition presentation
- public experiment/production terminology does not return
- published audio entries are still manifest-driven
- the availability count is derived rather than hard-coded
- presentation metadata joins by stable `ga-NNN` identity
- missing presentation metadata does not suppress playable audio
- missing art/quote produces graceful card fallbacks
- title changes do not change stable art association
- homepage continues to route prominently to the listening shelf

Run the existing R2 site tests, Greg Again audio validation, and full repository test suite before merge.

## Scope boundaries

This design does not:

- replace or redesign the audio production pipeline
- change stable audio identity
- regenerate or rewrite audio
- rewrite story prose
- require art before publishing audio
- build account-based listening progress or cloud resume state
- build a custom streaming player
- create 23 images before the page architecture can ship

The page system should ship independently. Chapter art can then be generated/reviewed and added incrementally, with the first batch targeting all currently published chapters.

## Success criteria

A first-time visitor should understand within seconds that R2 is principally something to listen to, see an intentional R2 visual identity, and be able to start Chapter 1 without learning anything about the production system.

A returning listener should be able to scan visually distinct chapter cards and play the desired chapter quickly.

Adding a newly published audio chapter should require no hand-editing of page markup. Adding or replacing its art should require only presentation metadata plus the approved image binary.
