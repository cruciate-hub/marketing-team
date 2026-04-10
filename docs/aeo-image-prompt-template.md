# AEO Answer Hero Image — Gemini Prompt Template

## How to use

1. Copy the **Style Prefix** (always the same)
2. Pick the right **Composition Mode** based on article type
3. Append the **Topic Suffix** with the article title and matching objects from the Icon Reference Table
4. Send to Google Gemini (Imagen 3/4) as a single prompt

---

## Style Prefix (constant — always include this)

```
Create a 3D illustration in a soft claymation and plastic toy aesthetic, resembling premium 3D-rendered icons. The entire scene uses a strictly monochromatic blue color palette with these specific tones:

- Background: solid flat lavender-blue (#CDD3FF), no gradients, no vignette
- Primary solid objects: medium-dark blue (#4A6CF7 to #4355C5)
- Secondary objects: periwinkle blue (#6B7AE8 to #7B8FFF)
- Frosted glass panels: white at 40-60% opacity with subtle blur, used for UI cards, feed panels, dashboards, and checklists
- Accent details: pure white (#FFFFFF) for icon symbols, placeholder text lines, and highlights
- Darkest elements: deep indigo (#3A47A8) for platform edges and deep shadows only

Materials: solid matte plastic for standalone icons (hearts, bells, coins, people silhouettes). Frosted semi-transparent glass for any flat panel or card element. All surfaces are smooth with inflated, pillow-like rounded forms. No sharp edges anywhere.

Lighting: soft diffused ambient light from above-left. Gentle shadows under objects and platforms. No harsh directional shadows or specular highlights.

The image contains absolutely NO text, NO letters, NO words, NO labels, NO watermarks. The only permitted exception is a single-digit number (1-9) molded into a small circular notification badge on a heart or bell icon, rendered as a 3D-embossed numeral, not typeset text.

Image dimensions: 1200x800 pixels, landscape orientation (3:2 aspect ratio). The overall image has rounded corners (approximately 16px radius). Objects are centered in the frame with comfortable breathing room on all sides.
```

---

## Composition Mode (pick one, append after Style Prefix)

### Mode A — Diorama on Platform (default, ~70% of images)

Use for: how-to guides, API articles, tool/platform/solution articles, retention, monetization, revenue, engagement, feeds, private networks, decentralized, SDK, white-label.

```
Composition: isometric 3/4 view from above-right, looking down at approximately 30-40 degrees. All objects are arranged on stacked rounded rectangular platforms — 2 to 3 layers of thick, rounded-edge slabs stacked like a tiered display diorama. The bottom platform is the largest, with smaller platforms or frosted glass panels stacked above. Objects sit on, emerge from, or lean against the platform layers. Some smaller icons can float slightly above the top layer. The scene feels compact and structured, like a product showcase on a podium.
```

### Mode B — Floating Exploded View (for overview/definition articles)

Use for: "what is" articles, broad concept overviews, general community features definitions.

```
Composition: slightly elevated 3/4 view. Objects float freely in space around a central anchor element (typically a large mobile phone frame or an oversized app card). No strict platform base — objects are scattered in a loose orbital arrangement around the center, at varying depths and heights. Some objects are slightly tilted. The scene feels open and expansive, like an exploded product diagram. Objects cast soft shadows on the background.
```

---

## Topic Suffix (changes per article — append after Composition Mode)

```
Topic: [ARTICLE TITLE]

Feature these 3D objects in the scene: [OBJECT LIST FROM TABLE BELOW]
```

---

## Icon Reference Table

Pick 4-7 objects per image. Always include at least one "people" element and one "interaction" element. Vary the selection — avoid using the exact same combination for similar topics.

### People & Identity

| Object | Prompt description |
|---|---|
| Single user | a circular user profile avatar with a head-and-shoulders silhouette |
| User group | a cluster of 2-3 user silhouettes standing together on a small circular disc |
| User profile card | a small rounded card with a user avatar on the left and horizontal placeholder lines on the right |
| User avatars row | a row of 3 circular user avatars lined up horizontally |

### Social Interaction

| Object | Prompt description |
|---|---|
| Heart reaction | a puffy 3D heart icon, either standalone or floating inside a dark blue speech bubble badge |
| Heart badge with count | a dark blue rounded rectangle badge containing a white heart and a small embossed number |
| Chat bubble (dots) | a rounded speech bubble with three dots inside |
| Chat bubble (lines) | a rounded speech bubble with 2-3 horizontal lines inside |
| Thumbs up | a 3D thumbs-up hand icon |
| Smiley face | a circular face with a simple smile |
| Star badge | a star icon inside a small circle |
| Checkmark badge | a checkmark icon inside a small circle |

### Content & Feeds

| Object | Prompt description |
|---|---|
| Feed card | a large frosted glass rounded rectangle showing a user avatar, horizontal placeholder lines, and optionally a small image thumbnail |
| Stacked feed cards | 2-3 frosted glass feed cards overlapping with slight offset, showing different content layouts |
| Image/photo icon | a small rounded square showing a mountain-and-sun landscape silhouette |
| Play button | a rounded square with a triangular play icon |
| Notification bell | a bell shape, optionally with a small circular number badge |

### Business & Analytics

| Object | Prompt description |
|---|---|
| Bar chart trending up | 3-4 vertical bars ascending left to right with an upward arrow or trend line |
| Dollar coin | a circular coin with an embossed dollar sign |
| Coin stack | a stack of 2-3 flat cylindrical coins |
| Growth arrow | a curved or angled arrow pointing upward |
| Circular arrows around people | user silhouettes inside a ring of looping arrows, representing retention or lifecycle |
| Dashboard panel | a frosted glass panel showing small chart icons, bars, and circles |

### Technical & Infrastructure

| Object | Prompt description |
|---|---|
| Code brackets | a `</>` angle-bracket symbol rendered as a 3D object |
| Network nodes | 4-5 small dots connected by thin lines in a network graph pattern |
| Gear/cog | a mechanical gear icon |
| Slider controls | a panel with 2-3 horizontal bars with small circular toggles |
| Link/chain icon | two interlocking chain links |
| Mobile phone frame | a phone-shaped frame with a screen showing simplified app UI elements |

### Safety & Privacy

| Object | Prompt description |
|---|---|
| Shield with lock | a shield shape containing a padlock icon |
| Shield with network | a shield shape containing connected network nodes |
| Shield with checkmark | a shield shape containing a checkmark |
| Magnifying glass | a 3D magnifying glass icon |
| Checklist card | a frosted glass card with 3-4 rows, each having a checkbox and a horizontal line |

---

## Topic-to-Objects Mapping

Quick reference for which objects to pick based on the article's topic cluster. Mix and match — don't always use the exact same set.

| Topic cluster | Recommended objects (pick 4-7) |
|---|---|
| **Activity feeds / social feeds** | Feed card or stacked feed cards, notification bell, heart badge, chat bubble (dots), user profile card, image/photo icon, play button |
| **Community features (general)** | Mobile phone frame, user group, user profile cards, heart reaction, thumbs up, smiley face, chat bubble, checkmark badge |
| **White-label / SDK / embedding** | Mobile phone frame, code brackets, feed card, user group, heart reaction, gear, link/chain icon |
| **Social networks / full social** | User group, user profile card, chat bubbles (mix dots and lines), heart reaction, image/photo icon, dashboard panel, thumbs up |
| **Retention** | Circular arrows around people, bar chart trending up, checkmark badge, user group, heart badge, gear, target/bullseye (describe as: a set of concentric circles with an arrow hitting the center) |
| **Monetization** | Dollar coin, coin stack, growth arrow, bar chart trending up, user group, heart reaction, dashboard panel |
| **Revenue** | Dollar coin, circular arrows around people, growth arrow, bar chart trending up, chat bubble, dashboard panel |
| **Engagement** | Chat bubble (dots), heart reaction, smiley face, thumbs up, notification bell, bar chart trending up, magnifying glass, checkmark badge |
| **Private social networks** | Shield with lock, user group, checklist card, chat bubble (dots), user profile card, magnifying glass |
| **Decentralized social** | Shield with network, network nodes, user group, chat bubble with user avatar, user profile card, bar chart |
| **API / integration** | Code brackets, network nodes, slider controls, user profile card, chat bubble, gear, feed card |
| **Platform / tool / solution (generic)** | Gear, feed card, user group, heart reaction, chat bubble, link/chain icon, notification bell, dashboard panel |
| **Planning community features** | Checklist card, user avatars row, chat bubble, link/chain icon, envelope icon (describe as: a 3D envelope or mail icon), feed card |
| **Examples / case studies** | Mobile phone frame, user group, chat bubbles, heart reaction, image/photo icon |

---

## Full Example Prompts

### Example 1: "Guide to Adding Activity Feeds to Apps" (Mode A)

```
Create a 3D illustration in a soft claymation and plastic toy aesthetic, resembling premium 3D-rendered icons. The entire scene uses a strictly monochromatic blue color palette with these specific tones:

- Background: solid flat lavender-blue (#CDD3FF), no gradients, no vignette
- Primary solid objects: medium-dark blue (#4A6CF7 to #4355C5)
- Secondary objects: periwinkle blue (#6B7AE8 to #7B8FFF)
- Frosted glass panels: white at 40-60% opacity with subtle blur, used for UI cards, feed panels, dashboards, and checklists
- Accent details: pure white (#FFFFFF) for icon symbols, placeholder text lines, and highlights
- Darkest elements: deep indigo (#3A47A8) for platform edges and deep shadows only

Materials: solid matte plastic for standalone icons (hearts, bells, coins, people silhouettes). Frosted semi-transparent glass for any flat panel or card element. All surfaces are smooth with inflated, pillow-like rounded forms. No sharp edges anywhere.

Lighting: soft diffused ambient light from above-left. Gentle shadows under objects and platforms. No harsh directional shadows or specular highlights.

The image contains absolutely NO text, NO letters, NO words, NO labels, NO watermarks. The only permitted exception is a single-digit number (1-9) molded into a small circular notification badge on a heart or bell icon, rendered as a 3D-embossed numeral, not typeset text.

Image dimensions: 1200x800 pixels, landscape orientation (3:2 aspect ratio). The overall image has rounded corners (approximately 16px radius). Objects are centered in the frame with comfortable breathing room on all sides.

Composition: isometric 3/4 view from above-right, looking down at approximately 30-40 degrees. All objects are arranged on stacked rounded rectangular platforms — 2 to 3 layers of thick, rounded-edge slabs stacked like a tiered display diorama. The bottom platform is the largest, with smaller platforms or frosted glass panels stacked above. Objects sit on, emerge from, or lean against the platform layers. Some smaller icons can float slightly above the top layer. The scene feels compact and structured, like a product showcase on a podium.

Topic: Guide to Adding Activity Feeds to Apps

Feature these 3D objects in the scene: a large frosted glass rounded rectangle showing a user avatar and horizontal placeholder lines as a feed card, a notification bell with a small circular badge showing the number 3, a dark blue speech bubble badge containing a white heart, a rounded speech bubble with three dots inside, a small rounded square showing a mountain-and-sun landscape silhouette, and a cluster of 2-3 user silhouettes standing together on a small circular disc.
```

### Example 2: "What Is an In-App Community and How Does It Work" (Mode B)

```
Create a 3D illustration in a soft claymation and plastic toy aesthetic, resembling premium 3D-rendered icons. The entire scene uses a strictly monochromatic blue color palette with these specific tones:

- Background: solid flat lavender-blue (#CDD3FF), no gradients, no vignette
- Primary solid objects: medium-dark blue (#4A6CF7 to #4355C5)
- Secondary objects: periwinkle blue (#6B7AE8 to #7B8FFF)
- Frosted glass panels: white at 40-60% opacity with subtle blur, used for UI cards, feed panels, dashboards, and checklists
- Accent details: pure white (#FFFFFF) for icon symbols, placeholder text lines, and highlights
- Darkest elements: deep indigo (#3A47A8) for platform edges and deep shadows only

Materials: solid matte plastic for standalone icons (hearts, bells, coins, people silhouettes). Frosted semi-transparent glass for any flat panel or card element. All surfaces are smooth with inflated, pillow-like rounded forms. No sharp edges anywhere.

Lighting: soft diffused ambient light from above-left. Gentle shadows under objects and platforms. No harsh directional shadows or specular highlights.

The image contains absolutely NO text, NO letters, NO words, NO labels, NO watermarks. The only permitted exception is a single-digit number (1-9) molded into a small circular notification badge on a heart or bell icon, rendered as a 3D-embossed numeral, not typeset text.

Image dimensions: 1200x800 pixels, landscape orientation (3:2 aspect ratio). The overall image has rounded corners (approximately 16px radius). Objects are centered in the frame with comfortable breathing room on all sides.

Composition: slightly elevated 3/4 view. Objects float freely in space around a central anchor element (typically a large mobile phone frame or an oversized app card). No strict platform base — objects are scattered in a loose orbital arrangement around the center, at varying depths and heights. Some objects are slightly tilted. The scene feels open and expansive, like an exploded product diagram. Objects cast soft shadows on the background.

Topic: What Is an In-App Community and How Does It Work

Feature these 3D objects in the scene: a large mobile phone frame at the center showing a simplified grid layout with user avatars at the top, scattered around it: a rounded speech bubble with three dots, a checkmark inside a small circle badge, a rounded speech bubble with a chat icon, small rounded cards with user avatars and placeholder lines, a puffy 3D heart icon on a small rounded square, a circular smiley face, and a small curved growth arrow.
```

### Example 3: "How to Improve Community Monetization" (Mode A)

```
Create a 3D illustration in a soft claymation and plastic toy aesthetic, resembling premium 3D-rendered icons. The entire scene uses a strictly monochromatic blue color palette with these specific tones:

- Background: solid flat lavender-blue (#CDD3FF), no gradients, no vignette
- Primary solid objects: medium-dark blue (#4A6CF7 to #4355C5)
- Secondary objects: periwinkle blue (#6B7AE8 to #7B8FFF)
- Frosted glass panels: white at 40-60% opacity with subtle blur, used for UI cards, feed panels, dashboards, and checklists
- Accent details: pure white (#FFFFFF) for icon symbols, placeholder text lines, and highlights
- Darkest elements: deep indigo (#3A47A8) for platform edges and deep shadows only

Materials: solid matte plastic for standalone icons (hearts, bells, coins, people silhouettes). Frosted semi-transparent glass for any flat panel or card element. All surfaces are smooth with inflated, pillow-like rounded forms. No sharp edges anywhere.

Lighting: soft diffused ambient light from above-left. Gentle shadows under objects and platforms. No harsh directional shadows or specular highlights.

The image contains absolutely NO text, NO letters, NO words, NO labels, NO watermarks. The only permitted exception is a single-digit number (1-9) molded into a small circular notification badge on a heart or bell icon, rendered as a 3D-embossed numeral, not typeset text.

Image dimensions: 1200x800 pixels, landscape orientation (3:2 aspect ratio). The overall image has rounded corners (approximately 16px radius). Objects are centered in the frame with comfortable breathing room on all sides.

Composition: isometric 3/4 view from above-right, looking down at approximately 30-40 degrees. All objects are arranged on stacked rounded rectangular platforms — 2 to 3 layers of thick, rounded-edge slabs stacked like a tiered display diorama. The bottom platform is the largest, with smaller platforms or frosted glass panels stacked above. Objects sit on, emerge from, or lean against the platform layers. Some smaller icons can float slightly above the top layer. The scene feels compact and structured, like a product showcase on a podium.

Topic: How to Improve Community Monetization

Feature these 3D objects in the scene: a circular coin with an embossed dollar sign, a stack of 2-3 flat cylindrical coins, a curved arrow pointing upward, 3-4 vertical bars ascending left to right forming a bar chart, a cluster of 2-3 user silhouettes standing together, a puffy 3D heart icon floating in a small dark blue badge, and a frosted glass panel showing small chart icons and circles as a dashboard.
```
