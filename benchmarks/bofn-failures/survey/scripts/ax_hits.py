#!/usr/bin/env python3
"""Scan issues/PRs JSONL for terms; write hits.tsv and a per-thread text dump.
Usage: python -I hits.py DATADIR OUTDIR"""
import json, os, re, sys
datadir, outdir = sys.argv[1], sys.argv[2]
TERMS = ["failed trial", "mark_failed", "mark_trial_failed", "TrialStatus.FAILED", "abandon",
 "mark_abandoned", "fit_abandoned", "ABANDONED", "EARLY_STOPPED", "early stopping", "early-stopping", "STALE",
 "AddExecutionViability", "execution viability", "viability", "infeasible", "unknown constraint",
 "crash", "failure rate", "tolerated_trial_failure_rate", "FailureRateExceeded", "retry",
 "missing metric", "partial data", "complete_trial", "fit_out_of_design", "out of design", "out-of-design",
 "pending", "X_pending", "get_pending_observation_features", "outcome constraint", "feasibility",
 "classifier", "classification", "function network", "BOFN", "EIFN", "pKGFN", "composite", "multi-stage", "multistage",
 "cascade", "sequential stage", "MapData", "learning curve", "attach_trial", "manual", "deviat",
 "failed_reason", "status_reason", "mark_trial_abandoned", "mark_trial_early_stopped", "log_trial_failure",
 "MetricAvailability", "missing data", "NaN", "black-box constraint", "hidden constraint", "unknown constraints",
 "failure region", "trial failure", "failed trials", "fails", "unsuccessful", "Scheduler", "Orchestrator"]
CORE = ["failed trial", "failed trials", "trial failure", "mark_failed", "mark_trial_failed", "TrialStatus.FAILED",
 "abandon", "fit_abandoned", "EARLY_STOPPED", "STALE", "AddExecutionViability", "viability", "unknown constraint",
 "unknown constraints", "hidden constraint", "black-box constraint", "failure region", "failure rate",
 "tolerated_trial_failure_rate", "FailureRateExceeded", "missing metric", "partial data", "fit_out_of_design",
 "get_pending_observation_features", "X_pending", "function network", "BOFN", "EIFN", "pKGFN", "multi-stage", "multistage",
 "cascade", "sequential stage", "log_trial_failure", "failed_reason", "status_reason", "MetricAvailability",
 "mark_trial_abandoned", "mark_trial_early_stopped"]
pats = {t: re.compile(re.escape(t), re.I) for t in TERMS}
# 'STALE' should be case-sensitive-ish to avoid 'stale' noise? keep both: separate
pats["STALE"] = re.compile(r"\bSTALE\b")
pats["stale"] = re.compile(r"\bstale\b", re.I)
pats["NaN"] = re.compile(r"\bNaN\b")
rows = []
os.makedirs(os.path.join(outdir, "threads"), exist_ok=True)
for kind, fn in (("issue", "issues.jsonl"), ("pr", "prs.jsonl")):
    p = os.path.join(datadir, fn)
    if not os.path.exists(p):
        continue
    for line in open(p):
        d = json.loads(line)
        parts = [d.get("title") or "", d.get("body") or ""]
        authors = {(d.get("author") or {}).get("login")}
        for c in (d.get("comments") or {}).get("nodes", []):
            parts.append(c.get("body") or ""); authors.add((c.get("author") or {}).get("login"))
        for r in (d.get("reviews") or {}).get("nodes", []) if kind == "pr" else []:
            parts.append(r.get("body") or ""); authors.add((r.get("author") or {}).get("login"))
            for rc in (r.get("comments") or {}).get("nodes", []):
                parts.append(rc.get("body") or ""); authors.add((rc.get("author") or {}).get("login"))
        text = "\n".join(parts)
        matched = {t: len(pt.findall(text)) for t, pt in pats.items()}
        matched = {t: n for t, n in matched.items() if n}
        if not matched:
            continue
        core = sum(n for t, n in matched.items() if t in CORE)
        rows.append((kind, d["number"], d["url"], d.get("state"), d.get("merged"), (d.get("title") or "").replace("\t", " "),
                     core, "sgbaird" in authors, ";".join(f"{t}:{n}" for t, n in sorted(matched.items(), key=lambda x: -x[1]))))
rows.sort(key=lambda r: -r[6])
with open(os.path.join(outdir, "hits.tsv"), "w") as f:
    f.write("repo\tkind\tnumber\turl\tstate\tmerged\ttitle\tcore_score\tsgbaird_involved\tmatched_terms\n")
    for r in rows:
        f.write("meta/Ax\t" + "\t".join(str(x) for x in r) + "\n")
print(len(rows), "threads with hits")
