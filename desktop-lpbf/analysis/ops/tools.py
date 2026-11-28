"""Hand tools and hand envelopes for the access checks (issue #260, PR #266). Sources: SOURCES below and operations.md.

Every tool is built in a local frame: origin on the screw axis at the top of the screw head, +z out of the socket
(away from the screw tip), and +x the direction the tool's arm or bar points at a turn angle of 0. checks.tool_check()
turns it about z. Each tool carries two meshes, "tool" and "hand", and a turning tool fails if either touches anything.
A hex key's cross-section is drawn as a round bar over the hex's corners (ISO 2936 e max, ~1.13 s).

Dimensions (mm), all read 2026-11-20 UTC:
  ISO 2936:2014 Table 1 hex keys: long arm L1 (standard and long series) and short arm L2, s = 2 ... 5.
  Bondhus ball-end L-wrenches (10952 ... 10964): long arm and short arm; the ball end works up to 25 deg off the axis.
  Wera 454 / 454 HF T-handle hex keys: 100 mm shaft below the handle, cross-bar 65 / 77 / 77 / 99 mm for s = 2.5 / 3 / 4 / 5,
      handle 32-49 mm along the axis, 15-22 mm thick.
  Wera 7441 Kraftform torque screwdriver (1.2-3.0 N m, 1/4 in. bits, Rapidaptor chuck): 155 mm overall, 105 mm handle,
      so ~50 mm of chuck; with a Wera 840/4 Z 50 mm bit (Ø4-6 shank behind the hex tip) of which ~35 mm shows.
      Handle Ø40 and chuck Ø16 are assumptions (Wera does not list them; Wiha's TorqueVario-S handles are Ø36-41).
  Hands: a two-finger pinch 46 x 25 x 60 (index finger 23 mm wide at the middle knuckle, 95th percentile man, FAA HFDS
      App. B); a fist round a T-bar 100 x 55 x 60 and a 90 mm hand cylinder round a screwdriver handle (hand breadth across
      the knuckles 96-98 mm and hand thickness 33 mm, 95th percentile man: FAA HFDS ch. 14 / App. B, NASA RP-1024).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import trimesh

from checks import bvh

# ISO 2936:2014 Table 1: s -> (L1 standard, L1 long, L2), and e max (across corners)
ISO2936 = {2.0: (52.0, 77.0, 18.0), 2.5: (58.5, 87.5, 20.5), 3.0: (66.0, 93.0, 23.0), 4.0: (74.0, 104.0, 29.0), 5.0: (85.0, 120.0, 33.0)}
E_MAX = {2.0: 2.25, 2.5: 2.82, 3.0: 3.39, 4.0: 4.53, 5.0: 5.67}
BONDHUS_BALL = {2.0: (82.0, 16.0, "10952"), 2.5: (88.0, 17.0, "10954"), 3.0: (98.0, 19.0, "10956"), 4.0: (110.0, 22.0, "10960"),
                5.0: (119.0, 27.0, "10964")}
BALL_TILT = 25.0
WERA454 = {2.5: (65.0, 32.0, 15.0), 3.0: (77.0, 38.0, 19.0), 4.0: (77.0, 38.0, 19.0), 5.0: (99.0, 49.0, 22.0), 2.0: (65.0, 32.0, 15.0)}
TEE_SHAFT = 100.0
TSD = dict(bit=35.0, chuck_d=16.0, chuck=50.0, handle_d=40.0, handle=105.0, hand_d=90.0)
BIT_SHANK = {2.0: 4.0, 2.5: 4.0, 3.0: 4.0, 4.0: 5.0, 5.0: 6.0}
PINCH = (46.0, 25.0, 30.0)          # on a key's arm: along the arm, across it (turning direction), along the screw axis

SOURCES = {
    "ISO 2936": "ISO 2936:2014 Table 1, from the standard's public preview (cdn.standards.iteh.ai/samples/60231/...), matches fasten.it's "
                "DIN ISO 2936 table; read 2026-11-20 13:56 UTC",
    "Bondhus": "bondhus.com/pages/ball-end (ball-end L-wrenches 10952-10964, 25 deg), read 2026-11-20 13:57 UTC",
    "Wera 454": "wera.de 454 and 454 HF T-handle hexagon screwdrivers, datasheets, read 2026-11-20 13:59-14:13 UTC",
    "Wera 7441": "wera.de Series 7400 Kraftform adjustable torque screwdrivers, 7441 (05074701001), read 2026-11-20 13:59 UTC; "
                 "Wera 840/4 Z bits, read 14:01 UTC",
    "MIL-STD-1472H": "MIL-STD-1472H (2020) Fig. 56-57, access openings for tools and hands (everyspec.com), read 2026-11-20 14:03 UTC",
    "FAA HFDS": "FAA Human Factors Design Standard ch. 14 and App. B (hand breadth, finger breadth), read 2026-11-20 14:05-14:10 UTC",
}


def _cyl(r, p0, p1, sections=16):
    return trimesh.creation.cylinder(radius=r, segment=np.array([p0, p1], float), sections=sections)


def _box(ext, centre):
    m = trimesh.creation.box(extents=ext)
    m.apply_translation(centre)
    return m


def _pack(ms):
    m = trimesh.util.concatenate(ms) if isinstance(ms, list) else ms
    return bvh(m.vertices, m.faces), np.asarray(m.vertices), m


@dataclass
class Tool:
    name: str
    s: float
    axisym: bool
    meshes: dict = field(default_factory=dict)
    note: str = ""
    torque: bool = False        # sets a known torque
    tilts: tuple = (0.0,)

    def __post_init__(self):
        # meshes: name -> (FCL BVH, vertices) for the checks; tm: name -> trimesh, for drawing
        self.tm = {k: v[2] for k, v in self.meshes.items()}
        self.meshes = {k: (v[0], v[1]) for k, v in self.meshes.items()}


def engage(s):
    """socket engagement: the key's tip sits this deep in the head."""
    return 0.6 * s


def _r(s):
    return E_MAX.get(s, 1.13 * s) / 2


def lkey_short(s):
    """Short arm in the socket, long arm swung as the lever; a pinch on the long arm's outer end."""
    L1, _, L2 = ISO2936[s]
    r = _r(s)
    h = L2 - engage(s) - r
    shaft = _cyl(r, (0, 0, 0.2), (0, 0, h + r))
    arm = _cyl(r, (0, 0, h), (L1 - r, 0, h))
    hand = _box(PINCH, (L1 - PINCH[0] / 2, 0, h))
    return Tool(f"hex key {s:g} mm, short arm in (ISO 2936 {L1:g} x {L2:g})", s, False,
                {"tool": _pack([shaft, arm]), "hand": _pack(hand)}, "ISO 2936")


def lkey_long(s, series="standard"):
    """Long arm in the socket (straight reach), short arm as the lever; a pinch on the short arm and bend."""
    L1 = ISO2936[s][0] if series == "standard" else ISO2936[s][1]
    L2 = ISO2936[s][2]
    r = _r(s)
    h = L1 - engage(s) - r
    shaft = _cyl(r, (0, 0, 0.2), (0, 0, h + r))
    arm = _cyl(r, (0, 0, h), (L2 - r, 0, h))
    hand = _box(PINCH, (max(L2 - PINCH[0] / 2, PINCH[0] / 2 - 8), 0, h))
    return Tool(f"hex key {s:g} mm, long arm in (ISO 2936 {series} {L1:g} x {L2:g})", s, False,
                {"tool": _pack([shaft, arm]), "hand": _pack(hand)}, "ISO 2936")


def ball_end(s):
    L1, L2, pn = BONDHUS_BALL[s]
    r = _r(s)
    h = L1 - engage(s) - r
    shaft = _cyl(r, (0, 0, 0.2), (0, 0, h + r))
    arm = _cyl(r, (0, 0, h), (L2 - r, 0, h))
    hand = _box(PINCH, (max(L2 - PINCH[0] / 2, PINCH[0] / 2 - 8), 0, h))
    return Tool(f"ball-end key {s:g} mm, tilted up to 25 deg (Bondhus {pn}, {L1:g} x {L2:g})", s, False,
                {"tool": _pack([shaft, arm]), "hand": _pack(hand)}, "Bondhus", tilts=(15.0, BALL_TILT))


def tee(s):
    W, H, D = WERA454.get(s, WERA454[5.0])
    r = _r(s)
    b = TEE_SHAFT
    shaft = _cyl(max(r, 2.0), (0, 0, 0.2), (0, 0, b))
    bar = _box((W, D, H), (0, 0, b + H / 2))
    hand = _box((100.0, 55.0, 60.0), (0, 0, b + H / 2 + 8))
    return Tool(f"T-handle key {s:g} mm (Wera 454 class: {b:.0f} mm shaft, {W:.0f} mm bar)", s, False,
                {"tool": _pack([shaft, bar]), "hand": _pack(hand)}, "Wera 454")


def torque_sd(s):
    t = TSD
    r = _r(s)
    z0 = 6.0                                   # hex tip length in the socket's mouth
    z1 = t["bit"]
    z2 = z1 + t["chuck"]
    z3 = z2 + t["handle"]
    tip = _cyl(r, (0, 0, 0.2), (0, 0, z0), 12)
    shank = _cyl(BIT_SHANK.get(s, 6.0) / 2, (0, 0, z0), (0, 0, z1), 12)
    chuck = _cyl(t["chuck_d"] / 2, (0, 0, z1), (0, 0, z2), 16)
    handle = _cyl(t["handle_d"] / 2, (0, 0, z2), (0, 0, z3), 24)
    hand = _cyl(t["hand_d"] / 2, (0, 0, z2 + 3), (0, 0, z3 - 3), 24)
    return Tool(f"torque screwdriver + {s:g} mm bit (Wera 7441 class, {z3:.0f} mm long)", s, True,
                {"tool": _pack([tip, shank, chuck, handle]), "hand": _pack(hand)}, "Wera 7441", torque=True)


def candidates(s, need_torque=False):
    """tools to try on a socket of size s, best first (the torque screwdriver first, so its result is always known)."""
    return [torque_sd(s), tee(s), lkey_long(s), lkey_long(s, "long"), lkey_short(s), ball_end(s)]
