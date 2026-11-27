"""Moonwalk checks on what the robot-build video's frames draw: people's feet and the MiR bases (round 8, issue #260, PR #266).

Sterling, 2026-11-26: "moonwalk". His byu-vcl lessons (notes/2026-11-26-byu-vcl-video-lessons.md): lesson 2, a MiR250 is a
differential drive: it can't slide sideways, it drives along its heading (pivot, drive, pivot) and reverses only for a short
docking leg; lesson 8, a person's gait phase follows the distance walked (one cycle per people.Person.STRIDE = 1016 mm), the
lowest shoe on the floor every frame, and nobody glides. This reads audit_rec.py's recordings (ROBOTBUILD_AUDIT=1), as
scene_audit.py does, so it measures what was drawn.

    /tmp/venv/bin/python desktop-lpbf/cad/robotbuild/walk.py 50-integration

People (actors "<who>/shoes", people.py): the shoe mesh is split into its two feet (connected pieces; the left foot has x < 0
in the body frame). Per frame each foot's lowest point; a foot is DOWN when it is within FOOT_DOWN mm of the lower foot (the
lower one is grounded every frame). A stance is a run of frames with that foot down.
  slip        per frame, the mean horizontal travel of the foot's contact vertices (those within CONTACT mm of its lowest point
              at the earlier frame, the same vertices at the later one): a planted sole's material points don't move, so this
              is how far the sole slides, whatever the foot rolls. Per stance: the sum over its frames. Reported: per person
              the number of stances, slip max / 95th percentile / mean per stance, the worst stances (frames), and per-frame
              slip over SLIP_FRAME mm.
  gliding     a frame where the body's frame moved (more than GLIDE_MM, or turned more than GLIDE_DEG) while the legs stood still
              in it (no shoe vertex moved more than LEGS_MM in the body frame): the body translates on still feet.
  jumps       the body's frame moved more than JUMP_MM in one frame (a cut, a time-lapse or a teleport), listed apart and left
              out of slip and gliding.
MiR bases (actors "mir<tag>/..."): the base's centre (its "MiR250" body's bounding-box centre) and heading (the body's long
axis, local x) per frame. Per frame: sideways slip (travel perpendicular to the mean heading), travel along it, the heading
change. The mesh has no front, so "forward" is the end that leads over most of the chapter's travel (the most charitable
reading); the other direction is reversing: total, legs (runs of frames, pauses of up to LEG_PAUSE frames joined) and the
longest leg. Pivots (turning in place) are counted; jumps as for people.

Output: analysis/out/videoqa/walk_<chapter>.json.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import scene_audit as SA  # noqa: E402

FOOT_DOWN = 4.0          # mm: a foot within this of the lower foot's lowest point is on the floor
CONTACT = 2.0            # mm: a foot's contact vertices, from its lowest point
SLIP_FRAME = 5.0         # mm: a frame's slip reported as a slipping frame above this
GLIDE_MM, GLIDE_DEG, LEGS_MM = 1.0, 0.3, 0.5
JUMP_MM = 250.0          # mm in one frame (3 m/s at 12 fps): a cut, time-lapse or teleport, not a step
MIR_JUMP_MM = 150.0      # mm in one frame (1.8 m/s; the MiR250 tops out at 2 m/s, shop_cell drives 1 m/s)
LEG_PAUSE = 6
RE_SHOES = re.compile(r"^(?P<who>[^/]+)/shoes$")
RE_MIR = re.compile(r"^(?P<mir>mir[^/]*)/(?P<part>.+)$")


def _feet(V, F):
    """Vertex labels of the two feet (0 left, 1 right; -1 unused) from the shoe mesh's connected pieces."""
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    e = np.r_[F[:, [0, 1]], F[:, [1, 2]]]
    g = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(len(V), len(V)))
    nc, lab = connected_components(g, directed=False)
    used = np.zeros(len(V), bool)
    used[F.ravel()] = True
    cnt = np.bincount(lab[used], minlength=nc)
    big = np.argsort(-cnt)[:2]
    out = -np.ones(len(V), int)
    if len(big) < 2 or cnt[big[1]] == 0:          # one piece: split by the body's x
        out[used & (V[:, 0] < 0)] = 0
        out[used & (V[:, 0] >= 0)] = 1
        return out
    xs = [V[lab == c, 0].mean() for c in big]
    left, right = (big[0], big[1]) if xs[0] < xs[1] else (big[1], big[0])
    out[lab == left] = 0
    out[lab == right] = 1
    return out


def _yaw(M):
    return math.degrees(math.atan2(float(M[1, 0]), float(M[0, 0])))


def _pct(a, q):
    return round(float(np.percentile(a, q)), 1) if len(a) else 0.0


class PersonTrack:
    def __init__(self, who):
        self.who = who
        self.lab = None
        self.labF = None
        self.prev = None                 # (n, W (world), Vlocal, M, down[2], contact idx per foot)
        self.frames = 0
        self.dist = 0.0
        self.stance = [None, None]       # per foot: [start n, slip sum, frames, max per frame]
        self.stances = []
        self.slip_frames = []            # (n, foot, mm)
        self.glide = []                  # (n, mm, deg)
        self.jumps = []                  # (n, mm)

    def close_stance(self, f, n_end):
        s = self.stance[f]
        if s is not None:
            self.stances.append(dict(foot="LR"[f], start=s[0], end=n_end, frames=s[2], slip_mm=round(s[1], 1),
                                     max_frame_mm=round(s[3], 1)))
        self.stance[f] = None

    def step(self, n, V, F, M):
        if self.lab is None or self.labF is not F:
            self.lab, self.labF = _feet(V, F), F
        M = M.astype(float)
        W = V.astype(float) @ M[:3, :3].T + M[:3, 3]
        zmin = [W[self.lab == f, 2].min() if np.any(self.lab == f) else 1e9 for f in (0, 1)]
        low = min(zmin)
        down = [zmin[f] <= low + FOOT_DOWN for f in (0, 1)]
        contact = [np.nonzero((self.lab == f) & (W[:, 2] <= zmin[f] + CONTACT))[0] for f in (0, 1)]
        self.frames += 1
        if self.prev is not None:
            pn, pW, pV, pM, pdown, pcon = self.prev
            move = float(np.linalg.norm(M[:2, 3] - pM[:2, 3]))
            turn = abs((_yaw(M) - _yaw(pM) + 180.0) % 360.0 - 180.0)
            # round 9: people re-skinned in world coordinates keep an identity matrix, so a placement (a cut) moved only
            # the vertices; the shoes' centre moving more than JUMP_MM in a frame is a jump too
            shift = float(np.linalg.norm(W[:, :2].mean(0) - pW[:, :2].mean(0))) if len(W) == len(pW) else 0.0
            move_j = max(move, shift)
            if move_j > JUMP_MM:
                move = move_j
                self.jumps.append((n, round(move)))
                for f in (0, 1):
                    self.close_stance(f, pn)
            else:
                self.dist += move
                legs = float(np.max(np.linalg.norm(V.astype(float) - pV, axis=1))) if len(V) == len(pV) else 1e9
                if (move > GLIDE_MM or turn > GLIDE_DEG) and legs < LEGS_MM:
                    self.glide.append((n, round(move, 1), round(turn, 2)))
                for f in (0, 1):
                    if down[f] and pdown[f]:
                        c = pcon[f]
                        slip = float(np.mean(np.linalg.norm(W[c, :2] - pW[c, :2], axis=1))) if len(c) else 0.0
                        s = self.stance[f]
                        if s is None:
                            s = self.stance[f] = [pn, 0.0, 1, 0.0]
                        s[1] += slip
                        s[2] += 1
                        s[3] = max(s[3], slip)
                        if slip > SLIP_FRAME:
                            self.slip_frames.append((n, "LR"[f], round(slip, 1)))
                    elif not down[f] and pdown[f]:
                        self.close_stance(f, pn)
        self.prev = (n, W, V.astype(float), M, down, contact)

    def report(self):
        for f in (0, 1):
            if self.stance[f] is not None:
                self.close_stance(f, self.prev[0] if self.prev else 0)
        st = self.stances
        slips = np.array([s["slip_mm"] for s in st]) if st else np.zeros(0)
        moving = [s for s in st if s["frames"] > 1]
        return dict(
            person=self.who, frames=self.frames, walked_mm=round(self.dist), stances=len(st),
            slip_per_stance_mm=dict(max=_pct(slips, 100), p95=_pct(slips, 95), mean=round(float(slips.mean()), 1) if len(slips) else 0.0),
            worst_stances=sorted(moving, key=lambda s: -s["slip_mm"])[:10],
            slipping_frames=len(self.slip_frames), slipping_frame_list=self.slip_frames[:60],
            gliding_frames=len(self.glide), gliding_ranges=SA._ranges([g[0] for g in self.glide], 2)[:40],
            gliding_worst=sorted(self.glide, key=lambda g: -g[1])[:10],
            jumps=self.jumps[:40],
        )


class MirTrack:
    def __init__(self, tag):
        self.tag = tag
        self.c_local = None
        self.prev = None
        self.rows = []                   # (n, along, side, dturn)
        self.jumps = []

    def step(self, n, M, c_local):
        M = M.astype(float)
        c = M[:3, :3] @ c_local + M[:3, 3]
        h = M[:3, 0]
        if self.prev is not None:
            pn, pc, ph = self.prev
            d = (c - pc)[:2]
            hh = (h + ph)[:2]
            nh = float(np.linalg.norm(hh))
            hh = hh / nh if nh > 1e-9 else h[:2] / max(1e-9, float(np.linalg.norm(h[:2])))
            along = float(d @ hh)
            side = float(d @ np.array([-hh[1], hh[0]]))
            turn = math.degrees(math.atan2(h[1], h[0]) - math.atan2(ph[1], ph[0]))
            turn = (turn + 180.0) % 360.0 - 180.0
            if float(np.linalg.norm(d)) > MIR_JUMP_MM:
                self.jumps.append((n, round(float(np.linalg.norm(d))), round(along), round(side)))
            else:
                self.rows.append((n, along, side, turn))
        self.prev = (n, c, h)

    def report(self):
        R = np.array(self.rows, float) if self.rows else np.zeros((0, 4))
        fwd_pos = float(R[R[:, 1] > 0, 1].sum()) if len(R) else 0.0
        fwd_neg = float(-R[R[:, 1] < 0, 1].sum()) if len(R) else 0.0
        sign = 1.0 if fwd_pos >= fwd_neg else -1.0
        legs, cur, pause = [], None, 0
        for n, al, sd, tu in self.rows:
            rev = al * sign < -0.5
            if rev:
                if cur is None:
                    cur = [int(n), int(n), 0.0]
                cur[1], cur[2], pause = int(n), cur[2] + abs(al), 0
            elif cur is not None:
                if abs(al) > 0.5 or pause >= LEG_PAUSE:
                    legs.append(cur)
                    cur, pause = None, 0
                else:
                    pause += 1
        if cur is not None:
            legs.append(cur)
        side = np.abs(R[:, 2]) if len(R) else np.zeros(0)
        pivots = int(np.sum((np.abs(R[:, 3]) > 0.2) & (np.abs(R[:, 1]) < 1.0))) if len(R) else 0
        return dict(
            mir=self.tag, frames=len(self.rows) + 1 if self.prev else 0,
            driven_mm=round(fwd_pos + fwd_neg), forward="local +x" if sign > 0 else "local -x",
            forward_mm=round(max(fwd_pos, fwd_neg)), reverse_mm=round(min(fwd_pos, fwd_neg)),
            reverse_legs=len(legs), longest_reverse_leg_mm=round(max((l[2] for l in legs), default=0.0)),
            reverse_leg_list=[dict(start=l[0], end=l[1], mm=round(l[2])) for l in sorted(legs, key=lambda l: -l[2])[:20]],
            sideways_mm=dict(total=round(float(side.sum()), 1), max_frame=round(float(side.max()), 2) if len(side) else 0.0,
                             frames_over_1mm=int(np.sum(side > 1.0))),
            sideways_worst=[dict(frame=int(r[0]), side_mm=round(float(r[2]), 1), along_mm=round(float(r[1]), 1))
                            for r in sorted(self.rows, key=lambda r: -abs(r[2]))[:10] if abs(r[2]) > 1.0],
            pivot_frames=pivots, turned_deg=round(float(np.abs(R[:, 3]).sum()), 1) if len(R) else 0.0,
            jumps=self.jumps[:40],
        )


def run(chapter):
    t0 = time.time()
    dirs = SA.audit_dirs(chapter)
    if not dirs:
        raise SystemExit(f"{chapter}: no recordings")
    hist, ns = SA.histories(dirs)
    shoes = [n for n in hist if RE_SHOES.match(n)]
    mirs = {}
    for n in hist:
        m = RE_MIR.match(n)
        if m:
            mirs.setdefault(m["mir"], []).append(n)
    body = {}                                         # mir tag -> the actor whose box centre is the base's centre
    for tag, lst in mirs.items():
        body[tag] = next((n for n in lst if "MiR250" in n), sorted(lst)[0])
    want = set(shoes) | set(body.values())
    print(f"{chapter}: {len(ns)} recorded frames; people {[RE_SHOES.match(s)['who'] for s in shoes]}; MiRs {sorted(mirs)}",
          flush=True)
    people = {s: PersonTrack(RE_SHOES.match(s)["who"]) for s in shoes}
    bases = {tag: MirTrack(tag) for tag in mirs}
    rp = SA.Replay(dirs, want=lambda nm: nm in want)
    seen = set()
    for tag, n, actors, dirty in rp.frames():
        if tag not in seen:                           # a new slice: don't join tracks across slices
            seen.add(tag)
            for p in people.values():
                p.prev = None
            for b in bases.values():
                b.prev = None
        for s, tr in people.items():
            a = actors.get(s)
            if a is None or not a.vis or a.geom is None:
                if tr.prev is not None:            # round 9: hidden (between a person's jobs): the next time they are
                    for f in (0, 1):               # drawn starts new stances, nothing is measured across the gap
                        tr.close_stance(f, tr.prev[0])
                    tr.prev = None
                continue
            tr.step(n, a.geom.V, a.geom.F, a.M)
        for tg, tr in bases.items():
            a = actors.get(body[tg])
            if a is None or not a.vis or a.geom is None:
                continue
            c_local = 0.5 * (a.geom.V.min(0) + a.geom.V.max(0)).astype(float)
            tr.step(n, a.M, c_local)
    out = dict(chapter=chapter, frames_recorded=len(ns), recordings=[str(d) for _, d in dirs],
               people=[p.report() for p in people.values()], mirs=[b.report() for b in bases.values()],
               limits=dict(foot_down_mm=FOOT_DOWN, contact_mm=CONTACT, slip_frame_mm=SLIP_FRAME, glide_mm=GLIDE_MM,
                           glide_deg=GLIDE_DEG, legs_still_mm=LEGS_MM, jump_mm=JUMP_MM, mir_jump_mm=MIR_JUMP_MM),
               seconds=round(time.time() - t0, 1))
    SA.OUT.mkdir(parents=True, exist_ok=True)
    path = SA.OUT / f"walk_{chapter}.json"
    path.write_text(json.dumps(out, indent=1, default=SA._js) + "\n")
    for p in out["people"]:
        print(f"  person {p['person']}: {p['frames']} frames, walked {p['walked_mm']} mm, {p['stances']} stances, slip per "
              f"stance max {p['slip_per_stance_mm']['max']} p95 {p['slip_per_stance_mm']['p95']} mm, "
              f"{p['slipping_frames']} slipping frames, {p['gliding_frames']} gliding frames, {len(p['jumps'])} jumps",
              flush=True)
    for b in out["mirs"]:
        print(f"  {b['mir']}: driven {b['driven_mm']} mm, reverse {b['reverse_mm']} mm in {b['reverse_legs']} legs "
              f"(longest {b['longest_reverse_leg_mm']}), sideways {b['sideways_mm']}, pivots {b['pivot_frames']}, "
              f"{len(b['jumps'])} jumps", flush=True)
    print(f"  -> {path} ({out['seconds']} s)", flush=True)
    return out


# ================================================================================================ round 9: the foot lock's test
class _StubScene:
    """Enough of pvscene.PVScene for people.Person without VTK (the numbers only)."""

    def __init__(self):
        self.actors, self.group_of, self.parent, self.gmat, self.alpha, self.base_alpha = {}, {}, {}, {}, {}, {}
        self.before_render = []

    def add(self, name, poly, color, group="static", opacity=1.0, shown=True, **kw):
        self.actors[name], self.group_of[name] = poly, group
        self.gmat.setdefault(group, np.eye(4))
        self.alpha[name], self.base_alpha[name] = (1.0 if shown else 0.0), opacity

    def set_mesh(self, name, poly):
        self.actors[name] = poly

    def world(self, g):
        m = self.gmat.get(g, np.eye(4))
        while g in self.parent:
            g = self.parent[g]
            m = self.gmat.get(g, np.eye(4)) @ m
        return m

    def members(self, g):
        return [n for n, gg in self.group_of.items() if gg == g]


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


def _profile(dist, v, fps=12.0, ramp=1.0):
    """Distances along a move of `dist` mm at up to `v` mm/s, easing in and out over `ramp` s: one per frame."""
    n_r = max(2, int(ramp * fps))
    out, s, sp = [], 0.0, 0.0
    while s < dist - 1e-6:
        left = dist - s
        sp = min(v / fps, sp + v / fps / n_r, max(v / fps / n_r, math.sqrt(2.0 * left * v / fps / n_r)))
        s = min(dist, s + sp)
        out.append(s)
    return out


def _scenarios():
    """{name: (number of people, [per frame: [(x, y, hd, extra set() kwargs) per person]], load box or None)}"""
    sc = {}
    # 1. a straight walk: stand, 3 m along +x at 0.9 m/s, stand
    fr = [[(0.0, 0.0, -90.0, {})]] * 12
    fr += [[(s, 0.0, -90.0, {})] for s in _profile(3000.0, 900.0)]
    fr += [[(3000.0, 0.0, -90.0, {})]] * 18
    sc["straight"] = fr
    # 2. turns: 180 deg on the spot (90 deg/s), 1 m forward, a 90 deg left turn on a 0.8 m arc, 90 deg right on the spot
    fr = [[(0.0, 0.0, 0.0, {})]] * 6
    for k in range(24):
        fr.append([(0.0, 0.0, 180.0 * _ease((k + 1) / 24), {})])
    fr += [[(0.0, 0.0, 180.0, {})]] * 6
    for s in _profile(1000.0, 800.0):
        fr.append([(0.0, -s, 180.0, {})])
    r0 = 800.0
    n = 30
    for k in range(n):                                   # facing -y, turning left (to +x) round a centre at (800, -1000)
        a = 90.0 * _ease((k + 1) / n)
        fr.append([(r0 - r0 * math.cos(math.radians(a)), -1000.0 - r0 * math.sin(math.radians(a)), 180.0 + a, {})])
    x1, y1 = fr[-1][0][0], fr[-1][0][1]
    fr += [[(x1, y1, 270.0, {})]] * 6
    for k in range(18):
        fr.append([(x1, y1, 270.0 - 90.0 * _ease((k + 1) / 18), {})])
    fr += [[(x1, y1, 180.0, {})]] * 18
    sc["turn"] = fr
    # 3. side-steps and backing up: 0.6 m to the right at 0.3 m/s, 0.4 m backwards, 0.3 m to the left
    fr = [[(0.0, 0.0, 0.0, {})]] * 6
    for s in _profile(600.0, 300.0, ramp=0.6):
        fr.append([(s, 0.0, 0.0, {})])
    fr += [[(600.0, 0.0, 0.0, {})]] * 10
    for s in _profile(400.0, 350.0, ramp=0.6):
        fr.append([(600.0, -s, 0.0, {})])
    fr += [[(600.0, -400.0, 0.0, {})]] * 10
    for s in _profile(300.0, 250.0, ramp=0.6):
        fr.append([(600.0 - s, -400.0, 0.0, {})])
    fr += [[(300.0, -400.0, 0.0, {})]] * 18
    sc["side-step"] = fr
    return sc


def _carry_frames():
    """Two people carry a 330 x 241 x 140 mm block (the chamber blank, 30 kg) by its ends: 2 m along its length (one walks
    backwards), a quarter turn about its centre, 0.8 m sideways (both side-step), set down."""
    import people as PP
    lo, hi = np.array([-165.0, -120.5, -70.0]), np.array([165.0, 120.5, 70.0])
    zc = 1000.0

    def M(x, y, yaw):
        a = math.radians(yaw)
        m = np.eye(4)
        m[:2, :2] = [[math.cos(a), -math.sin(a)], [math.sin(a), math.cos(a)]]
        m[:3, 3] = (x, y, zc)
        return m
    poses = [(0.0, 0.0, 0.0)] * 10
    poses += [(s, 0.0, 0.0) for s in _profile(2000.0, 500.0)]
    poses += [(2000.0, 0.0, 0.0)] * 6
    for k in range(36):
        poses.append((2000.0, 0.0, 90.0 * _ease((k + 1) / 36)))
    poses += [(2000.0, 0.0, 90.0)] * 6
    poses += [(2000.0 + s, 0.0, 90.0) for s in _profile(800.0, 300.0, ramp=0.6)]
    poses += [(2800.0, 0.0, 90.0)] * 18
    frames = []
    for (x, y, yaw) in poses:
        m = M(x, y, yaw)
        st = PP.carry(lo, hi, m, ends=("-x", "+x"))
        frames.append((m, st))
    return lo, hi, frames


def selftest(gif=None):
    """Round 9's foot-lock test: a straight walk, turns, side-steps and backing up, and a two-person carry, each through
    people.Person and its Gait, measured by this file's own PersonTrack (as the frame audit measures a chapter): max
    stance-foot slip per stance and gliding frames; the carry also with people.carry_check (body clear of the load,
    hands in it). Output: analysis/out/videoqa/walk_selftest.json; with gif=<path>, a small GIF of the carry (xvfb)."""
    import people as PP
    res = {}
    t0 = time.time()
    for name, frames in _scenarios().items():
        sc = _StubScene()
        p = PP.Person(sc, "op")
        tr = PersonTrack("op")
        x0, y0, h0, _ = frames[0][0]
        p.place(x0, y0, h0, frame=0)
        for n, row in enumerate(frames):
            x, y, hd, kw = row[0]
            p.set(x=x, y=y, hd=hd, frame=n, **kw)
            d, poly = p.parts["shoes"]
            tr.step(n, np.asarray(poly.points, float), d["F"], sc.gmat[p.group])
        r = tr.report()
        res[name] = dict(frames=len(frames), walked_mm=r["walked_mm"], stances=r["stances"], steps=p.gait.steps,
                         slip_per_stance_mm=r["slip_per_stance_mm"], slipping_frames=r["slipping_frames"],
                         gliding_frames=r["gliding_frames"], overreach_frames=p.gait.overreach_frames)
    lo, hi, frames = _carry_frames()
    sc = _StubScene()
    ppl = [PP.Person(sc, "op", gloves=True), PP.Person(sc, "op2", gloves=True)]
    trs = [PersonTrack("op"), PersonTrack("op2")]
    clear, hands_in, reach = [], [], []
    for n, (m, st) in enumerate(frames):
        for p, tr, s in zip(ppl, trs, st):
            kw = {k: s[k] for k in ("x", "y", "hd", "lean", "hands", "palm", "elbow", "bend", "grip", "look")}
            if n == 0:
                p.place(s["x"], s["y"], s["hd"], frame=0)
            p.set(frame=n, **kw)
            d, poly = p.parts["shoes"]
            tr.step(n, np.asarray(poly.points, float), d["F"], sc.gmat[p.group])
            c = PP.carry_check(p, lo, hi, m)
            clear.append(c["body_clear_mm"])
            hands_in.append(c["hands_in_mm"])
            reach.append(s["reach_mm"])
    for p, tr in zip(ppl, trs):
        r = tr.report()
        res[f"carry/{p.n}"] = dict(frames=len(frames), walked_mm=r["walked_mm"], stances=r["stances"], steps=p.gait.steps,
                                   slip_per_stance_mm=r["slip_per_stance_mm"], slipping_frames=r["slipping_frames"],
                                   gliding_frames=r["gliding_frames"], overreach_frames=p.gait.overreach_frames)
    res["carry"] = dict(load="330 x 241 x 140 mm block, carried by its ends (side grip)", body_clear_mm_min=min(clear),
                        hands_in_load_mm_max=max(hands_in), reach_mm_worst=max(reach),
                        stance=dict(front_mm=frames[0][1][0]["front_mm"], lean_deg=frames[0][1][0]["lean"]))
    ok = all(v["slip_per_stance_mm"]["max"] <= 10.0 and v["gliding_frames"] == 0 for k, v in res.items() if k != "carry")
    out = dict(test="people.py's Gait (round 9 foot lock) through walk.py's PersonTrack", limits=dict(slip_per_stance_mm=10.0,
               gliding_frames=0, body_clear_mm=30.0), passed=bool(ok and min(clear) >= 29.0), results=res,
               seconds=round(time.time() - t0, 1))
    SA.OUT.mkdir(parents=True, exist_ok=True)
    path = SA.OUT / "walk_selftest.json"
    path.write_text(json.dumps(out, indent=1, default=SA._js) + "\n")
    for k, v in res.items():
        print(f"  {k}: {json.dumps(v)}", flush=True)
    print(f"  passed {out['passed']} -> {path}", flush=True)
    if gif:
        _gif(gif)
    return out


def _gif(path, size=(480, 270), every=2):
    """A small GIF of the carry and a straight walk (pvscene, under xvfb-run)."""
    import common
    import people as PP
    import pvscene
    import pyvista as pv
    from PIL import Image
    lo, hi, frames = _carry_frames()
    pl = pvscene.plotter(size)
    sc = pvscene.PVScene(pl)
    sc.add("floor", pv.Plane(center=(1400.0, 0.0, -1.0), i_size=9000, j_size=7000), common.FLOOR, specular=0.0)
    # footprints: a faint grid on the floor so a sliding foot would show
    for gx in np.arange(-1500.0, 4500.0, 500.0):
        sc.add(f"grid x{gx}", pv.Box(bounds=(gx - 3, gx + 3, -2500, 2500, -0.5, 0.6)), "#8f948e", specular=0.0)
    for gy in np.arange(-2500.0, 2600.0, 500.0):
        sc.add(f"grid y{gy}", pv.Box(bounds=(-1500, 4500, gy - 3, gy + 3, -0.5, 0.6)), "#8f948e", specular=0.0)
    box = pv.Box(bounds=(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
    sc.add("load", box, "#b8bec4", group="load", specular=0.4)
    ppl = [PP.Person(sc, "op", gloves=True), PP.Person(sc, "op2", gloves=True, coat=PP._rgb("#6b7f4e"))]
    imgs = []
    for n, (m, st) in enumerate(frames):
        sc.gmat["load"] = m
        for p, s in zip(ppl, st):
            kw = {k: s[k] for k in ("x", "y", "hd", "lean", "hands", "palm", "elbow", "bend", "grip", "look")}
            if n == 0:
                p.place(s["x"], s["y"], s["hd"], frame=0)
            p.set(frame=n, **kw)
        if n % every:
            continue
        cam = [(1500.0, -5200.0, 2300.0), (1500.0, 0.0, 650.0), (0, 0, 1)]      # a fixed camera: a sliding foot would show
        imgs.append(Image.fromarray(sc.render(cam, 36.0)))
    pal = [im.convert("P", palette=Image.ADAPTIVE, colors=160, dither=Image.Dither.NONE) for im in imgs]
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=int(1000 * every / 12), loop=0, optimize=True)
    print(f"  gif {path}: {len(pal)} frames, {Path(path).stat().st_size / 1e6:.2f} MB", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("chapter", nargs="?", help="a chapter whose frames were recorded with ROBOTBUILD_AUDIT=1")
    ap.add_argument("--selftest", action="store_true", help="round 9: the foot lock on a walk, turns, side-steps, a carry")
    ap.add_argument("--gif", help="with --selftest: also draw the carry into this GIF (under xvfb-run)")
    a = ap.parse_args()
    if a.selftest:
        selftest(a.gif)
    else:
        run(a.chapter)
