# Taste: how social.plus pages are put together

The section set says what the blocks are. This page says how to combine them so a page looks and feels like social.plus. Read it with `sections/README.md` (the rule and the definition of done) and the recipe for the page type; apply it when you build, and again when you render the page and check it.

- Status: draft (2026-10-07) — Amadeus to refine · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the live site as captured on 7 October 2026 (`sections/`, `foundations/`), the site audit of the same day, and the first Claude Design test (Agentry landing page, 7 October 2026)
- Each rule has a "do" and a "don't" from the live site or from that test. The measured values the rules rest on are in the foundations; this page does not repeat them

## 1. Calm pages, one focal point per screen

A social.plus page is quiet. Each screen (what fits in the viewport at 1440 and at 390) has one thing the eye lands on: the H1 and its product visual in the hero, one heading and one picture in a two-column section, one grid in a feature section. Everything else on that screen is secondary and looks it.

- Do: https://www.social.plus/chat, the hero: one heading, one paragraph, one blue button, one product video. Nothing competes.
- Don't: a hero with three buttons, a logo row, a badge and an animated diagram in one viewport (the source content of the test had three buttons and a logo row in the hero; the test build rightly kept one blue button and moved the rest down).

## 2. Section rhythm

Alternate dense and airy. A grid of cards (12, 13, 14, 15, 16) is dense; a two-column (11), a CTA band (23, G4) or a statement is airy. Put an airy section between two dense ones. Never stack three card grids. Every section is `.section.padding_y` (5rem top and bottom at 1440, 3rem under 480px, measured in `foundations/spacing/`); do not add extra padding or a spacer section to "give it air", change the order instead.

- Do: /chat: hero (airy) → logo marquee (thin) → three two-column rows (airy) → feature grid (dense) → customer story strip (dense, but pictures) → Why social.plus (dense) → Explore more (airy) → CTA band.
- Don't: problem cards → feature icon cards → bordered cards in a row. If a page wants three sets of cards, one of them is a two-column or an accordion with image (17).

## 3. One primary action per section, one per screen region

One blue button (`--social--main-blue`) per section, and never two blue buttons side by side. The primary action is the same ask across the page (Contact Sales on product pages, "Connect …" on an AI page) in the hero, the inline CTA band and the footer CTA band. A section that is not a hero or a CTA band uses grey buttons (`.cta-button.c-grey`) or text links. A second action next to the primary is a grey button; a third is a text link. Two actions of equal weight need approval from Stefan or Amadeus.

- Do: https://www.social.plus/ai/mcp-server: "Connect your AI tool" (blue) + "Documentation" (grey) in the hero; the same pair in the "Start building" band; Contact Sales in the footer band.
- Don't: "Connect on Claude" and "Connect on ChatGPT" as two blue buttons (the open question from the test). Pick one as primary, or make the choice a step inside the destination page.

## 4. Real product visuals, not abstract art

The picture next to a claim is the product: a screenshot in the dark rounded frame, a product video, a UI illustration in the style of `foundations/imagery/` (dark, one blue glow, UI metaphors). Not a drawn flow diagram, not clip art, not a generated abstract shape, not a stock photo of people at laptops.

When there is no product visual yet: use the simple hero (02) with text and buttons and the "Works with" logos row, and leave the right column empty; or place the approved placeholder (a rounded frame in `--social--dark-gray-background` with a 1px `--border--border-dark` border and the grey-light label "Product visual to come", see `sections/recipes/product-landing.md`) and say in the reply that the page needs a product visual. Never draw one to fill the gap.

- Do: /chat: the hero video is the product; the three two-column rows show screens of the product.
- Don't: the test build drew a flow of boxes and arrows as the hero visual. That is a diagram, not the product.

## 5. Colour: blue is the accent

The page is dark (`--social--dark`), text is white and grey-light, and blue is the one accent: button fills, tags, icon holders. The secondary colours (green, yellow, red, orange, purple, pink) signal status or decorate one small thing; they never colour a section, a heading or a call to action. Blue is never text or an icon colour on dark (2.84:1; the rule for links on dark is in `brain.md`). One highlighted card per set at most; the rest are greyscale (`foundations/cards/`).

- Do: /vs/circle: dark throughout, blue only on the buttons and the comparison highlight.
- Don't: a green "live" badge in the hero, a purple feature card, a yellow heading. Status colours stay in tags and inline markers.

## 6. Typography: one H1, headings are claims

One `<h1>` per page, 5 to 9 words, the product's promise. Every section heading is a claim in plain words (what the reader gets), not a label ("Features", "Benefits") and not a question, unless the section is the FAQ. Headings are short: H2 5 to 12 words, card titles 3 to 6, one line where it can be one line. Body copy stays in the measured sizes (`foundations/typography/`): no custom sizes, no bold runs inside paragraphs, no all-caps outside tags and the `.superscript` eyebrow.

- Do: "Build in-app messaging faster with a Chat SDK" (H1), "All the messaging features your app needs" (H2), "Reactions" (card title).
- Don't: a label ("Features", "Why Agentry") as the H2 with the real claim under it as a second heading. The label is the `.superscript` eyebrow; the claim is the H2.

## 7. Spacing: be generous, use the steps

Space is the way a dark page shows structure. Use the containers and steps that exist (`.container-large` 1280px, `.container-medium` 760px for text-only sections, the five spacing steps and `.section.padding_y`), and the measured grid gaps (`.grid-2` 4rem). Let a paragraph stop at 44 to 56 characters (`.max-ch-NN`). When a section feels crowded, cut content; do not shrink the type or the gaps.

- Do: the FAQ (18) sits in `.container-medium`; the two-column rows keep the 4rem gap.
- Don't: six cards squeezed into three columns at a smaller font to fit one screen. Six cards are two rows.

## 8. No one-off effects

No gradient text, no glow behind a card, no new animation, no parallax, no glassmorphism panels, no custom icon style, no new shadow. What moves on the live site (marquee, count-up, carousel) is in the captured sections; anything else is still. The live `h1` gradient text fill and the blue glows on the AI pages are known inconsistencies, not a licence (`foundations/colors/`, `foundations/shadows-and-radius/`). An effect the page seems to need is proposed first, like a section.

- Do: depth from lighter surfaces (`--social--dark-gray-background` cards on the `--social--dark` page), one `--border--border-dark` line between layers.
- Don't: a blue glow behind every card, a shimmering border on the hero, icons from an icon font.

## 9. Dark first

Every website page is dark. Light sections (`--social--grey-background`, white) exist only in the captured sections that have them (legal pages, the AWS page) and are not used for a new marketing page. Build the dark page first and completely; a light variant is not a thing to add "for contrast".

- Do: every recipe in `sections/recipes/`: dark background throughout.
- Don't: a white "trusted by" band to break up the page. Use the logo wall (10), which is dark.

## 10. Mobile

The page is built for 1440 and checked at 390. On a phone every section stacks to one column, the media goes above the text, the primary button is full width, nothing scrolls sideways, text stays at the measured mobile sizes (no smaller) and targets stay at 44px. A section that only works on desktop (a wide table, a six-column row) is the wrong section.

- Do: the captured `mobile.png` of each section is what it should look like at 390.
- Don't: a tab row that overflows on a phone, a hero visual that pushes the H1 below the fold.

## 11. Numbers and data

A number on a page is either real and sourced, or an example and labelled. Real numbers (customer metrics, the numbers band 25) come from `messaging/evidence-bank.md` or the customer story and carry their source or caveat in the footnote. Example numbers (a mock dashboard in a product visual, a sample answer in a chat) carry the visible label "Illustrative example" next to the visual, in `.text-size-tiny` grey-light, and the reply says so. Never make a chart or counter look like a measurement. Product facts come from `messaging/product-capabilities.md`.

- Do: the home page numbers band: four numbers with the footnote "Representative client results. Outcomes vary …".
- Don't: "+24% engagement" in a mock answer panel with no label (the test build needed a person to ask for the label; now the label is part of the definition of done).

## 12. What on-brand feels like

social.plus speaks as infrastructure: confident, clear, technical where it helps, never loud (`messaging/tone.md`). On a page that means: claims the reader can check, product screens rather than metaphors, one ask at a time, and room around everything. If a page feels like a launch poster (big effects, many colours, several buttons), it is off-brand even when every token is right. If it feels like the documentation of a serious platform with one clear next step, it is right.

- Do: /ai/vise: one promise, one proof structure, one pair of buttons, FAQ, footer band.
- Don't: emoji in headings, exclamation marks, "revolutionary", a countdown, a pop-up.

## 13. Before you say "done"

Go through the definition of done in `sections/README.md` (the rule), render the page at 1440 and 390, compare it with this page and the section notes, and list every mismatch in the reply. "Looks good" is not a check.
