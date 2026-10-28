# Avatar library: where people's photos come from

Every avatar photo in a social.plus illustration comes from one source, the graded faces in the social.plus design system's **Avatars** asset group. Never use stock sites, AI-generated faces, photos of real public figures or of social.plus staff and customers. This applies to every surface and every skill built on this one: blog thumbnails, in-blog images, motion, website, social.

## The library

The set lives in the social.plus design system (https://claude.ai/artifact/EtY7zLfKmoKRJVTpVjPAm7; `Artifact` `list` with `type` "Design System" finds it too), in its **Avatars** asset group: 37 people, each `<name>.jpg`, 320×320, already cut out of the grey background and graded dark, cool and slightly desaturated onto a dark ground. The group's card (`project/api/assets/Avatars.md`) lists every file with its asset id; `project/assets/Avatars/README.md` holds the rules and the casting notes (look, mood, which faces may be a large portrait). The file names are fictional first names, safe to use as on-screen names.

The faces live **only** in the design system. The marketing-team GitHub repository is public: never commit the faces, the source photos or a contact sheet to it.

## Which avatars use photos

- **Photos** for every avatar that shows a person at readable size: profile and post authors, leaderboard and member rows, comment previews, voter and avatar stacks, cursor owners. A face makes "people interacting" readable at 502px in a way a grey circle doesn't.
- **Grey gradient circles** (`linear-gradient(160deg, #939497, #414347)`) stay for texture-level avatars: inside a background pattern wall, or anything under ~40px at 1578px wide. They are also the placeholder while photos are being prepared.
- At most **one large portrait** (head-and-shoulders, about 160px or more) per image; small avatars may repeat as often as the composition needs.
- **Casting**: mix genders, ages and backgrounds across an image. Faces that smile fit community and engagement scenes; neutral faces suit moderation, trust or serious topics. Don't use the same faces as the most recent images on the same surface (look at the avatars on the recent canvases during the variety check).
- **Names**: the library's names (Olivia Rhye, Phoenix Baker…) and photographer credits never appear. Any name on screen is a fictional American placeholder (`content-and-locale.md`), and the delivery note says so.

## How to use them

1. **Read** the design system's Avatars card, `project/api/assets/Avatars.md`, and `project/assets/Avatars/README.md` (`Artifact` `read` with `path`, on the design system url).
2. **Pick** faces by the casting notes (mood, portrait OK, the notes column), mixing genders, ages and looks. Avoid the faces used in the most recent thumbnails (look at the avatars on the recent canvases during the variety check).
3. **Copy** them into the canvas with the `Artifact` tool: `publish`, `asset: true`, `url` = the canvas, `from_url` = the design system url, `asset_ids` = the chosen ids from the card (up to 10 per call). Nothing is downloaded or re-uploaded.
4. **Use** the returned `/_blob/<id>` urls in the markup (below). Never the design system's own ids: they only resolve on the design system.
5. **Before export**, read each avatar from the canvas **one at a time** (`Artifact` `read`, `url` = the canvas, `path` = the asset id; a multi-file `paths` read fails for asset ids) and save it in the `--assets` folder as `<blob id>.jpg`, next to any logo files.

## In the markup

A circle that crops to the face, so the graded ground reads as the avatar's background:

```html
<div style="width: 92px; height: 92px; flex: none; border-radius: 999px; overflow: hidden; background: #29292B">
  <img src="/_blob/<id>" alt="" style="width: 132%; margin: -3% 0 0 -16%; display: block">
</div>
```

In stacks, give each avatar a ring in the surface color (`border: 4px solid <card color>`, -18px overlap) as for grey avatars. Keep the photos as they come out of the script: no extra filters, borders in an accent color or glows. A photo never carries the accent.

## Adding new faces (maintenance only)

Only when the set needs more people. Not part of making an image.

- Work in a Cowork task **without** a Design canvas: Figma is blocked in Design canvas sessions.
- Review every face on magenta at 3x inside the 132% circle crop: no grey halos, no holes, no cut-off hair or ears.
- Settings may differ per face: `--hair-fix` for curly or loose hair, `--model birefnet-portrait` where the default model leaves grey in the hair (it needs about 14 GB of memory).
- Never share, commit or back up the source photos.
- New faces go **only** into the design system's Avatars group (upload, add the record to the index, add a casting row to `assets/Avatars/README.md`). Never into the marketing-team repository: it is public.

### The source library

- File: `❖ 370+ avatars and users library – Untitled UI (Community)`, https://www.figma.com/design/1u6Vs8rhhxBY3avtWCOjp5/?node-id=903-4176
- fileKey `1u6Vs8rhhxBY3avtWCOjp5`, page "Avatars" `903:4176`, frame "Avatar users" `903:11003`.
- The frame holds 9 groups of the same 14 people shown 3 times: row 1 on the original photo background, row 2 on pastel, **row 3 on neutral light grey**. **Always take people from row 3**: the flat grey cuts out cleanly.
- Row 3 of each group (each row's 14 children are `_Avatar image` instances, 320×380: the photo is the top 320×320, the library name and photographer credit sit underneath and are cropped off):

  | Group | Row 3 node | Instance ids |
  |---|---|---|
  | 1 | `903:11035` | `903:11036`–`903:11049` |
  | 2 | `903:11081` | `903:11082`–`903:11095` |
  | 3 | `903:11127` | `903:11128`–`903:11141` |
  | 4 | `903:11173` | `903:11174`–`903:11187` |
  | 5 | `903:11219` | `903:11220`–`903:11233` |
  | 6 | `903:11265` | `903:11266`–`903:11279` |
  | 7 | `903:11311` | `903:11312`–`903:11325` |
  | 8 | `903:11357` | `903:11358`–`903:11371` |
  | 9 | `903:11403` | `903:11404`–`903:11417` |

  In each row the instances run left to right in id order. If an id ever stops resolving (the library was edited), `get_metadata` on the row node lists its children.

### How to pull, cut out and grade

1. **Pick.** With the Figma MCP: `create_session` (fileKey above), then `get_screenshot` on a row 3 node (`maxDimension` 1400, `enableBase64Response: true`) to see the 14 faces and choose.
2. **Pull each face.** `get_screenshot` on the person's instance id with `maxDimension: 380` and `enableBase64Response: true`. Figma's asset URLs (`www.figma.com/api/mcp/asset/…`) are often blocked from a sandbox, so don't rely on `curl`: the inline image is saved by the harness as a PNG, and the result names its path ("source: …"). Copy that file to `avatars_raw/<name>.png`, using a short name of your own (not the library name). Where `curl` to the URL works, that's fine too.
3. **Cut out and grade** with `scripts/prepare_avatars.py`:
   ```
   python3 <skill>/scripts/prepare_avatars.py avatars_raw/ avatars/ --hair-fix loki,kelly
   ```
   It crops the 320×320 photo, removes the grey background with `rembg` (`u2net_human_seg`; `pip install rembg`, and the model downloads on first run), cleans the light fringe, closes holes in the mask, and grades the person **dark, cool and slightly desaturated** (saturation 0.62, brightness 0.84, contrast 1.06, a 7% blend toward `rgb(70,90,150)`) onto a dark ground (#1A1A1A with a soft #343437 lift at the upper left). Output: `avatars/<name>.jpg`, 320×320, plus `avatars_sheet.png` to check them side by side. Pass `--hair-fix` for people with curly or loose hair, where grey shows through the curls. Look at the sheet before using them: no grey halos, no holes in faces.
4. **Upload** the JPGs as canvas assets (Artifact `publish`, `asset: true`, `file_paths`) and use the returned `/_blob/<id>` urls. To export with `blog-thumbnails`' script, copy each JPG to a local folder as `<blob id>.jpg` and pass it as `--assets`.
