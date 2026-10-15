# Utah AI Convergence 2026 --- Talk

Materials for a 10-minute talk by **Sterling Baird** on the **Advanced
Manufacturing Academic Panel** at the
[Utah AI Convergence 2026](https://www.price.utah.edu/ai/convergence-2026)
(June 23--24, 2026; panel June 23, 1:00 PM, moderated by Ashley Spear).

The talk presents the lab's work on *autonomous alloy discovery via additive
manufacturing for aerospace applications* and highlights the computing tools that
transfer to other manufacturing sectors --- per the organizer's request. It ties
in elements from the FLAIME DOE Genesis Mission proposal
(`genesis-mission-proposal/`).

## Files

| File | Purpose |
| --- | --- |
| `talk.tex` | Beamer source (one message per slide; speaker notes via `\note{}`) |
| `Makefile` | Build targets for the three PDF variants |
| `fetched-content/convergence-2026.md` | Snapshot of the event + program page |
| `fetched-content/vertical-cloud-lab-readme.md` | Snapshot of the lab's GitHub profile README |

## Building

Requires a TeX distribution with `beamer` (e.g. `texlive-latex-recommended`).

```bash
make slides    # talk.pdf          -- audience deck (no notes)
make notes     # talk-notes.pdf    -- deck + speaker notes (rehearsal)
make handout   # talk-handout.pdf  -- one frame/page, overlays collapsed
make all       # all three
```

The build toggles (`\def\shownotes{}`, `\def\handout{}`) are applied on the
command line by the Makefile; do not hand-edit the `\setbeameroption` lines.

## Design notes (Jean-luc Doumont principles)

- **One message per slide**, stated as a full-sentence message title.
- Slides carry only what the audience must *see*; everything speaker-oriented
  lives in `\note{}` and appears only in `talk-notes.pdf` --- never on the slide.
- Minimal, uncluttered theme; navigation symbols removed; visuals over bullet
  walls.

## Generated PDFs

`talk.pdf` (audience deck), `talk-notes.pdf` (rehearsal), and `talk-handout.pdf`
are committed for convenience and can be regenerated at any time with `make all`.
Intermediate LaTeX/beamer artifacts (`.aux`, `.log`, `.nav`, `.snm`, ...) are
git-ignored.
