#!/usr/bin/env python3
"""
apply_internal_links.py — Deterministically embed internal-link suggestions into
post-content HTML.

The internal-linking-strategist returns suggestions as (anchor, target URL, and a
"rephrase suggestion" used when the anchor doesn't sit in the prose verbatim). Applying
those by hand-matching the strategist's long "Insert at" sentence is fragile — punctuation
or spacing drift makes the match miss (it dropped 2 of 7 links on one run). This helper
matches the short ANCHOR phrase instead, wraps the first clean occurrence in real prose,
and clearly reports anything it couldn't place so the caller can apply the rephrase.

Usage:
    python3 scripts/apply_internal_links.py <fielddata.json> <links.json> [--out <fielddata.json>]

    <links.json>: a list of suggestions from the strategist. Two shapes, matching the two
    cases the strategist itself distinguishes:

      # (1) anchor already sits in the prose → just wrap it
      {"anchor": "community SDK", "url": "https://www.social.plus/social/sdk"}

      # (2) anchor is NOT in the prose → the strategist gives the original sentence to
      #     replace ("insert_at") and the rewritten one ("rephrase") that weaves the anchor in
      {"anchor": "content moderation", "url": "https://www.social.plus/moderation",
       "insert_at": "AI-powered moderation and real-time analytics built into the platform",
       "rephrase":  "AI-powered content moderation and real-time analytics built into the platform"}

Behaviour per suggestion:
  - Case 1 (no rephrase): wrap the FIRST clean occurrence of the anchor in plain prose —
    NOT inside an <a>, a heading, the comparison-table embed, or any tag. Casing preserved.
  - Case 2 (rephrase given): find `insert_at` with WHITESPACE-FLEXIBLE matching (the drift
    that broke exact matching before), replace it with `rephrase`, and wrap the anchor inside
    the rephrase. Deterministic, so it doesn't depend on the agent eyeballing the sentence.
  - If neither the anchor nor `insert_at` can be located, report UNPLACED rather than forcing
    a bad edit — a genuinely rare case the caller resolves by hand.

Outputs: updated fielddata.json (post-content with links embedded) and a stdout JSON
summary {applied, unplaced:[…]}. Exits 0 always (unplaced links are expected, not errors).
"""
import json
import re
import sys

LINK_TMPL = '<a href="{url}" target="_blank">{text}</a>'


def protected_intervals(html: str):
    """Spans where an anchor must NOT be linked: existing links, headings, the table
    embed / figures, and every tag's own markup."""
    spans = []
    patterns = [
        r"<a\b[^>]*>.*?</a>",                       # already-linked text
        r"<h[1-6]\b[^>]*>.*?</h[1-6]>",             # headings
        r"<div data-rt-embed-type[^>]*>.*?</div>",  # comparison-table embed
        r"<figure\b[^>]*>.*?</figure>",             # inline images
        r"<[^>]+>",                                 # any tag's markup
    ]
    for pat in patterns:
        for m in re.finditer(pat, html, re.DOTALL | re.IGNORECASE):
            spans.append((m.start(), m.end()))
    return spans


def in_protected(pos_start, pos_end, spans):
    return any(s <= pos_start < e or s < pos_end <= e for s, e in spans)


def wrap_anchor_in_text(text: str, anchor: str, url: str) -> str:
    """Wrap the first occurrence of `anchor` inside a plain string (used on a rephrase)."""
    m = re.search(r"(?<!\w)" + re.escape(anchor) + r"(?!\w)", text)
    if not m:
        return text  # anchor missing from rephrase — leave as-is (reported upstream)
    return text[:m.start()] + LINK_TMPL.format(url=url, text=m.group(0)) + text[m.end():]


def wrap_first(html: str, anchor: str, url: str):
    """Case 1: wrap the first clean prose occurrence of `anchor`. Returns (html, applied)."""
    spans = protected_intervals(html)
    for flags in (0, re.IGNORECASE):                       # exact case first, then any case
        for m in re.finditer(r"(?<!\w)" + re.escape(anchor) + r"(?!\w)", html, flags):
            if not in_protected(m.start(), m.end(), spans):
                link = LINK_TMPL.format(url=url, text=m.group(0))  # preserve casing
                return html[:m.start()] + link + html[m.end():], True
    return html, False


def locate_sentence(html: str, sentence: str, spans):
    """Whitespace-flexible search for `sentence` in clean prose. Returns a match or None.
    Tokenize then join with \\s+ so any run of whitespace in the source matches — this is
    what fixes the exact-match drift that dropped links before. (Building the pattern with
    re.escape on the whole string is wrong here: in Python 3.7+ re.escape escapes spaces,
    which collides with the whitespace substitution.)"""
    tokens = sentence.strip().split()
    if not tokens:
        return None
    pat = r"\s+".join(re.escape(t) for t in tokens)
    for m in re.finditer(pat, html):
        if not in_protected(m.start(), m.end(), spans):
            return m
    return None


def apply_link(html: str, anchor: str, url: str, insert_at: str, rephrase: str):
    """
    Place one link, faithfully to the strategist's intent:
      1. Locate the strategist's `insert_at` sentence (whitespace-flexible).
         - with a rephrase  → replace that sentence with the rephrase (anchor wrapped)
         - without rephrase → wrap the anchor inside that exact sentence
      2. If the sentence can't be located, fall back to wrapping the anchor's first clean
         occurrence anywhere in prose.
      3. Otherwise UNPLACED.
    Returns (html, how|None).
    """
    spans = protected_intervals(html)
    loc = locate_sentence(html, insert_at, spans)
    if loc:
        s, e = loc.start(), loc.end()
        if rephrase:
            new = wrap_anchor_in_text(rephrase, anchor, url)
            return html[:s] + new + html[e:], "rephrase"
        seg = wrap_anchor_in_text(html[s:e], anchor, url)
        if seg != html[s:e]:
            return html[:s] + seg + html[e:], "wrapped (at insert_at)"
    # Fallback: anchor's first clean occurrence anywhere
    html2, ok = wrap_first(html, anchor, url)
    if ok:
        return html2, "wrapped (first occurrence)"
    return html, None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out_flag = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--out"), None)
    fielddata_path, links_path = args[0], args[1]
    out_path = out_flag or fielddata_path

    fd = json.load(open(fielddata_path))
    links = json.load(open(links_path))
    html = fd.get("post-content", "")

    applied, unplaced = [], []
    for s in links:
        anchor, url = s["anchor"], s["url"]
        html, how = apply_link(html, anchor, url, s.get("insert_at", ""), s.get("rephrase", ""))
        if how:
            applied.append(anchor)
            print(f"  ✓ {how:26} {anchor!r} → {url}", file=sys.stderr)
        else:
            unplaced.append({"anchor": anchor, "url": url,
                             "insert_at": s.get("insert_at", ""), "rephrase": s.get("rephrase", "")})
            print(f"  ⚠ unplaced {anchor!r} — insert_at sentence not found and anchor not in prose",
                  file=sys.stderr)

    fd["post-content"] = html
    json.dump(fd, open(out_path, "w"), indent=2, ensure_ascii=False)

    print(f"\n  {len(applied)}/{len(links)} links embedded; {len(unplaced)} need a rephrase",
          file=sys.stderr)
    print(json.dumps({"applied": applied, "unplaced": unplaced}))


if __name__ == "__main__":
    main()
