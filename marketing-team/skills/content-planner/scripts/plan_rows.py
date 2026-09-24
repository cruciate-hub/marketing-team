#!/usr/bin/env python3
"""
content-planner: turn candidate article ideas into Content Queue rows.

The skill (Claude) researches a seed and writes candidate ideas as JSON.
This script is the mechanical gate between those ideas and the Queue:

  1. Validates every candidate (required fields, collection/intent rules,
     per-collection cap, no duplicates inside the batch).
  2. Checks each candidate against every Queue row and published page with
     the shared intent matcher (scripts/intent_match.py).
  3. Labels each one: New / Merge / Update existing / Reject.
  4. Writes paste-ready Queue rows for the New ones (next free IDs), plus a
     review report listing merges, updates, rejections and warnings.

Usage
    python3 scripts/plan_rows.py --candidates outputs/candidates.json \
        --queue queue.csv --seed "app retention" --seed-type keyword \
        --entered-by "Amadeus" [--date 2026-09-24] [--out-dir outputs]

Candidate JSON
    {"candidates": [{
        "ref": "c1",                          # temporary key, unique in batch
        "collection": "Answer",               # Glossary | Answer | Blog
        "intent": "explainer",                # see VALID_INTENTS (aliases accepted)
        "cluster": "Retention & engagement",
        "stage": "Problem",                   # Problem | Solution | Evaluation | Implementation | Definition
        "question": "Why do fitness apps struggle with retention?",
        "first_sentence": "Fitness apps lose users because ...",
        "headings": ["...?", "...?"],         # sub-questions (Answer/Blog: 2+)
        "info_source": "Approved customers Noom, Smart Fit (evidence bank)",
        "premise": "https://... (source for the question's assumption)",
        "demand": "Ahrefs US: 'fitness app retention' 90",
        "dependencies": ["GL1", "c2"],        # Queue IDs or refs in this batch
        "suggested_priority": "P2",
        "notes": ""
    }]}

Exit codes
    0  plan written (warnings allowed)
    1  validation errors: fix the candidates and re-run
    2  an input could not be read
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT_SCRIPTS = Path(__file__).resolve().parents[4] / "scripts"
sys.path.insert(0, str(ROOT_SCRIPTS))
from intent_match import (  # noqa: E402
    LIKELY_DUPLICATE, NEEDS_REVIEW, load_pages, load_queue, question_form, score,
)

QUEUE_COLUMNS = [
    "ID", "Cluster", "Journey stage", "Seed", "Date added", "Collection", "Intent",
    "Canonical question", "Draft first sentence", "Headings (sub-questions)",
    "Unique information source", "Premise check (source)", "Demand evidence",
    "Check result", "Conflicts with", "Dependencies", "Priority", "Status",
    "Target publish date", "Reviewer", "Draft link", "Published URL", "Published date",
    "Links added from older pages", "Last refreshed", "Notes",
]
VALID_INTENTS = {
    "Glossary": {"definition"},
    "Answer": {"how-to", "decision", "explainer", "playbook"},
    "Blog": {"opinion", "original-research", "listicle", "trend", "product-deep-dive",
             "product-education", "customer-narrative"},
}
# Friendly spellings accepted from people and older Queue rows.
INTENT_ALIASES = {
    "original research": "original-research", "research": "original-research",
    "narrative": "customer-narrative", "customer narrative": "customer-narrative",
    "comparison": "listicle", "pov": "opinion", "thought leadership": "opinion",
    "product deep-dive": "product-deep-dive", "announcement": "product-deep-dive",
    "product education": "product-education", "tutorial": "product-education",
    "how to": "how-to", "howto": "how-to",
}


def canonical_intent(raw: str) -> str:
    k = (raw or "").strip().lower()
    return INTENT_ALIASES.get(k, k.replace(" ", "-") if k.replace(" ", "-") in
                              {i for s in VALID_INTENTS.values() for i in s} else k)
ID_PREFIX = {"Glossary": "GL", "Answer": "AN", "Blog": "BL"}
STAGES = {"Problem", "Solution", "Evaluation", "Implementation", "Definition"}
MAX_PER_COLLECTION = 10
PUBLISHED_STATES = {"published", "refresh due"}
PLANNED_STATES = {"idea", "approved", "writing", "in review", "changes requested", "blocked: needs data"}
IGNORED_STATES = {"scheduled for removal", "merged"}
PENDING_RE = re.compile(r"\b(pending|needs? legal|legal approval|not yet approved|to be approved)\b", re.I)
YEAR_RE = re.compile(r"\b20\d\d\b")


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "seed"


def words(s: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", s or ""))


def next_ids(queue: list[dict]) -> dict[str, int]:
    nxt = {}
    for coll, pre in ID_PREFIX.items():
        nums = [int(m.group(1)) for r in queue if (m := re.fullmatch(pre + r"(\d+)", r["id"]))]
        nxt[coll] = (max(nums) + 1) if nums else 1
    return nxt


def validate(cands: list[dict], queue_ids: set[str]) -> tuple[list[str], dict[str, list[str]]]:
    errors: list[str] = []
    for c in cands:
        c["intent"] = canonical_intent(c.get("intent", ""))
    warns: dict[str, list[str]] = {c.get("ref", f"#{i}"): [] for i, c in enumerate(cands)}
    refs = [c.get("ref") for c in cands]
    if len(set(refs)) != len(refs) or None in refs:
        errors.append("every candidate needs a unique 'ref'")
    counts: dict[str, int] = {}
    for c in cands:
        ref = c.get("ref", "?")
        coll = c.get("collection")
        counts[coll] = counts.get(coll, 0) + 1
        for f in ("collection", "intent", "cluster", "stage", "question", "first_sentence", "info_source"):
            if not str(c.get(f, "")).strip():
                errors.append(f"{ref}: missing '{f}'")
        if coll not in VALID_INTENTS:
            errors.append(f"{ref}: collection must be Glossary, Answer or Blog")
            continue
        if c.get("intent") not in VALID_INTENTS[coll]:
            errors.append(f"{ref}: intent '{c.get('intent')}' not valid for {coll} (use {sorted(VALID_INTENTS[coll])})")
        if c.get("stage") and c["stage"] not in STAGES:
            errors.append(f"{ref}: stage must be one of {sorted(STAGES)}")
        q = c.get("question", "")
        form = question_form(q)
        if coll == "Glossary" and form != "definition":
            errors.append(f"{ref}: Glossary questions are 'What is [term]?'")
        if coll in ("Answer", "Blog") and len(c.get("headings") or []) < 2:
            errors.append(f"{ref}: {coll} ideas need at least 2 sub-questions in 'headings'")
        if words(c.get("first_sentence", "")) > 60:
            errors.append(f"{ref}: first_sentence is {words(c['first_sentence'])} words (max 60)")
        for d in c.get("dependencies") or []:
            if d not in queue_ids and d not in refs:
                errors.append(f"{ref}: dependency '{d}' is neither a Queue ID nor a ref in this batch")
        if coll == "Answer" and form == "definition":
            warns[ref].append("reads as a definition: 'What is [term]?' belongs to Glossary")
        if coll == "Answer" and form in ("why", "whether") and not str(c.get("premise", "")).strip():
            warns[ref].append("question makes an assumption but has no premise source")
        if coll in ("Answer", "Glossary") and YEAR_RE.search(q):
            warns[ref].append("year in an evergreen question: drop it unless the answer is genuinely year-specific")
        if coll == "Blog" and c.get("intent") == "product-education" and form in ("howto",) and not re.search(r"social\.plus|\bour\b", q, re.I):
            warns[ref].append("general how-to question: unless it teaches a social.plus feature, it belongs to Answer")
        if coll == "Blog" and c.get("intent") == "listicle" and re.search(r"\bsocial\.plus\b", q, re.I):
            warns[ref].append("self-named listicle: keep criteria even and identify social.plus as publisher")
    for coll, n in counts.items():
        if coll in VALID_INTENTS and n > MAX_PER_COLLECTION:
            errors.append(f"{n} {coll} ideas from one seed (max {MAX_PER_COLLECTION}); keep the strongest")
    # duplicates inside the batch
    for i, a in enumerate(cands):
        for b in cands[i + 1:]:
            s = score(a.get("question", ""), a.get("first_sentence", ""), b.get("question", ""), b.get("first_sentence", ""))
            if s >= LIKELY_DUPLICATE:
                errors.append(f"{a.get('ref')} and {b.get('ref')} look like the same question ({s:.2f}): merge them")
    return errors, warns


def classify(c: dict, others: list[dict]) -> tuple[str, dict | None, float, list[tuple[float, dict]]]:
    scored = []
    for o in others:
        st = o["status"].lower()
        if st in IGNORED_STATES:
            continue
        s = score(c["question"], c.get("first_sentence", ""), o["question"], o.get("sentence", ""))
        if s >= NEEDS_REVIEW:
            scored.append((s, o))
    scored.sort(key=lambda x: -x[0])
    if scored and scored[0][0] >= LIKELY_DUPLICATE:
        s, o = scored[0]
        st = o["status"].lower()
        if st == "rejected":
            return "Reject", o, s, scored
        if st in PUBLISHED_STATES:
            return "Update existing", o, s, scored
        return "Merge", o, s, scored
    return "New", None, 0.0, scored


def main() -> int:
    ap = argparse.ArgumentParser(description="Turn candidate ideas into Content Queue rows")
    ap.add_argument("--candidates", type=Path, required=True)
    ap.add_argument("--queue", type=Path, required=True, help="Queue tab exported as CSV")
    ap.add_argument("--seed", required=True)
    ap.add_argument("--seed-type", default="keyword", choices=["keyword", "phrase", "prompt", "idea"])
    ap.add_argument("--entered-by", default="")
    ap.add_argument("--date", default=dt.date.today().isoformat())
    ap.add_argument("--pages", action="append", help="pages-*.json glob(s); default: none (the Queue already lists existing pages)")
    ap.add_argument("--out-dir", type=Path, default=Path("outputs"))
    args = ap.parse_args()

    try:
        cands = json.loads(args.candidates.read_text(encoding="utf-8"))["candidates"]
        queue = load_queue(args.queue)
        pages = []
        for pat in args.pages or []:
            pages += load_pages(pat)
    except Exception as e:  # noqa: BLE001
        print(f"Could not read input: {e}\nRESULT: UNVERIFIED")
        return 2

    queue_ids = {r["id"] for r in queue}
    with args.queue.open(encoding="utf-8-sig", newline="") as f:
        cluster_of = {r.get("ID", ""): (r.get("Cluster") or "").strip() for r in csv.DictReader(f)}
    errors, warns = validate(cands, queue_ids)
    if errors:
        print("Validation errors (nothing written):")
        for e in errors:
            print(f"  - {e}")
        print("RESULT: INVALID")
        return 1

    queue_urls = {r["url"].rstrip("/") for r in queue if r["url"]}
    others = queue + [p for p in pages if p["url"].rstrip("/") not in queue_urls]
    nxt = next_ids(queue)
    ref_to_id: dict[str, str] = {}
    results = []
    for c in cands:
        label, target, s, scored = classify(c, others)
        new_id = ""
        if label == "New":
            coll = c["collection"]
            new_id = f"{ID_PREFIX[coll]}{nxt[coll]}"
            nxt[coll] += 1
            ref_to_id[c["ref"]] = new_id
        results.append((c, label, target, s, scored, new_id))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.seed)
    csv_path = args.out_dir / f"plan-{slug}.csv"
    md_path = args.out_dir / f"plan-{slug}.md"

    new_rows = []
    for c, label, target, s, scored, new_id in results:
        if label != "New":
            continue
        blocked = bool(PENDING_RE.search(c.get("info_source", "")))
        conflicts = "; ".join(f"Review {sc:.2f}: {o['id'] or o['url']} ({o['question']})" for sc, o in scored)
        deps = "; ".join(ref_to_id.get(d, d) for d in c.get("dependencies") or [])
        notes = " ".join(x for x in [
            f"Suggested priority: {c['suggested_priority']}." if c.get("suggested_priority") else "",
            " ".join(warns.get(c["ref"], [])), c.get("notes", "")] if x).strip()
        row = {k: "" for k in QUEUE_COLUMNS}
        row.update({
            "ID": new_id, "Cluster": c["cluster"], "Journey stage": c["stage"], "Seed": args.seed,
            "Date added": args.date, "Collection": c["collection"], "Intent": c["intent"],
            "Canonical question": c["question"], "Draft first sentence": c["first_sentence"],
            "Headings (sub-questions)": " | ".join(c.get("headings") or []) or "Fixed glossary template",
            "Unique information source": c["info_source"], "Premise check (source)": c.get("premise", ""),
            "Demand evidence": c.get("demand", ""), "Check result": "New", "Conflicts with": conflicts,
            "Dependencies": deps, "Status": "Blocked: needs data" if blocked else "Idea", "Notes": notes,
        })
        new_rows.append(row)

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=QUEUE_COLUMNS)
        w.writeheader()
        w.writerows(new_rows)

    counts = {k: sum(1 for r in results if r[1] == k) for k in ("New", "Merge", "Update existing", "Reject")}
    by_coll = {k: sum(1 for r in new_rows if r["Collection"] == k) for k in VALID_INTENTS}
    md = [f"# Plan for seed: {args.seed}", "",
          f"Seed type: {args.seed_type}. Entered by: {args.entered_by or 'n/a'}. Date: {args.date}.", "",
          f"**{len(cands)} candidates:** {counts['New']} new "
          f"(Glossary {by_coll['Glossary']}, Answer {by_coll['Answer']}, Blog {by_coll['Blog']}), "
          f"{counts['Merge']} merge, {counts['Update existing']} update existing, {counts['Reject']} reject.", "",
          "## New rows (in the CSV, paste into the Queue tab)", "",
          "| ID | Collection | Intent | Question | Status | Needs review against | Same cluster in Queue |",
          "|---|---|---|---|---|---|---|"]
    active = {r["id"]: r for r in queue if r["status"].lower() not in IGNORED_STATES | {"rejected"}}
    for r in new_rows:
        rev = r["Conflicts with"].replace("|", "/") or "none"
        same = [i for i, cl in cluster_of.items() if cl and cl == r["Cluster"] and i in active and not i.startswith("EX-")]
        md.append(f"| {r['ID']} | {r['Collection']} | {r['Intent']} | {r['Canonical question']} | {r['Status']} | {rev} | "
                  f"{', '.join(same) or 'none'} |")
    changes = [(c, l, t, s) for c, l, t, s, _, _ in results if l != "New"]
    md += ["", "## Changes to existing rows (not in the CSV, apply by hand)", ""]
    if not changes:
        md.append("None.")
    for c, l, t, s in changes:
        ref = t["id"] or t["url"]
        action = {"Merge": f"add as a sub-question or note on {ref}",
                  "Update existing": f"consider setting {ref} to Refresh due and covering this angle there",
                  "Reject": f"previously rejected as {ref}; not re-proposed"}[l]
        md.append(f"- **{l}** ({s:.2f}): \"{c['question']}\" matches {ref} \"{t['question']}\". Action: {action}.")
    w_all = [(c["ref"], m) for c in cands for m in warns.get(c["ref"], [])]
    md += ["", "## Warnings", ""] + ([f"- {ref}: {m}" for ref, m in w_all] or ["None."])
    md += ["", "## Seeds tab row", "",
           f"`{args.seed}` | {args.seed_type} | {args.entered_by} | {args.date} | fill the two count formulas down from the row above", ""]
    md_path.write_text("\n".join(md), encoding="utf-8")

    print(f"Plan for '{args.seed}': {counts['New']} new, {counts['Merge']} merge, "
          f"{counts['Update existing']} update existing, {counts['Reject']} reject, {len(w_all)} warning(s)")
    print(f"  rows:   {csv_path}")
    print(f"  report: {md_path}")
    print("RESULT: PLANNED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
