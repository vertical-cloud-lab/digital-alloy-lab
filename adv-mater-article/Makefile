# Advanced Materials collection article: build
#
#   make draft    manuscript + SI with line numbers and visible [TBD] markers (default)
#   make clean-pdf  same text, markers hidden (to read the prose as a reviewer would)
#   make refs     rebuild references.bib from tools/refs.tsv and re-check it against Crossref
#   make figs     regenerate the figures that have scripts
#   make atomizer RUNS='<glob of run.yaml>'   Fig. 2/3b and the repeatability check from run records
#   make bofn-sync  refresh the optimizer benchmark's numbers, curves and SI figures from BOFN_REF
#   make bofn-check check that those files still match BOFN_REF
#   make all      refs + figs + draft + clean-pdf
#   make clean    remove LaTeX intermediates
#
# Needs: pdflatex, biber, latexmk (TeX Live with biblatex-chem), Python 3 with requests + matplotlib.

LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error
CLEANDEF = \def\cleanbuild{}

# The optimizer's synthetic benchmark belongs to the BOFN methods paper (issue #121). Its paper_stats.py
# writes ../benchmarks/bofn-paper/paper-stats/ (numbers.tex: every number as a \stat{key} macro; curves.csv;
# table-contrasts.tex) and its paper_figures.py the two SI figures below. This article reads those files
# unchanged, at the same paths, so its numbers cannot disagree with the MethodsX draft. Never edit them
# here: rerun paper_stats.py on the BOFN branch, then `make bofn-sync`. After that branch merges, use
# BOFN_REF=origin/main.
BOFN_REF ?= origin/claude/issue-121-20261127-1913
BOFN_PATHS = benchmarks/bofn-paper/paper-stats \
	bofn-methods-article/figures/fig-curves-am.pdf bofn-methods-article/figures/fig-curves-am.png \
	bofn-methods-article/figures/fig-speedup-am.pdf bofn-methods-article/figures/fig-speedup-am.png
BOFN_DEPS = $(wildcard ../benchmarks/bofn-paper/paper-stats/*) $(wildcard ../bofn-methods-article/figures/*-am.pdf)

.PHONY: all draft clean-pdf refs figs atomizer bofn-sync bofn-check clean

draft: manuscript.pdf supporting-information.pdf

manuscript.pdf: manuscript.tex references.bib $(wildcard figures/*) $(BOFN_DEPS)
	$(LATEXMK) manuscript.tex

supporting-information.pdf: supporting-information.tex references.bib $(wildcard figures/*) $(wildcard si/*) $(BOFN_DEPS)
	$(LATEXMK) supporting-information.tex

clean-pdf:
	$(LATEXMK) -jobname=manuscript-clean -usepretex='$(CLEANDEF)' manuscript.tex
	$(LATEXMK) -jobname=supporting-information-clean -usepretex='$(CLEANDEF)' supporting-information.tex

refs:
	python tools/build_bib.py
	python tools/check_refs.py

figs:
	python tools/make_figures.py

atomizer:
	python tools/atomizer_analysis.py --runs '$(RUNS)' --out figures/

bofn-sync:
	git fetch origin $(patsubst origin/%,%,$(BOFN_REF))
	cd .. && git checkout $(BOFN_REF) -- $(BOFN_PATHS)
	python tools/make_figures.py

bofn-check:
	cd .. && git diff --quiet $(BOFN_REF) -- $(BOFN_PATHS) && echo "optimizer benchmark files match $(BOFN_REF)"

all: refs figs draft clean-pdf

clean:
	latexmk -C manuscript.tex supporting-information.tex
	latexmk -C -jobname=manuscript-clean manuscript.tex
	latexmk -C -jobname=supporting-information-clean supporting-information.tex
