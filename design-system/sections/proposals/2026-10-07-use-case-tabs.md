# Proposed section: Use-case tabs (question + answer)

- Status: proposed (2026-10-07) — needs approval by Stefan or Amadeus · Proposed by: Stefan, after the first Claude Design test (Agentry landing page)
- Not in the set. Until approved, a page that needs it uses the closest existing section, the accordion with image (17), and the reply says so ("built on 17; use-case tabs proposed"). After approval it is added to `capture/capture.config.json` once it exists on the live site, captured, given a `section.md` and a row in the index of `../README.md`.

## What it is for

Showing a product that answers questions ("Agentry in action"): one section where the reader picks a question a team would ask and sees the kind of answer the product gives, with a small data visual and the outcome in one line. For products whose value is a conversation (Agentry, the MCP server), where a feature grid says what the product does but not what it is like to use.

## Structure

- Heading block: optional eyebrow `.superscript` (live source content: "Agentry in action"), H2 5 to 9 words as a claim ("Every team's question, answered in seconds")
- Tab list: 3 to 5 questions, each a short role-based label of 2 to 3 words ("Campaign readout", "Audience understanding", "Executive prep"). Left column at 1440 (the layout of 17: list on one side, panel on the other), a stacked list under 992px
- Answer panel (one visible at a time), right column, a `.card-plain` surface (`--social--dark-gray-background`, radius .5rem, padding 32px):
  - the question as it would be asked, one sentence in quotes, white (`.h5-font-size`)
  - a small data visual: 2 to 4 numbers with a label each (the numbers band 25 at card scale: value white, label grey-light) or a short list of up to 5 rows with a label and a value; no chart library, no colour beyond white and grey-light, one blue-filled tag at most
  - the visible label "Illustrative example" (`.text-size-tiny`, grey-light) under the visual, unless the numbers are real and sourced
  - the outcome in one line, 12 to 20 words, grey-light ("A marketer gets a clear answer with the data behind it, in time for the debrief")
- No buttons inside the section; the page's calls to action stay in the hero and the CTA bands

## What it reuses

- Layout and rhythm: 17 Accordion with image (two columns, list and panel; stacks on phones), `.section.padding_y`, `.container-large`
- Surfaces and type: `foundations/cards/` (`.card-plain`), `foundations/typography/` (`.h5-font-size`, body, `.text-size-tiny`), `foundations/tags/` for the one optional tag, the numbers of 25 for the value and label pairing
- Tokens only: `--social--dark`, `--social--dark-gray-background`, `--border--border-dark`, white, `--text--text-color-grey-light`, `--social--main-blue` for the active tab marker (a blue fill or a 2px blue left border; never blue text on dark)
- Nothing new: no icon style, no chart style, no glow, no animation beyond the panel swap (none under reduced motion)

## Accessibility

- The tab list is `<div role="tablist">` with real `<button role="tab" aria-selected aria-controls>` elements; the panels are `role="tabpanel"` with `aria-labelledby`. The tabs are reachable with Tab, switched with the arrow keys, and show the focus ring of `foundations/accessibility/` (`:focus-visible`, 2px, visible on dark); the active tab is marked by more than colour (the blue marker plus bold or an underline)
- Rows are at least 44px; no text under 12px; every pair in the contrast table (white and grey-light on `--social--dark-gray-background`)
- On phones the tabs stack above the panel as a list of buttons; nothing scrolls sideways at 390px
- The static state (first tab selected, its panel shown) is what the screenshots and `source.html` show, as for every scripted section

## Example

The source content of the Agentry page (7 October 2026): five questions (Campaign readout, Audience understanding, Content strategy, Executive prep, Trendspotting), each with a quoted question, a three-number visual (for example "+24% engagement, +31% reactions, 847 new posts") and an outcome line. The test build placed this on the accordion with image (17) without marking it proposed; this proposal is the section it wanted.

## Open points for the approver

- Tabs or accordion: on phones the two are the same thing; on desktop tabs keep the list visible. The live site has one tab section (/social/stories, "Tabs with image", outside the set) that could be the base instead of 17
- Whether the "Illustrative example" label stays when the product can show a real, sourced answer
- Where the section sits in the product-landing recipe (today: the "how it works or use cases" slot, `../recipes/product-landing.md`)
