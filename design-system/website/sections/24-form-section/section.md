# 24 · Form section

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/contact/contact-sales, `section#main-content`
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css (variants: the same files with a `--<variant>` suffix)
- Variants captured: default (contact: heading, text and customer logos left; the contact form right); `--with-image` (https://www.social.plus/social/uikit, `section#figma`: download form left, image right)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
A page exists to collect one thing: a sales request (contact pages), a download (Figma UI kit), a subscription. One form per page.

## Don't use it when
A /vs/ page (the form is part of 53), a page that already has a form, a newsletter (that is the footer).

## Content slots
- Heading H2, 4 to 7 words ("Get in touch with our team", "Figma Social UI Kit"); paragraph 20 to 40 words
- Contact form: first name, last name, business email, company, monthly active users (select), company size (select), use case (textarea), consent checkbox, submit `.button.is-full-width`; the privacy line in `.text-size-tiny`
- Download form: first name, last name, business email, submit; privacy line
- Left column extras (contact): a row of customer logos; right column (download): one image

## Allowed variations
- Field set per purpose (3 to 8 fields); with logos, with image, or text only; TO CHECK: the subscribe form (/product-updates/subscribe) is not captured

## Not allowed
- Two forms, a form inside a card grid, fields without labels, a blue primary `.cta-button` as the submit (the submit is `.button`, as-is today; the audit proposes styling it as the primary button)

## Accessibility and mobile
- Every field has a `<label>` (floating label on `placeholder=" "`); required fields carry `required`; the checkbox is a custom Webflow checkbox with its native input hidden by inline style (kept)
- The form's `action`, hidden fields and the anti-bot attributes are removed in source.html; success and error states are not captured
- Two columns stack on phones, form below the text; no sideways scroll at 390px

## Webflow note
- Webflow components "CC / Contact Form" (8), "CC / Form" (5), "Form Privacy Disclaimer" (6). The `.input-field` style comes from page `<style>` embeds on the live site (kept in source.html). Class names are not a concern.
