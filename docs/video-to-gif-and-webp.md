# Video to GIF and WebP

Claude skill for creating or optimizing animated .webp and .gif files from YouTube videos, local video files, or existing animated images.

Handles the full pipeline — downloading, frame extraction, assembly, and size optimization — behind a friendly, non-technical guided intake. The user never sees ffmpeg flags or quality numbers.

## What it does

- Accepts YouTube URLs, local video files (mp4, mov), or existing animated webp/gif files as input.
- Downloads only the needed clip section from YouTube (not the full video), with automatic cookie fallback when YouTube blocks.
- Converts animated webp to GIF intermediate before processing (ffmpeg cannot read animated webp; webpmux delta frame extraction produces scrambled output).
- Extracts frames with lanczos scaling, assembles with `img2webp` (webp) or two-pass palette method (gif).
- Auto-iterates quality, fps, and dimensions to hit a target file size — no manual back-and-forth.
- Checks aspect ratio before resizing — warns the user in plain language if proportions don't match, never silently stretches.
- Names output files with `_website` / `_email` suffix and co-locates them next to the source file.
- Cleans up all temp files after every run.

## When it triggers

Any request to create or optimize an animated image from video. Trigger phrases include "make a webp from this video", "gif from YouTube", "animated thumbnail", "video loop", "convert this clip", "webp from video", "gif for email", "optimize this gif", "resize this webp", "convert gif to webp", or dragging/referencing a video or animated image file. Also triggers on webinar thumbnails, mega menu images, product update talking heads, customer story loops, or newsletter gifs.

## Guided intake (5 questions)

1. **Source** — YouTube link, local video file, or existing animated webp/gif
2. **The moment** — start and end timestamps (video input only)
3. **Format** — .webp (website) or .gif (email newsletters)
4. **What's it for?** — preset dimensions per use case:
   - Webinar (two outputs: mega menu 502x283 + poster 640x360)
   - Mega Menu thumbnail (502x283)
   - Product update talking head (144x144 square, 2x retina)
   - Customer story card / blog thumbnail (640px wide)
   - Sidebar widget / small UI loop (480px wide)
   - Mobile card (320px wide)
   - Email newsletter (750px wide, matching MailerLite container)
   - Custom dimensions
5. **Max file size** — 200KB / 500KB / 1MB / custom

## Dependencies

Installed via Homebrew. The skill checks silently and only asks to install if something is missing.

- `ffmpeg` — always needed
- `img2webp` (from `webp` package) — always needed
- `yt-dlp` — needed for YouTube input only
- `gifski` — optional, better GIF quality

## What it does NOT do

- Does not pick or suggest timestamps — the user must provide them.
- Does not use `ffmpeg -c:v libwebp` for animated webp (inferior results).
- Does not read animated webp directly with ffmpeg (unsupported).
- Does not extract animated webp frames with webpmux for reassembly (delta frames scramble).

## Files

- `SKILL.md` — full pipeline, guided intake, presets, and anti-patterns
