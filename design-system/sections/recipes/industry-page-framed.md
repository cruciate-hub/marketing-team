# Recipe: an industry page, framed

The framed version of the industry page recipe (`industry-page.md`), built from the framed sections in `../framed/` on the web library's frame (approved by Stefan, 12 October 2026). Use it when the person chose the framed look; for the current Webflow look use `industry-page.md` (when the request does not say, ask first: "Current Webflow look or the new framed design?"). Never mix the two on one page. Fixed order; a section may be left out only where the table says "optional".

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| F01 | Navigation | none (shared) | always |
| F03 | Hero / Split | eyebrow (the industry), H1 5 to 9 words (the promise for that industry), lead 25 to 45 words, primary + secondary button, a product visual for the industry in the art panel | replaces 03 Hero / Industry |
| F04 | Logo wall (grid) | 6 or 12 customers from the industry | optional: only customers named in `messaging/evidence-bank.md` with approved logo files |
| F07 | Feature grid | section header (H2: the industry's problem in one claim); 3 or 6 cells, icon, title 3 to 6 words, 1 to 2 sentences | the challenges or outcomes (replaces 15 and 13) |
| F06 | Feature tabs | section header; 3 to 5 tabs, each a use case with its own visual | the use cases for the industry (replaces 17) |
| F18 | Use case cards | section header; 4 or 8 linked use cases | optional (replaces 16) |
| F09 | Bento grid | section header; stats, short claims and one visual | why social.plus (replaces 20); numbers only from `messaging/evidence-bank.md` |
| F05 | Feature row | one or two rows | "made for product teams that build fast" (replaces 11) |
| F12 | Customer stories (grid) | 3 stories from the industry | optional: only when stories exist; never invented |
| F14 | FAQ | 5 to 8 questions | optional |
| F15 | CTA band | heading, one line, one primary button ("Contact Sales") | always |
| F16 | Footer | none (shared) | always |

Rules for the page:

- One frame from the navigation to the footer; inside the frame cells divided by lines, never cards; no captured section on the page and none wrapped in the frame.
- One primary button per section, the same primary action in the hero and the CTA band.
- Customer names, logos and numbers only from `messaging/evidence-bank.md`; example numbers in a visual carry "Illustrative example".
- Check the page against `../../feedback.md` and go through the definition of done in `../README.md` before delivery.
