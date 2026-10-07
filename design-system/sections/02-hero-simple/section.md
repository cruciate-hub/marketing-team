# 02 · Hero / Simple (title, text, buttons)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/ai/mcp-server, `header.section.padding_y.background-color_dark` (first)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (eyebrow, H1, text, primary + grey button, small logos row "Works in …"); `--illustration` (https://www.social.plus/chat/sdk, `section#main-content`: H1, text, two buttons, platform icons row, image slider right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A page opens with a statement and buttons but has no single product image to show: overview pages (Chat SDK overview, trust, AI pages).

## Don't use it when
A product image or video exists (01); industry pages (03); articles (04).

## Content slots
- Eyebrow: a short `.superscript` line above the title (live: "social.plus MCP Server"); optional
- H1: 6 to 9 words; paragraph: 20 to 40 words (`.max-ch-50` caps the line length)
- Buttons: primary + grey secondary (live: "Connect your AI tool" + "Documentation"; "Contact Sales" + "Documentation")
- Default: the "Works in" row: the label "Works in" between two divider lines, then one link per tool: the icon in a 40px tile with a 1px `--border--border-hover` border (`.mcp-logo`), the name beside it, and "+ Any MCP-compatible tool" as plain text at the end. The icons are the approved files in `../../assets/third-party/ai-tools/` (Claude, Cursor, VS Code, Copilot, OpenAI for Codex and ChatGPT; the Claude mark for Claude Code); only tools the product supports today. The label is always "Works in"
- Illustration variant: a row of platform icons (iOS, Android, Web, …) and an image slider on the right (`.bf-slider`; the first image shows, the rest is script)

## Allowed variations
- With or without the eyebrow and the logos row; one or two buttons; text left with illustration right, or centred (default)

## Not allowed
- A video, a form, a background image, more than two buttons, a light variant
- The tool names as plain text when an approved icon exists; any other label than "Works in"; logos redrawn or lettered

## Accessibility and mobile
- One `<h1>`; the logos row images need alt text (TO CHECK on the live site); the slider arrows are script driven and not in source.html
- The default page (/ai/mcp-server) adds its own `<style>` embeds with page-only custom properties; they are kept in source.html and are not tokens (TO CHECK: rebuild on the set's tokens)
- Stacks on phones; no sideways scroll at 390px

## Webflow note
- Built as a plain section on the page; class names are not a concern.
