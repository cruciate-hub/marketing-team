#!/usr/bin/env python3
"""Cut one ElevenLabs voiceover take into its beats and place them on the film's timeline.

Usage: python3 place_voiceover.py OUT_DIR take.mp3 [--noise -35] [--min-gap 0.35]

The take has one beat per scene, separated by the script's pause tags: the intro, one beat per
feature, and the close. The script splits it at the longest silences (as many cuts as beats - 1),
trims each piece, encodes it as a small MP3 and writes:
  OUT_DIR/assets/vo-1.mp3 ...           the lines (mono, 96 kbps: under the player's 256 KiB a line)
  OUT_DIR/film/docs/modules/narration.js.json   the narration module (kit.narration)
  OUT_DIR/film/voice.json               uploads (name, path, mime, seconds) and the timing check
Beat starts: intro 0.4 s; each feature 0.8 s after its scene starts; the close 1.6 s before the logos.
Needs ffmpeg/ffprobe.
"""
import json, os, re, subprocess, sys


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True)


def seconds(path):
    return float(sh(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', path]).stdout)


def main():
    out, take = sys.argv[1], sys.argv[2]
    args = sys.argv[3:]
    noise = args[args.index('--noise') + 1] if '--noise' in args else '-35'
    min_gap = args[args.index('--min-gap') + 1] if '--min-gap' in args else '0.35'
    mods = f'{out}/film/docs/modules'
    sc = json.loads(json.load(open(f'{mods}/scenes.json.json'))['text'])
    cfg = json.loads(json.load(open(f'{mods}/showcase.json.json'))['text'])
    T, acc = {}, 0.0
    for s in sc['scenes']:
        T[s['id']] = acc; acc += s['dur']
    T['END'] = acc
    beats = [('intro', 0.4)] + [(f['id'], 0.8) for f in cfg['features']] + [('lockup', -1.6)]
    at = [round(T[k] + d, 2) for k, d in beats]

    # silences in the take
    log = sh(['ffmpeg', '-hide_banner', '-i', take, '-af', f'silencedetect=noise={noise}dB:d={min_gap}', '-f', 'null', '-']).stderr
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', log)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', log)]
    total = seconds(take)
    gaps = [(s, e) for s, e in zip(starts, ends) if s > 0.05 and e < total - 0.05]  # inner silences only
    need = len(beats) - 1
    if len(gaps) < need:
        sys.exit(f'place_voiceover: found {len(gaps)} pauses, need {need}. Regenerate with the pause tags, '
                 f'or retry with --noise -30 / --min-gap 0.25.')
    cuts = sorted(sorted(gaps, key=lambda g: g[1] - g[0], reverse=True)[:need])
    lead = next((e for s, e in zip(starts, ends) if s <= 0.05), 0.0)
    tail = next((s for s, e in zip(starts, ends) if e >= total - 0.05), total)
    spans = [(lead, cuts[0][0])] + [(cuts[i][1], cuts[i + 1][0]) for i in range(need - 1)] + [(cuts[-1][1], tail)]

    os.makedirs(f'{out}/assets', exist_ok=True)
    lines, uploads, problems = [], [], []
    for i, ((a, b), t0, (k, _)) in enumerate(zip(spans, at, beats), 1):
        name = f'vo-{i}.mp3'
        p = os.path.abspath(f'{out}/assets/{name}')
        a0, b0 = max(0, a - 0.04), min(total, b + 0.08)  # keep the breath in and the word's tail
        sh(['ffmpeg', '-v', 'error', '-y', '-ss', f'{a0:.3f}', '-to', f'{b0:.3f}', '-i', take, '-ac', '1', '-ar', '44100',
            '-af', 'afade=t=in:d=0.02,areverse,afade=t=in:d=0.04,areverse', '-c:a', 'libmp3lame', '-b:a', '96k', p])
        d = round(seconds(p), 2)
        if os.path.getsize(p) > 256 * 1024:
            problems.append(f'{name} is over 256 KiB')
        nxt = at[i] if i < len(at) else T['END']
        if t0 + d > nxt - 0.15:
            problems.append(f'beat {i} ({k}) runs {t0 + d - (nxt - 0.15):.2f} s into the next beat: '
                            f'trim words or raise Speed for this line')
        base = 'T.' + k if k != 'lockup' else 'T.lockup'
        off = round(t0 - T[k], 2)
        lines.append(f"    {{ at: {base} {'+' if off >= 0 else '-'} {abs(off)}, dur: {d}, audio: '{name}' }},")
        uploads.append({'name': name, 'path': p, 'mime': 'audio/mpeg', 'seconds': d, 'at': t0})
    code = ('// Voiceover: one line per beat, cut from the ElevenLabs take by place_voiceover.py.\n'
            '// The music dips under each line; Export includes it.\n'
            'kit.narration(function (T) {\n  return { lines: [\n' + '\n'.join(lines) + '\n  ] };\n});\n')
    json.dump({'kind': 'js', 'text': code}, open(f'{mods}/narration.js.json', 'w'))
    json.dump({'uploads': uploads, 'problems': problems}, open(f'{out}/film/voice.json', 'w'), indent=1)
    print(code)
    print(json.dumps({'problems': problems}, indent=1))


if __name__ == '__main__':
    main()
