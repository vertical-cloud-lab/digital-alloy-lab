# FLAIME critical-minerals concept outlines

Three 1–2 page concept outlines extracted from `nsf-funding-opportunities.md` (the "Best critical-minerals fit — one each from NSF, DOE, DoD" section). Each is a self-contained LaTeX document compiled to PDF for sharing.

| # | Agency | Solicitation | Source | PDF | DOCX |
|---|---|---|---|---|---|
| 1 | NSF | DMREF (NSF 25-508) | [`01_nsf_dmref.tex`](01_nsf_dmref.tex) | [`01_nsf_dmref.pdf`](01_nsf_dmref.pdf) | [`01_nsf_dmref.docx`](01_nsf_dmref.docx) |
| 2 | DOE | AMMTO Multi-Topic / CMI Hub | [`02_doe_ammto_cmi.tex`](02_doe_ammto_cmi.tex) | [`02_doe_ammto_cmi.pdf`](02_doe_ammto_cmi.pdf) | [`02_doe_ammto_cmi.docx`](02_doe_ammto_cmi.docx) |
| 3 | DoD | DARPA DSO Office-Wide BAA | [`03_darpa_dso.tex`](03_darpa_dso.tex) | [`03_darpa_dso.pdf`](03_darpa_dso.pdf) | [`03_darpa_dso.docx`](03_darpa_dso.docx) |

The PDFs are the canonical, reference-quality output from the LaTeX source (preserves the TikZ pipeline DAG and typography). The DOCX copies are converted from the PDFs with `pdf2docx` for reviewers who require a Word format; layout fidelity is best-effort and the LaTeX/PDF pair should be treated as authoritative.

## Build

```sh
# PDFs from LaTeX source
pdflatex -interaction=nonstopmode 01_nsf_dmref.tex
pdflatex -interaction=nonstopmode 02_doe_ammto_cmi.tex
pdflatex -interaction=nonstopmode 03_darpa_dso.tex

# DOCX copies from the PDFs
python -c "from pdf2docx import Converter; \
[ (lambda p: (Converter(p).convert(p.replace('.pdf','.docx')), Converter(p).close()))(p) \
  for p in ['01_nsf_dmref.pdf','02_doe_ammto_cmi.pdf','03_darpa_dso.pdf'] ]"
```

Requires `pdflatex` (`texlive-latex-base`, `texlive-latex-recommended`, `texlive-latex-extra`, `texlive-fonts-recommended`) for the PDFs and `pip install pdf2docx` for the DOCX copies.
