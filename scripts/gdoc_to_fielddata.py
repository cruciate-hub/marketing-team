#!/usr/bin/env python3
"""
gdoc_to_fielddata.py — Convert a Google Doc listicle into Webflow CMS fielddata.json.

The SKILL reads the Google Doc via the Drive MCP and saves the raw exported text to
a file (a standalone script has no MCP access). This helper does the deterministic
part: parse metadata, convert the body to Webflow Rich Text HTML, map category names
to IDs, insert __INLINE_IMG_N__ placeholders, and emit fielddata.json.

Usage:
    python3 scripts/gdoc_to_fielddata.py <raw_doc.txt> <listicle_number> --out <fielddata.json>
    python3 scripts/gdoc_to_fielddata.py <raw_doc.txt> <listicle_number> --out <out.json> --slug <slug>

    <raw_doc.txt>       Raw text of the Google Doc (markdown-like), exactly as the
                        Drive MCP returns it. May contain multiple "# Listicle N" sections.
    <listicle_number>   Which listicle to extract (1, 2, 3 …).
    --out               Path to write fielddata.json.
    --slug              Override the auto-derived slug. The auto slug strips any
                        trailing "(YEAR)" — slugs never contain a year.

Exit codes: 0 ok, 1 on any parse/validation failure (message on stderr).
"""

import argparse
import json
import re
import sys

# ── Category name → Webflow reference ID ────────────────────────────────────────
# Source of truth: marketing-team/skills/blog-publisher/webflow-config.md
# (Categories rarely change; embedded here so the helper runs standalone.)
CATEGORY_IDS = {
    "acquisition":               "66e2765d540e1939a89dc2e9",
    "app growth":                "66e2765d540e1939a89dc04c",
    "community":                 "66e2765d540e1939a89dc049",
    "community stories":         "66e2765d540e1939a89dc2e8",
    "education":                 "66e2765d540e1939a89dc2eb",
    "engagement":                "66e2765d540e1939a89dc04b",
    "events":                    "66e2765d540e1939a89dc48f",
    "hospitality":               "66e2765d540e1939a89dc2e3",
    "insights":                  "66e2765d540e1939a89dbfd7",
    "monetization":              "66e2765d540e1939a89dc2e5",
    "news":                      "66e2765d540e1939a89dc2e6",
    "people":                    "66e2765d540e1939a89dc029",
    "product":                   "69d8d99d7d17ee9ca3ede77f",
    "retention":                 "66e2765d540e1939a89dc2ea",
    "social+":                   "66e2765d540e1939a89dc2e2",
    "vertical social networks":  "66e2765d540e1939a89dc2e7",
}


# ── Inline formatting ───────────────────────────────────────────────────────────

def clean_inline(text: str) -> str:
    """Markdown-ish inline → HTML. Used for paragraphs, list items, headings."""
    text = text.replace("\\*\\*", "**").replace("\\\\~", "~").replace("\\~", "~")
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*",     r"<em>\1</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" target="_blank">\1</a>', text)
    return text.strip()


def clean_cell(text: str) -> str:
    """Table cells render bold markers literally in Webflow — strip them to plain text."""
    text = text.replace("\\*\\*", "").replace("\\\\~", "~").replace("\\~", "~")
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    return text.strip()


def convert_table(table_lines: list) -> str:
    rows = []
    for line in table_lines:
        if re.match(r"^\s*\|[\s:\-|]+\|\s*$", line):       # alignment row
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(not c.replace(" ", "") for c in cells):     # empty row
            continue
        rows.append(cells)
    if not rows:
        return ""
    thead = "<thead><tr>" + "".join(f"<th>{clean_cell(c)}</th>" for c in rows[0]) + "</tr></thead>"
    tbody = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{clean_cell(c)}</td>" for c in r) + "</tr>" for r in rows[1:]
    ) + "</tbody>"
    return f"<table>{thead}{tbody}</table>"


# ── Body → HTML ─────────────────────────────────────────────────────────────────

PLATFORM_RE = re.compile(r"^### \*\*(.+?:.+?)\*\*\s*$")   # "### **Name: tagline**" → h2 + inline img
SECTION_RE  = re.compile(r"^### (.+)$")                    # "### Heading"           → h2


def convert_body(raw: str) -> tuple:
    """Returns (html, n_platform_images). Inserts __INLINE_IMG_N__ after each platform h2."""
    lines, html, i, img_n = raw.split("\n"), [], 0, 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue

        if line.startswith("|"):                           # table block
            tbl = []
            while i < len(lines) and lines[i].rstrip().startswith("|"):
                tbl.append(lines[i].rstrip()); i += 1
            html.append(convert_table(tbl)); continue

        m = PLATFORM_RE.match(line)                         # platform heading
        if m:
            img_n += 1
            html.append(f"<h2>{clean_inline(m.group(1))}</h2>__INLINE_IMG_{img_n}__")
            i += 1; continue

        m = SECTION_RE.match(line)                          # section heading
        if m:
            html.append(f"<h2>{clean_inline(m.group(1))}</h2>")
            i += 1; continue

        if re.match(r"^  - |^- ", line):                   # bullet list
            items = []
            while i < len(lines):
                l = lines[i].rstrip()
                if re.match(r"^  - ", l):  items.append(clean_inline(l[4:])); i += 1
                elif re.match(r"^- ", l):  items.append(clean_inline(l[2:])); i += 1
                elif not l:                i += 1; break
                else:                      break
            html.append("<ul>" + "".join(f"<li>{it}</li>" for it in items) + "</ul>")
            continue

        para = []                                          # paragraph
        while i < len(lines):
            l = lines[i].rstrip()
            if not l or l.startswith("### ") or l.startswith("|") or re.match(r"^  - |^- ", l):
                break
            para.append(l); i += 1
        if para:
            txt = " ".join(para)
            if "OPTIONAL DISCLOSURE" not in txt:           # drop the disclosure prompt line
                html.append(f"<p>{clean_inline(txt)}</p>")

    return "".join(html), img_n


# ── Metadata extraction ─────────────────────────────────────────────────────────

def first_match(pattern: str, text: str, default: str = "", dotall: bool = False) -> str:
    flags = re.DOTALL if dotall else 0
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default


# A year token is a 4-digit number starting 19 or 20 (1900–2099). This is what we
# strip from slugs and reject in overrides. It will not match other 4-digit numbers
# like "top-1000-apps" or "4000-users".
YEAR_RE = re.compile(r"(?:19|20)\d{2}")


def strip_years(text: str) -> str:
    """Remove every year token (e.g. 2026) from a string. Slugs must never contain a year."""
    return YEAR_RE.sub("", text)


def derive_slug(name: str) -> str:
    """Lowercase, hyphenate, drop special chars, and remove ANY year token. Never includes a year."""
    s = strip_years(name)                                  # remove "2026" anywhere, not just trailing parens
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s-]", "", s)                     # drop punctuation
    s = re.sub(r"\s+", "-", s).strip("-")
    s = re.sub(r"-+", "-", s)                              # collapse repeats left by removed years
    return s.strip("-")


def map_categories(tag_line: str) -> tuple:
    """'Community, Engagement, Retention' → (main_id, [all_ids]). Unknown names are skipped with a warning."""
    names = [t.strip() for t in tag_line.split(",") if t.strip()]
    ids = []
    for n in names:
        cid = CATEGORY_IDS.get(n.lower())
        if cid:
            if cid not in ids:
                ids.append(cid)
        else:
            print(f"  ⚠ Unknown category '{n}' — skipped (check webflow-config.md)", file=sys.stderr)
    if not ids:
        print("ERROR: No valid categories resolved from Main Category Tag line.", file=sys.stderr)
        sys.exit(1)
    return ids[0], ids


def extract_listicle(raw: str, n: int) -> str:
    """Slice out '# Listicle n' through just before '# Listicle n+1' (or end)."""
    start = raw.find(f"# Listicle {n}")
    if start == -1:
        print(f"ERROR: '# Listicle {n}' not found in the document.", file=sys.stderr)
        sys.exit(1)
    nxt = raw.find(f"# Listicle {n + 1}", start)
    return raw[start:nxt] if nxt != -1 else raw[start:]


# ── Main ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("raw_doc")
    ap.add_argument("listicle_number", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--slug", default=None)
    ap.add_argument("--date", default="2026-06-04T00:00:00.000Z",
                    help="ISO 8601 date-published (no Date.now in the harness).")
    args = ap.parse_args()

    with open(args.raw_doc) as f:
        raw = f.read()
    # The Drive MCP wraps the doc as {"fileContent": "..."} — unwrap if present.
    raw = raw.strip()
    if raw.startswith("{"):
        try:
            raw = json.loads(raw).get("fileContent", raw)
        except json.JSONDecodeError:
            pass

    block = extract_listicle(raw, args.listicle_number)

    # Metadata
    name      = first_match(r"\*\*Page title:\*\*\s*(.+)", block)
    if not name:
        print("ERROR: '**Page title:**' not found.", file=sys.stderr); sys.exit(1)
    meta_desc = first_match(r"\*\*Meta description\*\*\s*\n+\s*(.+)", block)
    min_read  = first_match(r"\*\*Minutes to read:\*\*\s*(\d+)", block)
    tag_line  = first_match(r"\*{0,2}Main Category Tag:\*{0,2}\s*(.+)", block)
    alt_text  = first_match(r"\*{0,2}Image alt text:\*{0,2}\s*(.+)", block)
    summary   = first_match(r"\*\*Introduction text\*\*\s*\n+\s*(.+?)\n\s*\n", block, dotall=True)

    # Slug: derive from name (auto strips years), or use --slug override.
    # HARD RULE: a slug must NEVER contain a year. If an override sneaks one in,
    # strip it and warn — never publish a year in the slug, and never resolve a
    # collision by appending one.
    slug = args.slug if args.slug else derive_slug(name)
    if YEAR_RE.search(slug):
        cleaned = re.sub(r"-+", "-", strip_years(slug)).strip("-")
        print(f"  ⚠ slug '{slug}' contained a year — stripped to '{cleaned}'", file=sys.stderr)
        slug = cleaned

    main_cat, all_cats = map_categories(tag_line)

    # Body: first '###' heading through just before the image/display trailer.
    # The trailer marker varies: "Image alt text:" or "**Image alt text:**",
    # and some listicles have an "OUTREACH VERSION" / "INTERNAL USE ONLY" block first.
    body_start = block.find("###")
    body_end = len(block)
    for marker in ("OUTREACH VERSION", "INTERNAL USE ONLY",
                   "Image alt text:", "**Image alt text:**",
                   "Display recommendations:", "**Display recommendations:**"):
        idx = block.find(marker)
        if idx != -1:
            body_end = min(body_end, idx)
    body_raw = block[body_start:body_end].strip()
    post_content, n_imgs = convert_body(body_raw)

    fielddata = {
        "name":                        name,
        "slug":                        slug,
        "post-summary":                summary,
        "post-content":                post_content,
        "meta-description":            meta_desc,
        "min-read":                    min_read or "5",
        "date-published":              args.date,
        "image-alt-text":              alt_text,
        "category":                    main_cat,
        "category-multi-reference-3":  all_cats,
        "featured":                    False,
        "blog-without-images":         False,
        "show-on-careers-page":        False,
    }

    with open(args.out, "w") as f:
        json.dump(fielddata, f, indent=2, ensure_ascii=False)

    print(f"✓ {args.out}", file=sys.stderr)
    print(f"  name:        {name}", file=sys.stderr)
    print(f"  slug:        {slug}", file=sys.stderr)
    print(f"  categories:  {len(all_cats)} ({tag_line})", file=sys.stderr)
    print(f"  post-content: {len(post_content):,} chars | platform images: {n_imgs}", file=sys.stderr)
    print(f"  inline placeholders: {post_content.count('__INLINE_IMG_')}", file=sys.stderr)
    if not meta_desc: print("  ⚠ meta-description empty", file=sys.stderr)
    if not summary:   print("  ⚠ post-summary empty", file=sys.stderr)
    if not alt_text:  print("  ⚠ image-alt-text empty", file=sys.stderr)


if __name__ == "__main__":
    main()
