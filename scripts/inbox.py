#!/usr/bin/env python3
"""Keep data/inbox.json, the repos waiting to be reviewed, one entry per repo.

Only repos tagged with the GitHub topic claude-code-mod or claude-code-mods
are reviewed; the wider catalogue is mostly noise. For each tagged repo the
inbox keeps its GitHub description, stars, dates and license, and its mods
from the catalogue that karanb192/awesome-claude-code-mods rebuilds every few
hours: those that pass `claude plugin validate`, are not archived, and are
not of kind builtin, fixture, duplicate or catalog. A tagged repo the
catalogue does not know at all is kept with no mods and inCatalogue false,
so it is still reviewed. A tagged repo whose catalogue mods all fail those
checks is left out.

Repos already in this list are skipped unless they were in the inbox before.
firstSeen survives from the last run, and decisions live in
data/decisions.json, untouched here.

Each repo also gets `commits`, its default-branch commit count, read from
the GitHub GraphQL API with GITHUB_TOKEN. A repo whose count cannot be read
keeps its old value.
"""
import datetime, json, os, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOGUE = "https://raw.githubusercontent.com/karanb192/awesome-claude-code-mods/main/data/mods.json"
INBOX = os.path.join(ROOT, "data/inbox.json")
TOPICS = ["claude-code-mod", "claude-code-mods"]
MOD_FIELDS = ["id", "name", "path", "description", "url", "reach", "sees", "draws", "hooks", "calls"]
DROP_KINDS = {"builtin", "fixture", "duplicate", "catalog"}
BATCH = 50


def github(url, token):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def topic_repos(token):
    """{full_name: search result} for every repo tagged with one of TOPICS.

    A failed request raises, so a bad run never empties the inbox."""
    repos = {}
    for topic in TOPICS:
        page = 1
        while True:
            q = urllib.parse.quote(f"topic:{topic}")
            data = github(f"https://api.github.com/search/repositories?q={q}&per_page=100&page={page}", token)
            for r in data["items"]:
                repos[r["full_name"]] = r
            if len(data["items"]) < 100:
                break
            page += 1
    return repos


def commit_counts(repos, token):
    """{repo: default-branch commit count}, asked for BATCH repos per GraphQL query."""
    counts = {}
    for start in range(0, len(repos), BATCH):
        chunk = repos[start:start + BATCH]
        fields = " ".join(
            f'r{i}: repository(owner: {json.dumps(r.split("/")[0])}, name: {json.dumps(r.split("/")[1])}) '
            "{ defaultBranchRef { target { ... on Commit { history { totalCount } } } } }"
            for i, r in enumerate(chunk))
        req = urllib.request.Request("https://api.github.com/graphql", json.dumps({"query": "{ " + fields + " }"}).encode(),
                                     {"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                data = json.load(r).get("data") or {}
        except Exception as e:
            print(f"Commit counts for repos {start}-{start + len(chunk) - 1} failed: {e}")
            continue
        for i, repo in enumerate(chunk):
            try:
                counts[repo] = data[f"r{i}"]["defaultBranchRef"]["target"]["history"]["totalCount"]
            except (KeyError, TypeError):
                pass
    return counts


def listed_repo(source):
    return (source.get("repo") or source.get("url") or "").lower()


def main():
    token = os.environ.get("GITHUB_TOKEN")
    tagged = topic_repos(token)
    with urllib.request.urlopen(CATALOGUE, timeout=120) as r:
        catalogue = json.load(r)
    market = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    listed = {listed_repo(p["source"]) for p in market["plugins"]}
    old = json.load(open(INBOX)) if os.path.exists(INBOX) else {}
    # The inbox used to be keyed by mod id; both shapes carry repo, firstSeen and commits.
    before = {}
    for e in old.values():
        b = before.setdefault(e["repo"], {})
        b["firstSeen"] = min(b.get("firstSeen", e["firstSeen"]), e["firstSeen"])
        if e.get("commits") is not None:
            b["commits"] = e["commits"]
    today = datetime.date.today().isoformat()

    known = {m["repo"] for m in catalogue["mods"]}
    mods = {}
    for m in catalogue["mods"]:
        if (m["repo"] in tagged and m.get("validate", {}).get("status") == "passed"
                and not m.get("archived") and m.get("kind") not in DROP_KINDS):
            mods.setdefault(m["repo"], []).append({k: m.get(k) for k in MOD_FIELDS})

    inbox, left_out = {}, []
    for repo, gh in tagged.items():
        if gh.get("archived") or (repo.lower() in listed and repo not in before):
            continue
        if repo in known and repo not in mods:
            left_out.append(repo)
            continue
        found = sorted(mods.get(repo, []), key=lambda m: m["name"])
        single = found[0] if len(found) == 1 else None
        inbox[repo] = {
            "repo": repo,
            "name": single["name"] if single else gh["name"],
            "description": (single and single["description"]) or gh.get("description") or "",
            "url": single["url"] if single else gh["html_url"],
            "stars": gh["stargazers_count"],
            "pushedAt": gh["pushed_at"],
            "createdAt": gh["created_at"],
            "license": (gh.get("license") or {}).get("spdx_id"),
            "commits": before.get(repo, {}).get("commits"),
            "firstSeen": before.get(repo, {}).get("firstSeen", today),
            "inCatalogue": repo in known,
            "mods": found,
        }

    if token:
        began = time.time()
        counts = commit_counts(sorted(inbox), token)
        for repo, n in counts.items():
            inbox[repo]["commits"] = n
        print(f"Commit counts: {len(counts)} of {len(inbox)} repos in {time.time() - began:.0f}s.")
    else:
        print("No GITHUB_TOKEN, so commit counts are left as they were.")

    order = sorted(inbox, key=lambda r: (inbox[r]["firstSeen"], inbox[r]["createdAt"] or ""), reverse=True)
    os.makedirs(os.path.dirname(INBOX), exist_ok=True)
    with open(INBOX, "w") as f:
        json.dump({r: inbox[r] for r in order}, f, indent=1, ensure_ascii=False)
        f.write("\n")
    outside = sum(not e["inCatalogue"] for e in inbox.values())
    print(f"Tagged repos: {len(tagged)}. Inbox: {len(inbox)} repos with {sum(len(e['mods']) for e in inbox.values())} mods, "
          f"{outside} not in the catalogue. Left out, catalogue mods all failing checks: {len(left_out)}.")


main()
