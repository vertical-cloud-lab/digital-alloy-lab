#!/usr/bin/env python3
"""Run the retrieval evaluation set against `RetrievalIndex`.

Reports per-query rank, plus aggregate Recall@k and Mean Reciprocal Rank
(MRR). Per-tag breakdown helps spot which compliance topics retrieve
poorly so we know what to label next.

This implements items 1-2 of the §8 "Evaluation Rubric" from
`edison-trajectories/llm-doc-tokenization/result.md`:

  > 1. Retrieval quality: NDCG@5, MRR, Recall@10 on a manually curated
  >    test set of 50–100 question-answer pairs drawn from your policy
  >    corpus.
  > 2. Citation accuracy: ...

The v1 eval set is 15 hand-labelled items (`eval_set.jsonl`); the
target is 50-100. NDCG@5 is omitted from the v1 metrics because all of
our labels are binary (one canonical id per query) so NDCG and MRR
collapse to the same ordering signal.

Usage:

    python nsf-resources-text/scripts/run_eval.py
    python nsf-resources-text/scripts/run_eval.py --top-k 10 --verbose
    python nsf-resources-text/scripts/run_eval.py --json > metrics.json
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from retrieve import RetrievalIndex  # noqa: E402


REPO_CORPUS = HERE.parent  # nsf-resources-text/
EVAL_SET = REPO_CORPUS / "eval" / "eval_set.jsonl"
ADVERSARIAL_SET = REPO_CORPUS / "eval" / "adversarial.jsonl"


def load_eval_set(path: Path) -> list[dict]:
    out: list[dict] = []
    for raw in path.read_text("utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        out.append(json.loads(line))
    return out


def evaluate_adversarial(contextual: bool = False) -> dict:
    """Score the refusal / adversarial set.

    For each query the retriever's top-1 hit score is compared to the
    item's `max_score` threshold. A *pass* means the top score is below
    the threshold (i.e. the playbook's `INSUFFICIENT EVIDENCE` rule
    would fire and the mock reviewer would refuse) AND the top hit is
    not in any `must_not_top_id` set the item supplies.

    Inspired by the refusal/abstain track in
    https://github.com/amazon-science/RAGChecker and
    https://github.com/stanford-futuredata/ARES — full claim-level
    scoring needs an LLM in the loop; this is the pure-stdlib proxy.
    """
    if not ADVERSARIAL_SET.exists():
        return {"n": 0, "refusal_rate": 0.0, "per_item": []}
    items = load_eval_set(ADVERSARIAL_SET)
    idx = RetrievalIndex.load_default(contextual=contextual)
    per_item: list[dict] = []
    refused = 0
    by_tag_pass: dict[str, int] = defaultdict(int)
    by_tag_n: dict[str, int] = defaultdict(int)
    for item in items:
        hits = idx.search(item["query"], top_k=1)
        top_score = hits[0].score if hits else 0.0
        top_id = hits[0].snippet["id"] if hits else None
        max_score = item.get("max_score", 8.0)
        forbid = set(item.get("must_not_top_id", []))
        passed = top_score <= max_score and top_id not in forbid
        if passed:
            refused += 1
        tag = item.get("tag", "untagged")
        by_tag_n[tag] += 1
        if passed:
            by_tag_pass[tag] += 1
        per_item.append({
            "query": item["query"],
            "tag": tag,
            "top_id": top_id,
            "top_score": round(top_score, 2),
            "max_score": max_score,
            "passed": passed,
        })
    n = len(items)
    return {
        "n": n,
        "refusal_rate": refused / n if n else 0.0,
        "by_tag_refusal_rate": {
            t: by_tag_pass[t] / by_tag_n[t] for t in sorted(by_tag_n)
        },
        "per_item": per_item,
    }


def evaluate(top_k: int = 5, verbose: bool = False,
             contextual: bool = False, expand_parent: bool = False) -> dict:
    items = load_eval_set(EVAL_SET)
    idx = RetrievalIndex.load_default(contextual=contextual)
    per_item: list[dict] = []
    rr_total = 0.0
    hit_at_1 = 0
    hit_at_k = 0
    by_tag_hits: dict[str, int] = defaultdict(int)
    by_tag_n: dict[str, int] = defaultdict(int)
    for item in items:
        expected = {item["expected_id"], *item.get("also_acceptable", [])}
        hits = idx.search(item["query"], top_k=max(top_k, 10),
                          expand_parent=expand_parent)
        # When parent-child expansion fires, the merged hit's id is the
        # parent id (e.g. `pappg-24-1#II.D.2.b`). If the eval expects a
        # child id (e.g. `~p2`), accept the parent as a match because the
        # merged text contains the child's text verbatim.
        rank = None
        for h in hits:
            hid = h.snippet["id"]
            if hid in expected:
                rank = h.rank
                break
            if h.snippet.get("expanded_from_parent"):
                kids = set(h.snippet.get("merged_children") or [])
                if expected & kids:
                    rank = h.rank
                    break
        if rank == 1:
            hit_at_1 += 1
        if rank is not None and rank <= top_k:
            hit_at_k += 1
        rr = (1.0 / rank) if rank else 0.0
        rr_total += rr
        tag = item.get("tag", "untagged")
        by_tag_n[tag] += 1
        if rank is not None and rank <= top_k:
            by_tag_hits[tag] += 1
        per_item.append({
            "query": item["query"],
            "expected_id": item["expected_id"],
            "rank": rank,
            "reciprocal_rank": rr,
            "tag": tag,
            "top_hit": hits[0].snippet["id"] if hits else None,
        })
    n = len(items)
    metrics = {
        "n": n,
        "top_k": top_k,
        f"recall@{top_k}": hit_at_k / n if n else 0.0,
        "mrr": rr_total / n if n else 0.0,
        "hit_at_1_rate": hit_at_1 / n if n else 0.0,
        f"by_tag_recall@{top_k}": {
            t: by_tag_hits[t] / by_tag_n[t] for t in sorted(by_tag_n)
        },
    }
    if verbose:
        metrics["per_item"] = per_item
    return metrics


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--top-k", "-k", type=int, default=5)
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Include per-item ranks in output.")
    parser.add_argument("--contextual", action="store_true",
                        help="Use snippets.contextual.jsonl (Anthropic-style).")
    parser.add_argument("--expand-parent", action="store_true",
                        help="Merge child chunks into parent on retrieval.")
    parser.add_argument("--adversarial", action="store_true",
                        help="Also score the refusal/adversarial set.")
    parser.add_argument("--json", action="store_true",
                        help="Print machine-readable JSON.")
    args = parser.parse_args(argv)
    metrics = evaluate(top_k=args.top_k, verbose=args.verbose,
                       contextual=args.contextual, expand_parent=args.expand_parent)
    if args.adversarial:
        metrics["adversarial"] = evaluate_adversarial(contextual=args.contextual)
    if args.json:
        json.dump(metrics, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    print(f"Eval set: {metrics['n']} items, top_k={metrics['top_k']}")
    print(f"  Recall@{args.top_k}: {metrics[f'recall@{args.top_k}']:.3f}  "
          f"({int(round(metrics[f'recall@{args.top_k}'] * metrics['n']))}/{metrics['n']})")
    print(f"  MRR:         {metrics['mrr']:.3f}")
    print(f"  Hit@1 rate:  {metrics['hit_at_1_rate']:.3f}")
    print("  By tag:")
    for tag, recall in metrics[f"by_tag_recall@{args.top_k}"].items():
        print(f"    {tag:30s} {recall:.3f}")
    if args.verbose:
        print("\nPer-item:")
        for r in metrics["per_item"]:
            mark = "✓" if r["rank"] == 1 else ("○" if r["rank"] else "✗")
            rank_s = f"#{r['rank']}" if r["rank"] else "miss"
            print(f"  {mark} {rank_s:>5}  {r['query']}")
            if r["rank"] != 1:
                print(f"           expected={r['expected_id']!r}, top_hit={r['top_hit']!r}")
    if args.adversarial and "adversarial" in metrics:
        adv = metrics["adversarial"]
        print(f"\nAdversarial / refusal set: {adv['n']} items")
        print(f"  Refusal rate (top1 score <= max_score, top_id not forbidden): "
              f"{adv['refusal_rate']:.3f}")
        for tag, rate in adv.get("by_tag_refusal_rate", {}).items():
            print(f"    {tag:30s} {rate:.3f}")
        if args.verbose:
            for r in adv["per_item"]:
                mark = "✓" if r["passed"] else "✗"
                print(f"  {mark} score={r['top_score']:5.2f} <= {r['max_score']:5.2f}  "
                      f"{r['query']}")
                if not r["passed"]:
                    print(f"           top_id={r['top_id']!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
