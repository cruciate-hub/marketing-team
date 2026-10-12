# Figma hand-off

How Claude turns a page built with the design system into a Figma file a designer can work in: editable layers, the design system's colours as variables, its parts as components. Tested on the Agentry page, 12 October 2026 (https://www.figma.com/design/aJx3urkr7Jy4j6cvPyEIQe). Figma cannot import a web page, so Claude rebuilds the page from its markup with the Figma connector.

- Status: in use since 12 October 2026 · Owner: Stefan · Designer: Victoria
- Every rule in `../feedback.md` holds in Figma too; items 7 to 11 came from this hand-off.

## What Claude builds

1. **Source.** The page as published (the Claude Design canvas), the sections' `source.html` and `sections/framed/framed.css`. Never memory or a screenshot. Texts, icons, buttons and the "Works in" list are copied from the page; a fact the page lacks is not added in Figma.
2. **Variables.** One collection, "social.plus · roles (dark)", with the role colours from `claude-design/tokens.json` under their token names (`color-bg`, `color-text`, `color-link` …). Every fill, stroke and text colour is bound to a variable.
3. **No components sheet.** The file holds the page frame and, to its right, the hidden tab panels and the open FAQ; nothing else. Never build a sheet of components ("Components · …") in a hand-off file: parts stay plain, editable layers with the colour variables. Shared components come only from a published social.plus Figma library, once it exists. Decision: Stefan, 12 October 2026.
4. **Page frame.** 1440 wide; one auto-layout frame per section, named like the section ("F06 Feature tabs"). Buttons follow definition of done point 5: in each group the first is blue, every one after it grey (secondary).
5. **Hidden tab panels and FAQ answers go to the right.** Content a visitor reaches only by switching a tab (Feature tabs: the other tabs, each active with its panel showing) gets its own frame to the right of the page frame (160 px gap), level with its section, as wide as the section and named after the tab ("F06 Feature tabs · Audience understanding (tab 2 active)"). The FAQ gets one frame with every answer open ("F14 FAQ · every answer open"; approved by Stefan, 12 October 2026). Nothing else: no open menus, no form states, no extra variants. Anything beyond what the page shows right away is added only when Stefan asks for it. Decision: Stefan, 12 October 2026.
5b. **Details drawn by the stylesheet, not the markup.** `framed.css` draws some parts with CSS only (`::before`/`::after`), so they are not in the page's HTML: the plus markers (11 px, `color-frame-marker`) where each section's top rule crosses the two frame lines, and the single rule under the navigation. Build them too; check `framed.css` for every section used.
6. **Visuals.** A mockup the section shows (chat, app screen, stats) is rebuilt as editable layers with its "Illustrative example" tag. An `Image slot` only where the page itself has an image placeholder; its brief says what goes there and the size.
7. **Icons and logos.** The page's own SVGs, copied from its markup; never chosen again in Figma. The social.plus logo and third-party logos only from the approved files (`../foundations/logo/foundation.md`).
8. **Fonts.** Figtree for everything, Geist Mono for eyebrows and code. Figma's Figtree is Google's version; install our build (`../figtree.woff2`) on the designer's machine so the letters match the site.
9. **Clean-up.** New auto-layout frames get a white fill by default; Claude removes every fill that is not bound to a variable.
10. **Check before handing over.** Screenshot the page frame, compare it with the page at 1440, go through `../feedback.md` item by item and list every mismatch in the reply ("none found" counts).

## The way back

The designer changes the Figma file. Claude reads the changed frames (screenshot and layer data) and makes the same change on the page and, when it is a rule, in the section's source and `../feedback.md`, the same day, in one pull request. Images the designer places go into the asset store of the page and `assets/media/`.

## Known limits

- No published social.plus Figma library yet: the colour variables live in each file and the parts are plain layers. A library is a separate decision for Stefan.
- The way back is not tested yet (first test: Victoria places one visual in the Agentry file).
