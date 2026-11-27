# Campaign paper build.
#   make            -> main.pdf (draft: notes and line numbers shown, placeholders in red)
#   make clean-pdf  -> main-clean.pdf (notes hidden; placeholders stay visible on purpose)
#   make si         -> si.pdf
#   make figures    -> redraw figures, tables and numbers from ../data (needs matplotlib, pandas)
#   make refs       -> check every reference against Crossref / DataCite
PY ?= python3
LATEX = pdflatex -interaction=nonstopmode -halt-on-error

.PHONY: all draft clean-pdf si figures refs clean
all: figures draft si

draft:
	$(LATEX) main.tex >/dev/null
	bibtex main >/dev/null
	$(LATEX) main.tex >/dev/null
	$(LATEX) main.tex | grep -E "Warning|Error" | grep -v "Font\|float specifier" || true

clean-pdf:
	$(LATEX) --jobname=main-clean "\def\cleanbuild{}\input{main}" >/dev/null
	bibtex main-clean >/dev/null
	$(LATEX) --jobname=main-clean "\def\cleanbuild{}\input{main}" >/dev/null
	$(LATEX) --jobname=main-clean "\def\cleanbuild{}\input{main}" >/dev/null

si:
	$(LATEX) si.tex >/dev/null
	bibtex si >/dev/null
	$(LATEX) si.tex >/dev/null
	$(LATEX) si.tex >/dev/null

figures:
	$(PY) ../scripts/make_figures.py

refs:
	$(PY) ../scripts/check_refs.py

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.spl *.toc *.lof *.lot
