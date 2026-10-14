# Explainers (Reels, shorts, Vox-style)

A story, not slides. The single biggest failure is a sequence of same-layout scenes with text in the same place. Think one continuous world and a camera travelling through it.

## 1. Script first

- Read the whole source. Pull the claim, 3–5 beats of evidence or turn, and one close.
- Arc: **hook** (the claim, ≤4 s) → **evidence** (1–2 numbers, with sources) → **turn** (why / what still works) → **payoff** (the alternative, with a number if the source has one) → **close** (a line people remember + social.plus).
- Voiceover at ~2.6–2.8 words per second: ~80 words for 30 s. Short sentences, spoken numbers ("almost fourteen percent"), no jargon.
- Deliver the script as a table: time · voiceover · on-screen text. On-screen text is the key point only, never the whole voiceover.

## 2. Storyboard as camera moves through one world

Lay out the objects of every beat in one large world (a phone, a document, a tilted plane, a card, a network) and move a camera (`cx, cy, z` keys, log-interpolated zoom) between them. Each beat changes perspective:

- **Extreme close-up → pull back** to reveal context (open on one notification, reveal the pile).
- **Whip pan** (fast ease-out, whoosh) to the evidence: a tilted report page, an accent highlighter sweeping over the quoted line.
- **New plane**: tilt the world (CSS 3D, rotateX ~48°) for a "system" view where things sort or flow.
- **Match cut**: an object from one beat becomes the hero of the next (a tile flips up into a full card).
- **Big pull back** to reveal scale (the card is one node in a network).
- **Dive** into the accent element to transition into the end card.

Objects persist and transform across beats; avoid hard cuts between unrelated layouts.

## 3. Kinetic typography — a different form every beat

Big single word · a label riding a line in the world (moves with the camera) · highlighter marks on a document · right-aligned block · annotation callouts with leader lines pinned to world points (dark label chips) · a number slammed in large and tilted · left-aligned closing line with an accent underline drawing in.

Word-by-word reveals (0.07–0.12 s stagger, ease-out, 30–60px rise). Type sizes at 1080 wide: headlines 96–150px, numbers 200–250px (but never into the right icon rail), annotations 36px mono.

## 4. Placement rules (9:16, Instagram/TikTok)

- Safe area: top 250px and bottom 420px are covered by platform UI; the right ~120px from y≈1000 to 1500 holds the action icons. All text inside x 90–990, y 250–1500.
- One left margin for every headline: 90px. Right-aligned blocks end at 990 (950 low on the frame).
- Text over busy imagery gets a dark scrim (gradient band) or sits in a chip.
- **Sources**: one consistent chip, bottom-left (x 90, y ≈1420): Geist Mono 28px, #B3B3B3, on rgba(17,17,17,.88) with a 2px #343437 border and 14px radius. Visible as long as the number is.

## 5. Blue and grain

One accent element per beat (ultramarine by default, another brand color when the beat's meaning calls for it — social-plus-illustration's `color-accents.md`) (the highlighter, the unread dot, the reaction, the underline); the glow follows it. No glow when a beat has no accent. Grain on for editorial.

## 6. Check

`scripts/contact_sheet.py cut.js --size 1080x1920 --times …` with one time per text moment and per beat; read every frame against the guides before handing over.

Example: `assets/examples/explainer-reel-push-ceiling.js` — "Push Notifications Have Hit a Ceiling" (camera world, six beats, annotations, source chips, foley score).
