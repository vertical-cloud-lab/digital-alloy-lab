# The synthetic alloy network as a DAG

Requested on a pull request in a private repo,
2026-10-05: draw the function network behind the BOFN preliminary results the
way function networks are drawn elsewhere in this work (the FLAIME DAG on this
branch, the x/f/y figure from the BOFN papers in the Utah deck), including the
views that teach partial evaluation.

Everything here is generated from [`../bofn_alloy.py`](../bofn_alloy.py):
[`network_dag.py`](network_dag.py) reads `SPEC`, `GROUPS`, `COSTS` and `LAMBDA`
out of that file (without importing torch), so the picture cannot drift from
the code that ran the benchmark. Styling follows the deck: Aptos, gray boxes,
red as the only highlight, no legend, labels joined by plain lines, no message
baked into the image (the slide headline carries it).

## The graph

| Node | Stage (cost per action) | Inputs | Returns |
|---|---|---|---|
| `s` | CALPHAD ($10, one call returns all three) | composition `c` = Zn+Mg, Cu, Zr, Sc | strengthening-phase fraction |
| `f` | CALPHAD | `c` | freezing range |
| `g` | CALPHAD | `c` | primary-nucleant (Al3Zr / Al3Sc) fraction |
| `q` | Atomize ($1,500 per run) | atomizer setting `a`, `g` | powder quality |
| `rho` | Print ($2,500 per build) | laser power `P`, scan speed `v`, `f`, `g`, `q` | dense, crack-free fraction |
| `U` | Test ($200 per bar) | `s`, `rho` | strength |
| objective | known, free | `U`, `c` | `U` − 0.3 × critical-mineral burden `B(c)` |

A full make-print-test pass on one design costs $4,210. Physical rules in the
benchmark: a powder lot must exist before it can be printed, a build before it
can be tested, one lot can be printed many times, and the first experiment on an
alloy runs its CALPHAD call automatically. The one simulation-versus-experiment
gap is the `g → rho` edge (`kappa`): nucleants suppress hot cracking in the
print, which a freezing-range screen cannot see
([Martin et al., Nature 2017](https://doi.org/10.1038/nature23894)). Costs are
the abstract's; $10 for CALPHAD is an assumption.

## Files

| File | What | Suggested headline |
|---|---|---|
| [`bofn_dag_network.png`](bofn_dag_network.png) | The network in the FLAIME-DAG style: a column per stage with its cost, rounded gray boxes, the three CALPHAD outputs grouped as one call, the known penalty routed above as a dashed bypass | The benchmark is **a network of six surrogate nodes** in four priced stages |
| [`bofn_dag_network_symbols.png`](bofn_dag_network_symbols.png) | The same with the code's node letters and the cost units | same |
| [`bofn_dag_posteriors.png`](bofn_dag_posteriors.png) | A posterior glyph on every node-to-node edge (the proposal figure's convention) | **One Gaussian process per node**; each child sees its parents' outputs |
| [`bofn_dag_paper_style.png`](bofn_dag_paper_style.png) | The graph as Astudillo & Frazier (2021) and Buathong et al. (2024) draw function networks: circles `f_k`, bare inputs `x_i`, outputs `y_k` on the edges | The same network the way the BOFN papers draw it |
| [`bofn_dag_paper_style_words.png`](bofn_dag_paper_style_words.png) | The paper style with gray words and costs next to each node | same |
| [`bofn_dag_missed_effect.png`](bofn_dag_missed_effect.png) | The `g → rho` edge in red with a callout | The effect a CALPHAD screen **cannot see** |
| [`bofn_dag_partial_simulate.png`](bofn_dag_partial_simulate.png), [`_atomize`](bofn_dag_partial_atomize.png), [`_print`](bofn_dag_partial_print.png), [`_test`](bofn_dag_partial_test.png) | One action at a time: its stage header, nodes, incoming edges and chosen input in red, everything else faint | Simulate one composition for **$10** / Atomize one powder lot for **$1,500** / Print one build for **$2,500** / Test one bar for **$200** |
| [`bofn_dag_full_chain.png`](bofn_dag_full_chain.png) | All four stages red | Or run the whole chain for **$4,210**: what the full-pipeline policies buy per design |
| [`bofn_dag_partial_evaluation.gif`](bofn_dag_partial_evaluation.gif) | Flip-book (1.6 s a frame): the network, then the four actions, then the chain | |
| [`contact-sheet.jpg`](contact-sheet.jpg) | All eleven PNGs on one sheet | |
| [`bofn-dag-slides.pptx`](bofn-dag-slides.pptx) | Nine slides on the Utah master, native shapes with Morph: network, GPs, the four actions, the chain, the missed effect, network again. Built by [`scripts/slides/bofn_dag_slides.py`](../../../../scripts/slides/bofn_dag_slides.py); notes carry the detail | |
| [`bofn-dag-figure.pptx`](bofn-dag-figure.pptx) | The network alone on a blank slide, editable | |
| [`bofn-dag-slides-contact-sheet.jpg`](bofn-dag-slides-contact-sheet.jpg), [`-slides.pdf`](bofn-dag-slides-slides.pdf) | LibreOffice renders of the deck (Aptos installed) | |

Both `.pptx` files pass the Open XML SDK validator with 0 errors
([`scripts/slides/ooxml_validate/`](../../../../scripts/slides/ooxml_validate/)).
Morph needs PowerPoint 2019 or 365; elsewhere the transition falls back to a
fade. Paste with *Use Destination Theme* and keep the slide order.

## Layout notes

- Columns are stages, and a stage is one priced action, so the cost sits in the
  column header rather than on each box; the dashed group around the three
  CALPHAD outputs says that one $10 call returns all of them.
- Inputs are white boxes with a light border (decision variables, not
  surrogates); the objective is white with a black border (a known function,
  not a GP). The atomizer setting and the laser settings sit under the node they
  feed, which keeps every long edge clear of every box.
- Edge end points are spread along a box's side in the order of the far end's
  row, so no two edges cross at a box.
- In the partial-evaluation views, red marks what the action pays for and
  observes: the stage header with its cost, the node(s), the edges that bring
  their inputs, and the input box the optimizer chooses. Faint gray is what
  already exists or is not touched.

Regenerate with

```bash
python presentations/2026-10-mst26/bofn-prelim/dag/network_dag.py
python scripts/slides/bofn_dag_slides.py
python scripts/slides/render_deck.py presentations/2026-10-mst26/bofn-prelim/dag/bofn-dag-slides.pptx \
    --out-dir presentations/2026-10-mst26/bofn-prelim/dag --name bofn-dag-slides --cols 3
```

(matplotlib, Pillow, python-pptx, lxml; LibreOffice and PyMuPDF for the renders;
Aptos from Microsoft's download, see the gap-slides README).
