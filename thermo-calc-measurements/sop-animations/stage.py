"""The shared stage for the SOP animations (#262, PR #263): a lab bench, instruments placed on it as rigs, data panels
beside the 3-D, title cards between chapters, and the joining of chapters into one video per SOP.

It builds on byu-vcl's vertical-lab code (``vl_fetch.py`` fetches it, pinned, into ``vl/``):

* ``scene.Scene``: PyVista actors in groups (a group can ride on another), ``step(label, caption, seconds, update,
  hold, cam_to, labels)`` for one captioned sub-step with an eased motion and a camera move, text drawn with PIL,
  every frame piped to ffmpeg (``out/mp4/<name>.mp4``) and a GIF (``out/<name>.gif``), the sub-steps' frame ranges in
  ``out/<name>.json``.
* ``instruments.Instrument`` / ``Joint``: a model as named pieces (CadQuery solids with materials) and the joints
  that move them (slide, hinge, spin, path, fade), sized from the maker's published W x D x H.
* ``register.py``: fits a model to frames of real footage or photos (see ``fit.py`` here).

Frame: x to the right and y away from you when you face the bench, z up, millimetres. The floor is z = 0 and the
bench top z = BENCH_H, so a benchtop instrument goes at ``T((x, y, BENCH_H))``.

    import stage as S
    sc = S.SOPScene("sop01_dsc_c1", "SOP 01 · DSC melting and freezing of atomized powder")
    S.room(sc, x0=-1500, x1=1500)                       # floor, bench, wall
    inst, ents = S.get("furnace")                       # a byu-vcl model, or one of ours (models_*.py)
    rig = S.Rig(sc, inst, ents, "furnace:", at=S.T((0, 0, S.BENCH_H)))
    sc.cam = S.look((0, 0, S.BENCH_H + 250), dist=1600, az=-30, el=20)
    sc.step("1.1", "Open the door.", 2.0, rig.move({"door": (0, 1)}))
    sc.save()

Environment: ``VIZ3D_FPS`` (default 15 here), ``VIZ3D_SIZE`` (default 1280x720), ``PREVIEW=1`` (only the last frame of
each sub-step, as a contact sheet in /tmp).
"""
from __future__ import annotations

import hashlib
import importlib
import json
import math
import os
import pickle
import subprocess
import sys
from pathlib import Path

os.environ.setdefault("VIZ3D_FPS", "15")

import numpy as np

HERE = Path(__file__).resolve().parent
VL = HERE / "vl"
if not (VL / "scene.py").exists():
    raise SystemExit("vl/ is missing: run `python vl_fetch.py` first")
for _p in (str(HERE), str(VL), str(VL / "lab_models")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pyvista as pv  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

import scene  # noqa: E402
from scene import FPS, Scene, R, T, ease, font, mix, window  # noqa: E402,F401

scene.OUT = HERE / "out"
OUT = scene.OUT
CACHE = HERE / ".cache"

import common as LM  # noqa: E402
import instruments as I  # noqa: E402
from instruments import Instrument, Joint  # noqa: E402,F401

BENCH_H = 900.0          # bench top above the floor, mm (a standard lab bench is 900-915 mm)
BENCH_D = 760.0          # bench depth, mm

# ============================================================================================== materials
# (r, g, b, opacity, shininess 0-1), as in byu-vcl's tables
MATERIALS = {
    "bench_top": (0.17, 0.18, 0.19, 1.0, 0.30),        # black epoxy-resin worktop
    "bench_edge": (0.12, 0.12, 0.13, 1.0, 0.25),
    "cabinet": (0.78, 0.80, 0.80, 1.0, 0.12),          # painted steel base cabinets
    "cabinet_line": (0.55, 0.57, 0.58, 1.0, 0.10),
    "kick": (0.20, 0.20, 0.21, 1.0, 0.10),
    "wall": (0.93, 0.93, 0.91, 1.0, 0.02),
    "floor_tile": (0.86, 0.86, 0.84, 1.0, 0.05),
    "alumina_crucible": (0.95, 0.94, 0.89, 1.0, 0.15),
    "al_powder": (0.60, 0.61, 0.63, 1.0, 0.05),
    "cu_powder": (0.74, 0.48, 0.30, 1.0, 0.05),
    "al_metal": (0.80, 0.81, 0.83, 1.0, 0.85),
    "cu_metal": (0.80, 0.52, 0.36, 1.0, 0.85),
    "melt": (1.00, 0.58, 0.18, 1.0, 0.10),
    "hot": (0.95, 0.30, 0.05, 1.0, 0.10),
    "nitrile": (0.30, 0.46, 0.86, 1.0, 0.15),
    "glass": (0.82, 0.90, 0.95, 0.28, 0.90),
    "water_clear": (0.60, 0.78, 0.92, 0.40, 0.80),
    "label": (0.98, 0.98, 0.96, 1.0, 0.05),
    "paper": (0.97, 0.97, 0.95, 1.0, 0.02),
    "ptfe": (0.95, 0.95, 0.93, 1.0, 0.10),
    "steel": (0.62, 0.64, 0.66, 1.0, 0.70),
    "brass": (0.80, 0.64, 0.30, 1.0, 0.70),
    "rubber": (0.10, 0.10, 0.11, 1.0, 0.10),
    "screen_ui": (0.20, 0.45, 0.70, 1.0, 0.60),
    "led_green": (0.20, 0.90, 0.35, 1.0, 0.10),
    "led_red": (0.95, 0.15, 0.10, 1.0, 0.10),
    "plasma": (0.75, 0.55, 1.00, 0.85, 0.00),
    "argon_blue": (0.25, 0.45, 0.75, 1.0, 0.40),         # argon cylinder paint (varies by country; blue-grey here)
}
GLOWY = {"glow", "laser", "screen_on", "vlm_led", "led_blue", "px_ui", "nat_screen", "melt", "hot", "plasma",
         "screen_ui", "led_green", "led_red"}

MATS: dict = {}


def _collect_materials() -> None:
    MATS.update(LM.MATERIALS)
    for name in ("instruments", "instruments_char", "instruments_lab", "instruments_r7", "r8_prep", "r8_char",
                 "r8_specimens", "r8_test", "r8_store"):
        try:
            MATS.update(getattr(importlib.import_module(name), "MATERIALS", {}))
        except Exception as e:                             # noqa: BLE001
            print(f"stage: materials of {name} skipped ({type(e).__name__}: {e})", flush=True)
    MATS.update(MATERIALS)
    for f in sorted(HERE.glob("models_*.py")):
        try:
            MATS.update(getattr(importlib.import_module(f.stem), "MATERIALS", {}))
        except Exception as e:                             # noqa: BLE001
            print(f"stage: materials of {f.stem} skipped ({type(e).__name__}: {e})", flush=True)


# ================================================================================================= meshes
def to_mesh(shape, tol: float = 0.5, ang: float = 0.12) -> pv.PolyData:
    """CadQuery shape -> triangles (tol: chord tolerance in mm; ang: angular, radians)."""
    if hasattr(shape, "val") and not hasattr(shape, "tessellate"):
        vals = shape.vals()
        shape = vals[0] if len(vals) == 1 else LM.cq.Compound.makeCompound(vals)
    verts, tris = shape.tessellate(tol, ang)
    if not tris:
        return pv.PolyData()
    pts = np.array([(v.x, v.y, v.z) for v in verts], float)
    faces = np.hstack([[3, *t] for t in tris])
    return pv.PolyData(pts, faces)


def merge(meshes) -> pv.PolyData:
    meshes = [m for m in meshes if m is not None and m.n_points]
    if not meshes:
        return pv.PolyData()
    out = meshes[0].merge(meshes[1:]) if len(meshes) > 1 else meshes[0]
    return out.clean(tolerance=1e-6)


def piece_entries(inst: Instrument, tol: float = 0.5, ang: float = 0.12) -> dict:
    """{piece: [entry]}, one merged mesh per material (as byu-vcl's tour.py)."""
    if not MATS:
        _collect_materials()
    out = {}
    for name, model in inst.pieces.items():
        by = {}
        for p in model.parts:
            by.setdefault(p.material, []).append(to_mesh(p.shape, tol, ang))
        out[name] = []
        for mat, ms in by.items():
            if mat not in MATS:
                raise KeyError(f"{inst.key}/{name}: material {mat!r} is in no MATERIALS table")
            r, g, b, a, spec = MATS[mat]
            out[name].append(dict(mesh=merge(ms), color=(r, g, b), opacity=a, specular=spec, material=mat))
    for name, parts in inst.meshes.items():
        out.setdefault(name, [])
        for mesh, col, op in parts:
            out[name].append(dict(mesh=mesh, color=col, opacity=op, specular=0.25, material="mesh"))
    return out


# where each model we reuse from byu-vcl is built: key -> (module, function). Ours register in models_*.py REGISTRY.
VL_MODELS = {
    "polisher": ("instruments", "polisher"),           # LECO PX500, fitted to the lab's own SOP videos
    "mount_press": ("r8_prep", "mount_press"),          # LECO MX400, from the lab's "Making Bakelite Polishing Puck"
    "hardness": ("r8_char", "hardness"),                # Mitutoyo HM-220 Type D (AVPAK) micro-Vickers
    "furnace": ("instruments", "furnace"),              # Nabertherm NAT 15/65, fitted to Nabertherm's video
    "fumehood": ("instruments_r7", "fumehood"),         # Labconco Protector XStream 4 ft
    "vhx": ("r8_char", "vhx"),                          # Keyence VHX-7000 digital microscope
    "sem": ("r8_char", "sem"),                          # Hitachi TM4000PlusII tabletop SEM
    "quench_tank": ("r8_test", "quench_tank"),          # a water tank with a lift basket
    "xrd": ("instruments", "xrd"),                      # Rigaku MiniFlex
}


def _builder(key: str):
    """(build function, its source files) for a key: ours first (models_*.py), then byu-vcl's."""
    for f in sorted(HERE.glob("models_*.py")):
        mod = importlib.import_module(f.stem)
        if key in getattr(mod, "REGISTRY", {}):
            return mod.REGISTRY[key], [f, Path(__file__)]
    if key in VL_MODELS:
        modname, fn = VL_MODELS[key]
        mod = importlib.import_module(modname)
        return getattr(mod, fn), sorted(VL.glob("*.py")) + sorted((VL / "lab_models").glob("*.py"))
    raise KeyError(f"no model {key!r}: add it to a models_*.py REGISTRY")


def get(key: str, rebuild: bool = False, tol: float = 0.5):
    """(Instrument, entries) for a model key, cached in .cache/ on its sources' hash."""
    if not MATS:
        _collect_materials()
    build, sources = _builder(key)
    h = hashlib.sha256(f"{key}|{tol}".encode())
    for f in sources:
        h.update(Path(f).read_bytes())
    CACHE.mkdir(exist_ok=True)
    path = CACHE / f"{key}_{h.hexdigest()[:12]}.pkl"
    if path.exists() and not rebuild:
        try:
            return pickle.loads(path.read_bytes())
        except Exception:                                   # noqa: BLE001  (half-written by another process)
            pass
    inst = build()
    out = (inst, piece_entries(inst, tol))
    tmp = path.with_suffix(f".{os.getpid()}.tmp")
    tmp.write_bytes(pickle.dumps(out))
    os.replace(tmp, path)
    return out


def props(name: str, model: "LM.Model", tol: float = 0.3) -> dict:
    """A small Model (a crucible, a vial, tweezers) as entries, like an instrument's one piece."""
    if not MATS:
        _collect_materials()
    inst = Instrument(name, name, name, (0, 0, 0), "", pieces={"body": model})
    return piece_entries(inst, tol)["body"]


# ================================================================================================= staging
class Rig:
    """An instrument in a scene: its pieces as groups under `prefix`, placed at `at` (4x4), with joint values.
    ``move({piece: (v0 or None, v1)})`` returns an update(u) for Scene.step; ``set(piece=v)`` jumps there."""

    def __init__(self, sc: Scene, inst: Instrument, entries: dict, prefix: str, at=np.eye(4), parent=None):
        self.sc, self.inst, self.prefix = sc, inst, prefix
        self.base = at
        self.v = {k: j.v0 for k, j in inst.joints.items()}
        self.v.update({f"~{k}": 0.0 for k in entries})              # see-through amount of each piece
        self.names: dict[str, list[str]] = {}
        root = f"{prefix}body"
        for piece, ents in entries.items():
            g = f"{prefix}{piece}"
            self.names[piece] = []
            for i, e in enumerate(ents):
                if not e["mesh"].n_points:
                    continue
                kw = dict(specular=e["specular"])
                if e["material"] in GLOWY:
                    kw.update(ambient=0.9, diffuse=0.25)
                n = f"{g}/{e['material']}{i}"
                sc.add(n, e["mesh"], e["color"], g, opacity=e["opacity"], **kw)
                self.names[piece].append(n)
            if piece != "body":
                j = inst.joints.get(piece)
                sc.parent[g] = f"{prefix}{j.parent}" if j is not None and j.parent else root
        sc.gmat[root] = at
        if parent is not None:
            sc.parent[root] = parent
        self.apply()

    def group(self, piece: str = "body") -> str:
        return f"{self.prefix}{piece}"

    def apply(self):
        for piece, j in self.inst.joints.items():
            g = f"{self.prefix}{piece}"
            self.sc.gmat[g] = j.matrix(self.v[piece])
            if j.kind == "fade":
                for n in self.names.get(piece, []):
                    self.sc.alpha[n] = self.v[piece]
        for piece, ns in self.names.items():
            g = self.v.get(f"~{piece}", 0.0)
            if g > 0 or piece not in self.inst.joints or self.inst.joints[piece].kind != "fade":
                for n in ns:
                    self.sc.alpha[n] = 1.0 - 0.82 * g

    def move(self, targets: dict):
        start = {}

        def up(u):
            if not start:
                start.update({k: self.v[k] for k in targets})
            for k, (a, b) in targets.items():
                a = start[k] if a is None else a
                self.v[k] = a + (b - a) * u
            self.apply()
        return up

    def set(self, **values):
        self.v.update(values)
        self.apply()

    def world(self, xyz, piece: str = "body") -> np.ndarray:
        """A point given in the instrument's own frame (of `piece`, as it is now) -> world."""
        m = self.sc.world(f"{self.prefix}{piece}") if piece != "body" else self.sc.world(f"{self.prefix}body")
        return (m @ np.array([*xyz, 1.0]))[:3]

    def show(self, a: float = 1.0):
        self.sc.show(self.all_names(), a)

    def all_names(self):
        return [n for ns in self.names.values() for n in ns]


def add_entries(sc: Scene, entries: list, name: str, group: str, at=None, parent=None) -> list[str]:
    """Add a props() entry list as one group (`group`), placed at `at` and riding on `parent` if given."""
    names = []
    for i, e in enumerate(entries):
        if not e["mesh"].n_points:
            continue
        kw = dict(specular=e["specular"])
        if e["material"] in GLOWY:
            kw.update(ambient=0.9, diffuse=0.25)
        n = f"{name}/{e['material']}{i}"
        sc.add(n, e["mesh"], e["color"], group, opacity=e["opacity"], **kw)
        names.append(n)
    if at is not None:
        sc.gmat[group] = at
    if parent is not None:
        sc.parent[group] = parent
    return names


def mover(sc: Scene, group: str, a, b):
    """update(u) moving a group from pose a to pose b (4x4s; rotation by slerp-free blend of axis-angle)."""
    a, b = np.asarray(a, float), np.asarray(b, float)

    def up(u):
        sc.gmat[group] = blend(a, b, u)
    return up


def blend(a: np.ndarray, b: np.ndarray, u: float) -> np.ndarray:
    """A pose between a and b: positions linear, rotation along the shortest path."""
    from scipy.spatial.transform import Rotation, Slerp
    ra, rb = Rotation.from_matrix(a[:3, :3]), Rotation.from_matrix(b[:3, :3])
    m = np.eye(4)
    m[:3, :3] = Slerp([0, 1], Rotation.concatenate([ra, rb]))(u).as_matrix()
    m[:3, 3] = a[:3, 3] + (b[:3, 3] - a[:3, 3]) * u
    return m


def path_mover(sc: Scene, group: str, poses: list):
    """update(u) moving a group through several 4x4 poses, evenly in u."""
    poses = [np.asarray(p, float) for p in poses]

    def up(u):
        s = min(max(u, 0.0), 1.0) * (len(poses) - 1)
        i = min(int(s), len(poses) - 2)
        sc.gmat[group] = blend(poses[i], poses[i + 1], s - i)
    return up


def together(*ups):
    """One update(u) calling several."""
    def up(u):
        for f in ups:
            if f is not None:
                f(u)
    return up


def staged(*parts):
    """update(u) running parts in sequence: staged((0, 0.5, f), (0.5, 1, g)) -> f over u in [0, .5], g over [.5, 1]."""
    def up(u):
        for t0, t1, f in parts:
            if u >= t0:
                f(min(1.0, (u - t0) / max(t1 - t0, 1e-9)))
    return up


# ================================================================================================= the room
def room(sc: Scene, x0: float = -1500.0, x1: float = 1500.0, y_front: float | None = None, wall: bool = True,
         bench: bool = True, floor_size: float = 12000.0, depth: float = BENCH_D, height: float = BENCH_H) -> dict:
    """The floor, a bench from x0 to x1 (its front edge at y_front, default -depth/2, its back at the wall) and the
    wall behind it. Returns the bench's extent."""
    yf = -depth / 2 if y_front is None else y_front
    yb = yf + depth
    floor = pv.Plane(center=(0.5 * (x0 + x1), 0.0, -0.5), direction=(0, 0, 1), i_size=floor_size,
                     j_size=floor_size)
    sc.add("floor", floor, MATERIALS["floor_tile"][:3], "floor", ambient=1.0, diffuse=0.0, specular=0.0,
           smooth_shading=False)
    if bench:
        top = pv.Box(bounds=(x0, x1, yf, yb, height - 32.0, height))
        sc.add("bench/top", top, MATERIALS["bench_top"][:3], "bench", specular=0.25)
        cab = pv.Box(bounds=(x0 + 10, x1 - 10, yf + 45, yb - 5, 100.0, height - 32.0))
        sc.add("bench/cabinet", cab, MATERIALS["cabinet"][:3], "bench", specular=0.1)
        kick = pv.Box(bounds=(x0 + 10, x1 - 10, yf + 85, yb - 5, 0.0, 100.0))
        sc.add("bench/kick", kick, MATERIALS["kick"][:3], "bench", specular=0.05)
        # door and drawer seams: thin dark strips on the cabinet front, every ~600 mm
        n = max(1, int(round((x1 - x0) / 600.0)))
        seams = []
        for i in range(1, n):
            x = x0 + (x1 - x0) * i / n
            seams.append(pv.Box(bounds=(x - 2, x + 2, yf + 43, yf + 46, 100.0, height - 32.0)))
        seams.append(pv.Box(bounds=(x0 + 10, x1 - 10, yf + 43, yf + 46, height - 32.0 - 160, height - 32.0 - 156)))
        for i in range(n):
            xa = x0 + (x1 - x0) * (i + 0.5) / n
            seams.append(pv.Box(bounds=(xa - 60, xa + 60, yf + 38, yf + 45, height - 32.0 - 95, height - 32.0 - 85)))
        sc.add("bench/seams", merge(seams), MATERIALS["cabinet_line"][:3], "bench", specular=0.2)
    if wall:
        w = pv.Plane(center=(0.5 * (x0 + x1), yb + 2.0, 1500.0), direction=(0, -1, 0), i_size=3000.0,
                     j_size=floor_size)
        sc.add("wall", w, MATERIALS["wall"][:3], "wall", ambient=0.9, diffuse=0.2, specular=0.0,
               smooth_shading=False)
    return dict(x0=x0, x1=x1, y_front=yf, y_back=yb, top=height)


def contact_shadow(sc: Scene, bb, z: float = 0.0, strength: float = 0.18, name: str = "shadow"):
    """A soft darker patch under a footprint (bb: xmin, xmax, ymin, ymax in world mm) at height z."""
    x0, x1, y0, y1 = bb[:4]
    w, d = x1 - x0, y1 - y0
    r = 0.08 * min(w, d) + 0.04 * max(w, d) + 8.0
    grid = pv.Plane(center=((x0 + x1) / 2, (y0 + y1) / 2, z + 0.6), direction=(0, 0, 1), i_size=w + 5 * r,
                    j_size=d + 5 * r, i_resolution=40, j_resolution=40)
    p = grid.points
    dx = np.maximum(np.abs(p[:, 0] - (x0 + x1) / 2) - w / 2, 0.0)
    dy = np.maximum(np.abs(p[:, 1] - (y0 + y1) / 2) - d / 2, 0.0)
    a = strength * np.exp(-(np.hypot(dx, dy) / r) ** 2)
    rgba = np.zeros((grid.n_points, 4), np.uint8)
    rgba[:, :3] = 30
    rgba[:, 3] = np.round(255 * a).astype(np.uint8)
    grid.point_data["rgba"] = rgba
    sc.add(name, grid, None, "floor", scalars="rgba", rgba=True, ambient=1.0, diffuse=0.0, specular=0.0,
           smooth_shading=False, show_scalar_bar=False)


def place(sc: Scene, key: str, x: float, y: float, z: float = BENCH_H, rot_deg: float = 0.0, prefix=None,
          shadow: bool = True) -> Rig:
    """get(key) as a Rig at (x, y, z), turned rot_deg about z; with a contact shadow under it."""
    inst, ents = get(key)
    at = T((x, y, z)) @ R((0, 0, 1), rot_deg)
    rig = Rig(sc, inst, ents, prefix or f"{key}:", at=at)
    if shadow:
        bb = inst.bbox()
        c = np.array([[bb[0], bb[2]], [bb[1], bb[2]], [bb[0], bb[3]], [bb[1], bb[3]]])
        th = math.radians(rot_deg)
        rot = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        cw = c @ rot.T + np.array([x, y])
        contact_shadow(sc, (cw[:, 0].min(), cw[:, 0].max(), cw[:, 1].min(), cw[:, 1].max()), z=z,
                       name=f"{rig.prefix}shadow")
    return rig


# ================================================================================================= cameras
def look(target, dist: float, az: float = -30.0, el: float = 20.0):
    """A camera `dist` mm from `target`, az degrees round z from straight in front (-y), el degrees up."""
    a, e = math.radians(az), math.radians(el)
    d = np.array([math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)])
    c = np.asarray(target, float)
    return [tuple(c + d * dist), tuple(c), (0, 0, 1)]


def frame_cam(bb, direction=(1.0, -1.6, 0.9), pad: float = 0.85, look_z: float = 0.42):
    x0, x1, y0, y1, z0, z1 = bb
    c = np.array([(x0 + x1) / 2, (y0 + y1) / 2, z0 + (z1 - z0) * look_z])
    r = 0.5 * np.linalg.norm([x1 - x0, y1 - y0, z1 - z0])
    d = np.asarray(direction, float)
    d /= np.linalg.norm(d)
    dist = pad * r / np.tan(np.radians(15.0)) * 1.05
    return [tuple(c + d * dist), tuple(c), (0, 0, 1)]


# ================================================================================================= the scene
def fig_image(fig, dpi: int = 100) -> Image.Image:
    """A matplotlib figure -> RGBA image (and the figure closed)."""
    import matplotlib.pyplot as plt
    fig.canvas.draw()
    im = Image.frombuffer("RGBA", fig.canvas.get_width_height(), fig.canvas.buffer_rgba(), "raw", "RGBA", 0, 1)
    im = im.copy()
    plt.close(fig)
    return im


class SOPScene(Scene):
    """A Scene with data panels over the 3-D (drawn under the caption) and title cards.

    ``panels[key] = dict(fn=f, rect=(fx, fy, fw), u=0.0, alpha=1.0)``: f(u) -> an RGBA image, drawn with its top left
    at (fx, fy) of the frame and fw of its width; set ``u`` (0-1) from a step's update to animate it. Images are cached
    on (key, round(u, 3)), so a panel can be redrawn only when u moves.
    """

    def __init__(self, name: str, title: str, **kw):
        super().__init__(name, title, **kw)
        self.panels: dict = {}
        self._panel_cache: dict = {}
        self.intro = 0.8

    def panel(self, key, fn, rect=(0.62, 0.10, 0.36), u=0.0, alpha=1.0):
        self.panels[key] = dict(fn=fn, rect=rect, u=u, alpha=alpha)

    def _draw_panels(self, img: Image.Image) -> Image.Image:
        if not self.panels or scene.CLEAN:
            return img
        W, H = img.size
        base = img.convert("RGBA")
        for key, p in list(self.panels.items()):
            a = float(p.get("alpha", 1.0))
            if a <= 0.02:
                continue
            fx, fy, fw = p["rect"]
            tag = (key, round(float(p.get("u", 0.0)), 3), int(fw * W))
            im = self._panel_cache.get(tag)
            if im is None:
                src = p["fn"](float(p.get("u", 0.0)))
                w = int(fw * W)
                h = int(src.height * w / src.width)
                im = src.convert("RGBA").resize((w, h), Image.LANCZOS)
                if len(self._panel_cache) > 400:
                    self._panel_cache.clear()
                self._panel_cache[tag] = im
            if a < 0.999:
                im = im.copy()
                im.putalpha(Image.eval(im.getchannel("A"), lambda v: int(v * a)))
            base.alpha_composite(im, (int(fx * W), int(fy * H)))
        return base.convert("RGB")

    def overlay(self, img: Image.Image, scale: float, anchors) -> Image.Image:
        return super().overlay(self._draw_panels(img), scale, anchors)

    def fade_panel(self, key, a0, a1):
        def up(u):
            if key in self.panels:
                self.panels[key]["alpha"] = a0 + (a1 - a0) * u
        return up

    def drive_panel(self, key, u0=0.0, u1=1.0):
        def up(u):
            if key in self.panels:
                self.panels[key]["u"] = u0 + (u1 - u0) * u
        return up

    # ------------------------------------------------------------------------------------- title cards
    def card(self, heading: str, lines=(), seconds: float = 3.0, label: str = "", note: str = ""):
        """A full-frame title card (white, the SOP's colours) for `seconds`, as its own sub-step."""
        start = self.n
        W, H = self.size
        s = W / 1280.0
        img = Image.new("RGB", (W, H), (250, 251, 252))
        d = ImageDraw.Draw(img)
        d.rectangle((0, 0, W, int(8 * s)), fill=(30, 60, 140))
        fh, fl, fn = font(40 * s, bold=True), font(24 * s), font(17 * s)
        y = int(H * 0.30)
        for t in _wrap(d, heading, fh, W - 160 * s):
            d.text((80 * s, y), t, font=fh, fill=(20, 22, 30))
            y += int(52 * s)
        y += int(16 * s)
        for line in lines:
            for t in _wrap(d, line, fl, W - 160 * s):
                d.text((80 * s, y), t, font=fl, fill=(55, 58, 66))
                y += int(34 * s)
        if note:
            for i, t in enumerate(_wrap(d, note, fn, W - 160 * s)[:3]):
                d.text((80 * s, H - 90 * s + i * 22 * s), t, font=fn, fill=(110, 114, 122))
        frames = max(1, int(round(seconds * FPS)))
        self._write(img, frames)
        self.substeps.append(dict(label=label, caption=heading, start_frame=start, end_frame=self.n - 1,
                                  card=True))

    def _write(self, img: Image.Image, n: int):
        """Write a finished frame (already with its text) n times, to the MP4s and the GIF."""
        if scene.PREVIEW:
            self.preview.append(img)
            self.n += n
            return
        buf = np.asarray(img.convert("RGB")).tobytes()
        for proc in (self.mp4, self.mp4_text):
            if proc is not None:
                for _ in range(n):
                    proc.stdin.write(buf)
        if self.gif:
            small = img.resize(scene.GIF_SIZE, Image.LANCZOS)
            for i in range(n):
                k = self.n + i
                if math.floor(math.ceil(k * scene.GIF_FPS / FPS) * FPS / scene.GIF_FPS) == k:
                    self.gif_frames.append(small)
        self.n += n


def _wrap(d, text, f, maxw):
    words, cur, out = text.split(), "", []
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) > maxw and cur:
            out.append(cur)
            cur = w
        else:
            cur = t
    if cur:
        out.append(cur)
    return out


# ================================================================================================= output
def join(name: str, parts: list[str]) -> Path:
    """out/mp4/<name>.mp4 from the chapters out/mp4/<part>.mp4 (same size, rate and codec, so copied), and
    out/<name>.json with every chapter's sub-steps on the joined clock."""
    mp4 = OUT / "mp4"
    files = [mp4 / f"{p}.mp4" for p in parts]
    missing = [str(f) for f in files if not f.exists()]
    if missing:
        raise FileNotFoundError(f"chapters not rendered: {missing}")
    lst = mp4 / f"{name}.concat.txt"
    lst.write_text("".join(f"file '{f.name}'\n" for f in files))
    dst = mp4 / f"{name}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", str(dst)], check=True)
    lst.unlink()
    subs, off, fps = [], 0, None
    for p in parts:
        meta = json.loads((OUT / f"{p}.json").read_text())
        fps = meta["fps"]
        for s in meta["substeps"]:
            subs.append(dict(s, chapter=p, start_frame=s["start_frame"] + off, end_frame=s["end_frame"] + off))
        off += meta["n_frames"]
    (OUT / f"{name}.json").write_text(json.dumps(dict(name=name, fps=fps, n_frames=off, chapters=parts,
                                                      substeps=subs), indent=1, ensure_ascii=False) + "\n")
    return dst


def contact_sheet(name: str, cols: int = 4, width: int = 480) -> Path:
    """out/<name>_steps.jpg: the last frame of every sub-step of out/mp4/<name>.mp4, numbered, for review."""
    meta = json.loads((OUT / f"{name}.json").read_text())
    fps = meta["fps"]
    tiles = []
    for s in meta["substeps"]:
        if s.get("card"):
            continue
        t = max(0.0, (s["end_frame"] - 1) / fps)
        r = subprocess.run(["ffmpeg", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", str(OUT / "mp4" / f"{name}.mp4"),
                            "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
        if r.returncode or not r.stdout:
            continue
        import io
        tiles.append(Image.open(io.BytesIO(r.stdout)).convert("RGB"))
    if not tiles:
        raise RuntimeError("no frames")
    h = int(width * tiles[0].height / tiles[0].width)
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * width, rows * h), "white")
    for i, im in enumerate(tiles):
        sheet.paste(im.resize((width, h), Image.LANCZOS), ((i % cols) * width, (i // cols) * h))
    dst = OUT / f"{name}_steps.jpg"
    sheet.save(dst, quality=82, optimize=True)
    return dst


def preview_gif(name: str, seconds: float = 24.0, width: int = 640, fps: int = 8) -> Path:
    """out/<name>_preview.gif: `seconds` of the video, sampled evenly over its whole length (a fast-forward)."""
    src = OUT / "mp4" / f"{name}.mp4"
    meta = json.loads((OUT / f"{name}.json").read_text())
    dur = meta["n_frames"] / meta["fps"]
    speed = max(1.0, dur / seconds)
    tmp = OUT / f"{name}_preview.tmp.gif"
    dst = OUT / f"{name}_preview.gif"
    vf = (f"setpts=PTS/{speed:.4f},fps={fps},scale={width}:-1:flags=lanczos,split[a][b];"
          f"[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", vf, str(tmp)], check=True)
    subprocess.run(["gifsicle", "-O3", "--lossy=60", str(tmp), "-o", str(dst)], check=True)
    tmp.unlink()
    return dst
