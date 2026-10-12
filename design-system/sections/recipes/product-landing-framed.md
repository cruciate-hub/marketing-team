# Recipe: a product or feature landing page, framed

The framed version of the product landing recipe (`product-landing.md`): the same page type (Agentry, the MCP server, Vise, an add-on), built from the framed sections in `../framed/` on the web library's frame. This is the version to build since 12 October 2026; the captured version stays for reading the live AI pages. Never mix the two on one page. Fixed order; a section may be left out only where the table says "optional".

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| F01 | Navigation | none (shared) | always |
| F02 | Hero / Centered | eyebrow (the product name, Geist Mono), H1 6 to 9 words, lead 20 to 40 words, primary + secondary button, the "Works in" row under the buttons | when there is no product visual; the art-panel visual is left out |
| F03 | Hero / Split | eyebrow, H1 5 to 9 words, lead 25 to 45 words, primary + secondary, product visual in the art panel | instead of F02 when a real product visual exists. Never both |
| F04 | Logo wall (inline) | customers | optional; only with F03. With F02 the "Works in" row is the logo row |
| F07 | Feature grid | section header (eyebrow optional, H2 4 to 8 words: the value in one claim, optional lead); 3 or 6 cells, each an icon tile, a title of 3 to 6 words and 1 to 2 sentences | the value cells ("Your team asks. Your first-party data answers."): cells divided by frame lines, never cards |
| F06 | Feature tabs | section header (H2 3 to 6 words); 3 to 5 tabs, each a title, one or two sentences and its own visual | the use cases or how it works ("Every team's question, answered in seconds") |
| F12 | Customer stories (grid) | 3 stories from the CMS | optional: only when stories for this product exist; never invented |
| F14 | FAQ | 5 to 10 questions with one-paragraph answers | at least: what it is, what it works with, what data it reads or changes, who controls access, how to get started |
| F15 | CTA band | heading 2 to 6 words, one line, one primary button (the page's primary action) | always, last before the footer |
| F16 | Footer | none (shared) | always |

Rules for the page:

- One frame from the nav to the footer: every section is framed, none is a captured section, and no captured section is wrapped in the frame (the Grid and frame foundation).
- Inside the frame, content sits in cells divided by frame lines: no card fill, no radius, no gap between cells. Cards exist only outside the frame (a pop-up, a floating panel).
- Colours through the role tokens, type on the type scale, spacing on the steps and section paddings; eyebrows in Geist Mono. The art panel is the only gradient surface and sits only behind a product visual.
- One primary button per section: hero and CTA band with the same primary action. Two actions of equal weight need approval from Stefan or Amadeus.
- Numbers in a visual carry the visible label "Illustrative example"; product facts come from `messaging/product-capabilities.md`; the "Works in" row uses the approved icons in `../../assets/third-party/ai-tools/` and names only what the product supports today.
- Links that do not exist yet are `href="#"` with a note of the intended path. A visual that does not exist yet is the library's placeholder in the art panel, marked "placeholder" in the reply.
- Before delivery, go through the definition of done in `../README.md`.
