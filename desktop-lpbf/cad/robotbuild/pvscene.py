"""A small scene adapter over a pyvista Plotter: the part of byu-vcl PR 318's ``scene.Scene`` (commit 9740ba8,
``vertical-lab/scene.py``) that ``people.Person`` uses, so the MakeHuman person can be drawn into any robotbuild chapter.

Actors are grouped; a group has a 4x4 matrix (``gmat``) and may have a parent group (``parent``), and ``apply()`` pushes
each group's world matrix (``world(group)``) and each actor's visibility and opacity (``alpha`` times ``base_alpha``) to
VTK, sending only what changed since the last call. ``set_mesh`` points an actor's mapper back at a PolyData that the
caller edits in place (the person re-skins its meshes every frame).

    import common, pvscene, people
    pl = common.plotter()                      # 1280 x 720, the shared background and lights
    sc = pvscene.PVScene(pl)
    sc.add("can", pv.Cylinder(radius=33, height=122), "#c8102e", group="can")   # any other mesh, in a group
    p = people.Person(sc, "op")                # 1.75 m, work shirt, safety glasses
    p.set(x=0, y=0, hd=90, amp=1.0, phase=0.4) # stand or walk (phase += 2 pi per people.Person.STRIDE mm walked)
    img = sc.render([(4000, -3000, 2500), (0, 0, 900), (0, 0, 1)])           # apply() + camera + screenshot

Meshes added straight to ``pl`` (not through ``add``) are drawn as usual and never touched by ``apply``.
"""
from __future__ import annotations

import numpy as np
import pyvista as pv
import vtk

FEATURE_ANGLE = 35.0


def _wait_for_x(timeout=90.0):
    """Under load Xvfb can still be starting when xvfb-run hands over, and VTK then falls back to OSMesa (not installed)
    and the render dies at its first frame (byu-vcl PR 318's scene.py found and fixed this). Wait until the display
    accepts a connection."""
    import ctypes
    import os
    import time
    if not os.environ.get("DISPLAY"):
        return
    try:
        x11 = ctypes.cdll.LoadLibrary("libX11.so.6")
    except OSError:
        return
    x11.XOpenDisplay.restype = ctypes.c_void_p
    t0 = time.time()
    while time.time() - t0 < timeout:
        d = x11.XOpenDisplay(None)
        if d:
            x11.XCloseDisplay(ctypes.c_void_p(d))
            return
        time.sleep(0.5)


def plotter(size=None):
    """common.plotter(), made safe on a loaded runner: wait for the X display, and if VTK still came up without an X
    window (an OSMesa window while DISPLAY is set), close it and try again (PR 318's _plotter)."""
    import os
    import time
    import common
    size = size or (common.W, common.H)
    _wait_for_x()
    pl = None
    for attempt in range(40):
        pl = common.plotter(size)
        if not os.environ.get("DISPLAY") or pl.render_window.GetClassName() != "vtkOSOpenGLRenderWindow":
            if attempt:
                print(f"pvscene: an X window on try {attempt + 1}", flush=True)
            return pl
        pl.close()
        time.sleep(0.5 + 0.25 * min(attempt, 8))
    return pl


def surface_style(shininess: float) -> dict:
    """specular and specular_power for a material's 0-1 shininess (PR 318's curve: paint and cloth close to matte)."""
    s = min(max(float(shininess), 0.0), 1.0)
    return dict(specular=0.30 * s * s, specular_power=12.0 + 68.0 * s)


class PVScene:
    def __init__(self, pl: pv.Plotter | None = None, size=None):
        if pl is None:
            pl = plotter(size)
        self.pl = pl
        self.actors: dict[str, vtk.vtkActor] = {}
        self.group_of: dict[str, str] = {}
        self.parent: dict[str, str] = {}
        self.gmat: dict[str, np.ndarray] = {}
        self.alpha: dict[str, float] = {}
        self.base_alpha: dict[str, float] = {}
        self.color: dict[str, tuple] = {}
        self._keep: dict = {}
        self._mats: dict = {}
        self._sent: dict = {}
        self.view_angle = 30.0

    # ------------------------------------------------------------------------------------------- actors
    def add(self, name, poly, color, group="static", opacity=1.0, shown=True, **kw):
        if poly is None:
            return None
        style = dict(smooth_shading=True, split_sharp_edges=True, feature_angle=FEATURE_ANGLE, ambient=0.22,
                     diffuse=0.80)
        style.update(surface_style(kw.pop("specular", 0.35)))
        style.update(kw)
        if name in self.actors:
            self.remove(name)
        actor = self.pl.add_mesh(poly, color=color, opacity=opacity, **style)
        self.actors[name] = actor
        self._hold(name, actor)
        self.group_of[name] = group
        self.base_alpha[name] = opacity
        self.alpha[name] = 1.0 if shown else 0.0
        self.gmat.setdefault(group, np.eye(4))
        return actor

    def set_mesh(self, name, poly):
        """Draw `poly` itself (not the copy add_mesh made for smooth shading), so edits to it in place show."""
        self.actors[name].GetMapper().SetInputData(poly)
        self._hold(name, self.actors[name])

    def remove(self, name):
        a = self.actors.pop(name, None)
        if a is not None:
            self.pl.remove_actor(a, render=False)
        for d in (self.group_of, self.alpha, self.base_alpha, self.color, self._keep, self._sent):
            d.pop(name, None)

    def _hold(self, name, actor):
        """Keep the Python wrappers of an actor's property, mapper and mesh alive (PR 318: dropped temporary wrappers
        cost VTK a walk of its ghost map on every later call)."""
        m = actor.GetMapper()
        self._keep[name] = (actor.GetProperty(), m, m.GetInput() if m is not None else None)
        return self._keep[name]

    def members(self, group):
        return [n for n, g in self.group_of.items() if g == group]

    def show(self, names, a=1.0):
        for n in names:
            self.alpha[n] = a

    # ------------------------------------------------------------------------------------------- frames
    def world(self, group: str) -> np.ndarray:
        m = self.gmat.get(group, np.eye(4))
        g = group
        while g in self.parent:
            g = self.parent[g]
            m = self.gmat.get(g, np.eye(4)) @ m
        return m

    def apply(self):
        """Each group's world matrix and each actor's visibility, opacity and colour onto VTK (only what changed)."""
        cache = {}
        for name, actor in self.actors.items():
            g = self.group_of[name]
            vm = cache.get(g)
            if vm is None:
                w = self.world(g)
                key = w.tobytes()
                prev = self._mats.get(g)
                if prev is None or prev[0] != key:
                    vm = vtk.vtkMatrix4x4()
                    vm.DeepCopy(np.asarray(w, float).ravel().tolist())
                    self._mats[g] = (key, vm)
                else:
                    vm = prev[1]
                cache[g] = vm
            a = self.alpha[name]
            vis = a > 0.02
            opac = min(1.0, self.base_alpha[name] * a)
            col = self.color.get(name)
            col = tuple(float(c) for c in col) if col is not None else None
            prop = self._keep.get(name, self._hold(name, actor))[0]
            rec = self._sent.get(name)
            if rec is not None and rec[0] is vm and rec[1] == vis and rec[2] == opac and rec[3] == col:
                continue
            actor.SetUserMatrix(vm)
            actor.SetVisibility(vis)
            prop.SetOpacity(opac)
            if col is not None:
                prop.SetColor(*col)
            self._sent[name] = (vm, vis, opac, col)

    def camera(self, cam, view_angle=None):
        """cam: [position, focal point, view up] (mm)."""
        if view_angle is not None:
            self.view_angle = view_angle
        self.pl.camera_position = [tuple(float(v) for v in c) for c in cam]
        self.pl.camera.view_angle = float(self.view_angle)
        self.pl.renderer.ResetCameraClippingRange()

    def render(self, cam=None, view_angle=None) -> np.ndarray:
        """apply(), the camera (if given), render; the frame as an H x W x 3 uint8 array."""
        self.apply()
        if cam is not None:
            self.camera(cam, view_angle)
        self.pl.render()
        return np.asarray(self.pl.screenshot(return_img=True))[:, :, :3]
