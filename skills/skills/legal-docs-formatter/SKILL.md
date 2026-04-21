---
name: legal-docs-formatter
description: >
  Convert legal documents (Google Docs, Word, or pasted text) into clean HTML
  ready to paste into the Embed block inside a Rich Text field on a
  📜 Legals CMS item on social.plus. Use this skill for: Master Service
  Agreements (MSA), Data Processing Agreements (DPA), Service Level Agreements
  (SLA), Terms of Service, Privacy Policies, Acceptable Use Policies,
  definitions pages, cookie policies, or any other legal/contract content
  destined for pages under `/legal/` on social.plus. Also trigger when the user
  pastes legal copy and asks to convert, reformat, or prepare it for Webflow,
  or when they provide a Google Doc URL containing legal content. Trigger on
  phrases like "format this legal doc", "convert MSA to HTML", "Webflow HTML
  for DPA", "legal page for Webflow", "format for /legal/", "turn this into a
  legal page", "prep this contract for Webflow".
  Do NOT trigger for blog posts, marketing copy, landing pages, or product
  copy (use the corresponding content skill instead). Do NOT trigger for
  generic HTML conversion that isn't destined for a Webflow `.w-richtext`
  container.
---

# Legal Document → Webflow HTML Formatter

Convert legal documents into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item. The user does the copy-paste — this skill produces HTML only.

## Context

- Site: social.plus (project ID: `66e2765d540e1939a89db4bb`)
- CMS collection: 📜 Legals (collection ID: `66e2765d540e1939a89db772`)
- Legal pages live under `/legal/` (e.g. `/legal/msa-na`, `/legal/dpa`, `/legal/sla`)
- The HTML goes inside an Embed block nested in a Rich Text field on a CMS item — the Rich Text field renders wrapped in `.w-richtext`
- Font, text color, and base typography are inherited from Webflow — the HTML stays plain, with CSS only where Webflow's `.w-richtext` defaults break the intended formatting

## Critical Rule: Honor the Original Formatting

**Exact fidelity to the source document's formatting.** If the original uses:

- Bullet points → use `<ul>`
- A, B, C lettering → use `<ol type="A">` (uppercase) or `<ol type="a">` (lowercase)
- Numbered lists (1, 2, 3) → use `<ol>`
- Hierarchical numbering (1.1, 1.2, 2.1) → hardcode numbers in `<p>` tags (HTML `<ol>` cannot render hierarchical numbering natively)
- Tables → use `<table>` with `<thead>` and `<tbody>`

Never convert one list type to another. Never change A/B/C to bullet points or vice versa.

## Required `<style>` Block

Every output must start with a `<style>` block that overrides Webflow's `.w-richtext` CSS. Webflow applies a custom blue SVG `background-image` to ALL `<li>` elements, which breaks ordered list numbering and replaces normal bullet dots with branded icons.

### Base style block (always include)

```html
<style>
  .w-richtext ul { padding-left: 1.5em; }
  .w-richtext ul li { background-image: none !important; padding-left: 0 !important; list-style-type: disc; }
</style>
```

### If the document uses ordered lists, add

```html
  .w-richtext ol { padding-left: 1.5em; }
  .w-richtext ol li { background-image: none !important; padding-left: 0 !important; }
```

### If the document uses A/B/C lettering, add

```html
  .w-richtext ol[type="A"] { list-style-type: upper-alpha; }
```

### If the document uses a/b/c lettering, add

```html
  .w-richtext ol[type="a"] { list-style-type: lower-alpha; }
```

### If the document has tables, add

```html
  .w-richtext table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5em 0;
    font-size: 0.95em;
  }
  .w-richtext th,
  .w-richtext td {
    border: 1px solid #d0d0d0;
    padding: 0.75em 1em;
    text-align: left;
    vertical-align: top;
  }
  .w-richtext thead th {
    background-color: #f5f5f5;
    font-weight: 600;
  }
  .w-richtext tbody tr:nth-child(even) {
    background-color: #fafafa;
  }
```

## HTML Structure Rules

### Headings

- Document title: `<p><strong>Title</strong></p>` (not `<h1>` — that's reserved for the Webflow page title)
- Major sections (1, 2, 3...): `<h2>`
- Subsections (1.1, 1.2...): `<h3>`

### Hierarchical Numbering (1.1, 1.2, 2.1, etc.)

HTML `<ol>` cannot render hierarchical numbers. Hardcode them:

```html
<p><strong>1.1</strong> The parties agree that...</p>
<p><strong>1.2</strong> In the event of...</p>
```

### Lettered Lists (A, B, C)

Use the `type` attribute AND inline style (both are needed — Webflow's CSS overrides the `type` attribute alone):

```html
<ol type="A" style="list-style-type: upper-alpha;">
  <li>First item</li>
  <li>Second item</li>
</ol>
```

### Bullet Points

Standard `<ul>` — the style block handles the rest:

```html
<ul>
  <li>Item one</li>
  <li>Item two</li>
</ul>
```

### Tables with Row Spans

When a table groups rows (e.g. severity levels spanning Response + Resolution rows), use `rowspan`:

```html
<td rowspan="2"><strong>(S1) Critical</strong></td>
```

Remove empty columns that exist only as Google Docs formatting artifacts.

### Bold Terms / Definitions

Use `<strong>` inside `<p>`:

```html
<p><strong>Defined Term:</strong> The definition text goes here.</p>
```

### Links

Use standard `<a>` with `target="_blank"`:

```html
<a href="https://status.social.plus" target="_blank">status.social.plus</a>
```

### Centered Text (e.g. Annex headings)

Use inline style:

```html
<p style="text-align:center;"><strong>ANNEX I</strong></p>
```

## Do NOT

- Add any `font-family`, `color`, or `font-size` styling — inherited from Webflow.
- Use `<h1>` — reserved for the Webflow page title.
- Use CSS classes — the Embed inherits `.w-richtext` styles.
- Use `<ol>` for hierarchical numbering — hardcode the numbers in `<p>` tags.
- Trust that `<ol type="A">` alone will work — Webflow's CSS overrides it; you need the `<style>` block AND the inline `style="list-style-type: upper-alpha;"`.
- Add any JavaScript.
- Wrap the output in `<div>`, `<section>`, or any container — just start with `<style>` and then the content.

## Output Format

Deliver the full HTML in a single code block. Start with the `<style>` block and end with the last piece of content — no `<!DOCTYPE>`, no `<html>`, no `<head>`, no `<body>`, no wrapping `<div>`.

The user copies the HTML and pastes it into the Embed block inside the Rich Text field on the target 📜 Legals CMS item. That's the full workflow — the skill does not push to Webflow automatically.

## Live legal pages on social.plus

| Webflow Page | Entity / Purpose |
|---|---|
| /legal/msa-na | Master Service Agreement — Social Plus North America Inc. (Delaware) |
| /legal/msa-emea | Master Service Agreement — Social Plus Holdings Ltd (England & Wales) |
| /legal/msa-sea | Master Service Agreement — Social Plus SEA Co., Ltd. (Thailand) |
| /legal/dpa | Data Processing Agreement |
| /legal/sla | Service Level Agreement |
| /legal/definitions | Definitions and Overcharges Policy |

## Paste checklist (for the user)

After pasting into the Embed block:

- Bullets render as dots (not blue SVG icons).
- Ordered list numbers are visible (not replaced by icons).
- A/B/C lists show letters, not numbers.
- Tables show borders and zebra striping.
- No `<h1>` collides with the page title.
