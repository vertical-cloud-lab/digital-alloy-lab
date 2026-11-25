# Independent review reproduction

Run from the supplied workspace:

```sh
python outputs/recompute.py /workspace
python outputs/truth_checks.py /workspace
python outputs/certify_shortlist.py /workspace
```

The first script reproduces budget scores, standard errors and paired Wilcoxon tests without importing compare.py/analyze.py. The second runs a new million-design truth audit and build rescoring. The third rigorously excludes hard immersion passes on the original tiered shortlists using factorwise bounds over process rectangles and the analytic maximum powder quality. Dependencies: numpy, scipy, pandas; truth checks also require torch, botorch and gpytorch. Runtime versions are in runtime.json.

All other executed notebook inputs (including diagnostics and script creation) are preserved in executed_notebook_history.txt; that file is a provenance log, not a promised linear CLI. No finished high-fidelity copper pKGFN run was supplied or generated. report.md contains the complete conclusions and limitations. references.bib contains full primary-source citations.
