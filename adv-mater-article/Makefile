# Advanced Materials collection article: build
#
#   make draft    manuscript + SI with line numbers and visible [TBD] markers (default)
#   make clean-pdf  same text, markers hidden (to read the prose as a reviewer would)
#   make refs     rebuild references.bib from tools/refs.tsv and re-check it against Crossref
#   make figs     regenerate the figures that have scripts
#   make all      refs + figs + draft + clean-pdf
#   make clean    remove LaTeX intermediates
#
# Needs: pdflatex, biber, latexmk (TeX Live with biblatex-chem), Python 3 with requests + matplotlib.

LATEXMK = latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error
CLEANDEF = \def\cleanbuild{}

.PHONY: all draft clean-pdf refs figs clean

draft: manuscript.pdf supporting-information.pdf

manuscript.pdf: manuscript.tex references.bib $(wildcard figures/*)
	$(LATEXMK) manuscript.tex

supporting-information.pdf: supporting-information.tex references.bib $(wildcard figures/*) $(wildcard si/*)
	$(LATEXMK) supporting-information.tex

clean-pdf:
	$(LATEXMK) -jobname=manuscript-clean -usepretex='$(CLEANDEF)' manuscript.tex
	$(LATEXMK) -jobname=supporting-information-clean -usepretex='$(CLEANDEF)' supporting-information.tex

refs:
	python tools/build_bib.py
	python tools/check_refs.py

figs:
	python tools/make_figures.py

all: refs figs draft clean-pdf

clean:
	latexmk -C manuscript.tex supporting-information.tex
	latexmk -C -jobname=manuscript-clean manuscript.tex
	latexmk -C -jobname=supporting-information-clean supporting-information.tex
