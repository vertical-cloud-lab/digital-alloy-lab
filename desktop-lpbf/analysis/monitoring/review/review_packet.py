"""The review packet for the monitoring hardware: what BYU's Laser Safety Officer and the machine shop are asked to look at
(issue #260, PR 281; desktop-lpbf/monitoring/review-packet.md).

Builds lpbf_low twice, without and with the monitoring parts (cad/monitoring_parts.py), on one module, then:
  1. picks every part monitoring adds that is made, not bought: a BOM line whose group is "custom" in monitoring-bom.csv,
     or a metal, G-10 or plastic part whose name says it is made (a bracket, clamp, boss, wedge, clip, duct, hood, break...);
  2. picks every existing part monitoring changes (a port, bore, groove, cut-out or trim): its volume differs from the
     default model's part of the same name;
  3. writes each as STEP (analysis/out/monitoring/review/step/<slug>.step), the material monitoring removes from a changed
     part as its own STEP (<slug>-removed.step), a PNG of each (made parts on their own; changed parts grey with the
     removed material red, the whole part and a close-up of each place it changes), and review_packet.json with the name,
     BOM line, material, size, volume and mass, and where the features are.

Run (about 3-6 min, 3 GB):
  /tmp/heavy 3 env OMP_NUM_THREADS=1 xvfb-run -a -s "-screen 0 1920x1080x24" \
      /tmp/venv/bin/python desktop-lpbf/analysis/monitoring/review/review_packet.py [--module M50] [--no-png]
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import re
import sys
import time

import numpy as np

D = pathlib.Path(__file__).resolve().parents[3]          # desktop-lpbf/
sys.path.insert(0, str(D / "cad"))
OUT = D / "analysis" / "out" / "monitoring" / "review"
STEP = OUT / "step"
PNG = OUT / "png"

DENSITY = {"al6061": 2.70, "al5083": 2.66, "al7075": 2.81, "ss316l": 8.0, "ss304": 8.0, "g10": 1.85, "petg": 1.27, "pla": 1.24,
           "abs": 1.05, "fused_silica": 2.20, "fkm": 1.85, "steel": 7.85, "brass": 8.5, "copper": 8.96, "ptfe": 2.2, "peek": 1.32}
MADE_MATS = {"al6061", "al5083", "al7075", "ss316l", "ss304", "g10", "petg", "pla", "abs", "steel", "brass", "copper", "ptfe", "peek"}
MADE_WORDS = re.compile(r"\b(bracket|clamp|boss|wedge|clip|duct|hood|thermal break|break plate|baffle|light trap|shroud|"
                        r"adapter plate|spring seat|seat|guide|bush|sleeve|plug|cap|waveguide|purge tube|standoff|spacer|cover|"
                        r"plenum|manifold|mount|holder|block|ring)\b", re.I)
BOUGHT_WORDS = re.compile(r"\b(Thorlabs|Edmund|Kowa|Chronos|PicoScope|PDA36A2|MISTRAS|Vallen|retaining ring|SM1-class|"
                          r"envelope\b|fitting|needle valve|O-ring|gasket|window|slide|filter|lens|camera\b|sensor\b|LED\b|fan\b)", re.I)


def slug(s, n=60):
    s = re.sub(r"\(.*", "", s).strip()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:n]


def base_name(n):
    """a part's name without its parenthetical, which monitoring_parts sometimes rewrites"""
    return re.split(r"\s*\(", n, maxsplit=1)[0].strip()


def bom_groups():
    p = D / "monitoring-bom.csv"
    return {r["id"]: r for r in csv.DictReader(open(p))} if p.exists() else {}


def kind(p, bom):
    """"made", "bought, modified" (a bought part the shop works on), or None (bought as is, or not monitoring's)"""
    if "monitoring" not in p.tags:
        return None
    row = bom.get(p.bom)
    if row and "custom" in row.get("group", ""):
        return "made"
    if re.search(r"bored through|cut to length|bent\b|tip flattened", p.name, re.I):
        return "bought, modified"
    if re.match(r"G-10 thermal break", p.name):          # cut or turned from G-10 sheet and rod; the model calls it "misc"
        return "made"
    if p.mat not in MADE_MATS:
        return None
    b = base_name(p.name)
    if BOUGHT_WORDS.search(b) and not re.search(r"\b(bracket|clamp|wedge|clip|duct|hood|break|baffle|boss)\b", b, re.I):
        return None
    return "made" if MADE_WORDS.search(b) else None


def bbox(shape):
    b = shape.BoundingBox()
    return dict(min=[round(b.xmin, 1), round(b.ymin, 1), round(b.zmin, 1)], max=[round(b.xmax, 1), round(b.ymax, 1), round(b.zmax, 1)],
                size=[round(b.xlen, 1), round(b.ylen, 1), round(b.zlen, 1)])


def clusters(solids, gap=25.0):
    """group the removed solids that sit within `gap` mm of each other (one close-up per place a part changes)"""
    boxes = [s.BoundingBox() for s in solids]
    n = len(solids)
    lab = list(range(n))

    def find(i):
        while lab[i] != i:
            lab[i] = lab[lab[i]]
            i = lab[i]
        return i
    for i in range(n):
        for j in range(i + 1, n):
            a, b = boxes[i], boxes[j]
            if (a.xmin - gap <= b.xmax and b.xmin - gap <= a.xmax and a.ymin - gap <= b.ymax and b.ymin - gap <= a.ymax
                    and a.zmin - gap <= b.zmax and b.zmin - gap <= a.zmax):
                lab[find(i)] = find(j)
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return [[solids[i] for i in g] for g in groups.values()]


def render(items, path, focus=None, title=None):
    """items: [(shape, rgb, opacity)]; focus: a bounding box to frame (else the whole of items)"""
    import pyvista as pv
    pv.OFF_SCREEN = True
    pl = pv.Plotter(off_screen=True, window_size=(900, 700), lighting="three lights")
    pl.set_background("#f7f9fb", top="#dfe6ee")
    for shape, rgb, op in items:
        vs, ts = shape.tessellate(0.05 if focus is not None else 0.15, 0.2)
        if not ts:
            continue
        pts = np.array([(v.x, v.y, v.z) for v in vs], float)
        faces = np.hstack([np.full((len(ts), 1), 3), np.array(ts)]).ravel()
        m = pv.PolyData(pts, faces).compute_normals(split_vertices=True, feature_angle=35)
        pl.add_mesh(m, color=rgb, opacity=op, smooth_shading=True, specular=0.15, ambient=0.3, diffuse=0.8)
        pl.add_mesh(m.extract_feature_edges(feature_angle=35, boundary_edges=True, non_manifold_edges=False, manifold_edges=False),
                    color="#333333", line_width=1)
    if focus is not None:
        lo, hi = np.array(focus[0], float), np.array(focus[1], float)
        c, r = (lo + hi) / 2, max(np.linalg.norm(hi - lo) / 2, 8.0)
        d = np.array([1.0, -1.3, 0.9]) / np.linalg.norm([1.0, -1.3, 0.9])
        pl.camera.focal_point = c
        pl.camera.position = c + d * r * 4.2
        pl.camera.up = (0, 0, 1)
    else:
        pl.view_isometric()
        pl.reset_camera()
        pl.camera.zoom(0.9)                 # 1.15 cropped long thin parts (the AE cartridge and waveguide)
    pl.add_axes(line_width=2, labels_off=False)
    img = pl.screenshot(return_img=True)
    pl.close()
    from PIL import Image
    Image.fromarray(img).quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(str(path), optimize=True)


def tables(res):
    """the two tables review-packet.md shows: made parts, and existing parts monitoring changes"""
    L = [f"# Monitoring review packet: parts ({res['module']}; written by review_packet.py)", "",
         "STEP files are in millimetres, in the machine's coordinates. Views: grey is the part, red what monitoring removes.", "",
         "## Made, or bought and worked on", "",
         "| Part | BOM | Kind | Material | Size x × y × z (mm) | Mass (g) | STEP | View |", "|---|---|---|---|---|---:|---|---|"]
    for m in res["made"]:
        sz = " × ".join(f"{v:g}" for v in m["bbox"]["size"])
        L.append(f"| {m['name']} | {m['bom']} | {m['kind']} | {m['mat']} | {sz} | {m['mass_g'] if m['mass_g'] is not None else '–'} | "
                 f"[STEP]({m['step']}) | [PNG]({m['png']}) |")
    L += ["", "## Existing parts that monitoring changes", "",
          "| Part | BOM | Material | Removed (cm³) | Places | STEP as changed | Removed material | Views |", "|---|---|---|---:|---:|---|---|---|"]
    for c in res["changed"]:
        views = " ".join(f"[{i + 1}]({pl['png']})" for i, pl in enumerate(c["places"]))
        rs = f"[STEP]({c['removed_step']})" if c.get("removed_step") else "–"
        L.append(f"| {c['name']} | {c['bom']} | {c['mat']} | {c['removed_cm3']:g} | {len(c['places'])} | [STEP]({c['step']}) | {rs} | "
                 f"[whole]({c['png']}) {views} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--module", default="M50")
    ap.add_argument("--no-png", action="store_true")
    a = ap.parse_args()
    import cadquery as cq  # noqa: F401
    import lpbf_low as M
    t0 = time.time()
    kw = {}
    try:
        import inspect
        if "module" in inspect.signature(M.build).parameters:
            kw["module"] = a.module
    except (TypeError, ValueError):
        pass
    base = M.build(monitoring=False, **kw)
    mon = M.build(monitoring=True, **kw)
    t_build = time.time() - t0
    bom = bom_groups()
    for d in (STEP, PNG):
        d.mkdir(parents=True, exist_ok=True)
        for f in d.iterdir():
            f.unlink()

    by_name = {}
    for p in base:
        by_name.setdefault(p.name, []).append(p)
    by_base = {}
    for p in base:
        by_base.setdefault(base_name(p.name), []).append(p)

    made, changed, seen = [], [], set()
    for p in mon:
        kd = kind(p, bom)
        if kd:
            s = slug(p.name)
            k, i = s, 2
            while k in seen:
                k, i = f"{s}-{i}", i + 1
            seen.add(k)
            p.shape.exportStep(str(STEP / f"{k}.step"))
            v = p.shape.Volume() / 1000.0
            rho = DENSITY.get(p.mat) or (DENSITY["g10"] if p.name.startswith("G-10") else None)
            made.append(dict(slug=k, kind=kd, name=p.name, bom=p.bom, bom_group=bom.get(p.bom, {}).get("group", ""),
                             bom_action=bom.get(p.bom, {}).get("action", ""), mat=p.mat, module=p.module, motion_group=p.group,
                             bbox=bbox(p.shape), volume_cm3=round(v, 2), mass_g=round(v * rho, 1) if rho else None,
                             step=f"step/{k}.step", png=f"png/{k}.png"))
            if not a.no_png:
                render([(p.shape, "#9fb3c8", 1.0)], PNG / f"{k}.png")
            continue
        if "monitoring" in p.tags:
            continue
        cands = by_name.get(p.name) or by_base.get(base_name(p.name)) or []
        if len(cands) != 1:
            continue
        q = cands[0]
        v0, v1 = q.shape.Volume(), p.shape.Volume()
        if abs(v0 - v1) < 0.5:
            continue
        s = slug(p.name)
        k, i = s, 2
        while k in seen:
            k, i = f"{s}-{i}", i + 1
        seen.add(k)
        removed = q.shape.cut(p.shape)
        sol = [x for x in removed.Solids() if x.Volume() > 0.05]
        added = [x for x in p.shape.cut(q.shape).Solids() if x.Volume() > 0.05]
        if not sol and not added:                  # volumes differ only in how OCC sums an overlapping compound
            continue
        p.shape.exportStep(str(STEP / f"{k}.step"))
        if sol:
            cq.Compound.makeCompound(sol).exportStep(str(STEP / f"{k}-removed.step"))
        places = []
        for j, g in enumerate(clusters(sol)):
            comp = cq.Compound.makeCompound(g)
            bb = bbox(comp)
            places.append(dict(bbox=bb, removed_cm3=round(sum(x.Volume() for x in g) / 1000.0, 3), solids=len(g),
                               png=f"png/{k}-{j + 1}.png"))
            if not a.no_png:
                lo, hi = np.array(bb["min"]) - 6, np.array(bb["max"]) + 6
                render([(p.shape, "#c8ced6", 0.55), (comp, "#d62728", 1.0)], PNG / f"{k}-{j + 1}.png", focus=(lo, hi))
        if not a.no_png:
            render([(p.shape, "#c8ced6", 0.6)] + ([(cq.Compound.makeCompound(sol), "#d62728", 1.0)] if sol else []), PNG / f"{k}.png")
        rho = DENSITY.get(p.mat)
        changed.append(dict(slug=k, name=p.name, default_name=q.name, bom=p.bom or q.bom, mat=p.mat, module=p.module,
                            motion_group=p.group, bbox=bbox(p.shape), volume_default_cm3=round(v0 / 1000.0, 2),
                            volume_cm3=round(v1 / 1000.0, 2), removed_cm3=round(sum(x.Volume() for x in sol) / 1000.0, 3),
                            added_cm3=round(sum(x.Volume() for x in added) / 1000.0, 3),
                            mass_change_g=round((v1 - v0) / 1000.0 * rho, 1) if rho else None, places=places,
                            step=f"step/{k}.step", removed_step=f"step/{k}-removed.step" if sol else None, png=f"png/{k}.png"))
    res = dict(module=a.module, built_s=round(t_build, 1), run_s=round(time.time() - t0, 1),
               parts_default=len(base), parts_monitoring=len(mon), made=made, changed=changed,
               note="STEP in mm, machine coordinates (the model's); bought parts are envelopes and are not in the packet")
    (OUT / "review_packet.json").write_text(json.dumps(res, indent=1))
    (OUT / "parts.md").write_text(tables(res))
    print(f"{len(made)} made parts, {len(changed)} changed parts in {res['run_s']} s")
    for m in made:
        print(f"  {m['kind'][:8]:8s} {m['bom']:7s} {m['mat']:8s} {m['bbox']['size']} {m['name'][:80]}")
    for c in changed:
        print(f"  changed {c['bom']:7s} {c['mat']:8s} -{c['removed_cm3']} +{c['added_cm3']} cm3 in {len(c['places'])} place(s): {c['name'][:70]}")


if __name__ == "__main__":
    main()
