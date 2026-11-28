"""Build person.npz, the scale figure in the build animation (render_scale.person), from MakeHuman's CC0 assets.

Why: the figure had been lofted from ellipses and tubes twice (2026-11-20, 2026-11-23), and both looked wrong ("human
looks weird", "the human still looks weird", PR #266). This one is MakeHuman's anatomical base mesh, shaped into an
adult man with MakeHuman's own macro targets, dressed in MakeHuman's clothes fitted to it the way MakeHuman fits them,
and carrying MakeHuman's skeleton and skin weights, so render_scale.person() can pose it (arms down, reaching).

Assets, all CC0 1.0 ("These assets have been released under CC0 1.0 Universal", part C of MakeHuman's LICENSE.md):
  base mesh, macro targets, skeleton and skin weights:
      github.com/makehumancommunity/makehuman @ a8bc2d54ff0ac92e78ff71431b1023eda42bf482, makehuman/data/
  clothes (male_casualsuit02: long-sleeved T-shirt and jeans), shoes (shoes06), hair (short02), eyes (low-poly),
  eyebrows (eyebrow001):
      makehuman_system_assets_cc0.zip from files.makehumancommunity.org/asset_packs/makehuman_system_assets/
      (280,737,770 bytes, sha256 b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107)
No MakeHuman program code (AGPL) is used or copied: this script reads the asset file formats itself.

The man: MakeHuman's default proportions for a 25-year-old male of average muscle and weight, with its default equal
blend of its three ancestry targets, scaled to 1750 mm barefoot (crown to sole), the stature the earlier figures used.
Drawn in flat colours (no textures): the T-shirt and jeans are told apart by their shells, the eyebrows by the opaque
part of their texture, the iris by direction.

Output (desktop-lpbf/cad/human/person.npz), all in mm, z up, the figure facing -y with its left side at +x, shoe soles on
z = 0, in MakeHuman's rest pose (an A-pose; person() poses it):
  V (n, 3) float32 vertices        F (m, 3) int32 triangles        fmat (m,) uint8 material, names in `mats`
  bones (b,) names                 head (b, 3) joint each bone turns about        parent (b,) int (-1 for the root)
  sk_i (n, 4) uint8 bones          sk_w (n, 4) float32 weights (each row sums to 1)
  marks: named points (crown, chin, shoulder and wrist joints, ...) for checks

Run:  python desktop-lpbf/cad/human/build_person.py [--cache /tmp/makehuman-cc0]   (downloads ~282 MB once)
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import pathlib
import sys
import urllib.request
import zipfile

import numpy as np

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "person.npz"
MH_SHA = "a8bc2d54ff0ac92e78ff71431b1023eda42bf482"
MH_RAW = f"https://raw.githubusercontent.com/makehumancommunity/makehuman/{MH_SHA}/makehuman/data/"
SYS_URL = "https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip"
SYS_SHA256 = "b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107"
GH_FILES = ["3dobjs/base.obj", "rigs/default.mhskel", "rigs/default_weights.mhw",
            "targets/macrodetails/african-male-young.target", "targets/macrodetails/asian-male-young.target",
            "targets/macrodetails/caucasian-male-young.target",
            "targets/macrodetails/universal-male-young-averagemuscle-averageweight.target"]
SUIT, SHOES, HAIR, EYES, BROWS = ("clothes/male_casualsuit02", "clothes/shoes06", "hair/short02", "eyes/low-poly",
                                  "eyebrows/eyebrow001")
STATURE = 1750.0          # mm, barefoot, crown to sole
BROW_ALPHA = 0.3          # an eyebrow card's face is drawn where its texture is at least this opaque on average


# ------------------------------------------------------------------ fetching
def fetch(cache: pathlib.Path):
    """MakeHuman's files into `cache` (once); returns {relative path: local path} and the opened system-asset zip."""
    cache.mkdir(parents=True, exist_ok=True)
    paths = {}
    for f in GH_FILES:
        p = cache / "gh" / f
        if not p.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(urllib.request.urlopen(MH_RAW + f, timeout=120).read())
        paths[f] = p
    z = cache / "makehuman_system_assets_cc0.zip"
    if not z.exists():
        tmp = z.with_suffix(".part")
        with urllib.request.urlopen(SYS_URL, timeout=600) as r, open(tmp, "wb") as fh:
            while True:
                b = r.read(1 << 20)
                if not b:
                    break
                fh.write(b)
        tmp.rename(z)
    h = hashlib.sha256()
    with open(z, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    if h.hexdigest() != SYS_SHA256:
        sys.exit(f"system-asset zip sha256 {h.hexdigest()} != {SYS_SHA256}: stop")
    return paths, zipfile.ZipFile(z)


# ------------------------------------------------------------------ readers (asset formats, read here)
def read_obj(text):
    """(V, VT, faces, face-uv, face-group) from Wavefront OBJ text; faces keep their n-gons (MakeHuman uses quads)."""
    V, VT, F, FT, G = [], [], [], [], []
    g = None
    for line in text.splitlines():
        if line.startswith("v "):
            V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("vt "):
            VT.append([float(x) for x in line.split()[1:3]])
        elif line.startswith("g "):
            parts = line.split()
            g = parts[1] if len(parts) > 1 else None
        elif line.startswith("f "):
            ids, tids = [], []
            for tok in line.split()[1:]:
                p = tok.split("/")
                ids.append(int(p[0]) - 1)
                tids.append(int(p[1]) - 1 if len(p) > 1 and p[1] else -1)
            F.append(ids)
            FT.append(tids)
            G.append(g)
    return np.array(V, float), np.array(VT, float) if VT else np.zeros((0, 2)), F, FT, G


def read_target(text, n):
    """A .target file: lines 'vertex dx dy dz' -> dense (n, 3) offsets."""
    d = np.zeros((n, 3))
    for line in text.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        i, x, y, z = line.split()
        d[int(i)] = (float(x), float(y), float(z))
    return d


def read_mhclo(text):
    """A .mhclo proxy: the three base-mesh vertices and weights each proxy vertex hangs from, its offset, the axis scale
    references (vertex, vertex, reference distance per axis), the base-mesh vertices it hides, and its OBJ name."""
    refs, wts, offs, scale, delete, obj = [], [], [], {}, set(), None
    mode = None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        key = line.split()[0]
        if key == "verts":
            mode = "verts"
            continue
        if key == "delete_verts":
            mode = "delete"
            continue
        if key in ("x_scale", "y_scale", "z_scale"):
            a, b, r = line.split()[1:4]
            scale["xyz".index(key[0])] = (int(a), int(b), float(r))
            continue
        if key == "obj_file":
            obj = line.split()[1]
            continue
        if not key.lstrip("-").replace(".", "", 1).isdigit():  # any other keyword line (material, tag, ...) can sit
            continue                                              # between "verts 0" and the vertex lines
        if mode == "verts":
            t = line.split()
            if len(t) == 9:
                refs.append([int(t[0]), int(t[1]), int(t[2])])
                wts.append([float(t[3]), float(t[4]), float(t[5])])
                offs.append([float(t[6]), float(t[7]), float(t[8])])
            elif len(t) == 1:                    # exact copy of one base vertex
                refs.append([int(t[0])] * 3)
                wts.append([1.0, 0.0, 0.0])
                offs.append([0.0, 0.0, 0.0])
            else:
                mode = None
        elif mode == "delete":
            t = line.split()
            k = 0
            while k < len(t):
                if k + 2 < len(t) and t[k + 1] == "-":
                    delete.update(range(int(t[k]), int(t[k + 2]) + 1))
                    k += 3
                else:
                    delete.add(int(t[k]))
                    k += 1
    return np.array(refs), np.array(wts), np.array(offs), scale, delete, obj


def fit_proxy(V, refs, wts, offs, scale):
    """Proxy vertices on the shaped base mesh: the weighted sum of the three reference vertices plus the offset, the
    offset stretched per axis by how far the shaped mesh's scale vertices are apart against the reference distance."""
    s = np.ones(3)
    for ax, (a, b, r) in scale.items():
        s[ax] = abs(V[a, ax] - V[b, ax]) / r
    return (V[refs] * wts[..., None]).sum(axis=1) + offs * s


def tri(faces):
    """Fan-triangulate n-gons."""
    out = []
    for f in faces:
        for k in range(1, len(f) - 1):
            out.append([f[0], f[k], f[k + 1]])
    return np.array(out, int)


# ------------------------------------------------------------------ skeleton: MakeHuman's 163 bones grouped into 23
GROUPS = [  # (group, parent group, MakeHuman bones whose weights it takes, bones whose mean head is its joint)
    ("hips", None, ["root", "spine05", "pelvis.L", "pelvis.R"], None),
    ("spine_low", "hips", ["spine04", "spine03"], None),
    ("spine_up", "spine_low", ["spine02", "spine01", "breast.L", "breast.R"], None),
    ("neck", "spine_up", ["neck01", "neck02", "neck03"], None),
    ("head", "neck", ["head"], None),                               # plus every face bone (group_of)
]
for S in ("L", "R"):
    GROUPS += [
        (f"clavicle.{S}", "spine_up", [f"clavicle.{S}", f"shoulder01.{S}"], None),
        (f"upperarm.{S}", f"clavicle.{S}", [f"upperarm01.{S}", f"upperarm02.{S}"], None),
        (f"lowerarm.{S}", f"upperarm.{S}", [f"lowerarm01.{S}", f"lowerarm02.{S}"], None),
        (f"hand.{S}", f"lowerarm.{S}", [f"wrist.{S}"], None),          # plus the metacarpals and the thumb
        (f"fingers.{S}", f"hand.{S}", [f"finger{k}-1.{S}" for k in range(2, 6)], [f"finger{k}-1.{S}" for k in range(2, 6)]),
        (f"fingertips.{S}", f"fingers.{S}", [f"finger{k}-{j}.{S}" for k in range(2, 6) for j in (2, 3)],
         [f"finger{k}-2.{S}" for k in range(2, 6)]),
        (f"upperleg.{S}", "hips", [f"upperleg01.{S}", f"upperleg02.{S}"], None),
        (f"lowerleg.{S}", f"upperleg.{S}", [f"lowerleg01.{S}", f"lowerleg02.{S}"], None),
        (f"foot.{S}", f"lowerleg.{S}", [f"foot.{S}"], None),                 # plus the toes
    ]


def group_of(bone, skel):
    """The group a MakeHuman bone's weights go to: its own, or the nearest ancestor's that is listed."""
    listed = {b: g for g, _, bs, _ in GROUPS for b in bs}
    b = bone
    while b is not None:
        if b in listed:
            return listed[b]
        b = skel["bones"][b]["parent"]
    return "hips"


# ------------------------------------------------------------------ build
def build(cache):
    paths, Z = fetch(cache)
    rd = lambda p: Z.read(p).decode("utf-8", "replace")                  # noqa: E731
    V, _, faces, _, groups = read_obj(paths["3dobjs/base.obj"].read_text())
    n = len(V)
    # 25-year-old male, average muscle and weight, MakeHuman's default equal blend of its three ancestry targets
    for t, w in (("african-male-young", 1 / 3), ("asian-male-young", 1 / 3), ("caucasian-male-young", 1 / 3),
                 ("universal-male-young-averagemuscle-averageweight", 1.0)):
        V = V + w * read_target(paths[f"targets/macrodetails/{t}.target"].read_text(), n)
    skel = json.loads(paths["rigs/default.mhskel"].read_text())
    jpos = {j: V[idx].mean(axis=0) for j, idx in skel["joints"].items()}
    wfile = json.loads(paths["rigs/default_weights.mhw"].read_text())["weights"]
    gnames = [g for g, _, _, _ in GROUPS]
    gi = {g: k for k, g in enumerate(gnames)}
    W = np.zeros((n, len(gnames)))
    for bone, pairs in wfile.items():
        k = gi[group_of(bone, skel)]
        for v, w in pairs:
            W[v, k] += w
    unweighted = W.sum(axis=1) <= 1e-9
    W[unweighted, gi["hips"]] = 1.0
    W /= W.sum(axis=1, keepdims=True)
    heads = np.array([np.mean([jpos[skel["bones"][b]["head"]] for b in (jb or bs[:1])], axis=0) for _, _, bs, jb in GROUPS])
    parent = np.array([gi[p] if p else -1 for _, p, _, _ in GROUPS])

    # ---- the body: MakeHuman's "body" group, less what the clothes hide
    body_f = [f for f, g in zip(faces, groups) if g == "body"]
    pieces = []                                   # (vertices, weights, triangles, material per triangle)
    hidden = set()
    proxies = {}
    for name, path in (("suit", SUIT), ("shoes", SHOES), ("hair", HAIR), ("eyes", EYES), ("brows", BROWS)):
        stem = path.split("/")[-1]
        refs, wts, offs, scale, delete, obj = read_mhclo(rd(f"{path}/{stem}.mhclo"))
        PV = fit_proxy(V, refs, wts, offs, scale)
        PW = (W[refs] * wts[..., None]).sum(axis=1)
        PW /= PW.sum(axis=1, keepdims=True)
        _, PVT, pf, pft, _ = read_obj(rd(f"{path}/{obj}"))
        proxies[name] = (PV, PW, pf, pft, PVT)
        hidden |= delete
    keep = [f for f in body_f if not any(v in hidden for v in f)]
    T = tri(keep)
    pieces.append((V, W, T, np.full(len(T), 0)))                          # skin
    MATS = ["skin", "shirt", "jeans", "shoe", "sole", "hair", "eye_white", "iris", "brow"]
    m = {k: i for i, k in enumerate(MATS)}

    # suit: the T-shirt and the jeans are two separate shells of one mesh; a shell is the jeans if most of its faces sit in
    # the jeans' block of the texture atlas (u < 0.72, v < 0.585)
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    PV, PW, pf, pft, PVT = proxies["suit"]
    T = tri(pf)
    uv = PVT[tri(pft)].mean(axis=1)
    by_uv = (uv[:, 0] < 0.72) & (uv[:, 1] < 0.585)
    r, c = np.r_[T[:, 0], T[:, 1], T[:, 2]], np.r_[T[:, 1], T[:, 2], T[:, 0]]
    _, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(PV), len(PV))), directed=False)
    flab = lab[T[:, 0]]
    mat = np.full(len(T), m["shirt"])
    for comp in np.unique(flab):
        if by_uv[flab == comp].mean() > 0.5:
            mat[flab == comp] = m["jeans"]
    pieces.append((PV, PW, T, mat))
    # shoes: uppers, and the soles darker (the lowest faces)
    PV, PW, pf, pft, PVT = proxies["shoes"]
    T = tri(pf)
    zc = PV[T].mean(axis=1)[:, 1]
    floor = PV[:, 1].min()
    pieces.append((PV, PW, T, np.where(zc < floor + 0.09, m["sole"], m["shoe"])))
    PV, PW, pf, pft, PVT = proxies["hair"]
    T = tri(pf)
    pieces.append((PV, PW, T, np.full(len(T), m["hair"])))
    # eyes: white, with the iris where the face points within 30 deg of straight ahead (+z in MakeHuman)
    PV, PW, pf, pft, PVT = proxies["eyes"]
    T = tri(pf)
    mat = np.full(len(T), m["eye_white"])
    for side in (PV[:, 0] > 0, PV[:, 0] <= 0):
        idx = np.where(side)[0]
        c = PV[idx].mean(axis=0)
        fc = PV[T].mean(axis=1)
        on = side[T].all(axis=1)
        d = fc - c
        d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-12
        mat[on & (d[:, 2] > np.cos(np.radians(30)))] = m["iris"]            # iris ~12 mm across a ~24 mm eye
    pieces.append((PV, PW, T, mat))
    # eyebrows: MakeHuman draws them as alpha-textured cards; keep the faces whose texture is mostly opaque
    from PIL import Image
    PV, PW, pf, pft, PVT = proxies["brows"]
    alpha = np.asarray(Image.open(io.BytesIO(Z.read(f"{BROWS}/{BROWS.split('/')[-1]}.png"))).convert("RGBA"), float)[..., 3] / 255
    T, TT = tri(pf), tri(pft)
    hgt, wid = alpha.shape
    cover = np.zeros(len(T))
    for wa, wb, wc in ((1 / 3, 1 / 3, 1 / 3), (0.6, 0.2, 0.2), (0.2, 0.6, 0.2), (0.2, 0.2, 0.6)):
        q = PVT[TT[:, 0]] * wa + PVT[TT[:, 1]] * wb + PVT[TT[:, 2]] * wc
        cover += alpha[np.clip(((1 - q[:, 1]) * hgt).astype(int), 0, hgt - 1), np.clip((q[:, 0] * wid).astype(int), 0, wid - 1)] / 4
    T = T[cover > BROW_ALPHA]
    pieces.append((PV, PW, T, np.full(len(T), m["brow"])))

    # ---- merge, keep only used vertices, convert to mm / z up / facing -y, stand the soles on z = 0
    allV, allW, allT, allM = [], [], [], []
    off = 0
    for PVk, PWk, Tk, Mk in pieces:
        used = np.unique(Tk)
        remap = -np.ones(len(PVk), int)
        remap[used] = np.arange(len(used)) + off
        allV.append(PVk[used])
        allW.append(PWk[used])
        allT.append(remap[Tk])
        allM.append(Mk)
        off += len(used)
    V2 = np.concatenate(allV)
    W2 = np.concatenate(allW)
    T2 = np.concatenate(allT)
    M2 = np.concatenate(allM)
    body_v = V[np.unique(tri(body_f))]
    s = STATURE / (body_v[:, 1].max() - body_v[:, 1].min())             # barefoot crown-to-sole -> 1750 mm

    def conv(P):
        P = np.asarray(P, float) * s
        return np.stack([P[..., 0], -P[..., 2], P[..., 1]], axis=-1)

    V2 = conv(V2)
    H2 = conv(heads)
    z0 = V2[np.unique(T2[M2 == m["sole"]])][:, 2].min()                  # the soles stand on z = 0
    V2[:, 2] -= z0
    H2[:, 2] -= z0
    # four largest weights per vertex
    order = np.argsort(-W2, axis=1)[:, :4]
    sw = np.take_along_axis(W2, order, axis=1)
    sw /= sw.sum(axis=1, keepdims=True)
    bodyc = conv(body_v)
    bodyc[:, 2] -= z0
    marks = {
        "crown": bodyc[np.argmax(bodyc[:, 2])],
        "barefoot_sole": bodyc[np.argmin(bodyc[:, 2])],
        "shoulder.L": H2[gi["upperarm.L"]], "elbow.L": H2[gi["lowerarm.L"]], "wrist.L": H2[gi["hand.L"]],
        "hip.L": H2[gi["upperleg.L"]], "knee.L": H2[gi["lowerleg.L"]], "ankle.L": H2[gi["foot.L"]],
    }
    for S in ("L", "R"):                                                    # knuckle lines, for curling the fingers
        for k in (2, 5):
            q = conv(jpos[skel["bones"][f"finger{k}-1.{S}"]["head"]])
            q[2] -= z0
            marks[f"knuckle{k}.{S}"] = q
    print(f"{len(V2)} vertices, {len(T2)} triangles; scale {s:.3f} mm per MakeHuman unit; soles at z=0, barefoot sole "
          f"at {marks['barefoot_sole'][2]:.1f} mm, crown at {marks['crown'][2]:.1f} mm")
    for k, v in marks.items():
        print(f"  {k:14s} {v.round(1)}")
    for k, name in enumerate(MATS):
        print(f"  {name:10s} {(M2 == k).sum()} triangles")
    np.savez_compressed(OUT, V=V2.astype(np.float32), F=T2.astype(np.int32), fmat=M2.astype(np.uint8), mats=np.array(MATS),
                        bones=np.array(gnames), head=H2.astype(np.float32), parent=parent.astype(np.int16),
                        sk_i=order.astype(np.uint8), sk_w=sw.astype(np.float32),
                        mark_names=np.array(list(marks)), mark_pos=np.array(list(marks.values()), np.float32))
    print("wrote", OUT, f"{OUT.stat().st_size / 1e6:.2f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/makehuman-cc0")
    build(pathlib.Path(ap.parse_args().cache))
