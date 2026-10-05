#!/usr/bin/env python3
"""Write a digest of new and rising Claude Code mods, as markdown on stdout.

Reads the catalogue that karanb192/awesome-claude-code-mods rebuilds from a
GitHub scan every few hours, compares it with data/scout-state.json (the star
counts seen last time), and lists:

- repositories with mods first seen since the last run, most stars first
- repositories that gained the most stars since the last run

Only mods that pass `claude plugin validate`, are not archived and are not
built into Claude Code are listed. Mods already in this list are skipped.
The state file is updated, so the next run starts from here.
"""
import json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = "https://raw.githubusercontent.com/karanb192/awesome-claude-code-mods/main/data/mods.json"
STATE = os.path.join(ROOT, "data/scout-state.json")
TOP = 15


def group_by_repo(mods):
    """One entry per repository, since stars belong to the repo, not the mod."""
    repos = {}
    for m in mods:
        repos.setdefault(m["repo"], []).append(m)
    return repos


def row(repo, mods, extra=""):
    top = mods[0]
    if len(mods) == 1:
        name = f"[{top['name']}]({top['url']})"
        desc = top.get("description") or ""
    else:
        name = f"[{repo}](https://github.com/{repo})"
        desc = f"{len(mods)} mods: " + ", ".join(m["name"] for m in mods[:6]) + ("…" if len(mods) > 6 else "")
    desc = desc.replace("|", "/").replace("\n", " ")
    if len(desc) > 140:
        desc = desc[:137].rsplit(" ", 1)[0] + "…"
    reach = max((m.get("reach", {}) for m in mods), key=lambda r: r.get("level", 0)).get("name", "?")
    pushed = max(m["pushedAt"] for m in mods)[:10]
    return f"| {name} | {desc} | ★ {top['stars']}{extra} | {pushed} | {reach} |"


def table(rows):
    return ["| Mod | What it does | Stars | Last update | Reach |", "|-----|--------------|------:|-------------|-------|", *rows]


def main():
    with urllib.request.urlopen(CATALOGUE, timeout=120) as r:
        catalogue = json.load(r)
    market = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    listed = {p["source"]["repo"].lower() for p in market["plugins"]}

    repos = group_by_repo(
        m for m in catalogue["mods"]
        if m.get("validate", {}).get("status") == "passed"
        and not m.get("archived") and m.get("kind") != "builtin"
        and m["repo"].lower() not in listed
    )
    stars = {repo: mods[0]["stars"] for repo, mods in repos.items()}
    seen = json.load(open(STATE)) if os.path.exists(STATE) else None

    out = []
    if seen is None:
        out += ["First run, so here are the most starred repositories with mods.", ""]
        top = sorted(repos, key=lambda r: -stars[r])[:TOP]
        out += table([row(r, repos[r]) for r in top])
    else:
        new = sorted((r for r in repos if r not in seen), key=lambda r: -stars[r])
        out += [f"## New since last week ({len(new)})", ""]
        out += table([row(r, repos[r]) for r in new[:TOP]]) if new else ["None."]
        rising = sorted(
            ((stars[r] - seen[r], r) for r in repos if r in seen and stars[r] > seen[r]),
            key=lambda x: -x[0],
        )
        out += ["", "## Rising", ""]
        out += table([row(r, repos[r], f" (+{d})") for d, r in rising[:TOP]]) if rising else ["None."]

    out += ["", f"From the catalogue at {catalogue.get('generated', '?')[:16]}: {len(catalogue['mods'])} mods in {len(repos)} repositories that pass validation."]
    out += ["Reach is the most a mod can do: reads, writes or runs, or sends over the network."]
    print("\n".join(out))

    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    json.dump(stars, open(STATE, "w"), indent=0, sort_keys=True)


main()
