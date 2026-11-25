# Edison result — task `fc3988c8-1676-4bd6-9321-d75b1062cd70`

Status: success

---

# Literature Review: Tokenizing, Chunking, Indexing, and Serving Regulatory/Policy Documents for LLM Workflows

## 1. PDF/HTML/DOCX → Structured Markdown Extraction Pipelines

The conversion of regulatory and policy documents (NSF PAPPG, NIH grants policy, DOE FOAs, FDA guidances, ISO/IEEE standards, building codes, legal statutes) from their native formats into structured, LLM-consumable representations is the foundational step in any compliance-oriented RAG pipeline. A comprehensive comparative study of ten PDF parsing tools across six document categories (including Law & Regulations) using the DocLayNet dataset found that **PyMuPDF and pypdfium2 generally outperformed other rule-based tools** for text extraction on digitally-born PDFs, achieving very high F1/precision/recall scores (≈0.98 for Law documents) with strong preservation of word order and layout (adhikari2410acomparativestudy pages 8-10, adhikari2410acomparativestudy pages 12-13, adhikari2410acomparativestudy pages 1-2). However, all parsers struggled with complex scientific and patent documents, where learning-based tools demonstrated superior performance (adhikari2410acomparativestudy pages 10-12).

**Docling** (IBM Research, MIT-licensed) has emerged as a leading open-source extraction toolkit. It uses specialized AI models — DocLayNet for layout analysis and TableFormer for table structure recognition — and implements a learned reading-order predictor that computes geometric features, builds a directed graph, and applies topological sort to produce human-like reading order (nawalny2025comparativeevaluationof pages 7-8, livathinos2025doclinganefficient pages 1-2). Docling's TableFormer achieves state-of-the-art performance on the TEDS metric across PubTabNet, FinTabNet, TableBank, and SynthTabNet benchmarks (nawalny2025comparativeevaluationof pages 7-8). The toolkit produces a unified DoclingDocument representation encoding text, headings, tables, images, code, formulas, lists, headers, and footers, with lossless JSON serialization and lossy exports to Markdown, HTML, and other formats (borskyUnknownyearimprovingtextand pages 21-26, livathinos2025doclinganefficient pages 2-3). Docling runs at approximately 1–1.3 pages/second on CPU and integrates with LangChain and LlamaIndex (livathinos2025doclinganefficient pages 1-2).

**Nougat** (Meta AI), a Visual Transformer model based on the Donut architecture with a Swin Transformer encoder, converts page images directly to markup without OCR. It excels on academic documents with mathematical expressions, "outperforming all rule-based parsers by a huge margin" on scientific content (blecher2023nougatneuraloptical pages 1-3, adhikari2410acomparativestudy pages 8-10). However, Nougat has notable weaknesses: tendency to collapse into repeating loops (observed in 1.5% of test pages), failure on non-Latin scripts, substantially slower throughput (~19.5s per batch on A10G vs. GROBID's 10.6 PDF/s), and occasional hallucinations when parsing documents (blecher2023nougatneuraloptical pages 8-10, adhikari2410acomparativestudy pages 13-15).

**Unstructured.io** uses a hybrid pipeline combining PDFMiner with layout detection (via detectron2) and OCR, producing structured components (titles, text, lists, tables, images, headers, footers) serializable to JSON/CSV/Markdown; tables are represented as HTML tags (borskyUnknownyearimprovingtextand pages 17-21). For table detection in the Law & Regulations category, learning-based detectors such as Table Transformer (TATR) substantially outperformed rule-based tools like Camelot, pdfplumber, and Tabula (adhikari2410acomparativestudy pages 12-13).

PDFs fundamentally store positioned graphical objects rather than semantic structure, so reading order, paragraph boundaries, table layouts, and other logical structure must be reconstructed — a challenge that remains the primary differentiator among tools (borskyUnknownyearimprovingtextand pages 13-17). Modern hybrid systems combining rule-based reliability with machine-learning structure recovery are recommended for regulatory documents (borskyUnknownyearimprovingtextand pages 13-17).

**Actionable rules for Theme 1:**
- Use Docling as the primary extraction tool for regulatory PDFs; it provides the best combination of structure preservation, table recognition, and section hierarchy recovery.
- Fall back to PyMuPDF for simple, digitally-born single-column documents where speed matters.
- Reserve Nougat for scientific appendices with heavy mathematical content.
- Always validate extraction quality on a sample of your specific corpus before committing to a tool.

---

## 2. Chunking Strategies

Chunking strategy is a critical yet often overlooked determinant of RAG quality. An empirical study comparing four chunking strategies on enterprise documents (including text-heavy manuals and table-heavy specifications) found that **structure-aware chunking yields the highest overall retrieval effectiveness**, particularly in top-K metrics, and incurs significantly lower computational costs than semantic or baseline strategies (taiwo2603evaluatingchunkingstrategies pages 1-3, taiwo2603evaluatingchunkingstrategies pages 9-11).

**Fixed-size chunking** (e.g., 512-character windows with 128-character overlap) is computationally efficient but "frequently creates breakpoints mid-sentence," causing fragmentation of essential contextual information and a "weakest link effect" that degrades downstream generation (taiwo2603evaluatingchunkingstrategies pages 1-3, lyu2025crudragacomprehensive pages 16-18). Larger fixed-size chunks tend to improve semantic-similarity metrics and preserve document structure but reduce precision for tasks requiring specific sub-paragraph extraction (lyu2025crudragacomprehensive pages 16-18).

**Recursive chunking** hierarchically splits text using progressively smaller delimiters to better preserve paragraphs and sections, offering a middle ground between fixed-size and structure-aware approaches but without explicit structural awareness (taiwo2603evaluatingchunkingstrategies pages 3-6).

**Semantic (breakpoint-based) chunking** uses embedding similarity to detect topic boundaries. While it can attain the highest ranking accuracy (MRR = 0.517 on full-text biomedical documents), it is "structurally blind, always retrieving from a single section" and performed worst on highly structured technical documents (mortezaagha2603graphawarelatechunking pages 1-3, taiwo2603evaluatingchunkingstrategies pages 6-9).

**Structure-aware chunking** follows document headings (H1/H2/H3) and section boundaries, achieving the highest MRR and top-ranked quality (NDCG@3, NDCG@5) while minimizing fragmentation, index size, and retrieval latency. For regulatory documents where explicit structure is meaningful, structure-aware chunking is the clear recommendation (taiwo2603evaluatingchunkingstrategies pages 6-9, conner2025structuringcontentfor pages 8-12).

### 2025–2026 Advances

**Late chunking** (Günther et al., 2024) first embeds all tokens of a long document through a long-context transformer, then applies chunking boundaries after the transformer and before pooling. This preserves cross-chunk contextual dependencies and yields contextually enriched chunk embeddings without additional training (merola2025reconstructingcontext pages 3-6, conti2025contextisgold pages 5-6). Empirical comparisons show late chunking is more computationally efficient than contextual retrieval while achieving comparable retrieval quality (merola2025reconstructingcontext pages 12-15).

**Contextual retrieval** (Anthropic, 2024) prepends LLM-generated context summaries to each chunk before embedding, preserving semantic coherence across chunk boundaries. This approach involves prompting an LLM per chunk to generate a brief summary situating it within the source document, combined with hybrid retrieval (dense + BM25 rank fusion) and reranking. It tends to preserve semantic coherence better but at significantly higher computational cost (~20GB VRAM for contextualization) (merola2025reconstructingcontext pages 6-9, merola2025reconstructingcontext pages 3-6, merola2025reconstructingcontext pages 1-3).

**ColBERT late interaction** stores token-level embeddings rather than pooled representations, enabling fine-grained token-wise matching between queries and document chunks. After specialized training (InSeNT), ColBERT with late chunking shows large nDCG gains on contextual retrieval tasks (conti2025contextisgold pages 3-5, conti2025contextisgold pages 5-6).

**Actionable rules for Theme 2:**
- For regulatory/policy documents with clear hierarchical structure, use structure-aware chunking anchored to section headings.
- Keep chunks self-contained: each chunk should include its section path (e.g., "Chapter II > Section A > §2.3") as a prefix.
- Target 500–1000 tokens per chunk with heading-based boundaries.
- Consider late chunking with long-context embedding models (e.g., ModernBERT) for improved contextual representation without the cost of LLM-based contextualization.

---

## 3. Token-Budgeting and Context-Window Engineering

The decision between long-context (LC) LLMs and retrieval-augmented generation (RAG) is now a nuanced, task-dependent choice rather than a binary one. A comprehensive study benchmarking RAG and LC across multiple datasets found that "when resourced sufficiently, LC consistently outperforms RAG in terms of average performance," but RAG's "significantly lower cost remains a distinct advantage" (li2024retrievalaugmentedgeneration pages 1-2). The Self-Route method, which routes queries between RAG and LC based on model self-reflection, achieved 65% cost reduction for Gemini-1.5-Pro and 39% for GPT-4O while maintaining comparable performance (li2024retrievalaugmentedgeneration pages 1-2).

The LaRA benchmark found that the optimal choice depends on "a complex interplay of factors, including the model's parameter size, long-text capabilities, context length, task type, and the characteristics of the retrieved chunks" (li2025larabenchmarkingretrievalaugmented pages 1-2). RAG tends to provide larger gains for weaker base models (up to 38% improvement on Mistral-Nemo-12B), while strong models (GPT-4o, Claude-3.5-sonnet) generally perform better with full long-context input (li2025larabenchmarkingretrievalaugmented pages 2-3). At very large context lengths (128k tokens), RAG can outperform LC by 3.68% (li2025larabenchmarkingretrievalaugmented pages 1-2).

For domain-specific regulatory documents, the NEPAQuAD study on Environmental Impact Statements found that "RAG powered models significantly outperform the long context models in answer accuracy regardless of the choice of the frontier LLM" (phan2024ragvs.long pages 1-2). Current LLMs "perform poorly in processing and understanding long, context-rich sequences," and RAG is recommended as an effective strategy for domain-specific QA (phan2024ragvs.long pages 5-7).

Increasing the number of retrieved passages follows an "inverted-U pattern" — initially improving performance but then declining due to hard negatives. With strong retrievers, the benefit peaks around 12,000 tokens of retrieved context; RAG consistently outperforms LC beyond 100K tokens with appropriate top-k settings (jin2410longcontextllmsmeet pages 3-4, xu2024chatqa2bridging pages 9-11).

**Actionable rules for Theme 3:**
- For a 200k–500k token policy corpus: use RAG as the primary strategy; the corpus exceeds even the largest context windows when multiple documents must be consulted.
- Reserve long-context ingestion for single-document deep reading tasks (e.g., analyzing a complete NSF PAPPG chapter).
- Implement a routing mechanism: if a query can be answered from a few retrieved chunks, use RAG; if it requires cross-section synthesis, escalate to long-context.
- Budget approximately 8,000–12,000 tokens of retrieved context per query for optimal accuracy/cost balance.

---

## 4. Citation and Traceability Mechanisms

Reliable citation is essential for compliance workflows where every claim must be traceable to a specific regulatory provision. Current approaches suffer from coarse citation granularity — citing only document IDs or URLs — which makes fine-grained verification difficult (huang2024learningfinegrainedgrounded pages 1-2).

The **FRONT framework** trains LLMs to produce fine-grained grounded citations by first selecting supporting quotes from retrieved sources (grounding), then conditioning generation on those quotes. Experiments on the ALCE benchmark demonstrated a 14.21% average improvement in citation quality over baselines (huang2024learningfinegrainedgrounded pages 1-2). The **PaperTrail** system implements claim–evidence provenance by decomposing and linking claims to supporting passages in source documents, though empirical findings show granular provenance increases cognitive load and reduces usability under time constraints (martinboyle2026papertrailaclaimevidence pages 2-3).

For span-level traceability, citation-grounded code comprehension work demonstrated that **mechanical citation verification** using `[file:start-end]` span references achieved 92% citation accuracy with zero hallucinations across 30 repositories. The approach combines hybrid retrieval (BM25 + dense embeddings), graph expansion for cross-document dependencies, and automated interval-arithmetic validation of cited spans (arafat2512citationgroundedcodecomprehension pages 2-2, arafat2512citationgroundedcodecomprehension pages 2-3). This `[source:start-end]` model directly applies to regulatory documents as `[PAPPG-Chapter-II:§2.3:p15-p16]`.

**Post-hoc verification pipelines** such as RARR retrieve evidence and revise outputs to align claims with sources, while SearChain interleaves retrieval with reasoning to produce retrieval-verified citations at each step. NLI-based verification adds an entailment layer to ensure cited evidence directly validates claims. Analysis shows that span-level Chain-of-Thought citation produced the best results for GPT-4 (pang2025largelanguagemodel pages 23-24).

**Actionable rules for Theme 4:**
- Embed structured frontmatter in each chunk: `{source: "NSF PAPPG 25-1", section: "Chapter II.E.3", page: 42, chunk_hash: "sha256:abc123"}`.
- Instruct the LLM to cite using section anchors (e.g., "per PAPPG §II.E.3, p.42").
- Implement post-generation NLI verification: decompose each claim and verify entailment against the cited chunk.
- Store content-addressable hashes for each chunk to detect corpus drift.

---

## 5. llms.txt and LLM-Friendly Documentation Conventions

The **llms.txt** specification (https://llmstxt.org) defines a Markdown file served at `/llms.txt` containing LLM-friendly documentation for a website. It provides a curated, machine-friendly table of contents with brief project descriptions and pointers to Markdown versions of key pages (e.g., `.html.md`) to simplify retrieval and context construction for AI agents (marro2025permissionmanifestsfor pages 3-5, marro2025permissionmanifestsfor pages 5-6). The specification is positioned as complementary to `robots.txt` but focused on accessibility and comprehension rather than access control (hurley2026cooperativecontentnegotiation pages 11-14).

Critically, llms.txt **lacks any mechanism for expressing or enforcing behavioral constraints**, limiting its ability to convey allowed interaction patterns or serve as an enforcement tool for regulatory content (marro2025permissionmanifestsfor pages 3-5, marro2025permissionmanifestsfor pages 5-6). It also provides only site-level documentation rather than per-page structured content delivery (hurley2026cooperativecontentnegotiation pages 11-14).

**Adoption** has been primarily among technology companies (Anthropic, Vercel, Cloudflare, Stripe, Supabase) for code documentation. The **ReadMe.LLM** framework extends the concept, demonstrating that LLM-oriented documentation can achieve up to 100% success on code generation tasks where human-oriented documentation fails.

**Extending to regulatory corpora** requires several additions not present in the current specification: (1) versioning metadata (e.g., "PAPPG 25-1, effective January 2025"), (2) hierarchical section identifiers with stable anchors, (3) effective dates and supersession information, (4) cross-reference resolution between documents, and (5) provision-level granularity rather than page-level pointers.

**Actionable rules for Theme 5:**
- Create a `policy-llms.txt` manifest for your corpus listing each document with version, effective date, and section inventory.
- Convert each policy document to structured Markdown with YAML frontmatter containing metadata.
- Maintain version-controlled Markdown alongside the original PDFs in a git repository.

---

## 6. Context7, Code-Doc Tokenizers/MCP Servers, and Generalizability

**Context7** (https://context7.com) and similar tools (DeepWiki, GitMCP, Cursor docs) are designed to index code documentation and serve it to LLMs via the **Model Context Protocol (MCP)**. MCP is a standardized open protocol introduced by Anthropic that defines a unified, bi-directional communication protocol between AI models and external tools or resources (venkiteela2025thenewinteroperability pages 2-5, singh2025asurveyof pages 3-5). MCP exposes three interaction surfaces: **tools** (invocable functions), **resources** (structured files, datasets, API entities), and **prompts** (reusable reasoning templates), all described via structured manifests with dynamic schema negotiation (venkiteela2025thenewinteroperability pages 2-5).

For serving documentation, MCP treats documents as addressable Resources accompanied by metadata, discovered via `resource.list` and retrieved via `resource.get` through a JSON-RPC API. MCP supports streaming responses, notifications, and batched requests for large documents (krishnan2504advancingmultiagentsystems pages 16-19). Context is treated as a first-class, persistent asset bound to a ContextID, with governance directives and provenance traveling with the context (venkiteela2025thenewinteroperability pages 6-9).

**Why code-doc approaches don't directly generalize to regulatory PDFs:**
1. Code documentation is natively structured (API signatures, function docstrings, class hierarchies) while regulatory documents require complex extraction from PDF/DOCX.
2. Code docs are version-controlled in git; regulatory documents arrive as opaque PDFs with no machine-readable structure.
3. Code-doc indexers assume clean Markdown or HTML input; policy documents require the extraction pipeline described in Theme 1.
4. Regulatory documents have cross-reference networks (e.g., "See 2 CFR Part 200") that require resolution — a feature absent from code-doc tools.

**What would need to change:** A regulatory MCP server would need to integrate document extraction (Docling), structure-aware chunking, cross-reference resolution, version tracking, and provision-level addressing — essentially building the full pipeline described in this review as an MCP-compatible backend.

---

## 7. Empirical Evaluations of LLM Compliance/Review

The most rigorous empirical evaluation of AI legal research tools to date found that **RAG-based proprietary systems still hallucinate at alarming rates**: Lexis+ AI hallucinated in approximately 17% of queries, Westlaw AI-Assisted Research in approximately 33%, and Ask Practical Law AI showed only 19% accuracy. While these rates represent improvement over general-purpose chatbots like GPT-4, they demonstrate that "the providers' claims [of hallucination-free output] are overstated" (magesh2025hallucination‐free?assessingthe pages 9-10, magesh2025hallucination‐free?assessingthe pages 1-2). Broader evaluations found hallucination rates of 69% for ChatGPT-3.5 and 88% for Llama 2 on specific legal queries without RAG augmentation (munir2025evaluatingaiin pages 2-4).

**LegalBench** is a collaboratively built benchmark containing 162 tasks covering six types of legal reasoning: issue-spotting, rule-recall, rule-application, rule-conclusion, interpretation, and rhetorical-understanding. It was built through an interdisciplinary process with legal professionals and evaluates models via few-shot prompting. The benchmark evaluated 20 LLMs including GPT-3.5, GPT-4, Claude-1, and 17 open-source models (guha2023legalbenchacollaboratively pages 5-7, guha2023legalbenchacollaboratively pages 12-13). **LawBench** extends this to Chinese legal reasoning with 20 tasks organized into three cognitive levels (memorization, comprehension, application) evaluating 21 LLMs (fei2024lawbenchbenchmarkinglegal pages 3-5). **HSE-Bench** focuses on Health, Safety, and Environment compliance with 1,000+ manually curated questions from regulations, court cases, safety exams, and fieldwork videos, finding that current LLMs rely on semantic matching rather than principled legal reasoning. **AIReg-Bench** benchmarks LLM compliance assessment against AI regulations.

Additional relevant benchmarks include **RAFT** (Real-world Annotated Few-shot Tasks), **FinanceBench** for financial document QA, **ContractNLI** for contract natural language inference, and long-document subsets of **MTEB** for retrieval evaluation. The **RAGBench** framework provides 100k examples across five industry domains with the TRACe evaluation framework for explainable RAG assessment (guha2023legalbenchacollaboratively pages 5-7).

**Actionable rules for Theme 7:**
- Expect 15–30% hallucination rates even with well-implemented RAG on regulatory content; always require human verification for compliance-critical outputs.
- Use LegalBench-style task decomposition to evaluate your pipeline: test issue-spotting, rule-recall, and rule-application separately.
- Implement automated NLI-based fact-checking as a post-generation verification layer.

---

## 8. Recommended Pipeline for a Private Lab Repository (200k–500k Tokens)

For a laboratory corpus comprising NSF/DOE/NIH policy documents, grant-writing guidance, and workbook chapters, the following pipeline is recommended based on the evidence reviewed:

### Extraction
**Primary tool: Docling** — provides the best combination of structure preservation (DocLayNet layout analysis), table recognition (TableFormer), reading-order prediction, and section hierarchy recovery. Runs on commodity CPU hardware at ~1–1.3 pages/second, produces structured Markdown and JSON with bounding boxes and provenance metadata (nawalny2025comparativeevaluationof pages 7-8, livathinos2025doclinganefficient pages 1-2, livathinos2025doclinganefficient pages 2-3). For any scientific appendices with heavy mathematical notation, supplement with Nougat (blecher2023nougatneuraloptical pages 1-3).

### Chunking Strategy
**Structure-aware chunking** anchored to document section headings (Chapter/Section/Subsection). Target 500–1000 tokens per chunk. Each chunk should carry its full section path as a prefix (e.g., "NSF PAPPG 25-1 > Chapter II > Section E > §3: Budget Preparation") (taiwo2603evaluatingchunkingstrategies pages 1-3, taiwo2603evaluatingchunkingstrategies pages 6-9). Implement Docling's built-in chunker class hierarchy for seamless integration.

### Frontmatter Schema
Each chunk should include YAML frontmatter:
```yaml
source: "NSF PAPPG 25-1"
version: "January 2025"  
section: "Chapter II.E.3"
title: "Budget Preparation Instructions"
page_range: [42, 44]
chunk_hash: "sha256:abc123def456"
effective_date: "2025-01-13"
```

### Retrieval Setup
**Hybrid BM25 + dense retrieval** with a reranker. Use BM25 for exact regulatory terminology matching (e.g., "2 CFR §200.474") combined with dense embeddings (e.g., BGE-M3 or text-embedding-3-large) for semantic search. Apply 4:1 dense-to-sparse weighting in rank fusion (merola2025reconstructingcontext pages 3-6). Add a cross-encoder reranker (e.g., Jina Reranker V2 or a fine-tuned model) to reorder top-k candidates (merola2025reconstructingcontext pages 6-9). Consider ColBERT late interaction for token-level matching precision on regulatory provisions (conti2025contextisgold pages 5-6).

### Serving Layer
**Git-checked structured Markdown** as the source of truth, with an MCP server for programmatic access. Store extracted Markdown files alongside original PDFs in a version-controlled repository. Implement an MCP server exposing documents as Resources with section-level addressing, version metadata, and cross-reference resolution (krishnan2504advancingmultiagentsystems pages 16-19). For interactive use, deploy a RAG endpoint (e.g., via LlamaIndex or LangChain) with the hybrid retrieval backend.

### Context-Window Strategy
Use RAG as the primary approach for multi-document queries. For single-document deep analysis (e.g., "summarize all budget requirements in PAPPG Chapter II"), consider long-context ingestion with Claude or Gemini. Implement query routing: if retrieved chunks score high confidence (>0.85 similarity), use RAG; otherwise escalate to long-context (li2024retrievalaugmentedgeneration pages 1-2, phan2024ragvs.long pages 1-2).

### Citation Protocol
Instruct the LLM to cite exact provisions using the format `[Source §Section, p.Page]`. Implement post-generation mechanical verification: decompose each generated claim, match it against cited chunks via NLI, and flag unsupported claims for human review (arafat2512citationgroundedcodecomprehension pages 2-2, pang2025largelanguagemodel pages 23-24).

### Evaluation Rubric
1. **Retrieval quality**: NDCG@5, MRR, Recall@10 on a manually curated test set of 50–100 question-answer pairs drawn from your policy corpus.
2. **Citation accuracy**: Percentage of generated citations that correctly identify the source section and are entailed by the cited text.
3. **Hallucination rate**: Percentage of generated claims not supported by any retrieved chunk (target <5% with human verification).
4. **Completeness**: Percentage of relevant provisions surfaced when querying about a specific compliance topic.
5. **Latency**: End-to-end response time (target <5 seconds for RAG queries).

This pipeline balances extraction fidelity, retrieval precision, citation traceability, and practical deployability for a moderate-sized regulatory corpus, while incorporating the latest advances in structure-aware chunking, late interaction retrieval, and mechanical citation verification.
