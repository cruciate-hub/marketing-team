#!/usr/bin/env python3
"""Regression tests for the webflow-publisher shared scripts (repo-root scripts/).

Covers, without touching any API:
  * the blog adapter (gdoc_to_fielddata.py) still produces what the pre-refactor script
    produced for a Google Doc listicle export (legacy golden fixture), modulo the documented
    deltas (docs/webflow-publisher-design.md: internal links without target="_blank", and
    since 2026-10-01 the table standard and the FAQPage embed, items 8 and 9);
  * the common intermediate (blog-seo-content / glossary-content `.draft.md` shape)
    converts correctly for the blog and glossary field maps;
  * the generalized dry-run catches a flattened table and a raw (non-embedded) table under
    headings that contain neither "At-a-Glance" nor "Comparison" (the bug this refactor fixes);
  * the glossary path is blocked, loudly, while its field slugs are unconfirmed;
  * the old positional CLIs (blog-publisher.py, resize_blog_images.py) still work;
  * the content-engine rules (2026-09-29 to 10-01): the table standard, FAQPage schema,
    live images/videos carried over on a rewrite, rewrite dates, and slug numbers.

Stdlib only. Image-dimension assertions run only when Pillow is importable (the engine
itself skips dimension checks without Pillow and says so).

Usage:
    python3 marketing-team/skills/webflow-publisher/tests/run_tests.py
Exit 0 when every test passes; exit 1 with details on any failure.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SCRIPTS = REPO / "scripts"
FIX = HERE / "fixtures"
DATE = "2026-01-01T00:00:00.000Z"

try:
    from PIL import Image
    PILLOW = True
except ImportError:
    PILLOW = False

TESTS = []


def test(fn):
    TESTS.append(fn)
    return fn


def run(*cmd, cwd=None):
    return subprocess.run([sys.executable, *map(str, cmd)], capture_output=True, text=True, cwd=cwd)


def load(path):
    return json.load(open(path))


def report_checks(tmp) -> dict:
    """{check name: passed} from the dry-run-report.json written next to the fielddata."""
    rep = load(Path(tmp) / "dry-run-report.json")
    return {c["check"]: c["passed"] for c in rep["checks"]}


def normalize_legacy_links(html: str) -> str:
    """The ONE documented delta vs. the pre-refactor converter: internal (social.plus /
    relative) links no longer get target="_blank". Strip it from the legacy golden."""
    return re.sub(r'(<a href="(?:/|https?://(?:www\.)?social\.plus)[^"]*")\s+target="_blank"', r"\1", html)


def to_legacy_shape(html: str) -> str:
    """Deltas 8 and 9 in docs/webflow-publisher-design.md (2026-10-01): tables now use the table
    standard (scroll wrapper, margin-bottom:0, hidden caption, scope="col"/"row" header cells)
    and a post with an FAQ section ends with a FAQPage JSON-LD embed. Map new output back to the
    legacy shape so the golden parity test keeps checking everything else."""
    html = re.sub(r'<div style="overflow-x:auto[^"]*">(<table)', r"\1", html)
    html = html.replace("</table></div></div>", "</table></div>")
    html = html.replace('<table style="margin-bottom:0 !important">', "<table>")
    html = re.sub(r"<caption[^>]*>.*?</caption>", "", html)
    html = html.replace('<th scope="col">', "<th>")
    html = re.sub(r'<th scope="row" style="[^"]*">(.*?)</th>', r"<td>\1</td>", html)
    return re.sub(r"""<div data-rt-embed-type='true'><script type="application/ld\+json">.*?</script></div>""", "", html)


def publisher_module():
    """Import scripts/webflow-publisher.py (hyphenated name) for its pure helpers."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("webflow_publisher", SCRIPTS / "webflow-publisher.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def make_webp(path: Path, size):
    if PILLOW:
        Image.new("RGB", size, (40, 90, 200)).save(path, "WEBP", quality=80)
    else:
        path.write_bytes(b"RIFF....WEBPVP8 ")  # placeholder; dims are skipped without Pillow


def hero_set(tmp: Path, slug="post"):
    """Three exact-size hero files + two inline files, named like resize_images.py does."""
    files = {
        "header": tmp / f"{slug}_page-header_1578x888.webp",
        "grid":   tmp / f"{slug}_thumbnail_724x408.webp",
        "menu":   tmp / f"{slug}_mega-menu_502x283.webp",
    }
    make_webp(files["header"], (1578, 888))
    make_webp(files["grid"], (724, 408))
    make_webp(files["menu"], (502, 283))
    inline = [tmp / f"{slug}_img-1_1578x888.webp", tmp / f"{slug}_img-2_1578x888.webp"]
    for p in inline:
        make_webp(p, (1578, 888))
    return files, inline


# ── Field maps ──────────────────────────────────────────────────────────────────

@test
def field_maps_load_and_report_readiness():
    sys.path.insert(0, str(SCRIPTS))
    import webflow_fieldmap as wf
    names = wf.list_collections()
    assert {"blog", "glossary", "answers"} <= set(names), names
    blog = wf.load_field_map("blog")
    assert wf.unconfirmed_slugs(blog) == {"required": [], "optional": []}
    assert blog["fields"]["body"] == "post-content" and blog["collection_id"] == "66e2765d540e1939a89db6a4"
    assert blog["taxonomies"]["categories"]["Community"] == "66e2765d540e1939a89dc049"
    # glossary: confirmed 2026-09-18 (sync_fieldmap.py against the live schema) — ready, not a stub.
    glossary = wf.load_field_map("glossary")
    assert wf.unconfirmed_slugs(glossary) == {"required": [], "optional": []}
    assert glossary["fields"]["body"] == "glossary" and glossary["collection_id"] == "66e2765d540e1939a89db93e"
    assert glossary["fields"]["title"] == "name" and glossary["fields"]["slug"] == "slug"
    # answers: confirmed 2026-10-01 against the live schema (7 fields).
    answers = wf.load_field_map("answers")
    assert wf.unconfirmed_slugs(answers) == {"required": [], "optional": []}
    assert answers["fields"]["body"] == "content" and answers["fields"]["title"] == "name"
    assert answers["metadata"]["Meta title"]["slug"] == "meta-title" and answers["faq_schema"] is True
    assert answers["images"][0]["slug"] == "image-2" and answers["images"][0]["optional"] is True
    # the blog map carries the rewrite date field and the FAQ schema switch; glossary has neither
    assert blog["fields"]["date_edited"] == "date-edited-manual" and blog["faq_schema"] is True
    assert not glossary.get("faq_schema"), "the glossary template already emits FAQPage"
    p = run(SCRIPTS / "webflow-publisher.py", "--list-collections")
    assert p.returncode == 0 and all(n in p.stdout for n in ("blog", "glossary", "answers")), p.stdout + p.stderr
    assert "UNCONFIRMED" not in p.stdout, p.stdout


# ── Blog adapter: legacy parity ─────────────────────────────────────────────────

@test
def gdoc_adapter_matches_legacy_golden_listicle_1():
    with tempfile.TemporaryDirectory() as tmp:
        out, md = Path(tmp) / "fd.json", Path(tmp) / "l1.md"
        p = run(SCRIPTS / "gdoc_to_fielddata.py", FIX / "gdoc-listicle.txt", "1",
                "--out", out, "--date", DATE, "--emit-intermediate", md)
        assert p.returncode == 0, p.stderr
        new, legacy = load(out), load(FIX / "gdoc-listicle.expected-legacy.json")
        legacy["post-content"] = normalize_legacy_links(legacy["post-content"])
        pc = new["post-content"]
        new["post-content"] = to_legacy_shape(pc)
        diff = {k for k in set(new) | set(legacy) if new.get(k) != legacy.get(k)}
        assert not diff, f"fields differ from the pre-refactor script: {sorted(diff)}"
        # The Embed-wrapped table (now in the standard shape) and the H3 platform entries survived.
        assert "<div data-rt-embed-type='true'><div style=\"overflow-x:auto" in pc
        assert '<table style="margin-bottom:0 !important"><caption' in pc
        assert pc.count("</h3>__INLINE_IMG_") == 2
        assert "OPTIONAL DISCLOSURE" not in pc and "OUTREACH" not in pc
        assert new["slug"] == "best-in-app-community-platforms-for-consumer-apps"
        assert new["image-alt-text"] == "Six in-app community platform logos arranged on a dark grid"
        # The emitted intermediate is the common contract.
        text = md.read_text()
        assert text.startswith("# 6 Best In-App Community Platforms")
        for needle in ("Category: Community, Engagement, Retention", "Tags: Community",
                       "## At-a-Glance Comparison", "### social.plus: Best for", "__INLINE_IMG_1__"):
            assert needle in text, needle


@test
def gdoc_adapter_listicle_2_and_slug_override_rules():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "fd.json"
        p = run(SCRIPTS / "gdoc_to_fielddata.py", FIX / "gdoc-listicle.txt", "2", "--out", out, "--date", DATE)
        assert p.returncode == 0, p.stderr
        new, legacy = load(out), load(FIX / "gdoc-listicle-2.expected-legacy.json")
        legacy["post-content"] = normalize_legacy_links(legacy["post-content"])
        new["post-content"] = to_legacy_shape(new["post-content"])
        assert new == legacy
        # NON-NEGOTIABLE: a --slug override is still stripped of year + leading count.
        p = run(SCRIPTS / "gdoc_to_fielddata.py", FIX / "gdoc-listicle.txt", "2", "--out", out,
                "--date", DATE, "--slug", "7-best-chat-sdks-2027")
        assert p.returncode == 0, p.stderr
        assert load(out)["slug"] == "best-chat-sdks", load(out)["slug"]
        assert "contained a year" in p.stderr and "began with a count" in p.stderr


# ── Common intermediate: blog-seo-content shape ─────────────────────────────────

@test
def blog_draft_shape_converts_with_generic_rules():
    with tempfile.TemporaryDirectory() as tmp:
        out, rep = Path(tmp) / "fd.json", Path(tmp) / "rep.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-draft.draft.md", "--collection", "blog",
                "--out", out, "--date", DATE, "--report", rep)
        assert p.returncode == 0, p.stderr
        fd, report = load(out), load(rep)
        assert fd["name"] == "How to Choose a Community SDK for Your Mobile App in 2026"
        assert fd["slug"] == "how-to-choose-a-community-sdk-for-your-mobile-app", fd["slug"]   # year stripped from Slug:
        assert fd["post-summary"].startswith("Choosing a community SDK for your mobile app comes down")
        pc = fd["post-content"]
        assert pc.startswith("<h2>What a community SDK covers</h2>"), pc[:80]           # intro lifted out
        assert '<a href="https://www.social.plus/social/sdk">social.plus community SDK docs</a>' in pc  # internal: same tab
        assert '<a href="https://getstream.io/" target="_blank">Stream</a>' in pc                       # external: new tab
        assert pc.count("__INLINE_IMG_") == 2 and "__INLINE_IMG_2__" in pc                # ![alt](…) → placeholders
        assert "<h3>Integration effort</h3>" in pc
        assert ("<ul><li>Single-SDK approach<ul><li>Fewer moving parts</li><li>One vendor data model</li></ul></li>"
                "<li>Multi-vendor approach</li></ul>") in pc                                # nested bullets
        assert "<ol><li>Pick the surface you need first</li><li>Run a two-week pilot</li>" in pc  # numbered list
        assert ("<div data-rt-embed-type='true'><div style=\"overflow-x:auto;-webkit-overflow-scrolling:touch;"
                "margin-bottom:2rem\"><table style=\"margin-bottom:0 !important\"><caption") in pc  # indented table, standard shape
        assert '<thead><tr><th scope="col">Option</th>' in pc
        assert "<blockquote><p>Ship the smallest social surface" in pc
        assert "<p>---</p>" not in pc
        assert fd["category"] == "66e2765d540e1939a89dc049"                              # Community
        assert fd["category-multi-reference-3"] == ["66e2765d540e1939a89dc049", "66e2765d540e1939a89dc04b"]
        assert fd["min-read"] == "6" and fd["date-published"] == DATE and fd["featured"] is False
        assert report["tables"] == 1 and report["placeholders"] == 2
        assert report["unmapped_labels"] == ["Focus keyword"]
        assert "__unconfirmed__" not in fd
    # --html-only needs no field map
    p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-draft.draft.md", "--html-only")
    assert p.returncode == 0 and "<h2>What a community SDK covers</h2>" in p.stdout, p.stderr


# ── Glossary path ───────────────────────────────────────────────────────────────

@test
def glossary_draft_converts_but_is_blocked_while_slugs_unconfirmed():
    # Uses a dedicated always-unconfirmed fixture, not --collection glossary: the real
    # glossary-content/webflow-fields.json is expected to become confirmed over time (it
    # already is, as of 2026-09-18), and this test must keep exercising the "blocked while
    # unconfirmed" path regardless of that map's real-world state.
    unconfirmed_map = FIX / "glossary-test-fieldmap-unconfirmed.json"
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "fd.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "glossary-entry.draft.md",
                "--field-map", unconfirmed_map, "--out", out)
        assert p.returncode == 0, p.stderr
        fd = load(out)
        assert fd["name"] == "Active User" and fd["slug"] == "active-user"
        parked = fd["__unconfirmed__"]
        assert "body" in parked and "Meta description" in parked and "Category" in parked, sorted(parked)
        body = parked["body"]
        assert body.startswith("<p>An active user is any person"), body[:60]              # definition stays in body
        assert "<div data-rt-embed-type='true'><div style=\"overflow-x:auto" in body       # metrics table embedded
        assert '<thead><tr><th scope="col">Metric</th>' in body
        assert "<h3>" not in body
        assert re.findall(r"<h2>(.*?)</h2>", body)[-1] == "Related Terms"
        assert body.count('<a href="https://www.social.plus/glossary/') == 3               # Related Terms, same tab
        # dry-run fails loudly on the unconfirmed map, but the structural checks still run on the parked body
        p = run(SCRIPTS / "webflow-publisher.py", out, "--field-map", unconfirmed_map,
                "--source", FIX / "glossary-entry.draft.md", "--dry-run")
        assert p.returncode == 1, p.stderr
        chk = report_checks(tmp)
        assert chk["fieldmap:required-slugs-confirmed"] is False
        assert chk["content:no-unconfirmed-values"] is False
        assert chk["content:table-not-flattened"] is True and chk["content:table-in-embed"] is True
        assert chk["content:has-internal-links"] is True
        assert "CONFIRM" in p.stderr.upper() or "unconfirmed" in p.stderr
        # a real publish attempt is refused before any token is needed
        p = run(SCRIPTS / "webflow-publisher.py", out, "--field-map", unconfirmed_map)
        assert p.returncode == 1 and "unconfirmed" in p.stderr, p.stderr


@test
def glossary_path_passes_dry_run_with_a_confirmed_test_map():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "fd.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "glossary-entry.draft.md",
                "--field-map", FIX / "glossary-test-fieldmap.json", "--out", out)
        assert p.returncode == 0, p.stderr
        fd = load(out)
        assert "__unconfirmed__" not in fd
        assert fd["test-only-category"] == "test-only-engagement-id"
        assert fd["test-only-meta-description"].startswith("An active user is a person")
        p = run(SCRIPTS / "webflow-publisher.py", out, "--field-map", FIX / "glossary-test-fieldmap.json",
                "--source", FIX / "glossary-entry.draft.md", "--dry-run")
        assert p.returncode == 0, p.stderr
        assert json.loads(p.stdout.strip().splitlines()[-1])["allPassed"] is True
        # Rewrite mode (the glossary's common case) dry-runs the same payload without images…
        p = run(SCRIPTS / "webflow-publisher.py", out, "--field-map", FIX / "glossary-test-fieldmap.json",
                "--replace", "abc123", "--source", FIX / "glossary-entry.draft.md", "--dry-run")
        assert p.returncode == 0 and "Would replace" in p.stderr, p.stderr
        # …and a real --replace stops at the token gate (no network), after the map checks.
        env_free = subprocess.run([sys.executable, str(SCRIPTS / "webflow-publisher.py"), str(out),
                                   "--field-map", str(FIX / "glossary-test-fieldmap.json"), "--replace", "abc123"],
                                  capture_output=True, text=True, env={k: v for k, v in __import__("os").environ.items()
                                                                        if k != "WEBFLOW_API_TOKEN"})
        assert env_free.returncode == 1 and "WEBFLOW_API_TOKEN is not set" in env_free.stderr, env_free.stderr
        p = run(SCRIPTS / "webflow-publisher.py", out, "--field-map", FIX / "glossary-test-fieldmap.json",
                "--replace", "abc123", "--staged")
        assert p.returncode == 1 and "--replace cannot be combined with --staged" in p.stderr


# ── The table bug ───────────────────────────────────────────────────────────────

@test
def dry_run_catches_flattened_table_under_any_heading():
    with tempfile.TemporaryDirectory() as tmp:
        fd_path = Path(tmp) / "fd.json"
        fd = load(FIX / "dryrun-flattened-table.json")
        fd.pop("_doc", None)
        assert "At-a-Glance" not in fd["test-only-body"] and "Comparison" not in fd["test-only-body"]
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json", "--dry-run")
        assert p.returncode == 1, p.stderr
        chk = report_checks(tmp)
        assert chk["content:table-not-flattened"] is False, chk
        assert "collapsed into prose" in p.stderr
        # Source-vs-output layer: a draft with one table but a body with no <table> at all.
        fd["test-only-body"] = re.sub(r"<p>\| Metric.*?</p>", "<p>See the table.</p>", fd["test-only-body"])
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json",
                "--source", FIX / "glossary-entry.draft.md", "--dry-run")
        assert p.returncode == 1, p.stderr
        assert report_checks(tmp)["content:table-not-flattened"] is False
        assert "source has 1 table block(s) but body has 0" in p.stderr, p.stderr


@test
def dry_run_catches_raw_table_not_in_embed():
    with tempfile.TemporaryDirectory() as tmp:
        fd_path = Path(tmp) / "fd.json"
        fd = load(FIX / "dryrun-raw-table.json")
        fd.pop("_doc", None)
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json", "--dry-run")
        assert p.returncode == 1, p.stderr
        chk = report_checks(tmp)
        assert chk["content:table-not-flattened"] is True
        assert chk["content:table-in-embed"] is False, chk
        # Wrapping it in the Embed fixes that check, but the table standard still fails…
        raw_body = fd["test-only-body"]
        fd["test-only-body"] = raw_body.replace("<table>", "<div data-rt-embed-type='true'><table>") \
                                       .replace("</table>", "</table></div>")
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json", "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["content:table-in-embed"] is True
        assert report_checks(tmp)["content:table-standard"] is False and "scroll wrapper" in p.stderr, p.stderr
        # …until the table has the standard shape (scroll wrapper, margin-bottom:0, caption).
        fd["test-only-body"] = raw_body.replace(
            "<table>", "<div data-rt-embed-type='true'><div style=\"overflow-x:auto;-webkit-overflow-scrolling:touch;"
                       "margin-bottom:2rem\"><table style=\"margin-bottom:0 !important\"><caption>Metrics</caption>") \
            .replace("</table>", "</table></div></div>")
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json", "--dry-run")
        assert p.returncode == 0, p.stderr


# ── Content-engine rules (2026-09-29 to 10-01) ──────────────────────────────────

@test
def table_standard_caption_comes_from_the_heading():
    p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--html-only")
    assert p.returncode == 0, p.stderr
    html = p.stdout
    assert ('<caption style="position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;'
            'clip:rect(0,0,0,0);white-space:nowrap;border:0">Feeds and groups</caption>') in html, html[:400]
    assert ('<tr><th scope="row" style="background:transparent !important">Activity feed</th>'
            "<td>Shows new posts</td>") in html
    assert html.count('<th scope="col">') == 3 and html.count("</table></div></div>") == 1


@test
def faq_schema_for_blog_and_answers_but_not_glossary():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        for name, expect in (("blog", True), ("answers", True), ("glossary", False)):
            out = tmp / f"{name}.json"
            p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--collection", name,
                    "--out", out, "--keep-slug")
            assert p.returncode == 0, p.stderr
            fd = load(out)
            body = fd[{"blog": "post-content", "answers": "content", "glossary": "glossary"}[name]]
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', body, re.S)
            assert bool(blocks) is expect, (name, blocks)
            if expect:
                assert body.endswith("</script></div>"), "the FAQPage embed goes at the very end"
                data = json.loads(blocks[0])
                assert data["@type"] == "FAQPage" and len(data["mainEntity"]) == 2
                q1, q2 = data["mainEntity"]
                assert q1["name"] == "What is the most important community feature?"
                assert q1["acceptedAnswer"]["text"] == ("An activity feed, because it gives members a reason to "
                                                        "return every day. See feeds.")      # plain text, links dropped
                assert q2["acceptedAnswer"]["text"] == ("Start with a feed and groups. Add moderation before you "
                                                        "open to the public.")              # list items joined
        # answers: meta-title defaults to the title (live items use the H1 title)
        assert load(tmp / "answers.json")["meta-title"] == "15 Must-Have Community Features for Any App"
        # the dry-run accepts the JSON-LD embed and the carried-over video iframe, and checks the schema
        p = run(SCRIPTS / "webflow-publisher.py", tmp / "blog.json", "--collection", "blog", "--replace", "abc123",
                "--source", FIX / "blog-rewrite.draft.md", "--dry-run")
        chk = report_checks(tmp)
        assert chk["content:no-script-or-iframe"] is True and chk["content:faq-schema"] is True, chk
        assert p.returncode == 0, p.stderr
        # a FAQ section whose schema went missing is caught
        fd = load(tmp / "blog.json")
        fd["post-content"] = re.sub(r"<div data-rt-embed-type='true'><script.*?</script></div>", "", fd["post-content"])
        (tmp / "blog.json").write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", tmp / "blog.json", "--collection", "blog", "--replace", "abc123", "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["content:faq-schema"] is False


@test
def rewrite_keeps_slug_and_carries_live_figures():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out, rep_path = tmp / "fd.json", tmp / "rep.json"
        # without --keep-slug the blog rules strip the leading count (new-post behaviour)…
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--collection", "blog", "--out", out)
        assert p.returncode == 0 and load(out)["slug"] == "must-have-community-features-for-any-app"
        # …with --keep-slug the live URL stays exactly as it is
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--collection", "blog", "--out", out,
                "--keep-slug", "--report", rep_path)
        assert p.returncode == 0, p.stderr
        fd, report = load(out), load(rep_path)
        assert fd["slug"] == "15-must-have-community-features-for-any-app"
        assert report["figures"] == 2 and report["faq_questions"] == 2
        pc = fd["post-content"]
        assert '<img alt="Feed example" src="https://cdn.example.test/live-feed.webp" loading="lazy">' in pc
        assert '<iframe src="https://www.youtube.com/embed/test123"' in pc
        # in rewrite mode the slug-shape rules are informational; the number matches the title
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "blog", "--replace", "abc123", "--dry-run")
        chk = report_checks(tmp)
        assert chk["slug:no-leading-count"] is True and chk["slug:number-matches-title"] is True, chk
        assert p.returncode == 0, p.stderr
        # the guard that runs before any PATCH: a live image missing from the new body is reported
        wp = publisher_module()
        live_body = pc + ('<figure class="w-richtext-figure-type-image" data-rt-type="image"><div>'
                          '<img src="https://cdn.example.test/old-chart.webp"></div></figure>')
        assert wp.missing_live_figures(live_body, pc) == ["https://cdn.example.test/old-chart.webp"]
        assert wp.missing_live_figures(pc, pc) == []
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "blog", "--replace", "abc123",
                "--allow-image-removal", "--dry-run")
        assert p.returncode == 0, p.stderr


@test
def rewrite_dates_keep_published_and_set_edited():
    wp = publisher_module()
    blog = __import__("webflow_fieldmap").load_field_map("blog")
    now = "2026-10-01T10:00:00.000Z"
    fd = {"date-published": now, "name": "x"}
    notes = wp.apply_rewrite_dates(blog, {"date-published": "2024-09-12T00:00:00.000Z"}, "2024-09-10T00:00:00.000Z", fd, now)
    assert "date-published" not in fd, "a rewrite never overwrites the original publish date"
    assert fd["date-edited-manual"] == now and len(notes) == 2
    fd = {"date-published": now}
    wp.apply_rewrite_dates(blog, {}, "2024-09-10T00:00:00.000Z", fd, now)
    assert fd["date-published"] == "2024-09-10T00:00:00.000Z", "empty publish date is filled from createdOn"
    glossary = __import__("webflow_fieldmap").load_field_map("glossary")
    fd = {"name": "x"}
    assert wp.apply_rewrite_dates(glossary, {}, "2024-09-10T00:00:00.000Z", fd, now) == [] and fd == {"name": "x"}


@test
def slug_number_must_match_the_title():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = tmp / "fd.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--collection", "blog", "--out", out,
                "--keep-slug", "--slug", "4-strategies-to-ensure-mobile-app-user-retention")
        assert p.returncode == 0, p.stderr
        fd = load(out)
        fd["name"] = "5 Strategies to Ensure Mobile App User Retention"         # the title's count changed
        out.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "blog", "--replace", "abc123", "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["slug:number-matches-title"] is False, p.stderr
        assert "add a 301" in p.stderr
        wp = publisher_module()
        assert wp.slug_numbers("only-3-and-a-half-procent-of-followers") == ["3"]
        assert wp.title_numbers("Only 3.5% of Followers See Your Posts (2026)") == {"3", "5", "35"}   # year ignored
        assert wp.slug_numbers("best-chat-apis-2026") == []


def write_draft(tmp: Path, name: str, body: str, title="Test Page", extra="") -> Path:
    path = tmp / name
    path.write_text(f"# {title}\n\nMeta description: A short test description.\nCategory: Community\n"
                    f"Tags: Community\n{extra}\nOpening paragraph for the summary.\n\n{body}\n")
    return path


@test
def faq_extraction_skips_non_prose_and_dry_run_agrees_on_headings():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        body = ("## *FAQs*\n\n### What is a test?\n\nX is a thing.\n\n![diagram](x.png)\n\n__INLINE_IMG_1__\n\n"
                "```\ncode here\n```\n\n<figure data-rt-type=\"video\"><div><iframe src=\"https://www.youtube.com/embed/x\">"
                "</iframe></div>\n</figure>\n\n---\n\n## Conclusion\n\nDone.")
        draft = write_draft(tmp, "faq.md", body)
        out = tmp / "fd.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", draft, "--collection", "answers", "--out", out)
        assert p.returncode == 0, p.stderr
        fd = load(out)
        data = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', fd["content"], re.S).group(1))
        assert data["mainEntity"][0]["acceptedAnswer"]["text"] == "X is a thing.", data
        # italic FAQ heading: the dry-run finds the section the converter used (no false fail)
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "answers", "--dry-run")
        assert report_checks(tmp)["content:faq-schema"] is True, p.stderr
        # an FAQ section whose questions are not H3 headings fails with a useful message
        draft2 = write_draft(tmp, "faq2.md", "## FAQs\n\n**What is a test?** X is a thing.\n\n## Conclusion\n\nDone.")
        p = run(SCRIPTS / "md_to_webflow_html.py", draft2, "--collection", "answers", "--out", out)
        assert p.returncode == 0 and "no FAQPage schema added" in p.stderr, p.stderr
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "answers", "--dry-run")
        assert p.returncode == 1 and "### Question?" in p.stderr, p.stderr


@test
def figure_blocks_must_be_closed_and_keep_their_spacing():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        bad = write_draft(tmp, "bad.md", '## A\n\n<figure class="x"><div><img src="https://cdn.example.test/a.webp">\n\n## B\n\nText.')
        p = run(SCRIPTS / "md_to_webflow_html.py", bad, "--collection", "answers", "--out", tmp / "fd.json")
        assert p.returncode == 1 and "no closing </figure>" in p.stderr, p.stderr
        p = run(SCRIPTS / "md_to_webflow_html.py", bad, "--html-only")
        assert p.returncode == 1 and "no closing </figure>" in p.stderr, p.stderr
        ok = write_draft(tmp, "ok.md", '## A\n\n<figure class="x"\ndata-rt-type="image"><div><img alt="Feed\nexample" '
                                       'src="https://cdn.example.test/a.webp"></div></figure>\n\n## B\n\nText.')
        p = run(SCRIPTS / "md_to_webflow_html.py", ok, "--html-only")
        assert p.returncode == 0 and 'class="x" data-rt-type="image"' in p.stdout and 'alt="Feed example"' in p.stdout, p.stdout
        # the dry-run catches a broken figure in a hand-built body
        fd = {"name": "T", "slug": "t", "content": "<p>x</p><figure><div><img src=\"a\"></div>", "meta-description": "d"}
        (tmp / "h.json").write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", tmp / "h.json", "--collection", "answers", "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["content:figures-closed"] is False


@test
def script_exceptions_are_narrow():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        base = {"name": "T", "slug": "t", "meta-description": "d"}
        cases = {
            "smuggled second script": "<div data-rt-embed-type='true'><script type=\"application/ld+json\">{\"@type\":\"FAQPage\"}</script><script>alert(1)</script></div>",
            "non-FAQPage JSON-LD": "<div data-rt-embed-type='true'><script type=\"application/ld+json\">{\"@type\":\"Product\"}</script></div>",
            "script inside a video figure": "<figure data-rt-type=\"video\"><div><iframe src=\"https://x\"></iframe><script>x()</script></div></figure>",
        }
        for name, html in cases.items():
            (tmp / "h.json").write_text(json.dumps({**base, "content": "<p>x</p>" + html}))
            run(SCRIPTS / "webflow-publisher.py", tmp / "h.json", "--collection", "answers", "--dry-run")
            assert report_checks(tmp)["content:no-script-or-iframe"] is False, name
        # --allow-image-removal only means something on a rewrite
        p = run(SCRIPTS / "webflow-publisher.py", tmp / "h.json", "--collection", "answers", "--allow-image-removal", "--dry-run")
        assert p.returncode == 1 and "only applies to --replace" in p.stderr


@test
def slug_numbers_accept_derived_slugs_and_catch_stale_years():
    sys.path.insert(0, str(SCRIPTS))
    import md_to_webflow_html as conv
    wp = publisher_module()
    for title in ("Why only 3.5% of followers see your posts", "How to reach 1,000 users",
                  "Why 24/7 moderation matters", "What is a Web 3.0 community?", "How to add 1:1 chat to an app"):
        slug = conv.derive_slug(title, {"strip_years": True})
        assert all(n in wp.title_numbers(title) for n in wp.slug_numbers(slug)), (title, slug)
    assert wp.stale_slug_years("top-5-social-sdks-for-2025-and-how-to-choose-one", "Top 5 Social SDKs for 2026") == ["2025"]
    assert wp.stale_slug_years("social-sdks-2026", "Best Social SDKs (2026)") == []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        out = tmp / "fd.json"
        p = run(SCRIPTS / "md_to_webflow_html.py", FIX / "blog-rewrite.draft.md", "--collection", "blog", "--out", out,
                "--keep-slug", "--slug", "top-5-social-sdks-for-2025-and-how-to-choose-one")
        fd = load(out); fd["name"] = "Top 5 Social SDKs for 2026 and How to Choose One"; out.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", out, "--collection", "blog", "--replace", "abc123", "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["slug:number-matches-title"] is False, p.stderr


@test
def replace_end_to_end_with_a_mocked_api():
    import contextlib, io
    wp = publisher_module()
    sys.path.insert(0, str(SCRIPTS))
    import webflow_fieldmap as wf
    blog = wf.load_field_map("blog")
    live_fig = ('<figure class="w-richtext-figure-type-image" data-rt-type="image"><div>'
                '<img src="https://cdn.example.test/live.png?a=1&amp;b=2"></div></figure>')
    live = {"slug": "post", "name": "Post", "post-content": "<p>Old.</p>" + live_fig,
            "date-published": "2021-02-18T05:12:03.721Z"}
    calls = []

    def fake_http(method, url, headers=None, json_body=None, raw_body=None, timeout=30):
        calls.append((method, url, json_body))
        if method == "GET" and "/items/" in url:
            return 200, json.dumps({"fieldData": live, "createdOn": "2021-02-18T05:12:03.721Z"})
        return 200, "{}"
    wp.http = fake_http

    def attempt(body, allow):
        calls.clear()
        fd = {"name": "Post", "slug": "post", "post-content": body, "date-published": "2026-10-01T00:00:00.000Z"}
        err = io.StringIO()
        with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
            try:
                wp.replace_item("token", blog, "abc123", fd, {}, [], allow_image_removal=allow)
                code = 0
            except SystemExit as e:
                code = e.code
        patch = next((c[2] for c in calls if c[0] == "PATCH"), None)
        return code, patch, err.getvalue()

    code, patch, err = attempt("<p>New.</p>", allow=False)
    assert code == 1 and patch is None and "drops 1 image" in err, err          # refused before any PATCH
    code, patch, _ = attempt("<p>New.</p>", allow=True)
    assert code == 0 and patch is not None                                        # reviewer removed it on purpose
    code, patch, _ = attempt("<p>New.</p>" + live_fig.replace("&amp;", "&"), allow=False)
    assert code == 0, "the same figure with & instead of &amp; is carried over"
    fields = patch["fieldData"]
    assert "date-published" not in fields and fields["date-edited-manual"].startswith("20")
    # answers: a custom live meta title survives a rewrite whose draft had no Meta title line
    answers = wf.load_field_map("answers")
    fd = {"name": "Q?", "slug": "q", "content": "<p>A.</p>", "meta-title": "Q?"}
    assert wp.keep_live_title_copies(answers, {"meta-title": "Custom title"}, fd) == ["meta-title"] and "meta-title" not in fd
    fd = {"name": "Q?", "slug": "q", "content": "<p>A.</p>", "meta-title": "Set by the draft"}
    assert wp.keep_live_title_copies(answers, {"meta-title": "Custom title"}, fd) == [] and fd["meta-title"] == "Set by the draft"


@test
def caption_is_not_double_escaped():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        d = write_draft(tmp, "c.md", "## AT&amp;T vs Stream\n\n| A | B |\n|---|---|\n| x | y |")
        p = run(SCRIPTS / "md_to_webflow_html.py", d, "--html-only")
        assert ">AT&amp;T vs Stream</caption>" in p.stdout, p.stdout


# ── Blog wrapper CLI + internal links ───────────────────────────────────────────

@test
def blog_wrapper_positional_cli_still_works_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        fd_path, md = tmp / "fd.json", tmp / "l1.md"
        p = run(SCRIPTS / "gdoc_to_fielddata.py", FIX / "gdoc-listicle.txt", "1", "--out", fd_path,
                "--date", DATE, "--emit-intermediate", md)
        assert p.returncode == 0, p.stderr
        # Phase 3: deterministic internal links (same-tab policy)
        links = tmp / "links.json"
        links.write_text(json.dumps([
            {"anchor": "moderation tooling", "url": "https://www.social.plus/moderation"},
            {"anchor": "community layer", "url": "/social", "insert_at": "Consumer apps that add a community layer",
             "rephrase": "Consumer apps that add a community layer"},
        ]))
        p = run(SCRIPTS / "apply_internal_links.py", fd_path, links, "--collection", "blog")
        assert p.returncode == 0, p.stderr
        summary = json.loads(p.stdout.strip().splitlines()[-1])
        assert "moderation tooling" in summary["applied"], summary
        pc = load(fd_path)["post-content"]
        assert '<a href="https://www.social.plus/moderation">moderation tooling</a>' in pc
        assert 'target="_blank">moderation tooling' not in pc
        # Phase 7: the old positional dry-run command, translated onto the engine
        heroes, inline = hero_set(tmp, "best-in-app-community-platforms-for-consumer-apps")
        p = run(SCRIPTS / "blog-publisher.py", fd_path, heroes["header"], heroes["grid"], heroes["menu"],
                *inline, "--dry-run", "--source", md)
        assert p.returncode == 0, p.stderr
        chk = report_checks(tmp)
        for name in ("content:table-not-flattened", "content:table-in-embed", "content:has-internal-links",
                     "content:placeholders-match-inline", "slug:no-year", "slug:no-leading-count",
                     "taxonomy:category-multi-reference-3-includes-category", "image:header:provided"):
            assert chk[name] is True, (name, chk)
        assert json.loads(p.stdout.strip().splitlines()[-1])["collection"] == "blog"
        # Placeholder/inline mismatch is still caught (one inline image dropped).
        p = run(SCRIPTS / "blog-publisher.py", fd_path, heroes["header"], heroes["grid"], heroes["menu"],
                inline[0], "--dry-run")
        assert p.returncode == 1 and report_checks(tmp)["content:placeholders-match-inline"] is False
        # --update dry-run (dimension-only)
        p = run(SCRIPTS / "blog-publisher.py", "--update", "abc123", heroes["header"], heroes["grid"], heroes["menu"], "--dry-run")
        assert p.returncode == 0, p.stderr
        assert json.loads(p.stdout.strip())["update"] is True
        if PILLOW:
            bad = tmp / "bad_page-header_1578x888.webp"
            make_webp(bad, (1500, 888))
            p = run(SCRIPTS / "blog-publisher.py", fd_path, bad, heroes["grid"], heroes["menu"], *inline, "--dry-run")
            assert p.returncode == 1 and "expected 1578x888" in p.stderr, p.stderr
            # unreadable file with Pillow present is a FAIL, not a silent skip
            garbage = tmp / "garbage_page-header_1578x888.webp"
            garbage.write_bytes(b"not an image")
            p = run(SCRIPTS / "blog-publisher.py", fd_path, garbage, heroes["grid"], heroes["menu"], *inline, "--dry-run")
            assert p.returncode == 1 and "unreadable image" in p.stderr, p.stderr


@test
def resize_wrapper_emits_exact_blog_sizes():
    if not PILLOW:
        print("    (skipped: Pillow not installed)")
        return
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        master, inline = tmp / "master.png", tmp / "img-1.png"
        Image.new("RGB", (1920, 1080), (10, 20, 30)).save(master)
        Image.new("RGB", (3156, 1776), (30, 20, 10)).save(inline)
        p = run(SCRIPTS / "resize_blog_images.py", master, "my-post", tmp / "out", "--inline", inline)
        assert p.returncode == 0, p.stderr
        expected = {"my-post_page-header_1578x888.webp": (1578, 888), "my-post_thumbnail_724x408.webp": (724, 408),
                    "my-post_mega-menu_502x283.webp": (502, 283), "my-post_img-1_1578x888.webp": (1578, 888)}
        for name, size in expected.items():
            with Image.open(tmp / "out" / name) as im:
                assert im.size == size and im.format == "WEBP", (name, im.size, im.format)
        # a non-16:9 master is refused
        Image.new("RGB", (1600, 1600)).save(tmp / "square.png")
        p = run(SCRIPTS / "resize_images.py", tmp / "square.png", "x", tmp / "out2", "--collection", "blog")
        assert p.returncode == 1 and "distort" in p.stderr
        # a collection with no image fields refuses to resize
        p = run(SCRIPTS / "resize_images.py", master, "x", tmp / "out3", "--collection", "glossary")
        assert p.returncode == 1 and "no image fields" in p.stderr


def main() -> int:
    failures = []
    for fn in TESTS:
        try:
            fn()
            print(f"✓ {fn.__name__}")
        except Exception:  # noqa: BLE001 — report every failure, keep going
            failures.append(fn.__name__)
            print(f"❌ {fn.__name__}\n{traceback.format_exc()}")
    print()
    if failures:
        print(f"{len(failures)} test(s) failed: {failures}")
        return 1
    print(f"All {len(TESTS)} tests passed" + ("" if PILLOW else " (image-dimension assertions skipped: no Pillow)") + ".")
    return 0


if __name__ == "__main__":
    sys.exit(main())
