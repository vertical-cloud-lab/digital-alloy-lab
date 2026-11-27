"""The fast-track video, chapter by chapter: which parts come in, in what order, along which checked path, under which fixed
camera, with the calendar (scenario A of ft_progression.py), the running spend (parts.csv, as ft_progression.spend()
counts it) and the captions.

    build(n) -> engine.Timeline for chapter n (0-7)
"""
from __future__ import annotations

import csv
import math

import numpy as np

import engine as E
import scan as SC
import scene as S

M = S.model()
P = M.P
FAR = 1500.0
LEFT_PARK, RIGHT_PARK = S.parks()
HX0 = P["rc_travel"] / 2                          # the model draws the hopper here (hx=None)
LAYER = 0.030                                     # mm, fast_track.LAYER_UM
SPREAD_V = 10.0                                   # mm/s: Heriot-Watt's recoater (Bidare et al. 2017, the study's 3.3)
RETURN_V = 40.0                                   # mm/s: the return stroke (estimate; X-LSQ075B tops out at 280 mm/s)
PISTON_V = 10.0                                   # mm/s: plate moves other than the layer step (X-VSR20A max 48 mm/s)
OPTICS_V = 5.0                                    # mm/s: sliding the cross-beam up by hand (estimate)

# ------------------------------------------------------------------------------------------------ cameras (fixed tripods)
C = E.Cam
CAMS = dict(
    room=C((-2900, -3700, 1050), (-150, 80, -560), 34, name="room"),
    bench=C((-1900, -2450, 900), (-140, 60, -120), 30, name="bench"),
    wide=C((-1500, -2100, 1250), (-160, 40, 20), 30, name="wide"),
    core=C((-1180, -1480, 930), (-50, 40, 60), 30, name="core"),
    optics=C((-760, -1000, 760), (-60, 20, 230), 30, name="optics"),
    target=C((-330, -560, 330), (0, 0, 0), 26, name="target"),
    box=C((-980, -1330, 640), (-40, 40, 20), 30, name="box"),
    well=C((-150, -400, 175), (5, 5, -6), 24, name="well"),
    lowwell=C((-120, -430, 60), (5, 10, -22), 22, name="lowwell"),
    under=C((-700, -1050, -60), (0, 40, -110), 30, name="under"),
    cube=C((-1350, -1850, 1050), (-60, 40, 80), 30, name="cube"),
)


# ------------------------------------------------------------------------------------------------ schedule and spend
_SCHED = {}


def sched(task):
    if not _SCHED:
        import ft_progression as FP
        res = FP.run()
        scn = [k for k in res if k.startswith("A:")][0]
        _SCHED.update({k: (v[2], v[3]) for k, v in res[scn][1].items()})
        _SCHED["_scenario"] = scn
    lo, hi = _SCHED[task]
    return lo, hi


def line_costs():
    """{(state, id): (low, high, item)} counted as ft_progression.spend() counts them; the block's two heaters as H1b."""
    import ft_progression as FP
    rows = {r["id"]: r for r in csv.DictReader(open(FP.HERE.parent / "parts.csv"))}
    out = {}
    for st, ids in FP.FIRST_STATE.items():
        for i in ids:
            r = rows.get(i)
            if r is None:
                continue
            q = float(r["FT1V"] if st == "FT-1V" else r["FT1"] if st == "FT-1" else r["FT0"] or 0) or float(r["FT1"] or 0)
            if i == "H1":
                q = 2.0
            if i == "F2b":
                lo = float(r["unit_low"]) - float(rows["F2a"]["unit_low"])
                hi = float(r["unit_high"]) - float(rows["F2a"]["unit_high"])
            elif i == "F2c":
                lo = float(r["unit_low"]) - float(rows["F2b"]["unit_low"])
                hi = float(r["unit_high"]) - float(rows["F2b"]["unit_high"])
            else:
                lo, hi = q * float(r["unit_low"]), q * float(r["unit_high"])
            out[(st, i)] = (lo, hi, r["item"])
        if st == "FT-1":
            out[("FT-1", "H1b")] = (2 * float(rows["H1"]["unit_low"]), 2 * float(rows["H1"]["unit_high"]),
                                    "two more heaters, for the well block")
    return out


def cumulative():
    import ft_progression as FP
    return {r["state"]: (r["cumulative_low"], r["cumulative_high"]) for r in FP.spend()}


STATE_BEFORE = {"S1": None, "S2": "S1", "FT-0": "S2", "FT-1": "FT-0", "FT-1V": "FT-1"}


class Book:
    """The running spend: each parts.csv line is counted when its first part goes in (or at a named moment)."""

    def __init__(self, tl, state, bought=False):
        self.tl, self.state = tl, state
        cum = cumulative()
        prev = state if bought else STATE_BEFORE.get(state)
        self.lo, self.hi = cum[prev] if prev else (0.0, 0.0)
        self.bought = bought
        self.costs = line_costs()
        self.done = set()
        self.recent = []
        tl.overlay("spend", (self.lo, self.hi, list(self.recent)), 0.0)

    def buy(self, *ids, state=None):
        st = state or self.state
        for i in ids:
            k = (st, i)
            if k in self.done or k not in self.costs:
                continue
            lo, hi, item = self.costs[k]
            self.lo += lo
            self.hi += hi
            self.done.add(k)
            self.recent = (self.recent + [(i if i != "H1b" else "H1", item, lo, hi)])[-5:]
        self.tl.overlay("spend", (self.lo, self.hi, list(self.recent)))

    def close(self):
        """Count anything of this state not yet counted, and check the total against ft_progression.spend()."""
        if self.bought:
            return []
        rest = [i for (st, i) in self.costs if st == self.state and (st, i) not in self.done]
        if rest:
            self.buy(*rest)
        lo, hi = cumulative()[self.state]
        assert abs(self.lo - lo) < 2 and abs(self.hi - hi) < 2, (self.state, self.lo, lo, self.hi, hi)
        return rest


# ------------------------------------------------------------------------------------------------ actors of a chapter
def same(a, b):
    return len(a["F"]) == len(b["F"]) and np.allclose(a["V"].min(0), b["V"].min(0), atol=0.01) and \
        np.allclose(a["V"].max(0), b["V"].max(0), atol=0.01)


def actors_for(a_state, b_state, room=True, person=None):
    """Actors of a chapter going from a_state to b_state: the start state's parts ('A|name'), and the target's parts that
    are new or drawn elsewhere ('B|name'). Returns (actors, present, A, B) with A/B: model name -> actor key."""
    acts, present, A, B = {}, set(), {}, {}
    ma = S.state_meshes(a_state) if a_state else {}
    mb = S.state_meshes(b_state) if b_state else {}
    if not a_state:                                     # the empty bench: only the bench top is there
        ma = {k: v for k, v in mb.items() if k == "Bench top"}
    for n, d in ma.items():
        k = f"A|{n}"
        acts[k] = E.Actor(k, d["V"], d["F"], d["color"], d["opacity"], d["pid"], group=d["group"], label=n)
        present.add(k)
        A[n] = k
    for n, d in mb.items():
        if n in ma and same(ma[n], d):
            B[n] = A[n]
            continue
        k = f"B|{n}"
        acts[k] = E.Actor(k, d["V"], d["F"], d["color"], d["opacity"], d["pid"], group=d["group"], label=n)
        B[n] = k
    for k, a in acts.items():
        if "lift column" in a.label:
            a.group = "column"
    if room:
        for n, d in S.room().items():
            acts[n] = E.Actor(n, d["V"], d["F"], d["color"], 1.0, "", kind="room", edges=False, label=n)
            present.add(n)
    if person is not None:
        for (n, V, F, col) in S.person_meshes(person):
            acts[n] = E.Actor(n, V, F, col, 1.0, "", kind="person", edges=False, label="person for scale")
            present.add(n)
    return acts, present, A, B


def components(V, F):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    key = np.round(V * 1000.0).astype(np.int64)
    _, first, inv = np.unique(key, axis=0, return_index=True, return_inverse=True)
    inv = inv.ravel()
    Fw = inv[F]
    e = np.r_[Fw[:, [0, 1]], Fw[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(first), len(first)))
    nc, lab = connected_components(g, directed=False)
    return lab[Fw[:, 0]]                                         # component of each triangle


def split_part(s, name, side):
    """Split a model part drawn as one mesh (the cube's six KF-25 ports) into the pieces that go on with different plates:
    side(centroid) -> tag. New actors 'B|name [tag]' keep the model name as their label."""
    tl = s.tl
    k = s.Bm[name]
    a = tl.actors.pop(k)
    comp = components(a.V, a.F)
    tags = {}
    for c in np.unique(comp):
        tri = a.F[comp == c]
        cen = a.V[np.unique(tri)].mean(0)
        tags.setdefault(side(cen), []).append(tri)
    out = {}
    for tag, tris in tags.items():
        tri = np.vstack(tris)
        used, inv = np.unique(tri, return_inverse=True)
        kk = f"B|{name} [{tag}]"
        tl.actors[kk] = E.Actor(kk, a.V[used], inv.reshape(-1, 3).astype(np.int32), a.color, a.opacity, a.pid,
                                group=a.group, label=name)
        out[tag] = kk
    s.Bm.pop(name)
    for tag, kk in out.items():
        s.Bm[f"{name} [{tag}]"] = kk
    return out


class Story:
    def __init__(self, num, title, a, b, state_title=None, person=None):
        acts, present, self.Am, self.Bm = actors_for(a, b, person=person)
        self.tl = E.Timeline(num, title, acts, present)
        self.a, self.b = a, b
        self.tl.overlay("chapter", (num, title), 0.0)
        self.tl.overlay("state", state_title or (M.TITLES[b] if b else ""), 0.0)
        self.book = Book(self.tl, b, bought=(a == b)) if b else None

    def A(self, *subs):
        return [k for n, k in self.Am.items() if any(s in n for s in subs)]

    def B(self, *subs, new=True):
        out = [k for n, k in self.Bm.items() if any(s in n for s in subs)]
        return [k for k in out if (k.startswith("B|") or not new)]

    def cal(self, task, note=""):
        lo, hi = sched(task)
        self.tl.overlay("calendar", (task, lo, hi, note))

    def speed(self, text):
        self.tl.overlay("speed", text)

    def unplaced(self):
        """Target parts that no event has put in yet (B keys never inserted)."""
        done = set()
        for nt in self.tl.notes:
            done |= set(nt.get("names", ()))
        return [k for k in set(self.Bm.values()) if k.startswith("B|") and k not in done]


def verify_end(story):
    """At the chapter's end the drawn scene must be the target state: every target part drawn where the model puts it, and
    nothing else from the model drawn. Returns a list of problems."""
    tl = story.tl
    st = tl.state(tl.t + 1e-3)
    tgt = S.state_meshes(story.b)
    probs = []
    drawn = {}
    for k, a in tl.actors.items():
        if a.kind != "part":
            continue
        s = st[k]
        if not s["vis"]:
            continue
        o = s["off"] + s["stage"]
        V = s["morph"][1] if "morph" in s else a.V
        lab = a.label
        if lab in drawn and " [" in k and any(" [" in x[2] for x in drawn[lab]):
            l0, h0, k0 = drawn[lab][-1]
            drawn[lab][-1] = (np.minimum(l0, V.min(0) + o), np.maximum(h0, V.max(0) + o), k0)
            continue
        drawn.setdefault(lab, []).append((V.min(0) + o, V.max(0) + o, k))
    for n, d in tgt.items():
        lo, hi = d["V"].min(0), d["V"].max(0)
        tol = np.array([0.6, 0.6, 0.6])
        if d["group"] == "recoater":
            tol[0] = P["rc_travel"]
        if d["group"] == "piston" or "lift column" in n:
            tol[2] = abs(P["pz_bot"]) + P["pz_top"]
        if not any(np.all(np.abs(lo - l2) <= tol) and np.all(np.abs(hi - h2) <= tol + (tol[2] if "lift column" in n else 0))
                   for (l2, h2, _) in drawn.get(n, [])):
            probs.append(f"missing or misplaced: {n} (drawn: {[(np.round(l2, 1).tolist(), k) for l2, h2, k in drawn.get(n, [])][:2]})")
    for n, lst in drawn.items():
        if n not in tgt:
            probs.append(f"drawn but not in {story.b}: {n}")
        elif len(lst) > 1:
            probs.append(f"drawn twice: {n}")
    return probs


# ------------------------------------------------------------------------------------------------ effects
def fx_lines(name, segs, color, width=3.0):
    return dict(kind="lines", data=np.asarray(segs, np.float32).reshape(-1, 2, 3), color=color, width=width, solid=False)


def disc(r, z0, z1, n=72, x_max=None):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    xy = np.c_[r * np.cos(a), r * np.sin(a)]
    if x_max is not None:
        xy[:, 0] = np.minimum(xy[:, 0], x_max)
    V = np.vstack([np.c_[xy, np.full(n, z0)], np.c_[xy, np.full(n, z1)], [[0, 0, z0], [0, 0, z1]]]).astype(np.float32)
    F = []
    for i in range(n):
        j = (i + 1) % n
        F += [[i, j, n + j], [i, n + j, n + i], [2 * n, j, i], [2 * n + 1, n + i, n + j]]
    return V, np.array(F, np.int32)


def boxes(bxs, z0, z1):
    Vs, Fs, k = [], [], 0
    for (x0, y0, x1, y1) in bxs:
        V, F = S._box(x0, x1, y0, y1, z0, z1)
        Vs.append(V)
        Fs.append(F + k)
        k += len(V)
    return np.vstack(Vs).astype(np.float32), np.vstack(Fs).astype(np.int32)


def beam_mesh(state):
    return S.tess(M.beam_cone(state, 0.0, P["lens_wd"]))


# ------------------------------------------------------------------------------------------------ shared moves
OPTICS = ("Gantry cross-beam", "Scan-head plate", "SCANLAB", "f-theta lens", "Collimator")
LID = ("Box lid", "Inner clamp ring", "Window ring", "Window, ", "Window retaining flange", "Cover-slide holder", "Cover slide,",
       "Continuous hinge")
_FIB = {}


def fibre_mesh(state, lift):
    """The process fibre as ft_model draws it with the head `lift` mm higher (its laser end stays put)."""
    key = (state, round(lift, 3))
    if key not in _FIB:
        old = P["lens_wd"]
        try:
            P["lens_wd"] = old + lift
            part = [p for p in M.build(state) if p.name == "Process fibre"][0]
        finally:
            P["lens_wd"] = old
        _FIB[key] = S.tess(part.shape)
    return _FIB[key]


def lid_group(s, which):
    return s.A(*LID) if which == "A" else [s.Bm[n] for n in s.Bm if any(x in n for x in LID)]


def tube_group(s, which="A", long=True):
    nm = "Beam tube, long" if long else "Beam tube, short"
    if which == "A":
        return s.A(nm, "Beam-tube interlock switch")
    return [s.Bm[n] for n in s.Bm if nm in n or "Beam-tube interlock switch" in n]


def free_rise(tl, tube, lens, hp):
    """How far the beam tube can slide up the lens: until its collar's floor ring meets the lens bottom, or its collar the
    head plate (from the drawn meshes, so a v2 collar changes it)."""
    T = tl.actors[tube].V
    Lv, H = tl.actors[lens].V, tl.actors[hp].V
    lens_r = float(np.hypot(Lv[:, 0], Lv[:, 1]).max())
    lens_bot = float(Lv[:, 2].min())
    r = np.hypot(T[:, 0], T[:, 1])
    below = T[(r < lens_r - 0.5) & (T[:, 2] <= lens_bot + 1e-6)]
    ring_top = float(below[:, 2].max()) if len(below) else -1e9
    return min(lens_bot - ring_top, float(H[:, 2].min()) - float(T[:, 2].max())) - 0.5


def access(s, tube_keys, lid_keys, body_keys, under=0.0):
    """What opening the box takes on this model: the lid's lift (its lowest part over the gasket), the tube's rise (its
    bottom over the lid's window stack once lifted, and over the rim by `under`, the tallest part that has to pass
    under the tube) and the optics' lift (what the tube's own travel up the lens lacks)."""
    tl = s.tl
    tube = [k for k in tube_keys if "Beam tube" in k][0]
    lens = [k for k in tl.actors if "f-theta lens" in k and tl.actors[k].label.startswith("f-theta")][0]
    hp = [k for k in tl.actors if "Scan-head plate" in k][0]
    zl = min(float(tl.actors[k].V[:, 2].min()) for k in lid_keys)
    zt = max(float(tl.actors[k].V[:, 2].max()) for k in lid_keys)
    zg = max(float(tl.actors[k].V[:, 2].max()) for k in body_keys)
    lift_lid = math.ceil(zg - zl + 1.0)
    zb = float(tl.actors[tube].V[:, 2].min())
    rise = math.ceil(max(zt + lift_lid + 2.0, zg + under + 2.5) - zb)
    fr = free_rise(tl, tube, lens, hp)
    lift_o = max(0, math.ceil(rise - fr))
    return dict(lift_lid=lift_lid, rise=rise, free_rise=round(fr, 1), lift_optics=lift_o)


def optics_move(s, state, dz_from, dz_to, verb, v=None):
    """Slide the gantry cross-beam with the head, lens and collimator; the fibre follows."""
    tl = s.tl
    keys = [k for k in tl.actors if k.startswith("A|") and any(x in k for x in OPTICS)]
    fib = [k for k in tl.actors if k.startswith("A|") and "Process fibre" in k]
    t0 = tl.t
    Pm = tl.move(keys, [(0, 0, 0), (0, 0, dz_to - dz_from)], v=v or OPTICS_V, a=20, verb=verb,
                 label=[("Gantry cross-beam with the head and lens", "E4, L3, L4, MK-09")])
    if fib:
        V0 = fibre_mesh(state, dz_from)[0]
        V1 = fibre_mesh(state, dz_to)[0]
        if len(V0) == len(tl.actors[fib[0]].V) == len(V1):
            tl.morph(fib[0], V1, t0, t0 + Pm.T, V0=V0)
        else:
            print(f"  ! fibre mesh changes topology with the head height: drawn rigid", flush=True)
            tl.move(fib, [(0, 0, 0), (0, 0, dz_to - dz_from)], v=v or OPTICS_V, overlay=False)
    return Pm


def open_box(s, tube, lid, body, state, under=0.0):
    tl = s.tl
    acc = access(s, tube, lid, body, under)
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    if acc["lift_optics"]:
        tl.caption("Optics up, tube up, lid off", f"the beam tube is captive: head and lens slide up {acc['lift_optics']} mm")
        optics_move(s, state, 0.0, acc["lift_optics"], "sliding up")
    else:
        tl.caption("Tube up, lid off", f"the beam tube slides up the lens {acc['rise']} mm")
    tl.move(tube, [(0, 0, 0), (0, 0, acc["rise"])], v=30, verb="sliding up",
            label=[("Beam tube and its interlock switch", "MK-10, S1")])
    tl.remove(lid, way=[(0, 0, 0), (0, 0, acc["lift_lid"]), (0, -FAR, acc["lift_lid"])], verb="lifting off",
              label=[("Box lid with the window stack", "E1, MK-02, L8")])
    return acc


def close_box(s, lid, tube, acc, state):
    tl = s.tl
    tl.caption("Lid on, tube down", "the window stack rides on the lid; the tube sits on its flange")
    tl.insert(lid, way=[(0, -FAR, acc["lift_lid"]), (0, 0, acc["lift_lid"]), (0, 0, 0)],
              label=[("Box lid with the window stack", "E1, MK-02, L8")])
    tl.move(tube, [(0, 0, 0), (0, 0, -acc["rise"])], v=30, verb="sliding down", label=[("Beam tube onto the flange", "MK-10")])
    if acc["lift_optics"]:
        tl.caption("Optics back to the lens height", "then refocus: the focus ladder again")
        optics_move(s, state, acc["lift_optics"], 0.0, "sliding down")


def place_rest(s, prefs=None):
    """Any part of the target state the script has not placed (a v2 addition, say) comes in on a planned path."""
    tl = s.tl
    rest = sorted(s.unplaced())
    for k in rest:
        try:
            tl.insert([k], prefs=prefs)
        except RuntimeError as e:
            tl.notes.append(dict(t=round(tl.t, 2), names=[k], collision=f"no clear path: {e}"))
            print(f"  ! no clear path for {k}", flush=True)
    return rest


# ================================================================================================ chapter 0
def ch0():
    s = Story(0, "The bench and the room", None, "S1", state_title="Day 0: nothing has arrived",
              person=(1000.0, -260.0, S.floor_z()))
    tl, b = s.tl, s.book
    tl.overlay("spend", (0.0, 0.0, []), 0.0)
    tl.overlay("calendar", ("orders out", 0, 0, "every order goes out on day 0"), 0.0)
    tl.shot(CAMS["room"])
    tl.caption("An empty lab bench", "1.46 x 0.79 m top, 0.9 m high; the person is 1.75 m")
    s.speed("")
    tl.wait(8.0)
    tl.shot(CAMS["bench"])
    tl.caption("Day 0: every order out", "laser chain, stock, box, stages on PCards, cube on a PO")
    orders = ["used optics chain arrives", "McMaster stock and hardware", "PC + RTC5 software", "enclosure arrives",
              "stages arrive", "cube frame and plates arrive (PO)", "LSO registration and SOP", "EHS review (Al powder)"]
    tl.overlay("orders", [(o, *sched(o)) for o in orders])
    tl.wait(9.0)
    tl.end()
    return s


# ================================================================================================ chapter 1: S1
def ch1():
    s = Story(1, "S1: optics on the frame", None, "S1")
    tl, b = s.tl, s.book
    tl.shot(CAMS["wide"])
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    s.cal("McMaster stock and hardware", "T-slot frame")
    tl.caption("The T-slot frame", "30 mm extrusion: base, support rails, gantry")
    tl.insert(s.B("T-slot base and support rails"), prefs=["down"])
    b.buy("E4")
    tl.insert(s.B("Gantry uprights"), prefs=["down"])
    tl.insert(s.B("Gantry cross-beam"), prefs=["down", "front"])
    s.cal("deck plate and target stand made", "made parts MK-01, MK-18")
    tl.caption("Deck plate on the rails", "250 x 250 x 10 mm 6061: the cassette from day 0")
    tl.insert(s.B("Deck plate"), prefs=["down", "front-down"])
    s.cal("PC + RTC5 software")
    tl.caption("PC with the RTC5 card", "used RTC5 PCIe, tested with an IPG YLR")
    tl.insert(s.B("PC with the RTC5"), prefs=["down", "right"])
    b.buy("C1", "L5", "L7")
    s.cal("S1 optics bench assembled", "used optics chain in: day " + "%d-%d" % sched("used optics chain arrives"))
    tl.shot(CAMS["optics"])
    tl.caption("The scan head goes on", "used hurrySCAN 25 on a 12 mm head plate")
    tl.insert(s.B("Scan-head plate"), prefs=["front", "front-down", "down"])
    tl.insert(s.B("SCANLAB hurrySCAN 25"), prefs=["down", "front-down"])
    b.buy("L3", "L10")
    tl.insert(s.B("f-theta lens"), prefs=["front-up", "down"])
    b.buy("L4")
    tl.insert(s.B("Collimator"), prefs=["left", "down", "front-down", "left-down"])
    b.buy("L2")
    tl.insert(s.B("+-15 V supply"), prefs=["front", "right", "down", "front-down"])
    b.buy("L6")
    tl.shot(CAMS["wide"])
    tl.caption("Laser and fibre on the bench", "used IPG YLR-400-SM, 400 W CW, 1070 nm")
    tl.insert(s.B("IPG YLR-400", "Process fibre"), prefs=["down", "left-down", "front-down"])
    b.buy("L1")
    s.cal("deck plate and target stand made", "MK-18")
    tl.shot(CAMS["target"])
    tl.caption("Target at the powder plane", "anodised 6061, 80 x 80 x 3 mm, on its stand")
    tl.insert(s.B("Guide-laser target stand", "Anodised target"), prefs=["front-down", "left-down", "right-down"])
    # the guide-laser check: a 5 mm grid over the 40 mm field, traced at 100 mm/s (a test pattern)
    s.cal("S1 guide-laser and scanner checks", "LSO registration gates the late end")
    b.buy("S2")
    tl.caption("Guide laser on the target", "field size and distortion at the powder plane")
    s.speed("real time (guide laser at 100 mm/s)")
    pts = []
    for k, y in enumerate(np.arange(-20, 20.1, 5.0)):
        xs = (-20.0, 20.0) if k % 2 == 0 else (20.0, -20.0)
        pts += [(xs[0], y), (xs[1], y)]
    pts = [p for p in pts if math.hypot(*p) <= 20.01 or True]
    path = E.Path([(x, y, 0.0) for x, y in pts], [100.0] * (len(pts) - 1), [2000.0] * (len(pts) - 1), pause=0.0)
    t0 = tl.t + 0.5
    zl = P["lens_wd"]

    def guide(st, t, path=path, t0=t0):
        if t < t0:
            return
        q = path.at(t - t0)
        done = []
        for (ta, tb, a, bb, L, sfn) in path.legs:
            if t - t0 >= tb:
                done.append((a, bb))
            elif t - t0 >= ta:
                done.append((a, q))
                break
        z = 0.05
        st["_fx"]["guide trace"] = fx_lines("guide trace", [((a[0], a[1], z), (c[0], c[1], z)) for a, c in done],
                                            "#ff3b30", 2.0)
        if t - t0 <= path.T + 0.5:
            st["_fx"]["guide beam"] = fx_lines("guide beam", [((0, 0, zl), (q[0], q[1], z))], "#ff2d2d", 2.0)
            V, F = disc(0.9, z, z + 0.05)
            st["_fx"]["guide spot"] = dict(kind="mesh", data=(V + np.array([q[0], q[1], 0], np.float32), F),
                                           color="#ff1a1a", opacity=1.0, solid=False, key=f"spot{q[0]:.2f},{q[1]:.2f}")
    tl.fx(guide, t0)
    tl.wait(0.5 + path.T + 1.5)
    tl.caption("S1 done: the optics answer", "head and RTC5 talk; field measured")
    tl.wait(3.0)
    b.close()
    tl.end()
    return s


# ================================================================================================ chapter 2: S2
def ch2():
    s = Story(2, "S2: the box closed round the beam", "S1", "S2")
    tl, b = s.tl, s.book
    tl.shot(CAMS["core"])
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    s.cal("enclosure arrives", "the box arrives; the target makes way")
    tl.caption("Target and deck off the rails", "the box goes on the rails where the deck was")
    tl.remove(s.A("Guide-laser target stand", "Anodised target"), prefs=["front-down", "left-down", "right-down"])
    tl.remove(s.A("Deck plate"), prefs=["front-down", "front", "down"])
    s.cal("box cut and fitted", "window bore, bulkheads, glands, rod hole")
    tl.caption("The 304 NEMA 4X box", "16 x 12 x 8 in., 14 ga, cut for everything FT-1 needs")
    body = s.B("304 NEMA 4X box", "Lid gasket", "Lid clamps")
    tl.insert(body, prefs=["front-down", "down"])
    b.buy("E1")
    tl.caption("Deck plate into the box", "the same plate, now on the box floor")
    tl.insert(s.B("Deck plate"), prefs=["front-down", "front-step"])
    s.cal("window, cover slides, beam dump (Edmund, Thorlabs)")
    tl.caption("A 500 W water-cooled dump", "for calorimetry of the used laser")
    tl.insert(s.B("Water-cooled beam dump", "Dump water lines"), prefs=["front-down", "front-step"])
    b.buy("L9")
    s.cal("window stack and beam tube made", "MK-02, MK-10")
    tube, lid = tube_group(s, "B", long=True), lid_group(s, "B")
    acc = access(s, tube, lid, body)
    tl.overlay("access", acc)
    tl.shot(CAMS["box"])
    if acc["lift_optics"]:
        tl.caption("Optics up to fit the tube", f"its collar slides only {acc['free_rise']:.0f} mm up the lens")
        optics_move(s, "S2", 0.0, acc["lift_optics"], "sliding up")
    tl.caption("Beam tube onto the lens", "it waits up the lens while the lid goes on")
    lo = -(float(tl.actors[tube[0]].V[:, 2].max()) - (float(tl.actors[[k for k in tl.actors if 'f-theta' in k][0]].V[:, 2].min())
                                                      + acc["lift_optics"]) + 2.0)
    tl.insert(tube, way=[(0, -FAR, lo), (0, 0, lo), (0, 0, acc["rise"])],
              label=[("Beam tube, long, with lens collar", "MK-10"), ("Beam-tube interlock switch", "S1")])
    tl.caption("Lid with the window stack", "fused silica window, cover slide below it")
    tl.insert(lid, way=[(0, -FAR, acc["lift_lid"]), (0, 0, acc["lift_lid"]), (0, 0, 0)],
              label=[("Box lid with the window stack", "E1, MK-02, L8")])
    b.buy("L8")
    tl.move(tube, [(0, 0, 0), (0, 0, -acc["rise"])], v=30, verb="sliding down", label=[("Beam tube onto the flange", "MK-10")])
    if acc["lift_optics"]:
        tl.caption("Optics back to the lens height", "the focus is set again in the full-power check")
        optics_move(s, "S2", acc["lift_optics"], 0.0, "sliding down")
    s.cal("S2 interlocks wired and proven")
    tl.shot(CAMS["core"])
    tl.caption("Interlocks", "coded lid switches, E-stop, key switch, lamp")
    tl.insert(s.B("Coded lid switches"), prefs=["front", "front-down", "down"], gap=-2.5)
    tl.insert(s.B("Safety relay box", "E-stop", "Key switch"), prefs=["down", "front-down"], gap=-2.5)
    tl.insert(s.B("Emission lamp"), prefs=["down", "back-down"])
    b.buy("S1")
    place_rest(s)
    tl.shot(CAMS["box"])
    s.cal("S2 FULL POWER INTO THE DUMP", "inside the laser's return window")
    tl.caption("Full power into the dump", "400 W CW in a closed Class 1 box")
    s.speed("real time")
    t0 = tl.t + 1.0
    tl.paint(s.B("Emission lamp", new=False)[0], "#ff2020", t0, t0 + 9.0)
    bm = beam_mesh("S2")

    def beam(st, t, t0=t0, bm=bm):
        if t0 <= t < t0 + 9.0:
            st["_fx"]["beam"] = dict(kind="mesh", data=bm, color="#ff2a2a", opacity=0.45, solid=False, key="beamS2")
    tl.fx(beam, t0, t0 + 9.0)
    tl.overlay("panel", ["Calorimetry: flow x heat capacity x rise", "checks the used laser to a few %",
                         "focus ladder on anodised Al next"], t0, t0 + 9.5)
    tl.wait(10.5)
    tl.caption("S2 done: power and spot", "the laser makes its power, inside its return window")
    tl.wait(3.0)
    b.close()
    tl.end()
    return s


# ================================================================================================ chapter 3: FT-0
def ch3():
    s = Story(3, "FT-0: single tracks", "S2", "FT-0")
    tl, b = s.tl, s.book
    tl.shot(CAMS["core"])
    s.cal("FT-0 assembled in the box", "FT-0 parts made: day %d-%d" % sched("FT-0 parts made"))
    tube, lid = tube_group(s, "A"), lid_group(s, "A")
    body = s.A("304 NEMA 4X box", "Lid gasket", "Lid clamps")
    hb = max(float(np.ptp(d["V"][:, 2])) for n, d in S.state_meshes("FT-0").items() if n.startswith("Well block"))
    acc = open_box(s, tube, lid, body, "S2", under=hb)
    tl.overlay("access", acc)
    tl.caption("The dump comes out", "slid out from under the tube, then lifted")
    zr = max(float(tl.actors[k].V[:, 2].max()) for k in body)
    dump = s.A("Water-cooled beam dump", "Dump water lines")
    hd = math.ceil(zr + 1.5 - min(float(tl.actors[k].V[:, 2].min()) for k in dump))
    tl.remove(dump, way=[(0, 0, 0), (-100, 0, 0), (-100, 0, hd), (-100, -FAR, hd)])
    tl.shot(CAMS["box"])
    tl.caption("The well block on Macor", "80 x 80 x 40 mm 6061, a 40.00 mm bore")
    tl.insert(s.B("Rod gland plate"), prefs=["front-up", "left", "right", "front"])
    tl.insert(s.B("Macor standoffs"), prefs=["front-down", "front-step"])
    b.buy("H4")
    tl.insert(s.B("Well block"), prefs=["front-down", "front-step"])
    b.buy("F1", "F2a")
    tl.insert(s.B("FT-0 rod collar"), prefs=["front-down", "front-step"])
    tl.caption("The plate on its rod", "heater plate, substrate, rope wiper; leads down the rod")
    stack = s.B("Substrate disc", "Heater plate", "Fibreglass rope", "Plate heaters", "Piston rod")
    tl.insert(stack, prefs=["front-step", "front-down"])
    b.buy("H1", "H2", "H3")
    tl.caption("Overflow cup under the slot", "slides into its pocket in the deck")
    cup = s.B("Overflow cup")
    zr = max(float(tl.actors[k].V[:, 2].max()) for k in body)
    hc = math.ceil(zr + 1.5 - float(tl.actors[cup[0]].V[:, 2].min()))
    tl.insert(cup, way=[(24, -FAR, hc), (24, 0, hc), (24, 0, 0), (0, 0, 0)])
    tl.insert(s.B("Film applicator"), prefs=["front-down", "front-step"])
    b.buy("M4")
    # the hand-spread layer, before the nozzle and the collector go on (the 70 mm applicator does not fit between them)
    tl.shot(CAMS["well"])
    s.cal("FT-0 hand-spread layers and pads", "a 50 um layer by hand")
    tl.caption("A layer spread by hand", "film applicator on shims: 50 um")
    app = s.B("Film applicator", new=False)
    lo = tl.actors[app[0]].V.min(0)
    hi = tl.actors[app[0]].V.max(0)
    xc_app = 0.5 * (lo[0] + hi[0])
    lift = 0.0 - lo[2] + 0.0                     # its foot on the block top
    x_start = -40.0 + (hi[0] - lo[0]) / 2 - xc_app
    x_end = 36.0 - xc_app
    way = [(0, 0, 0), (0, 0, lift + 30), (x_start, 0, lift + 30), (x_start, 0, lift)]
    tl.move(app, way, v=120, a=400, verb="lifting onto the block", label=[("Film applicator", "M4")])
    s.speed("hand speed, ~20 mm/s (estimate)")
    t0 = tl.t
    Pp = tl.move(app, [(0, 0, 0), (x_end - x_start, 0, 0)], v=20, a=60, verb="spreading", label=[("Film applicator", "M4")])
    blade0 = lo[0] + x_start

    def layer(st, t, t0=t0, T=Pp.T, x0=-20.0, x1=20.0):
        if t < t0:
            return
        s_ = min(1.0, (t - t0) / max(T, 1e-6))
        xm = x0 + (x1 - x0 + 2) * s_ - 1
        if xm <= x0:
            return
        V, F = disc(19.9, 0.0, 0.05, x_max=xm)
        st["_fx"]["powder layer"] = dict(kind="mesh", data=(V, F), color="#8b8d8f", opacity=1.0, solid=False,
                                         key=f"layer{xm:.2f}")
    tl.fx(layer, t0)
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    tl.move(app, [(0, 0, 0), (0, 0, 30), (-x_end, 0, 30), (-x_end, 0, -lift)], v=120, a=400, verb="parking",
            label=[("Film applicator", "M4")])
    tl.shot(CAMS["box"])
    tl.caption("Nozzle and exhaust collector", "45 x 4 mm slot: argon across the plate")
    tl.insert(s.B("Slot nozzle"), prefs=["front-down", "front-step"])
    tl.insert(s.B("Exhaust collector"), prefs=["front-down", "front-step", "back-down"])
    # the tubes' ends sit in bulkheads in the side walls, under the gasket's overhang: lowered clear of the wall, then
    # slid into the bulkhead
    feed = s.B("Argon feed tube")
    hf = math.ceil(zr + 2.0 - float(tl.actors[feed[0]].V[:, 2].min()))
    tl.insert(feed, way=[(10, -FAR, hf), (10, 0, hf), (10, 0, 0), (0, 0, 0)])
    exh = s.B("Exhaust hose to the HEPA")
    he = math.ceil(zr + 2.0 - float(tl.actors[exh[0]].V[:, 2].min()))
    tl.insert(exh, way=[(-15, -FAR, he), (-15, 15, he), (-15, 15, 0), (0, 0, 0)])
    b.buy("G3")
    tl.shot(CAMS["wide"])
    s.cal("FT-0 purge and heat (O2 log)", "O2 analyzer in: day %d-%d" % sched("O2 analyzer (used)"))
    tl.caption("Gas, filter and O2 analyzer", "argon in, HEPA out, trace O2 logged")
    tl.insert(s.B("Argon regulator"), prefs=["down", "front-down"], gap=-3.0)
    b.buy("G1", "G2", "C2")
    tl.insert(s.B("Exhaust HEPA"), prefs=["down", "front-down"], gap=-3.0)
    b.buy("G4")
    tl.insert(s.B("Trace O2 analyzer"), prefs=["down", "back-down"])
    b.buy("G5")
    place_rest(s, prefs=["front-step", "front-down", "down"])
    close_box(s, lid, tube, acc, "FT-0")
    tl.caption("Purge to 1000 ppm, plate to 200 C", "13-31 min expected at 20 L/min (flow purge)")
    tl.overlay("panel", ["O2: 20.9 % -> 1000 ppm", "23.5 L box, 20 L/min argon", "ideal 6.3 min, expected 13-31 min",
                         "plate heaters 2 x 50 W to 200 C"])
    tl.wait(6.0)
    tl.overlay("panel", None)
    # first tracks, slow motion
    tl.shot(CAMS["well"])
    s.cal("FT-0 FIRST TRACKS", "milestone")
    b.buy("S3", "S4", "P1")
    prog = SC.program()
    tl.overlay("scan", prog["source"])
    slow = 10.0
    tl.caption("First single tracks", "25 tracks, 9 mm, 25 power-speed pairs")
    s.speed(f"slow motion: 1/{slow:.0f} of real speed")
    tracks = prog["tracks"]
    tt = SC.timeline(tracks)
    t0 = tl.t + 0.8

    def draw_tracks(st, t, t0=t0):
        if t < t0:
            return
        tr = (t - t0) / slow
        segs, hot = [], []
        for (x0, y0, x1, y1, v, pw), (ta, tb) in zip(tracks, tt):
            if tr < ta:
                break
            f = min(1.0, (tr - ta) / max(tb - ta, 1e-9))
            seg = ((x0, y0, 0.06), (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 0.06))
            (hot if tr - tb < 0.05 else segs).append(seg)
        if segs:
            st["_fx"]["tracks"] = fx_lines("tracks", segs, "#5a5f66", 3.0)
        if hot:
            st["_fx"]["tracks hot"] = fx_lines("tracks hot", hot, "#ffb000", 4.0)
    tl.fx(draw_tracks, t0)
    T = tt[-1][1] * slow
    tl.overlay("panel", [f"25 tracks drawn in {tt[-1][1]:.2f} s of laser time", "speeds 200-1400 mm/s, 150-350 W",
                         "Bosio et al. 2019's screening on a 40 mm disc"], t0)
    tl.wait(0.8 + T + 3.0)
    tl.caption("FT-0 done: first tracks", "track widths give the hatch spacing")
    tl.wait(3.0)
    tl.overlay("panel", None)
    b.close()
    tl.end()
    return s


# ================================================================================================ chapter 4: FT-0 -> FT-1
def ch4():
    s = Story(4, "FT-0 to FT-1: stages and recoater", "FT-0", "FT-1")
    tl, b = s.tl, s.book
    tl.shot(CAMS["core"])
    s.cal("FT-0 -> FT-1 upgrade", "stages arrived day %d-%d (PCards)" % sched("stages arrive"))
    tube, lid = tube_group(s, "A"), lid_group(s, "A")
    body = s.A("304 NEMA 4X box", "Lid gasket", "Lid clamps")
    hb = max(float(np.ptp(d["V"][:, 2])) for n, d in S.state_meshes("FT-0").items() if n.startswith("Well block"))
    acc = open_box(s, tube, lid, body, "FT-0", under=hb)
    tl.overlay("access", acc)
    tl.remove(s.A("Film applicator"), prefs=["front-step", "front-down"])
    tl.shot(CAMS["box"])
    tl.caption("Plate up, collar off", "the rod comes out of the collar; the collar leaves")
    stack = s.A("Substrate disc", "Heater plate", "Fibreglass rope", "Plate heaters", "Piston rod")
    tl.move(stack, [(0, 0, 0), (0, 0, 140), (75, 0, 140)], v=40, verb="lifting aside",
            label=[("The plate on its rod", "MK-04, MK-05, MK-06")])
    tl.remove(s.A("FT-0 rod collar"), prefs=["front-down", "front-step"])
    tl.shot(CAMS["under"])
    tl.caption("The X-VSR20A under the box", "20 mm lift, 100 N continuous")
    tl.insert(s.B("Piston-stage bracket plate", "Zaber X-VSR20A", "X-VSR20A platform", "X-VSR20A lift column"),
              prefs=["front", "front-up"])
    b.buy("M2", "F2b")
    tl.insert(s.B("Rod clamp"), way=[(FAR, -40, 0), (0, -40, 0), (0, 0, 0)])
    tl.shot(CAMS["box"])
    tl.caption("Rod down into the clamp", "through the deck, the floor and the O-ring gland")
    tl.move(stack, [(0, 0, 0), (-75, 0, 0), (-75, 0, -140)], v=40, verb="lowering",
            label=[("The plate on its rod", "MK-04, MK-05, MK-06")])
    tl.caption("The X-LSQ075B recoater", "75 mm travel, behind the well")
    tl.insert(s.B("Zaber X-LSQ075B", "X-LSQ carriage"), prefs=["back-down", "back-step", "front-step", "front-down", "right-down", "left-down"])
    b.buy("M1b")
    tl.insert(s.B("Stage shield"), prefs=["back-down", "back-step", "front-step", "front-down"])
    tl.caption("Arm, hopper and blade", "~30 cm3 hopper, 3 mm silicone cord")
    tl.insert(s.B("Carriage bracket and arm", "Vibration motor"), prefs=["back-down", "back-step", "front-step", "front-down", "right-down"])
    tl.insert(s.B("Hopper, ~30"), prefs=["back-down", "back-step", "front-step", "front-down", "right-down"])
    tl.insert(s.B("Silicone-cord blade", "Cord clamp"), prefs=["back-down", "back-step", "front-step", "front-down", "right-down"])
    b.buy("M3")
    tl.caption("Two heaters into the block", "the block is held at the plate's 200 C")
    tl.insert(s.B("Well-block heaters"), way=[(-60, -FAR, 200), (-60, 0, 200), (-60, 0, 0), (0, 0, 0)])
    b.buy("H1b")
    tl.shot(CAMS["core"])
    tl.insert(s.B("120 mm fan"), prefs=["left", "left-down", "front-down", "down"])
    place_rest(s, prefs=["front-step", "front-down", "down"])
    close_box(s, lid, tube, acc, "FT-1")
    s.cal("FT-1 re-commission", "home both stages, purge, heat")
    tl.shot(CAMS["well"])
    tl.caption("Home both stages", "plate to +5 mm and back; hopper park to park")
    s.speed("real time (homing at 10 and 50 mm/s)")
    t0 = tl.t + 0.5
    piston = [k for k in tl.actors if tl.actors[k].group in ("piston", "column")]
    rec = [k for k in tl.actors if tl.actors[k].group == "recoater"]
    pz_path = E.Path([(0, 0, 0), (0, 0, 5), (0, 0, 0)], [PISTON_V] * 2, [50.0] * 2, pause=0.5)
    hx_path = E.Path([(0, 0, 0), (LEFT_PARK - HX0, 0, 0), (RIGHT_PARK - HX0, 0, 0)], [50.0] * 2,
                     [200.0] * 2, pause=0.5)
    add_stages(tl, piston, rec, lambda t: pz_path.at(t - t0)[2], lambda t: hx_path.at(max(0.0, t - t0 - pz_path.T - 0.5))[0],
               t0, t0 + pz_path.T + 0.5 + hx_path.T)
    tl.wait(0.5 + pz_path.T + 0.5 + hx_path.T + 1.0)
    tl.caption("FT-1 ready", "re-commissioned: purge, heat, stages homed")
    tl.wait(3.0)
    b.close()
    tl.end()
    return s


def add_stages(tl, piston, rec, pz_fn, hx_fn, t0, t1):
    """The piston group follows pz(t) (the lift column stretches with it); the recoater group follows hx(t) - HX0."""
    col = [k for k in piston if tl.actors[k].group == "column"]
    pis = [k for k in piston if k not in col]
    h0 = float(P["vs_plat"][2])                                  # unused; column height from the model
    a = tl.actors[col[0]] if col else None
    z_lo = float(a.V[:, 2].min()) if a else 0.0
    z_hi = float(a.V[:, 2].max()) if a else 1.0

    def off_p(t):
        return (0.0, 0.0, pz_fn(t))

    def off_r(t):
        return (hx_fn(t), 0.0, 0.0)

    def fn(st, t):
        tt = min(max(t, t0), t1)
        pz = pz_fn(tt)
        for k in pis:
            st[k]["stage"] = np.array([0.0, 0.0, pz])
        for k in col:
            # the column's bottom stays on the stage body; its top follows the platform: scale z about z_lo
            sc = (z_hi - z_lo + pz) / (z_hi - z_lo)
            st[k]["scale"] = (1.0, 1.0, sc, z_lo)
        hx = hx_fn(tt)
        for k in rec:
            st[k]["stage"] = np.array([hx, 0.0, 0.0])
    tl.events.append((t0, t1, fn))


# ================================================================================================ chapter 5: FT-1 coupons
def ch5():
    s = Story(5, "FT-1: the first coupons", "FT-1", "FT-1")
    tl, b = s.tl, s.book
    prog = SC.program()
    cp = prog["coupons"]
    tl.overlay("scan", prog["source"])
    piston = [k for k in tl.actors if tl.actors[k].group in ("piston", "column")]
    rec = [k for k in tl.actors if tl.actors[k].group == "recoater"]
    tl.shot(CAMS["well"])
    s.cal("FT-1 powder layers: dose, spread, pads")
    tl.caption("One layer, in real time", "spread at 10 mm/s, scan at 1000 mm/s")
    s.speed("real time")
    # one full layer cycle in real time: (hopper at the left park) plate down one layer, spread to the right park, scan,
    # return to the left park
    L = RIGHT_PARK - LEFT_PARK
    t_sp = E.trapezoid(L, SPREAD_V, 50.0)[0]
    t_ret = E.trapezoid(L, RETURN_V, 200.0)[0]
    vec0 = cp["layer"](0)
    tt0 = SC.timeline(vec0)
    t_scan = tt0[-1][1]
    t0 = tl.t + 0.6
    # timeline of the cycle
    a_ret0 = t0                                           # from the model's park (right) to the left park first
    t_ret0 = E.trapezoid(RIGHT_PARK - LEFT_PARK, RETURN_V, 200.0)[0]
    a_sp = a_ret0 + t_ret0 + 0.6
    a_scan = a_sp + t_sp + 0.4
    a_ret = a_scan + t_scan + 0.4
    t_end = a_ret + t_ret + 0.5

    def hx(t):
        if t < a_ret0:
            return RIGHT_PARK - HX0
        if t < a_sp:
            s_ = E.trapezoid(L, RETURN_V, 200.0)[1](t - a_ret0)
            return RIGHT_PARK - HX0 - s_
        if t < a_scan:
            return LEFT_PARK - HX0 + E.trapezoid(L, SPREAD_V, 50.0)[1](t - a_sp)
        if t < a_ret:
            return RIGHT_PARK - HX0
        return RIGHT_PARK - HX0 - E.trapezoid(L, RETURN_V, 200.0)[1](t - a_ret)

    def pz(t):
        return -LAYER if t >= a_sp - 0.3 else 0.0
    add_stages(tl, piston, rec, pz, hx, t0, t_end)
    hot = "#ffb000"

    def draw_scan(st, t):
        if t < a_scan - 0.01 or t > t_end + 30:
            return
        tr = t - a_scan
        segs, hots = [], []
        for (x0, y0, x1, y1, v), (ta, tb) in zip(vec0, tt0):
            if tr < ta:
                break
            f = min(1.0, (tr - ta) / max(tb - ta, 1e-9))
            seg = ((x0, y0, 0.05), (x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, 0.05))
            (hots if tr - tb < 0.15 else segs).append(seg)
        if segs:
            st["_fx"]["scan"] = fx_lines("scan", segs, "#4d5157", 1.5)
        if hots:
            st["_fx"]["scan hot"] = fx_lines("scan hot", hots, hot, 2.5)

    def bed(st, t):
        # the fresh layer behind the blade during the spread
        if a_sp <= t < a_scan:
            xb = LEFT_PARK + E.trapezoid(L, SPREAD_V, 50.0)[1](t - a_sp) - P["hopper"][0] / 2 - 2.0
            if xb > -20:
                V, F = disc(19.9, -LAYER, 0.0, x_max=min(xb, 20.0))
                st["_fx"]["fresh layer"] = dict(kind="mesh", data=(V, F), color="#9a9c9e", opacity=1.0, solid=False,
                                                key=f"fresh{xb:.1f}")
        elif t >= a_scan:
            V, F = disc(19.9, -LAYER, 0.0)
            st["_fx"]["fresh layer"] = dict(kind="mesh", data=(V, F), color="#9a9c9e", opacity=1.0, solid=False, key="fresh")
    tl.fx(bed, a_sp)
    tl.fx(draw_scan, a_scan)
    tl.overlay("panel", [f"layer 1 of {cp['n_layers']}: {LAYER * 1000:.0f} um",
                         f"spread {L:.1f} mm at {SPREAD_V:.0f} mm/s: {t_sp:.1f} s", f"scan: {t_scan:.1f} s",
                         f"return at {RETURN_V:.0f} mm/s: {t_ret:.1f} s"], t0)
    tl.t = t_end + 0.5
    # the time-lapse: one frame per layer, taken after each layer's scan
    tl.shot(CAMS["lowwell"])
    n = int(cp["n_layers"])
    s.cal("FT-1 FIRST COUPONS", "milestone")
    cyc = t_sp + t_scan + t_ret + 1.4
    tl.caption("Coupons growing", f"{n} layers, 10 mm: one frame per layer")
    s.speed(f"time-lapse x{cyc * E.FPS:.0f}: one frame per layer ({cyc:.0f} s of build)")
    for k in tl.actors:
        if "Well block" in tl.actors[k].label or "Box lid" in tl.actors[k].label:
            tl.fade(k, 0.22, tl.t)
    t1 = tl.t + 1.0
    T = n / E.FPS
    boxes_ = cp["boxes"]

    def grow(st, t, t1=t1):
        if t < t1:
            return
        k = min(n, int((t - t1) * E.FPS) + 1)
        h = k * LAYER
        for a in piston:
            if tl.actors[a].group == "column":
                st[a]["scale"] = (1.0, 1.0, (17.0 - h) / 17.0, float(tl.actors[a].V[:, 2].min()))
            else:
                st[a]["stage"] = np.array([0.0, 0.0, -h])
        for a in rec:
            st[a]["stage"] = np.array([RIGHT_PARK - HX0, 0.0, 0.0])
        V, F = boxes(boxes_, -h, 0.0)
        st["_fx"]["coupons"] = dict(kind="mesh", data=(V, F), color="#b9bec4", opacity=1.0, solid=True, key=f"coup{k}")
        V, F = disc(19.9, -h, 0.0)
        st["_fx"]["powder bed"] = dict(kind="mesh", data=(V, F), color="#8b8d8f", opacity=0.35, solid=False,
                                       key=f"bed{k}")
        vec = cp["layer"](k - 1)
        st["_fx"]["scan"] = fx_lines("scan", [((x0, y0, 0.05), (x1, y1, 0.05)) for (x0, y0, x1, y1, v) in vec],
                                     hot, 1.5)
        st["_fx"].pop("scan hot", None)
        st["_fx"].pop("fresh layer", None)
    tl.fx(grow, t1)
    tl.overlay("panel", [f"{n} layers x {LAYER * 1000:.0f} um = {n * LAYER:.1f} mm",
                         f"~{cyc:.0f} s a layer: {n * cyc / 3600:.1f} h (study: 1.2-1.8 h)",
                         "plate down one layer each time", "4 coupons, 10 x 10 mm"], t1)
    tl.wait(1.0 + T + 2.5)
    tl.caption("FT-1 done: first coupons", "10 x 10 x 10 mm, 100-1000 ppm O2")
    tl.overlay("panel", None)
    tl.wait(3.5)
    b.close()
    tl.end()
    return s


# ================================================================================================ chapter 6: FT-1 -> FT-1V
def ch6():
    s = Story(6, "FT-1 to FT-1V: into the vacuum cube", "FT-1", "FT-1V")
    tl, b = s.tl, s.book
    tl.shot(CAMS["cube"])
    s.cal("FT-1 -> FT-1V transfer", "cube in: day %d-%d; plates machined day %d-%d" % (
        *sched("cube frame and plates arrive (PO)"), *sched("cube plates machined")))
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    drive = s.A("X-VSR20A platform", "X-VSR20A lift column", "Rod clamp")
    col = [k for k in drive if tl.actors[k].group == "column"]
    drv = [k for k in drive if k not in col]
    zc0 = float(tl.actors[col[0]].V[:, 2].min()) if col else 0.0
    stack = s.A("Substrate disc", "Heater plate", "Fibreglass rope", "Plate heaters", "Piston rod")
    STACK_UP, BOX_UP = 30.0, 17.0
    tl.caption("Rod unclamped; stage down 15 mm", "then the plate is lifted 30 mm by hand")
    s.speed("real time (stage at 10 mm/s)")
    t0 = tl.t
    pz_path = E.Path([(0, 0, 0), (0, 0, -15)], [PISTON_V], [50.0])

    def drop(st, t):
        if t < t0:
            return
        z = pz_path.at(t - t0)[2]
        for k in drv:
            st[k]["stage"] = np.array([0.0, 0.0, z])
        for k in col:
            st[k]["scale"] = (1.0, 1.0, (17.0 + z) / 17.0, zc0)
    tl.events.append((t0, t0 + pz_path.T, drop))
    tl.wait(pz_path.T + 0.3)
    for k in drv:
        if k in tl.world.g:
            tl.world.move(k, np.array([0.0, 0.0, -15.0]))
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    tl.move(stack, [(0, 0, 0), (0, 0, STACK_UP)], v=15, verb="lifting", label=[("The plate on its rod", "MK-04, MK-05, MK-06")])
    tl.caption("Optics up 21 mm for the cube", "its floor plate is 21 mm thicker than the box's sheet")
    optics_move(s, "FT-1", 0.0, 21.0, "sliding up")
    tube = tube_group(s, "A", long=True)
    lid = lid_group(s, "A")
    zt = max(float(tl.actors[k].V[:, 2].max()) for k in lid)
    rise = math.ceil(zt + BOX_UP + 2.0 - float(tl.actors[tube[0]].V[:, 2].min()))
    tl.caption("Tube up; the box slides out", "with the cassette, the gland and the lid in it")
    tl.move(tube, [(0, 0, 0), (0, 0, rise)], v=30, verb="sliding up", label=[("Beam tube, long", "MK-10")])
    inside = [k for k in s.Am.values() if k.startswith("A|") and any(x in k for x in (
        "304 NEMA", "Lid gasket", "Box lid", "Continuous hinge", "Lid clamps", "Inner clamp ring", "Window ring", "Window, ",
        "Window retaining", "Cover-slide holder", "Cover slide,", "Coded lid switches", "120 mm fan", "Deck plate",
        "Macor standoffs", "Well block", "Well-block heaters", "Overflow cup", "Slot nozzle", "Exhaust collector",
        "Argon feed tube", "Exhaust hose", "Zaber X-LSQ", "X-LSQ carriage", "Carriage bracket", "Stage shield",
        "Hopper", "Silicone-cord", "Cord clamp", "Vibration motor", "Rod gland plate"))]
    inside = [k for k in inside if k not in tube] + stack
    tl.remove(inside, way=[(0, 0, 0), (0, 0, BOX_UP), (0, -FAR, BOX_UP)], verb="sliding out",
              label=[("The box with the cassette in it", "E1 + cassette")])
    lens_bot = float(tl.actors[[k for k in tl.actors if "f-theta" in k][0]].V[:, 2].min()) + 21.0
    off = math.floor(lens_bot - 2.0 - float(tl.actors[tube[0]].V[:, 2].max()))
    tl.caption("The long tube comes off", "down off the lens, out to the front")
    tl.remove(tube, way=[(0, 0, 0), (0, 0, off - rise), (0, -FAR, off - rise)], verb="taking off",
              label=[("Beam tube, long", "MK-10")])
    st_ = tube_group(s, "B", long=False)
    sh = [k for k in st_ if "Beam tube" in k][0]
    Tv = tl.actors[sh].V
    r = np.hypot(Tv[:, 0], Tv[:, 1])
    lens_r = 55.0
    below = Tv[(r < lens_r - 0.5) & (Tv[:, 2] <= lens_bot + 1e-6)]
    ring_top = float(below[:, 2].max()) if len(below) else -1e9
    hp_bot = float(tl.actors[[k for k in tl.actors if "Scan-head plate" in k][0]].V[:, 2].min()) + 21.0
    fr = math.floor(min(lens_bot - ring_top, hp_bot - float(Tv[:, 2].max())) - 0.5)
    lo = math.floor(lens_bot - 2.0 - float(Tv[:, 2].max()))
    tl.caption("Short tube onto the lens", f"it waits {fr:.0f} mm up the lens until the cube is in")
    tl.insert(st_, way=[(0, -FAR, lo), (0, 0, lo), (0, 0, fr)],
              label=[("Beam tube, short, with lens collar", "MK-10"), ("Beam-tube interlock switch", "S1")])
    kfn = [n for n in s.Bm if n.startswith("KF-25 ports")][0]
    F_ = P["cube_frame"]
    xc_, yc_ = P["deck_c"]
    ports = split_part(s, kfn, lambda c: "left" if c[0] < xc_ - F_ / 2 else "right" if c[0] > xc_ + F_ / 2 else "back")
    tl.caption("The 12 in. aluminium cube", "Ideal Vacuum frame, plates MK-13 and MK-14")
    cube = [s.Bm[n] for n in s.Bm if any(x in n for x in ("cube frame", "Cube top plate", "Cube bottom plate", "Cube back",
                                                          "Window ring", "Window, ", "Window retaining", "Cover-slide holder",
                                                          "Cover slide,"))] + [ports["back"]]
    tl.insert(cube, way=[(0, -FAR, 3), (0, 0, 3), (0, 0, 0)], label=[("Ideal Vacuum 12 in. cube with the window stack",
                                                                     "E2, MK-13, MK-14, MK-02, L8")])
    b.buy("E2", "F2c")
    tl.shot(CAMS["under"])
    tl.caption("Gland under the cube floor", "the same O-ring gland, re-bolted")
    tl.insert([s.Bm["Rod gland plate, 2 O-rings (MK-07)"]], prefs=["left", "front-up", "right"])
    tl.shot(CAMS["cube"])
    tl.caption("The cassette goes in", "250 mm deck through the face opening (266 mm, est.)")
    cas = [s.Bm[n] for n in s.Bm if s.Bm[n].startswith("B|") and any(x in n for x in (
        "Deck plate", "Macor standoffs", "Well block", "Well-block heaters", "Overflow cup", "Slot nozzle", "Exhaust collector",
        "Zaber X-LSQ", "X-LSQ carriage", "Carriage bracket", "Stage shield", "Hopper",
        "Silicone-cord", "Cord clamp", "Vibration motor"))]
    tl.insert(cas, way=[(0, -FAR, 14), (0, 0, 14), (0, 0, 0)], label=[("Deck cassette with the recoater", "MK-01 + all on it")])
    tl.caption("Gas tubes in from the sides", "they reach past the front opening; side plates after")
    tl.insert(s.B("Argon feed tube"), prefs=["left", "left-step", "left-down"], gap=-2.0)
    tl.insert(s.B("Exhaust hose to the HEPA"), prefs=["right", "right-step", "right-down"])
    tl.insert(s.B("Cube left plate") + [ports["left"]], way=[(-10, -FAR, 0), (-10, 0, 0), (0, 0, 0)], gap=-2.0,
              label=[("Cube left plate with its KF-25 ports", "E2, E3")])
    tl.insert(s.B("Cube right plate") + [ports["right"]], way=[(10, -FAR, 0), (10, 0, 0), (0, 0, 0)],
              label=[("Cube right plate with its KF-25 ports", "E2, E3")])
    tl.caption("Plate on the long rod", "21 mm longer rod, down into the clamp")
    stack_b = [s.Bm[n] for n in s.Bm if any(x in n for x in ("Substrate disc", "Heater plate", "Fibreglass rope",
                                                             "Plate heaters", "Piston rod"))]
    tl.insert(stack_b, way=[(0, -FAR, 145), (0, 0, 145), (0, 0, 0)])
    t0 = tl.t
    up = E.Path([(0, 0, -15), (0, 0, 0)], [PISTON_V], [50.0])
    s.speed("real time (stage at 10 mm/s)")

    def rise_(st, t):
        if t < t0:
            return
        z = up.at(t - t0)[2]
        for k in drv:
            st[k]["stage"] = np.array([0.0, 0.0, z])
        for k in col:
            st[k]["scale"] = (1.0, 1.0, (17.0 + z) / 17.0, zc0)
    tl.events.append((t0, t0 + up.T, rise_))
    tl.overlay("adding", ("moving", [("X-VSR20A up to the rod, clamped", "M2, MK-15")]), t0, t0 + up.T + 0.5)
    tl.wait(up.T + 0.4)
    for k in drv:
        if k in tl.world.g:
            tl.world.move(k, np.zeros(3))
    s.speed("by hand: 0.8 m/s, set down at 90 mm/s (estimates)")
    tl.caption("Door, ports and pump", "KF-25 ports, Pirani, feedthroughs, rotary-vane pump")
    tl.insert([s.Bm[n] for n in s.Bm if "Cube front plate" in n or "Door hinges" in n], prefs=["front", "front-down"])
    # the hose is drawn with its end in the pump's inlet, and its other end over the KF port's flange (clamped): the pump
    # comes with its hose, and the hose's clamp end meets the port (an allowed contact in the audit, up to 5 mm)
    tl.insert([s.Bm[n] for n in s.Bm if "Rotary-vane pump" in n or "KF-25 pump hose" in n],
              prefs=["down", "front-down", "left-down"], ignore=[ports["left"]],
              label=[("Rotary-vane pump with its KF-25 hose and valve", "E3")])
    b.buy("E3", "E5")
    tl.insert(s.B("Coded lid switches"), prefs=["front", "front-down", "down"])
    tl.insert(s.B("120 mm fan"), prefs=["back", "back-down", "down"])
    place_rest(s)
    tl.move(st_, [(0, 0, 0), (0, 0, -fr)], v=30, verb="sliding down", label=[("Short beam tube onto the flange", "MK-10")])
    tl.shot(CAMS["cube"])
    s.cal("FT-1V leak check and pump-purge")
    tl.caption("Leak check, then pump-purge", "two pump-and-fill cycles to ~1 mbar")
    tl.overlay("panel", ["2 cycles to ~1 mbar: < 100 ppm on paper", "~7 min and 44 L of argon",
                         "against 250-900 L for the box's flow purge"])
    tl.wait(6.0)
    s.cal("FT-1V FIRST COUPONS (< 100 ppm)", "milestone")
    tl.caption("FT-1V: coupons below 100 ppm", "the box becomes the spreadability rig")
    tl.overlay("panel", None)
    tl.wait(4.0)
    b.close()
    tl.end()
    return s


# ================================================================================================ chapter 7: summary
def ch7():
    s = Story(7, "Summary: weeks and dollars", "FT-1V", "FT-1V")
    tl = s.tl
    tl.shot(CAMS["cube"])
    tl.caption("One machine, five states", "S1 -> S2 -> FT-0 -> FT-1 -> FT-1V")
    s.cal("FT-1V FIRST COUPONS (< 100 ppm)", "")
    ms = ["S1 guide-laser and scanner checks", "S2 FULL POWER INTO THE DUMP", "FT-0 FIRST TRACKS", "FT-1 FIRST COUPONS",
          "FT-1V FIRST COUPONS (< 100 ppm)"]
    tl.overlay("summary", dict(milestones=[(m, *sched(m)) for m in ms], spend=cumulative(), scenario=_SCHED["_scenario"]))
    tl.wait(20.0)
    tl.end()
    return s


CHAPTERS = {0: ch0, 1: ch1, 2: ch2, 3: ch3, 4: ch4, 5: ch5, 6: ch6, 7: ch7}


def build(n):
    s = CHAPTERS[n]()
    return s
