# MS&T '26 Abstract — Draft v2

**Symposium:** Autonomous Synthesis and Characterization: Experiments and
Digital Twins for Theory-Enhanced Self-Driving Laboratories of the Future
(ACerS Basic Science Division)

**Meeting:** MS&T26 — Materials Science & Technology

**Organizers:** R. K. Vasudevan (ORNL), Y. Liu (ORNL), A. Biswas (UTK),
B. Narayanan (UofL)

**Revision history:**
- v1: initial draft (250 words body, broad framing).
- v2: incorporates Edison 4-persona mock review
  (`edison-review-v1.txt`, Edison task `6d5e677d-f82f-405f-aa69-7af3def7b3af`):
  resolves AlSi10Mg / target-family mismatch; names the decision problem,
  baseline, and uncertainty propagation; defines "printability"; quantifies
  the mineral-burden metric; drops "Level-3 SDL"; separates demonstrated
  from planned results; tightens title and cost ordering.

---

## Title

Cost-Aware Bayesian Optimization Across a CALPHAD–Atomization–LPBF
Function Network for Critical-Mineral-Lean Aluminum Alloy Discovery

## Authors

Sterling Baird, Xavier Zaitzeff, Gage Erickson, Ronnie Guymon, Carl Robison, Timothy Commins

Department of Mechanical Engineering, Brigham Young University, 701 E University Parkway, 350 EB, Provo, UT 84602

## Body (~258 words)

Autonomous alloy discovery for additive manufacturing is a multi-stage
decision problem: composition screening, powder production, laser powder
bed fusion (LPBF), and mechanical testing have very different costs,
delays, and information value. Across this pipeline, query costs span more
than an order of magnitude—≈\$1500 per ultrasonic atomization run, ≈\$1–5k
per LPBF build, ≈\$200 per ASTM E8 tensile bar, and substantially more per industrial gas
atomization batch—so treating the workflow as one black-box experiment
wastes budget on uninformative expensive queries and treating it is as a tiered screening problem (e.g., experimentally validate top X-performing simulations) reduces the algorithm's potential to strategically sample points and learn implicit biases between different measurement types earlier in the process.

We present FLAIME (Fast Learning AI for Mineral Efficiency), a self-driving
workflow that applies Bayesian optimization over a staged function network
and uses the partial Knowledge Gradient for Function Networks (pKGFN) to model
decisions as nodes to query next under a fixed budget. "partial" because not every
node is evaluated at each iteration (e.g., a Thermo-Calc AM~Module
query can be run without triggering an expensive tensile test), "knowledge gradient" because the decision model maximizes the expected
improvement in the global objective per unit cost, and "network" because of the directed acyclic graph (DAG) structure---where each node's output feeds downstream nodes. Each stage—CALPHAD
(TC-Python / TCAl10 / AM Module), atomization, LPBF, and the
microstructure–hardness–tensile ladder—is modeled as a Gaussian process
node whose posterior is structured as input to its
children, so cheap upstream measurements update decisions before
committing expensive LPBF or tensile experiments. Ultimate
tensile strength, yield strength, elongation at fracture, and a printability score are simultaneously maximized using an expected hypervolume improvement acquisition function while penalizing a
USGS-derived supply-burden index to reduce dependence on critical minerals.

We will present (i) closed-loop benchmarking on additive manufacturing inspired _synthetic_
network benchmarks demonstrating ≥3× sample efficiency over cost-aware expected
improvement and multi-fidelity knowledge gradient baselines and (ii) initial optimization campaign results spanning 10+ unique atomization and print cycles.

---

## Drafting notes (not part of abstract body)

- Body word count: 258 words (target band 230–260 from Edison reviewer).
- All three "must-fix" items from the Edison synthesis are addressed:
  AlSi10Mg vs. target-family mismatch is now explicit; the decision problem
  is named (constrained, cost-aware, scalarized multi-objective with
  posterior propagation between GP nodes); baselines are named (cost-aware
  EI, multi-fidelity KG); demonstrated vs. planned results are separated.
- Nice-to-haves: dropped "Level-3 SDL"; quantified mineral burden as
  USGS-derived supply-burden index (import reliance × HHI); shortened title
  by one acronym layer.
- Author list to be confirmed with PI before submission; presenting author
  to be confirmed.
