# 23 · CTA band (inline)

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/pricing, `section#support-packages`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (centred heading, one paragraph, one grey button); `--two-buttons` (https://www.social.plus/ai/mcp-server, section "Start building": centred heading, one line, primary + grey button)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A page needs a short call to action between sections (pricing: support packages; AI pages: start building) that is not the closing band.

## Don't use it when
As the last section (that is the footer CTA band, G4), more than once per page, or when the page has a form section (24).

## Content slots
- Heading H2, 2 to 6 words; one paragraph 15 to 35 words or one line
- One grey button, or primary + grey (two-buttons variant)

## Allowed variations
- One or two buttons; with or without the paragraph

## Not allowed
- Images, a background band in another colour, three buttons, a form

## Accessibility and mobile
- Heading `<h2>`; buttons are links
- Height about 340px (default) to 580px (two-buttons); stacks on phones; no sideways scroll at 390px

## Webflow note
- Webflow component "CTA / Features Pages" (3) and plain sections. Class names are not a concern.
