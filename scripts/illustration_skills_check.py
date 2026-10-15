#!/usr/bin/env python3
"""Keep the illustration skills in step with the design system.

social-plus-illustration, social-plus-motion and blog-thumbnails are self-contained
(they also run as claude.ai skills without this repo), so they carry their own copies
of the fonts and write colour values out in full. This check fails when those copies
drift from design-system/:

  1. assets/fonts/*.woff2 must be byte-identical to design-system/figtree.woff2 and
     design-system/geist-mono.woff2.
  2. Every "token-name `#hex`" pair in the skills (e.g. "blue-400 `#6F89FC`") must match
     the token's value in design-system/sections/framed/framed.css, written either way
     round ("`#202022` (neutral-850)" too); a token name that framed.css doesn't define fails.
  3. Every hex colour (6- or 3-digit) in the skills' markdown, shell and examples must be
     a design-system value, or one of the few values listed in SKILL_ONLY below.
  4. Every file path the markdown names in backticks under assets/, references/ or
     scripts/ (e.g. `assets/fonts/figtree.woff2`) must exist in one of the three skills.

Run from the repo root: python3 scripts/illustration_skills_check.py
"""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ["social-plus-illustration", "social-plus-motion", "blog-thumbnails"]
DS = ROOT / "design-system"

# Values the skills may use that are not design-system tokens, each with a reason.
# Empty since Amadeus's 15 October 2026 export (every colour is a design-system value);
# any NEW non-token value fails the check until it is listed here or replaced.
SKILL_ONLY = {}

def norm(h):
    h = h.upper()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    fails = []
    for s in SKILLS:
        if not (ROOT / "marketing-team/skills" / s / "SKILL.md").is_file():
            fails.append(f"{s}: SKILL.md missing")
    if fails:
        print("\n".join("FAIL " + f for f in fails)); return 1

    # 1. fonts
    fonts = ROOT / "marketing-team/skills/social-plus-illustration/assets/fonts"
    for name in ["figtree.woff2", "geist-mono.woff2"]:
        if sha(fonts / name) != sha(DS / name):
            fails.append(f"fonts: {name} differs from design-system/{name}")

    # design-system values
    framed = (DS / "sections/framed/framed.css").read_text()
    named = {m.group(1): norm(m.group(2))
             for m in re.finditer(r"--([a-z]+-\d{3}):\s*(#[0-9A-Fa-f]{3,6})\b", framed)}
    ds_text = "".join(p.read_text(errors="ignore") for p in
                      [DS / "tokens.css", DS / "tokens.json", DS / "sections/framed/framed.css",
                       DS / "claude-design/tokens.json", DS / "foundations/colors/foundation.md"]
                      if p.is_file())
    ds_hex = {norm(h) for h in re.findall(r"#[0-9A-Fa-f]{6}\b|#[0-9A-Fa-f]{3}\b", ds_text)}

    files = []
    for s in SKILLS:
        base = ROOT / "marketing-team/skills" / s
        files += sorted(base.rglob("*.md"))
        files += sorted(p for p in (base / "assets").rglob("*") if p.suffix in (".html", ".js"))

    pairs = set()
    for f in files:
        text = f.read_text()
        rel = f.relative_to(ROOT)
        # 2. token pairs, name first ("blue-400 `#6F89FC`") or hex first ("`#202022` (neutral-850)")
        found = [(m.group(1), m.group(2)) for m in re.finditer(
            r"\b((?:neutral|blue|green|purple|pink|orange|yellow|red)-\d{2,3})\b[^`#\n]{0,3}`(#[0-9A-Fa-f]{6})`", text)]
        found += [(m.group(2), m.group(1)) for m in re.finditer(
            r"`(#[0-9A-Fa-f]{6})`\s*\(((?:neutral|blue|green|purple|pink|orange|yellow|red)-\d{2,3})\b", text)]
        for name, val in found:
            pairs.add((name, norm(val)))
            if name not in named:
                fails.append(f"{rel}: {name} is not a token in framed.css")
            elif named[name] != norm(val):
                fails.append(f"{rel}: {name} is {norm(val)} here, {named[name]} in the design system")
        # 3. every hex is known (word-bounded, so "#111" and "#111111" both count)
        for h in re.findall(r"#(?:[0-9A-Fa-f]{6}|[0-9A-Fa-f]{3})\b", text):
            v = norm(h)
            if v not in ds_hex and v not in SKILL_ONLY:
                fails.append(f"{rel}: {v} is not a design-system value (add it to the design system, "
                             f"or to SKILL_ONLY in this script with a reason)")

    # 4. file paths named in the markdown exist
    roots = [ROOT / "marketing-team/skills" / s for s in SKILLS]
    for f in files:
        if f.suffix != ".md":
            continue
        for m in re.finditer(r"`((?:assets|references|scripts)/[A-Za-z0-9_./-]+\.[a-z0-9]+)`", f.read_text()):
            ref = m.group(1)
            if not any((r / ref).is_file() for r in roots):
                fails.append(f"{f.relative_to(ROOT)}: `{ref}` does not exist in any of the three skills")

    if fails:
        for f in sorted(set(fails)):
            print("FAIL", f)
        return 1
    print(f"OK: fonts identical, {len(files)} files, {len({n for n, _ in pairs})} token names "
          f"({len(pairs)} name/value pairs) verified against framed.css")
    return 0

if __name__ == "__main__":
    sys.exit(main())
