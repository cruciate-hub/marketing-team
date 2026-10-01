# HTML Conversion Rules — Markdown intermediate → Webflow Rich Text

`scripts/md_to_webflow_html.py` converts the common markdown intermediate into HTML for a
collection's RichText body field and builds the rest of `fielddata.json` from the field
map. This document describes what it emits and why; the script is the source of truth.
Google-Doc-export specifics (the `# Listicle N` / `### **Platform: tagline**` shape) are
normalized *into* this intermediate by `scripts/gdoc_to_fielddata.py` and documented in
`blog-publisher/SKILL.md`.

## The intermediate

```
# Title                       ← the only H1; becomes the CMS item name

Meta description: …           ← contiguous `Label: value` block directly under the H1.
Slug: …                          A wrapped value continues on the next line. Unknown labels
Alt text: …                      are kept and reported as "unmapped" (e.g. aeo-content's
Category: …                      `Intent:`), never treated as body text.
Tags: …

[first paragraph]             ← lifted into `fields.intro` when the map declares one
                                 (blog → post-summary, PlainText, markdown stripped);
                                 stays in the body otherwise (glossary definition paragraph)

## Section …                  ← body
```

Which labels map to which CMS field, and which are required, is decided per collection in
that content-type skill's own `webflow-fields.json` (schema: `field-map-schema.md`). No HTML
in the intermediate.

## Heading conversion

| Intermediate | HTML |
|---|---|
| `## Heading` | `<h2>Heading</h2>` |
| `### Sub-heading` | `<h3>Sub-heading</h3>` |
| `#### …` | `<h4>…</h4>` (h5/h6 likewise) |
| `# Heading` inside the body | emitted as `<h1>` **with a warning**; the dry-run fails `content:no-h1`. The title is the page's only H1. |

Place H2/H3 every 200–300 words to aid readability (writing-skill rule, not enforced here).

## Inline formatting

| Intermediate | HTML |
|---|---|
| `**bold text**` | `<strong>bold text</strong>` |
| `*italic text*` | `<em>italic text</em>` |
| `[anchor](https://external.example)` | `<a href="…" target="_blank">anchor</a>` |
| `[anchor](https://www.social.plus/…)` or `[anchor](/path)` | `<a href="…">anchor</a>` — **internal links open in the same tab** |
| Plain paragraph (consecutive lines joined with a space) | `<p>paragraph text</p>` |
| `\*\*` / `\~` (Google Docs export artifacts) | unescaped |

Blank lines separate paragraphs; never `<br>`.

## Lists

```
- item                      <ul><li>item</li>
  - nested item               <li>…<ul><li>nested item</li></ul></li></ul>
1. step                     <ol><li>step</li></ol>
```

An indented run with no parent bullet (e.g. `  - …` under a plain "Key strengths:"
paragraph) stays a flat `<ul>`. A blank line ends a list.

## Tables

A GFM pipe table (leading whitespace tolerated; the `|---|` alignment row is dropped) becomes
the **table standard** (Stefan, 2026-09-29):

```html
<div data-rt-embed-type='true'><div style="overflow-x:auto;-webkit-overflow-scrolling:touch;margin-bottom:2rem"><table style="margin-bottom:0 !important"><caption style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0">Heading above the table</caption><thead><tr><th scope="col">Column A</th><th scope="col">Column B</th></tr></thead><tbody><tr><th scope="row" style="background:transparent !important">Row label</th><td>Cell</td></tr></tbody></table></div></div>
```

- **Why the inline styles.** A site-wide hidden embed sets `table{margin-bottom:.5rem
  !important}` and `th{background-color:#2a2a2a !important; color:#fff !important}`, so the next
  paragraph sat glued to the table and row labels looked like header cells; there was no mobile
  scroll either. Only inline `!important` beats that CSS. The wrapper scrolls a wide table
  sideways on a phone (the page itself never scrolls sideways) and leaves a 32px gap below it.
- **Caption and header cells.** The visually hidden `<caption>` says what the table compares:
  the converter uses the nearest heading above the table, or the column names when there is
  none. Column headers get `scope="col"`; the first cell of each body row is the row label,
  a `scope="row"` header with a transparent background. The dry-run check
  `content:table-standard` fails any table without the wrapper, `margin-bottom:0` and a caption.
- **Check after publishing:** a 375px-wide viewport shows no sideways page scroll and a 32px
  gap under each table. Reference post: /blog/api-vs-sdk-which-is-which (29 Sep 2026).

- **The table sits inside a Webflow Embed.** `data-rt-embed-type='true'` is Webflow's marker
  for an Embed block inside rich text. The Designer's rich-text editor has no native table
  tool, so a bare `<table>` is at risk of being mangled when an editor changes the post body
  and saves. Inside an Embed the table is one opaque block — editors can change all the
  surrounding prose and the table survives; they only touch it by double-clicking the embed.
  The live legal pages embed their fragile HTML the same way. The dry-run check
  `content:table-in-embed` enforces it for **every** table.
- **Bold markers are stripped inside cells** — Webflow renders them as literal asterisks in
  table cells. Plain text only inside `<td>`/`<th>`.
- **Table CSS does NOT go in the body as a bare `<style>`.** Tried and reverted: Webflow's
  RichText renderer shows a bare `<style>` block as literal text at the top of the post.
  Table styling is owned by the **site** (a Webflow custom code field / page embed,
  maintained outside this skill); the embedded table is still `.w-richtext table` in the
  DOM so that CSS applies. The dry-run check `content:no-style-block` keeps `<style>` out.
  Reference CSS for the site:

  ```html
  <style>.w-richtext table{width:100%;border-collapse:collapse;margin:1.5em 0;font-size:0.95em;}.w-richtext th,.w-richtext td{border:1px solid #d0d0d0;padding:0.75em 1em;text-align:left;vertical-align:top;}.w-richtext thead th{background-color:#f5f5f5;font-weight:600;}.w-richtext tbody tr:nth-child(even){background-color:#fafafa;}</style>
  ```

- **Never let a table collapse into a paragraph.** The dry-run check
  `content:table-not-flattened` fails on any `<p>` carrying `| … |` / `|---` syntax and, when
  `--source <draft.md>` is passed, on fewer `<table>` elements than table blocks in the
  source. It is structural — it does not care what the heading above the table says (the
  old check only fired under "At-a-Glance"/"Comparison", which is why a glossary "Metrics"
  table could have shipped flattened).

## Inline images (full-width figures)

An image line `![alt](anything)` — or a bare `__INLINE_IMG_N__` line — becomes a placeholder
numbered in document order. At publish time `webflow-publisher.py` uploads the matching
`--inline` file and replaces the placeholder with Webflow's full-width figure:

```html
<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth"
  style="max-width:1578px"
  data-rt-type="image"
  data-rt-align="fullwidth"
  data-rt-max-width="1578px">
  <div><img alt="__wf_reserved_inherit" src="{url}" loading="lazy"></div>
</figure>
```

All five attributes on `<figure>` are required (a bare `<figure><img>` renders at intrinsic
size and is not recognized as a Webflow image block), the `<img>` **must** be wrapped in a
`<div>` (without it the Designer silently strips the image on save), and `max-width` comes
from the collection's `inline_images.width`. `alt="__wf_reserved_inherit"` matches
production; the real alt text lives in the collection's standalone alt-text field. The
dry-run check `content:placeholders-match-inline` requires exactly one `--inline` file per
placeholder.

## Images and videos carried over from the live post

A rewrite keeps every image and video of the live post (Stefan, 2026-09-29: never drop one
silently; only the reviewer may remove one). Copy each live `<figure>…</figure>` block into
the draft at its matching section, on its own lines. The converter passes it through
unchanged (`carried-over figures` in the conversion summary), and `webflow-publisher.py
--replace` refuses to run when a live figure is missing from the new body. A video figure
(`data-rt-type="video"` with its `<iframe>`) is the one place an `<iframe>` may appear.

## FAQ schema (FAQPage JSON-LD)

When the field map sets `"faq_schema": true` (blog and answers; their templates emit only
Article + Organization JSON-LD), the converter finds the first H2 that reads "FAQ", "FAQs" or
"Frequently asked questions…", takes each H3 under it as a question and the paragraphs and
list items up to the next H3 as its answer (plain text, links dropped), and appends one embed
at the very end of the body:

```html
<div data-rt-embed-type='true'><script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[…]}</script></div>
```

Question and answer text come from the same markdown as the visible FAQ, so they always match
it. The glossary template already emits FAQPage, so the glossary map leaves `faq_schema` off
(two FAQPage blocks on one page would conflict). The dry-run check `content:faq-schema` fails
a body with an FAQ section but no parsable FAQPage embed, or an embed without an FAQ section.

## Other blocks

| Intermediate | HTML |
|---|---|
| `> quote` | `<blockquote><p>quote</p></blockquote>` |
| `---` alone | dropped (no rich-text equivalent) |

## Slugs

`Slug:` line > `--slug` override > derived from the title, all subject to the collection's
`slug_rules`: `strip_years` removes every `19xx`/`20xx` token (`top-1000-apps` survives),
`strip_leading_count` removes a leading `6-`/`five-` (blog only). A collision is never
resolved by appending anything — see the NON-NEGOTIABLE rules.

## What the Webflow Data API keeps vs. drops

These behaviors are for the **Data API** RichText path — they differ from the Designer paste flow.

Kept by the API:
- `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>`, `rowspan` — preserved (inside the Embed div).
- `<figure>` with the full Webflow class set plus `data-rt-*` attributes — preserved as a
  full-width image block.
- `target="_blank"` on `<a>` — preserved; the converter sets it for external links only.
- `<style>` blocks — technically preserved, but DON'T use them (rendered as literal text).

Never put in the body:
- `<style>`, `<script>`, `<iframe>` — the dry-run fails `content:no-style-block` /
  `content:no-script-or-iframe`. Exceptions: the FAQPage JSON-LD embed the converter appends,
  and a video `<figure>` carried over from the live post.
- `<h1>` — the page title is already the H1.
- `<div>` wrappers other than the table Embed and its scroll wrapper — use `<p>`.
- Arbitrary `class` attributes — ignored (except the Webflow figure classes above).

## Compliance reminder

Conversion is mechanical. The calling skill's `compliance.py` and the brain.md check
(no em dashes, no emojis, no forbidden terminology, no fabricated claims) run on the draft
**before** conversion; a clean conversion does not make a non-compliant draft publishable.
