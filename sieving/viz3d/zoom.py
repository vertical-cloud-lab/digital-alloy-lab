"""The magnifier for the sieving step: a soft-sphere DEM of the powder on a patch of the No. 230 mesh.

steps.py calls ``Zoom.advance()`` and ``Zoom.render()`` once a frame and pastes the image into the frame as a circular
inset pointed at the No. 230. It shows what the sieve does at the particles' scale: the fines (< 63 um, blue) drop
through the openings and fall out of the bottom, the coarse (orange) stay on the wires, and a few particles just over
63 um wedge into openings and stay (blinding). Units are um, ms and ng, so forces are in pN and g = 9.81 um/ms^2.

Real numbers:

* The mesh: ASTM E11 No. 230, plain-woven 304 stainless, 63 um opening and 44 um wire (nominal, wovenwire.com's
  E11 table), so a 107 um pitch. Each wire's centreline waves +-22 um (half a wire diameter), so warp and weft
  touch at every crossover.
* The powder: Al, 2.7 g/cm3, log-normal by volume with D10/D50/D90 = 40/53/70 um (ultrasonically atomized AlSi12
  on the 35 kHz ATO Lab, the numbers our doc cites), plus three 85-120 um agglomerates, so 74 % of the mass is
  under 63 um. Nothing is over 250 um: the No. 60 above has taken it.
* Gravity, and Stokes drag in air (1.8e-5 Pa s) moving with the sieve.

Chosen:

* The patch is 6 x 6 openings (even, so the weave repeats), periodic in x and y, and drawn with its periodic images
  so the circle never shows an edge. 474 particles (the finest tail clipped at 30 um) make a bed about three deep;
  they start as a loose cloud just above the mesh and land in the first second (the pour).
* Contacts: linear spring-dashpot, stiffness 3e4 pN/um per um of effective radius (a 50 um particle landing at
  70 um/ms overlaps a wire by under 7 % of its radius, at rest by far under 1 %), restitution 0.3, Coulomb friction
  0.45 capped by a viscous tangential force. The spheres turn (I = 0.4 m r^2), with rolling resistance 0.03.
  Wires are chains of capsules, 8 a pitch, one contact a wire. Step about 2.4 us, a twelfth of the shortest contact.
* SLOWMO = 50: one second of animation is 20 ms at the sieve, so a fine takes about a third of a second to fall
  out of the bottom.
* Agitation, exaggerated, as a pseudo-force in the mesh's frame. At the bench, hand sieving is a ~2 Hz circle of
  +-5-10 mm (0.1-0.3 g, turning) and a tap every ~0.6 s; the 9 s of animation are only 180 ms of that, a third of
  one circle and no tap, and 0.3 g can't roll a sphere out of the pocket between wires (that takes ~0.65 g). So both
  run on the animation's clock, not the slowed one: the gyration is 0.8 g turning once a second of animation, and a
  tap kicks every particle up at 30 um/ms over 0.25 ms (the bed hops about 45 um and lands a third of a second
  later). What is cut is the bed at rest between taps. ``agitation`` scales both.
* Blinding: a particle bigger than the opening but under 67 um sits in it with its four wire contacts within 15 deg
  of horizontal (tan 0.28, under the friction of 0.45 with a margin), so friction can hold it like a cork once
  something pushes it in. A model with no static friction can't hold it, so a particle like that, centred in an
  opening and pressed into it with more than four times its weight, is locked there for good (counted as wedged).

    xvfb-run -a -s "-screen 0 1920x1080x24" python zoom.py      # /tmp/zoom_demo.gif and /tmp/zoom_sheet.png
"""
from __future__ import annotations

import math
import time
from statistics import NormalDist

import numpy as np
from numba import njit, prange

FINE, MID, GRIT = (0.20, 0.45, 0.85), (0.95, 0.55, 0.15), (0.30, 0.30, 0.33)   # <63 um, 63-250 um, >250 um
BG = (0.95, 0.95, 0.95)
STEEL = (0.72, 0.74, 0.77)
INK = (0.13, 0.13, 0.15)                # ring and scale bar

SLOWMO = 50.0                           # animation time / time at the sieve

# ------------------------------------------------------------------------------------------- the mesh
OPEN, WIRE = 63.0, 44.0                 # um, ASTM E11 No. 230
PITCH = OPEN + WIRE                     # 107
RW = WIRE / 2
CRIMP = RW                              # centreline amplitude: warp and weft +-22 um at a crossover
NCELL = 6                               # openings across the periodic patch
LBOX = NCELL * PITCH                    # 642
SEG = 8                                 # capsules a pitch (a power of 2: indices are masked)
HSEG = PITCH / SEG
MESH_TOP = CRIMP + RW                   # 44: top of the knuckles; the bottom is at -44
ZTAB = CRIMP * np.cos(np.pi * np.arange(2 * SEG) / SEG)     # centreline height at the capsule ends

# ------------------------------------------------------------------------------------------ the powder
RHO = 2.7e-3                            # ng/um^3
GRAV = 9.81                             # um/ms^2
MU_AIR = 1.8e-2                         # ng/(um ms), 1.8e-5 Pa s
D10, D50, D90 = 40.0, 53.0, 70.0        # um, by volume
N_MAIN = 471
AGGLOM = (85.0, 100.0, 120.0)           # um
D_MIN = 30.0                            # the finest tail is clipped here, for the time step
PACK0 = 0.25                            # solid fraction of the poured cloud

# ------------------------------------------------------------------------------------------- contacts
K0 = 3.0e4                              # pN/um per um of effective radius
E_REST = 0.3
CN = 2.0 * -math.log(E_REST) / math.sqrt(math.pi ** 2 + math.log(E_REST) ** 2)   # 2 x damping ratio
MU = 0.45
GT = 1.0                                # tangential viscous coefficient / normal one
MU_R = 0.03                             # rolling resistance
SKIN = 10.0                             # um, neighbour-list margin
MAXN = 128

# ------------------------------------------------------------------------------------------ agitation
A_GYR = 0.8 * GRAV                      # um/ms^2 (bench: 0.1-0.3 g)
GYR_REV_S = 1.0                         # turns a second of animation
TAP_DV = 30.0                           # um/ms
TAP_MS = 0.25                           # ms at the sieve

# ---------------------------------------------------------------------------------------- bookkeeping
Z_GONE = -300.0                         # passed particles are dropped below this
FADE_TOP = -MESH_TOP - 20.0             # and fade into the background from here down
D_LOCK = 67.0                           # um, see the docstring
F_LOCK = 4.0                            # x own weight
LOCK_OFF = 0.2                          # max offset from an opening's centre, in pitches

# --------------------------------------------------------------------------------------------- camera
CAM_EL, CAM_AZ = 40.0, -68.0            # deg; looking from -y, turned a little
CAM_FOV = 22.0                          # deg
VIEW_W = 4.5 * PITCH                    # um across the circle at the focal point
FOCAL_Z = 20.0
AA = "fxaa"


# ============================================================================================ DEM
@njit(cache=True, fastmath=True, inline="always")
def _contact(nx, ny, nz, delta, k, g, ri, vx, vy, vz, sx, sy, sz):
    """Force on a particle and the torque about its centre, at a contact with normal n (pointing into it) and
    overlap delta; (vx, vy, vz) is its velocity relative to the other body, s = ri w_i (+ rj w_j)."""
    vn = vx * nx + vy * ny + vz * nz
    fn = k * delta - g * vn
    if fn < 0.0:
        fn = 0.0
    # slip of the contact point: relative velocity minus s x n, its tangential part
    cx = vx - (sy * nz - sz * ny)
    cy = vy - (sz * nx - sx * nz)
    cz = vz - (sx * ny - sy * nx)
    cn = cx * nx + cy * ny + cz * nz
    tx, ty, tz = cx - cn * nx, cy - cn * ny, cz - cn * nz
    vt = math.sqrt(tx * tx + ty * ty + tz * tz)
    ftx = 0.0
    fty = 0.0
    ftz = 0.0
    if vt > 1e-9:
        ft = min(GT * g * vt, MU * fn) / vt
        ftx, fty, ftz = -ft * tx, -ft * ty, -ft * tz
    # torque = (-ri n) x Ft
    qx = -ri * (ny * ftz - nz * fty)
    qy = -ri * (nz * ftx - nx * ftz)
    qz = -ri * (nx * fty - ny * ftx)
    return fn * nx + ftx, fn * ny + fty, fn * nz + ftz, qx, qy, qz, fn


@njit(cache=True, fastmath=True, parallel=True)
def _substep(p0, v0, w0, p1, v1, w1, rad, mass, idrag, flag, nbr, nn, ax, ay, az, dt, nwc, fwz):
    """One explicit step: forces from (p0, v0, w0), the new state into (p1, v1, w1). flag: 0 on the mesh,
    1 passed, 2 gone, 3 wedged (fixed)."""
    n = p0.shape[0]
    half = 0.5 * LBOX
    for i in prange(n):
        fi = flag[i]
        if fi >= 2:
            for c in range(3):
                p1[i, c] = p0[i, c]
                v1[i, c] = 0.0
                w1[i, c] = 0.0
            nwc[i] = 0
            fwz[i] = 0.0
            continue
        xi, yi, zi = p0[i, 0], p0[i, 1], p0[i, 2]
        vxi, vyi, vzi = v0[i, 0], v0[i, 1], v0[i, 2]
        ri = rad[i]
        mi = mass[i]
        sxi, syi, szi = ri * w0[i, 0], ri * w0[i, 1], ri * w0[i, 2]
        fx = 0.0
        fy = 0.0
        fz = 0.0
        qx = 0.0
        qy = 0.0
        qz = 0.0
        roll = 0.0                                           # rolling-resistance torque available
        # particle-particle (a passed particle falls free, below everything else)
        for kk in range(nn[i] if fi == 0 else 0):
            j = nbr[i, kk]
            fj = flag[j]
            if fj == 1 or fj == 2:
                continue
            dx = xi - p0[j, 0]
            if dx > half:
                dx -= LBOX
            elif dx < -half:
                dx += LBOX
            dy = yi - p0[j, 1]
            if dy > half:
                dy -= LBOX
            elif dy < -half:
                dy += LBOX
            dz = zi - p0[j, 2]
            rj = rad[j]
            rs = ri + rj
            d2 = dx * dx + dy * dy + dz * dz
            if d2 >= rs * rs or d2 == 0.0:
                continue
            d = math.sqrt(d2)
            mj = mass[j]
            meff = mi if fj == 3 else mi * mj / (mi + mj)
            k = K0 * ri * rj / rs
            g = CN * math.sqrt(k * meff)
            gx, gy, gz, tx, ty, tz, fn = _contact(dx / d, dy / d, dz / d, rs - d, k, g, ri,
                                                  vxi - v0[j, 0], vyi - v0[j, 1], vzi - v0[j, 2],
                                                  sxi + rj * w0[j, 0], syi + rj * w0[j, 1], szi + rj * w0[j, 2])
            fx += gx
            fy += gy
            fz += gz
            qx += tx
            qy += ty
            qz += tz
            roll += MU_R * ri * fn
        # wires: one contact a wire, at its nearest capsule
        nw = 0
        fws = 0.0
        if fi == 0 and zi - ri < MESH_TOP and zi + ri > -MESH_TOP:
            reach = ri + RW
            kw = K0 * ri * RW / reach
            gw = CN * math.sqrt(kw * mi)
            rr = reach * reach
            for axis in range(2):
                # warps (axis 0) run along x at y = j * PITCH, centreline z = s_j * ZTAB; wefts the other way
                u = xi if axis == 0 else yi                  # along the wire
                o = yi if axis == 0 else xi                  # across
                j0 = int(math.floor((o - reach) / PITCH))
                j1 = int(math.floor((o + reach) / PITCH))
                k0 = int(math.floor((u - reach) / HSEG))
                k1 = int(math.floor((u + reach) / HSEG))
                for jw in range(j0, j1 + 1):
                    dov = o - jw * PITCH
                    if abs(dov) >= reach:
                        continue
                    s = 1.0 if (jw & 1) == 0 else -1.0
                    if axis == 1:
                        s = -s
                    best = 1e30
                    bu = 0.0
                    bz = 0.0
                    for k in range(k0, k1 + 1):
                        ua = k * HSEG
                        za = s * ZTAB[k & (2 * SEG - 1)]
                        ez = s * ZTAB[(k + 1) & (2 * SEG - 1)] - za
                        t = ((u - ua) * HSEG + (zi - za) * ez) / (HSEG * HSEG + ez * ez)
                        t = min(max(t, 0.0), 1.0)
                        cu = u - ua - t * HSEG
                        cz = zi - za - t * ez
                        dd = cu * cu + dov * dov + cz * cz
                        if dd < best:
                            best, bu, bz = dd, cu, cz
                    if best < rr:
                        d = math.sqrt(best)
                        if axis == 0:
                            nx, ny = bu / d, dov / d
                        else:
                            nx, ny = dov / d, bu / d
                        gx, gy, gz, tx, ty, tz, fn = _contact(nx, ny, bz / d, reach - d, kw, gw, ri,
                                                              vxi, vyi, vzi, sxi, syi, szi)
                        fx += gx
                        fy += gy
                        fz += gz
                        qx += tx
                        qy += ty
                        qz += tz
                        roll += MU_R * ri * fn
                        fws += fn * bz / d
                        nw += 1
        nwc[i] = nw
        fwz[i] = fws
        # semi-implicit Euler, with gravity, the pseudo-force and Stokes drag
        dr = idrag[i]
        nvx = vxi + (fx / mi + ax - vxi * dr) * dt
        nvy = vyi + (fy / mi + ay - vyi * dr) * dt
        nvz = vzi + (fz / mi + az - vzi * dr) * dt
        x = xi + nvx * dt
        y = yi + nvy * dt
        if x >= LBOX:
            x -= LBOX
        elif x < 0.0:
            x += LBOX
        if y >= LBOX:
            y -= LBOX
        elif y < 0.0:
            y += LBOX
        p1[i, 0] = x
        p1[i, 1] = y
        p1[i, 2] = zi + nvz * dt
        v1[i, 0] = nvx
        v1[i, 1] = nvy
        v1[i, 2] = nvz
        # spin (I = 0.4 m r^2), then rolling resistance takes off up to roll * dt / I
        ii = 2.5 / (mi * ri * ri)
        wx = w0[i, 0] + qx * ii * dt
        wy = w0[i, 1] + qy * ii * dt
        wz = w0[i, 2] + qz * ii * dt
        wn = math.sqrt(wx * wx + wy * wy + wz * wz)
        if wn > 0.0:
            c = max(0.0, 1.0 - roll * ii * dt / wn)
            wx *= c
            wy *= c
            wz *= c
        w1[i, 0] = wx
        w1[i, 1] = wy
        w1[i, 2] = wz


@njit(cache=True, fastmath=True, parallel=True)
def _build(p, rad, flag, nbr, nn):
    """Full neighbour lists (both i->j and j->i), everything within the sum of radii plus SKIN."""
    n = p.shape[0]
    half = 0.5 * LBOX
    for i in prange(n):
        c = 0
        if flag[i] == 0:
            for j in range(n):
                if j == i or flag[j] == 1 or flag[j] == 2:
                    continue
                dx = p[i, 0] - p[j, 0]
                if dx > half:
                    dx -= LBOX
                elif dx < -half:
                    dx += LBOX
                dy = p[i, 1] - p[j, 1]
                if dy > half:
                    dy -= LBOX
                elif dy < -half:
                    dy += LBOX
                dz = p[i, 2] - p[j, 2]
                rc = rad[i] + rad[j] + SKIN
                if dx * dx + dy * dy + dz * dz < rc * rc and c < MAXN:
                    nbr[i, c] = j
                    c += 1
        nn[i] = c


@njit(cache=True)
def _frame(p, v, om, q, w, wo, rad, mass, idrag, flag, nbr, nn, pref, nwc, fwz, nsub, dt, agyr, ph0, dph, ntap,
           atap, d_lock, f_lock, lock_off):
    """nsub steps of one animation frame; updates the flags and rebuilds the neighbour lists as needed."""
    n = p.shape[0]
    half = 0.5 * LBOX
    lim2 = (0.5 * SKIN) ** 2
    for s in range(nsub):
        ph = ph0 + dph * s
        az = -GRAV + (atap if s < ntap else 0.0)
        _substep(p, v, om, q, w, wo, rad, mass, idrag, flag, nbr, nn, agyr * math.cos(ph), agyr * math.sin(ph), az,
                 dt, nwc, fwz)
        p[:, :] = q
        v[:, :] = w
        om[:, :] = wo
        far = 0.0
        for i in range(n):
            fl = flag[i]
            if fl == 0:
                if p[i, 2] + rad[i] < -MESH_TOP:
                    flag[i] = 1
                elif nwc[i] >= 3 and OPEN < 2.0 * rad[i] < d_lock and fwz[i] > f_lock * mass[i] * GRAV:
                    ox = p[i, 0] / PITCH
                    oy = p[i, 1] / PITCH
                    if abs(ox - math.floor(ox) - 0.5) < lock_off and abs(oy - math.floor(oy) - 0.5) < lock_off:
                        flag[i] = 3
                        v[i, 0] = 0.0
                        v[i, 1] = 0.0
                        v[i, 2] = 0.0
                        om[i, 0] = 0.0
                        om[i, 1] = 0.0
                        om[i, 2] = 0.0
            elif fl == 1 and p[i, 2] < Z_GONE:
                flag[i] = 2
            if flag[i] == 0:
                dx = p[i, 0] - pref[i, 0]
                if dx > half:
                    dx -= LBOX
                elif dx < -half:
                    dx += LBOX
                dy = p[i, 1] - pref[i, 1]
                if dy > half:
                    dy -= LBOX
                elif dy < -half:
                    dy += LBOX
                dz = p[i, 2] - pref[i, 2]
                far = max(far, dx * dx + dy * dy + dz * dz)
        if far > lim2:
            _build(p, rad, flag, nbr, nn)
            pref[:, :] = p


# ======================================================================================== the inset
def _psd():
    """Diameters: the log-normal at evenly spaced quantiles (by number), plus the agglomerates."""
    sig = math.log(D90 / D50) / NormalDist().inv_cdf(0.9)
    med_n = D50 * math.exp(-3.0 * sig * sig)          # number median of a log-normal whose volume median is D50
    z = np.array([NormalDist().inv_cdf((k + 0.5) / N_MAIN) for k in range(N_MAIN)])
    d = np.maximum(med_n * np.exp(sig * z), D_MIN)
    return np.concatenate([d, AGGLOM])


def _pour(d, rng):
    """Random sequential placement in a loose cloud above the mesh, largest first."""
    vol = float(np.sum(np.pi / 6 * d ** 3))
    z0 = MESH_TOP + 10.0
    z1 = z0 + vol / (LBOX * LBOX * PACK0)
    pos = np.zeros((len(d), 3))
    done = np.zeros(len(d), bool)
    for i in np.argsort(-d):
        r = d[i] / 2
        for _ in range(20000):
            c = np.array([rng.uniform(0, LBOX), rng.uniform(0, LBOX), rng.uniform(z0 + r, z1 - r)])
            dd = pos[done] - c
            dd[:, :2] -= LBOX * np.round(dd[:, :2] / LBOX)
            if not len(dd) or np.min(np.einsum("ij,ij->i", dd, dd) - (d[done] / 2 + r + 1.0) ** 2) > 0:
                break
        pos[i] = c
        done[i] = True
    return pos


def _wave(t):
    return CRIMP * np.cos(np.pi * t / PITCH)


class Zoom:
    """The powder on a patch of No. 230 mesh, stepped once a frame and drawn as a circular magnifier.

    advance(dt_anim, agitation, tap): one animation frame (dt_anim in s of animation, normally 1/15). The micro-scale
    runs in slow motion, SLOWMO = 50 (a frame of 1/15 s is 1.33 ms at the sieve, ~550 DEM steps). agitation 0..1
    scales the gyration (0.8 g, turning once a second of animation) and the tap; tap=True kicks the bed up once this
    frame. Both are exaggerated and time-compressed against the bench, see the module docstring.

    The kernels are Numba prange loops launched once a DEM step; in a process that shares the CPU, run them on one
    thread (NUMBA_NUM_THREADS=1), where a frame costs ~20 ms.
    
    """

    def __init__(self, size_px: int = 300, seed: int = 0):
        import pyvista as pv

        self.size = int(size_px)
        rng = np.random.default_rng(seed)
        d = _psd()
        self._n = n = len(d)
        self._rad = d / 2
        self._mass = RHO * np.pi / 6 * d ** 3
        self._idrag = 18.0 * MU_AIR / (RHO * d ** 2)     # 1 / Stokes relaxation time
        self._p = _pour(d, rng)
        self._v = np.zeros((n, 3))
        self._om = np.zeros((n, 3))                     # spin, rad/ms
        self._q = np.zeros((n, 3))
        self._w = np.zeros((n, 3))
        self._wo = np.zeros((n, 3))
        self._flag = np.zeros(n, np.int8)
        self._nbr = np.zeros((n, MAXN), np.int32)
        self._nn = np.zeros(n, np.int32)
        self._nwc = np.zeros(n, np.int32)
        self._fwz = np.zeros(n)
        _build(self._p, self._rad, self._flag, self._nbr, self._nn)
        self._pref = self._p.copy()
        self._phase = 0.0
        # time step from the stiffest, lightest contact: two of the smallest particles
        r0, m0 = self._rad.min(), self._mass.min()
        tc = min(math.pi * math.sqrt(0.5 * m0 / (K0 * r0 / 2)), math.pi * math.sqrt(m0 / (K0 * r0 * RW / (r0 + RW))))
        self._dt = tc / 12.0
        self.fine = d < OPEN
        base = np.where(d < OPEN, 0, np.where(d < 250.0, 1, 2))
        shade = 1.0 + 0.06 * (rng.random(n) - 0.5)
        self._col = np.clip(np.array([FINE, MID, GRIT])[base] * shade[:, None], 0, 1)
        self.fine_mass_frac = float(self._mass[d < OPEN].sum() / self._mass.sum())

        # camera
        S = self.size
        el, az = math.radians(CAM_EL), math.radians(CAM_AZ)
        self._foc = np.array([LBOX / 2, LBOX / 2, FOCAL_Z])
        dist = VIEW_W / 2 / math.tan(math.radians(CAM_FOV) / 2)
        back = np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])
        self._cam = self._foc + dist * back
        f = -back
        r = np.cross(f, [0.0, 0.0, 1.0])
        r /= np.linalg.norm(r)
        u = np.cross(r, f)
        self._basis = np.array([r, u, f])
        self._tan = math.tan(math.radians(CAM_FOV) / 2)

        pl = pv.Plotter(off_screen=True, window_size=(S, S), lighting="light kit")
        pl.set_background(BG)
        pl.camera_position = [tuple(self._cam), tuple(self._foc), (0.0, 0.0, 1.0)]
        pl.camera.view_angle = CAM_FOV
        pl.camera.clipping_range = (0.2 * dist, 4.0 * dist)
        self._pl = pl
        self._add_wires(pv)
        self._add_glyphs()
        if AA:
            pl.enable_anti_aliasing(AA)

        # periodic images to draw: every offset whose patch can show in the circle
        k = np.arange(-3, 4) * LBOX
        self._offs = np.array([(a, b, 0.0) for a in k for b in k])

        # circle, ring and the 100 um scale bar (at the mesh plane, near the bottom of the circle)
        yy, xx = np.mgrid[0:S, 0:S] + 0.5
        rr = np.hypot(xx - S / 2, yy - S / 2)
        rad_px = S / 2 - 0.5
        ring_w = max(1.5, S / 160)
        self._alpha = np.clip(rad_px - rr + 0.5, 0, 1)
        self._ring = np.clip(rr - (rad_px - ring_w) + 0.5, 0, 1) * self._alpha
        hit = self._ground(S / 2, 0.88 * S, 0.0)
        a, b = self._project(hit - 50.0 * r), self._project(hit + 50.0 * r)
        yb = int(round(0.5 * (a[1] + b[1])))
        self.bar_px = ((int(round(a[0])), yb), (int(round(b[0])), yb))

    # ------------------------------------------------------------------------------------- geometry
    def _project(self, P):
        rel = np.asarray(P, float) - self._cam
        xc, yc, zc = rel @ self._basis.T
        F = self.size / 2 / self._tan
        return np.array([self.size / 2 + F * xc / zc, self.size / 2 - F * yc / zc])

    def _ground(self, px, py, z):
        """The point at height z seen at pixel (px, py)."""
        F = self.size / 2 / self._tan
        r, u, f = self._basis
        ray = f + (px - self.size / 2) / F * r - (py - self.size / 2) / F * u
        t = (z - self._cam[2]) / ray[2]
        return self._cam + t * ray

    def _footprint(self, z):
        S = self.size
        a = np.linspace(0, 2 * np.pi, 49)
        pts = [self._ground(S / 2 + 0.51 * S * math.cos(t), S / 2 + 0.51 * S * math.sin(t), z) for t in a]
        return np.array(pts)[:, :2]

    def _add_wires(self, pv):
        """Every wire crossing the circle as a smooth tube. The frame is fixed (one axis across the wire), so the
        tube doesn't twist, and the normals are exact."""
        from vtkmodules.util.numpy_support import numpy_to_vtk
        from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper

        fp = np.vstack([self._footprint(MESH_TOP + 5), self._footprint(-MESH_TOP - 5)])
        lo, hi = fp.min(0) - RW, fp.max(0) + RW
        ns = 14
        phi = np.linspace(0, 2 * np.pi, ns, endpoint=False)
        pts, nrm, faces, base = [], [], [], 0
        for axis in (0, 1):                                  # 0: warps along x, 1: wefts along y
            t = np.linspace(lo[axis], hi[axis], int((hi[axis] - lo[axis]) / PITCH * 14) + 2)
            o = 1 - axis
            for j in range(int(math.floor(lo[o] / PITCH)), int(math.ceil(hi[o] / PITCH)) + 1):
                s = (1.0 if j % 2 == 0 else -1.0) * (1.0 if axis == 0 else -1.0)
                zc = s * _wave(t)
                dz = -s * CRIMP * np.pi / PITCH * np.sin(np.pi * t / PITCH)
                h = np.hypot(1.0, dz)
                N = np.zeros((len(t), 3))                    # in the wire's vertical plane, normal to it
                N[:, axis], N[:, 2] = -dz / h, 1.0 / h
                B = np.zeros(3)
                B[o] = 1.0
                ring = np.cos(phi)[None, :, None] * N[:, None, :] + np.sin(phi)[None, :, None] * B
                c = np.zeros((len(t), 3))
                c[:, axis], c[:, o], c[:, 2] = t, j * PITCH, zc
                pts.append((c[:, None, :] + RW * ring).reshape(-1, 3))
                nrm.append(ring.reshape(-1, 3))
                k, m = np.meshgrid(np.arange(len(t) - 1), np.arange(ns), indexing="ij")
                q = np.stack([k * ns + m, k * ns + (m + 1) % ns, (k + 1) * ns + (m + 1) % ns, (k + 1) * ns + m], -1)
                if axis == 0:
                    q = q[..., ::-1]                         # wind every face outward
                faces.append(np.hstack([np.full((q.size // 4, 1), 4), q.reshape(-1, 4) + base]))
                base += len(t) * ns
        mesh = pv.PolyData(np.vstack(pts), np.vstack(faces).ravel())
        nv = numpy_to_vtk(np.vstack(nrm).astype(np.float32), deep=True)
        nv.SetName("Normals")
        mesh.GetPointData().SetNormals(nv)
        mapper = vtkPolyDataMapper()
        mapper.SetInputData(mesh)
        mapper.ScalarVisibilityOff()
        actor = vtkActor()
        actor.SetMapper(mapper)
        prop = actor.GetProperty()
        prop.SetColor(*STEEL)
        prop.SetInterpolationToPhong()
        prop.SetAmbient(0.2)
        prop.SetDiffuse(0.7)
        prop.SetSpecular(0.6)
        prop.SetSpecularPower(35)
        self._pl.add_actor(actor)

    def _add_glyphs(self):
        from vtkmodules.vtkCommonDataModel import vtkPolyData
        from vtkmodules.vtkFiltersSources import vtkSphereSource
        from vtkmodules.vtkRenderingCore import vtkActor, vtkGlyph3DMapper

        src = vtkSphereSource()
        src.SetRadius(1.0)
        src.SetThetaResolution(18)
        src.SetPhiResolution(12)
        m = vtkGlyph3DMapper()
        m.SetSourceConnection(src.GetOutputPort())
        m.SetInputData(vtkPolyData())
        m.SetScaleArray("r")
        m.SetScaleModeToScaleByMagnitude()
        m.SetScaleFactor(1.0)
        m.OrientOff()
        m.SetScalarModeToUsePointFieldData()
        m.SelectColorArray("rgb")
        m.SetColorModeToDirectScalars()
        m.ScalarVisibilityOn()
        actor = vtkActor()
        actor.SetMapper(m)
        prop = actor.GetProperty()
        prop.SetInterpolationToPhong()
        prop.SetAmbient(0.15)
        prop.SetDiffuse(0.85)
        prop.SetSpecular(0.35)
        prop.SetSpecularPower(30)
        self._pl.add_actor(actor)
        self._gmap = m

    # ------------------------------------------------------------------------------------------ API
    def advance(self, dt_anim: float, agitation: float = 1.0, tap: bool = False) -> None:
        """Advance by one animation frame (dt_anim = 1/15 s). agitation 0..1 scales the gyratory shaking and the
        tap; tap=True gives one vertical jolt this frame. The micro-scale physics runs in slow motion: SLOWMO = 50,
        one second of animation is 20 ms at the sieve."""
        t_ms = dt_anim / SLOWMO * 1000.0
        nsub = max(1, int(math.ceil(t_ms / self._dt)))
        dt = t_ms / nsub
        ag = float(min(max(agitation, 0.0), 1.0))
        dph = 2 * math.pi * GYR_REV_S * dt_anim / nsub
        ntap = int(round(TAP_MS / dt)) if (tap and ag > 0) else 0
        atap = ag * TAP_DV / (ntap * dt) if ntap else 0.0
        _frame(self._p, self._v, self._om, self._q, self._w, self._wo, self._rad, self._mass, self._idrag,
               self._flag, self._nbr, self._nn, self._pref, self._nwc, self._fwz, nsub, dt, ag * A_GYR, self._phase,
               dph, ntap, atap, D_LOCK, F_LOCK, LOCK_OFF)
        self._phase += 2 * math.pi * GYR_REV_S * dt_anim

    def _visible(self):
        """Positions, radii and colours of everything to draw, periodic images included, culled to the circle."""
        live = self._flag != 2
        P, R, C = self._p[live], self._rad[live], self._col[live]
        f = np.clip((FADE_TOP - P[:, 2]) / (FADE_TOP - Z_GONE), 0, 1)[:, None]
        C = C * (1 - f) + np.array(BG) * f
        Q = (P[:, None, :] + self._offs[None]).reshape(-1, 3)
        k = len(self._offs)
        R, C = np.repeat(R, k), np.repeat(C, k, axis=0)
        xc, yc, zc = ((Q - self._cam) @ self._basis.T).T
        keep = zc > 0.25 * np.linalg.norm(self._cam - self._foc)
        rs = np.hypot(xc, yc)
        keep &= (rs - R * 1.05) / np.maximum(zc, 1e-6) < self._tan * 1.01
        return Q[keep], R[keep], C[keep]

    def render(self):
        """RGBA, size_px x size_px, circular, fully transparent outside the circle."""
        from PIL import Image, ImageDraw
        from vtkmodules.util.numpy_support import numpy_to_vtk
        from vtkmodules.vtkCommonCore import vtkPoints
        from vtkmodules.vtkCommonDataModel import vtkPolyData

        Q, R, C = self._visible()
        pd = vtkPolyData()
        pts = vtkPoints()
        pts.SetData(numpy_to_vtk(np.ascontiguousarray(Q, np.float32), deep=True))
        pd.SetPoints(pts)
        ra = numpy_to_vtk(np.ascontiguousarray(R, np.float32), deep=True)
        ra.SetName("r")
        ca = numpy_to_vtk(np.ascontiguousarray(np.round(C * 255), np.uint8), deep=True)
        ca.SetName("rgb")
        pd.GetPointData().AddArray(ra)
        pd.GetPointData().AddArray(ca)
        self._gmap.SetInputData(pd)
        self._pl.render()                                    # (a no-op before the first screenshot)
        img = self._pl.screenshot(return_img=True).astype(np.float32)[:, :, :3]
        ring = self._ring[:, :, None]
        img = img * (1 - ring) + np.array(INK, np.float32) * 255 * ring
        rgba = np.dstack([img, self._alpha * 255]).round().astype(np.uint8)
        im = Image.fromarray(rgba, "RGBA")
        dr = ImageDraw.Draw(im)
        (x0, y0), (x1, y1) = self.bar_px
        lw = max(2, round(self.size / 150))
        tk = max(3, round(self.size / 60))
        ink = tuple(int(c * 255) for c in INK) + (255,)
        halo = (255, 255, 255, 170)
        for col, grow in ((halo, 1), (ink, 0)):
            dr.line([(x0 - grow, y0), (x1 + grow, y1)], fill=col, width=lw + 2 * grow)
            for x in (x0, x1):
                dr.line([(x, y0 - tk - grow), (x, y0 + tk + grow)], fill=col, width=lw + 2 * grow)
        return im

    def stats(self) -> dict:
        fl = self._flag
        gone = fl == 1
        gone |= fl == 2
        return {"passed": int(gone.sum()), "on_mesh": int((fl == 0).sum()), "wedged": int((fl == 3).sum()),
                "passed_mass_frac": float(self._mass[gone].sum() / self._mass.sum())}


# ============================================================================================ demo
if __name__ == "__main__":
    from PIL import Image

    t0 = time.perf_counter()
    zm = Zoom(300, seed=0)
    print(f"setup {time.perf_counter() - t0:.1f} s: {zm._n} particles, {zm.fine_mass_frac:.1%} of the mass < 63 um, "
          f"dt {zm._dt * 1e3:.2f} us, bar {zm.bar_px}")
    fps, nframes, pour = 15, 135, 15
    frames, ta, tr = [], [], []
    for i in range(nframes):
        t0 = time.perf_counter()
        on = i >= pour
        zm.advance(1 / fps, agitation=1.0 if on else 0.0, tap=on and (i - pour) % 9 == 0)
        t1 = time.perf_counter()
        frames.append(zm.render())
        t2 = time.perf_counter()
        ta.append(t1 - t0)
        tr.append(t2 - t1)
        if i % 15 == 0 or i == nframes - 1:
            print(i, zm.stats())
    ta, tr = np.array(ta[1:]) * 1e3, np.array(tr[1:]) * 1e3
    print(f"advance: mean {ta.mean():.1f} ms, max {ta.max():.1f} ms; render: mean {tr.mean():.1f} ms, "
          f"max {tr.max():.1f} ms (frame 0, with the JIT, excluded)")
    bg = Image.new("RGBA", frames[0].size, (255, 255, 255, 255))
    flat = [Image.alpha_composite(bg, f).convert("RGB") for f in frames]
    flat[0].save("/tmp/zoom_demo.gif", save_all=True, append_images=flat[1:], duration=int(1000 / fps), loop=0)
    S = frames[0].size[0]
    sheet = Image.new("RGB", (3 * S, 3 * S), (255, 255, 255))
    for k, i in enumerate(np.linspace(0, nframes - 1, 9).round().astype(int)):
        sheet.paste(flat[i], ((k % 3) * S, (k // 3) * S))
    sheet.save("/tmp/zoom_sheet.png")
    print("wrote /tmp/zoom_demo.gif, /tmp/zoom_sheet.png;", zm.stats())
