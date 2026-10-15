#!/usr/bin/env python3
"""
Extract all PR/issue comments, commits, and Edison trajectory IDs
from the digital-alloy-lab-private repo for Kosmos context upload.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime

REPO = "vertical-cloud-lab/digital-alloy-lab-private"
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

PR_NUMBERS = [
    52,
    51,
    49,
    46,
    44,
    42,
    40,
    38,
    36,
    34,
    32,
    30,
    28,
    26,
    24,
    22,
    20,
    18,
    16,
    14,
    12,
    10,
    8,
    6,
    4,
    2,
]
ISSUE_NUMBERS = [
    53,
    50,
    48,
    47,
    45,
    43,
    41,
    39,
    37,
    35,
    33,
    31,
    29,
    27,
    25,
    23,
    21,
    19,
    17,
    15,
    13,
    11,
    9,
    7,
    5,
    3,
    1,
]

EDISON_ID_RE = re.compile(r"\b([0-9a-f]{8})\b")  # 8-hex task IDs like 400210a0


def gh(*args):
    result = subprocess.run(["gh", *args], capture_output=True, text=True)
    if result.returncode != 0:
        print(
            f"  WARNING: gh {' '.join(args[:4])} failed: {result.stderr[:200]}",
            file=sys.stderr,
        )
        return None
    return result.stdout.strip()


def gh_json(*args):
    out = gh(*args)
    if out is None:
        return None
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        print(f"  WARNING: JSON parse failed: {e}", file=sys.stderr)
        return None


def extract_edison_ids(text):
    if not text:
        return []
    return list(set(EDISON_ID_RE.findall(text)))


def fetch_pr(number):
    print(f"  Fetching PR #{number}...")
    meta = gh_json(
        "pr",
        "view",
        str(number),
        "--repo",
        REPO,
        "--json",
        "number,title,state,author,createdAt,updatedAt,mergedAt,"
        "headRefName,baseRefName,body,labels,milestone",
    )
    if meta is None:
        meta = {"number": number, "error": "fetch_failed"}

    # Issue-style comments on the PR
    comments = (
        gh_json("pr", "view", str(number), "--repo", REPO, "--json", "comments") or {}
    )
    meta["comments"] = comments.get("comments", [])

    # Review comments (inline code comments)
    review_comments_raw = gh(
        "api", f"repos/{REPO}/pulls/{number}/comments", "--paginate"
    )
    if review_comments_raw:
        try:
            meta["review_comments"] = json.loads(review_comments_raw)
        except Exception:
            meta["review_comments"] = []
    else:
        meta["review_comments"] = []

    # Reviews (approve/request-changes with bodies)
    reviews_raw = gh("api", f"repos/{REPO}/pulls/{number}/reviews", "--paginate")
    if reviews_raw:
        try:
            meta["reviews"] = json.loads(reviews_raw)
        except Exception:
            meta["reviews"] = []
    else:
        meta["reviews"] = []

    # Commits on the PR
    commits_raw = gh("api", f"repos/{REPO}/pulls/{number}/commits", "--paginate")
    if commits_raw:
        try:
            raw_commits = json.loads(commits_raw)
            meta["pr_commits"] = [
                {
                    "sha": c.get("sha", ""),
                    "message": c.get("commit", {}).get("message", ""),
                    "author": c.get("commit", {}).get("author", {}),
                    "committer": c.get("commit", {}).get("committer", {}),
                    "url": c.get("html_url", ""),
                }
                for c in raw_commits
            ]
        except Exception:
            meta["pr_commits"] = []
    else:
        meta["pr_commits"] = []

    # Collect all Edison IDs from body + comments + reviews
    all_text = [meta.get("body") or ""]
    for c in meta.get("comments", []):
        all_text.append(c.get("body") or "")
    for c in meta.get("review_comments", []):
        all_text.append(c.get("body") or "")
    for r in meta.get("reviews", []):
        all_text.append(r.get("body") or "")
    for c in meta.get("pr_commits", []):
        all_text.append(c.get("message") or "")

    meta["edison_task_ids"] = extract_edison_ids(" ".join(all_text))

    return meta


def fetch_issue(number):
    print(f"  Fetching issue #{number}...")
    meta = gh_json(
        "issue",
        "view",
        str(number),
        "--repo",
        REPO,
        "--json",
        "number,title,state,author,createdAt,updatedAt,body,labels,milestone",
    )
    if meta is None:
        meta = {"number": number, "error": "fetch_failed"}

    comments = (
        gh_json("issue", "view", str(number), "--repo", REPO, "--json", "comments")
        or {}
    )
    meta["comments"] = comments.get("comments", [])

    all_text = [meta.get("body") or ""]
    for c in meta.get("comments", []):
        all_text.append(c.get("body") or "")

    meta["edison_task_ids"] = extract_edison_ids(" ".join(all_text))

    return meta


def fetch_commits():
    print("  Fetching full commit history (git log --all)...")
    return []  # replaced by fetch_commits_per_branch below


def fetch_commits_per_branch():
    """Use git log --all to extract all commits across all branches from local clone."""
    import subprocess as _sp

    REPO_DIR = os.path.dirname(OUT_DIR)  # /workspaces/digital-alloy-lab-private

    # Fetch all remote refs so we have complete history
    _sp.run(["git", "fetch", "--all", "--quiet"], cwd=REPO_DIR, capture_output=True)

    # --format uses %x00 (null) as field separator to safely handle newlines in bodies
    result = _sp.run(
        [
            "git",
            "log",
            "--all",
            "--no-merges",
            "--format=%H%x00%an%x00%ae%x00%ai%x00%cn%x00%ci%x00%D%x00%B%x01",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )
    if result.returncode != 0:
        print(f"  WARNING: git log failed: {result.stderr[:200]}", file=sys.stderr)
        return []

    # Also include merge commits
    result2 = _sp.run(
        [
            "git",
            "log",
            "--all",
            "--merges",
            "--format=%H%x00%an%x00%ae%x00%ai%x00%cn%x00%ci%x00%D%x00%B%x01",
        ],
        capture_output=True,
        text=True,
        cwd=REPO_DIR,
    )

    raw = result.stdout
    if result2.returncode == 0:
        raw += result2.stdout

    entries = raw.split("\x01")
    all_commits = {}
    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        parts = entry.split("\x00", 7)
        if len(parts) < 8:
            continue
        (
            sha,
            author_name,
            author_email,
            author_date,
            committer_name,
            committer_date,
            refs,
            body,
        ) = parts
        sha = sha.strip()
        body = body.strip()
        if not sha or sha in all_commits:
            continue

        # Build short URL
        url = f"https://github.com/{REPO}/commit/{sha}"

        # Branches/tags from refs decoration
        branch_tags = (
            [r.strip() for r in refs.split(",") if r.strip()] if refs.strip() else []
        )

        all_commits[sha] = {
            "sha": sha,
            "message": body,
            "subject": body.split("\n")[0][:120],
            "author": {"name": author_name, "email": author_email, "date": author_date},
            "committer": {"name": committer_name, "date": committer_date},
            "refs": branch_tags,
            "url": url,
            "edison_task_ids": extract_edison_ids(body),
        }

    # Sort newest-first by author date
    commits = sorted(
        all_commits.values(), key=lambda c: c["author"]["date"], reverse=True
    )
    return commits


def build_edison_index(prs, issues, commits):
    """Build a consolidated index of all Edison task IDs found."""
    index = {}  # task_id -> list of references

    for pr in prs:
        for tid in pr.get("edison_task_ids", []):
            index.setdefault(tid, []).append(
                {
                    "type": "pr",
                    "number": pr.get("number"),
                    "title": pr.get("title", ""),
                }
            )

    for issue in issues:
        for tid in issue.get("edison_task_ids", []):
            index.setdefault(tid, []).append(
                {
                    "type": "issue",
                    "number": issue.get("number"),
                    "title": issue.get("title", ""),
                }
            )

    for c in commits:
        for tid in c.get("edison_task_ids", []):
            index.setdefault(tid, []).append(
                {
                    "type": "commit",
                    "sha": c.get("sha", "")[:12],
                    "message": c.get("message", "").split("\n")[0][:80],
                }
            )

    # Also scan all markdown files in edison-trajectories/
    traj_dir = os.path.join(os.path.dirname(OUT_DIR), "edison-trajectories")
    if os.path.isdir(traj_dir):
        for fname in os.listdir(traj_dir):
            if fname.endswith(".md"):
                fpath = os.path.join(traj_dir, fname)
                try:
                    with open(fpath) as f:
                        content = f.read()
                    for tid in set(EDISON_ID_RE.findall(content)):
                        index.setdefault(tid, []).append(
                            {
                                "type": "trajectory_file",
                                "file": fname,
                            }
                        )
                except Exception:
                    pass

    return index


def write_summary_md(prs, issues, commits, edison_index):
    lines = [
        "# FLAIME Repository Context for Kosmos Upload",
        f"\nGenerated: {datetime.utcnow().isoformat()}Z",
        f"\nRepository: {REPO}",
        "",
        "---",
        "",
        f"## Summary",
        f"- **Pull Requests**: {len(prs)}",
        f"- **Issues**: {len(issues)}",
        f"- **Unique Commits**: {len(commits)}",
        f"- **Unique Edison Task IDs found**: {len(edison_index)}",
        "",
        "### Files in this package",
        "| File | Contents |",
        "|------|----------|",
        "| `prs_metadata.json` | All PR metadata, bodies, comments, review comments, inline code review comments |",
        "| `issues_metadata.json` | All issue metadata, bodies, and comments |",
        "| `commits_all.json` | All commits across all branches with messages and authors |",
        "| `edison_task_index.json` | Index of Edison task IDs → where they appear |",
        "| `pr_comments_flat.json` | All PR comments flattened (one record per comment) |",
        "| `issue_comments_flat.json` | All issue comments flattened |",
        "| `review_comments_flat.json` | All inline code review comments flattened |",
        "",
        "---",
        "",
        "## Pull Requests",
        "",
    ]

    for pr in sorted(prs, key=lambda x: x.get("number", 0)):
        n = pr.get("number", "?")
        title = pr.get("title", "(no title)")
        state = pr.get("state", "?")
        author = pr.get("author", {})
        author_login = (
            author.get("login", "?") if isinstance(author, dict) else str(author)
        )
        created = pr.get("createdAt", "?")
        merged = pr.get("mergedAt") or "—"
        n_comments = len(pr.get("comments", []))
        n_review_comments = len(pr.get("review_comments", []))
        n_reviews = len(pr.get("reviews", []))
        n_commits = len(pr.get("pr_commits", []))
        edison_ids = pr.get("edison_task_ids", [])

        lines.append(f"### PR #{n}: {title}")
        lines.append(f"- **State**: {state}")
        lines.append(f"- **Author**: @{author_login}")
        lines.append(f"- **Created**: {created}  |  **Merged**: {merged}")
        lines.append(
            f"- **Branch**: `{pr.get('headRefName','?')}` → `{pr.get('baseRefName','?')}`"
        )
        lines.append(
            f"- **Comments**: {n_comments} general, {n_review_comments} inline, {n_reviews} reviews"
        )
        lines.append(f"- **Commits in PR**: {n_commits}")
        if edison_ids:
            lines.append(f"- **Edison Task IDs**: `{'`, `'.join(edison_ids)}`")
        lines.append("")

        # Body excerpt
        body = (pr.get("body") or "").strip()
        if body:
            excerpt = body[:800].replace("\n", "\n  ")
            lines.append(f"  **Description excerpt**:\n  {excerpt}")
            if len(body) > 800:
                lines.append(f"  *(truncated — full body in prs_metadata.json)*")
        lines.append("")

        # Commits
        if pr.get("pr_commits"):
            lines.append(f"  **Commits**:")
            for c in pr["pr_commits"]:
                sha = c.get("sha", "")[:10]
                msg = (c.get("message") or c.get("subject") or "").split("\n")[0][:100]
                author_obj = c.get("author", {})
                author_name = (
                    author_obj.get("name", "?") if isinstance(author_obj, dict) else "?"
                )
                date = (
                    author_obj.get("date", "?") if isinstance(author_obj, dict) else "?"
                )
                lines.append(f"  - `{sha}` — {msg} *(by {author_name} on {date})*")
            lines.append("")

        # Comments
        for comment in pr.get("comments", []):
            c_author = comment.get("author", {})
            c_login = (
                c_author.get("login", "?")
                if isinstance(c_author, dict)
                else str(c_author)
            )
            c_date = comment.get("createdAt", "?")
            c_body = (comment.get("body") or "").strip()[:600]
            lines.append(f"  **Comment by @{c_login} on {c_date}**:")
            lines.append(f"  > {c_body.replace(chr(10), chr(10)+'  > ')}")
            lines.append("")

    lines += [
        "---",
        "",
        "## Issues",
        "",
    ]

    for issue in sorted(issues, key=lambda x: x.get("number", 0)):
        n = issue.get("number", "?")
        title = issue.get("title", "(no title)")
        state = issue.get("state", "?")
        author = issue.get("author", {})
        author_login = (
            author.get("login", "?") if isinstance(author, dict) else str(author)
        )
        created = issue.get("createdAt", "?")
        n_comments = len(issue.get("comments", []))
        edison_ids = issue.get("edison_task_ids", [])

        lines.append(f"### Issue #{n}: {title}")
        lines.append(f"- **State**: {state}")
        lines.append(f"- **Author**: @{author_login}")
        lines.append(f"- **Created**: {created}")
        lines.append(f"- **Comments**: {n_comments}")
        if edison_ids:
            lines.append(f"- **Edison Task IDs**: `{'`, `'.join(edison_ids)}`")
        lines.append("")

        body = (issue.get("body") or "").strip()
        if body:
            excerpt = body[:800].replace("\n", "\n  ")
            lines.append(f"  **Description excerpt**:\n  {excerpt}")
            if len(body) > 800:
                lines.append(f"  *(truncated — full body in issues_metadata.json)*")
        lines.append("")

        for comment in issue.get("comments", []):
            c_author = comment.get("author", {})
            c_login = (
                c_author.get("login", "?")
                if isinstance(c_author, dict)
                else str(c_author)
            )
            c_date = comment.get("createdAt", "?")
            c_body = (comment.get("body") or "").strip()[:600]
            lines.append(f"  **Comment by @{c_login} on {c_date}**:")
            lines.append(f"  > {c_body.replace(chr(10), chr(10)+'  > ')}")
            lines.append("")

    lines += [
        "---",
        "",
        "## Edison Task ID Index",
        "",
        "IDs that appear to be Edison Scientific task UUIDs (8-char hex), found in PR/issue bodies, comments, and commit messages.",
        "",
        "| Task ID | Appears In |",
        "|---------|-----------|",
    ]

    for tid, refs in sorted(edison_index.items()):
        refs_str = "; ".join(
            (
                f"PR #{r['number']}"
                if r["type"] == "pr"
                else (
                    f"Issue #{r['number']}"
                    if r["type"] == "issue"
                    else (
                        f"commit {r.get('sha','')[:8]}"
                        if r["type"] == "commit"
                        else f"file {r.get('file','')}"
                    )
                )
            )
            for r in refs[:5]
        )
        if len(refs) > 5:
            refs_str += f" (+{len(refs)-5} more)"
        lines.append(f"| `{tid}` | {refs_str} |")

    lines += [
        "",
        "---",
        "",
        "## Commit History (most recent first)",
        "",
    ]

    for c in commits[:200]:  # cap at 200 in the markdown
        sha = c.get("sha", "")[:10]
        msg = (c.get("subject") or c.get("message") or "").split("\n")[0][:100]
        author_obj = c.get("author", {})
        author_name = (
            author_obj.get("name", "?") if isinstance(author_obj, dict) else "?"
        )
        date = author_obj.get("date", "?") if isinstance(author_obj, dict) else "?"
        eids = c.get("edison_task_ids", [])
        eid_str = f" `{'` `'.join(eids)}`" if eids else ""
        lines.append(f"- `{sha}` **{msg}** — {author_name} ({date}){eid_str}")

    if len(commits) > 200:
        lines.append(
            f"\n*(showing 200 of {len(commits)} commits — see commits_all.json for full list)*"
        )

    return "\n".join(lines)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    print("=== Fetching Pull Requests ===")
    prs = []
    for n in PR_NUMBERS:
        pr = fetch_pr(n)
        prs.append(pr)

    print("\n=== Fetching Issues ===")
    issues = []
    for n in ISSUE_NUMBERS:
        issue = fetch_issue(n)
        issues.append(issue)

    print("\n=== Fetching Commits (all branches) ===")
    commits = fetch_commits_per_branch()
    print(f"  Found {len(commits)} unique commits")

    print("\n=== Building Edison Task ID Index ===")
    edison_index = build_edison_index(prs, issues, commits)
    print(f"  Found {len(edison_index)} unique Edison task IDs")

    # --- Save JSON files ---
    with open(os.path.join(OUT_DIR, "prs_metadata.json"), "w") as f:
        json.dump(prs, f, indent=2, default=str)
    print("  Saved prs_metadata.json")

    with open(os.path.join(OUT_DIR, "issues_metadata.json"), "w") as f:
        json.dump(issues, f, indent=2, default=str)
    print("  Saved issues_metadata.json")

    with open(os.path.join(OUT_DIR, "commits_all.json"), "w") as f:
        json.dump(commits, f, indent=2, default=str)
    print("  Saved commits_all.json")

    with open(os.path.join(OUT_DIR, "edison_task_index.json"), "w") as f:
        json.dump(edison_index, f, indent=2, default=str)
    print("  Saved edison_task_index.json")

    # --- Flat comment files ---
    pr_comments_flat = []
    issue_comments_flat = []
    review_comments_flat = []

    for pr in prs:
        pr_num = pr.get("number")
        pr_title = pr.get("title", "")
        for c in pr.get("comments", []):
            pr_comments_flat.append(
                {
                    "pr_number": pr_num,
                    "pr_title": pr_title,
                    **{k: v for k, v in c.items()},
                }
            )
        for c in pr.get("review_comments", []):
            review_comments_flat.append(
                {
                    "pr_number": pr_num,
                    "pr_title": pr_title,
                    "comment_type": "inline_review",
                    "id": c.get("id"),
                    "author": c.get("user", {}).get("login"),
                    "created_at": c.get("created_at"),
                    "updated_at": c.get("updated_at"),
                    "body": c.get("body"),
                    "path": c.get("path"),
                    "line": c.get("line"),
                    "diff_hunk": c.get("diff_hunk"),
                    "url": c.get("html_url"),
                }
            )
        for r in pr.get("reviews", []):
            if r.get("body", "").strip():
                review_comments_flat.append(
                    {
                        "pr_number": pr_num,
                        "pr_title": pr_title,
                        "comment_type": "review_summary",
                        "id": r.get("id"),
                        "author": r.get("user", {}).get("login"),
                        "submitted_at": r.get("submitted_at"),
                        "state": r.get("state"),
                        "body": r.get("body"),
                        "url": r.get("html_url"),
                    }
                )

    for issue in issues:
        issue_num = issue.get("number")
        issue_title = issue.get("title", "")
        for c in issue.get("comments", []):
            issue_comments_flat.append(
                {
                    "issue_number": issue_num,
                    "issue_title": issue_title,
                    **{k: v for k, v in c.items()},
                }
            )

    with open(os.path.join(OUT_DIR, "pr_comments_flat.json"), "w") as f:
        json.dump(pr_comments_flat, f, indent=2, default=str)
    print("  Saved pr_comments_flat.json")

    with open(os.path.join(OUT_DIR, "issue_comments_flat.json"), "w") as f:
        json.dump(issue_comments_flat, f, indent=2, default=str)
    print("  Saved issue_comments_flat.json")

    with open(os.path.join(OUT_DIR, "review_comments_flat.json"), "w") as f:
        json.dump(review_comments_flat, f, indent=2, default=str)
    print("  Saved review_comments_flat.json")

    # --- Summary markdown ---
    md = write_summary_md(prs, issues, commits, edison_index)
    with open(os.path.join(OUT_DIR, "CONTEXT_SUMMARY.md"), "w") as f:
        f.write(md)
    print("  Saved CONTEXT_SUMMARY.md")

    print(f"\n=== Done. Output in {OUT_DIR} ===")
    sizes = []
    for fname in os.listdir(OUT_DIR):
        fpath = os.path.join(OUT_DIR, fname)
        if os.path.isfile(fpath) and not fname.endswith(".py"):
            sizes.append((fname, os.path.getsize(fpath)))
    for fname, size in sorted(sizes):
        print(f"  {fname:40s}  {size/1024:.1f} KB")


if __name__ == "__main__":
    main()
