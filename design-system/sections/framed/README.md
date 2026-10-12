# Framed sections

The section set on the web library's frame (Amadeus, decision 8 October 2026): 23 sections taken unchanged from the library on 12 October 2026 (F01 to F16 from its page demo, F17 to F23 from its section pages) (one social.plus addition: the "Works in" variant of F02, `feedback.md` item 5). They replace the captured sections on a framed page; the captured sections stay as the record of the live site. Not yet in Webflow.

- Status: approved (2026-10-12) · Owner: Amadeus · Approved by: Stefan, 12 October 2026
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its page demo
- Files: `framed.css` (the library's stylesheet, one copy for all sections), and per section `source.html` (links `../../../tokens.css` and `../framed.css`; no scripts, interactive parts in their first state) and `section.md`
- On the Claude Design page: the groups "Framed · …"; `framed.css` is `components/framed.css` there

## The rule

A page is framed or captured, never both. A framed page uses only framed sections, on one frame from the navigation to the footer; a captured section is never wrapped in the frame. Framed or current (captured) is chosen per page by the person who asks for it; when the request does not say, ask before building: "Current Webflow look or the new framed design?" (decision: Stefan, 12 October 2026). Framed recipes exist today for `../recipes/product-landing-framed.md`, `../recipes/industry-page-framed.md` and `../recipes/vs-framed.md`, next to their current versions; other page types exist only in the current look.

- The framed navigation (F01) and footer (F16) keep the live site's content (`../global/nav/`, `../global/footer/`): the same links, labels, legal text and social links. Only the layout is new. Content the library added on its own does not ship (`../../feedback.md` item 10).
- A Figma hand-off of a framed page follows `../../figma/README.md`.

## The set

| # | Section | Group | Replaces on a framed page |
|---|---|---|---|
| F01 | Navigation | Global | G1 Nav |
| F02 | Hero / Centered | Heroes | 02 Hero / Simple |
| F03 | Hero / Split | Heroes | 01 Hero / Product, 03 Hero / Industry |
| F04 | Logo wall | Proof | 10 Logo wall |
| F05 | Feature row | Features | 11 Two-column |
| F06 | Feature tabs | Features | 17 Accordion with image |
| F07 | Feature grid | Features | 12 Feature grid, 13 Card grid / Icon cards, 14 Bordered, 15 Plain |
| F08 | Platform row | Features | (none) |
| F09 | Bento grid | Features | 20 Why social.plus, 25 Numbers band |
| F10 | Video | Features | 11 Two-column, video variant |
| F11 | Testimonial | Proof | 26 Quote carousel |
| F12 | Customer stories | Proof | 19 Customer story strip |
| F13 | Resource cards | Resources | 30 Thumbnail grid, 22 Explore more |
| F14 | FAQ | Conversion | 18 FAQ |
| F15 | CTA band | Conversion | G4 Footer CTA band, 23 CTA band (inline) |
| F16 | Footer | Global | G5 Footer |
| F17 | Page header | Heroes | 04 Article / Title header |
| F18 | Use case cards | Features | 16 Image-card grid |
| F19 | Industry list | Features | (none) |
| F20 | Stats | Proof | 25 Numbers band |
| F21 | Comparison table | Conversion | 52 vs / Comparison table |
| F22 | Pricing | Conversion | 60 Plan cards, 62 Additional fees |
| F23 | Contact form | Conversion | 24 Form section, the form of 53 |

Not framed yet, so these page types exist only in the current look: product and SDK pages (no framed sub-nav, G2), blog posts, answers, glossary entries and customer stories (no framed article body, 40 to 43; F17 covers only their header), and the pricing compare table (61). A framed version of these is proposed first, like any new section.

## Known points (TO CHECK)

- The library's icons are Phosphor (duotone in the icon tiles) and the platform marks are Simple Icons; the icons foundation still describes the live site's icons. Decide which set new pages use.
- The library hero uses weight 700 in places where the typography foundation took 600.
- Visuals, photos, customer logos, numbers (F20) and pricing tiers (F22) in the previews are the library's placeholders.
