"""Axisymmetric FEA toolkit for the collection-cup studies: gmsh meshing, CalculiX decks, result readers.

Units: mm, s, tonne, N. So power is mW, energy mJ, k in mW/(mm K) (numerically the same as W/(m K)),
cp in mJ/(t K) (1 J/(kg K) = 1e6), density in t/mm3 (1 kg/m3 = 1e-12), film coefficient in mW/(mm2 K)
(1 W/(m2 K) = 1e-3), stress in MPa. Temperatures in deg C with ABSOLUTE ZERO = -273.15.

A model is a list of Region(name, material, polygon) in the (r, z) half-plane, r >= 0. The polygons are
fragmented with gmsh's OpenCASCADE kernel so that neighbouring regions share nodes (perfect contact);
put a thin "contact" region between two parts where the contact is imperfect. Quadratic 6-node
triangles (CAX6) are used throughout.
"""

import math
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SIGMA = 5.669e-11            # mW/(mm2 K4)
ABS0 = -273.15
J_PER_KGK = 1e6               # cp unit factor
KG_M3 = 1e-12                 # density unit factor
W_M2K = 1e-3                  # film coefficient factor


@dataclass
class Region:
    name: str
    material: str
    poly: list                 # [(r, z), ...] closed implicitly
    size: float = 1.5          # target element size (mm)
    init_T: float = None       # initial temperature (default: model ambient)


@dataclass
class Mesh:
    nodes: dict                # id -> (r, z)
    elems: dict                # id -> (n1..n6)
    elem_region: dict          # id -> region name
    regions: list
    edges: list = field(default_factory=list)   # boundary edges: dict(elem, face, n=(a,b,m), mid, normal, length)

    def elset(self, names):
        names = set([names] if isinstance(names, str) else names)
        return [e for e, r in self.elem_region.items() if r in names]

    def region_nodes(self, names):
        out = set()
        for e in self.elset(names):
            out.update(self.elems[e])
        return sorted(out)


def build_mesh(regions, scale_min=0.25, verbose=False, max_size=None, order=2):
    """Mesh the regions with gmsh (OCC fragment, order 2). Returns a Mesh."""
    import gmsh
    gmsh.initialize()
    gmsh.option.setNumber("General.Terminal", 1 if verbose else 0)
    gmsh.model.add("axi")
    occ = gmsh.model.occ
    surf_of = []
    for reg in regions:
        pts = [occ.addPoint(r, z, 0) for r, z in reg.poly]
        lines = [occ.addLine(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts))]
        loop = occ.addCurveLoop(lines)
        surf_of.append(occ.addPlaneSurface([loop]))
    owner = {}
    if len(surf_of) == 1:
        occ.synchronize()
        owner[surf_of[0]] = 0
    else:
        # object = first region, tools = the rest; omap lists the pieces of each input in that order
        out, omap = occ.fragment([(2, surf_of[0])], [(2, s) for s in surf_of[1:]])
        occ.synchronize()
        for i, pieces in enumerate(omap):
            for dim, tag in pieces:
                owner[tag] = i                # later regions win where inputs overlap
    # mesh size at the points of each piece
    for tag, i in owner.items():
        pts = gmsh.model.getBoundary([(2, tag)], recursive=True)
        gmsh.model.mesh.setSize(pts, regions[i].size)
    for tag, i in owner.items():
        pts = gmsh.model.getBoundary([(2, tag)], recursive=True)
        for p in pts:
            pass
    gmsh.option.setNumber("Mesh.MeshSizeMin", scale_min)
    if max_size:
        gmsh.option.setNumber("Mesh.MeshSizeMax", max_size)
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 1)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 1)
    gmsh.option.setNumber("Mesh.Algorithm", 6)
    gmsh.option.setNumber("Mesh.ElementOrder", order)
    gmsh.option.setNumber("Mesh.SecondOrderLinear", 1)
    gmsh.model.mesh.generate(2)
    ntags, coords, _ = gmsh.model.mesh.getNodes()
    nodes = {int(t): (float(coords[3 * k]), float(coords[3 * k + 1])) for k, t in enumerate(ntags)}
    elems, elem_region = {}, {}
    for tag, i in owner.items():
        types, etags, enodes = gmsh.model.mesh.getElements(2, tag)
        for ty, et, en in zip(types, etags, enodes):
            nn = {9: 6, 2: 3}.get(ty)
            if nn is None:
                raise RuntimeError(f"unexpected element type {ty}")
            en = np.asarray(en, dtype=int).reshape(-1, nn)
            for e, ns in zip(et, en):
                elems[int(e)] = tuple(int(n) for n in ns)
                elem_region[int(e)] = regions[i].name
    gmsh.finalize()
    # renumber nodes and elements compactly (only nodes used by elements)
    used = sorted({n for ns in elems.values() for n in ns})
    nmap = {n: k + 1 for k, n in enumerate(used)}
    nodes = {nmap[n]: nodes[n] for n in used}
    emap = {e: k + 1 for k, e in enumerate(sorted(elems))}
    elems2, reg2 = {}, {}
    for e, ns in elems.items():
        ns = [nmap[n] for n in ns]
        # counter-clockwise in the (r, z) plane
        (x1, y1), (x2, y2), (x3, y3) = (nodes[ns[0]], nodes[ns[1]], nodes[ns[2]])
        if (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1) < 0:
            ns = [ns[0], ns[2], ns[1], ns[5], ns[4], ns[3]] if len(ns) == 6 else [ns[0], ns[2], ns[1]]
        elems2[emap[e]] = tuple(ns)
        reg2[emap[e]] = elem_region[e]
    m = Mesh(nodes, elems2, reg2, regions)
    m.edges = boundary_edges(m)
    return m


FACE_NODES = {1: (0, 1, 3), 2: (1, 2, 4), 3: (2, 0, 5)}   # corner, corner, mid (CAX6 face numbering)
FACE_NODES_LIN = {1: (0, 1), 2: (1, 2), 3: (2, 0)}


def face_nodes(ns):
    return FACE_NODES if len(ns) == 6 else FACE_NODES_LIN


def boundary_edges(m, between_regions=False):
    """Edges used by one element (the model's boundary). Each: elem, face, nodes, midpoint, outward normal."""
    count = {}
    for e, ns in m.elems.items():
        for f, fn in face_nodes(ns).items():
            key = tuple(sorted((ns[fn[0]], ns[fn[1]])))
            count.setdefault(key, []).append((e, f))
    out = []
    for key, lst in count.items():
        if len(lst) != 1:
            continue
        e, f = lst[0]
        ns = m.elems[e]
        fn = face_nodes(ns)[f]
        a, b = fn[0], fn[1]
        p1, p2 = np.array(m.nodes[ns[a]]), np.array(m.nodes[ns[b]])
        mid = (p1 + p2) / 2
        t = p2 - p1
        L = float(np.hypot(*t))
        n = np.array([t[1], -t[0]]) / L          # right-hand normal; outward for a CCW element
        out.append(dict(elem=e, face=f, n=tuple(ns[i] for i in fn), mid=mid, normal=n, length=L,
                        region=m.elem_region[e]))
    return out


def interface_edges(m, reg_a, reg_b):
    """Edges shared by an element of region a and one of region b (returns the region-a side)."""
    count = {}
    for e, ns in m.elems.items():
        for f, fn in face_nodes(ns).items():
            key = tuple(sorted((ns[fn[0]], ns[fn[1]])))
            count.setdefault(key, []).append((e, f))
    out = []
    for key, lst in count.items():
        if len(lst) != 2:
            continue
        (e1, f1), (e2, f2) = lst
        r1, r2 = m.elem_region[e1], m.elem_region[e2]
        if (r1 == reg_a and r2 == reg_b) or (r2 == reg_a and r1 == reg_b):
            e, f = (e1, f1) if r1 == reg_a else (e2, f2)
            ns = m.elems[e]
            fn = face_nodes(ns)[f]
            p1, p2 = np.array(m.nodes[ns[fn[0]]]), np.array(m.nodes[ns[fn[1]]])
            out.append(dict(elem=e, face=f, n=tuple(ns[i] for i in fn), mid=(p1 + p2) / 2,
                            length=float(np.hypot(*(p2 - p1)))))
    return out


def ring_area(edge, nodes):
    """Area (mm2, full 360 deg) swept by an edge revolved about the axis."""
    (r1, z1), (r2, z2) = nodes[edge["n"][0]], nodes[edge["n"][1]]
    return math.pi * (r1 + r2) * math.hypot(r2 - r1, z2 - z1)


# ------------------------------------------------------------------------------------- deck writing
def write_mesh(f, m):
    f.write("*NODE, NSET=NALL\n")
    for n, (r, z) in m.nodes.items():
        f.write(f"{n}, {r:.6f}, {z:.6f}, 0.0\n")
    for reg in m.regions:
        els = m.elset(reg.name)
        if not els:
            continue
        et = "CAX6" if len(m.elems[els[0]]) == 6 else "CAX3"
        f.write(f"*ELEMENT, TYPE={et}, ELSET=E_{reg.name}\n")
        for e in els:
            f.write(f"{e}, " + ", ".join(str(n) for n in m.elems[e]) + "\n")


def write_set(f, kind, name, ids, per_line=12):
    f.write(f"*{kind}, {kind[0]}SET={name}\n" if kind in ("NSET", "ELSET") else "")
    ids = list(ids)
    for k in range(0, len(ids), per_line):
        f.write(", ".join(str(i) for i in ids[k:k + per_line]) + ",\n")


def run_ccx(job, cwd, threads=4, timeout=7200):
    env = dict(os.environ, OMP_NUM_THREADS=str(threads), CCX_NPROC_EQUATION_SOLVER=str(threads))
    r = subprocess.run(["ccx", "-i", job], cwd=cwd, capture_output=True, text=True, env=env, timeout=timeout)
    log = Path(cwd) / f"{job}.log"
    log.write_text(r.stdout + "\n" + r.stderr)
    if r.returncode != 0 or "*ERROR" in r.stdout:
        tail = "\n".join((r.stdout + r.stderr).splitlines()[-30:])
        raise RuntimeError(f"ccx failed for {job}:\n{tail}")
    return r.stdout


# --------------------------------------------------------------------------------------- readers
def read_dat_blocks(path):
    """Parse a CalculiX .dat file: {(quantity, set): [(time, {id: values...}), ...]}."""
    out = {}
    cur = None
    head = re.compile(r"^\s*(.+?)\s+(?:\(.*?\)\s+)?for set\s+(\S+)\s+and time\s+([-+0-9.Ee]+)")
    for line in Path(path).read_text().splitlines():
        h = head.match(line)
        if h:
            q, s, t = h.group(1).strip(), h.group(2).upper(), float(h.group(3))
            cur = {}
            out.setdefault((q, s), []).append((t, cur))
            continue
        if cur is None:
            continue
        parts = line.split()
        if not parts:
            continue
        try:
            vals = [float(p) for p in parts]
        except ValueError:
            cur = None
            continue
        if len(vals) >= 2:
            cur[int(vals[0])] = vals[1:]
    return out


def read_frd(path, quantity="NDTEMP"):
    """Nodal results from an ASCII .frd: list of (time, {node: [values]}) for one result block name."""
    out = []
    lines = Path(path).read_text(errors="ignore").splitlines()
    i = 0
    time = None
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("    1PSTEP"):
            pass
        if ln[:6].strip() == "100CL" or ln.startswith("  100CL"):
            try:
                time = float(ln[12:24])
            except ValueError:
                time = None
        if ln.startswith(" -4") and quantity in ln:
            i += 1
            while lines[i].startswith(" -5"):
                i += 1
            vals = {}
            while not lines[i].startswith(" -3"):
                s = lines[i]
                if s.startswith(" -1"):
                    node = int(s[3:13])
                    nums = [float(s[13 + 12 * k: 25 + 12 * k]) for k in range((len(s) - 13) // 12)]
                    vals[node] = nums
                i += 1
            out.append((time, vals))
        i += 1
    return out
