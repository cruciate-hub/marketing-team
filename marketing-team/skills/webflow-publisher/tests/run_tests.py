#!/usr/bin/env python3
"""Regression tests for the webflow-publisher shared scripts (repo-root scripts/).

Covers, without touching any API:
  * the blog adapter (gdoc_to_fielddata.py) still produces what the pre-refactor script
    produced for a Google Doc listicle export (legacy golden fixture), modulo the one
    documented delta (internal links no longer carry target="_blank");
  * the common intermediate (blog-seo-content / glossary-content `.draft.md` shape)
    converts correctly for the blog and glossary field maps;
  * the generalized dry-run catches a flattened table and a raw (non-embedded) table under
    headings that contain neither "At-a-Glance" nor "Comparison" (the bug this refactor fixes);
  * the glossary path is blocked, loudly, while its field slugs are unconfirmed;
  * the old positional CLIs (blog-publisher.py, resize_blog_images.py) still work.

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
    # answers: still an untouched stub.
    answers = wf.load_field_map("answers")
    unc = wf.unconfirmed_slugs(answers)
    assert "fields.body" in unc["required"], f"answers: body must be null until confirmed: {unc}"
    assert answers["fields"]["title"] == "name" and answers["fields"]["slug"] == "slug"
    p = run(SCRIPTS / "webflow-publisher.py", "--list-collections")
    assert p.returncode == 0 and "blog" in p.stdout and "glossary" in p.stdout and "UNCONFIRMED" in p.stdout, p.stdout + p.stderr


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
        diff = {k for k in set(new) | set(legacy) if new.get(k) != legacy.get(k)}
        assert not diff, f"fields differ from the pre-refactor script: {sorted(diff)}"
        # The Embed-wrapped table and the H3 platform entries survived the move.
        pc = new["post-content"]
        assert "<div data-rt-embed-type='true'><table><thead>" in pc
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
        assert "<div data-rt-embed-type='true'><table><thead><tr><th>Option</th>" in pc   # indented table still a table
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
        assert "<div data-rt-embed-type='true'><table><thead><tr><th>Metric</th>" in body  # metrics table embedded
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
        # Wrapping it fixes it.
        fd["test-only-body"] = fd["test-only-body"].replace("<table>", "<div data-rt-embed-type='true'><table>") \
                                                   .replace("</table>", "</table></div>")
        fd_path.write_text(json.dumps(fd))
        p = run(SCRIPTS / "webflow-publisher.py", fd_path, "--field-map", FIX / "glossary-test-fieldmap.json", "--dry-run")
        assert p.returncode == 0, p.stderr


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
