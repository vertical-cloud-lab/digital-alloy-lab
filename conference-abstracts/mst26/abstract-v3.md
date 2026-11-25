# MS&T '26 Abstract — Draft v3 (150-word portal-compliant)

**Symposium:** Autonomous Synthesis and Characterization: Experiments and Digital Twins for Theory-Enhanced Self-Driving Laboratories of the Future (ACerS Basic Science Division)

**Meeting:** MS&T26 — Materials Science & Technology

**Organizers:** R. K. Vasudevan (ORNL), Y. Liu (ORNL), A. Biswas (UTK), B. Narayanan (UofL)

**Portal rules (per organizer guidance):** ≤150 words; sentence case in the title (no Title Case); no hard returns in the body; special characters via portal codes (see `submission.txt`).

**Revision history:**
- v1: initial draft (broad framing).
- v2: Edison 4-persona mock review revisions; subsequently edited by Sterling Baird and Xavier Zaitzeff (cost numbers, EHVI/hypervolume framing, "10+ atomization/print cycles," BYU MechE author list).
- v3 (this file): trims v2 to the portal's 150-word limit while preserving Sterling/Xavier edits; converts title to sentence case.

---

## Title (sentence case)

Cost-aware Bayesian optimization across a CALPHAD–atomization–LPBF function network for critical-mineral-lean aluminum alloy discovery

## Authors

Sterling Baird, Xavier Zaitzeff, Gage Erickson, Ronnie Guymon, Carl Robison, Timothy Commins

Department of Mechanical Engineering, Brigham Young University, 701 E University Parkway, 350 EB, Provo, UT 84602

## Body (150 words, single paragraph — no hard returns when pasted into the portal)

Autonomous alloy discovery for additive manufacturing is a multi-stage decision problem with per-query costs spanning more than an order of magnitude: ≈$1500 per ultrasonic atomization run, ≈$1–5k per LPBF build, ≈$200 per ASTM E8 tensile bar, and substantially more per industrial gas atomization batch. Tiered screening (e.g., experimentally validating top-performing simulations) wastes budget on uninformative expensive queries and forfeits the algorithm's ability to strategically sample and learn cross-measurement biases early. We present FLAIME (Fast Learning AI for Mineral Efficiency), which applies the partial Knowledge Gradient for Function Networks (pKGFN) to a directed acyclic graph of CALPHAD (TC-Python/TCAl10/AM Module), atomization, LPBF, and microstructure–hardness–tensile nodes; each is a Gaussian process whose posterior feeds its children. Ultimate tensile strength, yield strength, elongation, and a printability score are jointly maximized via expected hypervolume improvement while penalizing a USGS-derived critical-mineral burden. We present synthetic-network benchmarks showing ≥3× sample efficiency and an initial campaign spanning 10+ atomization/print cycles.
