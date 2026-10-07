# 53 · vs / Customer stories (tabbed) + form

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, section "Trusted by today's leading consumer apps. Yours could be next."
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variant captured: 4 stories (logo tabs plus photo slide) and the contact form
- Captured on 2026-10-07 from https://www.social.plus/vs/circle by capture/capture.mjs

## Use it when
The page needs its conversion point: proof (customer stories) and the contact form in one card. On /vs/ pages it follows the comparison table.

## Don't use it when
The page has a dedicated form section already, or when stories without a form are wanted (TO CHECK: whether a stories-only variant belongs in the set).

## Content slots
- Heading (H2, max 12 words, centred, wide)
- One rounded card (radius 1.44 rem, `--social--dark`) with a soft blue radial background on the section
- Left: story slider. 4 logo tabs, each with a thin progress bar above the logo (bar fills left to right during autoplay, the picked story keeps a full white bar). One story visible: full-bleed photo with a dark shade, a big stat (number plus label, for example "40%" "market Share in the US"), a one-line title, and a "Read story" text link with arrow. Live stories: Ulta Beauty, Noom, Smart Fit, Syngenta
- Right: form title (H3, max 15 words) and the contact form: Full name, Business email, Company, Monthly Active Users (select, 7 options), Use case (textarea), "How did you first hear about social.plus?", a marketing opt-in checkbox, a full-width "Submit" button (main blue), and a consent line with a Privacy Policy link. A Company size select exists in the HTML but is hidden

## Allowed variations
- Which 4 stories (from the Customer Stories CMS). Heading and form title text. Nothing else

## Not allowed
- More or fewer than 4 tabs (TO CHECK), a form without the consent line, extra fields, a light background, stories without stats

## Accessibility and mobile
- Tabs are `<button>`s with `aria-pressed`; slides switch on click, tap or keyboard. Autoplay (6 s per story) pauses on hover, focus and while off-screen; off under reduced motion
- Form fields have visible floating labels, `required` attributes and glass styling (`.c-glass`: translucent field over the photo on desktop)
- Desktop: the stories fill the card and the form sits in a 47% column on the right. Phones: stories on top (30 rem tall), form below, full width; no sideways scroll at 390 px
- `source.html` shows the first story (static-state CSS at the end of the `<style>`); the other three are in the HTML

## Webflow note
- Custom section: Customer Stories CMS list plus Webflow form. The slider script, the form endpoint (`action`), hidden fields and anti-bot attributes were removed from source.html; the field styling `<style>` embed is kept. Class names are not a concern.
