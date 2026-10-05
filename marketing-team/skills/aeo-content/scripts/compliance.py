#!/usr/bin/env python3
"""
AEO article compliance checker.

Deterministic checks for AEO articles produced by the aeo-content skill.
Human / LLM judgment still owns tone, factuality, and citation quality — this
script owns the mechanical checks that slip past eyeball review.

The script reads the markdown intermediate (outputs/[slug].draft.md) that the
skill produces before converting to `.docx`. Metadata lives in labeled
paragraphs directly under the H1:

    # Article title

    Meta description: ...
    Slug: ...
    Alt text: ...
    Intent: how-to | decision | explainer | playbook
    Queue ID: A1
    Last updated: 2026-09-24
    Editor (named human reviewer): [fill before publish]

    [answer-first block starts here]

Usage:
    python scripts/compliance.py path/to/article.draft.md
    python scripts/compliance.py path/to/article.draft.md --intent how-to
    python scripts/compliance.py path/to/article.draft.md --min 700 --max 1500
    python scripts/compliance.py path/to/article.draft.md --queue queue.csv
    python scripts/compliance.py path/to/article.draft.md --json

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
from dataclasses import dataclass, field
from pathlib import Path


# Case-insensitive patterns — marketing fluff and category mislabels.
# Kept in sync with blog-seo-content/scripts/compliance.py (shared brand law).
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
    # Anti-slop vocabulary, hard-block tier (SKILL.md "Anti-slop rules").
    # Unedited AI-generation patterns are the "little added value" signal
    # Google's scaled-content enforcement keys on; these have no legitimate
    # blog use. Context-dependent items live in RISKY_TERMS_WARN below —
    # keep both tiers in sync with the SKILL.md list.
    r"\bdelv(e|es|ed|ing)\b",
    r"\bin today[’']?s fast[- ]paced\b",
    r"\bdigital landscape\b",
    r"\bever[- ]evolving\b",
]

# The "social network" rule is self-referential only — social.plus must not
# call itself a social network. External references ("social networks such as
# Facebook") are legitimate and essential in AEO comparative articles — they
# must not fire. Scope tightly.
SELF_REFERENTIAL_SOCIAL_NETWORK = [
    r"\bsocial\.plus\s+is\s+(?:a|an|the)?\s*social[- ]network\b",
    r"\bwe(?:'re|\s+are)\s+(?:a|an|the)?\s*social[- ]network\b",
]

# Risky terms — surfaced as WARN, not FAIL. terminology.md allows them in
# narrow contexts; WARN lets a human make the contextual call instead of
# hard-blocking a legitimate use.
RISKY_TERMS_WARN = [
    r"\bplug[- ]and[- ]play\b",
    # Self-referential "social network" via apposition: "social.plus, the social
    # network for apps". The FAIL patterns above catch the "is a/the" form; this
    # WARNs on the comma-descriptor form, where a hard FAIL would false-fire on
    # contrasts like "more than a social network".
    r"\bsocial\.plus\s*,\s*(?:a|an|the)\s+social[- ]network\b",
    # Anti-slop vocabulary, context-dependent tier (SKILL.md "Anti-slop
    # rules"). Legitimate in narrow technical uses ("robust error handling",
    # "unlock a locked account"); slop as generic marketing filler. WARN so a
    # human makes the contextual call. Hard-block tier lives in
    # FORBIDDEN_TERMS_ANY_CASE above — keep both tiers in sync with SKILL.md.
    r"\bunlock(s|ed|ing)?\b",
    r"\belevat(e|es|ed|ing)\b",
    r"\bseamless(ly)?\b",
    r"\brobust(ly|ness)?\b",
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

# Required metadata keys. `title` comes from the H1; the rest come from
# labeled paragraphs directly under the H1 ("Meta description: …", etc.).
REQUIRED_METADATA = ["title", "metaDescription", "slug", "altText", "intent", "queueId"]

# Map the labeled-paragraph key (case/space-insensitive) to the canonical key.
LABELED_PARAGRAPH_KEYS = {
    "metadescription": "metaDescription",
    "slug": "slug",
    "alttext": "altText",
    "intent": "intent",
    "queueid": "queueId",
    "lastupdated": "lastUpdated",
    "editor(namedhumanreviewer)": "editor",
}

# v2 templates. "What is X?" definitions belong to glossary-content, not here.
VALID_INTENTS = {"how-to", "decision", "explainer", "playbook"}
RETIRED_INTENTS = {"definition", "procedural", "comparative"}

# Intent-specific defaults.
INTENT_WORD_RANGE: dict[str, tuple[int, int]] = {
    "how-to": (700, 1500),
    "decision": (700, 1500),
    "explainer": (700, 1500),
    "playbook": (700, 1500),
}

INTENT_CITATION_MIN: dict[str, int] = {
    "how-to": 0,     # internal product consistency instead
    "decision": 3,   # you are comparing things: cite the things
    "explainer": 2,  # claims about why/whether need outside evidence
    "playbook": 1,
}

SUMMARY_RANGE = (80, 150)
ANSWER_FIRST_RANGE = (25, 60)
MIN_STATISTICS = 3
FAQ_RANGE = (3, 5)
PITCH_RANGE = (80, 150)
QUESTION_HEADING_SHARE = 0.6

# Headings that produced identical boilerplate across the legacy collection.
BOILERPLATE_HEADINGS = re.compile(
    r"^(?:the\s+)?(?:leading|best|top)\s+.*:\s*social\.plus\s*$"
    r"|^why\s+social\.plus\s+(?:powers|is)\b"
    r"|^why\s+teams\s+(?:build|choose|use)\b.*social\.plus",
    re.IGNORECASE,
)
NON_QUESTION_SECTIONS = re.compile(r"^(faqs?|frequently asked questions|conclusion|summary)$", re.IGNORECASE)

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
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]"
)

EM_DASH = "\u2014"
HTML_TAG_PATTERN = re.compile(r"<[a-zA-Z/][^>]*>")
MARKDOWN_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")
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

    Returns `(metadata, body_after_metadata)`. `metadata` always contains
    `title` if an H1 is present; the four label keys (metaDescription, slug,
    altText, intent) are present only if the matching labeled paragraph
    existed.

    Expected top-of-document structure:

        # Article title

        Meta description: ...
        Slug: ...
        Alt text: ...
        Intent: ...

        [answer-first block starts here]

    The function accepts a blank line between the H1 and the labeled
    paragraphs. It stops collecting metadata at the first non-labeled,
    non-blank line (that line is the start of the body).
    """
    meta: dict[str, str] = {}
    lines = text.splitlines()
    i = 0
    # Find the H1.
    while i < len(lines) and not lines[i].strip().startswith("# "):
        i += 1
    if i < len(lines):
        meta["title"] = lines[i].strip().lstrip("#").strip()
        i += 1
    # Skip blank lines.
    while i < len(lines) and not lines[i].strip():
        i += 1
    # Consume labeled paragraphs.
    label_re = re.compile(r"^([A-Za-z][A-Za-z ()]+?):\s*(.+)$")
    while i < len(lines):
        stripped = lines[i].strip()
        if not stripped:
            # Blank line — provisionally end of metadata, but skip and continue
            # only if the next non-blank line is also a labeled paragraph.
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j >= len(lines):
                i = j
                break
            next_stripped = lines[j].strip()
            if label_re.match(next_stripped) and next_stripped.split(":", 1)[0].lower().replace(" ", "") in LABELED_PARAGRAPH_KEYS:
                i = j
                continue
            i = j
            break
        m = label_re.match(stripped)
        if not m:
            break
        key_raw, value = m.group(1), m.group(2)
        key_norm = key_raw.lower().replace(" ", "")
        if key_norm in LABELED_PARAGRAPH_KEYS:
            meta[LABELED_PARAGRAPH_KEYS[key_norm]] = value.strip()
            i += 1
            continue
        break
    # Remaining lines are the body.
    body = "\n".join(lines[i:]).lstrip("\n")
    return meta, body


def word_count(text: str) -> int:
    # Strip code fences, inline code, HTML comments, table rows, headings.
    t = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL)
    t = re.sub(r"`[^`]+`", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"^\s*\|.*\|\s*$", "", t, flags=re.MULTILINE)
    t = re.sub(r"^#+\s+", "", t, flags=re.MULTILINE)
    return len(re.findall(r"\b[\w'-]+\b", t))


def first_paragraph(body: str) -> str:
    """The first prose paragraph of the body.

    Robust to:
    - a leftover H1 at the top (`parse_metadata` removes it, but accept both)
    - stray HTML comments that the `no_html` check will separately flag
    """
    after_h1 = re.sub(r"\A#\s+.+?\n+", "", body, count=1)
    for block in after_h1.split("\n\n"):
        stripped = block.strip()
        if not stripped:
            continue
        # Skip pure-comment paragraphs.
        if re.fullmatch(r"<!--.*?-->", stripped, flags=re.DOTALL):
            continue
        return stripped
    return ""


def first_two_sentences(body: str) -> tuple[str, int]:
    para = first_paragraph(body)
    sentences = re.split(r"(?<=[.!?])\s+", para)
    two = " ".join(sentences[:2]).strip()
    return two, len(re.findall(r"\b[\w'-]+\b", two))


def first_sentence(body: str) -> str:
    para = first_paragraph(body)
    return re.split(r"(?<=[.!?])\s+", para)[0].strip()


def extract_keyword_phrase(title: str) -> str:
    """Strip common interrogative prefixes and trailing punctuation to get the
    keyword phrase from a title.
    """
    t = re.sub(
        r"^(what\s+(is|are|does|do|should)|how\s+much\s+does|how\s+long\s+does|how\s+to|how\s+do\s+you|how\s+do|"
        r"should\s+(you|i)|do|does|which|who|guide\s+to|"
        r"why|when|where|introduction\s+to|the\s+ultimate\s+guide\s+to)\s+",
        "",
        title,
        flags=re.IGNORECASE,
    )
    return t.rstrip("?.! ").strip()


def strip_code_and_link_urls(text: str) -> str:
    """Remove syntax that's part of markdown infrastructure but not displayed
    prose: fenced code blocks, inline code, HTML comments, and URL targets
    inside markdown links/images. Anchor text and image alt text are kept.

    Used for the terminology checks so a forbidden term mentioned in a code
    example or appearing inside a link URL doesn't false-fire.
    """
    t = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.DOTALL)
    t = re.sub(r"`[^`]+`", "", t)
    t = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


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
    intent = meta.get("intent", "")
    if intent:
        ok = intent in VALID_INTENTS
        if intent in RETIRED_INTENTS:
            results.append(CheckResult("metadata_intent_valid", "FAIL",
                f"intent={intent} is a v1 intent. Use one of {sorted(VALID_INTENTS)}; "
                "'definition' pages belong to glossary-content."))
            return results
        results.append(
            CheckResult(
                "metadata_intent_valid",
                "PASS" if ok else "FAIL",
                f"intent={intent}"
                + (f" (expected one of {sorted(VALID_INTENTS)})" if not ok else ""),
            )
        )
    return results


def check_meta_description(meta: dict[str, str]) -> CheckResult:
    md = meta.get("metaDescription", "")
    length = len(md)
    ok = 1 <= length <= 160
    return CheckResult(
        "meta_description_length",
        "PASS" if ok else "FAIL",
        f"{length} chars (max 160)" + ("" if md else " — missing"),
    )


def check_word_count(body: str, lo: int, hi: int) -> CheckResult:
    wc = word_count(body)
    if lo <= wc <= hi:
        return CheckResult("word_count", "PASS", f"{wc} words (target {lo}-{hi})")
    detail = f"{wc} words (target {lo}-{hi})"
    return CheckResult("word_count", "WARN", detail)


def check_answer_first(body: str) -> CheckResult:
    _, wc = first_two_sentences(body)
    lo, hi = ANSWER_FIRST_RANGE
    ok = lo <= wc <= hi
    return CheckResult(
        "answer_first_block",
        "PASS" if ok else "FAIL",
        f"first two sentences = {wc} words (target {lo}-{hi})",
    )


def check_summary_word_count(body: str) -> CheckResult:
    """The summary paragraph sits directly under the answer-first block and
    above the first H2. AI citations cluster early on the page (one analysis
    of 1.2M ChatGPT answers found 44.2% of citations come from the first 30%
    of content), so a direct answer plus a short standalone summary is
    front-loaded on purpose. The 80-150 range is an editorial choice, not a
    research threshold.
    """
    paragraphs: list[str] = []
    for p in body.split("\n\n"):
        stripped = p.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            break
        paragraphs.append(stripped)
    if len(paragraphs) < 2:
        return CheckResult("summary_word_count", "FAIL",
            "summary paragraph not found (expected below the answer-first block, above the first H2)")
    if len(paragraphs) > 2:
        return CheckResult("summary_word_count", "FAIL",
            f"{len(paragraphs)} paragraphs before the first H2 (expected exactly 2: answer-first block, summary)")
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", paragraphs[1])
    wc = len(re.findall(r"\b[\w'-]+\b", plain))
    lo, hi = SUMMARY_RANGE
    status = "PASS" if lo <= wc <= hi else ("WARN" if lo - 10 <= wc <= hi + 10 else "FAIL")
    return CheckResult("summary_word_count", status, f"summary = {wc} words (target {lo}-{hi})")


def check_keyword_in_sentence_1(meta: dict[str, str], body: str) -> CheckResult:
    """Sentence 1 must contain a recognizable form of the title's keyword phrase.

    Practical rule: LLMs tolerate morphology ("add X" <-> "Adding X"), so we
    don't require a literal substring match. The check passes if either:
      1. The full keyword phrase appears verbatim (the best case), or
      2. A 3-word subsequence from the phrase appears verbatim.

    For very short keyword phrases (<3 words) we fall back to requiring all
    the phrase's content words to appear somewhere in sentence 1.
    """
    title = meta.get("title", "")
    if not title:
        return CheckResult(
            "keyword_in_first_sentence",
            "FAIL",
            "no title (no H1 found)",
        )
    phrase = extract_keyword_phrase(title)
    s1 = first_sentence(body).lower()
    phrase_lower = phrase.lower()

    if phrase_lower in s1:
        return CheckResult(
            "keyword_in_first_sentence",
            "PASS",
            f"full phrase '{phrase}' found in sentence 1",
        )

    words = phrase_lower.split()
    if len(words) < 3:
        missing = [w for w in words if w not in s1]
        if not missing:
            return CheckResult(
                "keyword_in_first_sentence",
                "PASS",
                f"all keyword words present in sentence 1",
            )
        return CheckResult(
            "keyword_in_first_sentence",
            "FAIL",
            f"missing words from keyword '{phrase}': {missing}",
        )

    for i in range(len(words) - 2):
        trigram = " ".join(words[i : i + 3])
        if trigram in s1:
            return CheckResult(
                "keyword_in_first_sentence",
                "PASS",
                f"3-word match '{trigram}' found (full phrase '{phrase}' not literal)",
            )

    return CheckResult(
        "keyword_in_first_sentence",
        "FAIL",
        f"no 3-word subsequence of '{phrase}' found in sentence 1",
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
    count = text.count(EM_DASH)
    return CheckResult(
        "no_em_dashes",
        "PASS" if count == 0 else "FAIL",
        f"found {count} em dashes" if count else "0",
    )


def check_emojis(text: str) -> CheckResult:
    hits = EMOJI_PATTERN.findall(text)
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
    """Forbid ALL HTML in the markdown intermediate. The final output is a Word
    document and a downstream automation converts it to Webflow HTML. HTML in
    the source corrupts both. Includes `<!-- comments -->`, which some
    markdown→docx converters render as visible text.
    """
    # A whole <figure>…</figure> block is an image or video carried over from the live page on a
    # rewrite (webflow-publisher passes it through unchanged) — legitimate, not stray HTML.
    body = re.sub(r"<figure\b.*?</figure>", "", body, flags=re.DOTALL | re.IGNORECASE)
    tag_hits = HTML_TAG_PATTERN.findall(body)
    comment_hits = re.findall(r"<!--.*?-->", body, flags=re.DOTALL)
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
    headings = HEADING_PATTERN.findall(body)
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
    skipped = any(b > a + 1 for a, b in zip(levels, levels[1:]))
    results.append(
        CheckResult(
            "no_skipped_heading_levels",
            "PASS" if not skipped else "FAIL",
            "well-formed" if not skipped else "a heading level was skipped",
        )
    )
    return results


def check_citations(body: str, intent: str) -> CheckResult:
    links = MARKDOWN_LINK_PATTERN.findall(body)
    external = [u for _, u in links if "social.plus" not in u]
    minimum = INTENT_CITATION_MIN.get(intent, 0)
    count = len(external)
    if minimum == 0:
        return CheckResult(
            "external_citations",
            "PASS",
            f"{count} external citation(s); intent={intent} (no minimum)",
        )
    ok = count >= minimum
    return CheckResult(
        "external_citations",
        "PASS" if ok else "FAIL",
        f"{count} external citation(s); intent={intent} (minimum {minimum})",
    )


def check_approved_customers(body: str) -> CheckResult:
    hits = WATCHED_UNAPPROVED.findall(body)
    unapproved = [h for h in hits if h not in APPROVED_CUSTOMERS]
    return CheckResult(
        "approved_customers_only",
        "PASS" if not unapproved else "FAIL",
        f"unapproved mentions: {sorted(set(unapproved))}" if unapproved else "0",
    )


def check_internal_links(body: str) -> CheckResult:
    """Warn (not fail) if the article has zero internal social.plus links.

    The internal-linking-strategist skill is supposed to add 0-3 links to
    related social.plus pages (/answers/, /glossary/, /use-cases/, etc.).
    A zero here usually means that step was skipped, not that no related
    page existed. Field testing showed this step gets dropped silently in
    parallel-subagent orchestration. Surfacing it as a WARN lets the
    parent session notice and backfill.
    """
    links = MARKDOWN_LINK_PATTERN.findall(body)
    internal = [u for _, u in links if "social.plus" in u]
    if internal:
        return CheckResult(
            "internal_links",
            "PASS",
            f"{len(internal)} internal social.plus link(s)",
        )
    return CheckResult(
        "internal_links",
        "WARN",
        "0 internal social.plus links — did internal-linking-strategist run? "
        "Zero is legitimate only if no related social.plus page exists for this topic.",
    )


def check_anchor_text_length(body: str, max_words: int = 8) -> CheckResult:
    """External link anchors must be <= max_words words.

    Long anchor text wraps the claim instead of naming the source, which
    degrades LLM citation extraction and is treated as anchor-text spam by
    search engines. The claim belongs in the prose; the anchor is the source
    name (3-6 words target, 8 hard limit).
    """
    pattern = r'\[([^\]]+)\]\(https?://[^)]+\)'
    links = re.findall(pattern, body)
    too_long = [(a, len(a.split())) for a in links if len(a.split()) > max_words]
    if too_long:
        sample = "; ".join(f"({n}w) {a[:50]}..." for a, n in too_long[:3])
        return CheckResult(
            "anchor_text_length",
            "FAIL",
            f"{len(too_long)} anchor(s) exceed {max_words} words: {sample}",
        )
    return CheckResult(
        "anchor_text_length",
        "PASS",
        f"all {len(links)} link anchor(s) <= {max_words} words",
    )


def check_no_jsonld(body: str) -> CheckResult:
    """Webflow handles schema at the template level; the body should not emit
    JSON-LD. Catch the common fenced form.
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


# ---------- v2 checks ----------


def h2_sections(body: str) -> list[tuple[str, str]]:
    """(heading, section text) for each H2 in order."""
    parts = re.split(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def pitch_section(sections: list[tuple[str, str]]) -> tuple[str, str] | None:
    for h, t in sections:
        if "social.plus" in h.lower():
            return h, t
    return None


def check_question_headings(body: str) -> CheckResult:
    sections = h2_sections(body)
    pitch = pitch_section(sections)
    content = [h for h, _ in sections
               if not NON_QUESTION_SECTIONS.match(h) and (pitch is None or h != pitch[0])]
    if not content:
        return CheckResult("question_headings", "FAIL", "no content H2 sections found")
    q = [h for h in content if h.rstrip().endswith("?")]
    share = len(q) / len(content)
    ok = share >= QUESTION_HEADING_SHARE
    return CheckResult("question_headings", "PASS" if ok else "FAIL",
        f"{len(q)}/{len(content)} content H2s phrased as questions "
        f"(minimum {int(QUESTION_HEADING_SHARE * 100)}%). Use the Queue row's sub-questions.")


def check_has_table(body: str) -> CheckResult:
    ok = bool(re.search(r"^\s*\|.+\|\s*$", body, re.MULTILINE)) and bool(
        re.search(r"^\s*\|?\s*:?-{2,}", body, re.MULTILINE))
    return CheckResult("has_table", "PASS" if ok else "FAIL", "" if ok else "no markdown table found")


STAT_PATTERN = re.compile(
    r"\b\d+(?:\.\d+)?\s?%"
    r"|\b\d+(?:\.\d+)?\s?(?:-|to)\s?\d+(?:\.\d+)?\s?(?:%|x|weeks?|months?|days?|hours?)"
    r"|\b\d[\d,.]*\s?(?:M|K|B|million|billion|thousand)\+?(?![\w])"
    r"|\$\s?\d[\d,.]*",
    re.IGNORECASE,
)


def check_statistics(body: str) -> CheckResult:
    text = re.sub(r"\]\([^)]+\)", "]", body)
    hits = STAT_PATTERN.findall(text)
    ok = len(hits) >= MIN_STATISTICS
    return CheckResult("statistics_count", "PASS" if ok else "FAIL",
        f"{len(hits)} statistic(s) detected (minimum {MIN_STATISTICS}); each needs a source "
        "in messaging/evidence-bank.md or an external citation")


def check_boilerplate_headings(body: str) -> CheckResult:
    bad = [h for h, _ in h2_sections(body) if BOILERPLATE_HEADINGS.search(h)]
    return CheckResult("no_boilerplate_headings", "FAIL" if bad else "PASS",
        f"legacy boilerplate heading(s): {bad}" if bad else "")


def check_pitch(body: str) -> CheckResult:
    sections = h2_sections(body)
    pitches = [h for h, _ in sections if "social.plus" in h.lower()]
    if len(pitches) != 1:
        return CheckResult("pitch_section", "FAIL",
            f"expected exactly 1 H2 naming social.plus (the pitch), found {len(pitches)}")
    _, text = pitch_section(sections)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    wc = len(re.findall(r"\b[\w'-]+\b", plain))
    lo, hi = PITCH_RANGE
    return CheckResult("pitch_section", "PASS" if lo <= wc <= hi else "WARN",
        f"pitch = {wc} words (target {lo}-{hi})")


def check_promotion_clean(body: str) -> CheckResult:
    """The answer-first block, summary and FAQ answers are what AI engines
    extract. They must not mention social.plus: selling happens only in the
    pitch section. Google's spam policies (updated May 15, 2026) cover
    attempts to manipulate generative AI responses in Search."""
    pre = []
    for p in body.split("\n\n"):
        if p.strip().startswith("#"):
            break
        if p.strip():
            pre.append(p)
    faq = ""
    for h, t in h2_sections(body):
        if re.match(r"^(faqs?|frequently asked questions)$", h, re.IGNORECASE):
            faq = t
    where = []
    if "social.plus" in " ".join(pre[:2]).lower():
        where.append("answer-first block / summary")
    if "social.plus" in faq.lower():
        where.append("FAQs")
    return CheckResult("promotion_clean_extraction_blocks", "FAIL" if where else "PASS",
        f"social.plus mentioned in: {where}" if where else "")


def faq_questions(body: str) -> list[str]:
    for h, t in h2_sections(body):
        if re.match(r"^(faqs?|frequently asked questions)$", h, re.IGNORECASE):
            return [q.strip() for q in re.findall(r"^###\s+(.+?)\s*$", t, re.MULTILINE)]
    return []


def check_faq_count(body: str) -> CheckResult:
    n = len(faq_questions(body))
    lo, hi = FAQ_RANGE
    return CheckResult("faq_count", "PASS" if lo <= n <= hi else "WARN",
        f"{n} FAQ(s) as H3 questions (target {lo}-{hi})")


def check_faq_overlap(body: str, queue: Path | None, own_id: str) -> CheckResult:
    """An FAQ that fully answers another Queue row's question cannibalises
    that page. Link to it instead."""
    if queue is None:
        return CheckResult("faq_queue_overlap", "WARN", "skipped: pass --queue <Queue CSV> to check")
    try:
        root = Path(__file__).resolve().parents[4] / "scripts"
        sys.path.insert(0, str(root))
        from intent_match import load_queue, score, LIKELY_DUPLICATE  # type: ignore
        rows = load_queue(queue)
    except Exception as e:  # noqa: BLE001
        return CheckResult("faq_queue_overlap", "WARN", f"skipped: {e}")
    clashes = []
    for fq in faq_questions(body):
        for r in rows:
            if r["id"] == own_id or r["status"].lower() in {"rejected", "merged", "scheduled for removal"}:
                continue
            if score(fq, "", r["question"], "") >= LIKELY_DUPLICATE:
                clashes.append(f"'{fq}' ~ {r['id']}")
    return CheckResult("faq_queue_overlap", "FAIL" if clashes else "PASS",
        ("FAQ duplicates another row's question, replace it with a link: " + "; ".join(clashes)) if clashes else "")


def check_conclusion(body: str) -> CheckResult:
    for h, t in h2_sections(body):
        if re.match(r"^conclusion$", h, re.IGNORECASE):
            if re.match(r"\s*in conclusion", t, re.IGNORECASE):
                return CheckResult("conclusion", "FAIL", "conclusion opens with 'In conclusion'")
            return CheckResult("conclusion", "PASS", "")
    return CheckResult("conclusion", "FAIL", "no '## Conclusion' section")


# Price-like figures (team decision, 19 Aug 2026: no specific prices on any page; describe the pricing model).
# A currency amount followed by a billing unit, or introduced by price wording. Cited cost statistics
# ("an average breach costs $4.44M") do not match.
PRICE_FIGURE = re.compile(
    r"(?:[$\u20ac\u00a3]\s?\d[\d,.]*\s?(?:k|K|M)?\s*(?:/|per|a|an)\s*(?:MAU|month|mo|user|seat|year|yr|license|licence)\b)"
    r"|(?:\b(?:starting at|starts at|priced at|pricing (?:is|starts at|from)|plans? (?:start|begin) at)\s+[$\u20ac\u00a3]\s?\d)",
    re.IGNORECASE)


def check_price_figures(text: str) -> CheckResult:
    hits = [m.group(0) for m in PRICE_FIGURE.finditer(text)]
    return CheckResult("no_price_figures", "PASS" if not hits else "WARN",
        "" if not hits else f"price-like figure(s): {hits[:3]}; describe the pricing model instead")


def check_editor_line(text: str) -> CheckResult:
    ok = "Editor (named human reviewer):" in text
    return CheckResult("editor_line_present", "PASS" if ok else "FAIL",
        "" if ok else "missing 'Editor (named human reviewer): [fill before publish]' line")


# ---------- runner ----------


def run(path: Path, intent_override: str | None, lo: int | None, hi: int | None,
        queue: Path | None = None) -> Report:
    report = Report()
    text = path.read_text(encoding="utf-8-sig")  # -sig strips a leading BOM
    meta, body = parse_metadata(text)

    intent = intent_override or meta.get("intent", "")
    if intent not in VALID_INTENTS:
        intent = "how-to"  # best-effort default for checks that need one

    if lo is None or hi is None:
        lo_default, hi_default = INTENT_WORD_RANGE.get(intent, (700, 1500))
        lo = lo if lo is not None else lo_default
        hi = hi if hi is not None else hi_default

    # The check_headings check needs the full document (to count the single H1
    # that was consumed by parse_metadata). Reconstruct a pseudo-body with the
    # H1 re-inserted for that one check.
    body_with_h1 = f"# {meta.get('title', '')}\n\n{body}" if meta.get("title") else body

    report.results.extend(check_metadata(meta))
    report.results.append(check_meta_description(meta))
    report.results.append(check_word_count(body, lo, hi))
    report.results.append(check_answer_first(body))
    report.results.append(check_summary_word_count(body))
    report.results.append(check_keyword_in_sentence_1(meta, body))
    report.results.append(check_filler_opener(body))
    report.results.append(check_em_dashes(body))
    report.results.append(check_emojis(body))
    report.results.append(check_forbidden_terms(body))
    report.results.append(check_risky_terms(body))
    report.results.append(check_html_tags(body))
    report.results.append(check_no_jsonld(body))
    report.results.extend(check_headings(body_with_h1))
    report.results.append(check_citations(body, intent))
    report.results.append(check_internal_links(body))
    report.results.append(check_anchor_text_length(body))
    report.results.append(check_approved_customers(body))
    report.results.append(check_question_headings(body))
    report.results.append(check_has_table(body))
    report.results.append(check_statistics(body))
    report.results.append(check_boilerplate_headings(body))
    report.results.append(check_pitch(body))
    report.results.append(check_promotion_clean(body))
    report.results.append(check_faq_count(body))
    report.results.append(check_faq_overlap(body, queue, meta.get("queueId", "")))
    report.results.append(check_conclusion(body))
    report.results.append(check_price_figures(body))
    report.results.append(check_editor_line(text))

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="AEO article compliance checker")
    parser.add_argument("path", type=Path, help="Path to the article markdown file")
    parser.add_argument(
        "--intent",
        choices=sorted(VALID_INTENTS),
        help="Override intent from metadata",
    )
    parser.add_argument("--min", type=int, help="Override minimum word count")
    parser.add_argument("--max", type=int, help="Override maximum word count")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    parser.add_argument("--queue", type=Path, help="Content Queue exported as CSV (enables the FAQ overlap check)")
    args = parser.parse_args()

    if not args.path.exists():
        print(f"file not found: {args.path}", file=sys.stderr)
        return 2

    report = run(args.path, args.intent, args.min, args.max, args.queue)

    if args.json:
        print(report.as_json())
    else:
        print(f"AEO compliance report for {args.path}\n")
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
