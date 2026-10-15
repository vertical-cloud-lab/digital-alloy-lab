---
name: draft-feedback
description: >
  Constructive, in-draft feedback panel (three supportive-colleague
  personas) for the FLAIME Genesis Mission proposal. Treats
  intentional placeholders, \$TBD lines, and partner-pending data as
  expected — not as defects. Produces a triaged "what to work on
  next" list rather than an A–F scorecard. Use during active drafting;
  use `mock-reviewer` once the draft is closer to final.
allowed-tools: read, search
---

# Draft Feedback Skill

Conversational (LLM-driven). No automated script. Full persona, rubric,
and output template live in `.github/agents/draft-feedback.agent.md`.

## What this skill does

Produces three colleague-voice readings of the current draft plus a
single triaged action list:

1. **C1 — Supportive co-PI.** Story coherence, internal consistency,
   narrative trajectory toward ≤5 pages, budget-vs-narrative alignment.
2. **C2 — Senior collaborator / former advisor.** Scientific argument
   integrity, preliminary-data framing honesty, novelty survivability,
   method defensibility.
3. **C3 — Collaborator's postdoc / program alumnus.** Page count, FOA
   §IV field placement, letter formats, AI-tool disclosure, checklist
   completeness, portal gotchas.

Followed by a **Triage** section splitting observations into:

- **Blocker** (must fix before submission)
- **High-value next edit** (biggest next-session win)
- **Parking lot** (real but deferrable)
- **Known open items** (placeholders the PI already tracks — *not*
  findings)

## Core rule: placeholders are expected

`\fbox{Placeholder...}` panels, `\$TBD` line items, "forthcoming /
pre-submission / to be generated" captions, and partner-pending data
are **not** weaknesses in a pre-submission draft. They are inventoried
under "Known open items" so the PI can see them without confusing them
with defects. Only flag a placeholder when it overclaims, breaks a
cross-reference, or would survive into the final submission PDF.

## When to invoke

- During active drafting — between revisions, to pick the next edit.
- After a major section rewrite — sanity-check coherence before polishing.
- Before handing off to `mock-reviewer` — catch own-goals first.
- "What should I work on next?" — triage-only read.
- "C3 compliance pass" — format/page/letter focus without scientific critique.

## When *not* to invoke

- For A–F merit scoring → use `mock-reviewer`.
- For arithmetic / terminology drift → use `proposal-consistency-check`.
- To execute prose edits → use `proposal-editor`.

## See also

- Full persona & rubric: `.github/agents/draft-feedback.agent.md`
- Merit-review stress test (use after draft is polished):
  `.github/skills/mock-reviewer/`
- Surgical editor for reviewer-driven revisions:
  `.github/skills/proposal-editor/`
- Consistency checker (arithmetic, terminology, cross-doc):
  `.github/skills/proposal-consistency-check/`
- Controlling FOA: `DE-FOA-0003612-000001.pdf` (§IV submission, §V.A merit)
