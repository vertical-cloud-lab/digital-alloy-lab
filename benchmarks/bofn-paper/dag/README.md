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
| [`bofn_dag_timelapse.mp4`](bofn_dag_timelapse.mp4); GIF in two parts, [`_1.gif`](bofn_dag_timelapse_1.gif) (the first four policies) and [`_2.gif`](bofn_dag_timelapse_2.gif) (the last four) | Timelapse, 2 min 52 s: one seed-0 run per policy, one after another, tiered screening first. Every purchase lights its stage on the network, its alloy's elements on a periodic table and its alloy on a composition map, and the run's best demonstrated alloy is traced against spend underneath (see [Timelapse](#timelapse)) | Where each policy puts its $100k |
| [`bofn_dag_timelapse_final.png`](bofn_dag_timelapse_final.png) | The timelapse's last frame: all eight seed-0 traces | |
| [`bofn-dag-slides.pptx`](bofn-dag-slides.pptx) | Nine slides on the Utah master, native shapes with Morph: network, GPs, the four actions, the chain, the missed effect, network again. Built by [`scripts/slides/bofn_dag_slides.py`](../../../../scripts/slides/bofn_dag_slides.py); notes carry the detail | |
| [`bofn-dag-figure.pptx`](bofn-dag-figure.pptx) | The network alone on a blank slide, editable | |
| [`bofn-dag-slides-contact-sheet.jpg`](bofn-dag-slides-contact-sheet.jpg), [`-slides.pdf`](bofn-dag-slides-slides.pdf) | LibreOffice renders of the deck (Aptos installed) | |

Both `.pptx` files pass the Open XML SDK validator with 0 errors
([`scripts/slides/ooxml_validate/`](../../../../scripts/slides/ooxml_validate/)).
Morph needs PowerPoint 2019 or 365; elsewhere the transition falls back to a
fade. Paste with *Use Destination Theme* and keep the slide order.

## Timelapse

[`timelapse.py`](timelapse.py) plays back the purchase log of one run per policy
on the network above, all on seed 0 at κ = 1, so every policy starts from the
same seed alloys. The order is tiered screening, tiered with no powder reuse,
random, standard BO, BOFN full pipeline, KGFN full pipeline, BOFN + powder
reuse, then pKGFN.

- **A purchase is a button press.** The stage it buys lights red: its header,
  its node(s), the edges into them, and the input that the action chooses
  (composition, atomizer setting, or laser settings). The light then fades
  like a fluorescent tube settling after it strikes: 65% of the brightness goes
  with a 0.15 s time constant and the rest with 1 s. A new press lights it
  again at full brightness. The objective box lights when a tensile test beats
  the best alloy so far.
- **The periodic table** (lower left) shows the composition of each purchase.
  Every purchase, at any stage, lights the alloy's elements in proportion to
  their amount (the design variables are scaled to 0–1), and they then fade the
  same way. Zn and Mg always light together, because they are one variable.
  Al is the balance and stays outlined.
- **The alloy map** (lower right) is the run's own copy of
  [`../behaviour`](../behaviour)'s composition figure, in CALPHAD's freezing-range
  index f and nucleant fraction g, with the screen cutoff, the 50% crack line
  and the optimum. A purchase lights its alloy's dot. When the light fades,
  the dot stays: gray if the alloy has only been simulated, blue once it has
  been atomized or printed, growing with each print. Tiered screening's
  CALPHAD screen fills the map with gray, and its four made alloys sit on the
  screen's cutoff.
- **Video time is proportional to spend**, at 18 s per $100k, so every run
  takes as long. That is 2.6 times slower than the first version, and it adds
  a 1 s title before each run and a 2 s hold after it, for 2 min 52 s in all.
  A $10 CALPHAD call is a blink, and tiered screening's 224-call screen takes
  0.4 s. The counter under each stage header counts that stage's purchases,
  and the figure at the top right is the money committed so far.
- **The trace** is that run's best demonstrated alloy (% of the true optimum)
  against spend. The y range is the finished plot's range from the first frame.
  Finished runs stay on the plot in the slide figures' styles, with labels at
  the positions they take in the last frame.
- **Data.** Only runs made after the port carry a purchase log:
  [`../results-rerun/k1`](../results-rerun/k1) (identical to the stored runs,
  action for action; see [`../PORT.md`](../PORT.md)) and
  [`../quality/kgfn-smoke/k1`](../quality/kgfn-smoke/k1) for KGFN. One seed is
  an anecdote, not a result: on seed 0, full-pipeline BOFN ends below standard
  BO, the reverse of the 20-seed means in the slide figures.
- The burden note above the dashed bypass makes way for the purchase counters.
- **Files.** The MP4 is the smooth version, at 1600 px and 20 fps. The GIF is 800 px at 5 fps, split into
  two files of four runs each, so that each stays under the 10 MB GitHub shows inline.

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
python benchmarks/bofn-paper/dag/timelapse.py   # about 13 min on 2 cores, plus 3 to encode; --seed, --policies
python scripts/slides/render_deck.py presentations/2026-10-mst26/bofn-prelim/dag/bofn-dag-slides.pptx \
    --out-dir presentations/2026-10-mst26/bofn-prelim/dag --name bofn-dag-slides --cols 3
```

(matplotlib, Pillow, python-pptx, lxml; LibreOffice and PyMuPDF for the renders;
Aptos from Microsoft's download, see the gap-slides README; the timelapse also
needs `../requirements.txt` for the true optimum, and ffmpeg, for which the
`imageio-ffmpeg` wheel's binary is enough).
