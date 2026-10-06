#!/usr/bin/env python3
"""Keep data/inbox.json, the mods waiting to be reviewed, in step with the catalogue.

Reads the catalogue that karanb192/awesome-claude-code-mods rebuilds from a
GitHub scan every few hours. Every mod that passes `claude plugin validate`,
is not archived, is not built into Claude Code and is not already in this
list goes into the inbox, keyed by mod id, with firstSeen set to today.
Mods already in the inbox get fresh stars and dates and keep their firstSeen.
Nothing is removed, and decisions live in data/decisions.json, untouched here.
"""
import datetime, json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = "https://raw.githubusercontent.com/karanb192/awesome-claude-code-mods/main/data/mods.json"
INBOX = os.path.join(ROOT, "data/inbox.json")
KEEP = ["name", "repo", "path", "description", "url", "stars", "pushedAt", "createdAt",
        "reach", "sees", "draws", "hooks", "calls", "license"]
FRESH = ["stars", "pushedAt", "createdAt", "license"]


def listed_key(source):
    """(repo, path) of a marketplace entry, the same shape as a catalogue mod."""
    if source.get("source") == "git-subdir":
        return source["url"].lower(), source["path"]
    return source["repo"].lower(), "."


def main():
    with urllib.request.urlopen(CATALOGUE, timeout=120) as r:
        catalogue = json.load(r)
    market = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    listed = {listed_key(p["source"]) for p in market["plugins"]}
    inbox = json.load(open(INBOX)) if os.path.exists(INBOX) else {}
    today = datetime.date.today().isoformat()

    added = updated = 0
    for m in catalogue["mods"]:
        if m["id"] in inbox:
            entry = inbox[m["id"]]
            if any(entry.get(k) != m.get(k) for k in FRESH):
                updated += 1
            entry.update({k: m.get(k) for k in FRESH})
        elif (m.get("validate", {}).get("status") == "passed"
              and not m.get("archived") and m.get("kind") != "builtin"
              and (m["repo"].lower(), m.get("path") or ".") not in listed):
            inbox[m["id"]] = {**{k: m.get(k) for k in KEEP}, "firstSeen": today}
            added += 1

    order = sorted(inbox, key=lambda i: (inbox[i]["firstSeen"], inbox[i]["createdAt"] or ""), reverse=True)
    os.makedirs(os.path.dirname(INBOX), exist_ok=True)
    with open(INBOX, "w") as f:
        json.dump({i: inbox[i] for i in order}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    repos = len({e["repo"] for e in inbox.values()})
    print(f"Inbox: {len(inbox)} mods in {repos} repos, {added} new, {updated} with fresh stars or dates.")


main()
