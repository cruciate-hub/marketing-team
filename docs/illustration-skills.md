# Illustration skills

Three skills by Amadeus for social.plus visuals, added on 14 October 2026:

| Skill | For |
|---|---|
| `social-plus-illustration` | The visual language and method for every surface: website, social posts and carousels, ads, decks, email. The other two build on it. |
| `blog-thumbnails` | Blog headers and thumbnails, in-blog charts, flows and diagrams, answer-page and glossary images. |
| `social-plus-motion` | Loops of a finished static (animated WebP or GIF) and explainer videos (Reels, TikTok, LinkedIn) from an article. |

Since 14 October 2026 these skills are how social.plus makes illustrations and blog, answers and glossary images. Where `design-system/foundations/imagery/foundation.md` differs, the skills win (the foundation says which of its rules they replace).

## How they work

- **Where:** on claude.ai. Statics are built on a Design canvas (one artboard per concept, started from `social-plus-illustration/assets/shell.dc.html`), motion with the Motion artifact type. The social.plus design system is installed in Claude Design.
- **Method:** a brief, then the treatment (grain for editorial work, clean for website, product and brand work) and one accent colour chosen by meaning, then ten ideas through eight lenses, two concepts that differ in layout, focal object and accent position, a review checklist, and delivery.
- **Blog files:** `blog-thumbnails/scripts/export_blog_images.py` renders the chosen artboard to the three WebP files the Webflow blog collection requires (`{slug}_page-header_1578x888.webp`, `{slug}_thumbnail_724x408.webp`, `{slug}_mega-menu_502x283.webp`) or an in-blog image (`--inline N`). Those are the files `webflow-publisher` uploads.
- **Motion files:** MP4 from the Motion page's Export button; animated WebP with `social-plus-motion/scripts/render_webp.py`; frame checks with `contact_sheet.py`; GIF from the MP4 via `video-to-gif-and-webp`.
- **Script needs:** Python 3 with Playwright (Chromium) and Pillow; `render_webp.py` also needs ffmpeg with `libwebp_anim`.
- **Answers and glossary images:** the export script knows only the blog sizes and in-blog images (1578 × 888). An answers image (field `image-2`, 1240 × 840) is exported from the canvas at that size and converted to WebP separately. The Glossary collection has no image field, so a glossary image goes in the body as an in-blog style figure (`--inline 1`).

## Self-contained by design

Unlike most skills in this kit, these three don't fetch the repo: they also run as claude.ai skills, so they carry their own copies of the fonts and write colour values out in full. Two scripts keep them current:

- `scripts/illustration_skills_check.py` (runs in CI) fails when the copies drift from `design-system/`: the fonts must be byte-identical to `design-system/figtree.woff2` and `geist-mono.woff2`, every token named with its value (either order) must match `sections/framed/framed.css` (22 tokens today), every colour in the references, the shell and the examples must be a design-system value or one of seven listed exceptions (chart grid lines, tick labels, logo tiles, three colours in the motion examples), and every `assets/`, `references/` or `scripts/` path the text names must exist.
- `scripts/import_skills.py <file.skill | bundle.zip>` brings in a new export from claude.ai: it replaces the repo copy of each skill it contains, shows what changed and runs the check. Then bump the plugin version and CHANGELOG as for any skill change. The skills can equally be edited here through a pull request.

If the design system changes a token these skills use, the check fails until the skills are updated to match.

## Notes for Amadeus's next version

Fixed here (14 October 2026), so a new export must keep it: `style-spec.md` pointed to `assets/figtree.woff2`; the file is `assets/fonts/figtree.woff2` (the check now fails on any file path that doesn't exist).

Things in the skill text itself, left as exported:
- `social-plus-illustration/SKILL.md` ends "until the imagery foundation is updated, say which rule you applied"; the foundation now defers to the skills (14 October 2026).
- `blog-thumbnails` lists glossary images at 1578 × 888, but the Glossary collection has no image field (inline only), and its export script has no 1240 × 840 answers size.
