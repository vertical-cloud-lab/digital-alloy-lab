#!/usr/bin/env python3
"""Bulk-fetch issues, PRs, and discussions (with comments) from GitHub GraphQL into JSONL.
Uses `gh api graphql --input -`, token taken from env var GH_TOKEN set by caller (never printed)."""
import json, subprocess, sys, time, os

OWNER, NAME = "meta-pytorch", "botorch"
OUT = "/tmp/research/botorch/raw"

def gql(query, variables, retries=6):
    payload = json.dumps({"query": query, "variables": variables})
    for attempt in range(retries):
        p = subprocess.run(["gh", "api", "graphql", "--input", "-"], input=payload,
                           capture_output=True, text=True)
        if p.returncode == 0:
            d = json.loads(p.stdout)
            if "errors" in d and not d.get("data"):
                print("GraphQL errors:", json.dumps(d["errors"])[:500], file=sys.stderr)
                time.sleep(10 * (attempt + 1))
                continue
            return d["data"]
        print(f"gh error (attempt {attempt}): {p.stderr[:400]}", file=sys.stderr)
        time.sleep(15 * (attempt + 1))
    raise RuntimeError("GraphQL failed repeatedly")

COMMENT_FIELDS = "author { login } createdAt url body"

ISSUE_Q = """
query($owner:String!, $name:String!, $cursor:String) {
  rateLimit { cost remaining resetAt }
  repository(owner:$owner, name:$name) {
    issues(first: 40, after: $cursor, orderBy:{field:CREATED_AT, direction:ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title state stateReason createdAt closedAt url body
        author { login }
        labels(first: 20) { nodes { name } }
        comments(first: 100) { pageInfo { hasNextPage endCursor } nodes { %s } }
      }
    }
  }
}""" % COMMENT_FIELDS

PR_Q = """
query($owner:String!, $name:String!, $cursor:String) {
  rateLimit { cost remaining resetAt }
  repository(owner:$owner, name:$name) {
    pullRequests(first: 20, after: $cursor, orderBy:{field:CREATED_AT, direction:ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title state merged mergedAt createdAt closedAt url body baseRefName headRefName
        author { login }
        labels(first: 20) { nodes { name } }
        comments(first: 100) { pageInfo { hasNextPage endCursor } nodes { %s } }
        reviews(first: 40) { pageInfo { hasNextPage endCursor } nodes { author { login } createdAt url body state
            comments(first: 40) { nodes { author { login } createdAt url body path } } } }
      }
    }
  }
}""" % COMMENT_FIELDS

MORE_COMMENTS_Q = """
query($id:ID!, $cursor:String) {
  node(id:$id) {
    ... on Issue { comments(first:100, after:$cursor) { pageInfo { hasNextPage endCursor } nodes { %s } } }
    ... on PullRequest { comments(first:100, after:$cursor) { pageInfo { hasNextPage endCursor } nodes { %s } } }
  }
}""" % (COMMENT_FIELDS, COMMENT_FIELDS)

DISC_Q = """
query($owner:String!, $name:String!, $cursor:String) {
  rateLimit { cost remaining resetAt }
  repository(owner:$owner, name:$name) {
    discussions(first: 25, after: $cursor, orderBy:{field:CREATED_AT, direction:ASC}) {
      pageInfo { hasNextPage endCursor }
      nodes {
        number title createdAt closed url body
        author { login }
        category { name }
        answer { author { login } url }
        comments(first: 60) { pageInfo { hasNextPage endCursor } nodes { author { login } createdAt url body
           replies(first: 40) { nodes { author { login } createdAt url body } } } }
      }
    }
  }
}"""

def login(a):
    return (a or {}).get("login") if isinstance(a, dict) or a is None else a

def norm_comments(nodes):
    return [{"author": login(c.get("author")), "createdAt": c["createdAt"], "url": c["url"], "body": c["body"]} for c in nodes]

def fetch_issues_or_prs(kind):
    q = ISSUE_Q if kind == "issues" else PR_Q
    out_path = os.path.join(OUT, f"{kind}.jsonl")
    f = open(out_path, "w")
    cursor, n = None, 0
    while True:
        d = gql(q, {"owner": OWNER, "name": NAME, "cursor": cursor})
        rl = d["rateLimit"]
        conn = d["repository"]["issues" if kind == "issues" else "pullRequests"]
        for node in conn["nodes"]:
            comments = node["comments"]["nodes"]
            pi = node["comments"]["pageInfo"]
            if pi["hasNextPage"]:
                # need node id; refetch by number
                idq = """query($owner:String!, $name:String!, $num:Int!) { repository(owner:$owner, name:$name) { issueOrPullRequest(number:$num) { ... on Issue { id } ... on PullRequest { id } } } }"""
                nid = gql(idq, {"owner": OWNER, "name": NAME, "num": node["number"]})["repository"]["issueOrPullRequest"]["id"]
                c2 = pi["endCursor"]
                while True:
                    dd = gql(MORE_COMMENTS_Q, {"id": nid, "cursor": c2})["node"]["comments"]
                    comments.extend(dd["nodes"])
                    if not dd["pageInfo"]["hasNextPage"]:
                        break
                    c2 = dd["pageInfo"]["endCursor"]
            rec = {
                "type": "issue" if kind == "issues" else "pr",
                "number": node["number"], "title": node["title"], "state": node["state"],
                "merged": node.get("merged"), "mergedAt": node.get("mergedAt"),
                "stateReason": node.get("stateReason"),
                "author": login(node.get("author")), "createdAt": node["createdAt"],
                "closedAt": node.get("closedAt"), "url": node["url"], "body": node["body"],
                "labels": [l["name"] for l in node["labels"]["nodes"]],
                "comments": norm_comments(comments),
            }
            if kind == "prs":
                rec["baseRefName"] = node.get("baseRefName"); rec["headRefName"] = node.get("headRefName")
                revs = []
                for r in node["reviews"]["nodes"]:
                    revs.append({"author": login(r.get("author")), "createdAt": r["createdAt"], "url": r["url"],
                                 "body": r["body"], "state": r["state"],
                                 "comments": [{"author": login(c.get("author")), "createdAt": c["createdAt"],
                                               "url": c["url"], "body": c["body"], "path": c.get("path")}
                                              for c in r["comments"]["nodes"]]})
                rec["reviews"] = revs
                rec["reviews_truncated"] = node["reviews"]["pageInfo"]["hasNextPage"]
            f.write(json.dumps(rec) + "\n"); n += 1
        f.flush()
        print(f"{kind}: {n} fetched; cost={rl['cost']} remaining={rl['remaining']}", file=sys.stderr, flush=True)
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
        if rl["remaining"] < 200:
            print("rate limit low; sleeping 300s", file=sys.stderr); time.sleep(300)
    f.close()

def fetch_discussions():
    out_path = os.path.join(OUT, "discussions.jsonl")
    f = open(out_path, "w")
    cursor, n = None, 0
    while True:
        d = gql(DISC_Q, {"owner": OWNER, "name": NAME, "cursor": cursor})
        rl = d["rateLimit"]; conn = d["repository"]["discussions"]
        for node in conn["nodes"]:
            comments = []
            for c in node["comments"]["nodes"]:
                comments.append({"author": login(c.get("author")), "createdAt": c["createdAt"], "url": c["url"], "body": c["body"]})
                for r in c["replies"]["nodes"]:
                    comments.append({"author": login(r.get("author")), "createdAt": r["createdAt"], "url": r["url"], "body": r["body"], "reply": True})
            rec = {"type": "discussion", "number": node["number"], "title": node["title"],
                   "state": "CLOSED" if node["closed"] else "OPEN", "author": login(node.get("author")),
                   "createdAt": node["createdAt"], "url": node["url"], "body": node["body"],
                   "category": (node.get("category") or {}).get("name"),
                   "answer": node.get("answer") and {"author": login(node["answer"].get("author")), "url": node["answer"]["url"]},
                   "comments": comments, "comments_truncated": node["comments"]["pageInfo"]["hasNextPage"]}
            f.write(json.dumps(rec) + "\n"); n += 1
        f.flush()
        print(f"discussions: {n} fetched; cost={rl['cost']} remaining={rl['remaining']}", file=sys.stderr, flush=True)
        if not conn["pageInfo"]["hasNextPage"]:
            break
        cursor = conn["pageInfo"]["endCursor"]
    f.close()

if __name__ == "__main__":
    which = sys.argv[1:] or ["issues", "prs", "discussions"]
    for w in which:
        if w == "discussions":
            fetch_discussions()
        else:
            fetch_issues_or_prs(w)
