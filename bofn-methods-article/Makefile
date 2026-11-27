# BOFN methods write-ups (issue #121): build
#
#   make stats      rerun the statistics and figures from the run files (benchmarks/bofn-paper)
#   make draft      both PDFs with line numbers, red [brackets] and author notes (default)
#   make clean-pdf  the same text with brackets plain and notes hidden
#   make refs       rebuild references.bib from tools/refs.tsv and re-check it against Crossref
#   make all        stats + refs + draft + clean-pdf
#   make clean      remove LaTeX intermediates
#
# Needs: TeX Live with biblatex, biblatex-chem, biber, latexmk; Python 3.12 with
# benchmarks/bofn-paper/requirements.txt (+ requests for refs).

PY ?= python
LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error
CLEANDEF = \def\cleanbuild{}
BENCH = ../benchmarks/bofn-paper
STATS = $(BENCH)/paper-stats/numbers.tex

.PHONY: all draft clean-pdf stats refs clean

draft: methodsx/manuscript.pdf adv-mater/methods-si.pdf

methodsx/manuscript.pdf: methodsx/manuscript.tex preamble.tex references.bib $(STATS) $(wildcard figures/*)
	cd methodsx && $(LATEXMK) manuscript.tex

adv-mater/methods-si.pdf: adv-mater/methods-si.tex preamble.tex references.bib $(STATS) $(wildcard figures/*)
	cd adv-mater && $(LATEXMK) methods-si.tex

clean-pdf:
	cd methodsx && $(LATEXMK) -jobname=manuscript-clean -usepretex='$(CLEANDEF)' manuscript.tex
	cd adv-mater && $(LATEXMK) -jobname=methods-si-clean -usepretex='$(CLEANDEF)' methods-si.tex

stats:
	cd $(BENCH) && $(PY) paper_stats.py && $(PY) paper_figures.py

refs:
	$(PY) tools/build_bib.py
	$(PY) tools/check_refs.py

all: stats refs draft clean-pdf

clean:
	cd methodsx && latexmk -C manuscript.tex && latexmk -C -jobname=manuscript-clean manuscript.tex
	cd adv-mater && latexmk -C methods-si.tex && latexmk -C -jobname=methods-si-clean methods-si.tex
