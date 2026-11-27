# Fit-check email to the Dynamic Data and Information Processing portfolio

Goes with `afosr-yip-white-paper-a2c.tex`. Send before the white paper deadline
(Fri 2026-10-09, 11:59 PM ET). The BAA lists the portfolio mailbox below for
Dr. Blasch, and the NOFO asks for the NOFO number in the subject line.

**To:** D2IP@us.af.mil
**Subject:** FA955026S0003 YIP white paper: fit question for Dynamic Data and Information Processing

```text
Dr. Blasch,

I plan to submit an FY27 YIP white paper (FA955026S0003) by October 9 and would like to check whether it fits Dynamic Data and Information Processing.

Developing a printed alloy runs through steps whose measurements take from minutes (thermodynamic calculations) to days (high-temperature tests), and today every candidate goes through every step. I would link physics models and data from each step with propagated uncertainty, and decide as results arrive which measurement to collect next and on which candidate. The method builds on cost-aware Bayesian optimization of function networks. I would extend it to several competing objectives and to batches whose results arrive at different times, and demonstrate it on a five-step physical workflow. Published tests of the method have used simulators. Printable high-strength aluminum alloys for aircraft are the test case.

The plan is a single-PI effort at about $150K per year for three years. Does this fit your portfolio?

Thank you,
Sterling Baird
Assistant Professor, Mechanical Engineering, Brigham Young University
sterling.baird@byu.edu | (801) 422-5344
```

## Notes

- The BAA asks researchers to contact the program officer first about the
  state of the art, how the work would advance it, and the yearly cost. The
  second paragraph covers the first two and the third gives the cost.
- The three advances named in the email (several objectives, results that
  arrive at different times, a physical five-step workflow) are the ones in
  Section 3 of the white paper. "Published tests of the method have used
  simulators" refers to Astudillo & Frazier (NeurIPS 2021) and Buathong et al.
  (ICML 2024).
- Checked with the cringe-filter `email` context (2026-10-08): no findings,
  169 words with the signature (budget 170).
- The test case is aluminum, matching the white paper. The atomizer's
  induction module covers aluminum but not refractory alloys, which need the
  plasma module. An earlier draft of this email named refractory alloys.
- If both this and the A.3.a white paper go in, set `\otherwhitepapers` at the
  top of each `.tex` file to name the other one (NOFO p. 21).
