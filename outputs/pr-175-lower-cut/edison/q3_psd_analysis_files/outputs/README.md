# SEM particle-size analysis

Read `report.md` for the complete numerical report and limitations.

`analysis.ipynb` is an executed notebook; `analysis.py` is the complete standalone code.

Install the pinned packages from `requirements.txt`, then rerun:

```bash
python analysis.py --input-dir inputs --output-dir rerun --bootstrap 20000
```

`fractions_and_intervals.csv` contains percentages or g per 100 g as labelled. Particle and field intervals are separate 95% percentile bootstrap intervals, conditional on counted particles. They do not cover missed-fine or aluminium-transfer bias.

Figure files are both 350 dpi PNG and vector PDF. Full original input files are in `inputs/`. Input hashes, seed and analysis settings are in `analysis_metadata.json`. The primary Lang citation is in `references.bib`.
