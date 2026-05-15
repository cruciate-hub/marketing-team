# Anti-patterns and Self-Review Checklist

This is the file the skill consults before declaring a release ready for .docx generation. Every drafted release runs against this list. If any check fails, fix and re-review.

---

## Section 1 — Banned words and phrases

### Hyperbole adjectives (banned globally)
| Banned | Why | Use instead |
|---|---|---|
| world-class | Empty superlative; the reader provides the judgment | Specifics: "used by X customers", "deployed across N apps" |
| best-in-class | Same | Same — specifics |
| industry-leading | Unprovable in a single line | "the [specific market] leader in [specific niche]" with proof |
| cutting-edge | Vintage tech-marketing language | Just describe the capability |
| next-generation | Marketing filler | If it's the next generation of *something specific*, say what |
| revolutionary | Almost never accurate | Describe the change in concrete terms |
| game-changing | Cliché | "shifts the economics", "removes the trade-off", "changes how X is done" |
| seamless | Means nothing | "without leaving the app", "in one click", "without setup" |
| robust | Empty | Numbers, uptime, scale figures |
| innovative | Self-applied; never lands | Show, don't tell |
| transformative | Adjective doing the work that verbs should do | Name the transformation |
| disruptive | Marketing trope | Name what's being disrupted and how |
| synergy / synergies | Banned without exception | Specific outcomes for each party |
| holistic | Vague | Name the components |
| paradigm shift | Cringe | Name the shift |
| solution | Sometimes ok, often filler | "platform", "service", or the named product |
| empower / empowers | Marketing verb | "lets", "gives", "enables" — or be specific |
| unlock / unleash | Overused | "makes possible", "enables", "removes the barrier" |
| ecosystem | Use sparingly; often filler | "platform", "network", "marketplace", "developer community" — specifically what |
| leverage (as a verb) | Banned | "use" |
| utilize | Banned | "use" |
| best-of-breed | Banned | Specifics |
| mission-critical | Cliché | "operational", "production", or describe the stakes |
| at scale | Often filler | Specify the scale |
| frictionless | Empty | What friction is removed |
| turnkey | Vintage marketing | "ready to use", "available today" |

### Banned opening phrases (release-level, paragraph-level, quote-level)
- "We are excited to announce..."
- "We are pleased to announce..."
- "We are thrilled to..."
- "Today marks..."
- "In an industry where..."
- "In today's fast-paced [anything]..."
- "As we continue to..."
- "It is our pleasure to..."
- "We are honored..."
- "Looking ahead..."

The lede starts with the city and date. The release announces things, not feelings.

### Banned quote anti-patterns
See `quote-engineering.md` for the six quote-specific anti-patterns. Briefly:
1. The summary quote (restates the lede)
2. The gratitude quote ("honored to work with...")
3. The adjective stack
4. The "as we" quote
5. The wrong-vantage-point quote (CEO talking architecture)
6. The strawman swipe at unnamed competitors

### Banned framing tropes
- "Imagine a world where..." (no)
- "What if..." (no)
- "It's no secret that..." (no)
- "Studies have shown..." without a citation (no)
- "Did you know..." (no)
- "Picture this:" (no)

---

## Section 2 — Structural anti-patterns

### The buried lede
**Anti-pattern:** The actual news appears in paragraph 2 or 3. The lede is industry context or a generic statement.

**Example (bad):**
> LONDON, April 29, 2026 — Community has become the most powerful force in modern brand building. Today, more than ever, customers expect to engage with brands in deeper ways. To meet this demand, social.plus today launched Commerce, a new suite that brings product discovery into community moments.

**Fix:**
> LONDON, April 29, 2026 — social.plus today launched Commerce, a suite of capabilities that connects high-intent community moments to the products users can act on, without leaving the app.

The first sentence carries the news. Period.

### The Russian-doll subheads
**Anti-pattern:** Section subheads that work only after reading the previous subhead. The release reads like a deck.

**Fix:** Each subhead is independently scannable. A reader who skims only the subheads should get the gist.

### The list lede
**Anti-pattern:** First paragraph is a bullet list. Bullet lists never appear in the body of a press release.

**Fix:** Prose paragraphs. If the announcement has multiple parts, the lede names the umbrella and the body explains each part in its own paragraph.

### The everything release
**Anti-pattern:** One release announces two unrelated things ("we raised $30M and launched a new product").

**Fix:** Split into two releases. If timing forces both, lead with the bigger news and treat the smaller as a body paragraph.

### The unnamed customer release
**Anti-pattern:** "A leading global retailer chose social.plus to..." without naming the retailer.

**Fix:** If the customer can't be named, this isn't a customer-win release — it's a product or milestone release. Rewrite around what *can* be named.

### The vague availability
**Anti-pattern:** "Available soon" or "coming later this year" with no specific date.

**Fix:** A date, a month, or a quarter. If none is decided, the release isn't ready.

---

## Section 3 — Voice and AP style

### Voice rules

- **Active voice** in the lede, always: "social.plus today launched" — not "Commerce was launched today by social.plus"
- **Present or past tense.** No future tense in the lede ("will launch tomorrow" — pick today's date and say "today launched", or change the dateline)
- **Specific nouns.** "Commerce" not "the new product". Name the thing.
- **No first person.** No "our customers" in body paragraphs (it's allowed in quotes). Body says "social.plus customers" or names specific customers.
- **No marketing intensifiers.** "Very", "really", "extremely", "incredibly" — all banned in the body. (Quotes can have them sparingly if the speaker actually talks that way.)

### AP style (newswire requires this)

| Item | Rule | Example |
|---|---|---|
| Dates | Month spelled out, day in numeral, comma, year | April 29, 2026 (not 29 April 2026 or 29/04/26) |
| State abbreviations | AP abbreviations, not USPS | "Calif." not "CA" (in datelines; in body, AP allows "California" spelled out) |
| Numbers | Spell out one through nine; numerals for 10+ | "nine customers", "47 customers" |
| Numbers (exceptions) | Numerals for percentages, money, dates, ages, measurements | "5 percent" or "5%" (5% acceptable on the wire), "$30 million", "10-year-old" |
| Time | Lowercase a.m./p.m. with periods, no leading zero | "9 a.m. ET" |
| Titles | Capitalize before a name, lowercase after | "VP of Marketing Amadeus Norén" / "Amadeus Norén, VP of Marketing" |
| Quotation marks | Curly quotes in the .docx output | "" not "" |
| Em dash | Em-dash with no spaces (AP) OR with spaces (house style) — pick one and be consistent. House style: with spaces. | " — " |
| Headlines | Sentence case for the subhead; title-case-with-sentence-case-after-colon for the headline | See structure-template.md |
| Oxford comma | No Oxford comma in headlines | "Brands, creators and customers" not "Brands, creators, and customers" in headlines. Body may use Oxford comma if the brand style guide does. |

---

## Section 4 — Mandatory self-review checklist

Before the .docx is generated, run this checklist in order. If any item fails, fix and re-check.

### Headline + subhead
- ⬜ Headline is 8–14 words, 70–110 characters
- ⬜ Headline uses the colon construction OR a strong subject-verb-object pattern
- ⬜ Headline names the specific thing (product name, dollar amount, customer name)
- ⬜ No banned adjectives in the headline
- ⬜ Subhead is one sentence, 14–25 words
- ⬜ Subhead does not restate the headline — it explains the *so what*

### Lede paragraph
- ⬜ Lede answers Who/What/When/Where in the first sentence
- ⬜ Active voice
- ⬜ "social.plus, [descriptor], [verb] [news]" pattern is intact
- ⬜ No banned opening phrase
- ⬜ 35–60 words total
- ⬜ Dateline format correct: `CITY, Month DD, YYYY — `

### Body paragraphs
- ⬜ Problem/category framing comes before product detail
- ⬜ No buried lede (the news is in the first sentence, not paragraph 3)
- ⬜ Section subheads are sentence case, declarative
- ⬜ Each paragraph 50–100 words (lede can be shorter)
- ⬜ No bullet lists in the prose (bullets only acceptable in "use of funds" or "what's included" if explicitly chosen)

### Quotes
- ⬜ Executive quote passes the four-rule test (lift / delete / human / category)
- ⬜ Executive quote is 35–65 words, 1–2 sentences
- ⬜ Executive quote attribution: "[Name], [Title]" on a separate line
- ⬜ Customer/partner quote is verbatim from the brief
- ⬜ No banned quote anti-patterns

### Availability + boilerplate
- ⬜ Availability block names specific date or quarter
- ⬜ Availability block names how to get the product (Console / contact sales / URL)
- ⬜ "About social.plus" boilerplate is verbatim from `boilerplates.md`
- ⬜ Media Contact block has email and URL

### Format
- ⬜ FOR IMMEDIATE RELEASE (or embargo line) at the top
- ⬜ `###` end marker on its own line at the bottom
- ⬜ No emojis
- ⬜ No URLs in the body except documentation/contact-sales links and the social.plus domain
- ⬜ No images embedded in the .docx (newswires accept images separately)
- ⬜ Total word count is within the target range for the release type (see structure-template.md)

### Compliance
- ⬜ Brand compliance check from `brain.md` has been run
- ⬜ All product names use exact official capitalization (social.plus, Commerce, etc.)
- ⬜ Tagline included only in boilerplate, not in body
- ⬜ No competitor names unless brief explicitly requires them
- ⬜ No metric or customer claim that isn't in the brief

---

## Section 5 — When in doubt

Ask:
- Would I quote this in an article?
- Does the speaker sound like the role they hold?
- If I cut this paragraph, does the release get worse or just shorter?
- Is the customer in the brief actually approved for naming?
- Is the number in the brief actually defensible if a journalist asks for the methodology?

If the answer to any of these is uncertain, surface it to the user before generating the .docx.
