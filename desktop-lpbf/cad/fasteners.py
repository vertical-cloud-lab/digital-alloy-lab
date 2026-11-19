"""Real fasteners for the desktop LPBF model (issue #260, PR #266), recreated in CadQuery from McMaster-Carr's listed
dimensions and from measurements of McMaster's own CAD, then checked against that CAD by volume (verify_fasteners.py,
results in out/fastener-check.md). McMaster's CAD files are copyrighted and are not committed: verify_fasteners.py
reads them from /tmp/mcm_cad, and fastener-cad-manifest.csv records the file, size, sha256, URL and time of each.

Every part is keyed by its McMaster part number. `shape(pn)` gives the part in its own frame, z being its axis:

    screws (shcs, captive): z = 0 is the bearing plane under the head; the head is toward +z, the shank toward -z.
    flat head screws (fhcs): z = 0 is the head's top (flush) face; the screw runs toward -z.
    set screws, dowel pins, helical inserts: z = 0 is the top face; the part runs toward -z.
    disc springs (disc) and washers/retainers (retainer): z = 0 is the bottom (bearing) face; the body is toward +z,
        so they sit under a screw head.

`place(pn, point, axis)` moves that frame so z = 0 on the axis sits at `point` and local -z points along `axis` (for a
screw: from head to tip). `detail=False` is the light shape used in the machine model and the interference checks: a
plain shank at the thread's major diameter with the head, socket, chamfers and fillets as McMaster draws them. It
matches McMaster's "3-D STEP simplified" model. `detail=True` adds the thread as revolved rings with McMaster's axial
thread profile. A helix and rings with the same axial profile have the same volume per unit length (pi * mean(r^2) over
one pitch), so the detailed shape is checked against McMaster's full "3-D STEP" (helical thread) by volume.

Helical inserts are the exception: McMaster draws a free-state coil with its driving prong (tang). Light shape: the
installed envelope, a tube from the screw's major diameter d to the STI thread's major diameter `od_installed`
(d + 1.299 P), the installed length long, so a member's hole can be cut to `od_installed`. Detailed shape: the coil as
revolved rings of the measured wire section, without the tang (it is broken off after installation).

Units mm. Prices are McMaster list prices read through the lab Pi on the date in `fetched_utc`.
"""
from __future__ import annotations

import math

import cadquery as cq

V = cq.Vector
S3 = math.sqrt(3.0)
IN = 25.4

# densities (kg/m3) for mass_g()
RHO = {"ss316": 8000.0, "ss188": 8000.0, "ss302": 7920.0, "ni718": 8190.0, "steel_zn": 7850.0}

_MCM = "https://www.mcmaster.com/{}/"
_T = "2026-11-19"   # pages and CAD read through the lab Pi between 21:17 and 21:40 UTC (per-file times: fastener-cad-manifest.csv)


# ---------------------------------------------------------------------------------------------------------------
# Catalogue
# ---------------------------------------------------------------------------------------------------------------
def _shcs(pn, d, P, L, dk, k, s, t, price, pack, b=None):
    """316 socket head screw, McMaster 92290A ('Highly Corrosion-Resistant 316 Stainless Steel', 70,000 psi).
    Measured from McMaster's models (92290A115, A144, ...): 45 deg head-edge chamfers of 0.0375*dk with 0.009375*dk blend
    radii at both ends; hex socket with corner fillets of 0.05*s, a 120 deg drill-point bottom starting at depth t, a
    90 deg entry countersink from the sharp-corner radius; a 45 deg tip chamfer down to the thread root (0.6495*P);
    thread crest and root flats P/8, depth 0.6495*P; the thread runs out under the head (or at the end of the thread
    length b on partly threaded screws) in a 60 deg half-angle cone."""
    thr = "Fully Threaded" if b is None else "Partially Threaded"
    style = "b" if (b is not None and d >= 3) else "a"
    if style == "b":
        # McMaster draws its partly threaded 92290A screws (M3 and up) differently, measured from 92290A124, A188, A334:
        # sharp 45 deg head chamfers of 0.025*dk (under the head) and 0.05*dk (top), a sharp hex socket with a flat
        # bottom (depth measured per size: M3 1.875, M4 2.25, M6 3.75), a 120 deg entry countersink, and a 45 deg tip
        # chamfer of 0.75*P.
        t = {3: 1.875, 4: 2.25, 6: 3.75}.get(d, 0.625 * d)
    return dict(kind="shcs", style=style, d=d, P=P, L=L, dk=dk, k=k, s=s, t=t, b=b, mat="ss316", price_usd=price,
                sold_as=f"pack of {pack}", pack=pack, url=_MCM.format(pn), fetched_utc=_T,
                desc=f"316 Stainless Steel Socket Head Screw, M{d:g} x {P:g} mm Thread, {L:g} mm Long, {thr}",
                head_ch=0.0375 * dk, head_rb=0.009375 * dk, sock_rc=0.05 * s, tip_ch=0.6495 * P) if style == "a" else \
        dict(kind="shcs", style=style, d=d, P=P, L=L, dk=dk, k=k, s=s, t=t, b=b, mat="ss316", price_usd=price,
             sold_as=f"pack of {pack}", pack=pack, url=_MCM.format(pn), fetched_utc=_T,
             desc=f"316 Stainless Steel Socket Head Screw, M{d:g} x {P:g} mm Thread, {L:g} mm Long, {thr}",
             head_ch_bot=0.025 * dk, head_ch_top=0.05 * dk, tip_ch=0.75 * P)


def _fhcs(pn, d, P, L, dk, s, t, margin, price, pack):
    """316 hex-drive flat head screw, 90 deg, McMaster 93395A. L is overall (McMaster measures flat heads from the top).
    Measured: a cylindrical margin `margin` at the head's top edge, then the 90 deg cone; sharp hex socket, flat bottom
    at depth t, 90 deg entry countersink; 45 deg tip chamfer of 0.75*P."""
    return dict(kind="fhcs", d=d, P=P, L=L, dk=dk, s=s, t=t, margin=margin, tip_ch=0.75 * P, mat="ss316",
                price_usd=price, sold_as=f"pack of {pack}", pack=pack, url=_MCM.format(pn), fetched_utc=_T,
                desc=f"316 Stainless Steel Hex Drive Flat Head Screw, 90 Degree Countersink, M{d:g} x {P:g} mm Thread, {L:g} mm Long")


def _set(pn, d, P, L, price, pack):
    """316 cup-point set screw, McMaster 92029A. Measured (M4): hex socket s = 2, depth 1.5, 100 deg drill point
    (50 deg half angle), 90 deg entry countersink; top edge chamfer at 55 deg half angle from r 1.659 on the top face;
    cup: 45 deg outer cone from the major radius to r 1.0 at the tip, then a 90 deg conical recess 1.0 deep."""
    return dict(kind="set", d=d, P=P, L=L, s=2.0, t=1.5, drill_half=50.0, top_r=1.659, top_half=55.0, cup_r=1.0,
                mat="ss316", price_usd=price, sold_as=f"pack of {pack}", pack=pack, url=_MCM.format(pn), fetched_utc=_T,
                desc=f"316 Stainless Steel Cup-Point Set Screw, M{d:g} x {P:g} mm Thread, {L:g} mm Long")


def _insert(pn, d, P, L, r_out, price, pack, turns):
    """18-8 helical insert, pronged, McMaster 91732A. L is the installed length. Measured wire section (every size):
    an inner thread flat P/4 wide at r_in = d/2 - 0.5413 P, 60 deg flanks to (d/2, +/-0.4375 P), flat to
    r_out - 0.6495 P, 60 deg flanks to an outer flat P/8 wide at the free-state radius r_out (measured per size).
    turns: the number of turns of wire in McMaster's model, from its length ((axial extent - wire width) / P)."""
    return dict(kind="insert", d=d, P=P, L=L, od_installed=round(d + 1.299 * P, 3), r_out=r_out, turns=turns,
                mat="ss188", price_usd=price, sold_as=f"pack of {pack}", pack=pack, url=_MCM.format(pn), fetched_utc=_T,
                desc=f"18-8 Stainless Steel Helical Threaded Insert, Pronged, M{d:g} x {P:g} mm Thread Size, {L:g} mm Installed Length")


CATALOG: dict[str, dict] = {
    # --- 316 stainless socket head screws (92290A) ---
    "92290A854": _shcs("92290A854", 2.5, 0.45, 30, 4.5, 2.5, 2.0, 1.25, 11.08, 10),
    "92290A065": _shcs("92290A065", 2.5, 0.45, 16, 4.5, 2.5, 2.0, 1.25, 5.82, 10),
    "92290A113": _shcs("92290A113", 3, 0.5, 8, 5.5, 3, 2.5, 1.5, 14.30, 50),
    "92290A115": _shcs("92290A115", 3, 0.5, 10, 5.5, 3, 2.5, 1.5, 14.84, 50),
    "92290A122": _shcs("92290A122", 3, 0.5, 20, 5.5, 3, 2.5, 1.5, 17.00, 50),
    "92290A124": _shcs("92290A124", 3, 0.5, 25, 5.5, 3, 2.5, 1.5, 19.97, 50, b=18.0),
    "92290A144": _shcs("92290A144", 4, 0.7, 10, 7.0, 4, 3.0, 2.0, 17.81, 50),
    "92290A148": _shcs("92290A148", 4, 0.7, 12, 7.0, 4, 3.0, 2.0, 18.62, 50),
    "92290A154": _shcs("92290A154", 4, 0.7, 16, 7.0, 4, 3.0, 2.0, 19.02, 50),
    "92290A168": _shcs("92290A168", 4, 0.7, 20, 7.0, 4, 3.0, 2.0, 10.40, 25),
    "92290A188": _shcs("92290A188", 4, 0.7, 50, 7.0, 4, 3.0, 2.0, 7.49, 10, b=20.0),
    "92290A228": _shcs("92290A228", 5, 0.8, 12, 8.5, 5, 4.0, 2.5, 11.47, 25),
    "92290A242": _shcs("92290A242", 5, 0.8, 20, 8.5, 5, 4.0, 2.5, 14.30, 25),
    "92290A252": _shcs("92290A252", 5, 0.8, 25, 8.5, 5, 4.0, 2.5, 15.11, 25),
    "92290A321": _shcs("92290A321", 6, 1.0, 16, 10.0, 6, 5.0, 3.0, 15.30, 25),
    "92290A326": _shcs("92290A326", 6, 1.0, 20, 10.0, 6, 5.0, 3.0, 15.79, 25),
    "92290A330": _shcs("92290A330", 6, 1.0, 25, 10.0, 6, 5.0, 3.0, 17.54, 25),
    "92290A334": _shcs("92290A334", 6, 1.0, 35, 10.0, 6, 5.0, 3.0, 9.75, 10, b=24.0),
    # --- 316 hex-drive flat head screws (93395A); head dia and height as listed: M3 6 x 1.7, M4 8 x 2.3 ---
    "93395A204": _fhcs("93395A204", 3, 0.5, 10, 6.0, 2.0, 1.02, 0.10, 15.65, 100),
    "93395A254": _fhcs("93395A254", 4, 0.7, 10, 8.0, 2.5, 1.38, 0.15, 19.97, 100),
    # --- 316 cup-point set screws (92029A) ---
    "92029A140": _set("92029A140", 4, 0.7, 4, 11.20, 50),
    "92029A142": _set("92029A142", 4, 0.7, 6, 12.38, 50),
    "92029A152": _set("92029A152", 4, 0.7, 16, 4.95, 10),
    "92029A155": _set("92029A155", 4, 0.7, 20, 6.18, 10),
    # --- 316 dowel pin, ISO 2338 m6 (93600A); measured: 15 deg (half angle) end chamfers 1.2 mm long ---
    "93600A686": dict(kind="dowel", d=6.0, L=20.0, ch_len=1.2, ch_half=15.0, mat="ss316", price_usd=7.89, sold_as="pack of 5",
                      pack=5, url=_MCM.format("93600A686"), fetched_utc=_T, tol_um="+4 to +12 (m6)",
                      desc="316 Stainless Steel Dowel Pin, 6 mm Diameter, 20 mm Long (ISO 2338 m6)"),
    # --- 18-8 helical inserts, pronged (91732A) ---
    "91732A767": _insert("91732A767", 2.5, 0.45, 3.8, 1.85, 4.26, 10, (3.744 - 0.3942) / 0.45),
    "91732A647": _insert("91732A647", 3.0, 0.5, 4.5, 2.175, 3.85, 10, (4.438 - 0.438) / 0.5),
    "91732A649": _insert("91732A649", 4.0, 0.7, 4.0, 2.8, 3.56, 10, None),
    "91732A656": _insert("91732A656", 4.0, 0.7, 6.0, 2.8, 3.68, 10, (5.912 - 0.613) / 0.7),
    "91732A261": _insert("91732A261", 5.0, 0.8, 7.5, 3.4, 3.82, 10, (7.4 - 0.7004) / 0.8),
    "91732A262": _insert("91732A262", 6.0, 1.0, 9.0, 3.975, 6.71, 10, (8.875 - 0.875) / 1.0),
    "91732A782": _insert("91732A782", 6.0, 1.0, 12.0, 3.975, 4.56, 10, (11.875 - 0.875) / 1.0),
    # --- captive panel screw and its retainer ---
    "95966A705": dict(kind="captive", d=6.0, P=1.0, L=20.0, dk=10.0, k=6.0, s=5.0, t=4.5, shank_d=4.2, thread_len=6.0,
                      top_ch=0.9, tip_ch=0.9, neck_ch=0.9, mat="ss188", price_usd=10.64, sold_as="each (1-24)", pack=1,
                      url=_MCM.format("95966A705"), fetched_utc=_T,
                      desc="Socket Head Captive Panel Screw, M6 x 1 mm Thread, 20 mm Long (6 mm thread, 4.2 mm reduced shank)"),
    "91065A610": dict(kind="retainer", d=6.0, od=8.0, id=5.2, t=0.32, mat="ss188", price_usd=13.54, sold_as="pack of 25", pack=25,
                      url=_MCM.format("91065A610"), fetched_utc=_T,
                      desc="Retainer for M6 x 1 mm Thread Size Captive Panel Screws, 18-8 Stainless Steel"),
    # --- disc (Belleville) springs. d = the screw size it fits. h0 = free cone height (H - t); H = free overall height ---
    "97125K111": dict(kind="disc", d=3.0, id=0.142 * IN, od=0.281 * IN, t=0.021 * IN, H=0.033 * IN, h0=(0.033 - 0.021) * IN,
                      work_load_N=95 * 4.448, work_defl=0.004 * IN, flat_load_N=135 * 4.448, temp_C=(-240, 593),
                      cone_deg=10.671, r_in_edge=0.0361, r_out_edge=0.0714,     # measured from McMaster's model
                      mat="ni718", price_usd=1.69, sold_as="each", pack=1, url=_MCM.format("97125K111"), fetched_utc=_T,
                      desc="Extreme-Temperature Belleville Disc Spring, 718 Nickel, for 0.138\" Shaft, 0.142\" ID, 0.281\" OD, 0.021\" Thick"),
    "9713K54": dict(kind="disc", d=2.5, id=0.125 * IN, od=0.25 * IN, t=0.013 * IN, H=0.020 * IN, h0=(0.020 - 0.013) * IN,
                    work_load_N=26 * 4.448, work_defl=0.003 * IN, flat_load_N=48 * 4.448, temp_C=None,
                    cone_deg=None, r_in_edge=0.0, r_out_edge=0.0,
                    mat="ss302", price_usd=11.81, sold_as="pack of 12", pack=12, url=_MCM.format("9713K54"), fetched_utc=_T,
                    note="fits an M2.5 shank, but its 6.35 mm OD does not fit a 5 mm counterbore; 302 stainless",
                    desc="Belleville Disc Spring, 302 Stainless Steel, for 1/8\" Shaft, 0.125\" ID, 0.25\" OD, 0.013\" Thick"),
}


# ---------------------------------------------------------------------------------------------------------------
# 2-D profile helpers: closed (r, z) paths revolved about z
# ---------------------------------------------------------------------------------------------------------------
def _unit(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy)
    return dx / n, dy / n


def _fillet_path(pts, radii):
    """Closed polyline with a fillet radius per vertex (0 = sharp) -> segments ('L', pt) / ('A', mid, end)."""
    n = len(pts)
    segs = []
    for i in range(n):
        p0, p, p1 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = radii[i]
        if r <= 0:
            segs.append(("L", p))
            continue
        u, v = _unit(p0, p), _unit(p, p1)
        th = math.acos(max(-1.0, min(1.0, u[0] * v[0] + u[1] * v[1])))
        if th < 1e-9:
            segs.append(("L", p))
            continue
        tl = r * math.tan(th / 2)
        t1 = (p[0] - u[0] * tl, p[1] - u[1] * tl)
        t2 = (p[0] + v[0] * tl, p[1] + v[1] * tl)
        bx, by = v[0] - u[0], v[1] - u[1]
        bn = math.hypot(bx, by)
        dm = r / math.cos(th / 2) - r
        segs.append(("L", t1))
        segs.append(("A", (p[0] + bx / bn * dm, p[1] + by / bn * dm), t2))
    return segs


def _revolve(segs, angle=360.0):
    w = cq.Workplane("XZ").moveTo(*segs[0][1])
    for s in segs[1:]:
        w = w.lineTo(*s[1]) if s[0] == "L" else w.threePointArc(s[1], s[2])
    return w.close().revolve(angle, (0, 0, 0), (0, 1, 0)).val()


def _poly(pts, angle=360.0):
    return cq.Workplane("XZ").polyline(pts).close().revolve(angle, (0, 0, 0), (0, 1, 0)).val()


def _frustum(r0, z0, r1, z1):
    """Cone frustum from radius r0 at z0 to r1 at z1 (z1 > z0)."""
    return cq.Solid.makeCone(r0, r1, z1 - z0, V(0, 0, z0), V(0, 0, 1))


def _hex_prism(s, rc, z0, h):
    sk = cq.Sketch().regularPolygon(s / S3, 6)
    if rc > 0:
        sk = sk.vertices().fillet(rc)
    return cq.Workplane("XY").workplane(offset=z0).placeSketch(sk).extrude(h).val()


def _socket(s, depth, top, rc=0.0, drill_half=None, csk_half=45.0):
    """Hex socket cut from z = top down to top - depth, sharp-corner countersink at the top, optional drill point."""
    cut = _hex_prism(s, rc, top - depth, depth + 1.0)
    rcorner = s / S3
    h = (rcorner - s / 2) / math.tan(math.radians(csk_half))
    cut = cut.fuse(_frustum(s / 2, top - h, s / 2 + (h + 1.0) * math.tan(math.radians(csk_half)), top + 1.0))
    if drill_half:
        cut = cut.fuse(cq.Solid.makeCone(s / 2, 0.0, (s / 2) / math.tan(math.radians(drill_half)), V(0, 0, top - depth), V(0, 0, -1)))
    return cut


# ---------------------------------------------------------------------------------------------------------------
# Threads (detail=True): revolved rings with McMaster's axial profile
# ---------------------------------------------------------------------------------------------------------------
def thread_profile(d, P):
    """(r_crest, r_root, crest_w, root_w, flank_w): symmetric, crest and root flats P/8, depth 0.6495*P (= 0.75 H)."""
    rc = d / 2
    w = P / 8
    return rc, rc - 0.6495190528 * P, w, w, (P - 2 * w) / 2


def thread_area(d, P):
    """Cross-section area of the threaded shank: pi * mean(r^2) over one pitch."""
    rc, rr, wc, wr, wf = thread_profile(d, P)
    return math.pi * (wc * rc ** 2 + wr * rr ** 2 + 2 * wf * (rc * rc + rc * rr + rr * rr) / 3) / P


def _thread_cutter(d, P, z0, z1, phase=0.0):
    """Grooves to subtract from a plain shank of radius d/2 between z0 and z1 (crest flats centred at z0 + phase + nP)."""
    rc, rr, wc, wr, wf = thread_profile(d, P)
    big = rc + 1.0
    solids = []
    zc = z0 + (phase % P) - P
    while zc < z1 + P:
        a = zc + wc / 2
        b, c, e = a + wf, a + wf + wr, a + 2 * wf + wr
        solids.append(_poly([(rc, a), (rr, b), (rr, c), (rc, e), (big, e), (big, a)]))
        zc += P
    out = solids[0]
    for s in solids[1:]:
        out = out.fuse(s)
    return out.clean().intersect(cq.Solid.makeCylinder(big + 1, z1 - z0, V(0, 0, z0), V(0, 0, 1)))


def _add_thread(body, d, P, z0, z1, runout_top=True):
    """Cut the thread into body between z0 (tip end) and z1; at z1 the thread runs out in a 60 deg half-angle cone."""
    cut = _thread_cutter(d, P, z0, z1)
    if runout_top:
        R = d / 2
        cut = cut.cut(cq.Solid.makeCone(R, 0.0, R / math.tan(math.radians(60)), V(0, 0, z1), V(0, 0, -1)))
    return body.cut(cut)


# ---------------------------------------------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------------------------------------------
def _g_shcs(c, detail=False):
    d, P, L, dk, k, s, t = c["d"], c["P"], c["L"], c["dk"], c["k"], c["s"], c["t"]
    R, Rk, tch = d / 2, dk / 2, c["tip_ch"]
    if c.get("style") == "b":
        cb, ct = c["head_ch_bot"], c["head_ch_top"]
        body = _poly([(0.0, -L), (R - tch, -L), (R, -L + tch), (R, 0.0), (Rk - cb, 0.0), (Rk, cb), (Rk, k - ct), (Rk - ct, k), (0.0, k)])
        body = body.cut(_socket(s, t, k, csk_half=60.0))
    else:
        ch, rb = c["head_ch"], c["head_rb"]
        pts = [(0.0, -L), (R - tch, -L), (R, -L + tch), (R, 0.0), (Rk - ch, 0.0), (Rk, ch), (Rk, k - ch), (Rk - ch, k), (0.0, k)]
        body = _revolve(_fillet_path(pts, [0, 0, 0, 0, rb, rb, rb, rb, 0]))
        body = body.cut(_socket(s, t, k, rc=c["sock_rc"], drill_half=60.0, csk_half=45.0))
    if detail:
        z1 = 0.0 if not c.get("b") else -L + c["b"]
        body = _add_thread(body, d, P, -L, z1)
    return body.clean()


def _g_fhcs(c, detail=False):
    d, P, L, dk, s, t, m, tch = c["d"], c["P"], c["L"], c["dk"], c["s"], c["t"], c["margin"], c["tip_ch"]
    R, Rk = d / 2, dk / 2
    zc = -(m + (Rk - R))                                     # bottom of the 90 deg head cone
    body = _poly([(0.0, -L), (R - tch, -L), (R, -L + tch), (R, zc), (Rk, -m), (Rk, 0.0), (0.0, 0.0)])
    body = body.cut(_socket(s, t, 0.0, csk_half=45.0))
    if detail:
        body = _add_thread(body, d, P, -L, zc)
    return body.clean()


def _g_set(c, detail=False):
    d, P, L, s, t = c["d"], c["P"], c["L"], c["s"], c["t"]
    R, rt, rcup = d / 2, c["top_r"], c["cup_r"]
    ztop_ch = -(R - rt) / math.tan(math.radians(c["top_half"]))
    zcup = -L + (R - rcup)                                   # top of the 45 deg cup cone
    body = _poly([(0.0, -L + rcup), (rcup, -L), (R, zcup), (R, ztop_ch), (rt, 0.0), (0.0, 0.0)])
    body = body.cut(_socket(s, t, 0.0, drill_half=c["drill_half"], csk_half=45.0))
    if detail:
        body = _add_thread(body, d, P, -L, 0.0, runout_top=False)
    return body.clean()


def _g_dowel(c, detail=False):
    R, L, cl = c["d"] / 2, c["L"], c["ch_len"]
    re = R - cl * math.tan(math.radians(c["ch_half"]))
    return _poly([(0.0, -L), (re, -L), (R, -L + cl), (R, -cl), (re, 0.0), (0.0, 0.0)])


def insert_section(c):
    """Measured wire section of a helical insert, as (r, dz) about the wire's centre plane."""
    d, P, ro = c["d"], c["P"], c["r_out"]
    ri, rm = d / 2 - 0.5413 * P, ro - 0.6495 * P
    return [(ri, -0.125 * P), (d / 2, -0.4375 * P), (rm, -0.4375 * P), (ro, -0.0625 * P),
            (ro, 0.0625 * P), (rm, 0.4375 * P), (d / 2, 0.4375 * P), (ri, 0.125 * P)]


def _g_insert(c, detail=False):
    d, P, L = c["d"], c["P"], c["L"]
    if not detail:
        return cq.Solid.makeCylinder(c["od_installed"] / 2, L, V(0, 0, -L), V(0, 0, 1)).cut(
            cq.Solid.makeCylinder(d / 2, L, V(0, 0, -L), V(0, 0, 1)))
    turns = c["turns"] if c["turns"] else (L - 0.875 * P) / P
    sec = insert_section(c)
    rings = []
    n_full = int(math.floor(turns))
    w2 = 0.4375 * P
    for i in range(n_full):
        zc = -w2 - i * P
        rings.append(_poly([(r, zc + dz) for r, dz in sec]))
    frac = turns - n_full
    if frac > 1e-3:
        zc = -w2 - n_full * P
        rings.append(_poly([(r, zc + dz) for r, dz in sec], 360.0 * frac))
    out = rings[0]
    for r in rings[1:]:
        out = out.fuse(r)
    return out.clean()


def _g_captive(c, detail=False):
    d, P, L, dk, k, s, t = c["d"], c["P"], c["L"], c["dk"], c["k"], c["s"], c["t"]
    R, Rk, Rs = d / 2, dk / 2, c["shank_d"] / 2
    zt = -L + c["thread_len"]                                # start of the threaded part (below the reduced shank)
    nc, tc, hc = c["neck_ch"], c["tip_ch"], c["top_ch"]
    body = _poly([(0.0, -L), (Rs, -L), (R, -L + tc), (R, zt - nc), (Rs, zt), (Rs, 0.0), (Rk, 0.0), (Rk, k - hc), (Rk - hc, k), (0.0, k)])
    body = body.cut(_socket(s, t, k, csk_half=60.0))
    if detail:
        cut = _thread_cutter(d, P, -L, zt)
        body = body.cut(cut)
    return body.clean()


def _g_retainer(c, detail=False):
    return cq.Solid.makeCylinder(c["od"] / 2, c["t"], V(0, 0, 0), V(0, 0, 1)).cut(
        cq.Solid.makeCylinder(c["id"] / 2, c["t"], V(0, 0, 0), V(0, 0, 1)))


def _g_disc(c, detail=False):
    """Conical disc: a t-thick ring section tilted by the cone angle (inner edge up), revolved; edge blends as measured."""
    ri, ro, t, H = c["id"] / 2, c["od"] / 2, c["t"], c["H"]
    th = math.radians(c["cone_deg"]) if c["cone_deg"] else math.atan((H - t) / (ro - ri))
    u = (math.cos(th), -math.sin(th))                       # along the section, outward and down
    n = (math.sin(th), math.cos(th))                        # normal, up
    w = (ro - ri) / math.cos(th) - t * math.tan(th) if c["cone_deg"] else (ro - ri) / math.cos(th)
    # inner-bottom corner at (ri, 0) before rounding; build the rectangle in (u, n)
    p0 = (ri, 0.0)
    pts = [p0, (p0[0] + u[0] * w, p0[1] + u[1] * w), (p0[0] + u[0] * w + n[0] * t, p0[1] + u[1] * w + n[1] * t), (p0[0] + n[0] * t, p0[1] + n[1] * t)]
    ri_e, ro_e = c["r_in_edge"], c["r_out_edge"]
    body = _revolve(_fillet_path(pts, [ri_e, ro_e, ro_e, ri_e])) if (ri_e or ro_e) else _poly(pts)
    bb = body.BoundingBox()
    return body.translate(V(0, 0, -bb.zmin))


GEN = {"shcs": _g_shcs, "fhcs": _g_fhcs, "set": _g_set, "dowel": _g_dowel, "insert": _g_insert, "captive": _g_captive,
       "retainer": _g_retainer, "disc": _g_disc}

_cache: dict[tuple, cq.Solid] = {}


def shape(pn: str, detail: bool = False) -> cq.Solid:
    """The part in its own frame (see the module docstring). Cached; callers get the same object, so use place()/moved()."""
    key = (pn, bool(detail))
    if key not in _cache:
        c = CATALOG[pn]
        _cache[key] = GEN[c["kind"]](c, detail=detail)
    return _cache[key]


def place(pn: str, point, axis, detail: bool = False, spin: float = 0.0) -> cq.Shape:
    """The part moved so z = 0 on its axis is at `point` and its local -z (head -> tip) points along `axis`."""
    s = shape(pn, detail)
    if spin:
        s = s.rotate(V(0, 0, 0), V(0, 0, 1), spin)
    zdir = V(*axis).normalized() * -1.0
    ref = V(1, 0, 0) if abs(zdir.x) < 0.9 else V(0, 1, 0)
    xdir = (ref - zdir * ref.dot(zdir)).normalized()
    return s.moved(cq.Location(cq.Plane(origin=V(*point), xDir=xdir, normal=zdir)))


def find(kind: str, d: float, L: float | None = None) -> str:
    """Part number by kind, thread size and length (L ignored for discs)."""
    hits = [pn for pn, c in CATALOG.items() if c["kind"] == kind and abs(c["d"] - d) < 1e-6 and (L is None or abs(c.get("L", 0) - L) < 1e-6)]
    if not hits:
        raise KeyError(f"no {kind} M{d:g} x {L}")
    return hits[0]


_mass: dict[str, float] = {}


def mass_g(pn: str) -> float:
    """Mass from the detailed volume (threads as McMaster draws them) and the material density."""
    if pn not in _mass:
        _mass[pn] = shape(pn, detail=True).Volume() * 1e-9 * RHO[CATALOG[pn]["mat"]] * 1000.0
    return _mass[pn]
