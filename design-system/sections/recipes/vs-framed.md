# Recipe: a /vs/ page, framed

The framed version of the /vs/ recipe (`vs.md`), built from the framed sections in `../framed/` on the web library's frame (approved by Stefan, 12 October 2026). Use it when the person chose the framed look; for the current Webflow look use `vs.md` (when the request does not say, ask first: "Current Webflow look or the new framed design?"). Never mix the two on one page. Fixed order; a section may be left out only where the table says "optional".

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| F01 | Navigation | none (shared) | always |
| F02 | Hero / Centered | eyebrow "Compare", H1 "social.plus vs <competitor>" or a claim of 5 to 9 words, lead 25 to 45 words that positions social.plus against the competitor in plain words, primary + secondary button; no visual | replaces 05 Hero / vs and 50 Statement band (the lead carries the statement) |
| F04 | Logo wall (inline) | customers | optional; only approved logos |
| F05 | Feature row | two or three rows: what social.plus delivers beyond the competitor, each with a product visual | replaces 51 Side-by-side |
| F21 | Comparison table | feature groups and rows; social.plus facts from `messaging/product-capabilities.md`, competitor facts with a source | always; replaces 52 |
| F12 | Customer stories (grid) | 3 stories | optional: only real stories |
| F23 | Contact form | heading, three reasons, the form | the conversion point (replaces 53) |
| F14 | FAQ | at least: the difference, what each offers that the other does not, data ownership, migration | always |
| F15 | CTA band | heading, one line, "Contact Sales" | always |
| F16 | Footer | none (shared) | always |

Rules for the page:

- One frame from the navigation to the footer; inside the frame cells divided by lines, never cards; no captured section on the page and none wrapped in the frame.
- Fair and factual: every competitor claim has a source in the reply; nothing about the competitor that the source does not say. The comparison table's social.plus column is the highlighted one.
- One primary button per section; the same primary action in the hero, the contact form and the CTA band.
- Check the page against `../../feedback.md` and go through the definition of done in `../README.md` before delivery.
