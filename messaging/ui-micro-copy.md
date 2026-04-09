# social.plus Copy Conventions

> **Precedence note:** For UI copy tasks, the voice and style rules in this file override the general `tone.md` rules. `tone.md` governs marketing and external content; this file governs product UI. `terminology.md` still applies everywhere — it is never overridden.

UI copy is part of the design. Every label, error message, button, tooltip, and placeholder is a moment where the brand either reinforces trust or erodes it.

---

## Voice

social.plus copy is **direct, confident, and human**. It never talks down to users, never over-explains, and never hides behind jargon.

| Principle | In practice |
|-----------|-------------|
| **Direct** | Say what something does. Skip the preamble. |
| **Confident** | No hedging. "Start building" not "You can start building if you'd like." |
| **Human** | Write like a sharp colleague, not a legal document or a startup cliché. |
| **Specific** | Name the action. "Delete community" not "Confirm action." |
| **Respectful** | Never blame the user. Errors are system failures, not user failures. |

---

## Tone by context

| Context | Tone |
|---------|------|
| Marketing / hero copy | Bold, energetic, aspirational — short sentences, active voice |
| Product UI | Clear and functional — users are working, don't interrupt them |
| Errors | Calm and helpful — explain what happened, offer a path forward |
| Empty states | Encouraging — invite action, don't just say "Nothing here" |
| Onboarding | Warm and direct — set up the user for success quickly |
| Docs / help | Precise and scannable — headers, short paragraphs, examples |

---

## UI Microcopy

### Buttons and CTAs

- Use **verb + noun** for clarity: "Create community", "Export report", "Invite member"
- Primary CTA in a section: action-oriented and specific — "Start building free", "Get started"
- Avoid: "Submit", "Click here", "OK", "Yes" — too generic, no meaning without context
- Destructive actions: name the thing being destroyed — "Delete community" not "Delete"
- Confirmation dialogs: repeat the action in the confirm button — if the dialog says "Delete this channel?", the button says "Delete channel"

### Labels

- Sentence case for all labels: "Email address" not "Email Address"
- No full stops on labels
- Keep labels short — one to three words where possible
- Avoid abbreviations unless universally understood (e.g. "API" is fine, "Msg" is not)

### Placeholders

- Placeholder text is supplementary, never a substitute for a label
- Use realistic examples: `you@company.com`, `Acme Inc.`, `My community`
- Do not repeat the label in the placeholder: if the label is "Email address", the placeholder can be `name@work.com` — not "Enter your email address"

### Error messages

- Explain what went wrong in plain language
- Tell the user what to do next
- Never blame: "That email is already in use" not "You entered a duplicate email"
- Never be vague: "Something went wrong" is only acceptable as a fallback when the error is genuinely unknown — always add "Try again or contact support" as a next step

| ❌ Avoid | ✅ Use instead |
|---------|--------------|
| "Invalid input" | "Enter a valid email address" |
| "Error 403" | "You don't have permission to do this" |
| "Something went wrong" | "We couldn't save your changes. Try again or contact support." |
| "Required field" | "Email address is required" |

### Helper / hint text

- Use to clarify format, constraints, or context: "Must be at least 8 characters"
- Do not restate the label: if the label is "Password", the hint adds new information
- Keep under 10 words where possible

### Empty states

- Name what's missing and invite the first action
- "No members yet — invite your team to get started"
- Never just: "No results" or "Nothing here"

### Loading and progress

- Be specific when possible: "Saving changes…", "Loading members…"
- Generic fallback: "Loading…" (not "Please wait…" — users know to wait)
- For long operations: show progress and give context — "Importing 2,400 members…"

---

## Capitalisation

| Element | Rule | Example |
|---------|------|---------|
| Page titles | Title case | "Community Settings" |
| Section headings (h2, h3) | Sentence case | "Everything you need to build community" |
| Buttons | Sentence case | "Start building free" |
| Labels | Sentence case | "Email address" |
| Navigation items | Title case | "Who We Serve" |
| Error messages | Sentence case | "Enter a valid email address" |
| All-caps labels (badges, tags) | Allowed at ≤ 12px, letter-spacing ≥ 0.08em | "ENTERPRISE" |

---

## Numbers and formatting

- Use numerals for all numbers in UI copy: "3 members", "10,000 communities", not "three members"
- Large numbers: use commas as thousands separator — `10,000` not `10000`
- Abbreviate at scale in display contexts: `1B+`, `60+`, `10K` — always with a `+` if the value is a minimum
- Percentages: numeral + % with no space — `20%` not `20 %`
- Dates: `20 March 2026` in full, `20 Mar` in compact UI, never `03/20/26` (ambiguous)

---

## Punctuation

- No full stops at the end of labels, button text, or headings
- Full stops in body copy, helper text, and error messages that are full sentences
- Do not use em dashes. Use a full stop, comma, or semicolon instead
- Ellipsis `…` for truncation and loading states — use the unicode character `…`, not three dots `...`
- Apostrophes: use curly quotes `'` not straight `'`
- Quotation marks: use curly `"` not straight `"`

---

## What to avoid

- **Jargon and buzzwords:** "synergy", "leverage", "seamless", "robust", "next-generation", "cutting-edge", "unlock"
- **Filler phrases:** "In order to", "Please note that", "It is important that"
- **Passive voice** in UI: "Your changes were saved" → "Changes saved"
- **Exclamation marks** in product UI: reserve for genuine moments of celebration (onboarding completion, first community created). Never in errors, never in routine confirmations.
- **Gendered language:** use "they/them" as default singular pronoun
