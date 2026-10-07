# Recipe: an SDK page

A page for one SDK on one platform (Chat SDK for iOS, Social SDK for Android, …), like https://www.social.plus/chat/sdk/ios. Fixed order. Nav (G1) and sub-nav (G2) above, footer CTA band (G4) and footer (G5) below.

| Order | Section | Content slots to fill | Notes |
|---|---|---|---|
| G1 | Nav | none (shared) | always |
| G2 | Sub-nav | product family links | Chat or Social family |
| 01 | Hero / Product (`--two-buttons`) | H1 with the platform name, paragraph, Contact Sales + Documentation, product video | `<header>` tag on SDK pages |
| 10 | Logo wall (`--marquee`) | customers from the CMS | |
| 11 | Two-column (`--checklist`) | heading, paragraph, 3 to 5 checklist items, image | "Easily integrate … in your <platform> app" |
| 11 | Two-column (`--image-left`) | heading, paragraph, grey button "UI Kit", image | the open-source UI kit for the platform; radial-gradient background |
| 12 | Feature grid | heading, intro, grey button, CMS features | the same features as the product page |
| 11 | Two-column (`--video-cta`) | eyebrow "Discover more", heading, paragraph, grey button, video | points to the other SDK (Social or Chat) for the same platform |
| G4 | Footer CTA band | heading, line | "Contact Sales" button |
| G5 | Footer | none (shared) | always |

Rules for the page:

- Three two-column sections, in this order and with these variants; the image side alternates (right, left, right).
- One platform per page; the platform name appears in the H1 and in the checklist heading.
- Nothing else is added. An SDK page never carries pricing, a form or a customer story strip.
