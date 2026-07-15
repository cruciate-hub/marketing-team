---
name: video-to-gif-and-webp
description: Create or optimize animated .webp and .gif files from video or existing animated images. Trigger when the user wants to convert a video clip into an animated image, optimize an existing gif or webp, resize an animated image for a specific use case, or convert between gif and webp. Mentions like "make a webp from this video", "gif from YouTube", "animated thumbnail", "video loop", "convert this clip", "webp from video", "gif for email", "optimize this gif", "resize this webp", "convert gif to webp", or drags/references a video or animated image file. Also trigger when the user mentions webinar thumbnails, mega menu images, product update talking heads, customer story loops, or newsletter gifs.
---

# Video to GIF and WebP

Turn a video clip or existing animated image into an optimized .webp or .gif — ready for the target use case.

## Tone

Keep it friendly and non-technical. The user never sees ffmpeg flags, frame rates, or quality numbers. Open with something like:

> "Don't worry about the technical side — I'll take care of that. Just help me with a few things."

## Input sources

This skill handles three types of input:

1. **YouTube URL** — downloads only the needed clip
2. **Local video file** — mp4, mov, etc.
3. **Existing animated webp or gif** — optimize, resize, or convert format

When the input is already an animated image (not a video), skip the timestamp question — the whole file is the source.

## Guided intake

Ask these questions before doing anything. Use the AskUserQuestion tool to present them cleanly. Skip questions that don't apply (e.g. no timestamp question for existing animated images).

### 1. Source

> Paste a YouTube link, or drag a video file right into this chat. Already have an animated webp or gif? That works too.

### 2. The moment (video input only)

> Which part of the video do you want? Just give me a start and end time, like 1:47 to 1:51.

The user must provide exact timestamps. Do not offer to browse or pick frames.

### 3. Format

- **.webp** — best for the website, small and sharp
- **.gif** — for email newsletters, since most email clients still can't handle .webp

When .gif is selected, tell them: "GIFs are bigger than .webp at the same quality, so I'll find the sweet spot between looking good and keeping the file size email-friendly."

### 4. What's it for?

All pixel sizes are 2x retina — the display size is half. Don't mention retina to the user, just use the correct pixel values.

- **Webinar** — generates both versions automatically:
  - Mega Menu thumbnail: 502x283px, .webp
  - Poster Image: 640x360px, .webp
- **Mega Menu thumbnail** (standalone): 502x283px
- **Product update talking head** — 144x144px square (displays at 72x72)
- **Customer story card / blog thumbnail** — 640px wide
- **Sidebar widget / small UI loop** — 480px wide
- **Mobile card** — 320px wide
- **Email newsletter** — 750px wide (matches our MailerLite container)
- **Something else** — ask for the width in pixels

When the format is .gif and the use case is "Email newsletter", apply email-specific defaults automatically:
- 750px max width
- 10–12 fps
- Target under 500KB
- Duration: keep it 2–5 seconds

### 5. Max file size

- **200KB** — Webflow CMS images, fast page load
- **500KB** — hero accents, email newsletters
- **1MB** — full-width background loops
- **Something else** — ask for the max in KB

## Dependency check

Before running the pipeline, verify the required tools are installed. Run these checks silently — only surface them to the user if something is missing.

**Always needed:**
- `ffmpeg` — frame extraction and video processing
- `img2webp` — animated .webp assembly (part of the `webp` brew package)

**Needed for YouTube input:**
- `yt-dlp` — video download

**Optional (better GIF quality):**
- `gifski` — high-quality GIF encoding with temporal dithering

If anything is missing, tell the user plainly:

> "I need a couple of tools installed to do this. Want me to run `brew install ffmpeg webp yt-dlp`? It'll take a minute or two."

Only list the missing ones in the command. Wait for approval before installing.

## Pipeline

### Handling animated webp input

**Critical:** ffmpeg cannot read animated webp files. Do NOT try to use ffmpeg directly on them — it will fail or produce empty output. Also do NOT try to extract individual frames with `webpmux` and reassemble — animated webp uses delta frames where each frame only contains changed pixels. Extracting individual frames gives you partial images that look scrambled when reassembled.

**The correct approach:** If the source is an animated webp, first convert it to GIF as an intermediate using any tool that properly composites frames, then work from the GIF through the normal pipeline. If a GIF version of the same content already exists alongside the webp, use that directly.

### Step 1 — Get the source material

**YouTube URL:**
```
yt-dlp --download-sections "*START-END" -f "bestvideo[height<=720]" -o "/tmp/vtgw_clip.%(ext)s" "<URL>"
```
Downloads only the needed section. No full video download.

If yt-dlp fails with a bot/sign-in error, automatically retry with browser cookies:
```
yt-dlp --cookies-from-browser chrome --download-sections "*START-END" -f "bestvideo[height<=720]" -o "/tmp/vtgw_clip.%(ext)s" "<URL>"
```
If that also fails, tell the user simply: "YouTube is being difficult — could you download that clip yourself and drop it here? I'll take it from there."

**Local video file:**
```
ffmpeg -y -ss START -t DURATION -i "INPUT_FILE" -c copy /tmp/vtgw_clip.mp4
```

**Existing animated gif:**
Use directly as input — no conversion needed. Copy to /tmp/vtgw_source.gif.

**Existing animated webp:**
Convert to GIF intermediate first (see "Handling animated webp input" above). If a GIF version exists alongside, use that instead.

### Step 2 — Extract frames

```
ffmpeg -y -i INPUT -vf "fps=FPS,scale=WIDTH:-2:flags=lanczos" /tmp/vtgw_frames/f_%04d.png
```

- FPS: 12 for email GIFs, 15 for .webp
- WIDTH: from the use case selection
- For square outputs (e.g. 144x144), use `scale=144:144:flags=lanczos,setsar=1` — but only after the aspect ratio check passes
- `-2` ensures height is divisible by 2

### Step 3 — Assemble

**For .webp:**
```
img2webp -loop 0 -lossy -q QUALITY -m 6 -d FRAME_DELAY /tmp/vtgw_frames/f_*.png -o OUTPUT.webp
```
- Start with `-q 80`
- `-d` = frame delay in ms (e.g. 67ms for 15fps, 83ms for 12fps)

**For .gif (with gifski):**
```
gifski --fps FPS --width WIDTH --quality 90 /tmp/vtgw_frames/f_*.png -o OUTPUT.gif
```

**For .gif (without gifski — two-pass palette method):**
```
ffmpeg -y -i INPUT -vf "fps=FPS,scale=WIDTH:-2:flags=lanczos,palettegen=max_colors=128:stats_mode=diff" /tmp/vtgw_palette.png
ffmpeg -y -i INPUT -i /tmp/vtgw_palette.png -lavfi "fps=FPS,scale=WIDTH:-2:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle" OUTPUT.gif
```

### Step 4 — Auto-iterate to hit file size target

1. Check output file size
2. If over target: reduce quality by 10, re-run Step 3
3. If still over after q=50: reduce fps by 2, re-run from Step 2
4. If still over: reduce dimensions by 20%, re-run from Step 2
5. Report final file size and dimensions to the user

Never expose the iteration to the user. Just say something like: "Optimizing..." and deliver the result.

### Step 5 — Cleanup

Remove all temp files:
```
rm -rf /tmp/vtgw_frames/ /tmp/vtgw_clip.* /tmp/vtgw_source.* /tmp/vtgw_palette.png
```

Always clean up, even if the pipeline fails partway through.

## Multi-output use cases

When the use case produces multiple files (e.g. Webinar → two versions), run the pipeline once for frame extraction at the largest dimension, then assemble separately for each target size. Don't download or extract frames twice.

## File naming

**Output filenames must always be under 100 characters.** If the source filename is long, truncate it at a natural word boundary to make room for the suffix. Keep enough of the name to stay recognizable.

When the input is an existing file, save next to the source file, using the original filename (truncated if needed) with `-optimized` appended. Add a suffix for the intended use:
- `_website` for .webp output
- `_email` for .gif output

Examples:
- `product-update-template-optimized_website.webp`
- `product-update-template-optimized_email.gif`
- `whats-new-in-social-plus-march-2026-optimized_website.webp`

When creating from a YouTube video (no source file to sit next to), name descriptively and save to the current working directory:
- `webinar-megamenu-502x283_website.webp`
- `newsletter-loop-750w_email.gif`

Never dump output files in random locations — always co-locate with the source.

## Aspect ratio check

Before resizing, compare the source proportions to the target dimensions. A few pixels off from rounding is fine — don't flag that. But if the proportions are genuinely different (e.g. a square video going into a wide target), **don't silently stretch or squeeze the image.** Tell the user simply:

> "Your image is [square/wide/tall] but the target size is [different shape]. If I resize it as-is, it'll look stretched. I can either crop it to fit, or adjust the size to keep the original shape. Which do you prefer?"

Never assume — always ask. Keep the explanation simple, avoid jargon like "aspect ratio."

## What NOT to do

- Never use `ffmpeg -c:v libwebp` directly for animated .webp output — produces inferior results. Always use frames → img2webp.
- Never use `ffmpeg` to read animated .webp input — it can't. Convert to GIF first.
- Never extract animated webp frames with `webpmux` for reassembly — delta frames produce scrambled output.
- Never try to pick or suggest timestamps — the user provides them.
- Never expose technical details (fps, quality numbers, compression flags) to the user.
- Never silently stretch or squeeze an image to fit target dimensions.
- Never leave temp files behind in /tmp.

## Reporting results

When done, tell the user:
- What file(s) were created and where
- The file size of each
- The dimensions of each

Keep it short. One or two lines per file.
