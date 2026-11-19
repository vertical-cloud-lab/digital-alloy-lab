"""One flange STL per parameter set, with the rectangle on top as wide as that set's spot.

Template: Gage's ``template/W011_348W_705_140um_h130.stl`` (PR 243, 2026-11-19), one
binary STL of 28 triangles that is already a single merged body:

- flange: x -0.705 to 0.565 mm (1.27 mm), y -12.7 to 0 mm (12.7 mm), z -5.08 to 0 mm (5.08 mm)
- rectangle on top: x -0.14 to 0 mm (0.14 mm, W011's 140 um spot), y -12.6 to 0 mm,
  z 0 to 0.05 mm, centred on the flange (x = -0.07 mm)

For every set in ``../out/wall_sets.csv`` this moves the rectangle's two long faces so that
it is the set's spot size wide and still centred on the flange. Nothing else changes: the
flange, the rectangle's height and length, the triangle order and the normals are the
template's, so each output is still one closed body, and W011's output is byte-identical
to the template.

    python make_fins.py           # writes stl/<set name>.stl, fins.csv and flange-fins-stl.zip

Standard library only. ``check_fins.py`` cross-checks every file with an independent boolean
union (manifold3d).
"""

import csv
import hashlib
import struct
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = HERE / "template" / "W011_348W_705_140um_h130.stl"
SETS = HERE.parent / "out" / "wall_sets.csv"
OUT = HERE / "stl"
ZIP = HERE / "flange-fins-stl.zip"
TABLE = HERE / "fins.csv"

SPOT_COL = "Adv. surface area: Spot size (µm)"
WALLS_COL = "Walls (square.part.wall)"
TOL = 1e-6  # mm; coordinates are float32 in the file


def f32(x):
    """Round a float to the nearest float32, as the STL stores it."""
    return struct.unpack("<f", struct.pack("<f", x))[0]


def read_stl(path):
    data = Path(path).read_bytes()
    if len(data) < 84:
        sys.exit(f"{path}: too short for a binary STL")
    n = struct.unpack("<I", data[80:84])[0]
    if len(data) != 84 + 50 * n:
        sys.exit(f"{path}: {len(data)} bytes, expected {84 + 50 * n} for {n} triangles")
    tris = []
    for i in range(n):
        vals = struct.unpack("<12fH", data[84 + 50 * i: 84 + 50 * (i + 1)])
        tris.append({"normal": vals[0:3], "v": [vals[3:6], vals[6:9], vals[9:12]], "attr": vals[12]})
    return data[:80], tris


def stl_bytes(header, tris):
    out = bytearray(header)
    out += struct.pack("<I", len(tris))
    for t in tris:
        out += struct.pack("<12fH", *t["normal"], *t["v"][0], *t["v"][1], *t["v"][2], t["attr"])
    return bytes(out)


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def template_geometry(tris):
    """Read the flange and rectangle limits off the template, and check they are what we expect."""
    xs = sorted({p[0] for t in tris for p in t["v"]})
    ys = sorted({p[1] for t in tris for p in t["v"]})
    zs = sorted({p[2] for t in tris for p in t["v"]})
    if len(xs) != 4 or len(ys) != 3 or len(zs) != 3:
        sys.exit(f"template has unexpected vertex coordinates: x {xs}, y {ys}, z {zs}")
    g = {
        "flange_x": (xs[0], xs[3]), "fin_x": (xs[1], xs[2]),
        "flange_y": (ys[0], ys[2]), "fin_y": (ys[1], ys[2]),
        "flange_z": (zs[0], zs[1]), "fin_z": (zs[1], zs[2]),
    }
    flange_c = (g["flange_x"][0] + g["flange_x"][1]) / 2
    fin_c = (g["fin_x"][0] + g["fin_x"][1]) / 2
    if abs(flange_c - fin_c) > TOL:
        sys.exit(f"template rectangle is not centred on the flange ({fin_c} vs {flange_c})")
    g["centre_x"] = round(flange_c, 6)
    return g


def check(tris, g, width):
    """Closed, consistently oriented, one body, right volume, right rectangle. Returns the volume."""
    assert len(tris) == 28, len(tris)
    key = lambda p: (round(p[0], 6), round(p[1], 6), round(p[2], 6))
    directed = {}
    verts = set()
    for i, t in enumerate(tris):
        a, b, c = (key(p) for p in t["v"])
        verts.update((a, b, c))
        n = cross(sub(t["v"][1], t["v"][0]), sub(t["v"][2], t["v"][0]))
        area2 = dot(n, n) ** 0.5
        assert area2 > 1e-9, f"triangle {i} is degenerate"
        assert dot(n, t["normal"]) / area2 > 0.999, f"triangle {i} is flipped against its normal"
        for e in ((a, b), (b, c), (c, a)):
            assert e not in directed, f"edge {e} used twice in the same direction"
            directed[e] = i
    # every edge has exactly one partner running the other way: closed and consistently wound
    for (a, b) in directed:
        assert (b, a) in directed, f"open edge {a} -> {b}"
    # one connected body
    parent = list(range(len(tris)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for (a, b), i in directed.items():
        parent[find(i)] = find(directed[(b, a)])
    assert len({find(i) for i in range(len(tris))}) == 1, "more than one body"
    n_edges = len(directed) // 2
    assert len(verts) - n_edges + len(tris) == 2, "Euler characteristic is not 2"
    # volume by the divergence theorem, against the two boxes
    vol = sum(dot(t["v"][0], cross(t["v"][1], t["v"][2])) for t in tris) / 6
    fx, fy, fz = g["flange_x"], g["flange_y"], g["flange_z"]
    ry, rz = g["fin_y"], g["fin_z"]
    expected = (fx[1] - fx[0]) * (fy[1] - fy[0]) * (fz[1] - fz[0]) + width * (ry[1] - ry[0]) * (rz[1] - rz[0])
    assert abs(vol - expected) < 1e-4, f"volume {vol} vs {expected}"
    # the rectangle as built: top face at the template's height, width and centre as asked
    top = [p for t in tris for p in t["v"] if abs(p[2] - rz[1]) < TOL]
    w = max(p[0] for p in top) - min(p[0] for p in top)
    c = (max(p[0] for p in top) + min(p[0] for p in top)) / 2
    assert abs(w - width) < 2e-6, f"rectangle is {w} wide, expected {width}"
    assert abs(c - g["centre_x"]) < 2e-6, f"rectangle centre {c}, expected {g['centre_x']}"
    return vol


def main():
    header, tmpl = read_stl(TEMPLATE)
    g = template_geometry(tmpl)
    lo0, hi0 = g["fin_x"]
    tmpl_width = round(hi0 - lo0, 6)
    with open(SETS, newline="", encoding="utf-8") as fh:
        sets = list(csv.DictReader(fh))
    OUT.mkdir(exist_ok=True)
    rows = []
    for s in sets:
        name = s["Set name"]
        spot_um = float(s[SPOT_COL])
        if float(s["Upside surface area: Spot size (µm)"]) != spot_um:
            sys.exit(f"{name}: the two tabs have different spots")
        width = spot_um / 1000.0
        lo = f32(round(g["centre_x"] - width / 2, 6))
        hi = f32(round(g["centre_x"] + width / 2, 6))
        if not (g["flange_x"][0] < lo < hi < g["flange_x"][1]):
            sys.exit(f"{name}: a {width} mm rectangle does not fit on the flange")
        tris = []
        for t in tmpl:
            v = []
            for p in t["v"]:
                x = p[0]
                if abs(x - lo0) < TOL:
                    x = lo
                elif abs(x - hi0) < TOL:
                    x = hi
                v.append((x, p[1], p[2]))
            tris.append({"normal": t["normal"], "v": v, "attr": t["attr"]})
        vol = check(tris, g, hi - lo)
        blob = stl_bytes(header, tris)
        path = OUT / f"{name}.stl"
        path.write_bytes(blob)
        rows.append({
            "set_name": name,
            "file": f"stl/{name}.stl",
            "spot_um": f"{spot_um:g}",
            "rectangle_width_mm": f"{width:.3f}",
            "rectangle_x_from_mm": f"{lo:.4f}",
            "rectangle_x_to_mm": f"{hi:.4f}",
            "rectangle_height_mm": f"{g['fin_z'][1] - g['fin_z'][0]:.3f}",
            "rectangle_length_mm": f"{g['fin_y'][1] - g['fin_y'][0]:.3f}",
            "flange_mm": "{:.3f} x {:.3f} x {:.3f}".format(
                g["flange_x"][1] - g["flange_x"][0], g["flange_y"][1] - g["flange_y"][0],
                g["flange_z"][1] - g["flange_z"][0]),
            "bodies": 1,
            "triangles": len(tris),
            "volume_mm3": f"{vol:.5f}",
            "walls": s[WALLS_COL],
            "sha256": hashlib.sha256(blob).hexdigest(),
        })
        if abs(width - tmpl_width) < TOL and blob != TEMPLATE.read_bytes():
            sys.exit(f"{name}: same width as the template but not byte-identical to it")
    with open(TABLE, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # one zip with every file, with fixed timestamps so reruns give the same zip
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for r in rows:
            info = zipfile.ZipInfo(f"flange-fins/{r['set_name']}.stl", date_time=(2026, 11, 19, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (OUT / f"{r['set_name']}.stl").read_bytes())
    same = [r["set_name"] for r in rows if abs(float(r["rectangle_width_mm"]) - tmpl_width) < TOL]
    print(f"{len(rows)} files in {OUT.relative_to(HERE)}/, all one closed body; "
          f"{', '.join(same)} byte-identical to the template")


if __name__ == "__main__":
    main()
