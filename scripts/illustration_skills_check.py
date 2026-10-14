#!/usr/bin/env python3
"""Keep the illustration skills in step with the design system.

social-plus-illustration, social-plus-motion and blog-thumbnails are self-contained
(they also run as claude.ai skills without this repo), so they carry their own copies
of the fonts and write colour values out in full. This check fails when those copies
drift from design-system/:

  1. assets/fonts/*.woff2 must be byte-identical to design-system/figtree.woff2 and
     design-system/geist-mono.woff2.
  2. Every "token-name `#hex`" pair in the skills (e.g. "blue-400 `#6F89FC`") must match
     the token's value in design-system/sections/framed/framed.css.
  3. Every hex colour in the skills' markdown and shell must be a design-system value,
     or one of the few values listed in SKILL_ONLY below.

Run from the repo root: python3 scripts/illustration_skills_check.py
"""
import hashlib, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ["social-plus-illustration", "social-plus-motion", "blog-thumbnails"]
DS = ROOT / "design-system"

# Values the skills use that are not design-system tokens (chart grid lines, tick labels,
# logo tiles). Listed so any NEW non-token value fails the check.
SKILL_ONLY = {
    "#1E1E20": "chart grid lines (blog-thumbnails in-blog-images.md)",
    "#6B6C70": "chart tick labels (blog-thumbnails in-blog-images.md)",
    "#1C1C1E": "alternative logo tile (social-plus-illustration third-party-logos.md)",
    "#E6E6E6": "monochrome logo colour (social-plus-illustration third-party-logos.md)",
}

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
        files += [p for p in [base / "assets/shell.dc.html"] if p.is_file()]

    for f in files:
        text = f.read_text()
        rel = f.relative_to(ROOT)
        # 2. "name `#hex`" and "name (`#hex`)" pairs
        for m in re.finditer(r"\b([a-z]+-\d{3})\b[^`#\n]{0,3}`(#[0-9A-Fa-f]{6})`", text):
            name, val = m.group(1), norm(m.group(2))
            if name in named and named[name] != val:
                fails.append(f"{rel}: {name} is {val} here, {named[name]} in the design system")
        # 3. every hex is known
        for h in re.findall(r"#[0-9A-Fa-f]{6}\b", text):
            v = norm(h)
            if v not in ds_hex and v not in SKILL_ONLY:
                fails.append(f"{rel}: {v} is not a design-system value (add it to the design system, "
                             f"or to SKILL_ONLY in this script with a reason)")

    if fails:
        for f in sorted(set(fails)):
            print("FAIL", f)
        return 1
    print(f"OK: fonts identical, {len(files)} files checked against {len(named)} named tokens")
    return 0

if __name__ == "__main__":
    sys.exit(main())
