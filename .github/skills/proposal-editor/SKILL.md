---
name: proposal-editor
description: >
  Surgical prose editor for the FLAIME Genesis Mission proposal LaTeX
  source. Applies revisions in response to reviewer comments, PI directives,
  or targeted editing requests while preserving page count, citations, and
  FOA compliance.
allowed-tools: read, search, edit, execute
---

# Proposal Editor Skill

Conversational (LLM-driven). No automated script. Full persona, conventions,
and workflow live in `.github/agents/proposal-editor.agent.md`.

## What this skill does

Takes one of:

- A **reviewer comment** (from the mock-reviewer skill or a real
  panelist/PO)
- A **PI directive** ("tighten X", "move Y", "replace Z with W")
- A **quoted reviewer/PI text block** to integrate

…and produces a surgical edit to
`genesis-mission-proposal/flaime-genesis-proposal.tex` that fully addresses
the request and nothing more.

## Guarantees

- Edits a single source file (no `-v2`, `-clean`, or alternates).
- Preserves canonical conventions: "We propose FLAIME..." framing, SDL
  Level 3/4, ternary=k=2, 15-element palette, TCAl10/AM~Module,
  \$750K = BYU~\$600K + partner subawards.
- Verifies cross-references, citations, and numerical consistency.
- Rebuilds the clean PDF and reports narrative page count.
- Does **not** commit — PI reviews the latexdiff PDF first.

## When to invoke

- Immediately after `mock-reviewer` returns a scorecard — feed the
  weaknesses in one at a time or in a batch.
- When the PI provides a specific rewrite instruction ("replace this
  sentence with: ...").
- When you notice during editing that a number, partner, or citation is
  inconsistent and want it propagated cleanly.
- Before submission, to apply a final pass of targeted fixes.

## Typical flow

1. `mock-reviewer` → scorecard with ranked weaknesses.
2. User: "apply R2's weakness #1 and R3's weakness #2."
3. `proposal-editor` → locates target passages, applies minimal edits,
   rebuilds clean PDF, reports narrative page count and any follow-ups.
4. User reviews latexdiff PDF → approves or requests further revision.
5. Commit only after explicit PI sign-off.

## See also

- Full workflow & conventions: `.github/agents/proposal-editor.agent.md`
- Upstream critic: `.github/skills/mock-reviewer/SKILL.md`
- Consistency checker (run before/after edits that touch numbers):
  `.github/skills/proposal-consistency-check/`
