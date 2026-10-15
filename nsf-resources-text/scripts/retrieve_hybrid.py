#!/usr/bin/env python3
"""Hybrid retrieval over the NSF requirements snippet store.

Implements the §5.1 v2 recommendation from
`edison-trajectories/llm-doc-tokenization/result.md` and the Edison
LITERATURE_HIGH synthesis in
`edison-trajectories/eager-framework-eval/result-literature.md`:

    BM25 (sparse) + BGE-M3 (dense) → Reciprocal Rank Fusion → bge-reranker-v2-m3

Published gains on regulatory corpora (legal / financial / policy text):

    +0.07 Recall@10
    +0.08 MAP@10
    +30 to +45 % nDCG@10 from the reranker layer alone

References:

  * BGE-M3 (Chen et al., 2024):     https://arxiv.org/abs/2402.03216
  * bge-reranker-v2-m3:             https://huggingface.co/BAAI/bge-reranker-v2-m3
  * NV-Embed-v2 (alternative):      https://huggingface.co/nvidia/NV-Embed-v2
  * Reciprocal Rank Fusion:         https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
  * Anthropic Contextual Retrieval: https://www.anthropic.com/news/contextual-retrieval

Design notes:

  * BM25 lives in `retrieve.py` and remains the pure-stdlib fast path
    (used by CI, by the mock-reviewer playbook, and by anyone without a
    GPU). This script *imports* `RetrievalIndex` for the sparse half and
    layers the dense + reranker stages on top.
  * Heavy deps (`torch`, `sentence-transformers`, `FlagEmbedding`) are
    imported lazily and gated behind `--engine`. With `--engine bm25`
    (the default) this script behaves exactly like `retrieve.py`. With
    `--engine hybrid` it requires the v2 deps to be installed and the
    BGE-M3 model to be cached locally.
  * Dense embeddings are cached at `snippets/embeddings.bge-m3.npy` so
    we only pay the encode cost once. Cache invalidation: when the
    snippet store's `chunk_hash`es change, delete the .npy.

Install (for `--engine hybrid` or `--engine rerank`):

    pip install sentence-transformers FlagEmbedding torch

Usage:

    # Same as retrieve.py (default — pure stdlib BM25)
    python nsf-resources-text/scripts/retrieve_hybrid.py "query"

    # Hybrid (BM25 sparse + BGE-M3 dense via RRF)
    python nsf-resources-text/scripts/retrieve_hybrid.py --engine hybrid "query"

    # Hybrid + cross-encoder rerank with bge-reranker-v2-m3
    python nsf-resources-text/scripts/retrieve_hybrid.py --engine rerank "query"

    # Build / refresh the dense index ahead of time
    python nsf-resources-text/scripts/retrieve_hybrid.py --build-index
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from retrieve import Hit, RetrievalIndex, _format_hit  # noqa: E402

REPO = HERE.parents[1]
SNIPPETS_DIR = REPO / "snippets"
DENSE_CACHE = SNIPPETS_DIR / "embeddings.bge-m3.npy"
DENSE_IDS_CACHE = SNIPPETS_DIR / "embeddings.bge-m3.ids.json"

# Conservative defaults from the cited literature. RRF constant k=60 is
# the value Cormack & Clarke (SIGIR 2009) reported as robust across
# TREC tracks; bumping to 100 favours later-ranked items more, which
# helps when sparse and dense disagree often (regulatory text).
DEFAULT_DENSE_MODEL = "BAAI/bge-m3"
DEFAULT_RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"
RRF_K = 60


def _require_torch_stack(component: str) -> tuple:
    """Lazy-import the heavy ML stack with a clear error if missing."""
    try:
        import numpy as np  # noqa: F401
    except ImportError as exc:
        raise SystemExit(
            f"--engine {component} requires numpy. Install with:\n"
            "    pip install numpy"
        ) from exc
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
    except ImportError as exc:
        raise SystemExit(
            f"--engine {component} requires sentence-transformers.\n"
            "Install with:\n"
            "    pip install sentence-transformers FlagEmbedding torch"
        ) from exc
    cross = None
    if component == "rerank":
        try:
            from sentence_transformers import CrossEncoder  # type: ignore

            cross = CrossEncoder
        except ImportError as exc:
            raise SystemExit(
                "--engine rerank requires sentence_transformers.CrossEncoder."
            ) from exc
    import numpy as np  # re-import for the returned reference

    return np, SentenceTransformer, cross


@dataclass
class HybridConfig:
    dense_model: str = DEFAULT_DENSE_MODEL
    reranker_model: str = DEFAULT_RERANKER_MODEL
    rrf_k: int = RRF_K
    top_k_sparse: int = 50
    top_k_dense: int = 50
    top_k_rerank: int = 20


class HybridRetrievalIndex:
    """BM25 + dense (BGE-M3) + cross-encoder reranker.

    Wraps the stdlib `RetrievalIndex` for the sparse half. The dense
    encoder and the reranker are loaded lazily on first call so import
    of this module stays cheap.
    """

    def __init__(self, sparse: RetrievalIndex, config: HybridConfig | None = None):
        self.sparse = sparse
        self.config = config or HybridConfig()
        self._dense_emb = None  # np.ndarray, shape (N, d)
        self._dense_ids = None  # list[str] — snippet ids in the same order
        self._encoder = None
        self._reranker = None

    # ---- dense half ------------------------------------------------

    def _ensure_dense(self) -> None:
        if self._dense_emb is not None:
            return
        np, SentenceTransformer, _ = _require_torch_stack("hybrid")
        if DENSE_CACHE.exists() and DENSE_IDS_CACHE.exists():
            self._dense_emb = np.load(DENSE_CACHE)
            self._dense_ids = json.loads(DENSE_IDS_CACHE.read_text("utf-8"))
            if self._dense_emb.shape[0] != len(self._dense_ids):
                raise SystemExit(
                    f"Dense cache shape mismatch: {self._dense_emb.shape[0]} "
                    f"emb vs {len(self._dense_ids)} ids. Rebuild with --build-index."
                )
            return
        # First-time build.
        self._encoder = SentenceTransformer(self.config.dense_model)
        texts = []
        ids = []
        for s in self.sparse.snippets:
            # Prefer the Anthropic-style contextual text if the index was
            # built with `use_contextual=True`. Otherwise concatenate
            # breadcrumbs + text so the dense vector still sees the
            # section path.
            if self.sparse.use_contextual and s.get("text_contextualized"):
                texts.append(s["text_contextualized"])
            else:
                texts.append(
                    " ".join(s.get("section_breadcrumbs", []))
                    + "\n\n"
                    + s.get("text", "")
                )
            ids.append(s["id"])
        emb = self._encoder.encode(
            texts, batch_size=16, normalize_embeddings=True, show_progress_bar=True,
        )
        self._dense_emb = np.asarray(emb, dtype="float32")
        self._dense_ids = ids
        SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
        np.save(DENSE_CACHE, self._dense_emb)
        DENSE_IDS_CACHE.write_text(json.dumps(ids), encoding="utf-8")

    def _dense_search(self, query: str, top_k: int) -> list[tuple[str, float]]:
        self._ensure_dense()
        import numpy as np  # noqa: F401

        if self._encoder is None:
            from sentence_transformers import SentenceTransformer  # type: ignore

            self._encoder = SentenceTransformer(self.config.dense_model)
        q = self._encoder.encode(
            [query], normalize_embeddings=True, show_progress_bar=False,
        )[0]
        scores = self._dense_emb @ q  # cosine because both are L2-normalized
        order = scores.argsort()[::-1][:top_k]
        return [(self._dense_ids[i], float(scores[i])) for i in order]

    # ---- reranker --------------------------------------------------

    def _rerank(self, query: str, candidates: list[str]) -> list[tuple[str, float]]:
        _, _, CrossEncoder = _require_torch_stack("rerank")
        if self._reranker is None:
            self._reranker = CrossEncoder(self.config.reranker_model)
        id_to_idx = {s["id"]: i for i, s in enumerate(self.sparse.snippets)}
        pairs = []
        for cid in candidates:
            i = id_to_idx.get(cid)
            if i is None:
                continue
            pairs.append([query, self.sparse.snippets[i].get("text", "")])
        scores = self._reranker.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda kv: -float(kv[1]))
        return [(cid, float(sc)) for cid, sc in ranked]

    # ---- public ----------------------------------------------------

    def search(self, query: str, top_k: int = 5, engine: str = "hybrid",
               doc_id: str | None = None, strength: str | None = None,
               expand_parent: bool = False) -> list[Hit]:
        if engine == "bm25":
            return self.sparse.search(query, top_k=top_k, doc_id=doc_id,
                                      strength=strength, expand_parent=expand_parent)
        # Sparse half (over-fetch for fusion)
        sparse_hits = self.sparse.search(
            query, top_k=self.config.top_k_sparse,
            doc_id=doc_id, strength=strength, expand_parent=False,
        )
        sparse_ranking = [(h.snippet["id"], h.score) for h in sparse_hits]
        # Dense half
        dense_ranking = self._dense_search(query, self.config.top_k_dense)
        # RRF fusion: 1 / (k + rank). See Cormack & Clarke 2009.
        fused: dict[str, float] = {}
        for rank, (cid, _) in enumerate(sparse_ranking, 1):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (self.config.rrf_k + rank)
        for rank, (cid, _) in enumerate(dense_ranking, 1):
            fused[cid] = fused.get(cid, 0.0) + 1.0 / (self.config.rrf_k + rank)
        ranked = sorted(fused.items(), key=lambda kv: -kv[1])
        candidate_ids = [cid for cid, _ in ranked[: self.config.top_k_rerank]]
        if engine == "rerank":
            reranked = self._rerank(query, candidate_ids)
            final = reranked[:top_k]
        else:
            final = [(cid, fused[cid]) for cid in candidate_ids[:top_k]]
        id_to_idx = {s["id"]: i for i, s in enumerate(self.sparse.snippets)}
        hits: list[Hit] = []
        for rank, (cid, score) in enumerate(final, 1):
            i = id_to_idx.get(cid)
            if i is None:
                continue
            hits.append(Hit(score=score, rank=rank, snippet=self.sparse.snippets[i]))
        return hits


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("query", nargs="*", help="Free-text query.")
    parser.add_argument("--engine", choices=["bm25", "hybrid", "rerank"],
                        default="bm25",
                        help="Retrieval engine. Default 'bm25' is pure stdlib; "
                             "'hybrid' adds BGE-M3 dense via RRF; "
                             "'rerank' additionally cross-encodes with bge-reranker-v2-m3.")
    parser.add_argument("--top-k", "-k", type=int, default=5)
    parser.add_argument("--doc")
    parser.add_argument("--strength", choices=[
        "prohibited", "required", "recommended", "permitted", "informational"])
    parser.add_argument("--contextual", action="store_true",
                        help="Index snippets.contextual.jsonl (Anthropic-style).")
    parser.add_argument("--expand-parent", action="store_true",
                        help="Merge child chunks into parent on retrieval (bm25 only).")
    parser.add_argument("--show-text", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--build-index", action="store_true",
                        help="Encode and cache the dense BGE-M3 embeddings, then exit.")
    args = parser.parse_args(argv)

    sparse = RetrievalIndex.load_default(contextual=args.contextual)
    hybrid = HybridRetrievalIndex(sparse)

    if args.build_index:
        hybrid._ensure_dense()
        print(f"Dense index built: {hybrid._dense_emb.shape} -> {DENSE_CACHE}")
        return 0

    if not args.query:
        parser.error("query is required unless --build-index is set")
    query = " ".join(args.query)
    hits = hybrid.search(query, top_k=args.top_k, engine=args.engine,
                         doc_id=args.doc, strength=args.strength,
                         expand_parent=args.expand_parent)
    if args.json:
        json.dump(
            [{"rank": h.rank, "score": h.score, "snippet": h.snippet} for h in hits],
            sys.stdout, indent=2,
        )
        sys.stdout.write("\n")
        return 0
    if not hits:
        print(f"No hits for: {query!r} (engine={args.engine})")
        return 1
    print(f"Query: {query!r}    engine={args.engine}    "
          f"({len(hits)} hit{'s' if len(hits) != 1 else ''})")
    for h in hits:
        print(_format_hit(h, show_text=args.show_text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
