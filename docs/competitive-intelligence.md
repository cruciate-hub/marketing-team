# Competitive Intelligence

Claude skill for role-tailored competitive briefings at social.plus. Maintained by Bam.

This is the **read layer** of a two-skill system: it queries two knowledge-layer documents and formats what it finds into a briefing tuned to the stakeholder's role. The **write layer** (`/competitive-intel`, which researches competitors and refreshes the knowledge layers monthly) is private and not part of this plugin.

## What it does

- Asks two intake questions (your role, your focus today) and nothing else before delivering.
- Reads both knowledge-layer docs fresh from Google Drive at the start of every session, checking the `Last full refresh` date and warning when data is older than 45 days.
- Delivers a three-part brief: what changed recently, what matters for your role (Sales, Marketing, Product, Growth, Leadership, Engineering), and suggested follow-ups.
- Answers ad-hoc follow-up questions from the knowledge layers first, with light supplementary research (WebSearch, Ahrefs, npm) only when the layers fall short.
- Logs unanswerable questions as data gaps so the next monthly refresh picks them up.

## When it triggers

"competitive briefing", "what's new with competitors", "how do we compare to [competitor]", "battle card for [competitor]", "competitive positioning", "brief me on competitors".

Not for refreshing or maintaining the intel itself — that's the private `/competitive-intel` skill's job. If data is wrong or missing, flag it to Bam.

## Data access

All competitor facts, figures, and findings live in two private Google Docs in a restricted Drive folder — none of it is in this repo. Using the skill requires:

- The Google Drive MCP connected in your Claude environment.
- Access to the knowledge-layer docs (`competitive-intel.md` and `competitive-marketing-intel.md`) — request it from Bam.

Without access, the skill stops and tells you who to ask; it does not substitute external research for the knowledge layers.

[SKILL.md →](../marketing-team/skills/competitive-intelligence/SKILL.md)
