#!/usr/bin/env python3
"""Import skills exported from claude.ai (.skill files, or a .zip holding them) into
marketing-team/skills/, replacing the repo copy, and show what changed.

For skills that are also edited outside this repo (Amadeus's illustration skills started
as claude.ai skills). Whichever copy was edited last, this makes the repo match it:

  python3 scripts/import_skills.py ~/Downloads/social-plus-illustration-skills.zip
  python3 scripts/import_skills.py ~/Downloads/blog-thumbnails.skill

A .skill file is a zip with one folder <name>/ holding SKILL.md. A bundle .zip may hold
.skill files and/or plain <name>/SKILL.md folders; when both exist for a name they must
be identical, or the import stops. Only skills that already exist in the repo, or are
named with --new, are written. A skill is replaced as a whole: files that exist only in
the repo copy are removed (git diff shows them). Exit code: 1 when the import stops or
the illustration check fails, else 0. Afterwards: git diff, bump the plugin version and
CHANGELOG as for any skill change.
"""
import argparse, atexit, filecmp, io, pathlib, shutil, subprocess, sys, tempfile, zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILLS = ROOT / "marketing-team/skills"
JUNK = {".DS_Store", "__MACOSX"}

def extract(zbytes, dest):
    root = dest.resolve()
    with zipfile.ZipFile(io.BytesIO(zbytes)) as z:
        for info in z.infolist():
            name = info.filename.replace("\\", "/")
            parts = pathlib.PurePosixPath(name).parts
            if any(p in JUNK for p in parts) or info.is_dir():
                continue
            # zip-slip guard: no absolute paths, no "..", nothing outside dest
            if name.startswith("/") or ".." in parts or (parts and ":" in parts[0]):
                sys.exit(f"STOP: unsafe path in archive: {info.filename}")
            out = dest.joinpath(*parts)
            if root not in out.resolve().parents:
                sys.exit(f"STOP: unsafe path in archive: {info.filename}")
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(info))

def skill_dirs(root):
    return {p.parent.name: p.parent for p in root.rglob("SKILL.md")}

def same_tree(a, b):
    c = filecmp.dircmp(a, b, ignore=list(JUNK))
    if c.left_only or c.right_only or c.funny_files:
        return False
    # dircmp compares size+mtime only; read the bytes
    if any(not filecmp.cmp(a / f, b / f, shallow=False) for f in c.common_files):
        return False
    return all(same_tree(a / d, b / d) for d in c.common_dirs)

def main():
    sys.stdout.reconfigure(line_buffering=True)
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help=".skill file or .zip bundle")
    ap.add_argument("--new", nargs="*", default=[], help="skill names allowed to be added (not yet in the repo)")
    o = ap.parse_args()
    src = pathlib.Path(o.source).expanduser()
    work = pathlib.Path(tempfile.mkdtemp(prefix="skill_import_"))
    atexit.register(shutil.rmtree, work, True)
    raw = work / "raw"; extract(src.read_bytes(), raw)

    # unpack nested .skill files next to the plain folders
    packed = work / "packed"
    for f in raw.rglob("*.skill"):
        extract(f.read_bytes(), packed / f.stem)
    plain = skill_dirs(raw)
    from_packed = skill_dirs(packed) if packed.exists() else {}

    found = {}
    for name in sorted(set(plain) | set(from_packed)):
        a, b = plain.get(name), from_packed.get(name)
        if a and b and not same_tree(a, b):
            sys.exit(f"STOP: {name} differs between its .skill file and its folder in {src.name}; ask which is current")
        found[name] = a or b
    if not found:
        sys.exit(f"STOP: no SKILL.md found in {src}")

    for name, path in found.items():
        target = SKILLS / name
        if not target.exists() and name not in o.new:
            print(f"SKIP {name}: not in the repo (pass --new {name} to add it)")
            continue
        if target.exists() and same_tree(path, target):
            print(f"same {name}")
            continue
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(path, target, ignore=shutil.ignore_patterns(*JUNK))
        print(f"wrote {name}")

    shutil.rmtree(work, ignore_errors=True)
    subprocess.run(["git", "-C", str(ROOT), "status", "--short", "--", "marketing-team/skills"])
    check = ROOT / "scripts/illustration_skills_check.py"
    if check.exists():
        sys.exit(subprocess.run([sys.executable, str(check)]).returncode)

if __name__ == "__main__":
    main()
