# G5 · Footer

- Status: draft (2026-10-07) · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/vs/circle, `footer.footer-wrapper` (the same footer is on every page)
- Screenshots: desktop.png, mobile.png · Code: source.html, styles.css
- Variants captured: default (dark, newsletter form, 4 link columns); `--no-newsletter` (https://www.social.plus/contact/contact-sales: the same footer without the newsletter form, as on the contact pages)
- Captured on 2026-10-07 by capture/capture.mjs

## Use it when
Every website page, directly below the footer CTA band (G4); on contact pages and article pages without a CTA band it follows the content.

## Don't use it when
Never leave it out.

## Content slots
- Row 1 left: logo, "Subscribe to our newsletter:", one email field (the Join button and the privacy line are hidden on the live site; TO CHECK whether that is intended)
- Row 1 right: 4 columns with a heading and 5 links each: Product, Company, Resources, Support. Careers carries a "We're hiring!" tag; external links (Documentation, Developer Forum, Service Status) carry an external-link icon
- Row 2: legal links (GDPR with icon, Privacy Policy, Terms and Conditions, Legal, Trust, Cookies) left; 5 social icons right (LinkedIn, Instagram, YouTube, Figma, GitHub; X exists but is hidden)
- Row 3: copyright line left, "Search" link right

## Allowed variations
- Link text and targets follow the site map. Column count stays 4
- With or without the newsletter form (contact pages leave it out so the page has one form)

## Not allowed
- Light background, extra rows, a second newsletter form, changed column order

## Accessibility and mobile
- `<footer aria-label="Site footer">`. Links are `<a role="button">` on the live site (TO CHECK: role should be dropped for plain links)
- On phones the 4 columns become 2 by 2, the newsletter block moves below them, the legal links stack, the logo and social icons sit at the bottom. No sideways scroll at 390 px
- Text sizes: headings 1 rem bold white, links `--text--text-color-grey-light`, bottom rows tiny `--text--text-color-grey-medium`

## Webflow note
- Webflow component "Footer". The newsletter form posts to the site's form endpoint; `action`, hidden fields and the anti-bot attributes were removed from source.html.
