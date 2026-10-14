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

## Self-contained by design

Unlike most skills in this kit, these three don't fetch the repo: they also run as claude.ai skills, so they carry their own copies of the fonts and write colour values out in full. Two scripts keep them current:

- `scripts/illustration_skills_check.py` (runs in CI) fails when the copies drift from `design-system/`: the fonts must be byte-identical to `design-system/figtree.woff2` and `geist-mono.woff2`, every "token `#hex`" pair must match `sections/framed/framed.css`, and every colour must be a design-system value or one of four listed exceptions (chart grid lines, tick labels, logo tiles).
- `scripts/import_skills.py <file.skill | bundle.zip>` brings in a new export from claude.ai: it replaces the repo copy of each skill it contains, shows what changed and runs the check. Then bump the plugin version and CHANGELOG as for any skill change. The skills can equally be edited here through a pull request.

If the design system changes a token these skills use, the check fails until the skills are updated to match.
