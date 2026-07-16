# social.plus Webflow — site identity & variable IDs

Pre-mapped so `data_style_tool` calls can pass `variable_as_value` **without** a prior `data_variable_tool query_variables` round-trip (one fewer call per binding). Only load this file when you're binding variables on the social.plus site. If variables get renamed/rebuilt, re-run `data_variable_tool query_variables` (`type: "Color" | "FontFamily" | "Size"`) and update the table.

> These IDs are already public (they ship in the site's compiled CSS). Nothing secret here — but they are social.plus-specific; on any other site, query first.

## Site identity

| Field | Value |
|---|---|
| Site ID | `66e2765d540e1939a89db4bb` |
| Staging URL | `https://social-plus.webflow.io` (publish here: `publishToWebflowSubdomain: true`, `customDomains: []`) |
| Production URLs | `https://social.plus`, `https://www.social.plus` (publish ONLY on explicit go-ahead) |
| Designer URL | `https://social-plus.design.webflow.com` (only needed for Designer-bridge tools) |
| Read the current page ID from the live page | `document.documentElement.getAttribute('data-wf-page')` |

## Colors

| Variable name | CSS name | Resolved | Variable ID |
|---|---|---|---|
| Main / White | `--main--white` | white | `variable-64679256` |
| Main / Whitesmoke | `--main--whitesmoke` | whitesmoke | `variable-64b3418a-aee4-0527-65cd-08e01561063f` |
| Main / Transparant | `--main--transparant` | rgba(0,0,0,0) | `variable-db517b61-7872-ac88-bdfa-14051268d017` |
| Social+ / Dark | `--social--dark` | #111 | `variable-4b9c57ec` |
| Social+ / Grey | `--social--grey` | #222 | `variable-93f1af9a-ee0a-62f6-5fb2-ce43081d7eda` |
| Social+ / Light Grey | `--social--light-grey` | #444 | `variable-a08161c0-23fb-489b-eebf-f535db04ade6` |
| Social+ / Main Blue | `--social--main-blue` | #3b41ec | `variable-90f1b4a4` |
| Social+ / Button Hover | `--social--button-hover` | #272b9d | `variable-7d4fe31d-0948-1b55-a84b-21deba3e4a6b` |
| Social+ / Button Pressed | `--social--button-pressed` | #27265e | `variable-8012071c-6fc9-c9a8-525f-c192cee5618b` |
| Social+ / Grey - Background | `--social--grey-background` | #f9f9f9 | `variable-f3ca0706` |
| Social+ / Dark Gray - Background | `--social--dark-gray-background` | #1a1a1a | `variable-0531ab56-9952-a6da-1c2c-8262ee55d79f` |
| Social+ / Blue - Transparent | `--social--blue-transparent` | rgba(42,49,233,0.1) | `variable-a1df43dd-b4b0-8263-c5e4-f38eb4513a63` |
| Border / Med Grey | `--border--border-med-grey` | #d0d0d1 | `variable-1ebfe481` |
| Border / Light Grey | `--border--border-light-grey` | #e7e7e7 | `variable-e1e41c15-557c-5595-6f23-7e4c9178fd09` |
| Border / Dark Grey | `--border--border-dark-grey` | #666 | `variable-c5053a4c-e7fa-05c0-7283-5ef0a55c0e29` |
| Border / Dark | `--border--border-dark` | #232324 | `variable-ee98de1f-5b66-8a8d-2010-ae0db98dd8e9` |
| Border / Hover | `--border--border-hover` | #39393a | `variable-2c99aafc-aeb3-0ebc-3d92-c92e7891f273` |
| Secondary / Green | `--secondary--green` | #1dc497 | `variable-18f1dead-7525-dd3f-bdd3-7cd00945b38c` |
| Secondary / Yellow | `--secondary--yellow` | #f7c506 | `variable-07fd785f` |
| Secondary / Red | `--secondary--red` | #ff305a | `variable-d9410529` |
| Secondary / Orange | `--secondary--orange` | #ff6937 | `variable-f5e53ba8` |
| Secondary / Purple | `--secondary--purple` | #9f72ff | `variable-9af8501e` |
| Secondary / Pink | `--secondary--pink` | #f568f0 | `variable-3e1afd9e-e8c4-70f8-a2d3-be13897db84e` |
| Secondary / menu-bg | `--secondary--menu-bg` | #181818 | `variable-e58813e9-3707-fe97-0d83-e8ebd9babe88` |
| Text / Grey Light | `--text--text-color-grey-light` | #b3b3b3 | `variable-fe935cb0` |
| Text / Grey Medium | `--text--text-color-grey-medium` | #717275 | `variable-40c37db5` |
| Text / Grey Dark | `--text--text-color-grey-dark` | #414347 | `variable-69de6259-0e11-0c77-68bb-b61792bb5111` |
| Text / Dark | `--text--text-color-dark` | #111 | `variable-ff7e9502` |
| Gradient / Light Blue | `--gradient--light-blue` | #45a5ed | `variable-27b4895e-439b-ad85-273f-1cab7a1c66dd` |
| Gradient / Medium Blue | `--gradient--medium-blue` | #3769ec | `variable-9d2daeaf-7873-d545-1df4-c1f6bbdd293f` |
| Gradient / Dark Blue | `--gradient--dark-blue` | (refs Main Blue) | `variable-21c7e8f0-11db-ff41-5442-73fa0b30e44b` |

**Nav-specific (from the 2026-07 nav rebuild):** the mobile nav sheet, top bar, and CTA card all use `--secondary--menu-bg` (#181818) as background; the card/subnav border is `--border--border-hover` (#39393a). Matching a "box" to the nav means binding its bg to `--secondary--menu-bg`.

## Fonts

| Variable name | CSS name | Variable ID |
|---|---|---|
| Font / Figtree | `--font--figtree` | `variable-349b794c-a39f-b897-5ec6-dcc9abc79896` |

*No monospace variable exists — use static `ui-monospace, monospace` for code-style fonts.*

## Sizes

| Variable name | CSS name | Resolved | Variable ID |
|---|---|---|---|
| CTA button icon size | `--cta-button_icon-size` | 1.75rem | `variable-908831f1-6b53-3941-0c6a-a6f11bfeaa5a` |
| H1 font-size | `--_typography---h1-font-size` | clamp(2.75rem, 1.5rem + 2svw, 5rem) | `variable-a8a20bf7-5527-65d0-d6f2-13a566cde28f` |
| H2 font-size | `--_typography---h2-font-size` | clamp(2.25rem, 1.5rem + 2svw, 3.25rem) | `variable-a5470ceb-ca75-3139-a1a5-75465e71c1d2` |
| H3 font-size | `--_typography---h3-font-size` | clamp(1.75rem, 1rem + 2svw, 2.25rem) | `variable-bae162a2-2440-1569-6548-bcdea4b7d040` |
| H4 font-size | `--_typography---h4-font-size` | clamp(1.5rem, 0.875rem + 2svw, 1.75rem) | `variable-58495678-3e36-43ed-7f9c-e2f27035eb9d` |
| H5 font-size | `--_typography---h5-font-size` | 1.25rem | `variable-09545625-e631-25f7-8e80-69a6f1657a38` |
| H6 font-size | `--_typography---h6-font-size` | 1.125rem | `variable-c49a7ca3-a0e4-72a0-c2c7-8f944dfc0734` |
