# Form inputs

The contact form (text fields, selects, textarea, custom checkbox, submit) and the footer newsletter form, with the site's own markup and rules. Success and error states are not captured.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Stefan or Amadeus)
- Source: https://www.social.plus/contact/contact-sales (`form`) and the footer form on /vs/circle
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured (1440)
- `.input-field`: 16px text, background #1b1b1b (not a token), 1px border `--social--main-blue`, radius 4px, height 52px; floating `<label class="input-label">` on `placeholder=" "`; label 14px `--text--text-color-grey-light`
- `.input-field_select` (`w-select`): same box with a chevron; `.input-field.c-area` textarea
- Checkbox: Webflow custom checkbox (`.w-checkbox-input--inputType-custom.c-checkbox-icon`); the native input is hidden by an inline style, which the capture keeps
- Submit: `input.button.is-full-width.w-button` (see foundations/buttons); privacy line `.text-size-tiny.text-color-grey-4` with a `.link-no-color` link
- Error text #dc3545 (not a token); `.c-contact-form__error` block
- Newsletter (footer): one email field and a "Join" submit `.button`; the Join button and the privacy line are hidden on the live site (TO CHECK)

## Known inconsistencies (as-is, no decision applied)
- `.input-field` is styled by page `<style>` embeds on the live site (170 embed references, 3 stylesheet rules); the preview carries the matching embed rules from the contact page
- The `.c-glass` input variant exists on /vs/ pages (see section 53)
- Two Talk to Sales pages (/contact/contact-sales and /contact/sales) differ in one numeric field
