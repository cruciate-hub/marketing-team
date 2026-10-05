#!/usr/bin/env python3
"""Claims about social.plus, checked against messaging/product-capabilities.md.

Why: the writing skills may only claim what social.plus really offers, but nothing listed it, so a draft
could tie social.plus to biometrics or budgeting tools and pass every check (EX-B-033, October 2026).

A paragraph *attributes* something to social.plus when it names social.plus or links a social.plus
product page (any www.social.plus link outside the content and legal sections). In such a paragraph, a word
from the "Outside social.plus scope" table of product-capabilities.md is
  FAIL  when its own sentence attributes it ("add groups, leaderboards and chat through social.plus"),
  WARN  when only the paragraph does ("Strava built leaderboards. ... the same patterns are available
        pre-built"), because the word may describe another company; the reviewer decides,
unless a negation comes before the word in its sentence ("social.plus does not process payments").
Headings count too, because the text under a heading is about what the heading names:
  - under social.plus's own entry in a list ("### social.plus: Best for ...", "### 1. social.plus") every
    sentence is about social.plus, so a word there is a FAIL even when the sentence does not repeat the name;
  - under any other heading that names social.plus ("## Where social.plus fits") the paragraph attributes, so a
    word there is at least a WARN.
  The context lasts until the next heading of the same or a higher level; the page's H1 never sets it.

  python3 scripts/product_claims.py DRAFT.md [--json] [--capabilities PATH]
      Lists every attributing paragraph (for the reviewer's "Claims about social.plus" box) and the
      outside-scope hits with their level. Exit 1 when there is a FAIL hit, else 0.

Used by the compliance scripts of aeo-content, blog-seo-content and glossary-content (check
`product_claims`: FAIL or WARN as above) and by the content engine's Doc builder.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CAPS = ROOT / "messaging" / "product-capabilities.md"
SCOPE_HEADING = re.compile(r"^##\s+Outside social\.plus scope", re.I)
# Links to these sections describe content, not the product, so they do not attribute anything.
CONTENT_PATHS = ("/blog/", "/glossary/", "/answers/", "/customer-story/", "/customer-stories", "/webinar",
                 "/product-update", "/release-note", "/legal", "/privacy", "/terms", "/contact", "/about", "/careers")
LINK = re.compile(r"\]\((https?://(?:www\.)?social\.plus(/[^)\s]*)?)\)")
# A negation counts only when it comes before the outside-scope word in the same sentence ("social.plus does not
# offer leaderboards"). Words like "instead of", "rather than" and "without" are not negations of the claim:
# "add leaderboards through social.plus instead of building them" is still a claim.
NEGATION = re.compile(r"\b(not|never|doesn't|does not|isn't|is not|aren't|are not|don't|do not|cannot|can't|neither|nor|"
                      r"has no|have no|no native|no built-in|lacks|out of scope|outside (?:social\.plus )?scope)\b", re.I)
# Reviewer notes that older drafts keep between the H1 and the first H2 (change summaries, push checks).
NOTE_START = re.compile(r"^\s*(?:\*\*)?(?:Confirm|Re-confirm|Re-verify|Verify|Verified|Check|Checked|Removed|Added|Rewrote|"
                        r"Restructured|Replaced|Rebuilt|Confirmed|Kept|Converted|Re-scoped|Ran|Original live post|Internal-linking|"
                        r"Dropped|Cut|Preserved|Changed|Updated|Merged|Split|Moved|Fixed)\b")
# A sentence that says the customer does the work ("connecting products to your checkout requires integration work on
# your team's side") describes a limit, not a feature: its hits are WARN, so the reviewer reads the wording.
LIMITATION = re.compile(r"\b(requires? (?:integration|custom|extra|engineering) work|on your (?:team's |own )?side|"
                        r"(?:you|your team) (?:would |will )?(?:need to |have to )?(?:build|connect|integrate|wire)\b[^.]*\b(?:yourself|yourselves|separately)|"
                        r"is up to (?:you|your team)|not included)\b", re.I)
SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\[(\"'])")


def load_scope(path: Path = DEFAULT_CAPS) -> list[tuple[str, list[str]]]:
    """(topic, match words) rows of the 'Outside social.plus scope' table: column 1 topic, column 2 words."""
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    rows, inside = [], False
    for ln in lines:
        if SCOPE_HEADING.match(ln):
            inside = True
            continue
        if inside and ln.startswith("## "):
            break
        if inside and ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) < 2 or set(cells[0]) <= set("-: ") or cells[0].lower() in ("topic", "outside scope"):
                continue
            words = [w.strip().strip("`").lower() for w in cells[1].split(",") if w.strip()]
            if words:
                rows.append((cells[0], words))
    return rows


def strip_meta(md: str) -> str:
    """Drop the metadata block above the first H2 that the skills put under the H1 (Meta description, Slug,
    reviewer notes), so only the article is checked. The H1 itself stays."""
    out, seen_h2 = [], False
    for ln in md.splitlines():
        if ln.startswith("## "):
            seen_h2 = True
        if not seen_h2 and not ln.startswith("#") and (
                re.match(r"^\s*\**\s*[A-Z][A-Za-z0-9 ()/,.-]{1,60}:\**\s", ln)   # Meta description: ..., **SEO title:** ...
                or re.match(r"^\s*[-*]\s", ln)                                     # note bullets (Verify at push, Change summary)
                or NOTE_START.match(ln) or re.search(r"\bat (?:time of )?push\b", ln, re.I)):   # change-summary notes
            continue
        out.append(ln)
    return "\n".join(out)


# social.plus's own entry in a vendor list: the heading starts with the name (after an optional "1." number) and the
# name is followed by nothing, a colon, a dash or a bracket ("social.plus: Best for ...", "1. social.plus").
# "social.plus and payments" is a section about a topic, not an entry.
ENTRY_HEADING = re.compile(r"^(?:\d+[.)]\s*)?social\.plus\s*(?:$|[:(\u2013\u2014-])", re.I)


def heading_context(md: str) -> list[tuple[str, str | None]]:
    """(paragraph, context) for every paragraph and table row, headings dropped. context is "entry" under
    social.plus's own list entry, "section" under another heading that names social.plus, else None."""
    out, cur, stack = [], [], []   # stack: (level, heading text) of the open H2..H6 headings

    def ctx():
        texts = [t for _, t in stack]
        if any(ENTRY_HEADING.match(t) for t in texts):
            return "entry"
        if any(re.search(r"social\.plus", t, re.I) for t in texts):
            return "section"
        return None

    def flush():
        if cur:
            out.append((" ".join(cur), ctx()))
            cur.clear()

    for ln in md.splitlines():
        if ln.lstrip().startswith("|"):
            flush()
            if not set(ln.replace("|", "").strip()) <= set("-: "):
                out.append((ln.strip(), ctx()))
            continue
        if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", ln):   # a list item is its own unit, like a table row
            flush()
        if not ln.strip() or ln.startswith("#"):
            flush()
            if ln.startswith("#"):
                level = len(ln) - len(ln.lstrip("#"))
                text = plain(ln.lstrip("# ").strip()).replace("*", "").replace("\\", "").strip()
                stack[:] = [(lv, t) for lv, t in stack if lv < level]
                if level > 1:
                    stack.append((level, text))
            continue
        cur.append(ln.strip())
    flush()
    return out


def paragraphs(md: str, keep_headings: bool = True) -> list[str]:
    """Paragraphs and table rows. Headings ("In-App Purchases and social.plus") end a paragraph and are
    dropped when keep_headings is False: a section title names a topic, it does not claim a feature."""
    paras, cur = [], []
    for ln in md.splitlines():
        if ln.lstrip().startswith("|"):   # a table row is its own unit; a whole table is not one paragraph
            if cur:
                paras.append(" ".join(cur))
                cur = []
            if not set(ln.replace("|", "").strip()) <= set("-: "):
                paras.append(ln.strip())
            continue
        if not ln.strip() or ln.startswith("#"):
            if cur:
                paras.append(" ".join(cur))
                cur = []
            if ln.startswith("#") and keep_headings:
                paras.append(ln.lstrip("# ").strip())
            continue
        cur.append(ln.strip())
    if cur:
        paras.append(" ".join(cur))
    return paras


DISCLOSURE = re.compile(r"(?:^|(?<=[.!?]\s))Disclosure:[^.!?]*[.!?]?", re.I)


def attributes(p: str) -> bool:
    p = DISCLOSURE.sub("", p)   # "Disclosure: social.plus publishes this blog ..." names us but attributes nothing
    if re.search(r"social\.plus", re.sub(r"\]\([^)]*\)", "]", p), re.I):
        return True
    for m in LINK.finditer(p):
        path = (m.group(2) or "/").lower()
        if path not in ("", "/") and not path.startswith(CONTENT_PATHS):
            return True
    return False


def plain(text: str) -> str:
    return re.sub(r"\]\([^)]*\)", "]", text).replace("[", "").replace("]", "")


def word_re(w: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z])" + re.escape(w) + r"(?:s|es)?(?![A-Za-z])", re.I)


def check_text(md: str, scope: list[tuple[str, list[str]]]) -> dict:
    if "ARTICLE STARTS HERE" in md:   # a review Doc exported as text: only the article counts
        md = md.split("ARTICLE STARTS HERE", 1)[1]
    claims, hits = [], []
    h1 = next((ln[2:] for ln in md.splitlines() if ln.startswith("# ")), "")
    for p, ctx in heading_context(strip_meta(md)):
        if not (attributes(p) or ctx):
            continue
        found = []
        for raw in SENTENCE.split(p):
            sent = plain(raw)
            for topic, words in scope:
                for w in words:
                    m = word_re(w).search(sent)
                    if m and not NEGATION.search(sent[:m.start()]):
                        # A word from the page's own title (a glossary entry for "In-App Purchase") is the topic of the
                        # page, so its "and social.plus" section must mention it: WARN, the reviewer checks the wording.
                        # Under social.plus's own list entry every sentence is about social.plus.
                        level = "FAIL" if ((attributes(raw) or ctx == "entry") and not word_re(w).search(h1)
                                           and not LIMITATION.search(sent)) else "WARN"
                        found.append({"topic": topic, "word": w, "level": level,
                                      "sentence": sent.strip()[:300]})
                        break
        claims.append({"paragraph": plain(p)[:600], "hits": found})
        hits += found
    return {"claims": claims, "hits": hits, "fails": [h for h in hits if h["level"] == "FAIL"], "scope_rows": len(scope)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("draft", type=Path)
    ap.add_argument("--capabilities", type=Path, default=Path(os.environ.get("MT_REPO", ROOT)) / "messaging" / "product-capabilities.md")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    scope = load_scope(a.capabilities)
    if not scope:
        print(f"product-capabilities.md not found or has no 'Outside social.plus scope' table: {a.capabilities}", file=sys.stderr)
        return 2
    r = check_text(a.draft.read_text(encoding="utf-8"), scope)
    if a.json:
        print(json.dumps(r, indent=1, ensure_ascii=False))
    else:
        for c in r["claims"]:
            flag = " <-- " + ", ".join(f'{h["level"]} {h["word"]} ({h["topic"]})' for h in c["hits"]) if c["hits"] else ""
            print(f"- {c['paragraph'][:200]}{flag}")
        print(f"{len(r['claims'])} paragraph(s) about social.plus, {len(r['fails'])} FAIL, {len(r['hits']) - len(r['fails'])} WARN")
    return 1 if r["fails"] else 0


if __name__ == "__main__":
    sys.exit(main())
