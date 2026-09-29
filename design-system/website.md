# social.plus Website Tokens

Source: the live Webflow site (Webflow variables, General + Typography collections), mirrored in the [website style guide](https://cruciate-hub.github.io/marketing-team/design-system/website/style-guide.html) and in `marketing-team/skills/claude-design-to-webflow/references/variable-ids.md` (variable IDs for binding).

**Use this file for anything that appears on, or must match, social.plus the website:** Webflow builds and styling, landing-page and section mockups, blog/glossary/answers visuals, marketing HTML, emails, social graphics. For those tasks these values override the extended design system (`colors-palette.md`, `colors-usage.md`, `buttons.md`); the heading scale matches `typography.md`. The extended files remain the reference for **product/app UI** (the in-app community UI kit: avatars, feeds, bottom sheets, tab bars).

If the site's variables change, re-run `data_variable_tool get_variables` on the social.plus site and update this file, `variable-ids.md` and the style guide together.

---

## Colors

### Core surfaces

| Webflow variable | Hex | Use |
|---|---|---|
| `--social--dark` | `#111111` | Default page background (dark-first) |
| `--social--dark-gray-background` | `#1A1A1A` | Raised dark section |
| `--secondary--menu-bg` | `#181818` | Nav bar, mobile nav sheet, nav CTA card |
| `--social--grey` | `#222222` | Dark card / panel |
| `--social--light-grey` | `#444444` | Dark subtle fill |
| `--social--grey-background` | `#F9F9F9` | Light section background |
| `--main--whitesmoke` | `#F5F5F5` | Light alternate background |
| `--main--white` | `#FFFFFF` | Light background, white text on dark |

### Brand blue (the only CTA color)

| Webflow variable | Hex | Use |
|---|---|---|
| `--social--main-blue` | `#3B41EC` | Primary button, links, brand fill |
| `--social--button-hover` | `#272B9D` | Primary button hover |
| `--social--button-pressed` | `#27265E` | Primary button pressed |
| `--social--blue-transparent` | `rgba(42, 49, 233, 0.1)` | Tinted blue background |

### Secondary (decoration and status, never CTAs)

| Webflow variable | Hex |
|---|---|
| `--secondary--green` | `#1DC497` |
| `--secondary--yellow` | `#F7C506` |
| `--secondary--red` | `#FF305A` |
| `--secondary--orange` | `#FF6937` |
| `--secondary--purple` | `#9F72FF` |
| `--secondary--pink` | `#F568F0` |

### Text

| Webflow variable | Hex | Use |
|---|---|---|
| `--main--white` | `#FFFFFF` | Text on dark |
| `--text--text-color-grey-light` | `#B3B3B3` | Secondary text on dark |
| `--text--text-color-grey-medium` | `#717275` | Muted text |
| `--text--text-color-grey-dark` | `#414347` | Secondary text on light |
| `--text--text-color-dark` | `#111111` | Text on light |

### Borders

| Webflow variable | Hex | Use |
|---|---|---|
| `--border--border-light-grey` | `#E7E7E7` | Light-mode divider |
| `--border--border-med-grey` | `#D0D0D1` | Light-mode input/card border |
| `--border--border-dark-grey` | `#666666` | Secondary button outline |
| `--border--border-dark` | `#232324` | Dark-mode divider |
| `--border--border-hover` | `#39393A` | Dark-mode card/subnav border, hover border |

### Gradients

Stops: `--gradient--light-blue` `#45A5ED`, `--gradient--medium-blue` `#3769EC`, `--gradient--dark-blue` = `#3B41EC` (main blue).

| Gradient on the site | Stops |
|---|---|
| Blue (announcement banner, heroes) | light-blue → medium-blue → dark-blue |
| Warm | pink `#F568F0` → orange `#FF6937` → yellow `#F7C506` |
| Orange to yellow | `#FF6937` → `#F7C506` |
| Pink to orange | `#F568F0` → `#FF6937` |
| Red to pink | `#FF305A` → `#F568F0` |

---

## Typography

Figtree variable font (weights 300-900). Heading sizes are fluid Webflow variables:

| Level | Variable | Value | Range |
|---|---|---|---|
| H1 | `--h1-font-size` | `clamp(2.75rem, 1.5rem + 2svw, 5rem)` | 44-80px |
| H2 | `--h2-font-size` | `clamp(2.25rem, 1.5rem + 2svw, 3.25rem)` | 36-52px |
| H3 | `--h3-font-size` | `clamp(1.75rem, 1rem + 2svw, 2.25rem)` | 28-36px |
| H4 | `--h4-font-size` | `clamp(1.5rem, 0.875rem + 2svw, 1.75rem)` | 24-28px |
| H5 | `--h5-font-size` | `1.25rem` | 20px |
| H6 | `--h6-font-size` | `1.125rem` | 18px |

No monospace variable exists on the site; use `ui-monospace, monospace` for code.

---

## Layout and components

| Element | Value |
|---|---|
| `.container-large` | max-width 80rem (1280px), centered |
| `.container-medium-large` | max-width 65rem (1040px) |
| `.container-heading` | max-width 50rem (800px) |
| `.container-medium` | max-width 47.5rem (760px) |
| Buttons | Pill shape (border-radius 10em/25em), arrow icon 1.75rem. Primary = main blue, hover `#272B9D`, pressed `#27265E`. Secondary = outline `--border--border-dark-grey` |
| Nav | Component "Nav / Main", bar height 5.25rem (84px), background `--secondary--menu-bg` |
| Footer CTA | Component "Section / Footer / Contact Forms", Contact Sales button scaled 1.2x |

---

## Where the extended design system differs

These extended-system values are **wrong for website output**. Use the website value.

| Role | Extended system | Website (use this) |
|---|---|---|
| Primary button hover | `#3133D1` | `#272B9D` |
| Primary button pressed | `#2B2FA8` (ultra-800) | `#27265E` |
| Orange | `#F66005` | `#FF6937` (also in the warm, orange-yellow and pink-orange gradients) |
| Purple | not defined | `#9F72FF` |
| Nav / menu background | not defined | `#181818` |
| Dark card / panel | not defined | `#222222`, `#444444` |
| Light section background | not defined | `#F9F9F9` |
| Text greys | `#535353`, `#A3A3A3`, white at 66%/36% | `#B3B3B3`, `#717275`, `#414347` |
| Borders | translucent black/white (`rgba(…, 0.05-0.28)`) | solid `#E7E7E7`, `#D0D0D1`, `#666666`, `#232324`, `#39393A` |

App UI component files (`avatars.md`, `cards.md`, `list-items.md`, `navigation.md`, `overlays.md`, `feedback.md`, `states.md`, `empty-states.md`) describe the in-app product UI. Don't apply them to website pages.
