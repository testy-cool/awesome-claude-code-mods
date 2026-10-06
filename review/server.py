#!/usr/bin/env python3
"""Serve the mod inbox review page on 127.0.0.1:8130.

GET  /              the page
GET  /api/inbox     inbox entries with their verdicts
GET  /api/readme    a mod's README from GitHub, cached in memory
POST /api/decide    {id, verdict: "keep" | "skip" | null} writes data/decisions.json,
                    and on keep adds the mod to .claude-plugin/marketplace.json
POST /api/flush     commit and push the pending decisions now (sent when the page closes)
POST /api/refresh   flush, then git pull

Decisions are committed and pushed as one batch once the page has been
quiet for IDLE seconds, or when it closes.
"""
import datetime, json, os, subprocess, threading, urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, "data/inbox.json")
DECISIONS = os.path.join(ROOT, "data/decisions.json")
MARKET = os.path.join(ROOT, ".claude-plugin/marketplace.json")
PAGE = os.path.join(ROOT, "review/index.html")
PORT, IDLE = 8130, 60

lock = threading.Lock()
pending = {}  # id -> verdict, since the last commit
timer = None
readmes = {}


def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)
    print("git", *args, "->", r.returncode, (r.stdout + r.stderr).strip()[-400:], flush=True)
    return r


def load(path, default):
    return json.load(open(path)) if os.path.exists(path) else default


def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def source_of(mod):
    if (mod.get("path") or ".") == ".":
        return {"source": "github", "repo": mod["repo"]}
    return {"source": "git-subdir", "url": mod["repo"], "path": mod["path"]}


def set_listed(mod, keep):
    """Add the mod to the marketplace, or take it out again on undo."""
    market = load(MARKET, {"plugins": []})
    src = source_of(mod)
    market["plugins"] = [p for p in market["plugins"] if p["source"] != src]
    if keep:
        owner = mod["repo"].split("/")[0]
        names = {p["name"] for p in market["plugins"]}
        name = mod["name"] if mod["name"] not in names else f"{mod['name']}-{owner.lower()}"
        entry = {
            "name": name,
            "description": mod.get("description") or "",
            "author": {"name": owner, "url": f"https://github.com/{owner}"},
            "homepage": mod["url"],
            "category": "other",
            "tags": ["mod"],
            "source": src,
        }
        if mod.get("license"):
            entry["license"] = mod["license"]
        market["plugins"].append(entry)
    save(MARKET, market)


def commit():
    global timer
    with lock:
        timer = None
        if not pending:
            return
        kept = sum(v == "keep" for v in pending.values())
        skipped = sum(v == "skip" for v in pending.values())
        undone = len(pending) - kept - skipped
        pending.clear()
        git("add", "data/decisions.json", ".claude-plugin/marketplace.json")
        if git("diff", "--cached", "--quiet").returncode == 0:
            return
        parts = [f"keep {kept} mod{'s' * (kept != 1)}" if kept else "",
                 f"skip {skipped}" if skipped else "",
                 f"take back {undone}" if undone else ""]
        subject = ", ".join(p for p in parts if p).capitalize() + " from the inbox"
        git("commit", "-m", subject)
        git("pull", "--rebase", "--autostash")
        git("push")


def decide(mod_id, verdict):
    global timer
    inbox = load(INBOX, {})
    if mod_id not in inbox or verdict not in ("keep", "skip", None):
        return False
    with lock:
        decisions = load(DECISIONS, {})
        if verdict:
            decisions[mod_id] = {"verdict": verdict, "at": datetime.date.today().isoformat()}
        else:
            decisions.pop(mod_id, None)
        save(DECISIONS, decisions)
        set_listed(inbox[mod_id], verdict == "keep")
        pending[mod_id] = verdict
        if timer:
            timer.cancel()
        timer = threading.Timer(IDLE, commit)
        timer.start()
    return True


def readme(mod_id):
    if mod_id in readmes:
        return readmes[mod_id]
    mod = load(INBOX, {}).get(mod_id)
    if not mod:
        return None
    folder = "" if (mod.get("path") or ".") == "." else mod["path"] + "/"
    tries = [folder + n for n in ("README.md", "readme.md", "Readme.md")]
    if folder:
        tries += ["README.md", "readme.md"]
    out = {"markdown": "", "base": ""}
    for path in tries:
        url = f"https://raw.githubusercontent.com/{mod['repo']}/HEAD/{path}"
        try:
            with urllib.request.urlopen(url, timeout=20) as r:
                out = {"markdown": r.read().decode("utf-8", "replace"), "base": url.rsplit("/", 1)[0] + "/",
                       "blob": f"https://github.com/{mod['repo']}/blob/HEAD/{path.rsplit('/', 1)[0] + '/' if '/' in path else ''}"}
            break
        except urllib.error.URLError:
            continue
    readmes[mod_id] = out
    return out


class Handler(BaseHTTPRequestHandler):
    def send(self, code, body, kind="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", kind)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == "/":
            self.send(200, open(PAGE, "rb").read(), "text/html; charset=utf-8")
        elif url.path == "/api/inbox":
            inbox, decisions = load(INBOX, {}), load(DECISIONS, {})
            checked = git("log", "-1", "--format=%cI", "--", "data/inbox.json").stdout.strip()
            mods = [{"id": i, **m, "verdict": decisions.get(i, {}).get("verdict")} for i, m in inbox.items()]
            self.send(200, {"checked": checked, "mods": mods})
        elif url.path == "/api/readme":
            out = readme(urllib.parse.parse_qs(url.query).get("id", [""])[0])
            self.send(200 if out is not None else 404, out or {"error": "unknown mod"})
        else:
            self.send(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/api/decide":
            ok = decide(body.get("id"), body.get("verdict"))
            self.send(200 if ok else 400, {"ok": ok})
        elif self.path == "/api/flush":
            commit()
            self.send(200, {"ok": True})
        elif self.path == "/api/refresh":
            commit()
            with lock:
                ok = git("pull", "--rebase", "--autostash").returncode == 0
            self.send(200, {"ok": ok})
        else:
            self.send(404, {"error": "not found"})


if __name__ == "__main__":
    git("pull", "--rebase", "--autostash")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
