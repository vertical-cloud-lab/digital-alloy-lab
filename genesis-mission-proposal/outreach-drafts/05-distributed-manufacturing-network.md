# Distributed Manufacturing Network — Multi-Site Validation Outreach

## Purpose

This is the **mass-outreach instrument** for the distributed manufacturing
network referenced at `flaime-genesis-proposal.tex:686-700`:

> "...[TBD_N_UNIV] universities, [TBD_N_LAB] national laboratories, and
> [TBD_N_COMPANY] companies have written letters of collaboration expressing
> intent to print with one or more of the 3–6 validated compositions..."

Target pool: the Top-75 worldwide metal-AM contacts list compiled in PR #57
(`edison-trajectories/metal-am-contacts-worldwide.md`). Each signed letter
populates one tally in the `[TBD_N_*]` counters in the narrative.

## Why this matters

The numerator in the narrative — "X universities, Y labs, Z companies" — is a
direct signal of industry validation and distributed-manufacturing adoption
pathway. The larger the signed set, the stronger the commercialization
narrative for merit review Criterion 5 (market relevance / adoption path).

## Master email template (copy-paste for each Top-75 contact)

Personalize only the greeting, the inserted technology (LPBF / DED / Binder
Jet), and the closing signature block. **Do not modify the 2-sentence letter
body** — FOA p.65 mandates the exact format.

```
Subject: FLAIME (DE-FOA-0003612) — 2-sentence Letter of Collaboration for
         multi-site Al-alloy validation printing

Dear [Name],

Sterling Baird at BYU. We're submitting FLAIME (Fast Learning AI for
Mineral Efficiency) to the DOE Genesis Mission program (DE-FOA-0003612,
Topic 3-B). FLAIME will discover and qualify new aluminum alloys with
reduced critical-mineral content (Mn, Cr, Zr, Co), validate them through
an AI-autonomous closed-loop pipeline at BYU, and scale the top 3–6
compositions to gas-atomized powder for external validation printing.

We'd like to include your facility in our distributed manufacturing
validation network. The ask is a single signed 2-sentence letter on your
institutional letterhead — FOA p.65 mandates this exact format (any
deviation and the letter is rejected). There is no financial commitment
and no effort reporting; the intent is simply to print one or more of
our validated compositions and return representative samples with build
metadata if/when FLAIME is funded.

Pre-filled letter (please adjust only the bracketed technology and
signature block):

    [Institutional Letterhead]
    [Date]

    To Whom It May Concern:

    If the application entitled, "FLAIME: Fast Learning AI for Mineral
    Efficiency," is selected for funding under DE-FOA-0003612, it is my
    intent to collaborate in this research by printing specimens from
    one or more of the 3–6 validated FLAIME aluminum-alloy compositions
    (scaled to gas-atomized powder at varying particle-size
    distributions) on our [LPBF / powder-DED / binder-jet] system (<insert brand / model type>) and
    returning at least one representative sample with
    associated build metadata (scan/process parameters, build log, and
    any post-processing parameters applied). Thank you for the
    opportunity to participate.

    Sincerely,
    [Name, Title]
    [Organization]
    [Address]
    [Email] | [Phone]

Deadline for signed PDF: [DEADLINE — ≥3 biz days before FOA submission].
If that's impossible on your side, even a same-day email confirmation of
intent is useful — we can collect the signed PDF in the follow-up window.

Happy to answer any questions. Thanks for considering.

Sterling

Sterling G. Baird, Ph.D.
Assistant Professor, Mechanical Engineering
Brigham Young University
sterling_baird@byu.edu
```

## Execution guidance

1. **Batch-send from PR #57 Top-75 list.** Use the LinkedIn cross-reference
   prioritization to warm-intro where possible; send cold to the rest.
2. **Fill per-contact fields only.** Greeting + technology type (LPBF / DED /
   binder-jet) + closing. The letter body itself is fixed by FOA.
3. **Track responses in a lightweight table** (session SQL or spreadsheet):
   - recipient, institution, technology (LPBF/DED/BJ), institution_class
     (university / DOE lab / company), sent_date, response_status,
     signed_letter_file
4. **Tally for the narrative `[TBD_N_*]` counters** in
   `flaime-genesis-proposal.tex:686-694` as signed letters come back.
   Conservative policy: count only letters received by T-48h before
   submission; update the tex once.
5. **Store signed PDFs** in `appendix-7/distributed-network/` (gitignored
   until submission).

## PI action items

- [ ] Greenlight mass outreach (yes/no) — this generates ~75 emails
- [ ] Decide on institutional-class bucketing (narrative counts
      universities / labs / companies separately)
- [ ] Confirm tech-type options (LPBF only, or include DED + binder jet?
      The narrative currently lists all three)
- [ ] Assign a tally-owner (PI? MS student?) to track responses and
      update `[TBD_N_*]` placeholders before submission freeze
