# Inputs: what to ask for, and how

Ask for everything in one message to CS (or the customer) and build only once it is all in. The recordings decide most of the film's quality, so send the recording spec as it is written here.

## Recordings (send this to whoever records)

- **Portrait screen recordings from the live app**, one per feature, 2 to 5 features. iPhone or Android built-in screen recording is fine.
- **6 to 15 seconds each.** The scene runs as long as the recording; anything past 15 s is cut.
- **Start on the feature's screen**, not on the home screen or a menu. A short opening transition is trimmed automatically; a long one is not.
- **Pause on the feature for about 2 seconds** somewhere after the first second: that is where the highlight goes. A recording that never stops scrolling gets no clean highlight.
- **Real but shareable content:** no personal data, no private messages, no notification banners, Do Not Disturb on, full battery and signal if the status bar shows.
- **One continuous take, no edits**, no screen-recording indicator tapped mid-way.
- **Same device and appearance** (light or dark mode) for all recordings, so the screens match when they slide.

## Brand files

- **App icon:** the square store icon (1024 x 1024 PNG from the App Store or Play Store listing is ideal). Not the rounded version: the film draws the corners.
- **Wordmark:** SVG, white or single-colour for a dark background. If only a dark wordmark exists, ask for the white one; never recolour a logo without the customer's say-so.
- **Permission:** the customer agrees to their logo and app footage being used (CS usually has this with the customer story).

## Copy

- **Customer name** exactly as the brand writes it (Like:me, South Sydney Rabbitohs). The intro reads "<Customer> is live / with social.plus" unless showcase.json sets `headline`, e.g. `"How South Sydney Rabbitohs / *use* social.plus"` ("/" breaks the line, `*word*` takes the accent colour; a long line shrinks to fit).
- **Feature title:** 1 to 3 words, sentence case, the social.plus capability as the customer uses it (Communities, Community feed, Chat, Live streams, Events, Expert sessions).
- **Benefit line:** under 40 characters, what the member gets, no full stop ("Join experts and like-minded people").
- US English; `social.plus` lowercase even at the start of a line; no numbers that aren't in the customer story.
- **Quote:** only an approved quote, attributed "Name, Title, Company". Without one, the film ends on the logos.

## Optional settings in showcase.json

- `aspect`: `"9:16"` (default, Reels and Stories) or `"16:9"` (1920 x 1080 for websites, decks and YouTube). The 16:9 film keeps the reel's layout exactly (label above the phone, everything centred), scaled to 2/3 so the wider frame only adds space at the sides. It's a separate Motion film: run prep and build into its own out folder.
- `quote.who`: `"Name, Title\nCompany"`, which shows as two lines.
