# Makefile for FLAIME Genesis Mission Proposal
# Single-source build: draft, clean, and final PDFs
# are all compiled from flaime-genesis-proposal.tex.
#
#   make draft     -> annotated PDF (watermark + todonotes + all sections)
#   make clean-pdf -> clean PDF (no watermark, no notes, all sections)
#   make final     -> submission-ready Field 8 PDF (also removes abstract, biosketch, budget)
#   make diff      -> latexdiff PDF vs last committed version (clean build)
#   make all       -> draft + clean + final + diff

TEX   = flaime-genesis-proposal
CLEAN = $(TEX)-clean
FINAL = $(TEX)-final
DIFF  = $(TEX)-diff
LATEX = pdflatex -interaction=nonstopmode

.PHONY: all draft clean-pdf final diff clean

# Build all variants
all: draft clean-pdf final diff

# Draft build: watermark + todonotes visible
draft:
	$(LATEX) $(TEX).tex
	bibtex $(TEX)
	$(LATEX) $(TEX).tex
	$(LATEX) $(TEX).tex

# Clean build: no watermark, no todonotes, all sections still present
clean-pdf:
	$(LATEX) --jobname=$(CLEAN) "\def\cleanbuild{}\input{$(TEX)}"
	bibtex $(CLEAN)
	$(LATEX) --jobname=$(CLEAN) "\def\cleanbuild{}\input{$(TEX)}"
	$(LATEX) --jobname=$(CLEAN) "\def\cleanbuild{}\input{$(TEX)}"

# Final/submission build: no watermark, no notes, abstract + biosketch + budget removed
final:
	$(LATEX) --jobname=$(FINAL) "\def\submissionbuild{}\input{$(TEX)}"
	bibtex $(FINAL)
	$(LATEX) --jobname=$(FINAL) "\def\submissionbuild{}\input{$(TEX)}"
	$(LATEX) --jobname=$(FINAL) "\def\submissionbuild{}\input{$(TEX)}"

# Diff build: latexdiff of working copy vs last committed version (clean mode)
# Requires: latexdiff, git
diff:
	git show HEAD:genesis-mission-proposal/$(TEX).tex > $(DIFF)-base.tex
	latexdiff $(DIFF)-base.tex $(TEX).tex > $(DIFF).tex
	$(LATEX) --jobname=$(DIFF) "\def\cleanbuild{}\input{$(DIFF)}"
	-bibtex $(DIFF)
	$(LATEX) --jobname=$(DIFF) "\def\cleanbuild{}\input{$(DIFF)}"
	$(LATEX) --jobname=$(DIFF) "\def\cleanbuild{}\input{$(DIFF)}"
	rm -f $(DIFF)-base.tex

# Remove all generated files
clean:
	rm -f $(TEX).aux $(TEX).log $(TEX).out $(TEX).fdb_latexmk $(TEX).fls $(TEX).pdf $(TEX).bbl $(TEX).blg
	rm -f $(CLEAN).aux $(CLEAN).log $(CLEAN).out $(CLEAN).pdf $(CLEAN).bbl $(CLEAN).blg
	rm -f $(FINAL).aux $(FINAL).log $(FINAL).out $(FINAL).pdf $(FINAL).bbl $(FINAL).blg
	rm -f $(DIFF).aux $(DIFF).log $(DIFF).out $(DIFF).pdf $(DIFF).bbl $(DIFF).blg $(DIFF).tex $(DIFF)-base.tex
