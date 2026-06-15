# blog-seo-content compliance regression tests

Fixtures that exercise the behaviours an audit pass uncovered. Each fixture isolates one targeted behaviour; `run_tests.py` enforces the expected outcome per fixture.

Run with:

```bash
python3 tests/run_tests.py
```

Exit 0 if every fixture behaves as documented; exit 1 with a per-fixture diff on any drift.

## Fixtures

| Fixture | Asserts | Origin |
|---|---|---|
| `F1-code-heading.md` | `# headings` inside fenced code blocks do NOT count toward `single_h1` / heading-skip | audit pass 2 |
| `F2-h1-h3-house-style.md` | H1→H3 (the dominant live-blog pattern — 19% of posts) WARNs, does not FAIL | live data (`pages-blog.json`) |
| `F4-emoji-gaps.md` | `⏰ ℹ ▶` (U+23F0, U+2139, U+25B6) trigger `no_emojis` | audit pass 2 |
| `F5-autolink.md` | CommonMark autolinks `<https://…>` do NOT trigger `no_html` | audit pass 2 |
| `F6-smart-apostrophe.md` | curly `’` in body vs straight `'` in title does not false-fail the keyword check | audit pass 2 |
| `F7-alt-violations.md` | em-dash + forbidden terms in `Alt text:` field FAIL the gate | audit pass 2 |
| `F8-cp1252.md` | Word-paste (cp1252-encoded em-dash 0x97) is detected via fallback decoder, no crash | audit pass 2 |
| `F9-bold-filler.md` | filler opener wrapped in `**` markdown emphasis still matches | audit pass 2 |
| `F10-reading-time.md` | claimed `Minutes to read` vs computed word count (~250 wpm) WARNs when off by >1 | audit pass 2 |
| `F11-high-leverage.md` | hyphenated "higher-leverage" (strategy English) does NOT trigger the leverage rule | audit pass 2 |

## Adding a fixture

1. Drop a `.md` file in `fixtures/` named `F<NN>-<short-name>.md`.
2. Add an entry to `EXPECTATIONS` in `run_tests.py` declaring `must_fail`, `must_warn`, `must_pass`, `must_not_fail`, and (optional) `exit_code`.
3. Run `python3 tests/run_tests.py` — your new fixture must pass.

Each fixture should isolate **one** targeted assertion. Incidental violations elsewhere in the fixture are tolerated as long as the runner asserts only on the targeted check name.

## What the suite does not cover

- Tone, factual accuracy, citation quality — owned by `brain.md` + LLM judgment, not the script.
- Live-Webflow CMS schema drift — checked manually against `pages-blog.json`.
- Internal-linking-strategist behaviour — separate skill, has its own validation surface.
