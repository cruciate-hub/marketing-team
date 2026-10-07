# Buttons

Primary, secondary and text link from the style guide, plus the form submit button. States are shown statically: the live `:hover` and `:active` rules are copied onto `.sim-hover` and `.sim-active` classes in the preview.

- Status: draft (2026-10-07), as-is: current live values, no team decision applied · Owner: Stefan · Approved by: TO CHECK (Amadeus)
- Source: https://www.social.plus/styleguide (buttons block) and live buttons from /vs/circle (primary), /chat/sdk/ios (secondary), /social/uikit (text link), /contact/contact-sales and the footer (submit)
- Preview: preview.html (self-contained, links ../../tokens.css) · Code: styles.css · Screenshots: desktop.png (1440), mobile.png (390)
- Built on 2026-10-07 by capture/foundations.mjs from live-site snippets (capture/capture.config.json, `snippets`)

## Values as measured (1440)
- Primary `.cta-button` > `.cta-button_bg` > `.button-content` > `.button-text` + `.button-icon_wrapper` (arrow): outer `--social--main-blue`, radius 10em, 2px padding; inner gradient main blue to `--social--button-hover`, min-height 2.8rem, padding 8px 24px, radius 25em; text 16px/500 white. Hover: `.cta-border_rotate` rotating border (animation) ; pressed: `--social--button-pressed`
- Secondary `.cta-button.c-grey` > `.cta-button_bg.c-white`: outer `--border--border-dark-grey` #666, inner `--social--dark-gray-background` #1a1a1a, no gradient, same size. The class names say grey and white; the button is dark grey
- Text link `.text-link` > `.button-text` + arrow: 16px/500 white, no underline, hover `--text--text-color-grey-light`; the blue variant (Webflow component variant) uses `--social--main-blue`
- Form submit `input.button.w-button` (`.is-full-width`, `.c-demo`, `.c-webinar`): flat `--social--main-blue`, radius 10em, no arrow, no gradient; every form uses it (102 pages)
- Icon size token `--cta-button_icon-size` 1.75rem; inner variants `.c-customer-stories`, `.c-subscribe`, `.c-no-icon`, `.c-hmpg_industry`, `.c-full-width`, `.c-grow` tweak padding and icon

## Known inconsistencies (as-is, no decision applied)
- Two primary-blue buttons: `.cta-button` (gradient, arrow, rotating hover border) and `.button` (flat, no arrow) for form submits. The audit proposes styling submits as the primary button
- `.button_open-pop-up` (AWS and pricing pop-ups, 13 uses) is a fourth style and its `:active` uses a deleted variable (rewritten to #04be8c in the capture)
- Secondary button class names (`.c-grey`, `.c-white`) do not describe what they render
- The focus ring is the browser default on buttons (TO CHECK: the nav sets a 2px white ring)
