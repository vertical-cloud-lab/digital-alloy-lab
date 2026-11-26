#!/usr/bin/env python3
"""Search all fetched JSONL records for research terms; write hits.tsv and a per-record score table."""
import json, re, sys, collections

RAW = "/tmp/research/botorch/raw"
TERMS = {
    "failed": r"\bfailed\b", "failure": r"\bfailures?\b", "crash": r"\bcrash(es|ed|ing)?\b",
    "unknown constraint": r"unknown[- ]constraints?", "feasibility": r"feasibility",
    "feasible": r"\bfeasible\b", "infeasible": r"\binfeasib", "classifier": r"classifiers?\b",
    "classification": r"classification", "probability of feasibility": r"probabilit(y|ies) of feasibility",
    "constrained EI": r"constrained[ _-]?(expected[ _-]?improvement|EI)\b|\bcEI\b",
    "ConstrainedMCObjective": r"ConstrainedMCObjective", "constraints=": r"constraints\s*=",
    "eta": r"\beta\b", "fat": r"\bfat\b|fatmoid", "get_infeasible_cost": r"get_infeasible_cost|infeasible_cost",
    "NaN": r"\bnans?\b", "missing data": r"missing (data|values|observations)",
    "missing outputs": r"missing (outputs?|outcomes?)", "heterotopic": r"heterotopic|isotopic",
    "ModelListGP different training sets": r"ModelListGP.{0,300}(different|separate|varying|distinct).{0,60}(training|inputs|train_X|X)|(different|separate|distinct) (training (sets|data|inputs)|train_X)",
    "function network": r"function[- ]networks?", "BOFN": r"\bBOFN\b", "EIFN": r"\bEIFN\b", "KGFN": r"\bKGFN\b",
    "pKGFN": r"\bp-?KGFN\b", "partial evaluation": r"partial(ly)? evaluat|partial (observation|feedback)s?",
    "composite": r"\bcomposite\b", "GenericDeterministicModel": r"GenericDeterministicModel",
    "cascade": r"\bcascad", "multi-stage": r"multi[- ]?stage|multistage|two[- ]stage",
    "cost-aware": r"cost[- ]aware|cost[- ]sensitive|InverseCostWeighted", "X_pending": r"X_pending",
    "pending points": r"pending (points?|evaluations?|trials?)", "async": r"\basync(hronous)?\b",
    "fantasize": r"fantasi[sz]", "abandoned": r"\babandon", "Ax trial": r"\bAx\b.{0,40}\btrials?\b|\btrials?\b.{0,40}\bAx\b",
    "safe": r"\bsafe\b|safe[- ]?(BO|bayesian|optimization|exploration)", "SafeOpt": r"safe[- ]?opt",
    "hidden constraint": r"hidden constraints?", "black-box constraint": r"black[- ]?box constraints?",
    "SkewGP": r"skew[- ]?GP|skew[- ]?gaussian|unified skew", "variational": r"variational",
    "Dirichlet": r"dirichlet", "Bernoulli": r"bernoulli", "binary": r"\bbinary\b",
    "PoF": r"\bPoF\b|\bPOF\b", "qLogPoF": r"qLogPoF|qLogProbabilityOfFeasibility", "LogPoF": r"\bLogPoF\b|LogProbabilityOfFeasibility",
    "ProbabilityOfFeasibility": r"ProbabilityOfFeasibility", "MultiTask": r"multi[- ]?task",
    "transfer": r"transfer[- ]learning|\btransfer\b", "warm start": r"warm[- ]?start", "botorch_community": r"botorch_community|botorch community",
    # extras
    "outcome constraint": r"outcome constraints?", "censor": r"censor", "dropout/out-of-bounds": r"out[- ]of[- ]bounds? (outcome|observation)",
    "base_samples": r"base_samples", "rsample_from_base_samples": r"rsample_from_base_samples",
    "shape is invalid": r"is invalid for input of size", "GPNetwork": r"gp[- _]?network|gaussianprocessnetwork|process network",
    "DecoupledAcquisition": r"decoupled", "evaluation_mask": r"evaluation_mask",
    "preference/binary outcome": r"binary (outcome|feedback|response)s?", "ApproximateGP": r"ApproximateGP|SingleTaskVariationalGP",
    "BernoulliLikelihood": r"BernoulliLikelihood", "Laplace": r"laplace approx",
    "infeasible region": r"infeasible region|crash region|failure region",
}
REGEX = {k: re.compile(v, re.I | re.S) for k, v in TERMS.items()}

BOTS = {"codecov-commenter", "codecov", "codecov-io", "facebook-github-bot", "github-actions", "dependabot", "meta-codesync", "pytorchbot", "facebook-github-tools"}

def texts(rec):
    """Yield (url, author, createdAt, where, text) for every text field (bot comments skipped)."""
    yield rec["url"], rec.get("author"), rec["createdAt"], "title", rec.get("title") or ""
    yield rec["url"], rec.get("author"), rec["createdAt"], "body", rec.get("body") or ""
    for c in rec.get("comments", []):
        if (c.get("author") or "") in BOTS or (c.get("author") or "").endswith("[bot]"):
            continue
        yield c["url"], c.get("author"), c["createdAt"], "comment", c.get("body") or ""
    for r in rec.get("reviews", []) or []:
        yield r["url"], r.get("author"), r["createdAt"], "review", r.get("body") or ""
        for c in r.get("comments", []):
            yield c["url"], c.get("author"), c["createdAt"], "review_comment", c.get("body") or ""

def snippet(text, m, w=110):
    s = max(0, m.start() - w); e = min(len(text), m.end() + w)
    return re.sub(r"\s+", " ", text[s:e]).replace("\t", " ")

def main():
    out = open("/tmp/research/botorch/hits.tsv", "w")
    out.write("term\ttype\tnumber\tstate\tmerged\ttitle\tfield\tauthor\tcreatedAt\turl\tsnippet\n")
    score = collections.defaultdict(lambda: collections.Counter())
    meta = {}
    for kind in ["issues", "prs", "discussions"]:
        for line in open(f"{RAW}/{kind}.jsonl"):
            rec = json.loads(line)
            key = (rec["type"], rec["number"])
            meta[key] = rec
            for url, author, created, where, text in texts(rec):
                for term, rx in REGEX.items():
                    m = rx.search(text)
                    if m:
                        score[key][term] += 1
                        out.write("\t".join([term, rec["type"], str(rec["number"]), rec.get("state") or "",
                                             str(rec.get("merged")), rec["title"].replace("\t", " "), where,
                                             author or "", created, url, snippet(text, m)]) + "\n")
    out.close()
    # per-record summary
    with open("/tmp/research/botorch/record_scores.tsv", "w") as f:
        f.write("type\tnumber\tstate\tmerged\tcreatedAt\tauthor\tn_terms\tterms\ttitle\turl\n")
        for key, cnt in sorted(score.items(), key=lambda kv: -len(kv[1])):
            rec = meta[key]
            f.write("\t".join([rec["type"], str(rec["number"]), rec.get("state") or "", str(rec.get("merged")),
                               rec["createdAt"][:10], rec.get("author") or "", str(len(cnt)),
                               ",".join(sorted(cnt)), rec["title"].replace("\t", " "), rec["url"]]) + "\n")
    tc = collections.Counter()
    for key, cnt in score.items():
        for t in cnt: tc[t] += 1
    for t, n in tc.most_common():
        print(f"{n:5d}  {t}")

main()
