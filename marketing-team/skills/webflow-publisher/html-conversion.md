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
`collections/<name>.json`. No HTML in the intermediate.

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

A GFM pipe table (leading whitespace tolerated; the `|---|` alignment row is dropped) becomes:

```html
<div data-rt-embed-type='true'><table><thead><tr><th>Column A</th><th>Column B</th></tr></thead><tbody><tr><td>Cell 1</td><td>Cell 2</td></tr></tbody></table></div>
```

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
  `content:no-script-or-iframe`.
- `<h1>` — the page title is already the H1.
- `<div>` wrappers other than the table Embed — use `<p>`.
- Arbitrary `class` attributes — ignored (except the Webflow figure classes above).

## Compliance reminder

Conversion is mechanical. The calling skill's `compliance.py` and the brain.md check
(no em dashes, no emojis, no forbidden terminology, no fabricated claims) run on the draft
**before** conversion; a clean conversion does not make a non-compliant draft publishable.
