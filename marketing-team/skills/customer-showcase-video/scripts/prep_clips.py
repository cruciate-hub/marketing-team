#!/usr/bin/env python3
"""Prepare a customer's screen recordings for the showcase film.

For each feature in showcase.json (its "src" recording):
  - re-encode to an export-safe MP4: starts at 0 (no empty edit list), keyframe every 10 frames,
    no B-frames, 30 fps, no audio, faststart, at most 640 px wide (never upscaled)
  - suggest a "trim" when the recording opens on a transition from another screen
  - set the scene length from the recording (5 to 15 s)
  - find where the screen rests (no scrolling) and suggest when the highlight plays
  - write <id>-first.webp and <id>-last.webp (the held frames), a 1 fps contact sheet and a
    measuring grid of the frame the highlight sits on, to choose its rectangle

Usage: python3 prep_clips.py showcase.json OUT_DIR
Writes OUT_DIR/assets/*, OUT_DIR/review/*, and updates showcase.json in place (clip, clipW, clipH,
dur, trim if unset, focus.t if unset). Needs ffmpeg/ffprobe, numpy and Pillow.
"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

FPS = 30
MAX_W = 640
MIN_DUR, MAX_DUR = 5.0, 15.0


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def probe(path):
    out = run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
               'stream=width,height:format=duration', '-of', 'json', path]).stdout
    d = json.loads(out)
    return d['streams'][0]['width'], d['streams'][0]['height'], float(d['format']['duration'])


def encode(src, dst):
    w, h, _ = probe(src)
    tw = min(MAX_W, w) // 2 * 2
    run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-an',
         '-vf', f'setpts=PTS-STARTPTS,fps={FPS},scale={tw}:-2:flags=lanczos',
         '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-profile:v', 'high',
         '-bf', '0', '-g', '10', '-keyint_min', '10', '-sc_threshold', '0', '-movflags', '+faststart', dst])
    return probe(dst)


def frames_gray(path, w, h):
    raw = run(['ffmpeg', '-v', 'error', '-i', path, '-f', 'rawvideo', '-pix_fmt', 'gray', '-']).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32)


def frame_rgb(path, n):
    """Frame number n of a clip (exact, by index)."""
    import io
    raw = run(['ffmpeg', '-v', 'error', '-i', path, '-vf', f'select=eq(n\\,{int(n)})', '-frames:v', '1',
               '-f', 'image2pipe', '-vcodec', 'png', '-']).stdout
    return Image.open(io.BytesIO(raw)).convert('RGB')


def motion(f):
    """Per-frame change in the content area (between status/header bar and tab bar)."""
    n, h, _ = f.shape
    a, b = int(h * 0.09), int(h * 0.92)
    d = np.abs(np.diff(f[:, a:b], axis=0)).mean(axis=(1, 2))
    return np.concatenate([[0.0], d])  # motion[i] = change into frame i


def rest_windows(m, thr=1.5, min_len=1.2):
    """Clip-time windows where the screen does not move (a blip of 1-2 frames, like a tap, is ignored)."""
    still = m < thr
    n = len(m)
    for i in range(1, n - 1):  # close gaps of up to two frames between still frames
        if not still[i]:
            j = i
            while j < n and not still[j] and j - i < 3:
                j += 1
            if j - i <= 2 and j < n and still[j] and still[i - 1]:
                still[i:j] = True
    out, i = [], 0
    while i < n:
        if still[i]:
            j = i
            while j < n and still[j]:
                j += 1
            if (j - i) / FPS >= min_len:
                out.append([round(i / FPS, 2), round((j - 1) / FPS, 2)])
            i = j
        else:
            i += 1
    return out


def lead_transition(m):
    """The recording opens on another screen: a short burst of change (a cut or cross-fade of a few
    frames) in the first second, then calm. A scroll is a long run of change and is not trimmed."""
    hi = np.where(m[:FPS] > 8)[0]
    if not len(hi):
        return 0.0
    j = hi[0]
    while j < len(m) and m[j] > 1.0:
        j += 1
    calm = m[j:j + 12]
    if j - hi[0] <= 8 and len(calm) == 12 and np.median(calm) < 0.5 and calm.max() < 3.0:
        return round(j / FPS + 0.03, 2)
    return 0.0


def pick_focus(windows, trim, dur, last):
    """Scene time for the highlight: after the label has landed, before it leaves, and with the screen
    at rest while it is fully dimmed (0.1 s to 1.3 s after it starts; its fades may overlap motion)."""
    lo = 1.2
    hi = (dur - 1.4 if last else dur - 0.35) - 1.5
    for a, b in windows:
        s0, s1 = a - trim - 0.1, b - trim - 1.3
        t0 = max(lo, s0)
        if t0 <= min(hi, s1):
            return round(t0, 2)
    return None


def grid(img, path, scale=2):
    W, H = img.size
    im = img.resize((W * scale, H * scale), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    step = 25 if W <= 420 else 40
    for y in range(0, H, step):
        major = (y // step) % 2 == 0
        d.line([(0, y * scale), (W * scale, y * scale)], fill=(255, 0, 0) if major else (255, 170, 170), width=1)
        if major:
            d.text((3, y * scale + 2), str(y), fill=(255, 0, 0))
    for x in range(0, W, step * 2):
        d.line([(x * scale, 0), (x * scale, H * scale)], fill=(0, 150, 255), width=1)
        d.text((x * scale + 3, 3), str(x), fill=(0, 0, 255))
    im.save(path)


def sheet(path, dst, dur):
    n = max(1, int(dur))
    run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-vf',
         f"fps=1,scale=240:-1,drawtext=text='%{{pts\\:hms}}':x=6:y=6:fontsize=16:fontcolor=red:box=1,tile={n}x1",
         '-frames:v', '1', dst])


def main():
    cfg_path, out = sys.argv[1], sys.argv[2]
    cfg = json.load(open(cfg_path))
    base = os.path.dirname(os.path.abspath(cfg_path))
    os.makedirs(f'{out}/assets', exist_ok=True)
    os.makedirs(f'{out}/review', exist_ok=True)
    feats = cfg['features']
    report = []
    for i, f in enumerate(feats):
        fid, last = f['id'], i == len(feats) - 1
        src = f['src'] if os.path.isabs(f['src']) else os.path.join(base, f['src'])
        clip = f'{fid}.mp4'
        w, h, cdur = encode(src, f'{out}/assets/{clip}')
        g = frames_gray(f'{out}/assets/{clip}', w, h)
        m = motion(g)
        windows = rest_windows(m)
        sug_trim = lead_transition(m)
        trim = f.get('trim', sug_trim)
        usable = len(g) / FPS - trim
        dur = round(min(MAX_DUR, max(MIN_DUR, int(usable * 10) / 10)) + (1.1 if last else 0), 1)
        play = dur - (1.1 if last else 0)
        focus_t = (f.get('focus') or {}).get('t')
        if focus_t is None:
            focus_t = pick_focus(windows, trim, play + (1.1 if last else 0), last)
        f.update({'clip': clip, 'clipW': w, 'clipH': h, 'trim': trim, 'dur': dur})
        f.setdefault('focus', {})
        if focus_t is not None:
            f['focus']['t'] = focus_t
        # held frames: the first (for the app launch) and the last shown (for the next slide)
        frame_rgb(f'{out}/assets/{clip}', round(trim * FPS)).save(f'{out}/assets/{fid}-first.webp', quality=92)
        frame_rgb(f'{out}/assets/{clip}', min(len(g) - 1, round((trim + play) * FPS) - 1)).save(
            f'{out}/assets/{fid}-last.webp', quality=92)
        sheet(f'{out}/assets/{clip}', f'{out}/review/{fid}-sheet.png', len(g) / FPS)
        if focus_t is not None:
            grid(frame_rgb(f'{out}/assets/{clip}', min(len(g) - 1, round((trim + focus_t + 0.6) * FPS))), f'{out}/review/{fid}-grid.png')
        report.append({'id': fid, 'clip_seconds': round(len(g) / FPS, 2), 'size': [w, h], 'trim': trim,
                       'trim_suggested': sug_trim, 'scene_seconds': dur, 'rest_windows_clip_time': windows,
                       'focus_t_scene_time': focus_t,
                       'grid': f'{out}/review/{fid}-grid.png' if focus_t is not None else None})
        if usable > MAX_DUR:
            report[-1]['note'] = f'recording runs {usable:.1f} s; the scene stops at {MAX_DUR:.0f} s'
        if focus_t is None:
            report[-1]['note'] = ('no resting moment of 1.5 s fits between the label and the next scene: '
                                  'ask for a recording that pauses on the feature, or set focus.t by hand')
    json.dump(cfg, open(cfg_path, 'w'), indent=2, ensure_ascii=False)
    json.dump(report, open(f'{out}/review/prep.json', 'w'), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
