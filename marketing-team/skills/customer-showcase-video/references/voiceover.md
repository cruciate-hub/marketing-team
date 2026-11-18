# Voiceover (ElevenLabs v4)

One calm narrator, one line per beat, written from the customer story. The person generates it in ElevenLabs as one take; `scripts/place_voiceover.py` cuts it at its pauses and places each line on its beat.

## Beats and how much fits

Build the film first: the beats come from its scene lengths (`out/film/docs/modules/scenes.json.json`).

| Beat | Starts | Ends before | Says |
|---|---|---|---|
| Intro | 0.4 s | the first feature's start + 0.8 s | who the customer is, and that they are live with social.plus |
| Each feature | its scene's start + 0.8 s | the next beat | what members do there, matching the label and the highlight |
| Close | 1.6 s before the logos | the film's end (or the quote card) | one line on what it adds up to, ending "powered by social.plus" |

Words per beat: about 2.5 x the beat's seconds, minus a breath (the Like:me intro had 4.4 s and 12 words). Leave the quote card unvoiced: viewers read it.

## Writing rules

- Facts only from the customer story: the customer's own description, what their members do, the features they use. No numbers the story doesn't have.
- Short spoken sentences, US English, no jargon, no claims the picture doesn't show.
- Each feature beat describes what the highlight shows, so the eye and the ear land together.
- Spell names for the voice, not the eye: write "Like me" for Like:me and "social plus" for social.plus, so the model never reads a colon or a dot. If a name still comes out wrong, Eleven v4 reads IPA between slashes (/laɪk miː/).

## The script doc

Deliver it as a Claude Doc: a brief (voice, pace, open questions), the timed table (beat, starts at, on screen, line, window), then one paste-ready block for ElevenLabs:

```text
[warm, confident] Like me — Brazil's holistic health app — is now live with social plus.

[long pause] [warm, conversational] Members join communities curated by health and wellbeing specialists... and meet people who share their goals.

[long pause] Experts post in the community feed. Members like, comment, and keep the conversation inside the app.

[long pause] Specialists announce live sessions in the forum — with replays for anyone who missed one.

[long pause] [warm, assured] One app for their health, their experts and each other — [confident, smiling] powered by social plus.
```

- One delivery tag opens the take and carries through until the next; change it only where the tone changes.
- Every beat after the first starts with `[long pause]`: those gaps are where the take is cut, so they must be the longest silences in it. Inside a beat use only full stops, dashes and ellipses, never a pause tag. v4 ignores SSML break tags.

## Settings to give the person

| Setting | Value |
|---|---|
| Model | Eleven v4 |
| Voice | one warm, mid-range US English narrator from the Voice Library |
| Stability | 0.5; lower for more expression, higher if takes drift |
| Speed | 1.0; 0.95 to 1.05 if a beat runs long (the range is 0.7 to 1.2, extremes cost quality) |
| Output | MP3, 44.1 kHz, 128 kbps; generate two or three takes and keep the best |

## Placing the take

`python3 $SKILL/scripts/place_voiceover.py out take.mp3` (after `build_film.py`). If it finds too few pauses, retry with `--noise -30` or `--min-gap 0.25`, or ask for a take with the pause tags in place. A beat that runs into the next is reported: trim words or raise Speed for that line and regenerate. Then upload `out/assets/vo-*.mp3` (mime `audio/mpeg`, each under 256 KiB and 30 s, which the player requires), write their `assets/` documents, and set `modules/narration.js` from `out/film/docs/modules/narration.js.json`. After the voice is in, nudge a feature's `focus.t` if its highlight should land on a particular word.
