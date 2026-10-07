# 40 · Article (blog post, answer, release note)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/blog/10-common-online-community-challenges-and-how-to-overcome-them, `section#main-content`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (blog post: tags, title, author and date, share buttons, intro, image, `.rich-text.c-blog` body, aside, bottom share row); `--answer` (https://www.social.plus/answers/api-for-…: title, image, `.answers_rich-text` body, one column); `--release-note` (https://www.social.plus/release-note/1-1-chat-…: title, tags, `.product-update_rich-text` body)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Every long-form page: blog posts, answers, tutorials, news, product updates and release notes. One layout: title block, meta, body in one of the rich-text styles (see foundations/rich-text).

## Don't use it when
Customer stories (41 + 42), glossary entries (04 + 43), marketing pages.

## Content slots
- Tags (blog, release notes), title H1 (48px on the blog, as-is), author with avatar and date (blog), share buttons (blog, news)
- Intro paragraph `.blog-intro-paragraph` (blog), hero image (blog, answers)
- Body: `.rich-text.c-blog` (blog), `.rich-text` (tutorials, news), `.answers_rich-text` (answers), `.product-update_rich-text` (updates, release notes): h2, h3, p, lists, blockquote, images, tables, links
- Aside (blog): table of contents and a webinar or CTA tile; the table of contents is built by a script on the live site and is empty in source.html (TO CHECK)
- Bottom: share row (blog), tags

## Allowed variations
- The three bodies above (the audit proposes one rich-text style with a light variant; captured as-is); with or without aside, image, share row
- Theme: the blog body is the "light body" of the audit (TO CHECK in the screenshot: the live section background stays `--social--dark`; only the rich-text colours differ)

## Not allowed
- Two columns of text, a sidebar form, pull quotes outside the rich text, headings above h2 in the body

## Accessibility and mobile
- One `<h1>`; body headings start at h2; images in the body need alt text (TO CHECK per post)
- The blog title is 48px/600 and the rich text 19.2px/1.8, the release note 17.6px/1.8 (as-is, see foundations/typography and rich-text)
- One column on phones, aside below the body; no sideways scroll at 390px

## Webflow note
- CMS templates (Blog Posts, Answers, Release Notes, Monthly Product Updates, Tutorials, Company News). Scripts for the table of contents, share buttons and reading time are removed from source.html. Class names are not a concern.
