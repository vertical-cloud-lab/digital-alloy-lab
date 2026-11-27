"""One flange STL per parameter set: a 1.25 x 12.6 x 2.00 mm flange with a line on top as wide as that set's spot.

History (both on PR 243):

- 2026-11-19, Gage: template ``template/W011_348W_705_140um_h130.stl``, one binary STL of 28 triangles,
  already a single merged body: a 1.27 x 12.7 x 5.08 mm flange (x -0.705 to 0.565, y -12.7 to 0,
  z -5.08 to 0) with a 0.14 x 12.6 x 0.05 mm rectangle on top (x -0.14 to 0, y -12.6 to 0, z 0 to 0.05),
  centred on the flange at x = -0.07 mm and flush with its y = 0 end. The first version of these files
  (e50d71d) was that file with only the rectangle's width changed.
- 2026-11-20, Carl: the flange was too tall. Each file is now a flange 2 mm tall, 1.25 mm wide and
  12.6 mm deep, with the line on top.

Every file is one closed body of 28 triangles, in mm, in the template's frame:

- flange: x -0.695 to 0.555 (1.25 mm), y -12.6 to 0 (12.6 mm), z -2.0 to 0 (2.0 mm)
- line on top: x -0.07 -/+ spot/2, y -12.6 to 0 (the flange's whole length), z 0 to 0.05 mm

From the template: the frame (the flange's top face at z = 0, the y = 0 end, the centre at x = -0.07 mm)
and the line's 0.05 mm height. From Carl's request: the flange's three sizes. The line now runs end to
end, as Gage first described it, because the new flange is as deep as the template's rectangle was long.

So the part is a prism: its end view (an 8-sided outline, the flange with the line standing on it) is
extruded 12.6 mm along y. Each end face is six triangles and each of the eight long faces two.

    python make_fins.py           # writes stl/<set name>.stl, fins.csv and flange-fins-2mm-stl.zip

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
ZIP_NAME = "flange-fins-2mm"  # the zip and the folder inside it; "2mm" tells it apart from the 5.08 mm version
ZIP = HERE / f"{ZIP_NAME}-stl.zip"
TABLE = HERE / "fins.csv"

# Carl, PR 243, 2026-11-20: "2mm tall, 1.25 mm wide, and 12.6 mm deep with the line on top"
FLANGE_WIDTH = 1.25   # mm, x
FLANGE_DEPTH = 12.6   # mm, y; the line runs all of it
FLANGE_HEIGHT = 2.0   # mm, z; the line stands on top of this

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


def new_geometry(t):
    """The 2026-11-20 flange in the template's frame: same top face, same y = 0 end, same centre."""
    cx = t["centre_x"]
    top = round(t["flange_z"][1], 6)
    end = round(t["fin_y"][1], 6)
    line_h = round(t["fin_z"][1] - t["fin_z"][0], 6)
    y = (f32(round(end - FLANGE_DEPTH, 6)), f32(end))
    return {
        "flange_x": (f32(round(cx - FLANGE_WIDTH / 2, 6)), f32(round(cx + FLANGE_WIDTH / 2, 6))),
        "flange_y": y,
        "flange_z": (f32(round(top - FLANGE_HEIGHT, 6)), f32(top)),
        "fin_y": y,  # end to end
        "fin_z": (f32(top), f32(round(top + line_h, 6))),
        "centre_x": cx,
    }


def unit_normal(v):
    n = cross(sub(v[1], v[0]), sub(v[2], v[0]))
    m = dot(n, n) ** 0.5
    return tuple(c / m + 0.0 for c in n)  # + 0.0 turns -0.0 into 0.0


def prism(g, lo, hi):
    """The flange with the line on top: an 8-sided end view extruded along y, wound so normals point out."""
    x0, x1 = g["flange_x"]
    y0, y1 = g["flange_y"]
    z0, z1 = g["flange_z"]
    z2 = g["fin_z"][1]
    # end view, counter-clockwise with x to the right and z up (as seen from -y)
    poly = [(x0, z0), (x1, z0), (x1, z1), (hi, z1), (hi, z2), (lo, z2), (lo, z1), (x0, z1)]
    # the flange's end as a fan from its bottom-left corner over every point on its top edge, then the line's end;
    # no point sits on another triangle's edge, so every edge is shared by exactly two triangles
    cap = [(0, 1, 2), (0, 2, 3), (0, 3, 6), (0, 6, 7), (3, 4, 5), (3, 5, 6)]

    def p(i, y):
        return (poly[i][0], y, poly[i][1])

    faces = []
    faces += [(p(a, y0), p(b, y0), p(c, y0)) for a, b, c in cap]  # y0 end, normal -y
    faces += [(p(a, y1), p(c, y1), p(b, y1)) for a, b, c in cap]  # y1 end, normal +y
    for i in range(len(poly)):  # the eight long faces
        j = (i + 1) % len(poly)
        faces.append((p(i, y0), p(i, y1), p(j, y1)))
        faces.append((p(i, y0), p(j, y1), p(j, y0)))
    return [{"normal": unit_normal(v), "v": list(v), "attr": 0} for v in faces]


def check(tris, g, width):
    """Closed, consistently oriented, one body, right size and volume, right line. Returns the volume."""
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
    # overall size: the flange's width and depth, and its height plus the line's
    fx, fy, fz = g["flange_x"], g["flange_y"], g["flange_z"]
    ry, rz = g["fin_y"], g["fin_z"]
    pts = [p for t in tris for p in t["v"]]
    for k, want in ((0, fx), (1, fy), (2, (fz[0], rz[1]))):
        got = (min(p[k] for p in pts), max(p[k] for p in pts))
        assert abs(got[0] - want[0]) < TOL and abs(got[1] - want[1]) < TOL, f"axis {k}: {got} vs {want}"
    assert abs((fx[1] - fx[0]) - FLANGE_WIDTH) < 2e-6, "flange width"
    assert abs((fy[1] - fy[0]) - FLANGE_DEPTH) < 2e-6, "flange depth"
    assert abs((fz[1] - fz[0]) - FLANGE_HEIGHT) < 2e-6, "flange height"
    # volume by the divergence theorem, against the two boxes
    vol = sum(dot(t["v"][0], cross(t["v"][1], t["v"][2])) for t in tris) / 6
    expected = (fx[1] - fx[0]) * (fy[1] - fy[0]) * (fz[1] - fz[0]) + width * (ry[1] - ry[0]) * (rz[1] - rz[0])
    assert abs(vol - expected) < 1e-4, f"volume {vol} vs {expected}"
    # the line as built: its top face is the only thing at the line's height; width, centre and length as asked
    top = [p for p in pts if abs(p[2] - rz[1]) < TOL]
    w = max(p[0] for p in top) - min(p[0] for p in top)
    c = (max(p[0] for p in top) + min(p[0] for p in top)) / 2
    length = max(p[1] for p in top) - min(p[1] for p in top)
    assert abs(w - width) < 2e-6, f"line is {w} wide, expected {width}"
    assert abs(c - g["centre_x"]) < 2e-6, f"line centre {c}, expected {g['centre_x']}"
    assert abs(length - (fy[1] - fy[0])) < 2e-6, f"line is {length} long, not end to end"
    return vol


def main():
    header, tmpl = read_stl(TEMPLATE)
    g = new_geometry(template_geometry(tmpl))
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
            sys.exit(f"{name}: a {width} mm line does not fit on the flange")
        tris = prism(g, lo, hi)
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
            "overall_height_mm": f"{g['fin_z'][1] - g['flange_z'][0]:.3f}",
            "bodies": 1,
            "triangles": len(tris),
            "volume_mm3": f"{vol:.5f}",
            "walls": s[WALLS_COL],
            "sha256": hashlib.sha256(blob).hexdigest(),
        })
    with open(TABLE, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    # one zip with every file, with fixed timestamps so reruns give the same zip
    with zipfile.ZipFile(ZIP, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for r in rows:
            info = zipfile.ZipInfo(f"{ZIP_NAME}/{r['set_name']}.stl", date_time=(2026, 11, 20, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, (OUT / f"{r['set_name']}.stl").read_bytes())
    print(f"{len(rows)} files in {OUT.relative_to(HERE)}/ and {ZIP.name}, all one closed body: flange "
          f"{rows[0]['flange_mm']} mm, line {rows[0]['rectangle_height_mm']} mm tall and "
          f"{rows[0]['rectangle_length_mm']} mm long, {min(float(r['rectangle_width_mm']) for r in rows):.3f} to "
          f"{max(float(r['rectangle_width_mm']) for r in rows):.3f} mm wide")


if __name__ == "__main__":
    main()
