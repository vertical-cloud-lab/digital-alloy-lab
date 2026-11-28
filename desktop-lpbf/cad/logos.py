"""The BYU Vertical Cloud Lab lockup and BYU's block Y, cut as 0.5 mm debosses (issue #260; Sterling, 2026-11-20).

    logos.apply(parts, M)      # called once, at the end of lpbf_low.build()
    python desktop-lpbf/cad/logos.py check   # machinability against a 1/32 in. (0.8 mm) engraving end mill -> analysis/out/logos/

Sources (the vector paths are used as published: lines and cubic Beziers become exact OCC lines and Bezier edges, nothing redrawn):
- logos/vcl-lockup-one-line.svg: the lab's one-line lockup (mark + "VERTICAL CLOUD LAB"), VCL_Logo_FINAL_Outlines-23.svg from
  VCL_FINAL_LOGOS-20260518T210517Z-3-001.zip in github.com/vertical-cloud-lab/.github/tree/main/profile (zip sha256
  a67b026b592bae2cd19ad48aef91d5cfc8ec88df8f0406453486e8dc1af32772; the same drawing as vcl-lockup-one-line-outcrop.png there).
  Path commands used: M, l, h, v, c, s, Z (no arcs); the mark is six rectangles.
- logos/byu-block-y.svg: BYU's block Y, the navy polygon of the block-Y figure on BYU's brand guide (https://brand.byu.edu/logos-marks,
  image block-y-usage.svg, fetched 2026-11-23). The block-Y .zip on that page needs a BYU sign-in, so the figure's polygon is the
  official outline we could reach: 21 straight edges, translated to the origin only. BYU's brand guidelines govern its use: the shape
  must not be modified (texture, shading or dimension are allowed, so a deboss is fine), clear space is the width of the Y's top,
  minimum width 0.375 in., colours navy, white or royal. The TM is left off: at this size it would be 2.4 mm tall with 0.3 mm strokes,
  below the cutter.

Placement (model frame: mm, +y back, +z up; both debosses are on faces seen from the front, -y):
- VCL lockup, 180 mm wide (24.5 mm tall), centred on the chamber door's front face at x = 0, z = 60: above the hinge leaves (z <= 30
  at |x| 80..100), below the handle posts (z >= 90), inside the 6 mm corner radii; 0.5 mm deep in the 15 mm door, whose seal groove
  (1.32 mm deep) is on the back face, so 13.2 mm of plate stays between them.
- Block Y, 50 mm tall (40.7 mm wide), on the 4U control drawer's front panel (4 mm 6061), at its left end with the brand guide's clear
  space (one Y-top width, 40.7 mm) inside the 18 mm rack ears. The drawer is the one unit of the rack the lab builds itself, it sits at
  the top of the rack at eye level, and its left end lines up with where the vendor units above and below carry their own badges.
"""
from __future__ import annotations

import json
import math
import pathlib
import re
import sys

import cadquery as cq

HERE = pathlib.Path(__file__).resolve().parent
V = cq.Vector
SVG = {"vcl": HERE / "logos" / "vcl-lockup-one-line.svg", "y": HERE / "logos" / "byu-block-y.svg"}
DEPTH = 0.5          # deboss depth, mm
TOOL_D = 25.4 / 32   # 1/32 in. engraving end mill (0.79 mm)
PLACE = {
    "vcl": dict(part="Chamber door", width=180.0, centre=(0.0, 60.0), anchor="centre"),
    "y": dict(part="DIN-rail drawer", height=50.0, anchor="left", ear=18.0),
}
LAST = {}            # filled by apply(): {key: dict(part=name, face=cq.Face compound at the deboss floor, y_face=..., box=...)}


# --------------------------------------------------------------------------------------------
# SVG path data -> subpaths of exact segments (lines and cubic Beziers)
# --------------------------------------------------------------------------------------------
def _tokens(d):
    for m in re.finditer(r"[MmLlHhVvCcSsQqTtZzAa]|[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", d):
        yield m.group(0)


def parse_path(d):
    """SVG path string -> list of closed subpaths; each is a list of segments ("L", p0, p1) or ("C", p0, c1, c2, p1)."""
    toks = list(_tokens(d))
    i, cmd = 0, None
    cur = start = (0.0, 0.0)
    last_c = None
    subs, seg = [], []

    def num():
        nonlocal i
        v = float(toks[i])
        i += 1
        return v

    def close():
        nonlocal seg, cur
        if seg:
            if math.dist(cur, start) > 1e-9:
                seg.append(("L", cur, start))
            subs.append(seg)
        seg, cur = [], start

    while i < len(toks):
        if re.match(r"[A-Za-z]", toks[i]):
            cmd = toks[i]
            i += 1
            if cmd in "Zz":
                close()
                last_c = None
                continue
            if cmd in "Aa":
                raise ValueError("arcs are not used by these logos")
        rel = cmd.islower()
        c = cmd.upper()
        ox, oy = cur if rel else (0.0, 0.0)
        if c == "M":
            if seg:
                close()
            cur = start = (ox + num(), oy + num())
            cmd = "l" if rel else "L"           # further pairs are implicit line-tos
            last_c = None
        elif c in "LHV":
            if c == "L":
                p = (ox + num(), oy + num())
            elif c == "H":
                p = ((cur[0] if rel else 0.0) + num(), cur[1])
            else:
                p = (cur[0], (cur[1] if rel else 0.0) + num())
            if math.dist(cur, p) > 1e-9:
                seg.append(("L", cur, p))
            cur, last_c = p, None
        elif c in "CS":
            if c == "C":
                c1 = (ox + num(), oy + num())
            else:
                c1 = (2 * cur[0] - last_c[0], 2 * cur[1] - last_c[1]) if last_c else cur
            c2 = (ox + num(), oy + num())
            p = (ox + num(), oy + num())
            seg.append(("C", cur, c1, c2, p))
            cur, last_c = p, c2
        elif c in "QT":                          # quadratic -> exact cubic
            if c == "Q":
                q = (ox + num(), oy + num())
            else:
                q = (2 * cur[0] - last_c[0], 2 * cur[1] - last_c[1]) if last_c else cur
            p = (ox + num(), oy + num())
            c1 = (cur[0] + 2 / 3 * (q[0] - cur[0]), cur[1] + 2 / 3 * (q[1] - cur[1]))
            c2 = (p[0] + 2 / 3 * (q[0] - p[0]), p[1] + 2 / 3 * (q[1] - p[1]))
            seg.append(("C", cur, c1, c2, p))
            cur, last_c = p, q
        else:
            raise ValueError(f"unsupported path command {cmd}")
    if seg:
        close()
    return subs


def load_svg(path):
    """All filled shapes of an SVG (path, rect, polygon) as closed subpaths in SVG units (y down), plus the viewBox."""
    t = pathlib.Path(path).read_text()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', t).group(1).split()]
    subs = []
    for m in re.finditer(r"<rect\b([^>]*)/?>", t):
        a = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        x, y, w, h = (float(a.get(k, 0.0)) for k in ("x", "y", "width", "height"))
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        subs.append([("L", pts[k], pts[(k + 1) % 4]) for k in range(4)])
    for m in re.finditer(r'<polygon\b[^>]*points="([^"]+)"', t):
        v = [float(s) for s in re.split(r"[\s,]+", m.group(1).strip())]
        pts = list(zip(v[0::2], v[1::2]))
        if math.dist(pts[0], pts[-1]) < 1e-9:
            pts = pts[:-1]
        subs.append([("L", pts[k], pts[(k + 1) % len(pts)]) for k in range(len(pts))])
    for m in re.finditer(r'<path\b[^>]*\sd="([^"]+)"', t):
        subs += parse_path(m.group(1))
    return subs, vb


def _sample(sub, n=12):
    pts = []
    for s in sub:
        if s[0] == "L":
            pts.append(s[1])
        else:
            p0, c1, c2, p1 = s[1:]
            for k in range(n):
                t = k / n
                a, b, c, d = (1 - t) ** 3, 3 * t * (1 - t) ** 2, 3 * t * t * (1 - t), t ** 3
                pts.append((a * p0[0] + b * c1[0] + c * c2[0] + d * p1[0], a * p0[1] + b * c1[1] + c * c2[1] + d * p1[1]))
    return pts


def _inside(pt, poly):
    x, y = pt
    c = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            c = not c
    return c


def _area(poly):
    return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))


def nest(subs):
    """Even-odd nesting: [(outer_index, [hole indices])]. A subpath's depth = how many others contain it."""
    polys = [_sample(s) for s in subs]
    areas = [abs(_area(p)) for p in polys]
    depth, parent = [], []
    for i, p in enumerate(polys):
        cont = [j for j, q in enumerate(polys) if j != i and areas[j] > areas[i] and _inside(p[0], q)]
        depth.append(len(cont))
        parent.append(min(cont, key=lambda j: areas[j]) if cont else None)
    out = []
    for i in range(len(subs)):
        if depth[i] % 2 == 0:
            out.append((i, [j for j in range(len(subs)) if parent[j] == i and depth[j] == depth[i] + 1]))
    return out, polys


# --------------------------------------------------------------------------------------------
# Faces in a plane facing -y (the viewer's right = +x, up = +z), extruded into the part along +y
# --------------------------------------------------------------------------------------------
def logo_faces(key, size, centre_xz=(0.0, 0.0), y=0.0):
    """Planar faces of the logo in the plane y = const, scaled so its width (vcl) or height (y) = size, centred on centre_xz.
    Returns (list of cq.Face, (w, h) in mm, scale)."""
    subs, vb = load_svg(SVG[key])
    allp = [p for s in subs for p in _sample(s)]
    x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
    y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)
    s = size / (x1 - x0) if key == "vcl" else size / (y1 - y0)
    cxs, cys = (x0 + x1) / 2, (y0 + y1) / 2

    def P(p):
        return V(centre_xz[0] + (p[0] - cxs) * s, y, centre_xz[1] - (p[1] - cys) * s)

    def wire(sub):
        edges = []
        for g in sub:
            if g[0] == "L":
                edges.append(cq.Edge.makeLine(P(g[1]), P(g[2])))
            else:
                edges.append(cq.Edge.makeBezier([P(q) for q in g[1:]]))
        return cq.Wire.assembleEdges(edges)

    groups, _ = nest(subs)
    faces = [cq.Face.makeFromWires(wire(subs[o]), [wire(subs[h]) for h in hs]) for o, hs in groups]
    return faces, ((x1 - x0) * s, (y1 - y0) * s), s


def deboss_tool(faces, depth=DEPTH):
    """Solids from the faces (at the part's face plane) 0.01 mm outside it to `depth` into it (+y)."""
    sols = [cq.Solid.extrudeLinear(f.translate(V(0, -0.01, 0)), V(0, depth + 0.01, 0)) for f in faces]
    return cq.Compound.makeCompound(sols)


def _find(parts, prefix):
    hits = [p for p in parts if p.name.startswith(prefix)]
    if len(hits) != 1:
        raise LookupError(f"logos: expected one part named '{prefix}...', found {len(hits)}")
    return hits[0]


def placements(parts):
    """Where each logo goes, read off the current parts: {key: (part, size, centre_xz, y_face)}. A target part that is
    missing or ambiguous (renamed by another change) is skipped with a warning, so build() never fails on a logo."""
    out = {}
    try:
        door = _find(parts, PLACE["vcl"]["part"])
        b = door.shape.BoundingBox()
        out["vcl"] = (door, PLACE["vcl"]["width"], PLACE["vcl"]["centre"], b.ymin)
    except LookupError as e:
        print(f"WARNING {e}: VCL lockup not cut", file=sys.stderr)
    try:
        dr = _find(parts, PLACE["y"]["part"])
        b = dr.shape.BoundingBox()
        h = PLACE["y"]["height"]
        w = h * 80.2695 / 98.6168                 # the block Y's width/height (logos/byu-block-y.svg)
        xc = b.xmin + PLACE["y"]["ear"] + w + w / 2   # clear space = one Y-top width inside the rack ear
        out["y"] = (dr, h, (xc, (b.zmin + b.zmax) / 2), b.ymin)
    except LookupError as e:
        print(f"WARNING {e}: block Y not cut", file=sys.stderr)
    return out


def apply(parts, M=None):
    """Cut both debosses into their parts (in place). Called by ONE line at the end of lpbf_low.build()."""
    LAST.clear()
    for key, (part, size, cxz, yf) in placements(parts).items():
        faces, (w, h), s = logo_faces(key, size, cxz, yf)
        part.shape = part.shape.cut(deboss_tool(faces))
        LAST[key] = dict(part=part.name, faces=[f.translate(V(0, DEPTH, 0)) for f in faces], y_face=yf, size_mm=(round(w, 2), round(h, 2)),
                         centre_xz=tuple(round(c, 2) for c in cxz), scale=s)
    return parts


# --------------------------------------------------------------------------------------------
# Machinability: what a 0.8 mm end mill cannot reach (raster morphology at 0.01 mm/px)
# --------------------------------------------------------------------------------------------
def check(px=0.01, tool_d=TOOL_D):
    import cv2
    import numpy as np
    out_dir = HERE.parent / "analysis" / "out" / "logos"
    out_dir.mkdir(parents=True, exist_ok=True)
    res = {}
    for key, size in (("vcl", PLACE["vcl"]["width"]), ("y", PLACE["y"]["height"])):
        subs, _ = load_svg(SVG[key])
        allp = [p for s in subs for p in _sample(s, 48)]
        x0, x1 = min(p[0] for p in allp), max(p[0] for p in allp)
        y0, y1 = min(p[1] for p in allp), max(p[1] for p in allp)
        s = size / (x1 - x0) if key == "vcl" else size / (y1 - y0)
        pad = 1.0
        W, H = int(((x1 - x0) * s + 2 * pad) / px), int(((y1 - y0) * s + 2 * pad) / px)
        polys = [np.array([[((p[0] - x0) * s + pad) / px, ((p[1] - y0) * s + pad) / px] for p in _sample(sub, 48)], np.int32) for sub in subs]
        img = np.zeros((H, W), np.uint8)
        for poly in polys:                      # XOR fill = even-odd
            m = np.zeros_like(img)
            cv2.fillPoly(m, [poly], 255)
            img ^= m
        r = int(round(tool_d / 2 / px))
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
        opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, k)
        miss = (img > 0) & (opened == 0)
        dt = cv2.distanceTransform((opened == 0).astype(np.uint8), cv2.DIST_L2, 5) * px     # distance of each pixel to the reachable area
        n0, _ = cv2.connectedComponents(img)
        n1, _ = cv2.connectedComponents(opened)
        # narrowest stroke: the smallest cutter diameter that clears less than half of some glyph (component-wise opening)
        ncomp, lab = cv2.connectedComponents(img)
        comp_area = np.bincount(lab.ravel(), minlength=ncomp)
        stroke = None
        for dd in (0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 3.0):
            rr = max(1, int(round(dd / 2 / px)))
            kk = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * rr + 1, 2 * rr + 1))
            op = cv2.morphologyEx(img, cv2.MORPH_OPEN, kk)
            kept = np.bincount(lab[op > 0].ravel(), minlength=ncomp)
            frac = kept[1:] / np.maximum(comp_area[1:], 1)
            if frac.min() < 0.5:
                stroke = dd
                break
        res[key] = dict(size_mm=[round((x1 - x0) * s, 2), round((y1 - y0) * s, 2)], scale_mm_per_unit=round(s, 5),
                        tool_d_mm=round(tool_d, 3), area_mm2=round(float((img > 0).sum()) * px * px, 1),
                        unreachable_mm2=round(float(miss.sum()) * px * px, 3), unreachable_pct=round(100.0 * miss.sum() / max((img > 0).sum(), 1), 2),
                        max_deviation_mm=round(float(dt[miss].max()) if miss.any() else 0.0, 3),
                        components_before=int(n0 - 1), components_after_tool=int(n1 - 1),
                        cutter_d_that_loses_half_a_glyph_mm=stroke)
        vis = np.dstack([img // 3] * 3)
        vis[opened > 0] = (200, 200, 200)
        vis[miss] = (0, 0, 255)
        sm = cv2.resize(vis, (min(W, 2400), int(H * min(W, 2400) / W)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(str(out_dir / f"tool_reach_{key}.png"), sm)
        print(key, json.dumps(res[key]))
    (out_dir / "machinability.json").write_text(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check()
    else:
        for k in SVG:
            subs, vb = load_svg(SVG[k])
            g, _ = nest(subs)
            print(k, len(subs), "subpaths,", len(g), "faces, viewBox", vb)
