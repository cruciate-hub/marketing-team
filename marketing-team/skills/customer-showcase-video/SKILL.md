---
name: customer-showcase-video
description: "The social.plus customer showcase video: a 9:16 film (with an optional 16:9 version) in which the customer's app icon opens into a phone, two to five of their features play with one highlight each, and the official social.plus logo lands beside theirs, with an optional approved quote and an ElevenLabs v4 voiceover. One fixed look (the approved Like:me video, October 2026); only the length changes, following the customer's screen recordings or screenshots. Use for any request to make a customer video, showcase reel, launch video, '[customer] is live with social.plus' video or a video for a customer story, even when the format isn't named. Built with the Motion artifact type."
---

# Customer showcase video

Every customer gets the same video. The look, motion, type, music and logo lockup are fixed and live in `template/`; never redesign them per customer. What changes is the material (their icon, wordmark, recordings, feature names) and, from it, the length: each feature's scene runs as long as its recording (5 to 15 s), with 2 to 5 features, so a film runs about 25 to 60 s.

The reference is the Like:me video (October 2026). Its decisions, from Amadeus's review, are the rules below.

## How to fetch reference files

<!-- FETCH-BLOCK:START v2 -->
Reference files live in the public `cruciate-hub/marketing-team` GitHub repo. Fetch them by shallow-cloning the repo once per session, then loading individual files with `cat`. Use this exact pattern at the start of every skill that needs reference files:

    REPO="${MT_REPO:-/tmp/cruciate-hub-marketing-team}"
    REMOTE="https://github.com/cruciate-hub/marketing-team.git"
    # Create the clone only when the path is absent. Never delete an existing
    # directory: it may be a working checkout holding un-pushed local commits.
    if [ ! -e "$REPO" ]; then
      git clone --depth 1 --quiet "$REMOTE" "$REPO" || true
    elif git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
      # Refresh, but do NOT ignore a failed pull. Silently serving stale
      # content is the exact bug this block exists to prevent.
      git -C "$REPO" pull --ff-only --quiet 2>/dev/null \
        || echo "Note: could not refresh $REPO; verifying existing content below." >&2
    fi
    # Mechanical integrity gate. Do not skip. Probes core files across several
    # top-level dirs so a missing, corrupt, or partial clone stops the skill
    # here instead of letting it read incomplete content and draw wrong conclusions.
    miss=""
    for f in brain.md messaging/brain.md messaging/terminology.md messaging/tone.md design-system/brain.md; do
      [ -s "$REPO/$f" ] || miss="$miss $f"
    done
    if ! git -C "$REPO" rev-parse HEAD >/dev/null 2>&1 || [ -n "$miss" ]; then
      echo "Fetch failed: clone at $REPO is unreachable or incomplete.${miss:+ Absent files:$miss}" >&2
      echo "Check your network. If the clone is corrupt and holds no local work, run  rm -rf \"$REPO\"  then re-run." >&2
      echo "(If \$MT_REPO points at your own checkout, rescue its changes first; this never auto-deletes it.)" >&2
      exit 1
    fi

    # Overlay the live website inventories. The auto-generated pages-*.json
    # are committed to the `site-data` branch (bot commits stay off main);
    # main only carries a point-in-time snapshot. Restricting the overlay to
    # pages-*.json keeps the clone fast-forwardable on the next session's pull.
    if git -C "$REPO" fetch --depth 1 --quiet origin site-data 2>/dev/null; then
      git -C "$REPO" checkout --quiet FETCH_HEAD -- 'website/pages-*.json' 2>/dev/null \
        || echo "Note: site-data overlay failed; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    else
      echo "Note: could not fetch site-data; website/pages-*.json are the main-branch snapshot (may be stale)." >&2
    fi

After the clone exists, read files with `cat "$REPO/<path>"`. Examples: `cat "$REPO/brain.md"`, `cat "$REPO/messaging/terminology.md"`.

The integrity gate above fails loud rather than serving partial content, and it never deletes `$REPO` (it can hold un-pushed local work). To make skills read your own local edits, point `MT_REPO` at your working checkout before running them.

The Bash tool truncates large stdout when the output exceeds the harness's token/byte cap (observed at ~50 KB in Cowork; varies by environment). When this happens the harness emits one of these signals — both mean the same thing:
- `Output too large (NkB). Full output saved to: …` followed by a short preview, OR
- `Error: result (N characters) exceeds maximum allowed tokens` with no preview, just a sidecar-file pointer.

In either case, the rest of the file is invisible to you in-call. Most files in this repo are small enough that `cat` returns them in full and you never see either signal. **If you do see either form, never proceed using the partial output as if it were the whole file** — switch to one of the patterns below.

- **Truncated markdown** (you saw either truncation signal above) — read in line-range chunks instead. First check the total line count: `wc -l "$REPO/<path>"`. Then read each chunk:

      sed -n '1,250p'     "$REPO/<path>"
      sed -n '251,500p'   "$REPO/<path>"
      sed -n '501,$p'     "$REPO/<path>"

  Each ~250-line chunk fits under the preview cap. Concatenate the chunks mentally. For files much larger than 750 lines, add more chunks at 250-line intervals until you reach the total.

  **If a chunk itself comes back as a truncated preview** (output above the harness's display cap — visible as an "Output too large" or similar marker, with the rest spilled to a file you can't see in-call), halve the chunk size and retry. For example, swap `sed -n '1,250p'` for `sed -n '1,125p'` then `sed -n '126,250p'`. Repeat until each chunk lands in full. Never proceed using a truncated chunk as if it were complete.

- **Large JSON inventories** (`website/pages-*.json`, up to 228 KB) — never `cat` raw. Process with `python3` or `jq` and emit only the fields you need:

      python3 -c "import json; d=json.load(open('$REPO/website/pages-blog.json')); print(len(d['pages']))"
      jq '.pages[].url' "$REPO/website/pages-blog.json"

  Some skills ship helper scripts that already follow this pattern (e.g. `marketing-team/skills/aeo-content/scripts/duplicate_check.py`).

  **Degraded-inventory guard.** The pages-*.json files are auto-generated; a generation failure can leave a file syntactically valid but empty or missing pages. After loading any of them, check `_meta.errors` and `len(pages)`:

      python3 -c "
      import json; d=json.load(open('$REPO/website/pages-industry.json'))
      errs = d.get('_meta',{}).get('errors') or []
      print(len(d.get('pages',[])), 'pages;', len(errs), 'extraction errors', errs)"

  If `pages` is empty, or `_meta.errors` is non-empty, the inventory is degraded: name the affected file and the missing paths in your output, scope any 'site-wide' claims accordingly, and never treat an empty inventory as 'this section has no pages'.

Note: Claude Code's `Read` tool can't reach files in `$REPO` — Cowork sandboxes Read to connected directories and `/tmp` is not connected by default. Use the `cat` / `sed` / `python` patterns above.

Validate every file before using it:
- Markdown: content must start with `#`
- JSON: content must start with `{` or `[`
- HTML: content must start with `<`
- Content must be non-empty

If anything fails — clone error, missing file, empty content, or wrong format:
- Do NOT reconstruct from memory or training data.
- Do NOT fall back to WebFetch or any other tool.
- Stop immediately and respond with exactly this line:

  `Fetch failed: <path>. Please check your network connection and rerun.`
<!-- FETCH-BLOCK:END v2 -->

This skill reads two files from the clone: the official social.plus logo for dark backgrounds, `design-system/assets/media/66fe6169153dc88a03557da6_29a5aaff9e31043f2175762ac854a9e5_logo.svg` (rules in `design-system/foundations/logo/foundation.md`), and `design-system/figtree.woff2`. `build_film.py` reads them from `$MT_REPO`.

## Fixed rules (from the approved Like:me video)

- **Intro:** the customer's app icon lands in a squircle with "<Customer> is live / with social.plus" under it ("live" in the accent), pulses twice, then opens into the phone like an app launch. For a customer-story film the headline can be the film's own, e.g. "How South Sydney Rabbitohs / *use* / social.plus" (`headline` in `showcase.json`: "/" breaks the line, `*word*` takes the accent).
- **Phone and label:** one block, centred vertically: feature title and one benefit line above a still, front-on phone. The phone never moves, zooms or floats.
- **No zooms:** the UI inside the phone is never scaled or cropped. Emphasis is one highlight per feature: everything on the screen dims for about a second except the part the label names, placed where the recording rests.
- **Between features:** the next screen slides in over the previous one's last frame, like in-app navigation.
- **Before the logos:** the phone simply fades out in place, at full size.
- **Lockup:** the official social.plus logo (colour mark, white wordmark, from the design system, never redrawn) and the customer's white wordmark side by side, a white x between them, the gap on each side the social.plus logo's clear space. The x draws, then both logos slide out from behind it on the music's downbeat.
- **Quote card:** only with an approved, attributed quote (a quote published in the customer story counts). Never a placeholder in a finished film. The credit is two lines: "Name, Title" over "Company".
- **16:9 version:** the same film with the same placement, scaled to 2/3 and centred, so the wider frame only adds space at the sides. Never a different layout.
- **Brand:** `social.plus`, lowercase, always. Figtree (static 500 and 700 cut from `design-system/figtree.woff2`), dark ground `#111111`, one soft blue glow, accent `#6E9BFF`, as in the approved film.
- **Export-safe material:** recordings are always re-encoded by `scripts/prep_clips.py` (some phone recordings open with an empty edit that exports as a white screen), and every held frame is a still image, never a paused clip.

## Inputs

Collect these before building; `references/inputs.md` has the recording spec and copy rules.

| Input | From | Notes |
|---|---|---|
| Customer name as written on screen | CS / the customer story | e.g. "Like:me" |
| App icon | App Store or Play Store listing, or the customer | square PNG, JPG or WebP, ideally 1024 px |
| Wordmark, white version | the customer | SVG; ask for the white or single-colour version for dark backgrounds |
| 2 to 5 portrait screen recordings, or screenshots | CS or the customer | recordings: one feature each, 6 to 15 s, pausing on the feature for 2 s. Screenshots: 2 or 3 per feature, in tap order |
| Per feature: title and one benefit line | you, from the story | title 1 to 3 words, line under 40 characters |
| Customer story URL | the website | for the voiceover script |
| Quote (optional) | the customer, approved | text plus "Name, Title\nCompany" (two lines) |
| Headline (optional) | Amadeus / the brief | replaces "<Customer> is live with social.plus" |
| 16:9 version (optional) | the brief | for websites, decks and YouTube |

## Workflow

Scripts need ffmpeg, numpy, Pillow, fontTools with brotli and Playwright. Work in a scratch folder; `$SKILL` is this skill's folder.

0. **Screenshots instead of recordings:** first turn them into tap-through clips with `python3 $SKILL/scripts/screens_to_clips.py screens.json clips` (the spec and the transitions are in the script's header). Pick the screens per feature from a contact sheet, fit them (no crop: padded at the top to the phone's shape), place the tap dots and pick the highlight from `clips/screens/grid_*.png`, then use `clips/<name>.mp4` as each feature's `src`. Fade for a tab or state change, push for opening something, scroll for a longer page. A motion the screenshots imply (a bottom sheet rising, a chat message arriving) can be built frame by frame from the screenshot itself; say so to the person, and offer to swap in a real recording.

1. **Write `showcase.json`** next to the material:

   ```json
   {
     "customer": "Like:me",
     "iconSrc": "src/icon.png",
     "wordmarkSrc": "src/wordmark-white.svg",
     "lockup": { "wordmarkH": 48 },
     "features": [
       { "id": "f1", "title": "Communities", "line": "Join experts and like-minded people", "src": "src/communities.mp4" },
       { "id": "f2", "title": "Community feed", "line": "Expert posts, likes and comments", "src": "src/feed.mp4" }
     ],
     "quote": null
   }
   ```

   Feature ids are `f1` to `f5`, in film order. Optional keys: `headline`, `aspect` (`"16:9"`) and `title` (the film's name); see `references/inputs.md`.

2. **Prepare the recordings:** `python3 $SKILL/scripts/prep_clips.py showcase.json out`. It re-encodes each recording, trims a recording that opens on another screen, sets each scene's length, finds where the screen rests and suggests `focus.t` (when the highlight starts, in scene seconds). It writes `out/review/<id>-sheet.png` (one frame a second) and `out/review/<id>-grid.png` (the frame the highlight sits on, with a measuring grid in clip pixels). Read `out/review/prep.json`.
   - Look at each sheet. Is it one feature, and does it start on that feature's screen? Is the trim right?
   - Look at each grid and set `focus.rect` = `[x, y, w, h, radius]` in clip pixels: the one card, post or row the label names, edge to edge, with the radius of its corners. Pick a part that shows the label's promise (the community card for "Communities", the post with its likes for "Community feed").
   - A feature with no resting moment (`focus_t_scene_time: null`): ask for a recording that pauses on the feature, or set `focus.t` by hand where it moves least.

3. **Build:** `MT_REPO="$REPO" python3 $SKILL/scripts/build_film.py showcase.json out`. It writes every store document to `out/film/docs/`, the batch to `out/film/batch.json` and the files to upload to `out/film/uploads.json`, and prints the film's length.

4. **Check before the person sees it:** `python3 $SKILL/scripts/preview.py out --key` renders the moments that matter to `out/review/stills.png`. Look at every still: the highlight sits on the part it names, labels are whole, the slide shows the right screens, the lockup is balanced. If the customer's wordmark looks heavier or lighter than the social.plus logo, change `lockup.wordmarkH` (and `wordmarkDy` to nudge it vertically) and rebuild.

5. **Make the film** (claude.ai):
   - Create a Motion film from the Motion artifact type, named "<Customer> x social.plus showcase". The look, colours and length are settled by this skill, so the type's style questions are not asked.
   - Upload every file in `uploads.json` to the film's asset store (Artifact `publish` with `url` = the film, `asset: true`, `file_paths`, up to 25 per call). Then write one `assets/<name>` document per file: `{"ref": "<the upload's /_blob/ url>", "mime": <its mime>, "w", "h"}`, in one `ArtifactData` batch.
   - Write the documents: one `ArtifactData` batch with the entries of `out/film/batch.json` as they are (`film/meta` first, `film/script` last). A new film needs no `if_version`.
   - Open the film and tell the person it's ready; Export on the film's page gives the MP4.

6. **Voiceover** (optional): write the script with `references/voiceover.md` (a Claude Doc, paste-ready for ElevenLabs v4). When the person sends back the take as one MP3, run `python3 $SKILL/scripts/place_voiceover.py out take.mp3`. It cuts the take at its pauses into one line per beat, checks each fits its window, and writes `out/assets/vo-*.mp3`, `out/film/voice.json` and `out/film/docs/modules/narration.js.json`. Upload the lines (mime `audio/mpeg`), write their `assets/` documents, then set `modules/narration.js`. The music dips under the voice, and Export includes it.

## A 16:9 version

Copy `showcase.json` with `"aspect": "16:9"` and a `title` ending "(16:9)", run `prep_clips.py` and `build_film.py` into a second out folder, check it with `preview.py`, and make it as its own Motion film (a film's aspect can't change). Same headline, copy and timing, so one voiceover take serves both.

## Changing a finished film

Edit `showcase.json`, run `build_film.py` again, and write only the documents that changed (each with the `if_version` from your last read of it). A new or replaced recording goes through `prep_clips.py` first. Never edit the generated scene code by hand: change `template/` here instead, so every future film gets the change.
