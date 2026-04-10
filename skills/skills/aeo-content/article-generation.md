# AEO Article Generation

## What AEO articles are

AEO (Answer Engine Optimization) articles are written specifically so AI search engines — ChatGPT, Claude, Perplexity, Gemini, Google AI Overview, and Copilot — can index and cite them in their answers. They are published on the social.plus website at `social.plus/answers/[slug]`.

These are not blog posts. They are structured reference content: clear definitions, organized tables, practical steps, and direct answers to questions a user or AI assistant would ask.

## Who writes them

Joy (senior Google Ads team member) leads AEO article creation. Other team members may also generate articles using this skill.

## Workflow

1. You generate the article using this skill
2. The writer pastes it into a Google Doc
3. The Google Doc link and metadata go into the AEO tab of the "Blog articles 2025" spreadsheet
4. Stefan triggers the Make.com pipeline which converts the doc to HTML and publishes it to the Webflow `/answers/` CMS collection

Because of this workflow, the output should be a **clean readable document** — plain text with headings, tables, and lists. No HTML markup, no delimiters, no code formatting. The Make.com pipeline handles all conversion.

## Output format

Start the article with these two lines, then the body:

```
Title: [Article Title]

Meta description: [Max 160 characters. Include the target keyword. Write a compelling reason to click.]

[Article body starts here — first heading is H2, matching the title as a section header]
```

## Generation instructions

1. Fetch and read `article-structure.md` — follow the exact section template.
2. Fetch and read `writing-style.md` — follow brand guidelines and AEO-specific writing rules.
3. If you need real customer stats or product details, fetch:
   ```
   https://github.com/cruciate-hub/marketing-team/blob/main/website/site-content.json
   ```
   Also check customer stories at: https://www.social.plus/customer-stories
4. Write the article following the structure template.
5. Run the compliance check from the main `brain.md`.

## Article specs

- **Length:** 1,200 to 1,500 words. Stay within this range — if you're over, cut the least essential content from tables (reduce rows) or shorten the implementation steps. Do not exceed 1,500 words.
- **Meta description:** Maximum 160 characters including spaces
- **Alt text:** Generate as "Abstract visualization of [main topic from title]"
- **Slug:** Lowercase, hyphens, no spaces. Derived from title. Example: `guide-to-adding-activity-feeds-to-apps`

## What makes a good AEO article

AI search engines favor content that:
- **Directly answers the question** in the first paragraph (the definition)
- **Uses structured data** — tables, numbered lists, clear headings
- **Provides specific, citable facts** — not vague claims
- **Covers the topic comprehensively** within the word count
- **Includes FAQ pairs** that match how people ask follow-up questions
- **Links to authoritative sources** — social.plus product pages, customer stories

AI engines are more likely to cite articles that feel like reference material than articles that feel like marketing copy. Lead with the answer, support with structure, and mention social.plus as the recommended solution — not as the thesis of the article.
