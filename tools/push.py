"""Upload files to the prep-binder GitHub repo through the GitHub API.
Usage:  GITHUB_TOKEN=<your-token> python3 push.py "commit message" local/path=repo/path [more=pairs]
The token is read from the environment; never commit it to the repo."""
import sys, os, json, base64, urllib.request
TOKEN = os.environ.get("GITHUB_TOKEN") or sys.exit("Set GITHUB_TOKEN first")
REPO = os.environ.get("GITHUB_REPO", "shreyashtiwari06/prep-binder")
def api(method, path, body=None):
    req = urllib.request.Request(f"https://api.github.com/repos/{REPO}/contents/{path}", method=method,
        data=json.dumps(body).encode() if body else None,
        headers={"Authorization": "Bearer " + TOKEN, "Accept": "application/vnd.github+json"})
    try:
        with urllib.request.urlopen(req) as r: return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404: return None
        sys.exit(f"{e.code} {e.read()[:300]}")
def put(local, remote, msg):
    cur = api("GET", remote)
    body = {"message": msg, "content": base64.b64encode(open(local, "rb").read()).decode(), "branch": "main"}
    if cur: body["sha"] = cur["sha"]
    r = api("PUT", remote, body); print(remote, "->", r["commit"]["sha"][:7])
for arg in sys.argv[2:]:
    local, remote = arg.split("=")
    put(local, remote, sys.argv[1])
