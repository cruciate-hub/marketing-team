#!/usr/bin/env python3
"""
md_to_webflow_html.py — convert a markdown intermediate into Webflow CMS fielddata.json
for any collection described by a field map (each content-type skill's own
webflow-fields.json — schema documented in webflow-publisher/field-map-schema.md).

This is the shared, collection-agnostic half of publishing. Content-type skills
(blog-seo-content, glossary-content, aeo-content, …) already produce this shape as their
compliance-checked draft, so no new format is needed:

    # Title                       ← the only H1 → CMS item name

    Meta description: …           ← contiguous `Label: value` block directly under the H1
    Slug: …                          (the field map decides which labels map to which slug)
    Category: …

    [first paragraph]             ← lifted into fields.intro when the map declares one
                                     (blog: post-summary); otherwise stays in the body

    ## Section → <h2>   ### → <h3>   #### → <h4>
    paragraphs, **bold**, *italic*, [links](url), - bullets, 1. numbered, > quotes
    | GFM | tables |  →  <div data-rt-embed-type='true'><table>…</table></div>
    ![alt](anything)  →  __INLINE_IMG_N__   (a bare __INLINE_IMG_N__ line is accepted too)

Usage:
    python3 scripts/md_to_webflow_html.py <draft.md> --collection <name> --out <fielddata.json>
    python3 scripts/md_to_webflow_html.py <draft.md> --field-map <map.json> --out <fielddata.json>
        [--slug <slug>]        override the slug (still subject to the collection's slug rules)
        [--date <iso8601>]     value for fields.date (default: now, UTC)
        [--report <path>]      also write a JSON conversion report (tables, placeholders, warnings)
    python3 scripts/md_to_webflow_html.py <draft.md> --html-only
        print only the converted body HTML to stdout (no field map needed)

Values whose CMS slug is still null in the field map are parked under "__unconfirmed__"
in the output so nothing is lost; webflow-publisher.py refuses to publish while that key
exists. Exit codes: 0 ok, 1 on any parse/validation failure (message on stderr).

Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from webflow_fieldmap import FieldMapError, load_field_map, unconfirmed_slugs  # noqa: E402

# ── Link policy ─────────────────────────────────────────────────────────────────
# Internal links open in the same tab; only external links get target="_blank"
# (html-conversion.md: "always include it for external links"; blog-seo-content:
# internal links "without target=_blank"). Same host test as the dry-run's internal-link count.
INTERNAL_HREF_RE = re.compile(r"^(?:/|#|https?://(?:www\.)?social\.plus(?:[/?#]|$))", re.IGNORECASE)


def render_link(url: str, text: str) -> str:
    url = url.strip()
    if INTERNAL_HREF_RE.match(url):
        return f'<a href="{url}">{text}</a>'
    return f'<a href="{url}" target="_blank">{text}</a>'


# ── Inline formatting ───────────────────────────────────────────────────────────

def _unescape_export_artifacts(text: str) -> str:
    """Google-Docs export writes \\*\\* for literal asterisks and \\~ for tildes."""
    return text.replace("\\*\\*", "**").replace("\\\\~", "~").replace("\\~", "~")


def clean_inline(text: str) -> str:
    """Markdown-ish inline → HTML. Used for paragraphs, list items, headings."""
    text = _unescape_export_artifacts(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", lambda m: render_link(m.group(2), m.group(1)), text)
    return text.strip()


def clean_cell(text: str) -> str:
    """Table cells render bold markers literally in Webflow — strip them to plain text."""
    text = text.replace("\\*\\*", "").replace("\\\\~", "~").replace("\\~", "~")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return text.strip()


def to_plain_text(text: str) -> str:
    """Markdown → plain text for PlainText CMS fields (meta description, summary, alt)."""
    text = _unescape_export_artifacts(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*", r"\1", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"\1", text)
    return text.strip()


# ── Tables ──────────────────────────────────────────────────────────────────────
# Webflow's marker for an Embed block inside a RichText field. Wrapping the table in this
# makes it an opaque embed in the Designer: editors can change all the surrounding prose
# and save without the rich-text editor mangling the table — it has no native table tool,
# so a bare <table> is at risk on a Designer save. The table is still `.w-richtext table`
# in the DOM, so the site's table CSS still applies. Confirmed against the live legal
# pages, which embed their fragile HTML the same way.
RT_EMBED_OPEN  = "<div data-rt-embed-type='true'>"
RT_EMBED_CLOSE = "</div>"

TABLE_LINE_RE      = re.compile(r"^\s*\|")
TABLE_ALIGN_ROW_RE = re.compile(r"^\s*\|[\s:\-|]+\|\s*$")


def convert_table(table_lines: list) -> str:
    rows = []
    for line in table_lines:
        if TABLE_ALIGN_ROW_RE.match(line):                 # alignment row
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(not c.replace(" ", "") for c in cells):     # empty row
            continue
        rows.append(cells)
    if not rows:
        return ""
    thead = "<thead><tr>" + "".join(f"<th>{clean_cell(c)}</th>" for c in rows[0]) + "</tr></thead>"
    tbody = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{clean_cell(c)}</td>" for c in r) + "</tr>" for r in rows[1:]
    ) + "</tbody>"
    # Wrap in a Webflow Embed so the rest of the post stays safely editable in the Designer.
    return f"{RT_EMBED_OPEN}<table>{thead}{tbody}</table>{RT_EMBED_CLOSE}"


# NOTE: never inject a <style> block into the body. The Data API preserves <style>, but
# Webflow's RichText renderer shows the CSS as literal text at the top of the post. Table
# CSS is owned by the site (custom code), not the CMS field — see html-conversion.md.


# ── Body → HTML ─────────────────────────────────────────────────────────────────

HEADING_RE     = re.compile(r"^(#{1,6})\s+(.+)$")
BULLET_RE      = re.compile(r"^(\s*)[-*]\s+(.*)$")
NUMBERED_RE    = re.compile(r"^(\s*)\d+[.)]\s+(.*)$")
IMAGE_LINE_RE  = re.compile(r"^\s*!\[([^\]]*)\]\(([^)]*)\)\s*$")
PLACEHOLDER_RE = re.compile(r"^\s*(__INLINE_IMG_\d+__)\s*$")
QUOTE_RE       = re.compile(r"^\s*>\s?(.*)$")
HRULE_RE       = re.compile(r"^\s*(?:-{3,}|\*{3,}|_{3,})\s*$")


def is_block_start(line: str) -> bool:
    """Lines that terminate a paragraph and start another block."""
    return bool(
        not line.strip()
        or HEADING_RE.match(line)
        or TABLE_LINE_RE.match(line)
        or BULLET_RE.match(line)
        or NUMBERED_RE.match(line)
        or IMAGE_LINE_RE.match(line)
        or PLACEHOLDER_RE.match(line)
        or QUOTE_RE.match(line)
        or HRULE_RE.match(line)
    )


_is_block_start = is_block_start  # backwards-compatible alias


def _convert_list(lines: list, i: int, item_re, tag: str) -> tuple:
    """Consume a list starting at lines[i]. The first item's indent is the list's base level;
    an item indented deeper than that nests one level under the previous top-level item.
    Equally indented items are siblings, so a `  - ` run under a plain "Key strengths:"
    paragraph (no parent bullet) stays a flat list. A blank line ends the list and is consumed."""
    items = []  # [text, [children]]
    base = None
    while i < len(lines):
        l = lines[i].rstrip()
        m = item_re.match(l)
        if m:
            indent, text = len(m.group(1).expandtabs(4)), clean_inline(m.group(2))
            if base is None:
                base = indent
            if indent > base and items:
                items[-1][1].append(text)
            else:
                items.append([text, []])
            i += 1
        elif not l:
            i += 1
            break
        else:
            break
    out = []
    for text, children in items:
        if children:
            out.append(f"<li>{text}<{tag}>" + "".join(f"<li>{c}</li>" for c in children) + f"</{tag}></li>")
        else:
            out.append(f"<li>{text}</li>")
    return f"<{tag}>" + "".join(out) + f"</{tag}>", i


def convert_body(raw: str) -> dict:
    """
    Body markdown → Webflow rich-text HTML.
    Returns {"html", "placeholders" (count), "tables" (count), "warnings" [..]}.
    Image lines become __INLINE_IMG_N__ placeholders numbered in document order; a bare
    placeholder line is passed through as-is (that is how the blog adapter marks the
    image slot after each platform heading).
    """
    lines, html, i = raw.split("\n"), [], 0
    n_img, n_tbl, warnings = 0, 0, []
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue

        if TABLE_LINE_RE.match(line):                       # table block
            tbl = []
            while i < len(lines) and TABLE_LINE_RE.match(lines[i].rstrip()):
                tbl.append(lines[i].rstrip()); i += 1
            t = convert_table(tbl)
            if t:
                html.append(t); n_tbl += 1
            continue

        m = PLACEHOLDER_RE.match(line)                       # bare inline-image placeholder
        if m:
            html.append(m.group(1)); n_img += 1
            i += 1; continue

        m = IMAGE_LINE_RE.match(line)                        # ![alt](url) → placeholder
        if m:
            n_img += 1
            html.append(f"__INLINE_IMG_{n_img}__")
            i += 1; continue

        m = HEADING_RE.match(line)                           # headings
        if m:
            level = len(m.group(1))
            if level == 1:
                warnings.append(f"H1 in body ('{m.group(2)[:40]}') — the title is the only H1; "
                                "the dry-run will fail content:no-h1")
            html.append(f"<h{level}>{clean_inline(m.group(2))}</h{level}>")
            i += 1; continue

        if HRULE_RE.match(line):                             # --- : drop (no rich-text equivalent)
            i += 1; continue

        if BULLET_RE.match(line):                            # bullet list
            block, i = _convert_list(lines, i, BULLET_RE, "ul")
            html.append(block); continue

        if NUMBERED_RE.match(line):                          # numbered list
            block, i = _convert_list(lines, i, NUMBERED_RE, "ol")
            html.append(block); continue

        if QUOTE_RE.match(line):                             # blockquote
            q = []
            while i < len(lines) and QUOTE_RE.match(lines[i].rstrip()):
                q.append(QUOTE_RE.match(lines[i].rstrip()).group(1)); i += 1
            html.append(f"<blockquote><p>{clean_inline(' '.join(x for x in q if x))}</p></blockquote>")
            continue

        para = []                                            # paragraph
        while i < len(lines):
            l = lines[i].rstrip()
            if _is_block_start(l):
                break
            para.append(l); i += 1
        if para:
            html.append(f"<p>{clean_inline(' '.join(para))}</p>")

    return {"html": "".join(html), "placeholders": n_img, "tables": n_tbl, "warnings": warnings}


def count_source_tables(markdown: str) -> int:
    """Number of GFM table blocks in a markdown source (same shape convert_body consumes)."""
    n, in_tbl = 0, False
    for line in markdown.split("\n"):
        is_tbl = bool(TABLE_LINE_RE.match(line.rstrip())) and bool(line.strip())
        if is_tbl and not in_tbl:
            n += 1
        in_tbl = is_tbl
    return n


# ── Document (title + labeled metadata + body) ──────────────────────────────────

LABEL_RE = re.compile(r"^([A-Za-z][A-Za-z0-9 ()/\-]{0,60}?):\s*(.+)$")


def parse_document(text: str) -> dict:
    """
    Split the intermediate into {"title", "meta": {label: value}, "body", "warnings"}.
    Metadata is the contiguous block of `Label: value` lines between the H1 and the first
    blank line. Same robustness rules as blog-seo-content/scripts/compliance.py:
      * a non-label line right after a label continues that value (wrapped meta description)
      * a non-label line with no preceding label ends the block (it is the body)
    All labels are collected (unknown ones are reported by the caller as unmapped).
    """
    lines = text.replace("\r\n", "\n").split("\n")
    i, warnings = 0, []
    while i < len(lines) and not lines[i].strip().startswith("# "):
        if lines[i].strip():
            warnings.append(f"content before the H1 ignored: {lines[i].strip()[:60]!r}")
        i += 1
    if i >= len(lines):
        return {"title": "", "meta": {}, "body": "", "warnings": ["no H1 title found"]}
    title = lines[i].strip()[2:].strip()
    i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    meta, last_key = {}, None
    while i < len(lines) and lines[i].strip():
        stripped = lines[i].strip()
        m = LABEL_RE.match(stripped)
        if m:
            last_key = m.group(1).strip()
            meta[last_key] = m.group(2).strip()
        elif last_key is not None:
            meta[last_key] = f"{meta[last_key]} {stripped}".strip()
        else:
            break
        i += 1
    body = "\n".join(lines[i:]).lstrip("\n")
    return {"title": title, "meta": meta, "body": body, "warnings": warnings}


def split_intro(body_md: str) -> tuple:
    """If the body opens with a plain paragraph (before any heading/list/table/image),
    return (intro_text, remaining_body); else ("", body_md)."""
    lines = body_md.split("\n")
    i = 0
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i >= len(lines) or _is_block_start(lines[i]):
        return "", body_md
    para = []
    while i < len(lines) and not _is_block_start(lines[i]):
        para.append(lines[i].rstrip()); i += 1
    return " ".join(para).strip(), "\n".join(lines[i:]).lstrip("\n")


# ── Slugs ───────────────────────────────────────────────────────────────────────

# A year token is a 4-digit number starting 19 or 20 (1900–2099). It will not match other
# 4-digit numbers like "top-1000-apps" or "4000-users".
YEAR_RE = re.compile(r"(?:19|20)\d{2}")
# A leading listicle count at the START of the slug — digits or a spelled cardinal up to
# twenty — followed by a hyphen. "6-best-…" → "best-…", "five-best-…" → "best-…".
LEAD_COUNT_RE = re.compile(
    r"^(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|"
    r"fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)-"
)
SLUG_FORMAT_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"\s+", "-", s).strip("-")
    return re.sub(r"-+", "-", s)


def apply_slug_rules(slug: str, rules: dict) -> tuple:
    """Enforce the collection's slug rules on any slug (derived or supplied). Returns
    (slug, warnings). Never appends anything — a collision is the caller's decision."""
    warnings = []
    if rules.get("strip_years") and YEAR_RE.search(slug):
        cleaned = re.sub(r"-+", "-", YEAR_RE.sub("", slug)).strip("-")
        warnings.append(f"slug '{slug}' contained a year — stripped to '{cleaned}'")
        slug = cleaned
    if rules.get("strip_leading_count") and LEAD_COUNT_RE.match(slug):
        cleaned = LEAD_COUNT_RE.sub("", slug).strip("-")
        warnings.append(f"slug '{slug}' began with a count — stripped to '{cleaned}'")
        slug = cleaned
    return slug, warnings


def derive_slug(title: str, rules: dict) -> str:
    """Title → slug under the collection's rules. Blog example:
    '6 Best In-App Community Platforms for Consumer Apps (2026)'
        → 'best-in-app-community-platforms-for-consumer-apps'."""
    s = YEAR_RE.sub("", title) if rules.get("strip_years") else title
    s = slugify(s)
    if rules.get("strip_leading_count"):
        s = LEAD_COUNT_RE.sub("", s)
    return s.strip("-")


# ── Taxonomy ────────────────────────────────────────────────────────────────────

def resolve_taxonomy(names_csv: str, table: dict) -> tuple:
    """'Community, Engagement' → ([ids in order, deduped], [unknown names])."""
    lookup = {k.lower(): v for k, v in table.items()}
    ids, unknown = [], []
    for n in [t.strip() for t in names_csv.split(",") if t.strip()]:
        cid = lookup.get(n.lower())
        if cid and cid not in ids:
            ids.append(cid)
        elif not cid:
            unknown.append(n)
    return ids, unknown


# ── Document → fielddata ────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def convert_document(text: str, fm: dict, slug_override: str = None, date: str = None) -> tuple:
    """
    Returns (fielddata: dict, report: dict). Hard errors are raised as ValueError.
    fielddata is the flat fieldData payload (plus "__unconfirmed__" when the map still has
    null slugs); report carries counts and warnings for the CLI summary and the dry-run.
    """
    doc = parse_document(text)
    warnings = list(doc["warnings"])
    if not doc["title"]:
        raise ValueError("no '# Title' H1 found — the intermediate must start with the title as its only H1")

    fields, meta = fm["fields"], doc["meta"]
    unconfirmed = {}
    fd = {}

    # Title
    fd[fields["title"]] = to_plain_text(doc["title"])

    # Slug: CLI override > `Slug:` label > derived from title. Rules apply to all three.
    rules = fm.get("slug_rules", {})
    slug = (slug_override or meta.get("Slug") or "").strip()
    if slug:
        slug = slugify(slug) if not SLUG_FORMAT_RE.fullmatch(slug) else slug
    else:
        slug = derive_slug(doc["title"], rules)
    slug, w = apply_slug_rules(slug, rules)
    warnings += w
    if not SLUG_FORMAT_RE.fullmatch(slug):
        raise ValueError(f"slug '{slug}' is not lowercase-hyphenated")
    fd[fields["slug"]] = slug

    # Intro + body
    body_md = doc["body"]
    intro = ""
    if fields.get("intro"):
        intro, body_md = split_intro(body_md)
        fd[fields["intro"]] = to_plain_text(intro)
        if not intro:
            warnings.append(f"{fields['intro']} empty — no plain paragraph found before the first heading")
    conv = convert_body(body_md)
    warnings += conv["warnings"]
    if fields.get("body"):
        fd[fields["body"]] = conv["html"]
    else:
        unconfirmed["body"] = conv["html"]

    # Metadata labels
    mapped_labels = set(fm.get("metadata", {})) | {"Slug"}
    for label, spec in fm.get("metadata", {}).items():
        raw = (meta.get(label) or "").strip()
        slug_key = spec.get("slug")
        typ = spec.get("type", "text")
        if not raw and spec.get("default") is not None:
            raw = str(spec["default"])
        if slug_key is None:
            if raw:
                unconfirmed[label] = raw
            continue
        if not raw:
            if spec.get("required"):
                warnings.append(f"{slug_key} empty (label '{label}:' missing) — the dry-run will fail field:{slug_key}")
                if typ == "text":
                    fd[slug_key] = ""   # keep the key visible so the operator sees what to supply
            continue
        if typ == "text":
            val = to_plain_text(raw)
            if spec.get("max_length") and len(val) > spec["max_length"]:
                warnings.append(f"{slug_key} is {len(val)} chars (max {spec['max_length']})")
            fd[slug_key] = val
        else:
            table = fm.get("taxonomies", {}).get(spec.get("taxonomy"), {})
            ids, unknown = resolve_taxonomy(raw, table)
            for u in unknown:
                warnings.append(f"Unknown {spec.get('taxonomy')} name '{u}' for '{label}' — skipped "
                                f"(check {fm['_path']})")
            if typ == "reference":
                if ids:
                    fd[slug_key] = ids[0]
                elif spec.get("required"):
                    raise ValueError(f"No valid {spec.get('taxonomy')} resolved from '{label}: {raw}'")
            else:
                if ids:
                    fd[slug_key] = ids
                elif spec.get("required") and not spec.get("must_include"):
                    raise ValueError(f"No valid {spec.get('taxonomy')} resolved from '{label}: {raw}'")

    # must_include: a multi-reference must contain its sibling reference's ID (e.g. Tags ⊇ Category)
    for label, spec in fm.get("metadata", {}).items():
        inc = spec.get("must_include")
        if not inc or spec.get("slug") is None:
            continue
        ref_slug = fm["metadata"][inc].get("slug")
        ref_id = fd.get(ref_slug) if ref_slug else None
        if ref_id:
            cur = fd.get(spec["slug"]) or []
            if ref_id not in cur:
                fd[spec["slug"]] = [ref_id] + cur
                if not cur:
                    warnings.append(f"{spec['slug']} missing — set to the {ref_slug} ID only")

    # Date
    if fields.get("date"):
        fd[fields["date"]] = date or now_iso()

    # Defaults (never override an explicit value)
    for k, v in fm.get("defaults", {}).items():
        fd.setdefault(k, v)

    # Unmapped labels are informational: `Intent:` for aeo-content, `Editor …` etc.
    unmapped = [l for l in meta if l not in mapped_labels]
    if unconfirmed:
        fd["__unconfirmed__"] = unconfirmed

    report = {
        "collection": fm["_name"],
        "slug": slug,
        "tables": conv["tables"],
        "source_tables": count_source_tables(body_md),
        "placeholders": conv["placeholders"],
        "body_chars": len(conv["html"]),
        "intro_chars": len(intro),
        "unmapped_labels": unmapped,
        "unconfirmed": sorted(unconfirmed),
        "unconfirmed_required_slugs": unconfirmed_slugs(fm)["required"],
        "warnings": warnings,
    }
    return fd, report


# ── CLI ─────────────────────────────────────────────────────────────────────────

def print_summary(out_path: str, fd: dict, fm: dict, report: dict) -> None:
    f = fm["fields"]
    print(f"✓ {out_path}", file=sys.stderr)
    print(f"  collection:  {fm['_name']} ({fm.get('display_name', '')})", file=sys.stderr)
    print(f"  name:        {fd.get(f['title'])}", file=sys.stderr)
    print(f"  slug:        {report['slug']}", file=sys.stderr)
    print(f"  body:        {report['body_chars']:,} chars | tables: {report['tables']} "
          f"(source: {report['source_tables']}) | inline placeholders: {report['placeholders']}",
          file=sys.stderr)
    if report["unmapped_labels"]:
        print(f"  unmapped labels (ignored): {report['unmapped_labels']}", file=sys.stderr)
    if report["unconfirmed"]:
        print(f"  ⚠ parked under __unconfirmed__ (field slug is null in the map): {report['unconfirmed']}",
              file=sys.stderr)
    for w in report["warnings"]:
        print(f"  ⚠ {w}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description="markdown intermediate → Webflow fielddata.json")
    ap.add_argument("draft")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--collection", help="registry name (each content-type skill's own webflow-fields.json)")
    g.add_argument("--field-map", help="path to a field-map JSON")
    ap.add_argument("--out", help="where to write fielddata.json")
    ap.add_argument("--slug", default=None)
    ap.add_argument("--date", default=None, help="ISO 8601 for fields.date (default: now UTC)")
    ap.add_argument("--report", default=None, help="write the conversion report JSON here")
    ap.add_argument("--html-only", action="store_true", help="print only the body HTML to stdout")
    args = ap.parse_args()

    try:
        text = Path(args.draft).read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        text = Path(args.draft).read_text(encoding="cp1252")
    except OSError as e:
        print(f"ERROR: cannot read {args.draft}: {e}", file=sys.stderr)
        return 1

    # The Drive MCP wraps a doc as {"fileContent": "..."} — unwrap if present.
    stripped = text.strip()
    if stripped.startswith("{"):
        try:
            text = json.loads(stripped).get("fileContent", text)
        except json.JSONDecodeError:
            pass

    if args.html_only:
        doc = parse_document(text)
        conv = convert_body(doc["body"] if doc["title"] else text)
        for w in conv["warnings"]:
            print(f"  ⚠ {w}", file=sys.stderr)
        print(conv["html"])
        return 0

    if not (args.collection or args.field_map) or not args.out:
        ap.error("--out and one of --collection / --field-map are required (or use --html-only)")

    try:
        fm = load_field_map(args.collection or args.field_map)
        fd, report = convert_document(text, fm, slug_override=args.slug, date=args.date)
    except (FieldMapError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    Path(args.out).write_text(json.dumps(fd, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.report:
        Path(args.report).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print_summary(args.out, fd, fm, report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
