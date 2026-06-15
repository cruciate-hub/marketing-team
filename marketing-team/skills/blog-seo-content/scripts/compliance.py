#!/usr/bin/env python3
"""
Blog post compliance checker.

Deterministic checks for blog posts produced by the blog-seo-content skill.
Human / LLM judgment still owns tone, factuality, and citation quality — this
script owns the mechanical checks that slip past eyeball review.

The script reads the markdown intermediate (outputs/[slug].draft.md) that the
skill produces before converting the body to HTML for the Webflow `post-content`
field. Metadata lives in labeled paragraphs directly under the H1:

    # Page title

    Meta description: ...
    Slug: ...
    Alt text: ...
    Category: Community
    Tags: Community, Engagement
    Minutes to read: 6

    [intro paragraph — becomes post-summary]

    ## First body section

    ...

Usage:
    python3 scripts/compliance.py outputs/[slug].draft.md
    python3 scripts/compliance.py outputs/[slug].draft.md --min 800 --max 2500
    python3 scripts/compliance.py outputs/[slug].draft.md --json

Exit codes:
    0 — no failures (warnings are allowed)
    1 — at least one failure
    2 — usage error
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path


# Case-insensitive patterns — marketing fluff and category mislabels.
FORBIDDEN_TERMS_ANY_CASE = [
    r"\brevolutioni[sz]e\b",
    r"\bgame[- ]chang(ing|er)\b",
    r"\bunlock the power\b",
    # (?<![-\w]) excludes the hyphenated-compound case ("high-leverage" /
    # "higher-leverage" — legitimate strategy English). Expanded to all four
    # inflections so "leveraged" and "leverages" no longer slip through.
    r"(?<![-\w])leverag(e|es|ed|ing)\b",
    r"\bcutting[- ]edge\b",
    r"\bnext[- ]generation\b",
    r"\bbest[- ]in[- ]class\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bforum platform\b",
    r"\bchat tool\b",
    # terminology.md "Forbidden and Risky Terminology" — brand law, not style.
    r"\bad[- ]network\b",
    r"\bguarantee[ds]?\s+(?:growth|retention|revenue|results?|outcomes?|success|engagement)\b",
]

# The "social network" rule is self-referential only — social.plus must not
# call itself a social network. External references ("social networks such as
# Facebook") are legitimate and must not fire. Scope tightly.
SELF_REFERENTIAL_SOCIAL_NETWORK = [
    r"\bsocial\.plus\s+is\s+(?:a|an|the)?\s*social[- ]network\b",
    r"\bwe(?:'re|\s+are)\s+(?:a|an|the)?\s*social[- ]network\b",
]

# Risky terms — surfaced as WARN, not FAIL. terminology.md allows them in narrow
# contexts (e.g. "plug and play" is fine for developer/SDK copy but must not
# imply effortless community success in business-facing blog posts). WARN lets a
# human make the contextual call instead of hard-blocking a legitimate use.
RISKY_TERMS_WARN = [
    r"\bplug[- ]and[- ]play\b",
    # Self-referential "social network" via apposition: "social.plus, the social
    # network for apps". The FAIL patterns above catch the "is a/the" form; this
    # WARNs on the comma-descriptor form, where a hard FAIL would false-fire on
    # contrasts like "more than a social network".
    r"\bsocial\.plus\s*,\s*(?:a|an|the)\s+social[- ]network\b",
]

# Case-sensitive — brand-name casing (correct form: `social.plus`).
FORBIDDEN_TERMS_CASE_SENSITIVE = [
    r"\bSocial\.Plus\b",
    r"\bSocialPlus\b",
    r"\bSocial\+",  # no trailing \b: '+' is non-word, so \b only matches before a following word char
]

# Filler openers — fail if the first sentence starts with one of these.
FILLER_OPENERS = [
    r"^In today'?s\b",
    r"^Now more than ever\b",
    r"^In the ever[- ]evolving\b",
    r"^In a world where\b",
    r"^Gone are the days\b",
    r"^It'?s no secret\b",
    r"^As we all know\b",
    r"^In recent years\b",
]

APPROVED_CUSTOMERS = {"Noom", "Harley-Davidson", "Smart Fit", "Ulta Beauty", "Betgames"}

# Customer names we might accidentally reach for but which are not approved.
WATCHED_UNAPPROVED = re.compile(
    r"\b(?:Duolingo|Strava|Reddit|Discord|Slack|Peloton|Calm|Headspace)\b"
)

# Approved blog categories from blog-seo-content/SKILL.md.
APPROVED_CATEGORIES = {
    "Community",
    "App Growth",
    "Insights",
    "Engagement",
    "Retention",
    "Acquisition",
    "News",
    "Product",
    "Social+",
    "Vertical Social Networks",
    "Community Stories",
    "Monetization",
    "Education",
    "Hospitality",
    "Events",
    "People",
}

REQUIRED_METADATA = ["title", "metaDescription", "slug", "altText", "category"]

# Map the labeled-paragraph key (case/space-insensitive) to the canonical key.
LABELED_PARAGRAPH_KEYS = {
    "metadescription": "metaDescription",
    "slug": "slug",
    "alttext": "altText",
    "category": "category",
    "tags": "tags",
    "minutestoread": "minutesToRead",
}

DEFAULT_WORD_RANGE = (900, 2200)

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U0001F1E6-\U0001F1FF"
    "\U00002B00-\U00002BFF"
    "\U00002300-\U000023FF"  # ⏰ ⌚ ⏳ ⌨ etc.
    "\U000025A0-\U000025FF"  # ▶ ◀ ■ etc.
    "\U00002139"             # ℹ
    "\U00002049"             # ⁉
    "\U0000203C"             # ‼
    "☀-⛿"
    "✀-➿"
    "]"
)

EM_DASH = "—"
EM_DASH_ENTITY = re.compile(r"&mdash;|&#0*8212;|&#[xX]0*2014;")  # HTML-entity forms
HTML_TAG_PATTERN = re.compile(r"<[a-zA-Z/][^>]*>")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
MARKDOWN_IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class CheckResult:
    name: str
    status: str  # "PASS", "FAIL", "WARN"
    detail: str = ""


@dataclass
class Report:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def failed(self) -> list[CheckResult]:
        return [r for r in self.results if r.status == "FAIL"]

    @property
    def warned(self) -> list[CheckResult]:
        return [r for r in self.results if r.status == "WARN"]

    def as_json(self) -> str:
        return json.dumps(
            {
                "passed": len(self.failed) == 0,
                "failures": len(self.failed),
                "warnings": len(self.warned),
                "results": [
                    {"name": r.name, "status": r.status, "detail": r.detail}
                    for r in self.results
                ],
            },
            indent=2,
        )


def parse_metadata(text: str) -> tuple[dict[str, str], str]:
    """Extract labeled-paragraph metadata from the top of the document.

    Per the skill's intermediate format the metadata is a contiguous block of
    `Label: value` lines between the H1 and the first blank line (the intro
    paragraph follows that blank line). Returns `(metadata, body)`.

    Robustness rules — each fixes a real failure mode:
      * An unrecognized label (`Author:`, `Focus keyword:`) is skipped, not
        treated as end-of-metadata, so a stray field can't drop the real ones
        that follow it.
      * A non-label line *after* a known label is treated as a continuation of
        that value (a wrapped meta description), so the value is reassembled
        instead of silently truncated.
      * A non-label line with no preceding label ends the block (it is the
        body), so a post with no metadata isn't swallowed.

    `metadata` always contains `title` if an H1 is present; other keys appear
    only if the matching labeled paragraph existed.
    """
    meta: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines) and not lines[i].strip().startswith("# "):
        i += 1
    if i < len(lines):
        meta["title"] = lines[i].strip().lstrip("#").strip()
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    label_re = re.compile(r"^([A-Za-z][A-Za-z ]+?):\s*(.+)$")
    last_key = None
    while i < len(lines) and lines[i].strip():
        stripped = lines[i].strip()
        m = label_re.match(stripped)
        key_norm = m.group(1).lower().replace(" ", "") if m else ""
        if m and key_norm in LABELED_PARAGRAPH_KEYS:
            last_key = LABELED_PARAGRAPH_KEYS[key_norm]
            meta[last_key] = m.group(2).strip()
        elif m:
            last_key = None  # unrecognized label — skip it, keep scanning
        elif last_key is not None:
            meta[last_key] = f"{meta[last_key]} {stripped}".strip()  # wrapped value
        else:
            break  # non-label line and no metadata yet — this is the body
        i += 1
    body = "\n".join(lines[i:]).lstrip("\n")
    return meta, body


_QUOTE_FOLD = {
    0x2018: 0x27, 0x2019: 0x27,  # ‘ ’ → '
    0x201C: 0x22, 0x201D: 0x22,  # “ ” → "
    0x2032: 0x27, 0x2033: 0x22,  # ′ ″ → ' "
}


def normalize_quotes(s: str) -> str:
    """NFKC + fold curly quotes/apostrophes to straight. Used by the keyword
    checks so a curly apostrophe in the title vs. a straight one in the intro
    (or vice versa) doesn't false-fail an obviously-present keyword.
    """
    return unicodedata.normalize("NFKC", s).translate(_QUOTE_FOLD)


def strip_fenced_code(text: str) -> str:
    """Drop fenced code blocks only. Lighter than strip_code_and_link_urls —
    used by the heading checks (which only need to ignore code-block `#` lines)
    and by check_html_tags (which already does this inline).
    """
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def strip_code_and_link_urls(text: str) -> str:
    """Remove syntax that's part of markdown infrastructure but not displayed
    prose: fenced code blocks, inline code, HTML comments, and URL targets
    inside markdown links/images. Anchor text and image alt text are kept.

    Used for checks that should only inspect what a reader sees — forbidden
    terms, em dashes, emojis, raw HTML — so a forbidden term mentioned in a
    code example or appearing inside a link URL doesn't false-fire.
    """
    t = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL)
    t = re.sub(r"`[^`]+`", "", t)
    t = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


def word_count(text: str) -> int:
    t = strip_code_and_link_urls(text)
    t = re.sub(r"^\s*\|.*\|\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^#+\s+", "", t, flags=re.MULTILINE)
    return len(re.findall(r"\b[\w'-]+\b", t))


def first_paragraph(body: str) -> str:
    after_h1 = re.sub(r"\A#\s+.+?\n+", "", body, count=1)
    for block in after_h1.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        if re.fullmatch(r"<!--.*?-->", stripped, flags=re.DOTALL):
            continue
        return stripped
    return ""


def first_sentence(body: str) -> str:
    para = first_paragraph(body)
    s = re.split(r"(?<=[.!?])\s+", para)[0].strip()
    # Strip leading markdown emphasis/blockquote/list markers so a filler
    # opener wrapped in `**` or prefixed by `>` still matches.
    return re.sub(r"^(?:[*_>\s]|[-*+]\s+)+", "", s)


def extract_keyword_phrase(title: str) -> str:
    # SEO titles put the keyword before a subtitle colon ("Keyword: Subtitle").
    # Keep only the part before the first colon so the subtitle's words don't
    # contaminate the phrase and break the first-paragraph / H2 keyword match.
    head = title.split(":", 1)[0].strip()
    if head:
        title = head
    t = re.sub(
        r"^(what\s+(is|are|does|do)|how\s+to|how\s+do\s+you|guide\s+to|"
        r"why|when|where|introduction\s+to|the\s+ultimate\s+guide\s+to)\s+",
        "",
        title,
        flags=re.IGNORECASE,
    )
    return t.rstrip("?.! ").strip()


# ---------- individual checks ----------


def check_metadata(meta: dict[str, str]) -> list[CheckResult]:
    results: list[CheckResult] = []
    for key in REQUIRED_METADATA:
        present = bool(meta.get(key))
        results.append(
            CheckResult(
                f"metadata_{key}",
                "PASS" if present else "FAIL",
                "" if present else "missing or empty",
            )
        )
    return results


def check_title_length(meta: dict[str, str]) -> list[CheckResult]:
    """SEO sweet spot is 50-60 characters. Webflow hard limit is 256."""
    title = meta.get("title", "")
    if not title:
        return [CheckResult("title_length", "FAIL", "no title (no H1 found)")]
    n = len(title)
    if n > 256:
        return [CheckResult("title_length", "FAIL", f"{n} chars (Webflow max 256)")]
    if 50 <= n <= 60:
        return [CheckResult("title_length", "PASS", f"{n} chars (target 50-60)")]
    return [CheckResult("title_length", "WARN", f"{n} chars (target 50-60 for SEO)")]


def check_meta_description(meta: dict[str, str]) -> CheckResult:
    md = meta.get("metaDescription", "")
    length = len(md)
    ok = 1 <= length <= 160
    return CheckResult(
        "meta_description_length",
        "PASS" if ok else "FAIL",
        f"{length} chars (max 160)" + ("" if md else " — missing"),
    )


def check_slug(meta: dict[str, str]) -> CheckResult:
    slug = meta.get("slug", "")
    if not slug:
        return CheckResult("slug_format", "FAIL", "missing")
    if len(slug) > 256:
        return CheckResult("slug_format", "FAIL", f"too long: {len(slug)} > 256")
    if slug != slug.lower():
        return CheckResult("slug_format", "FAIL", f"must be lowercase: {slug}")
    if re.search(r"[^a-z0-9-]", slug):
        return CheckResult("slug_format", "FAIL", f"invalid chars (only a-z, 0-9, hyphen allowed): {slug}")
    if "--" in slug:
        return CheckResult("slug_format", "FAIL", f"consecutive hyphens: {slug}")
    if slug.startswith("-") or slug.endswith("-"):
        return CheckResult("slug_format", "FAIL", f"leading/trailing hyphen: {slug}")
    return CheckResult("slug_format", "PASS", slug)


def check_category(meta: dict[str, str]) -> CheckResult:
    cat = meta.get("category", "")
    if not cat:
        return CheckResult("category_approved", "FAIL", "missing")
    if cat in APPROVED_CATEGORIES:
        return CheckResult("category_approved", "PASS", cat)
    return CheckResult(
        "category_approved",
        "FAIL",
        f"'{cat}' not in approved list: {sorted(APPROVED_CATEGORIES)}",
    )


def check_word_count(body: str, lo: int, hi: int) -> CheckResult:
    wc = word_count(body)
    if lo <= wc <= hi:
        return CheckResult("word_count", "PASS", f"{wc} words (target {lo}-{hi})")
    return CheckResult("word_count", "WARN", f"{wc} words (target {lo}-{hi})")


def check_keyword_in_first_paragraph(meta: dict[str, str], body: str) -> CheckResult:
    """Target keyword must appear in the first paragraph of the body.

    First paragraph is the intro (becomes post-summary). LLMs tolerate
    morphology, so we accept either the full keyword phrase or a 3-word
    subsequence; for short phrases we require all content words.
    """
    title = meta.get("title", "")
    if not title:
        return CheckResult("keyword_in_first_paragraph", "FAIL", "no title (no H1 found)")
    phrase = normalize_quotes(extract_keyword_phrase(title)).lower()
    para = normalize_quotes(first_paragraph(body)).lower()
    if not para:
        return CheckResult("keyword_in_first_paragraph", "FAIL", "no first paragraph found")
    if phrase in para:
        return CheckResult(
            "keyword_in_first_paragraph",
            "PASS",
            f"full phrase '{phrase}' found",
        )
    words = phrase.split()
    if len(words) < 3:
        missing = [w for w in words if w not in para]
        if not missing:
            return CheckResult("keyword_in_first_paragraph", "PASS", "all keyword words present")
        return CheckResult(
            "keyword_in_first_paragraph",
            "FAIL",
            f"missing words from '{phrase}': {missing}",
        )
    for i in range(len(words) - 2):
        trigram = " ".join(words[i : i + 3])
        if trigram in para:
            return CheckResult(
                "keyword_in_first_paragraph",
                "PASS",
                f"3-word match '{trigram}' found (full phrase not literal)",
            )
    return CheckResult(
        "keyword_in_first_paragraph",
        "FAIL",
        f"no 3-word subsequence of '{phrase}' found in first paragraph",
    )


def check_keyword_in_h2(meta: dict[str, str], body: str) -> CheckResult:
    """At least one H2 should contain a recognizable keyword variant.

    SEO signal — keyword presence in subheadings helps content relevance.
    WARN rather than FAIL since strict keyword-stuffing in H2s reads worse
    than a natural variant.
    """
    title = meta.get("title", "")
    if not title:
        return CheckResult("keyword_in_h2", "WARN", "no title to compare against")
    phrase = normalize_quotes(extract_keyword_phrase(title)).lower()
    words = [w for w in phrase.split() if len(w) > 2]
    if not words:
        return CheckResult("keyword_in_h2", "WARN", "keyword too short to check")
    h2_body = strip_fenced_code(body)
    h2s = [normalize_quotes(m.group(2)).lower() for m in HEADING_PATTERN.finditer(h2_body) if len(m.group(1)) == 2]
    if not h2s:
        return CheckResult("keyword_in_h2", "WARN", "no H2 headings found")
    for h2 in h2s:
        hits = sum(1 for w in words if w in h2)
        if hits >= max(1, len(words) // 2):
            return CheckResult("keyword_in_h2", "PASS", f"keyword variant found in H2: '{h2[:60]}'")
    return CheckResult(
        "keyword_in_h2",
        "WARN",
        f"no H2 contains a recognizable variant of '{phrase}' ({len(h2s)} H2s checked)",
    )


def check_filler_opener(body: str) -> CheckResult:
    s1 = first_sentence(body)
    for pattern in FILLER_OPENERS:
        if re.match(pattern, s1, re.IGNORECASE):
            return CheckResult(
                "no_filler_opener",
                "FAIL",
                f"sentence 1 starts with a filler phrase: {s1[:50]}…",
            )
    return CheckResult("no_filler_opener", "PASS", "")


def check_em_dashes(text: str) -> CheckResult:
    prose = strip_code_and_link_urls(text)
    count = prose.count(EM_DASH) + len(EM_DASH_ENTITY.findall(prose))
    return CheckResult(
        "no_em_dashes",
        "PASS" if count == 0 else "FAIL",
        f"found {count} em dashes" if count else "0",
    )


def check_emojis(text: str) -> CheckResult:
    prose = strip_code_and_link_urls(text)
    hits = EMOJI_PATTERN.findall(prose)
    return CheckResult(
        "no_emojis",
        "PASS" if not hits else "FAIL",
        f"found {len(hits)} emoji(s)" if hits else "0",
    )


def check_forbidden_terms(text: str) -> CheckResult:
    prose = strip_code_and_link_urls(text)
    hits: list[str] = []
    for pattern in FORBIDDEN_TERMS_ANY_CASE:
        for m in re.finditer(pattern, prose, re.IGNORECASE):
            hits.append(m.group(0))
    for pattern in SELF_REFERENTIAL_SOCIAL_NETWORK:
        for m in re.finditer(pattern, prose, re.IGNORECASE):
            hits.append(m.group(0))
    for pattern in FORBIDDEN_TERMS_CASE_SENSITIVE:
        for m in re.finditer(pattern, prose):
            hits.append(m.group(0))
    return CheckResult(
        "no_forbidden_terms",
        "PASS" if not hits else "FAIL",
        "found: " + ", ".join(sorted(set(hits))) if hits else "0",
    )


def check_risky_terms(text: str) -> CheckResult:
    """Context-dependent terminology — WARN, not FAIL (see RISKY_TERMS_WARN)."""
    prose = strip_code_and_link_urls(text)
    hits: list[str] = []
    for pattern in RISKY_TERMS_WARN:
        for m in re.finditer(pattern, prose, re.IGNORECASE):
            hits.append(m.group(0))
    return CheckResult(
        "no_risky_terms",
        "PASS" if not hits else "WARN",
        "review (terminology.md context rules): " + ", ".join(sorted(set(hits))) if hits else "0",
    )


def check_html_tags(body: str) -> CheckResult:
    """Forbid raw HTML in the markdown intermediate. The final delivery
    converts the body to HTML for the Webflow `post-content` field; HTML in
    the markdown source corrupts the conversion. Also catches
    `<sprscript-green>` (customer-story tag, not for blog).

    Code blocks are stripped first — a code block showing an HTML example is
    legitimate. HTML comments outside code are still flagged since some
    markdown converters render them as visible text.
    """
    prose = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    prose = re.sub(r"`[^`]+`", "", prose)
    # CommonMark autolinks (<https://…>, <mailto:…>, <user@host>) are legitimate
    # markdown, not raw HTML — strip them before the tag scan.
    prose = re.sub(r"<(?:https?://|mailto:)[^>\s]+>", "", prose)
    prose = re.sub(r"<\S+@\S+>", "", prose)
    tag_hits = HTML_TAG_PATTERN.findall(prose)
    comment_hits = re.findall(r"<!--.*?-->", prose, flags=re.DOTALL)
    total = len(tag_hits) + len(comment_hits)
    if total == 0:
        return CheckResult("no_html", "PASS", "0")
    details = []
    if tag_hits:
        details.append(f"{len(tag_hits)} tag(s): {tag_hits[:3]}")
    if comment_hits:
        trimmed = [c[:40] + "…" if len(c) > 40 else c for c in comment_hits[:2]]
        details.append(f"{len(comment_hits)} comment(s): {trimmed}")
    return CheckResult("no_html", "FAIL", "; ".join(details))


def check_headings(body: str) -> list[CheckResult]:
    # Strip fenced code blocks first — a `# Install the CLI` comment inside a
    # shell snippet is not a real H1 (this matches what check_html_tags and
    # the prose-sensitive checks already do).
    clean = strip_fenced_code(body)
    headings = HEADING_PATTERN.findall(clean)
    levels = [len(h[0]) for h in headings]
    results: list[CheckResult] = []
    h1_count = levels.count(1)
    results.append(
        CheckResult(
            "single_h1",
            "PASS" if h1_count == 1 else "FAIL",
            f"found {h1_count} H1 heading(s)",
        )
    )
    # WARN, not FAIL — measured against pages-blog.json, 19% of live posts skip
    # a level (44 of those go H1→H3, using H3 as the top-level section header).
    # Hard-FAILing the house style would block ~17% of valid drafts.
    skipped = any(b > a + 1 for a, b in zip(levels, levels[1:]))
    results.append(
        CheckResult(
            "no_skipped_heading_levels",
            "PASS" if not skipped else "WARN",
            "well-formed" if not skipped else "a heading level was skipped (informational — house style allows H1→H3)",
        )
    )
    return results


def check_image_alt_text(body: str) -> CheckResult:
    """Every markdown image must have non-empty alt text."""
    images = MARKDOWN_IMAGE_PATTERN.findall(body)
    if not images:
        return CheckResult("image_alt_text", "PASS", "no inline images")
    missing = [url for alt, url in images if not alt.strip()]
    if missing:
        return CheckResult(
            "image_alt_text",
            "FAIL",
            f"{len(missing)} image(s) missing alt text: {missing[:3]}",
        )
    return CheckResult("image_alt_text", "PASS", f"all {len(images)} image(s) have alt text")


def check_approved_customers(body: str) -> CheckResult:
    hits = WATCHED_UNAPPROVED.findall(body)
    unapproved = [h for h in hits if h not in APPROVED_CUSTOMERS]
    return CheckResult(
        "approved_customers_only",
        "PASS" if not unapproved else "FAIL",
        f"unapproved mentions: {sorted(set(unapproved))}" if unapproved else "0",
    )


def check_reading_time(meta: dict[str, str], body: str) -> CheckResult:
    """Sanity-check the claimed `Minutes to read` against the actual word count
    at ~250 wpm. LLMs often paste a stale or made-up reading time; WARN when
    the claimed value drifts by more than 1 minute from the computed value.
    """
    claimed_raw = meta.get("minutesToRead", "")
    if not claimed_raw:
        return CheckResult("reading_time", "PASS", "no claim to verify")
    m = re.search(r"\d+", claimed_raw)
    if not m:
        return CheckResult("reading_time", "WARN", f"unparseable: {claimed_raw!r}")
    claimed = int(m.group(0))
    actual = max(1, round(word_count(body) / 250))
    if abs(claimed - actual) <= 1:
        return CheckResult("reading_time", "PASS", f"claimed {claimed}, computed ~{actual}")
    return CheckResult(
        "reading_time",
        "WARN",
        f"claimed {claimed} min, ~{actual} min by word count (delta {abs(claimed - actual)})",
    )


def check_no_jsonld(body: str) -> CheckResult:
    """Webflow handles schema at the template level; the body should not
    emit JSON-LD.
    """
    if re.search(r"```json-ld", body, re.IGNORECASE):
        return CheckResult(
            "no_jsonld_block",
            "FAIL",
            "found a ```json-ld block — Webflow handles schema at the template level",
        )
    if re.search(r"application/ld\+json", body, re.IGNORECASE):
        return CheckResult(
            "no_jsonld_block",
            "FAIL",
            "found an inline JSON-LD script — Webflow handles schema",
        )
    return CheckResult("no_jsonld_block", "PASS", "")


# ---------- runner ----------


def _read_draft(path: Path) -> str:
    """Try UTF-8 (with BOM strip) first; fall back to cp1252 — common when
    prose was pasted from Word, which emits 0x97 for the em dash. Falling back
    to cp1252 preserves the em dash so the no_em_dashes check still fires;
    decoding with errors='replace' would silently drop it.
    """
    try:
        return path.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="cp1252")
        except UnicodeDecodeError as e:
            raise SystemExit(f"error: could not decode {path} as utf-8 or cp1252: {e}")


def run(path: Path, lo: int | None, hi: int | None) -> Report:
    report = Report()
    text = _read_draft(path)
    meta, body = parse_metadata(text)

    lo = lo if lo is not None else DEFAULT_WORD_RANGE[0]
    hi = hi if hi is not None else DEFAULT_WORD_RANGE[1]

    body_with_h1 = f"# {meta.get('title', '')}\n\n{body}" if meta.get("title") else body
    # Reader-facing prose the checks should scan: body + title + meta
    # description (Google snippet) + alt text (screen-reader text, ships in the
    # `image-alt-text` Webflow field). All four obey the same em-dash / emoji /
    # terminology rules.
    extras = [v for v in (meta.get("metaDescription"), meta.get("altText")) if v]
    prose = "\n\n".join([body_with_h1, *extras])

    report.results.extend(check_metadata(meta))
    report.results.extend(check_title_length(meta))
    report.results.append(check_meta_description(meta))
    report.results.append(check_slug(meta))
    report.results.append(check_category(meta))
    report.results.append(check_word_count(body, lo, hi))
    report.results.append(check_reading_time(meta, body))
    report.results.append(check_keyword_in_first_paragraph(meta, body))
    report.results.append(check_keyword_in_h2(meta, body))
    report.results.append(check_filler_opener(body))
    report.results.append(check_em_dashes(prose))
    report.results.append(check_emojis(prose))
    report.results.append(check_forbidden_terms(prose))
    report.results.append(check_risky_terms(prose))
    report.results.append(check_html_tags(body))
    report.results.append(check_no_jsonld(body))
    report.results.extend(check_headings(body_with_h1))
    report.results.append(check_image_alt_text(body))
    report.results.append(check_approved_customers(body_with_h1))

    return report


def scan_text(text: str) -> Report:
    """Scan an arbitrary string for em-dashes, emojis, and forbidden terms.
    Used by `--scan-text` to vet linker-supplied anchor text after the main
    compliance pass — the linker injects anchors into the HTML *after* the
    draft.md is checked, so its output otherwise bypasses the gate.
    """
    report = Report()
    report.results.append(check_em_dashes(text))
    report.results.append(check_emojis(text))
    report.results.append(check_forbidden_terms(text))
    report.results.append(check_risky_terms(text))
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Blog post compliance checker")
    parser.add_argument("path", nargs="?", type=Path, help="Path to the article markdown file")
    parser.add_argument("--min", type=int, help="Override minimum word count")
    parser.add_argument("--max", type=int, help="Override maximum word count")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument(
        "--scan-text",
        help="Scan a single string (e.g. a linker-supplied anchor) for em-dashes / "
             "emojis / forbidden terms instead of a draft file. Use this after the "
             "main compliance pass to vet each anchor returned by "
             "internal-linking-strategist before embedding.",
    )
    args = parser.parse_args()

    if args.scan_text is not None:
        report = scan_text(args.scan_text)
    else:
        if args.path is None:
            parser.error("either a draft path or --scan-text is required")
        if not args.path.exists():
            print(f"file not found: {args.path}", file=sys.stderr)
            return 2
        report = run(args.path, args.min, args.max)

    if args.json:
        print(report.as_json())
    else:
        label = args.scan_text if args.scan_text is not None else args.path
        print(f"Blog compliance report for {label}\n")
        for r in report.results:
            line = f"  [{r.status:4}] {r.name}"
            if r.detail:
                line += f" — {r.detail}"
            print(line)
        print()
        n_fail = len(report.failed)
        n_warn = len(report.warned)
        if n_fail:
            print(f"{n_fail} failure(s), {n_warn} warning(s) — fix failures before delivery.")
        elif n_warn:
            print(f"No failures, {n_warn} warning(s) — review and decide whether to address.")
        else:
            print("All checks passed.")

    return 0 if not report.failed else 1


if __name__ == "__main__":
    sys.exit(main())
