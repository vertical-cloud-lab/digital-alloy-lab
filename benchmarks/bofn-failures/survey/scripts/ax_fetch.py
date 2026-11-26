#!/usr/bin/env python3
"""Fetch all issues or PRs of meta/Ax via GraphQL, streaming to JSONL. Resumable via cursor file.
Usage: python -I fetch.py issues|prs OUTDIR
Token: read from env GH_TOKEN by gh; never printed."""
import json, os, subprocess, sys, time

kind, outdir = sys.argv[1], sys.argv[2]
out_path = os.path.join(outdir, f"{kind}.jsonl")
cur_path = os.path.join(outdir, f"{kind}.cursor")
PAGE = int(os.environ.get("PAGE", "25" if kind == "prs" else "50"))

COMMENT_FIELDS = "author{login} createdAt url body"
ISSUE_Q = """
query($cursor:String,$n:Int!){ repository(owner:"meta",name:"Ax"){ issues(first:$n, after:$cursor, orderBy:{field:CREATED_AT,direction:ASC}){
  pageInfo{hasNextPage endCursor}
  nodes{ number title state stateReason author{login} createdAt closedAt url body
    labels(first:20){nodes{name}}
    comments(first:100){ totalCount pageInfo{hasNextPage endCursor} nodes{ %s } } } } } rateLimit{cost remaining resetAt} }
""" % COMMENT_FIELDS
PR_Q = """
query($cursor:String,$n:Int!){ repository(owner:"meta",name:"Ax"){ pullRequests(first:$n, after:$cursor, orderBy:{field:CREATED_AT,direction:ASC}){
  pageInfo{hasNextPage endCursor}
  nodes{ number title state merged mergedAt author{login} createdAt closedAt url body baseRefName headRefName
    labels(first:20){nodes{name}}
    comments(first:100){ totalCount pageInfo{hasNextPage endCursor} nodes{ %s } }
    reviews(first:30){ totalCount nodes{ author{login} state createdAt url body
       comments(first:30){ totalCount nodes{ author{login} createdAt url body path } } } } } } } rateLimit{cost remaining resetAt} }
""" % COMMENT_FIELDS

def gql(query, variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        if v is None:
            continue
        if isinstance(v, int):
            args += ["-F", f"{k}={v}"]
        else:
            args += ["-f", f"{k}={v}"]
    for attempt in range(6):
        p = subprocess.run(args, capture_output=True, text=True)
        if p.returncode == 0:
            d = json.loads(p.stdout)
            if "errors" not in d:
                return d
            err = json.dumps(d["errors"])[:500]
        else:
            err = (p.stderr or "")[:500]
        print(f"  attempt {attempt} failed: {err}", file=sys.stderr, flush=True)
        time.sleep(5 * (attempt + 1))
    raise SystemExit("giving up")

cursor = open(cur_path).read().strip() if os.path.exists(cur_path) else None
q = ISSUE_Q if kind == "issues" else PR_Q
key = "issues" if kind == "issues" else "pullRequests"
n = PAGE
total = 0
while True:
    try:
        d = gql(q, {"cursor": cursor, "n": n})
    except SystemExit:
        if n > 5:
            n = max(5, n // 2); print(f"reducing page to {n}", file=sys.stderr); continue
        raise
    conn = d["data"]["repository"][key]
    with open(out_path, "a") as f:
        for node in conn["nodes"]:
            f.write(json.dumps(node) + "\n")
    total += len(conn["nodes"])
    rl = d["data"]["rateLimit"]
    last = conn["nodes"][-1]["number"] if conn["nodes"] else None
    print(f"{kind}: +{len(conn['nodes'])} (total {total}, last #{last}) cost={rl['cost']} remaining={rl['remaining']}", flush=True)
    if not conn["pageInfo"]["hasNextPage"]:
        break
    cursor = conn["pageInfo"]["endCursor"]
    with open(cur_path, "w") as f:
        f.write(cursor)
    n = PAGE
print("done", kind, total)
