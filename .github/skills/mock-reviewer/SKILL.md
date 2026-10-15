---
name: mock-reviewer
description: >
  Simulates a three-persona DOE merit review panel (materials academic,
  AI/ML methodologist, industry AM practitioner) and a separate DOE
  program-officer synthesis for the FLAIME Genesis Mission proposal.
  Scores against the five merit review criteria in FOA §V.A.
allowed-tools: read, search
---

# Mock Reviewer Skill

Conversational (LLM-driven). No automated script. Full persona, rubric, and
output template live in `.github/agents/mock-reviewer.agent.md`.

## What this skill does

Produces two separate artifacts from the proposal corpus:

1. **Three-reviewer panel scorecard** — materials academic (R1), AI/ML
   methodologist (R2), industry AM practitioner (R3) each grade A–F on the
   five FOA §V.A criteria with independent rationales. Reviewers are
   allowed (encouraged) to disagree.
2. **Program-officer synthesis** — integrates the panel, assesses
   award-readiness, cost realism, Phase I → Phase II setup, and FOA
   compliance posture. Program officer does not re-score.

## Merit review criteria (FOA §V.A, descending weight)

1. Scientific / Technical Merit
2. Technical Approach
3. Team
4. Commercialization / Tech Transfer
5. Budget / Resources justification

All scoring language is grounded in FOA §V.A verbatim phrasing where
possible ("novel, unique, innovative, or creative"; "reasonable and
realistic"; "qualifications, relevant experience, and time commitment").

## When to invoke

- Before a major revision — identify load-bearing weaknesses before you
  rewrite.
- Before submission — sanity check against FOA §V.A criteria and PO
  award-readiness.
- To stress-test a section — "score the Methods section" or "R3 only on
  the partner letters."
- To red-team a claim — "where would R2 push back on ≥3× AI acceleration?"
- To get a PO-only read — "PO view on staffing" or "PO view on Phase I →
  Phase II setup."

## See also

- Full persona & rubric: `.github/agents/mock-reviewer.agent.md`
- Controlling FOA: `DE-FOA-0003612-000001.pdf` (§V.A = merit criteria)
- FAQ v2 (4/10/26): `Genesis-Mission-RFA-FAQs-20260410-v2.pdf` (Phase I-only
  clarification for 3-B)
- Consistency check (arithmetic/terminology, run separately if desired):
  `.github/skills/proposal-consistency-check/`
