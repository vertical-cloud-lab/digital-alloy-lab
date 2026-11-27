# Makefile for the AFOSR FY27 YIP white paper (NOFO FA955026S0003)
#
#   make          -> afosr-yip-white-paper.pdf (A.3.a version: cover, 5-page
#                    body, references, then the CV from ../bios/baird-CV.pdf)
#                    and afosr-yip-white-paper-a2c.pdf (A.2.c version)
#   make a2c      -> only the A.2.c version
#   make preview  -> preview/page-N.png (A.3.a) and preview/a2c/page-N.png
#                    for the cover, body, and references
#                    (needs pdftoppm; the CV pages are not rendered)
#   make lint     -> cringe-filter lint + score, proposal context
#   make clean    -> remove LaTeX build artifacts (keeps the PDF)
#
# XeLaTeX uses the real Times New Roman when it is installed (macOS, Windows,
# or ttf-mscorefonts-installer on Linux) and TeX Gyre Termes otherwise.
# LATEX=pdflatex also works and uses the mathptmx Times clone.

TEX   = afosr-yip-white-paper
A2C   = afosr-yip-white-paper-a2c
LATEX = xelatex -interaction=nonstopmode -halt-on-error
CV    = ../bios/baird-CV.pdf
# Cover page + 5 body pages + 2 reference pages
PREVIEW_PAGES = 8

.PHONY: all a2c preview lint clean

all: $(TEX).pdf $(A2C).pdf

a2c: $(A2C).pdf

$(TEX).pdf: $(TEX).tex $(wildcard $(CV))
	$(LATEX) $(TEX).tex
	$(LATEX) $(TEX).tex

$(A2C).pdf: $(A2C).tex $(wildcard $(CV))
	$(LATEX) $(A2C).tex
	$(LATEX) $(A2C).tex

preview: $(TEX).pdf $(A2C).pdf
	mkdir -p preview/a2c
	rm -f preview/page-*.png preview/a2c/page-*.png
	pdftoppm -r 110 -png -f 1 -l $(PREVIEW_PAGES) $(TEX).pdf preview/page
	pdftoppm -r 110 -png -f 1 -l $(PREVIEW_PAGES) $(A2C).pdf preview/a2c/page

lint:
	cringe-filter lint -c proposal $(TEX).tex
	cringe-filter score -c proposal $(TEX).tex
	cringe-filter lint -c proposal $(A2C).tex
	cringe-filter score -c proposal $(A2C).tex

clean:
	rm -f $(TEX).aux $(TEX).log $(TEX).out $(TEX).fls $(TEX).fdb_latexmk
	rm -f $(A2C).aux $(A2C).log $(A2C).out $(A2C).fls $(A2C).fdb_latexmk
