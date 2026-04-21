# Legal Docs Formatter

Claude skill for converting legal documents (Google Docs, Word, pasted text) into clean HTML ready to paste into a Webflow Rich Text Embed block on a 📜 Legals CMS item on social.plus.

Handles Master Service Agreements (MSA), Data Processing Agreements (DPA), Service Level Agreements (SLA), Terms of Service, Privacy Policies, Acceptable Use Policies, definitions pages, and similar contract/legal content destined for pages under `/legal/`.

## What it does

- Produces HTML only. The user copies and pastes it into Webflow; the skill does not push to the CMS automatically.
- Preserves the source's exact formatting — bullets stay bullets, A/B/C stays A/B/C, 1.1/1.2 stays hierarchical.
- Emits a `<style>` block that overrides Webflow's `.w-richtext` defaults (Webflow applies a custom blue SVG `background-image` to all `<li>` elements, which breaks both ordered list numbering and standard bullet dots).
- Uses `<p><strong>Title</strong></p>` for the document title (never `<h1>` — reserved for Webflow's page title).
- Uses `<h2>` for major sections and `<h3>` for subsections.
- Hardcodes hierarchical numbering (1.1, 1.2, 2.1) in `<p>` tags because HTML `<ol>` cannot render it natively.
- Emits `<ol type="A">` with both the `type` attribute AND inline `list-style-type` (Webflow's CSS overrides the `type` attribute alone).
- Handles tables with `rowspan` for grouped rows and strips Google Docs formatting artifacts (empty columns).

## When it triggers

Any request to convert legal content into Webflow-ready HTML. Trigger phrases include "format this legal doc", "convert MSA to HTML", "Webflow HTML for DPA", "legal page for Webflow", "format for /legal/", "turn this into a legal page", "prep this contract for Webflow", or pasted legal content with defined terms, numbered clauses, or hierarchical sections.

## What it does NOT do

- Does not push to Webflow. Output is a code block; the user copies and pastes manually.
- Does not use CSS classes, `<h1>`, `<div>`, `<section>`, or any wrapping container — the output goes inside an Embed block that's already inside a `.w-richtext` Rich Text field.
- Does not emit a full HTML document — no `<!DOCTYPE>`, no `<html>`, no `<head>`, no `<body>`. Just `<style>` followed by the content.
- Does not add `font-family`, `color`, or `font-size` — all styling is inherited from Webflow.
- Does not add JavaScript.

## Workflow

1. Parse the source document — Google Doc URL via `google_drive_fetch`, or pasted text.
2. Identify formatting patterns: bullets, A/B/C, 1.1/1.2 hierarchy, tables, centered headings, bold definitions.
3. Emit the `<style>` block — base + conditional blocks for ordered lists, A/a lettering, tables.
4. Emit the content using `<p><strong>`, `<h2>`, `<h3>`, `<ul>`, `<ol>`, `<table>` per the source structure.
5. Deliver as a single code block. User pastes into the target Embed block.

## Reference: live legal pages

| Webflow Page | Entity / Purpose |
|---|---|
| /legal/msa-na | Master Service Agreement — Social Plus North America Inc. (Delaware) |
| /legal/msa-emea | Master Service Agreement — Social Plus Holdings Ltd (England & Wales) |
| /legal/msa-sea | Master Service Agreement — Social Plus SEA Co., Ltd. (Thailand) |
| /legal/dpa | Data Processing Agreement |
| /legal/sla | Service Level Agreement |
| /legal/definitions | Definitions and Overcharges Policy |

## Paste checklist

After pasting into the Embed block:

- Bullets render as dots (not blue SVG icons).
- Ordered list numbers are visible (not replaced by icons).
- A/B/C lists show letters, not numbers.
- Tables show borders and zebra striping.
- No `<h1>` collides with the page title.

## Files

```
legal-docs-formatter/
├── SKILL.md     Skill entry point — context, formatting rules, style block, output
└── README.md    This file
```
