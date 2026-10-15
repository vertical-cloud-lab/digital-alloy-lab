# Retrieval evaluation set

Hand-labelled `query → expected_snippet_id` pairs used by
[`../scripts/run_eval.py`](../scripts/run_eval.py) to measure the
retriever defined in [`../scripts/retrieve.py`](../scripts/retrieve.py).

Implements items 1-2 of the §8 *Evaluation Rubric* in
[`../../edison-trajectories/llm-doc-tokenization/result.md`](../../edison-trajectories/llm-doc-tokenization/result.md):

> 1. Retrieval quality: NDCG@5, MRR, Recall@10 on a manually curated test
>    set of 50–100 question-answer pairs drawn from your policy corpus.
> 2. Citation accuracy: percentage of generated citations that correctly
>    identify the source section and are entailed by the cited text.

## Files

* `eval_set.jsonl` — one JSON object per line, schema documented in the
  file header. v1 has 15 items; the §8 target is 50-100.

## Run

```bash
python nsf-resources-text/scripts/run_eval.py            # human output
python nsf-resources-text/scripts/run_eval.py --verbose  # per-item ranks
python nsf-resources-text/scripts/run_eval.py --json     # machine-readable
```

## Current baseline (BM25 only)

| metric | value |
| --- | ---: |
| Recall@5 | 0.867 (13/15) |
| MRR | 0.733 |
| Hit@1 | 0.600 |

The 2 misses are both lexical-mismatch paraphrases ("Should I number
the pages of my proposal sections myself?" → expected
`pappg-24-1#II.C.1` *Proposal Pagination Instructions*; "What happens
to a proposal that does not comply..." → expected `pappg-24-1#IV.B`
*Proposal Not Accepted or Returned Without Review*). Both are expected
to be fixed by the dense reranker on the upgrade path documented in
[`../snippets/README.md`](../snippets/README.md#upgrade-path).

## Adding new items

1. Pick a real compliance question a PI might ask.
2. Run `retrieve.py` to find the canonical snippet — verify it actually
   contains the answer, not just the keywords.
3. If multiple snippets are equally valid, list the secondaries under
   `also_acceptable`.
4. Tag with a short topic label so per-tag recall remains diagnostic.
5. Re-run `run_eval.py` and check that aggregate metrics didn't
   regress. Commit the updated baseline numbers in the README at the
   same time as the new items.

Do not fix labels by reading the retriever's top hit and copying its
id — that defeats the purpose of the evaluation.
