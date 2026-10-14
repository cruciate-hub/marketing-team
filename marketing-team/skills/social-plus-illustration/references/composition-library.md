# Composition library

The style (palette, grain, type, one accent, text budget) is constant. The composition is not. Two visuals side by side — in the blog grid, a social feed, a website page — should share a look but never a layout. This file is the menu: pick an archetype and a set of objects that fit the post, and that differ from the recent thumbnails (each surface's skill says how to find them).

## Archetypes

Each archetype is a different camera and arrangement, not a different decoration of the same layout.

| # | Archetype | Camera / arrangement | Typical objects | Best for |
|---|---|---|---|---|
| 1 | **Macro detail** | Extreme close-up on one control, 2–3× real size; one object fills half the frame, the rest is dark | a toggle, a single button, a cursor in a text field, a badge on an icon, a reaction | one feature, one decision, "the small thing that matters" |
| 2 | **Hero icon tile** | One big app-icon-style tile centred or slightly off, smaller UI fragments floating at the edges, cropped | icon tile + notification badge, 2–3 fragments (comment, invite, mention) | a product area (inbox, notifications, community), announcements |
| 3 | **Isometric grid** | Tilted plane of equal tiles filling the frame (CSS 3D: rotateX ~55°, rotateZ ~-45°), one tile different | feature tiles with icons or mono labels, SDK/logo tiles, empty slots | ecosystems, comparisons, "one of many", building blocks |
| 4 | **Selection overlay** | A design/editor canvas: selection frame with handles, component label, one or two named cursors, frame lines crossing the image | selection box, cursors with name pills, a component inside the frame | building, customising, collaboration, AI agents, "what's in scope" |
| 5 | **Split frame** | The image divided into two zones by a hard line or frame edge (left/right or top/bottom), different treatment each side | a light panel vs dark field, a before/after, a list vs a single item | contrasts, migrations, build vs buy |
| 6 | **Type-led field** | A full-bleed field of repeated short text (mono numbers, file names, labels) fading off; 2–4 items lit, one accent | text fragments only, no cards | data, scale, signals, "finding the one that matters" |
| 7 | **Stack / layers** | Cards stacked in depth (offset, scaled, fading back) or sheets peeling, seen at an angle | 3–6 identical surfaces, the front one detailed | volume, history, layers of infrastructure, versions |
| 8 | **Flow / path** | Objects strung along a diagonal or curved path crossing the frame, cropped at both ends | message bubbles, steps, avatars along a line, a chart line | journeys, funnels, growth, conversations over time |
| 9 | **Device crop** | A phone or window edge entering the frame at an angle, only a corner of the screen visible, UI inside at large scale | phone bezel corner, app header, composer | mobile experiences, in-app placement |
| 10 | **Wall + focal object** | A faded repeating pattern behind one large cropped object | pattern of units + one card | saturation, noise vs signal (used for "Push Notifications Have Hit a Ceiling") |

Variation within an archetype also counts: change the focal object, where the accent sits (top-left vs bottom-right vs centre), the crop edges, the scale.

## Object library

Pull from social.plus product vocabulary so images stay truthful. Vary the objects between posts as deliberately as the layout.

- **Controls:** toggle, primary button, segmented control, checkbox, radio, slider, text field with caret, composer with @ / emoji / attach icons, tooltip
- **Social units:** feed post, comment, reply thread, reaction chip, reaction burst, mention chip (@name), poll, story ring, live badge, member count chip
- **People:** avatar, avatar stack, profile card, named cursor pill, typing indicator
- **Structure:** app-icon tile, notification badge, inbox, sidebar, tab bar, modal, frame lines with plus markers, selection handles
- **Code and data:** terminal line, code block, file chips, mono number cells, chart line, metric tile (only numbers the post quotes)
- **Moderation and trust:** flag, shield, report menu, review queue row, blocked state, approve/decline pair

## Descriptive visuals (charts, flows, diagrams)

Some surfaces need to explain rather than evoke — in-blog images, explainer slides, docs. Then the archetype is a **chart** (one comparison or trend from real data, one accent series), a **flow** (steps as cards joined by dotted connectors, the accent card = the outcome), or a **system diagram** (labelled parts around a hub or in layers). More labels are allowed; the palette, grain rule and one-blue rule still hold. Details: blog-thumbnails' `in-blog-images.md`.

## Logo-led content

When the content is about named companies or technologies, their official logos are objects too — see `third-party-logos.md` for which archetypes carry them best (hero icon tile, isometric tile wall, stack, device crop, split frame).

## Composing well

- **One idea, one archetype.** Don't combine two archetypes in one image.
- **2–4 objects.** Count them. A pattern or field counts as one.
- **Different scales.** At least one object much bigger than the others.
- **Crop with intent.** Decide which edges each object leaves through; avoid the default "big card off bottom-right" unless the archetype calls for it.
- **Place the accent where the eye should land last or first**, and move it between posts (don't always put it bottom-left of a card).
- **Readability at 502px:** squint at the composition; the accent element and any readable word must survive.
