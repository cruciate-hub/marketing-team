# Rich text (article body)

The rich-text styles as they are today: `.rich-text` (blog with `.c-blog`, glossary, tutorials, news, legal with `.c-legal`), `.answers_rich-text`, `.product-update_rich-text` (product updates, release notes) and the plain `.w-richtext`. Long bodies are trimmed in the preview to the first elements of each kind.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/styleguide (rich text samples) and live bodies from a blog post, a glossary entry, an answer and a release note
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured (1440)
| Style | Where | h2 | h3 | p | a | Notes |
|---|---|---|---|---|---|---|
| `.rich-text` | blog, answers (via `.answers_rich-text`), tutorials, legal, glossary | 35.2px/700, margin-top 48px | 25.6px/700 | 19.2px/400, line height 1.8, margin-bottom 32px | 19.2px/500 #3769ec | base 1.2rem; images radius 1.5rem; `.c-legal` 1rem/1.4; `.c-blog h1` dark |
| `.product-update_rich-text` | product updates, release notes | 32px/700 | 27.2px/700 | 17.6px/400, 1.8 | 17.6px/500 | base 1.1rem; images radius 1rem; `.list-item.is-checkmark` |
| plain `.w-richtext` | anything without a class | 52px/600 | 36px/600 | 17.6px/400, 1.6 | 17.6px/400 | inherits the page scale: h2 52px inside running text |
| `.cs-story-rich-text`, `.event_rich-text`, `.people-rich-text` | customer stories, events, people | own colour overrides | | | | per-template overrides |

## Known inconsistencies (as-is, no decision applied)
- No monospace token on the site: code and `<pre>` use `ui-monospace, monospace`
- Three heading scales and two paragraph sizes for the same job; the audit proposes one rich-text style with a light variant, product updates adopting it
- Rich-text headings are 700 where page headings are 600
- Every rich-text style has to undo the h1 gradient text fill (`-webkit-text-fill-color: inherit; background-image: none`)
- Image radius 1.5rem (`.rich-text`) vs 1rem (`.product-update_rich-text`) vs 16px (thumbnails)
- The blog post adds a "Summarize this article with AI" box and share rows that are page embeds, not part of the rich-text style
