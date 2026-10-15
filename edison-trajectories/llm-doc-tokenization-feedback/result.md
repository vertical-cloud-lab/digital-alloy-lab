# Edison result — task `660a4e59-342b-49d0-95bf-4d61e2b2a3b2`

Status: success

---

The Context7-style tokenization of your regulatory corpus is a thoughtful, structured improvement over raw Markdown dumps. However, it still carries over the fundamental mismatch of treating heterogeneous, unstructured text documents as though they were a single, coherent rulebook. While the PAPPG (which has a strict outline grammar) parses reasonably well, the remainder of your corpus is functionally unbroken, causing downstream fragility in citation and retrieval.

Here is a focused critique organized under your requested headings.

### 1. Snippet granularity & chunking

Your decision to chunk on the PAPPG grammar (`A. -> 1. -> a.`) is correct for that specific document. Regulatory texts operate at the clause or sub-section level. However, the actual implementation of your tokenization script falls apart on the non-PAPPG documents.

*   **The chunking isn't actually happening for most docs.** A quick analysis of `03-corpus-summary.json` reveals that **31 out of 38 documents contain exactly 1 snippet**, meaning the entire chapter was ingested as a single ~800-token blob. You haven't tokenized the GWSW chapters; you've just wrapped them in a JSON dictionary.
*   **Arbitrary token boundaries break rules.** For sections that exceed 1,200 tokens (e.g., the Federal Register notice), `split_long()` breaks chunks on paragraph and sentence boundaries. This produces multi-part ids (e.g., `~p1`, `~p2`). A rule spanning that artificial split is orphaned from its context, and an LLM fetching `~p2` might miss the conditional qualifier ("If the proposal exceeds 15 pages...") stranded in `~p1`.
*   **Next step:** Move to **propositional chunking** (Chen et al. 2024) or sub-clause chunking for regulatory documents. A single ~300-token paragraph can contain five distinct rules (e.g., font size, margins, pagination, line spacing). The atomic unit should be the *rule* or *guideline*, not the paragraph. 

### 2. Schema completeness

The `01-snippet-schema.md` schema is missing several critical fields required to sustain an autonomous "mock review" workflow.

*   **`effective_date` / `version`:** Regulatory corpora are living documents. Without pinning the effective date (e.g., "May 20, 2024"), you cannot govern whether a rule applies to a specific proposal draft or whether a later supplement supersedes it.
*   **`applies_to_condition`:** Many PAPPG rules are strictly scoped (e.g., "If the proposal includes postdocs...", "For GOALI proposals..."). The current schema treats all snippets as universally applicable.
*   **`cross_references`:** As you noted, "see Chapter IV.B" is currently dead text. The schema needs an `xrefs: [string]` array that resolves string references to structural `id`s (e.g., `["pappg-24-1#IV.B"]`) so the serving layer or the LLM can traverse the dependency graph.
*   **Deontic structure:** To reliably evaluate compliance, you need a schema that isolates the rule's anatomy. Minimally: `actor` (Proposer/PI/NSF), `modality` (must/may), `object` (Data Management Plan), and `penalty` (Returned Without Review). 

*(Note: There is a severe reporting error in your documentation. `01-snippet-schema.md` claims there are 498 required, 87 prohibited, 142 recommended, 181 permitted, and 297 informational snippets — a sum of 1,205. But `03-corpus-summary.json` correctly shows a total of 619. You have multiple builds or stale documentation crossing wires.)*

### 3. Requirement-strength labels

Your regex-based strength labeller is brittle, naive, and heavily skewed by the lack of granular chunking. 

*   **Scope bleed.** Because 80% of your documents are chunked as single blobs, your script applies one label to the entire document. If an 800-token informational chapter contains the word "must" a single time, the *entire document* is incorrectly tagged as `required`. 
*   **Layout pollution.** The first snippet of your Federal Register sample is tagged `permitted` simply because the extraction boilerplate contains the phrase *"may appear out of order"*.
*   **Adversarial grammar.** As you identified, the regex fails on negation ("not required to"), scope-limited modals ("may include... but if it does, it must"), and quoted text.
*   **Taxonomy:** You should absolutely adopt a formalized taxonomy. **RFC 2119** (MUST, MUST NOT, SHOULD, SHOULD NOT, MAY) is the gold standard for technical compliance and maps cleanly to LLM understanding. Drop "prohibited/required/permitted" and map strictly to the RFC 2119 keywords, using dependency parsing (not regex) to attach the modal to the correct subject.

### 4. Serving model

The current flat-file surface (`snippets.jsonl` + shards) is not sufficient for a scalable retrieval system, and pre-loading 200k tokens into a massive-context model is slow, expensive, and prone to "lost in the middle" attention degradation, especially for regulatory checklists where every detail matters.

*   **Do not rely on a pure long-context strategy.** A mock reviewer needs surgical precision.
*   **Build an MCP (Model Context Protocol) Server:** Yes, stand up a lightweight MCP server. Expose tools like `get_rule(id)`, `search_rules(query, scope)`, and `resolve_xref(id)`. This forces the LLM to explicitly query for compliance checks (e.g., "What are the page limits for a Project Description?") rather than hallucinating over a 200k-token slurry.
*   **Hybrid Retrieval:** For the MCP search endpoint, use hybrid BM25 + dense embeddings. BM25 is critical here because regulatory texts rely on exact keyword matches (e.g., "SciENcv", "GOALI"), which dense embeddings sometimes smooth over.

### 5. Evaluation

You need a benchmark specifically tailored to NSF proposal compliance. Building an evaluation harness against a regulatory corpus requires testing *precision of retrieval* and *accuracy of application*.

**Concrete Eval Items (Label format: `Input` -> `Expected Citation` / `Expected Verdict`)**

1.  **Input:** "My Project Summary is exactly 1.5 pages long and includes Overview, Intellectual Merit, and Broader Impacts sections."
    *   **Expected Citation:** `pappg-24-1#II.D.2.b`
    *   **Expected Verdict:** Non-compliant (exceeds 1-page limit).
2.  **Input:** "The budget justification spans 4 pages and details all senior personnel travel."
    *   **Expected Citation:** `pappg-24-1#II.D.2.f` (or relevant budget sub-section)
    *   **Expected Verdict:** Compliant (under 5-page limit).
3.  **Input:** "We have included a 3-page mentoring plan for our undergraduate researchers."
    *   **Expected Citation:** `pappg-24-1#II.D.2.i.i`
    *   **Expected Verdict:** Non-compliant (Mentoring plans are for postdocs/grad students, and the limit is 1 page).
4.  **Input:** "The Facilities, Equipment, and Other Resources section includes a table showing the exact dollar value of the university's NMR spectrometer."
    *   **Expected Citation:** `pappg-24-1#II.D.2.g`
    *   **Expected Verdict:** Non-compliant (No quantifiable financial info permitted).
5.  **Input:** "I am submitting a proposal to the NSF, but I am formatting my references with extensive annotations evaluating each paper's methodology."
    *   **Expected Citation:** `pappg-24-1#II.D.2.e`
    *   **Expected Verdict:** Non-compliant (References must not include annotations).

### 6. What I'd change tomorrow (Highest ROI)

1.  **Fix the chunking for non-PAPPG documents.** The fact that 31 out of 38 documents are treated as single 800+ token snippets is breaking your requirement-strength labelling and diluting the utility of the Context7 format. Implement proper markdown heading chunking (ensure `parse_markdown_headings` is actually breaking the GWSW documents correctly, which it currently is not).
2.  **Strip the regex labeller; use an LLM for extraction.** Regex cannot parse deontic logic. Run a cheap, fast LLM (e.g., gpt-4o-mini or Claude 3.5 Haiku) over the snippets during the build process to extract the RFC 2119 requirement, the actor, the condition, and the cross-references. Bake *that* JSON into your snippet schema.
3.  **Implement an MCP server with hybrid search.** Stop passing 85k–200k tokens in the prompt. Build a simple Python MCP server that exposes the snippets via BM25 + embeddings, forcing the mock-reviewer LLM to look up specific compliance rules as it audits the document.

### Final Verdict

You are absolutely correct that treating this like a legal informatics problem is the right mental model. The NSF PAPPG *is* a legal rulebook. You don't necessarily need to adopt heavy enterprise standards like Akoma Ntoso or LegalRuleML, but you *must* adopt their underlying philosophy: rules must be atomic, conditional, and graph-linked. Your current script is halfway between a naive markdown dump and a true regulatory database. Push it the rest of the way.

***

### Discretionary Analytical Decisions
*   Chose to evaluate the discrepancy in metadata (schema documentation vs summary JSON) to verify whether the pipeline was outputting stale or conflicting data, determining that the schema documentation was out of date.
*   Chose to manually review the parsed Federal Register excerpt, identifying that the first chunk's strength was polluted by layout extraction boilerplate, highlighting a failure in the document parser pipeline.
*   Selected RFC 2119 as the recommended standard taxonomy over ISO/IEC Directives, as RFC 2119 is computationally deterministic, natively understood by LLMs, and maps cleanly to the binary nature of grant compliance.
*   Elected to recommend an MCP server approach over long-context ingestion, prioritizing strict citation fidelity and reduced hallucination risk over the simplicity of single-prompt ingestion.
