# Style spec

Exact values for the social.plus illustration system, on every surface. All colours are social.plus design-system tokens (dark theme); do not introduce others.

## Ground and light

| Layer | Value |
|---|---|
| Ground | `#111111` (neutral-950, `color-bg`) |
| Vignette (above the composition, under the grain — grain is always the topmost layer) | `radial-gradient(ellipse 980px 620px at center, rgba(0,0,0,0) 50%, rgba(0,0,0,0.75) 100%)` — edges go near-black, centre stays #111 |
| Glow (optional, one) | soft radial of blue-600 `rgba(59,65,236,0.42)` fading to 0 at 70%, placed under/behind the focal element; a violet `rgba(159,114,255,0.3)` second glow only if the scene needs depth. Never neon, never a full gradient wash |
| Darken behind focal element | radial `rgba(17,17,17,0.85)` → 0 so the pattern wall recedes where the focal UI sits |

## Neutrals (surfaces, from back to front)

`#1A1A1A` (neutral-900) background pills/panels · `#202022` (neutral-850) cards · `#29292B` (neutral-800) raised parts, icon tiles, borders · `#343437` (neutral-750) strong borders · `#414347` (neutral-700) muted bars and faded labels · `#939497` (neutral-500) primary placeholder bars · `#B3B3B3` (neutral-400) icons on dark · `#FFFFFF` real readable text.

Depth comes from these tonal steps (one step apart) and a single soft drop shadow on the focal card (`0 40px 120px rgba(0,0,0,0.6)`), not from many shadows.

## The one accent

The accent may be ultramarine or another brand color chosen by meaning — see `color-accents.md` for every family's fill, text and glow values. The rules below use ultramarine as the example; they apply to whichever accent the image uses.


- Fill: `#3B41EC` (blue-600) with `#FFFFFF` label/icon. Optional gradient `linear-gradient(145deg, #45A5ED, #3B41EC)` for a large blue shape.
- Blue text or line on dark: `#6F89FC` (blue-400), never #3B41EC (fails contrast).
- Exactly one accent thing per image (a button, a badge, a reaction, a line). A pulse ring of the same element doesn't count as a second.
- One accent family per image (charts may add a second for a second meaningful series — `color-accents.md`).

## Typography

- Figtree, social.plus's own build (`assets/fonts/figtree.woff2`, variable 300–900). Never Google Fonts, never `font-feature-settings`. Fallback `Arial, sans-serif`.
- Name / key label: 52px, 600, letter-spacing -0.015em, `#FFFFFF`.
- Button labels — two named sizes, chosen by the button's height (see Buttons and pills): **in-card button** (80px tall) 34px / 500; **hero accent pill** (140px tall, the image's main action) 52px / 600. White on ultramarine; non-blue accents are never buttons (`color-accents.md`).
- Pattern-wall labels (recognisable copy): 24px, 500, `#414347` — deliberately low contrast; they are texture, not reading matter.
- Budget: max ~4 readable phrases in the background, max 2 in the foreground (e.g. a name + a button). Everything else is bars.

## Abstract text (bars)

Rounded bars (radius = half height) replace copy. Sizes relative to what they replace: name/meta 14px tall; body lines 22px tall, widths stepping down (e.g. 900 / 760 / 520) with the last line darker; pill labels 10px tall.

## Shapes and scale

- Big. At least one object is very large (half the frame or more) and leaves the frame; the archetype decides which.
- Radii large and generous: focal card 44–60px, pills fully rounded, icon tiles 12–26px, avatars circles.
- 2–4 elements total (a pattern or field counts as one). Which elements: see `composition-library.md`.
- Icons: inline stroke SVG (2–2.4 stroke, round caps), `#B3B3B3` on grey, white on the accent fill (dark on yellow/green/orange/purple fills). Never emoji.

## Recognisable objects

Simplify, but keep the 2–3 details that make an object unmistakable:
- **Product**: a silhouette that says "product" (shoe, bag, bottle, headphones — drawn in neutrals as an inline SVG with a soft floor shadow), a price. Never a plain circle or blob.
- **Post / comment**: avatar, name bar, body bars, reaction chips.
- **Phone / window**: a bezel or window chrome edge.
- **Community / group**: cover block, avatar stack, member chip, Join.
Readable prices count as necessary words; use a plausible US placeholder (e.g. $79) and say it is one.

## Social layer

Add one quiet social layer to the main object when it fits the concept: a reaction chip (heart filled #B3B3B3) and a comment chip with bar counts, an avatar stack (3 × 44px, -14px overlap, #202022 rings), or a one-line comment preview (36px avatar + two bars on #1A1A1A). All neutral. At most one row of chips plus one comment preview per object.

## Buttons and pills

Content-sized: equal visual padding on both sides (e.g. 56px left with icon, 64px right). Hero accent pill 140px tall, label 52px / 600 white; in-card button 80px tall, label 34px / 500 white; secondary grey pill #29292B with #B3B3B3 icon and label 32px/500 — only for a different action than the accent one.

## Pattern wall (only for archetypes that use one)

Not every thumbnail has a background pattern — most shouldn't. When the archetype uses one: a repeating set of one UI unit (notification pills, chat bubbles, file chips, logo tiles, data cells…) that represents the "context" of the post — often the old way or the volume. Rows offset alternately so it reads as a texture, cropped on every edge. Units are #1A1A1A with #202022 border; most carry an icon tile + bar, 2–4 carry real low-contrast copy. Fade rows by distance from the focal area (opacity 1 → 0.25).

## Grain

Grain is a treatment, not part of the base style — see `treatments.md`.

## People

Optional, one at most: an avatar portrait (head-and-shoulders, plain/dark background), graded dark, cool, slightly desaturated so it sits in the grain. Photos can't be pulled from Unsplash or similar sites from the chat (network allow-list); ask the person to drop the image in the chat, then upload it as a canvas or film asset. Until a photo is supplied, use a grey gradient circle placeholder (`linear-gradient(160deg, #939497, #414347)`). Placeholder names are fictional and American (see `content-and-locale.md`); say so when delivering.

## Never

Light backgrounds · more than one accent · invented numbers or quotes · readable paragraphs · stock-illustration objects (hands, plants, rockets, 3D characters) · gradient text · other companies' logos unless the content is explicitly about them — named comparisons, listicles, integration or migration guides (`third-party-logos.md`) · fully visible "floating card" layouts.
