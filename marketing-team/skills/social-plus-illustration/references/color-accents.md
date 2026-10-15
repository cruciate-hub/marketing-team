# Accent colors

Every image still has **exactly one accent** — that is what keeps the style calm. What varies is *which* brand color that accent is, chosen by what the image is about. Ultramarine is primary: about **70% of images** (60–80% over any run of work) use it; the rest use one other brand color.

## The brand accents (dark-theme steps)

| Family | Fill (brand step) | Lines / text on dark | Glow (behind the accent) | Text on the fill |
|---|---|---|---|---|
| Ultramarine (primary) | blue-600 `#3B41EC` (gradient option `#45A5ED`→`#3B41EC`) | blue-400 `#6F89FC` | `rgba(59,65,236,0.42)` | white |
| Green | green-300 `#1DC497` | green-300 `#1DC497` / green-200 `#8DDFC0` | `rgba(29,196,151,0.30)` | `#111111` |
| Purple | purple-400 `#9F72FF` | purple-300 `#BDA7FC` | `rgba(159,114,255,0.35)` | `#111111` (white only ≥32px bold) |
| Pink | pink-300 `#F568F0` (brand step) | pink-300 `#F568F0` | `rgba(245,104,240,0.28)` | `#111111` |
| Orange | orange-400 `#FF6937` | orange-300 `#FCA58A` | `rgba(255,105,55,0.28)` | `#111111` (white only ≥32px bold) |
| Yellow | yellow-400 `#F7C506` | yellow-300 `#FDD76A` | `rgba(247,197,6,0.22)` | `#111111` |
| Red | red-400 `#FF305A` | red-300 `#FC9198` | `rgba(255,48,90,0.28)` | white only ≥32px bold, else `#111111` |

Fills use the brand step; text and thin lines in that color on the dark ground use the step shown (contrast). The glow always matches the accent; never leave an ultramarine glow under a non-blue accent. Icons sitting on a dark part of a filled shape stay light.

**Only ultramarine is ever an action.** In the design system every secondary color is "never a CTA". So a non-blue accent is a highlighted *thing* — a bar, a number, a ring, a badge, a line, a tag — never a button. If the image's focal element is a button, the accent is ultramarine.

## Choosing the accent — by meaning, not at random

| Accent | When the image is about… |
|---|---|
| **Ultramarine** (default) | product, social, engagement, community features — anything without a stronger fit |
| **Green** | growth and positive outcomes: revenue up, retention gains, conversion, money earned |
| **Purple** | AI, agents, automation, data and insights |
| **Pink** | creators, community moments, live and social energy (decoration and highlights only) |
| **Orange** | commerce and shopping, events |
| **Yellow** | rewards, gaming, highlights, badges, achievements |
| **Red** | only negative data or warnings — churn, a falling line, moderation flags. Never as a mood color. |

If two fit, prefer ultramarine. A topic fit is required to leave ultramarine — "for variety" alone is not a reason.

## Keeping the balance

- **Thumbnails**: the variety check reads the accents of the recent thumbnails too. Never two non-blue thumbnails in a row; at most 3 non-blue in the last 10. If the meaning points to a non-blue accent but the balance doesn't allow it, use ultramarine.
- **In-blog sets**: choose per chart by meaning; keep the set at ≥60% ultramarine. Neighbouring images in an article shouldn't both be non-blue.
- Never more than one accent family per image. **Exception (charts only):** when a chart compares two series that *both* matter, the second may use a second accent; baselines and "everything else" stay grey. Thumbnails are always single-accent.

## Worked example — "20 App monetization stats you should know"

Thumbnail: green (the post is about making money; recent thumbnails were all ultramarine). In-blog: img-4 yellow (the highlighted bar is gaming apps), img-5 green (subscription revenue +41%); img-1, 2, 3, 6, 7 ultramarine → 2 of 7 non-blue.
