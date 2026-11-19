# Brief template for a subagent build

About 40% of the corrections in the 19 Nov 2026 pricing build came from subagent work that skipped the gates. A subagent knows only its brief, so copy this, fill the brackets, and keep the gates in it word for word.

```
You are building [section(s)] of [page] on the social.plus Webflow site (site 66e2765d540e1939a89db4bb),
from the Claude Design board [artifact URL], version [version id]. Target page: [page id / slug], staging only.

Load the skill `claude-design-to-webflow` first and follow its five gates. Webflow is king: the site's
components, class chains and variables win over the board; never change a Webflow variable or shared class
to match the board.

Board sections you own and their Webflow mapping (from the Map step):
- [board section] → [component or existing section] · class chain [exact chain] · embeds [none / which]
- …

Do not:
- create a class, variable or component without asking me first (say which and why);
- edit a shared class or component without listing every page it reaches;
- publish to anything but staging;
- report "done" without the check output.

Report back with:
1. what you built (element ids), each embed and what it styles, each new class and why;
2. the `check-board.mjs` report (path to report.md) and every FAIL left with its reason;
3. the "Webflow won" list (where the build differs from the board because Webflow wins);
4. what you could not verify.
```

Then check the subagent's work yourself before reporting it (its report is not proof): open the check report, look at the side-by-side images.
