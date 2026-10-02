# Type: listicle

**For:** honest lists and vendor comparisons: "Best chat SDKs for mobile apps", "Examples of apps with successful in-app communities", "social.plus vs [alternative]".

**Length:** 1,500-3,200 words. **Required:** a heading that states the evaluation criteria, a comparison table, and, whenever social.plus appears, a plain disclosure that it is our product (compliance FAILs otherwise).

## Why the extra rules

Self-published "best of" lists are often cited by AI engines, which then recommend someone else. Google's spam policies (updated May 15, 2026) cover attempts to manipulate generative AI responses, and reporting on the change names biased listicles. A list is only worth publishing if a neutral reader would find it fair.

## Structure

1. **Intro:** who the list is for and the decision it helps with.
2. **How we evaluated** (H2): the criteria, why they matter, and the disclosure.
3. **At a glance** (H2): comparison table, every entry scored on the same criteria.
4. **One H2 or H3 per entry:** what it is, best for, strengths, limits, pricing model (sourced), with a link to its own documentation or pricing page.
5. **How to choose** (H2): "choose X if..." decision rules.

## Rules

- **One list per category, not per vertical.** "Best community platforms for fitness / gaming / retail / consumer apps" is one list with vertical notes, unless each vertical genuinely has a different vendor set and different criteria. Undifferentiated vertical variants are BLOCK condition 6 and cannot be overridden.
- Competitor claims come from their own documentation or pricing pages. No characterisations you can't source.
- **Per product, not per vendor.** When a vendor sells several products, state each capability for the product that has it ("Chat and Video ship pre-built UI components; Activity Feeds does not"). Never write "each product ships X" or "UI component libraries for Chat, Feeds and Video" unless you checked each product's own docs. A vendor's SDK list is not proof of UI components.
- **UIKit is not UI Kit.** Follow `messaging/terminology.md`: UIKit (or "pre-built UI components") means code components inside an SDK; UI Kit means Figma or other design files. Vendors often call their Figma files a "UI kit", so check whether code components exist before writing either term, and don't present design files as code or code as design files only.
- **No speed or effort claims without a source**, for any vendor including social.plus: "reduces integration time", "speed of integration", "faster interface work" need a cited figure or come out. Describe what ships instead. `compliance.py` WARNs on these phrases (`no_unsourced_effort_claims`).
- social.plus is not placed first by default. If it ranks first, the stated criteria must show why.
- No year in the title unless someone owns a refresh; then add `Last updated:`.
