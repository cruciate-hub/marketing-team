# Formatting research behind this skill

Source pages checked directly: appsflyer.com/glossary/active-users, adjust.com/glossary/active-user, and the current live social.plus/glossary/active-user, all fetched during skill design.

## What appsflyer.com and adjust.com do that this skill copies

- **Answer-first opening.** Both lead with a direct one- or two-sentence definition before any framing or context. AppsFlyer's is a bolded, standalone line above the first heading.
- **A visible "what's inside" outline** at the top (AppsFlyer only) — not required here since Webflow's page chrome handles in-page navigation, but it confirms both sites treat the section order as fixed and scannable, not freeform.
- **A dedicated metrics/variants breakdown**, usually as a bulleted or tabular list of the term's measurement windows or sub-types (AppsFlyer: DAU/WAU/MAU as bullets; this skill upgrades that to a table, since tables are the more AI-extractable structure).
- **A worked numeric example** immediately after the metric breakdown (AppsFlyer's DAU/MAU stickiness math). This is the single most concrete, most citable paragraph on either reference page.
- **A product tie-in section** near the end (Adjust: "Active users and Adjust"), kept short and grounded rather than promotional.
- **A closing recap** (AppsFlyer's "Key takeaways" bullets).
- **Consistent structure across the entire glossary**, not just consistent within one entry — this is what lets AI engines learn the extraction pattern for the whole collection rather than re-parsing each page from scratch.

## What the current social.plus glossary does that this skill exists to stop

Directly quoted from the live `/glossary/active-user` page at the time of this research:

- Opens with "In the realm of digital platforms and applications, understanding the concept of an 'active user' is pivotal for product managers..." — scene-setting instead of an answer, and contains the forbidden word "pivotal."
- Describes the product tie-in as something that "can be a game-changer for businesses using Social+'s suite of social features" — a hard-blocked filler phrase, and the section is generically promotional rather than grounded in a specific product capability.
- No table anywhere on the page.
- No "Related Terms" section — a missed internal-linking opportunity the strategy calls out explicitly.
- Headings follow a "deep dive" essay structure ("Introduction to X," "Understanding X: A deep dive") rather than a fixed, scannable template.

## Why tables specifically

The user's own framing of this skill's goal — "things AI likes, like tables" — matches the general finding across AEO/GEO research already cited in `aeo-content`'s SKILL.md: structured, self-contained blocks (tables, numbered lists) are lifted and cited by AI answer engines more reliably than equivalent prose. For a glossary entry specifically, a table is also usually the *natural* format for the content anyway (measurement windows, term variants, comparison of related concepts) — so the requirement isn't a stylistic overlay, it fits the material.
