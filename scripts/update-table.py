#!/usr/bin/env python3
"""Rebuild the mod tables in README.md from .claude-plugin/marketplace.json.

Each mod's row gets its star count and the date of its last push, read from
the GitHub API. Set GITHUB_TOKEN to avoid the low anonymous rate limit.
"""
import json, os, re, urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!-- mods:start -->", "<!-- mods:end -->"


def repo_info(repo):
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}")
    req.add_header("Accept", "application/vnd.github+json")
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def repo_from_source(source):
    if source.get("repo"):
        return source["repo"]
    url = urlparse(source["url"])
    if url.scheme != "https" or url.hostname != "github.com" or url.username or url.password:
        raise ValueError("Repository statistics require a public GitHub HTTPS URL")
    repo = url.path.strip("/").removesuffix(".git")
    if len(repo.split("/")) != 2 or not all(repo.split("/")):
        raise ValueError("Repository statistics require an owner/repository source")
    return repo


def main():
    market = json.load(open(os.path.join(ROOT, ".claude-plugin/marketplace.json")))
    by_category = {}
    for mod in market["plugins"]:
        by_category.setdefault(mod.get("category", "other"), []).append(mod)

    out = []
    for category in sorted(by_category):
        out += [f"### {category.capitalize()}", "", "| Mod | What it does | Stars | Last update |", "|-----|--------------|------:|-------------|"]
        rows = []
        for mod in by_category[category]:
            source = mod["source"]
            repo = repo_from_source(source)
            link = mod.get("homepage") or f"https://github.com/{repo}"
            info = repo_info(repo)
            author = mod.get("author", {}).get("name", info["owner"]["login"])
            rows.append((info["stargazers_count"], f"| [{mod['name']}]({link})<br>by {author} | {mod['description']} | ★ {info['stargazers_count']} | {info['pushed_at'][:10]} |"))
        out += [row for _, row in sorted(rows, key=lambda r: -r[0])] + [""]

    path = os.path.join(ROOT, "README.md")
    readme = open(path).read()
    table = "\n".join(out).rstrip()
    readme = re.sub(f"{re.escape(START)}.*?{re.escape(END)}", f"{START}\n{table}\n{END}", readme, flags=re.S)
    open(path, "w").write(readme)


if __name__ == "__main__":
    main()
