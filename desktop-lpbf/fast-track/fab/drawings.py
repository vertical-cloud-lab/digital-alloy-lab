"""One drawing sheet per piece (#260, PR 294 round 2): hidden-line orthographic views from OpenCascade's HLR (the
same kernel FreeCAD's TechDraw uses), drawn with matplotlib, with overall dimensions, the hole table, material, stock,
the tolerances that matter and the finish. Sheet parts also get their flat pattern. Third-angle projection, mm.

FreeCAD TechDraw was not tried headless (time); TechDraw's views come from the same OpenCascade HLR, reached here
directly through OCP.

    /tmp/tools/capmem 2 /tmp/venv/bin/python desktop-lpbf/fast-track/fab/drawings.py [pid ...]
        -> fab/drawings/<pid>.pdf, fab/img/drawings-contact.png
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from OCP.BRepAdaptor import BRepAdaptor_Curve  # noqa: E402
from OCP.BRepTools import BRepTools  # noqa: E402
from OCP.BRep import BRep_Builder  # noqa: E402
from OCP.GCPnts import GCPnts_QuasiUniformDeflection  # noqa: E402
from OCP.gp import gp_Ax2, gp_Dir, gp_Pnt  # noqa: E402
from OCP.HLRAlgo import HLRAlgo_Projector  # noqa: E402
from OCP.HLRBRep import HLRBRep_Algo, HLRBRep_HLRToShape  # noqa: E402
from OCP.TopAbs import TopAbs_EDGE  # noqa: E402
from OCP.TopExp import TopExp_Explorer  # noqa: E402
from OCP.TopoDS import TopoDS, TopoDS_Shape  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
SCR = pathlib.Path("/tmp/ft-fab")
DDIR = HERE / "drawings"
VIEWS = {  # name: (view normal toward the viewer, x direction on the sheet)
    "top": ((0, 0, 1), (1, 0, 0)),
    "front": ((0, -1, 0), (1, 0, 0)),
    "right": ((1, 0, 0), (0, 1, 0)),
}


def read_brep(path):
    s = TopoDS_Shape()
    BRepTools.Read_s(s, str(path), BRep_Builder())
    return s


def edges_2d(comp, defl=0.03):
    out = []
    if comp is None or comp.IsNull():
        return out
    exp = TopExp_Explorer(comp, TopAbs_EDGE)
    while exp.More():
        e = TopoDS.Edge_s(exp.Current())
        try:
            c = BRepAdaptor_Curve(e)
            d = GCPnts_QuasiUniformDeflection(c, defl)
            if d.IsDone() and d.NbPoints() >= 2:
                pts = [d.Value(i) for i in range(1, d.NbPoints() + 1)]
                out.append(np.array([(p.X(), p.Y()) for p in pts]))
        except Exception:
            pass
        exp.Next()
    return out


def hlr(shape, view):
    n, x = VIEWS[view]
    algo = HLRBRep_Algo()
    algo.Add(shape)
    algo.Projector(HLRAlgo_Projector(gp_Ax2(gp_Pnt(0, 0, 0), gp_Dir(*n), gp_Dir(*x))))
    algo.Update()
    algo.Hide()
    h = HLRBRep_HLRToShape(algo)
    vis = edges_2d(h.VCompound()) + edges_2d(h.OutLineVCompound()) + edges_2d(h.Rg1LineVCompound())
    hid = edges_2d(h.HCompound()) + edges_2d(h.OutLineHCompound())
    return vis, hid


def bounds(lines):
    if not lines:
        return (0, 1, 0, 1)
    a = np.vstack(lines)
    return a[:, 0].min(), a[:, 0].max(), a[:, 1].min(), a[:, 1].max()


def dim_h(ax, x0, x1, y, text, k):
    ax.annotate("", xy=(x0, y), xytext=(x1, y), arrowprops=dict(arrowstyle="<->", lw=0.5, color="k",
                                                                shrinkA=0, shrinkB=0))
    ax.text((x0 + x1) / 2, y - 0.6 * k, text, ha="center", va="top", fontsize=5.5)


def dim_v(ax, x, y0, y1, text, k):
    ax.annotate("", xy=(x, y0), xytext=(x, y1), arrowprops=dict(arrowstyle="<->", lw=0.5, color="k",
                                                                shrinkA=0, shrinkB=0))
    ax.text(x - 0.6 * k, (y0 + y1) / 2, text, ha="right", va="center", fontsize=5.5, rotation=90)


def sheet(pc, path):
    dp = SCR / "pieces" / (pc["pid"] + "_draw.brep")
    shape = read_brep(dp if dp.exists() else SCR / "pieces" / (pc["pid"] + ".brep"))
    views = {v: hlr(shape, v) for v in VIEWS}
    b = {v: bounds(views[v][0] + views[v][1]) for v in VIEWS}
    wt, ht = b["top"][1] - b["top"][0], b["top"][3] - b["top"][2]
    wf, hf = b["front"][1] - b["front"][0], b["front"][3] - b["front"][2]
    wr = b["right"][1] - b["right"][0]
    gap = 0.18 * max(wt, wf, ht, hf, 20.0)
    # layout in model mm: front at origin, top above it, right to its right (third angle)
    off = {"front": (-b["front"][0], -b["front"][2]),
           "top": (-b["top"][0], hf + gap - b["top"][2]),
           "right": (wf + gap - b["right"][0], -b["right"][2])}
    flat = pc.get("sheet")
    fig = plt.figure(figsize=(11.69, 8.27))   # A4 landscape
    ax = fig.add_axes([0.03, 0.30, 0.62, 0.64])
    k = 0.03 * max(wf + gap + wr, hf + gap + ht)
    for v in VIEWS:
        ox, oy = off[v]
        vis, hid = views[v]
        for ln in hid:
            ax.plot(ln[:, 0] + ox, ln[:, 1] + oy, color="0.55", lw=0.35, ls=(0, (2, 1.5)))
        for ln in vis:
            ax.plot(ln[:, 0] + ox, ln[:, 1] + oy, color="k", lw=0.6)
        x0, x1, y0, y1 = b[v]
        ax.text(x0 + ox, y1 + oy + 0.5 * k, v.upper(), fontsize=6, color="0.3")
        if v in ("front", "top"):
            dim_h(ax, x0 + ox, x1 + ox, y0 + oy - 1.2 * k, "%.2f" % (x1 - x0), k)
        if v in ("front", "top"):
            dim_v(ax, x0 + ox - 1.2 * k, y0 + oy, y1 + oy, "%.2f" % (y1 - y0), k)
        if v == "right":
            dim_h(ax, x0 + ox, x1 + ox, y0 + oy - 1.2 * k, "%.2f" % (x1 - x0), k)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.autoscale()
    xl, yl = ax.get_xlim(), ax.get_ylim()
    ax.set_xlim(xl[0] - 2.5 * k, xl[1] + k)
    ax.set_ylim(yl[0] - 2.5 * k, yl[1] + k)
    # flat pattern for sheet parts
    if flat and flat.get("outline"):
        fx = fig.add_axes([0.66, 0.62, 0.32, 0.32])
        o = np.array(flat["outline"] + [flat["outline"][0]], float)
        fx.plot(o[:, 0], o[:, 1], "k", lw=0.7)
        for hx, hy, hd in flat.get("holes", []):
            fx.add_patch(plt.Circle((hx, hy), hd / 2, fill=False, lw=0.5))
        if flat.get("slot"):
            s = flat["slot"]
            fx.add_patch(plt.Rectangle((s["u0"], s["v0"]), s["u1"] - s["u0"], s["v1"] - s["v0"], fill=False, lw=0.5))
        for bd in flat.get("bends", []):
            if "v" in bd:
                fx.axhline(bd["v"], color="tab:blue", lw=0.5, ls="--")
        fx.set_aspect("equal")
        fx.set_title("flat pattern (t %.2f, K %s); bends: %s" % (
            flat["thickness"], flat.get("k_factor"), ", ".join("%s %.0f deg" % (bd["line"], bd["angle"])
                                                            for bd in flat.get("bends", []))[:90]), fontsize=6)
        fx.tick_params(labelsize=5)
    # title block and notes
    tx = fig.add_axes([0.66, 0.03, 0.33, 0.57 if flat and flat.get("outline") else 0.92])
    tx.axis("off")
    lines = ["%s  %s" % (pc["pid"], pc["name"]),
             "Qty %d   first needed in %s   route: %s" % (pc["qty"], pc["state"], pc["route"]),
             "Material: %s" % pc["material"], "Stock: %s" % pc["stock"]]
    if pc.get("stock_pn"):
        lines.append("Stock PN: %s" % pc["stock_pn"])
    if pc.get("pos"):
        lines.append("Datum: %s" % pc["pos"])
    lines.append("Tolerances: general ISO 2768-m (+-0.1 to 30 mm, +-0.2 to 120, +-0.3 to 400)")
    for t in pc.get("tol", []):
        lines.append(" - " + t)
    lines.append("Finish: %s" % pc.get("finish", ""))
    feats = [f for f in pc.get("features", []) if f["kind"] in ("pocket", "groove", "bore", "opening", "custom_slot",
                                                                  "adaptive")]
    if feats:
        lines.append("Features: " + "; ".join(f["name"] for f in feats))
    for what, mins in pc.get("lathe", []):
        lines.append("Lathe: " + what)
    for what, mins in pc.get("manual", []):
        lines.append("By hand: " + what)
    if pc.get("holes"):
        lines.append("Holes:")
        for h in pc["holes"]:
            lines.append(" %s  %d x  %s" % (h["id"], h["n"], h["callout"]))
    txt = []
    for ln in lines:
        txt += textwrap.wrap(ln, 95, subsequent_indent="    ")
    tx.text(0, 1, "\n".join(txt), va="top", ha="left", fontsize=5.6, family="DejaVu Sans")
    # changes against the assembly model, bottom left
    cx = fig.add_axes([0.03, 0.03, 0.62, 0.22])
    cx.axis("off")
    ch = ["Added or changed against ft_model (the assembly model):"] + [" - " + c for c in pc.get("changes", [])]
    ct = []
    for ln in ch:
        ct += textwrap.wrap(ln, 150, subsequent_indent="   ")
    cx.text(0, 1, "\n".join(ct[:16]), va="top", ha="left", fontsize=5.4)
    fig.text(0.03, 0.965, "Desktop LPBF fast track (#260): %s, %s. Third-angle projection, mm. Hidden lines grey. "
             "Drawn by fab/drawings.py from fab/parts.py; not checked by a person." % (pc["pid"], pc["name"]),
             fontsize=6.5)
    fig.savefig(path)
    fig.savefig(SCR / "drawings" / (pc["pid"] + ".png"), dpi=60)
    plt.close(fig)


def main():
    spec = json.loads((SCR / "pieces.json").read_text())
    only = sys.argv[1:]
    DDIR.mkdir(exist_ok=True)
    (SCR / "drawings").mkdir(exist_ok=True)
    done = []
    for pc in spec["pieces"]:
        if only and pc["pid"] not in only:
            continue
        sheet(pc, DDIR / (pc["pid"] + ".pdf"))
        done.append(pc["pid"])
        print("drew", pc["pid"], flush=True)
    if not only:
        import matplotlib.image as mpimg
        n = len(done)
        cols = 6
        rows = int(math.ceil(n / cols))
        fig, axs = plt.subplots(rows, cols, figsize=(cols * 3.0, rows * 2.15))
        for a in axs.ravel():
            a.axis("off")
        for a, pid in zip(axs.ravel(), done):
            a.imshow(mpimg.imread(SCR / "drawings" / (pid + ".png")))
            a.set_title(pid, fontsize=7)
        fig.tight_layout()
        fig.savefig(HERE / "img" / "drawings-contact.png", dpi=90)
        plt.close(fig)


if __name__ == "__main__":
    main()
