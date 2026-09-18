# HTML Conversion Rules — Google Doc → Webflow Rich Text

The Google Drive MCP returns the doc as markdown-like plain text. These rules
convert it to HTML for the `post-content` RichText field.

## What goes in post-content

Start at the first `###` heading (e.g. `### What Is an In-App Community Platform?`).
Stop just before the line that starts `Image alt text:`.

Do NOT include:
- The `# Listicle N` title line
- The metadata block at the top (Page title, Main Category Tag, Minutes to read, Meta description, Introduction text)
- The `Image alt text:`, `Image concept:`, `Image sizes needed:` lines
- The `Display recommendations:` block
- Any section marked `OUTREACH VERSION` or `INTERNAL USE ONLY`
- The `[OPTIONAL DISCLOSURE: ...]` line (omit entirely; user decides whether to include it)

## Heading conversion

| Doc format | HTML output | When to use |
|---|---|---|
| `### Heading text` | `<h2>Heading text</h2>` | Top-level sections |
| `#### Sub-heading` | `<h3>Sub-heading</h3>` | Sub-sections within a top section |
| `**Platform Name: tagline**` (at start of line) | `<h2>Platform Name: tagline</h2>` | Platform entries in listicles |

Place H2/H3 every 200–300 words to aid readability.

## Inline formatting

| Doc format | HTML |
|---|---|
| `**bold text**` | `<strong>bold text</strong>` |
| `*italic text*` | `<em>italic text</em>` |
| `[anchor text](url)` | `<a href="url" target="_blank">anchor text</a>` |
| Plain paragraph | `<p>paragraph text</p>` |

## Lists

Consecutive lines starting with `- ` or `  - `:

```html
<ul>
  <li>First item</li>
  <li>Second item</li>
</ul>
```

Numbered lists (lines starting with `1.`, `2.`, etc.):

```html
<ol>
  <li>First item</li>
  <li>Second item</li>
</ol>
```

Nest with `<ul>` inside `<li>` for indented sub-bullets.

## Tables

Markdown table format → HTML table:

```html
<table>
  <thead>
    <tr>
      <th>Column A</th>
      <th>Column B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cell 1</td>
      <td>Cell 2</td>
    </tr>
  </tbody>
</table>
```

Strip `**` bold markers from inside table cells — Webflow renders them as literal asterisks in table cells. Use plain text inside `<td>` and `<th>`.

Strip `\*\*` escaped asterisks (Google Doc export artifact) — convert to the actual text without asterisks.

## Inline images (full-width figures)

Every inline image in `post-content` **must** use Webflow's full-width figure structure.
A bare `<figure><img></figure>` renders at its intrinsic size (not full width) and is
not recognized as a Webflow image block. The correct format:

```html
<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth"
  style="max-width:1578px"
  data-rt-type="image"
  data-rt-align="fullwidth"
  data-rt-max-width="1578px">
  <div><img src="{url}" alt="{alt text}" loading="lazy"></div>
</figure>
```

All five attributes on `<figure>` are required:
- `class="w-richtext-figure-type-image w-richtext-align-fullwidth"` tells the
  RichText renderer this is a full-width image block.
- `style="max-width:1578px"` caps the rendered width at the content column.
- `data-rt-type="image"`, `data-rt-align="fullwidth"`, `data-rt-max-width="1578px"`
  are Webflow's internal markers that the Designer reads when an editor opens the post.

The `<img>` **must** be wrapped in a `<div>` inside the `<figure>`. Without that `<div>`,
Webflow silently strips the image on save in the Designer.

When using `blog-publisher.py`, the script replaces `__INLINE_IMG_N__` placeholders with
this format automatically. When building `post-content` by hand or via the Webflow MCP
directly, use this exact structure for every inline image.

## Platform entry structure in listicles

Each platform entry follows this pattern in the doc:

```
### **Platform Name: tagline**

[intro paragraphs]

Key strengths:

  - bullet
  - bullet

Considerations:

  - bullet
  - bullet

Pricing: [text]

Best fit: [text]
```

Convert to:

```html
<h3>Platform Name: tagline</h3>
<figure class="w-richtext-figure-type-image w-richtext-align-fullwidth"
  style="max-width:1578px"
  data-rt-type="image"
  data-rt-align="fullwidth"
  data-rt-max-width="1578px">
  <div><img src="{cdn-url}" alt="{alt text}" loading="lazy"></div>
</figure>
<p>[intro paragraph]</p>
<p>Key strengths:</p>
<ul>
  <li>bullet</li>
</ul>
<p>Considerations:</p>
<ul>
  <li>bullet</li>
</ul>
<p><strong>Pricing:</strong> [text]</p>
<p><strong>Best fit:</strong> [text]</p>
```

## Comparison table ("At-a-Glance")

The doc has a comparison table. Convert it as a standard HTML
`<table><thead><tbody>` with `<th>` for the header row and `<td>` for data cells.
Strip all `\*\*` from cell content — plain text only inside cells.

**The table sits inside a Webflow Embed.** `convert_table` wraps it as:

```html
<div data-rt-embed-type='true'><table><thead>…</thead><tbody>…</tbody></table></div>
```

That `data-rt-embed-type='true'` div is Webflow's marker for an Embed block inside rich
text. Why it matters: Webflow's Designer rich-text editor has no native table tool, so a
bare `<table>` is at risk of being mangled when an editor changes the post body and saves.
Inside an Embed the table is one opaque block — editors can freely change all the
surrounding prose (intros, H3 platform sections, headings) and the table survives; they
only touch it by double-clicking the embed. The live legal pages embed their fragile HTML
the same way. The `--dry-run` check `content:table-in-embed` enforces it.

**Table CSS does NOT go in post-content as a bare `<style>`.** Tried and reverted:
Webflow's RichText renderer shows a bare `<style>` block as literal text at the top of the
post. Table CSS lives in the site's custom code instead. The embedded table is still
`.w-richtext table` in the DOM, so that site CSS applies to it normally. The `--dry-run`
check `content:no-style-block` keeps a bare `<style>` out of post-content.

Table styling is owned by the **site**, not the CMS field. The reference CSS below
lives in a Webflow custom code field (page embed or site-wide `<head>` code),
maintained outside this skill. Scoped to `.w-richtext` so it only affects CMS tables:

```html
<style>.w-richtext table{width:100%;border-collapse:collapse;margin:1.5em 0;font-size:0.95em;}.w-richtext th,.w-richtext td{border:1px solid #d0d0d0;padding:0.75em 1em;text-align:left;vertical-align:top;}.w-richtext thead th{background-color:#f5f5f5;font-weight:600;}.w-richtext tbody tr:nth-child(even){background-color:#fafafa;}</style>
```

Always keep the `<table><thead><tbody>` structure intact — it must never collapse
into a paragraph (the `content:table-not-flattened` dry-run check guards this).

## "How to Choose" section

This section uses bold sub-headings inline (e.g. `**What you're building.**`).
Convert to `<p><strong>What you're building.</strong> [rest of paragraph]</p>`.

## Paragraph spacing

Blank lines in the doc → separate `<p>` tags. Do not use `<br>` for paragraph
breaks — always `<p>`.

## What the Webflow Data API keeps vs. drops

These behaviors are for the **Data API** RichText path (what this skill uses) —
they differ from the Designer paste flow.

Kept by the API:
- `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>`, `rowspan` — preserved.
- `<figure>` with the full Webflow figure class set (`w-richtext-figure-type-image
  w-richtext-align-fullwidth`) plus `data-rt-*` attributes — preserved as a full-width
  image block. A bare `<figure><img>` without these classes renders at intrinsic size
  (not full width). See the "Inline images" section above for the required format.
- `target="_blank"` on `<a>` — preserved; always include it for external links.
- The API technically preserves `<style>` blocks too — but DON'T use them (see below).

Never put in post-content:
- `<style>` blocks — the API keeps them, but the RichText renderer shows the CSS as
  literal text in the published post. Table CSS goes in the site's custom code instead.
- `<h1>` — the page title is already the H1.
- `<div>` wrappers — use `<p>` instead.
- `<script>` or `<iframe>` — not allowed in RichText.
- arbitrary `class` attributes — ignored (except the Webflow figure classes above).

## Compliance reminder

After conversion, apply the brain.md compliance check:
- No em dashes (`—`) → replace with comma, parentheses, or restructure the sentence
- No emojis in body text
- No forbidden terminology (see terminology.md)
