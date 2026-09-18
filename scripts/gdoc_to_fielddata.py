#!/usr/bin/env python3
"""
gdoc_to_fielddata.py — BLOG ADAPTER: convert a Google Doc listicle export into Webflow
CMS fielddata.json for the Blog Posts collection.

The SKILL reads the Google Doc via the Drive MCP and saves the raw exported text to a
file (a standalone script has no MCP access). This helper does the blog-specific,
deterministic part — slice out one `# Listicle N`, extract the doc's labeled metadata
(`**Page title:**`, `**Meta description**`, `Main Category Tag:` …), normalize the export's
heading levels and platform entries — then hands the result to the shared converter
(scripts/md_to_webflow_html.py) as the common markdown intermediate, with the `blog`
field map (marketing-team/skills/webflow-publisher/collections/blog.json) supplying the
field slugs and category IDs.

Google Doc export → intermediate normalization:
    ### **Platform: tagline**   →  ### Platform: tagline  +  a bare __INLINE_IMG_N__ line
                                   (platform entries are H3 sub-sections; N counts up)
    ### Section heading         →  ## Section heading     (H2)
    #### Sub-heading            →  ### Sub-heading        (H3)
    Main Category Tag: A, B, C  →  Category: A, B, C  +  Tags: A, B, C
                                   (first VALID name is the main category; all valid → tags)
    [OPTIONAL DISCLOSURE …]     →  dropped (the user decides whether to include it)
    OUTREACH VERSION / INTERNAL USE ONLY / Image alt text / Display recommendations
                                →  end of body (trailers are never published)

Usage:
    python3 scripts/gdoc_to_fielddata.py <raw_doc.txt> <listicle_number> --out <fielddata.json>
        [--slug <slug>]                 override the auto-derived slug (year + leading count
                                        are still stripped — NON-NEGOTIABLE, see SKILL.md)
        [--date <iso8601>]              date-published (default: now, UTC)
        [--emit-intermediate <path>]    also write the normalized markdown intermediate
                                        (useful to inspect what the shared converter received)

Exit codes: 0 ok, 1 on any parse/validation failure (message on stderr). Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from md_to_webflow_html import convert_document, is_block_start, print_summary  # noqa: E402
from webflow_fieldmap import FieldMapError, load_field_map  # noqa: E402

COLLECTION = "blog"

PLATFORM_RE = re.compile(r"^### \*\*(.+?:.+?)\*\*\s*$")   # "### **Name: tagline**" → h3 + inline img


# ── Google Doc export parsing ──────────────────────────────────────────────────

def first_match(pattern: str, text: str, default: str = "", dotall: bool = False) -> str:
    flags = re.DOTALL if dotall else 0
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else default


def extract_listicle(raw: str, n: int) -> str:
    """Slice out '# Listicle n' through just before '# Listicle n+1' (or end)."""
    start = raw.find(f"# Listicle {n}")
    if start == -1:
        print(f"ERROR: '# Listicle {n}' not found in the document.", file=sys.stderr)
        sys.exit(1)
    nxt = raw.find(f"# Listicle {n + 1}", start)
    return raw[start:nxt] if nxt != -1 else raw[start:]


def extract_alt_text(block: str) -> str:
    """Some docs put "Image alt text: … Image concept: … Image sizes needed: …" all on ONE
    physical line, so a to-end-of-line capture over-grabs the concept + pixel notes into
    the alt text. Cut at the next label."""
    alt_text = first_match(r"\*{0,2}Image alt text:\*{0,2}\s*(.+)", block)
    for label in ("Image concept:", "**Image concept", "Image sizes needed:", "**Image sizes",
                  "Display recommendations:", "**Display"):
        cut = alt_text.find(label)
        if cut != -1:
            alt_text = alt_text[:cut]
    return alt_text.strip()


def slice_body(block: str) -> str:
    """First '###' heading through just before the image/display trailer. The trailer
    marker varies ("Image alt text:" or "**Image alt text:**"), and some listicles have an
    "OUTREACH VERSION" / "INTERNAL USE ONLY" block first."""
    body_start = block.find("###")
    if body_start == -1:
        print("ERROR: no '###' body heading found in listicle block.", file=sys.stderr)
        sys.exit(1)
    body_end = len(block)
    for marker in ("OUTREACH VERSION", "INTERNAL USE ONLY",
                   "Image alt text:", "**Image alt text:**",
                   "Display recommendations:", "**Display recommendations:**"):
        idx = block.find(marker)
        if idx != -1:
            body_end = min(body_end, idx)
    return block[body_start:body_end].strip()


def drop_paragraphs_containing(text: str, marker: str) -> str:
    """Remove every paragraph run (consecutive non-block lines) that contains `marker`,
    leaving headings, lists and tables around it untouched."""
    lines, out, i = text.split("\n"), [], 0
    while i < len(lines):
        if is_block_start(lines[i]):
            out.append(lines[i]); i += 1
            continue
        para = []
        while i < len(lines) and not is_block_start(lines[i]):
            para.append(lines[i]); i += 1
        if marker not in " ".join(para):
            out.extend(para)
    return "\n".join(out)


def normalize_gdoc_body(body_raw: str) -> tuple:
    """Export heading levels → intermediate heading levels. Returns (markdown, n_platforms)."""
    out, n = [], 0
    for line in body_raw.split("\n"):
        l = line.rstrip()
        m = PLATFORM_RE.match(l)
        if m:
            # Platform entries are sub-sections under the "N Best …" H2 section, so they
            # are H3, each followed by an inline-image slot.
            n += 1
            out.append(f"### {m.group(1)}")
            out.append(f"__INLINE_IMG_{n}__")
        elif l.startswith("### "):
            out.append("## " + l[4:])
        elif l.startswith("#### "):
            out.append("### " + l[5:])
        else:
            out.append(l)
    return drop_paragraphs_containing("\n".join(out), "OPTIONAL DISCLOSURE"), n


def build_intermediate(block: str) -> tuple:
    """Google Doc listicle block → (intermediate markdown, info dict)."""
    name = first_match(r"\*\*Page title:\*\*\s*(.+)", block)
    if not name:
        print("ERROR: '**Page title:**' not found.", file=sys.stderr)
        sys.exit(1)
    meta_desc = first_match(r"\*\*Meta description\*\*\s*\n+\s*(.+)", block)
    min_read  = first_match(r"\*\*Minutes to read:\*\*\s*(\d+)", block)
    tag_line  = first_match(r"\*{0,2}Main Category Tag:\*{0,2}\s*(.+)", block)
    summary   = first_match(r"\*\*Introduction text\*\*\s*\n+\s*(.+?)\n\s*\n", block, dotall=True)
    alt_text  = extract_alt_text(block)
    body_md, n_platforms = normalize_gdoc_body(slice_body(block))

    if not tag_line:
        print("ERROR: 'Main Category Tag:' line not found.", file=sys.stderr)
        sys.exit(1)

    labels = [("Meta description", meta_desc), ("Alt text", alt_text),
              ("Category", tag_line), ("Tags", tag_line), ("Minutes to read", min_read)]
    lines = [f"# {name}", ""]
    lines += [f"{k}: {v}" for k, v in labels if v]
    lines.append("")
    if summary:
        lines += [" ".join(summary.split()), ""]
    lines.append(body_md)
    info = {"tag_line": tag_line, "platforms": n_platforms, "summary_present": bool(summary)}
    return "\n".join(lines) + "\n", info


# ── Main ────────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Google Doc listicle export → Blog fielddata.json")
    ap.add_argument("raw_doc")
    ap.add_argument("listicle_number", type=int)
    ap.add_argument("--out", required=True)
    ap.add_argument("--slug", default=None)
    ap.add_argument("--date", default=None, help="ISO 8601 date-published (default: now, UTC).")
    ap.add_argument("--emit-intermediate", default=None,
                    help="also write the normalized markdown intermediate here")
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
    intermediate, info = build_intermediate(block)
    if args.emit_intermediate:
        Path(args.emit_intermediate).write_text(intermediate, encoding="utf-8")

    try:
        fm = load_field_map(COLLECTION)
        fielddata, report = convert_document(intermediate, fm, slug_override=args.slug, date=args.date)
    except (FieldMapError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    with open(args.out, "w") as f:
        json.dump(fielddata, f, indent=2, ensure_ascii=False)

    print_summary(args.out, fielddata, fm, report)
    print(f"  categories:  {len(fielddata.get('category-multi-reference-3', []))} ({info['tag_line']})",
          file=sys.stderr)
    print(f"  platform images: {info['platforms']}", file=sys.stderr)
    if not fielddata.get("meta-description"): print("  ⚠ meta-description empty", file=sys.stderr)
    if not fielddata.get("post-summary"):     print("  ⚠ post-summary empty", file=sys.stderr)
    if not fielddata.get("image-alt-text"):   print("  ⚠ image-alt-text empty", file=sys.stderr)


if __name__ == "__main__":
    main()
