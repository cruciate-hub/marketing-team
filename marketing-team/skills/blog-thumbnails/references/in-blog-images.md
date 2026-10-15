# In-blog images

Images placed inside the article. Unlike the thumbnail (which sells the post's idea in one glance), in-blog images **explain**: they show the article's data, processes and structures so a reader understands a section faster than from the text alone. Same illustration system, same grain, more descriptive.

## Specs

- Size **1578×888**, WebP, named `{slug}_img-N_1578x888.webp` (N = 1, 2, 3 in reading order) — the blog collection's inline image spec (`webflow-fields.json` → `inline_images`).
- Grain on (editorial), at full strength — inline images are shown large.
- **How many is decided per article** (see "Deciding how many" below), each placed directly after the paragraph it explains. Name the target section in the artboard title: `In-blog 2 — Hub: channels converging (Omni-channel engagement)`.

## Deciding how many

There is no fixed number. Decide from the article, and state the count and the reasoning in the plan before building.

1. **List the candidates.** Go section by section (every H2/H3) and note what could be shown: a sourced number or comparison (chart), a process or sequence (flow), parts of a whole (diagram), a product moment (annotated UI). Sections with only opinion or general advice get nothing.
2. **Filter for quality.** Drop candidates whose data is unsourced, internally inconsistent or only a single standalone number with nothing to compare; drop processes the text already makes obvious. Flag broken figures to the person instead of charting them.
3. **Merge what belongs together.** Related stats become one chart (e.g. 90-day retention for two app types; App Store vs Google Play) rather than one image each.
4. **Space them.** At most one image per section, and at least ~2 paragraphs (≈150 words) of text between two images, so the article still reads as an article.
5. **Sanity-check against length.** As a guide, roughly one image per 300–500 words of body for data-heavy pieces (stats roundups, benchmarks, comparisons), one per 600–900 words for argument-led pieces (guides, opinion). Short posts (<800 words) may need just one — or none.

Typical outcomes: a 5-minute strategy guide → 2–3; a 14-minute stats roundup → 6–8; a short opinion piece → 0–1. Present the full list with section placements; if it runs long, mark which are essential and which are optional so the person can trim.

## What makes a good in-blog image

Choose per section, in this order of preference:

1. **Data chart** — when the article has numbers. Use only the article's own figures, with their exact values and wording ("up to 5×", "48.85%"). One clear comparison or trend per chart; no invented series, no filler bars. If the article cites a source, add a source chip; if it states a figure without one, label it honestly ("as cited in the article").
2. **Flow / process diagram** — when the section describes steps, triggers, funnels, loops or a before→after: e.g. trigger → wait → action, signal → segment → message, channels converging on one user.
3. **Structure / system diagram** — when the section describes parts of a whole: channels around a hub, layers of a stack, segments of an audience — with readable labels for each part.
4. **Annotated UI** — when the section describes a product moment: the UI at large scale with 2–4 annotation callouts naming what matters.

Avoid purely atmospheric images here; if a section has nothing to explain visually, it doesn't need an image.

## Text and labels

More readable text than a thumbnail, still disciplined:
- A short mono eyebrow naming what the image shows (`COST TO WIN A USER`) — optional.
- Labels for every part a reader must identify: axis ticks, series names, step names, channel names, segment names.
- Values printed on or next to bars and points, large (62–72px at 1578 wide).
- No sentences or paragraphs — the article carries the explanation.
- American conventions, fictional American names, USD (master's `content-and-locale.md`).

## The frame (every in-blog image)

All in-blog images share one layout frame at 1578×888: **120px left and right, 100px top and bottom** (content box x 120–1458, y 100–788).
- The **eyebrow** sits on the top-left corner of the frame (x 120, top 100).
- The **source chip** sits on the bottom-left corner: x 120, its bottom edge at y 788 — the same distance from the bottom as the eyebrow is from the top. If the chart occupies the left column down to the bottom (e.g. a waffle grid), align the chip to the left edge of the text column instead, still bottom-aligned at 788.
- **One source chip per image.** Several sources go in the same chip ("Sources: Localytics; Business of Apps"). Caveats ("two separate studies", "as cited in the article") go in the eyebrow or under the chart, never as a second chip.
- Chart, labels, values and callouts stay inside the frame; leave ≥24px between the lowest chart element and the source chip.
- Check it: render the image with the frame drawn on it before showing it.

## Chart style

- Ground #111, vignette as usual, grain on (topmost).
- Bars and lines in neutrals (#343437 bars, #414347 lines); **one accent series or bar = the point** the section makes (e.g. the cheaper path, the highlighted segment). The accent is ultramarine unless the data's meaning calls for another brand color (growth → green, gaming → yellow, AI → purple…; master's `color-accents.md`), keeping the set ≥60% ultramarine. The accent never just decorates.
- Axis and grid: thin neutral-850 #202022 / neutral-750 #343437 lines; tick labels Geist Mono 28px neutral-500 #939497; series labels Figtree 38px #B3B3B3; values Figtree 600 62–72px white.
- Rounded bar ends (radius = half the bar height), generous spacing, at most ~6 bars or 3 lines.
- A trace of people where it helps the meaning: an avatar at the start of a row (dashed for "new/unknown", solid for "existing"), a small reaction chip — never as decoration that competes with the data.

## Flow and diagram style

- Steps as cards (#202022, 44px radius) with an icon tile, a mono step label (`TRIGGER`, `ACTION`) and a short readable name; connectors as dotted lines (#414347, round dots) with small grey nodes for waits or conditions.
- The blue card or element is the outcome or the step the section argues for.
- Diagrams may be fully in frame (no aggressive cropping) — legibility beats drama here; supporting objects (a preview card, a device) can still bleed off an edge.

## Worked example — "The advanced guide to app re-engagement strategies"

- **img-1, after the intro** — chart: "Acquiring a new user" (grey bar, up to 5×) vs "Re-engaging an existing user" (blue bar, 1×), on a 0–5× axis; dashed avatar for the new user, solid for the existing one; "as cited in the article" belongs in the eyebrow or source chip. Replaced a first attempt (users sorted into segments on a tilted plane) that was too abstract to explain anything.
- **img-2, Omni-channel engagement** — hub: Email, SMS, Push, In-app tiles in the corners, dotted lines flowing to one user profile in the centre (blue avatar ring).
- **img-3, Behavioral triggers and automation** — flow: "Cart abandoned" trigger card → dotted connector with a timer node → blue "Send personalized offer" action card; the offer (headphones) as a tilted preview card bleeding off the right.

## Worked example — "20 App monetization stats you should know"

Seven images by the per-article evaluation (14-minute data-heavy roundup): waffle (3% of apps are paid), split bar (83% freemium), two rings (90-day retention 24% vs 35%, two studies), fill columns (IAP share 48.2% vs 72% gaming — yellow), bars ($13B → $18.3B, +41% — green), horizontal bars (App Store $13.5B vs Google Play $4.8B), hub diagram (six monetization models). First versions had source chips 35px from the bottom against 120px from the left, and two chips colliding on the retention chart; fixed by the frame above.
