# Framed sections

The section set on the web library's frame (Amadeus, decision 8 October 2026): 16 sections taken unchanged from the library's page demo on 12 October 2026. They replace the captured sections on a framed page; the captured sections stay as the record of the live site. Not yet in Webflow.

- Status: draft (2026-10-12) · Owner: Amadeus · Approved by: TO CHECK (Stefan or Amadeus)
- Source: the web library (https://claude.ai/artifact/PhSYGn8yxneLKrCxCgeWmd), its page demo
- Files: `framed.css` (the library's stylesheet, one copy for all sections), and per section `source.html` (links `../../../tokens.css` and `../framed.css`; no scripts, interactive parts in their first state) and `section.md`
- On the Claude Design page: the groups "Framed · …"; `framed.css` is `components/framed.css` there

## The rule

A page is framed or captured, never both. A framed page uses only framed sections, on one frame from the navigation to the footer; a captured section is never wrapped in the frame. Build framed where the page type has a framed recipe (today: `../recipes/product-landing-framed.md`); other page types stay captured until their framed sections are here.

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

Still only in the library (next): page header, use case cards, industry list, stats, comparison table, pricing, contact form. Until they are here, the blog, answer, glossary, customer story, /vs/ and pricing pages stay captured.

## Known points (TO CHECK)

- The library's icons are Phosphor (duotone in the icon tiles) and the platform marks are Simple Icons; the icons foundation still describes the live site's icons. Decide which set new pages use.
- The library hero uses weight 700 in places where the typography foundation took 600.
- Visuals, photos and customer logos in the previews are the library's placeholders.
