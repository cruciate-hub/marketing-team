# Install — press-release skill

## What this is

A Claude Code skill that produces newswire-ready press releases as `.docx` files, written to the standard of a world-class B2B tech PR firm. Designed for the social.plus marketing plugin.

## Folder structure

```
press-release/
├── SKILL.md                              # Main entry point — Claude reads this first
├── INSTALL.md                            # This file
├── references/
│   ├── structure-template.md             # 12-block skeleton, block-by-block spec
│   ├── release-type-playbooks.md         # Lede formulas per release type
│   ├── brief-template.md                 # Canonical brief shape + 4 worked examples
│   ├── quote-engineering.md              # 4-rule quote test + drafting patterns
│   ├── anti-patterns.md                  # Banned words/phrases + self-review checklist
│   └── best-in-class-corpus.md           # Patterns from Stripe / Datadog / Snowflake / etc.
├── examples/
│   └── commerce-launch.md                # Gold-standard social.plus release (Commerce, Apr 29 2026)
└── scripts/
    ├── generate_press_release.py         # python-docx generator
    └── example_payload_commerce.json     # Reference payload (the Commerce release in JSON)
```

## To install in the social.plus marketing plugin

1. Copy the entire `press-release/` folder into your plugin's `skills/` directory:
   ```
   <social.plus-marketing-plugin>/skills/press-release/
   ```

2. The plugin's manifest will pick up the skill automatically — no manifest edit needed unless the plugin requires explicit registration. Check the plugin's existing skills (`newsletters`, `case-study`, etc.) for how skills are declared.

3. Verify `python-docx` is available in any environment where the skill runs:
   ```bash
   python3 -c "import docx" || pip install --break-system-packages python-docx
   ```

## How to use

Send Claude a brief that includes (at minimum) these three fields:
- The announcement and its key facts
- The target audience and angle
- Customer/partner quote(s) verbatim (if applicable to the release type)

See `references/brief-template.md` for the full canonical brief shape with worked examples for product launches, funding rounds, customer wins, and exec hires.

Claude will:
1. Fetch the social.plus brand brain from GitHub for tone and terminology
2. Load the local references in this skill
3. Read the Commerce gold-standard example
4. Ask clarifying questions if anything in the brief is missing or vague
5. Determine the release type and apply the right lede formula
6. Draft the release
7. Self-review against the anti-patterns checklist
8. Generate a properly formatted `.docx`
9. Run the brand compliance check
10. Deliver the file with a one-line summary and any flags

## Output

Every release ships as a `.docx` named:
```
press-release-<short-slug>-<YYYY-MM-DD>.docx
```

Format inside:
- `FOR IMMEDIATE RELEASE` (or embargo line) at top
- Bold 18pt headline
- Italic 12pt grey subhead
- Bold dateline + plain lede in one paragraph
- Bold sentence-case section subheads
- Lead-phrase-bolded detail paragraphs (Cloudflare style)
- Indented italic-attributed quote blocks with curly quotes
- About boilerplate (pulled from `boilerplates.md` unless overridden)
- Media Contact block
- Centered `###` end marker

Ready to upload to PR Newswire (Cision) or hand to any agency.

## Test it

A sample brief in JSON and the resulting .docx are bundled:

```bash
python3 scripts/generate_press_release.py \
  --input scripts/example_payload_commerce.json \
  --output /tmp/test-release.docx
```

Open the result in Word — it should match the social.plus Commerce launch press release exactly.
