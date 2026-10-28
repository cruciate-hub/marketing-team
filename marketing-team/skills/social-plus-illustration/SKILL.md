---
name: social-plus-illustration
description: "The social.plus illustration system — dark, abstract, UI-led illustrations built in HTML/SVG from the design system's tokens. Use it for any social.plus visual that isn't a photo or a chart from real data: website section and feature illustrations, hero visuals, social posts and carousels, ad creatives, deck visuals, email images, and as the foundation for the blog-thumbnails and social-plus-motion skills (read this first whenever those run). Trigger on \"illustration\", \"visual for…\", \"image for the website/LinkedIn/Instagram\", \"hero image\", \"feature graphic\", \"make this look like our blog images\", even when the style isn't named."
---

# social.plus illustration system

One visual language for every surface. It shows social.plus's subject — people interacting inside apps — as simplified product UI: dark ground, neutral surfaces, one accent (ultramarine by default), big cropped objects, a trace of people (real faces from the avatar library, graded dark). Surfaces differ in format and treatment, never in language.

Other skills build on this one:
- **blog-thumbnails** — editorial images for blog posts (grain on)
- **social-plus-motion** — loops, reels and explainers (grain only when editorial)

## The fixed rules (read the references before drawing)

- `references/style-spec.md` — palette, type, shapes, recognisable objects, social layer, buttons. Exact values.
- `references/content-and-locale.md` — words on screen: what may be readable, American names and conventions, no invented facts.
- `references/avatar-library.md` — **every avatar photo comes from the design system's Avatars group** (graded faces, ready to use): how to pick them by the casting notes, copy them into the canvas by asset id, and read them back for export; adding new faces is maintenance only.
- `references/third-party-logos.md` — when the content is about other companies or technologies (Flutter, chat SDKs…), their official logos go in the image; how to get them and place them.
- `references/color-accents.md` — **one accent per image, chosen by meaning**: ultramarine for ~70% of images, other brand colors (green, purple, pink, orange, yellow, red) when the topic calls for them, with exact fills, text colors and glows.
- `references/treatments.md` — **grain is a treatment, not the style.** Editorial work gets grain; product, website and brand work is clean. Decide before building.
- `references/review-checklist.md` — run on every artboard before showing it.

In one breath: #111 ground, design-system neutrals for every surface, exactly one accent element — ultramarine (#3B41EC fill / #6F89FC line) by default, another brand color when the topic calls for it (`color-accents.md`) — Figtree (Geist Mono only for all-caps labels; code in the system monospace, captions and chips in Figtree: design-system feedback 17), words only where necessary, 2–4 big objects that leave the frame, recognisable objects with a quiet grey social layer, no duplicates of the blue action.

## What changes every time

Concept, composition archetype, objects, the position of the accent — and, by meaning, the accent color. `references/composition-library.md` lists 10 archetypes and the object vocabulary; `references/ideation.md` is how to get from a brief to two genuinely different concepts (10 ideas through 8 lenses, then converge). Never default to the last layout that worked.

## Workflow (any surface)

1. **Brief** — what is the visual for, where does it live (surface + size, `references/treatments.md` has the table), what is the one point it must make. If a page or post is provided, read all of it, and list the companies and technologies it is about (`references/third-party-logos.md`); ask for their official logo files early.
2. **Treatment and accent** — editorial (grain) or clean? Which accent color, by meaning and balance (`color-accents.md`)? Say both in one line.
3. **Ideate** — `references/ideation.md`. Show the idea table compactly, pick 2 concepts that differ in lens, archetype, focal object and accent position.
4. **Build** — on claude.ai, a Design canvas, one artboard per concept, social.plus design system installed. Start each artboard from `assets/shell.dc.html` (ground, glow, vignette, fonts, optional grain). Upload `assets/fonts/figtree.woff2` and `assets/fonts/geist-mono.woff2` as canvas assets and put their blob ids in the @font-face rules. Set the `grain` prop default to 0.9 for editorial, leave 0 for clean. Avatar photos: copy them from the design system's Avatars group into the canvas (`references/avatar-library.md`). Name artboards `Concept A — <archetype>: <focal object>`. The shell is sized 1578×888; for another size (e.g. an answer page, 1240×840) change the root, the grain SVGs and the vignette centre to that size.
5. **Review** — `references/review-checklist.md`, then present: one line per concept, a recommendation, the trade-off.
6. **Deliver** — PNG/WebP from the canvas at the surface's sizes, then present the files (with `present_files` on claude.ai; in Claude Code, give the output paths); motion via social-plus-motion.

`assets/examples/` holds finished pieces for craft reference only — never copy their layouts.

