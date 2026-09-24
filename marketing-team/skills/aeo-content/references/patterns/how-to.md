# Template: how-to

**Use for:** "How do you [do X]?" questions where the reader wants to carry out a task. Examples: "How do you add in-app chat to a Flutter app?", "How do you launch an in-app community with no existing activity?"

**Citations:** none required. How-to pages earn trust through specific, correct product detail: real SDK names, real setup steps, real timelines. External links only where they genuinely support a claim.

**Unique information:** at least one product fact from `messaging/evidence-bank.md` (Product facts) or social.plus documentation, checked on the day of writing. Platform-specific pages (Flutter, React Native, iOS, Android, web) must contain setup steps and code that genuinely differ from their siblings; if they don't, they should be one page.

## Typical sections (order and wording come from the Queue row)

- **What do you need before you start?** Short list: accounts, keys, design decisions, platform versions.
- **The steps.** One H2 per phase, phrased as a question ("How do you set up user identity?"), or one H2 "What are the steps?" with a numbered list. Each step opens with a verb. Consistent level of detail: don't mix "install the SDK" with "design your governance model".
- **Table options:** approaches and trade-offs (build yourself / SDK / UI kit: effort, control, time to launch, when it fits), or a checklist table (step, owner, typical time).
- **What usually goes wrong?** 3-5 real pitfalls, each with the fix.
- **How do you know it worked?** The metric or check that confirms success.

## Rules

- The trade-off table describes each approach honestly. The row that matches social.plus's category is not written to "win"; say plainly when building in-house or another approach is the better fit.
- Timelines are ranges ("2-4 weeks"), never "quickly".
- Don't invent step counts. If the real procedure has 6 steps, write 6.
