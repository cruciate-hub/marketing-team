# Named companies, technologies and their logos

When the content is clearly about other companies or technologies, their logos belong in the image: they tell the reader at a glance what the piece covers. Examples: "How to build a social app in Flutter" → the Flutter logo; "The 6 best chat SDKs" → the six companies' logos; "Migrating from Firebase" → Firebase.

## 1. Decide from the whole content, not the title

Read the full article (or brief) and list every company, product, framework or platform it is *about* — the subject, the compared options, the integration target. Ignore passing mentions (a source cited once, an example in a footnote). Only use names that are certain from the text; never guess which companies a listicle covers from its title.

Typical cases:
| Content | Logos |
|---|---|
| Tutorial for a technology (Flutter, React Native, Swift, Unity) | that technology's logo, as the hero |
| Listicle / comparison of named products | all of them, equal size; social.plus included only if the article includes it |
| Integration or migration guide | both sides (e.g. the source platform and social.plus) |
| Industry or trend piece naming companies as examples | usually none — the point is the trend |

## 2. Get the official files — never draw a logo

Logos are always the companies' official artwork, placed as image assets. Never redraw, trace, approximate or "recreate in SVG" a logo from memory, and never invent a lookalike mark. Sources, in order:
1. Files the person attached in the chat.
2. A shared logo library in Google Drive, if connected (search for the company name + "logo", or a "Logos"/"Brand assets" folder).
3. Ask: "This article covers Flutter, Stream and Sendbird. Please share their official logos (SVG preferred, otherwise a transparent PNG at least 512px; a white/monochrome version if they have one)."

Until the files arrive, build the composition with neutral placeholder tiles and say which logos are missing; swap them in when they come. If a logo can't be obtained, use the company name set in Figtree on the tile instead — never a fake mark.

## 3. Treatment in the style

- **Monochrome first**: use the official white or single-colour version on dark tiles (#202022 or #1C1C1E), at #E6E6E6/white. This keeps the one-blue rule intact.
- **Full colour only when** the company provides no monochrome version, or the brand guidelines require colour. Then keep each logo small and on its own tile so the colours don't compete with the blue element; the blue element stays the only social.plus blue.
- Never recolour a logo to social.plus blue, never stretch, crop, rotate (beyond the composition's own perspective), add effects to, or combine logos.
- Equal visual weight for compared companies (same tile size, optically matched logo size); none highlighted unless the article ranks them — and then by position, not by recolouring.
- Clear space around each logo: at least the logo's own height ÷ 4.
- Follow each company's published brand guidelines when the person shares them; if a guideline conflicts with the style, the guideline wins.
- social.plus's own logo follows the social.plus design system.

## 4. Compositions that work with logos

- **Hero icon tile** — one big tile with the technology's logo (tutorials: Flutter, React Native), small UI fragments built with it around the edges.
- **Isometric grid / tile wall** — one logo per tile on a tilted plane (listicles, ecosystems).
- **Stack** — one company per card, logo in each card header (comparisons).
- **Device crop** — the app being built on a phone, with the framework's logo as a badge on the bezel or a floating tile.
- **Split frame** — two logos either side of a frame edge (migrations, "X vs Y").

## 5. Building and exporting

Upload each logo file as a canvas asset (`Artifact` publish with `asset: true`) and reference it by the `/_blob/<id>` url it returns, in an `<img>` with `alt` set to the company name. SVG and PNG both work. For exports with blog-thumbnails' script, read each asset back into the container (`Artifact` read with the asset id as `path`) and pass the folder with `--assets`.
