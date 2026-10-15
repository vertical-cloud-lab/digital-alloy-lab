# Makefile --- Utah AI Convergence 2026 talk (beamer)
#
#   make slides   -> talk.pdf          (audience deck, no speaker notes)
#   make notes    -> talk-notes.pdf    (deck + speaker notes for rehearsal)
#   make handout  -> talk-handout.pdf  (one frame/page, overlays collapsed)
#   make all      -> slides + notes + handout
#   make clean    -> remove build artifacts (keeps the three PDFs)

TEX   = talk
LATEX = pdflatex -interaction=nonstopmode -halt-on-error

.PHONY: all slides notes handout clean

all: slides notes handout

# Audience deck (default): no notes, no watermark
slides:
	$(LATEX) --jobname=$(TEX) "\input{$(TEX)}"
	$(LATEX) --jobname=$(TEX) "\input{$(TEX)}"

# Rehearsal deck: speaker notes shown alongside each slide
notes:
	$(LATEX) --jobname=$(TEX)-notes "\def\shownotes{}\input{$(TEX)}"
	$(LATEX) --jobname=$(TEX)-notes "\def\shownotes{}\input{$(TEX)}"

# Handout: overlays collapsed, one frame per page
handout:
	$(LATEX) --jobname=$(TEX)-handout "\def\handout{}\input{$(TEX)}"
	$(LATEX) --jobname=$(TEX)-handout "\def\handout{}\input{$(TEX)}"

clean:
	rm -f $(TEX).aux $(TEX).log $(TEX).nav $(TEX).out $(TEX).snm $(TEX).toc
	rm -f $(TEX)-notes.aux $(TEX)-notes.log $(TEX)-notes.nav $(TEX)-notes.out $(TEX)-notes.snm $(TEX)-notes.toc
	rm -f $(TEX)-handout.aux $(TEX)-handout.log $(TEX)-handout.nav $(TEX)-handout.out $(TEX)-handout.snm $(TEX)-handout.toc
