# FAQ Questions per Article

Approved articles: 3 · approved questions: 0 of 26

## Article 1 — What are in-app activity feeds?

Source: PAA for "activity feed", WebSearch results, LLM fallback

| # | Question | Source |
|---|---|---|
| 1 | What is an activity feed? | PAA |
| 2 | Do activity feeds require a social graph? | PAA |
| 3 | Can activity feeds be added to existing apps? | PAA |
| 4 | Is an activity feed suitable for a fitness app? | WebSearch |
| 5 | How long does it take to ship a feed? | PAA |
| 6 | How does moderation work in an activity feed? | PAA |
| 7 | What data does an activity feed capture? | LLM |
| 8 | How do you rank items in an activity feed? | WebSearch |

## Article 2 — How to add chat to a mobile app

Source: PAA for "add chat to mobile app", WebSearch results

| # | Question | Source |
|---|---|---|
| 1 | How long does it take to add chat to an app? | PAA |
| 2 | Do I need moderation from day one? | WebSearch |
| 3 | Can chat reuse my existing auth? | PAA |
| 4 | What does moderation load look like? | WebSearch |
| 5 | Can I start with one-to-one and add group chat later? | PAA |
| 6 | Does chat need its own notification service? | PAA |
| 7 | What chat SDK should I use? | PAA |
| 8 | How much does chat infrastructure cost? | LLM |
| 9 | Is chat GDPR compliant by default? | LLM |

## Article 3 — What is zero-party data?

Source: PAA for "zero-party data", WebSearch results

| # | Question | Source |
|---|---|---|
| 1 | What is zero-party data? | PAA |
| 2 | How is zero-party data different from first-party data? | PAA |
| 3 | Why does zero-party data matter? | PAA |
| 4 | How do you collect zero-party data? | WebSearch |
| 5 | Is zero-party data GDPR-safe? | PAA |
| 6 | What are examples of zero-party data? | PAA |
| 7 | How do brands use zero-party data for personalization? | WebSearch |
| 8 | Can I buy zero-party data? | LLM |
| 9 | How do community platforms capture zero-party data? | LLM |

## Notes

- LLM-sourced questions are candidate fillers when PAA/WebSearch returned fewer than 8 strong candidates. Prefer PAA/WebSearch when both are available.
- Article 3 question 8 ("Can I buy zero-party data?") is a common misconception; keep it if the colleague wants an explicitly corrective FAQ.

## Approval syntax

Per article, on its own line:
```
article 1: approve 1-4, drop 5, 7
article 2: approve 1, 3, 5; revise 2 — focus on operational load not policy
article 3: approve 1, 2, 4, 6
next
```

Final FAQ uses 4-6 of the approved questions per article. If more than 6 are approved, the draft phase picks the 6 strongest and lists the rest as "deferred" in the overview.
