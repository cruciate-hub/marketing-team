---
name: social-plus-motion
description: Motion design in the social.plus illustration system — subtle loops of static visuals (thumbnail/website/social loops exported as animated WebP or GIF), and story-driven explainer videos such as Instagram Reels, TikToks and LinkedIn videos built from a blog post in a Vox-style editorial manner (script, camera moves, kinetic typography, subtle sound effects). Use for any request to animate a social.plus visual, make a reel/short/explainer from an article, write a voiceover script for one, or export motion as WebP, GIF or MP4. Builds on social-plus-illustration (read it first).
---

# social.plus motion

You are the motion designer, sound editor and (for explainers) the scriptwriter. The visual language is **social-plus-illustration** — read its SKILL.md and references first. Motion adds time; it never changes the look.

## Two kinds of work

| | Loop | Explainer |
|---|---|---|
| What | A static visual made "a little bit alive" | A short film that tells a story, usually from an article |
| Length | 4–8 s, seamless | 15–60 s (Reels default 30 s) |
| Camera | locked | moves: push-ins, pull-backs, whip pans, dives |
| Text | none beyond the static's | kinetic type for key points only |
| Sound | none (GIF/WebP) | subtle SFX, room for a voiceover |
| Grain | only if the static is editorial | on when built from editorial content |
| Read | `references/loops.md` | `references/explainers.md` |

Both: `references/sound.md` for sound, `references/export.md` for files and sizes.

## Treatment

Grain follows social-plus-illustration's `treatments.md`: editorial (blog loops, reels built from a post, Vox-style) → grain; product, website, brand → clean. Motion grain is drawn on the fx canvas (alpha factor 0.15, 12 boils/s); always compare a motion frame with the static.

## Building on claude.ai

Use the Motion artifact type: a film with no scene list whose `film/script` sets `window.CUT` itself (`width`, `height`, `fps`, `duration`, `background: '#111111'`, `init`, `render(t)`, optional `score(S)`). Everything on screen is a pure function of `t`. Upload `figtree.woff2` and `geist-mono.woff2` from social-plus-illustration's `assets/fonts/` as film assets (families `figtree`, `geist-mono`). Examples in `assets/examples/` show the technique — never copy their layouts.

## Always check before handing over

Render frames locally (`scripts/contact_sheet.py` — draws the platform's safe zones) and look at every text moment and every beat. Fix placement, legibility and framing before the person sees it; they should never have to point out cropped text or unreadable sources.

## Logos

When the source is about named companies or technologies, their official logos appear (social-plus-illustration's `third-party-logos.md`): official files only, never drawn; upload each as a film asset (`assets/<name>` with its exact mime, e.g. `image/svg+xml`, read with `kit.assets.url('<name>')`). In an explainer they work as objects the camera visits — a tile wall to fly over, a badge that lands on a device.

## Copy

Brand is `social.plus`. On-screen and voiceover copy in US English; placeholder names American (`content-and-locale.md`). Every number comes from the source and carries a source chip on screen.
