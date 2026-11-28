"""Small sequential ray tracer for the monitoring optics (issue #260): spherical and plane surfaces, real glasses (Sellmeier),
Spencer-Murty intersection and vector Snell refraction, vectorised over rays with numpy.

Used by ftheta.py (a representative 3-element 1064 nm f-theta, traced from 600 to 1700 nm with the chamber window and the
cover slide) and viewports.py (tilted viewport windows). Units: mm, wavelengths in um. Light travels toward +z.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

# Sellmeier coefficients: n^2 = 1 + sum B_i l^2 / (l^2 - C_i), l in um.
#   fused silica: Malitson, JOSA 55, 1205 (1965) (Corning 7980 / UV fused silica)
#   N-BK7, N-SF11, N-SF6: SCHOTT optical glass data sheets (zemax AGF coefficients)
SELLMEIER = {
    "F_SILICA": ((0.6961663, 0.4079426, 0.8974794), (0.0684043 ** 2, 0.1162414 ** 2, 9.896161 ** 2)),
    "N-BK7": ((1.03961212, 0.231792344, 1.01046945), (0.00600069867, 0.0200179144, 103.560653)),
    "N-SF11": ((1.73759695, 0.313747346, 1.89878101), (0.013188707, 0.0623068142, 155.23629)),
    "N-SF6": ((1.77931763, 0.338149866, 2.08734474), (0.0133714182, 0.0617533621, 174.01759)),
}


def n_glass(name: str, lam_um) -> np.ndarray | float:
    if name == "AIR":
        return 1.0
    B, C = SELLMEIER[name]
    l2 = np.asarray(lam_um, float) ** 2
    return np.sqrt(1 + sum(b * l2 / (l2 - c) for b, c in zip(B, C)))


@dataclass
class Surf:
    z: float            # vertex position on the axis (mm)
    c: float            # curvature 1/R (1/mm); R > 0: centre of curvature on the +z side
    after: str          # medium after the surface ("AIR" or a glass name)
    semi: float = 1e9   # semi-diameter for vignetting (mm)
    tilt_x_deg: float = 0.0   # plane surfaces only: tilt of the normal about the x axis


def trace(P, D, surfs, lam_um, n0=1.0, keep=False):
    """Trace rays (P: (N,3) points, D: (N,3) unit directions) through surfs. Returns P, D at the last surface and a mask of
    rays that passed every surface (no miss, no TIR, inside every semi-diameter). keep=True also returns the path."""
    P = np.array(P, float)
    D = np.array(D, float)
    ok = np.ones(len(P), bool)
    n1 = n0
    path = [P.copy()]
    for s in surfs:
        if s.c == 0.0:
            nrm = np.array([0.0, -math.sin(math.radians(s.tilt_x_deg)), math.cos(math.radians(s.tilt_x_deg))])
            rel = P - np.array([0.0, 0.0, s.z])
            t = -(rel @ nrm) / (D @ nrm)
            Q = P + t[:, None] * D
            N = np.broadcast_to(nrm, Q.shape).copy()
        else:
            rel = P - np.array([0.0, 0.0, s.z])
            F = s.c * np.einsum("ij,ij->i", rel, rel) - 2 * rel[:, 2]
            G = D[:, 2] - s.c * np.einsum("ij,ij->i", rel, D)
            disc = G * G - s.c * F
            ok &= disc >= 0
            disc = np.where(disc > 0, disc, 0.0)
            t = F / (G + np.sqrt(disc))
            Q = P + t[:, None] * D
            q = Q - np.array([0.0, 0.0, s.z])
            N = np.stack([-s.c * q[:, 0], -s.c * q[:, 1], 1 - s.c * q[:, 2]], -1)
            N /= np.linalg.norm(N, axis=1)[:, None]
        ok &= np.hypot(Q[:, 0], Q[:, 1]) <= s.semi
        n2 = float(n_glass(s.after, lam_um))
        mu = n1 / n2
        cosI = np.einsum("ij,ij->i", D, N)
        N = np.where(cosI[:, None] < 0, -N, N)
        cosI = np.abs(cosI)
        k = 1 - mu * mu * (1 - cosI * cosI)
        ok &= k >= 0
        k = np.where(k > 0, k, 0.0)
        D = mu * D + (np.sqrt(k) - mu * cosI)[:, None] * N
        D /= np.linalg.norm(D, axis=1)[:, None]
        P = Q
        n1 = n2
        if keep:
            path.append(P.copy())
    if keep:
        return P, D, ok, path
    return P, D, ok


def to_plane(P, D, z):
    t = (z - P[:, 2]) / D[:, 2]
    return P + t[:, None] * D


def pupil_grid(n_rings=8, n_arms=16):
    """Unit-disc sample points (hexapolar-like, equal-area rings) plus the centre."""
    pts = [(0.0, 0.0)]
    for i in range(1, n_rings + 1):
        r = math.sqrt(i / n_rings)
        m = max(6, int(round(n_arms * r)))
        for j in range(m):
            a = 2 * math.pi * (j + 0.5 * (i % 2)) / m
            pts.append((r * math.cos(a), r * math.sin(a)))
    return np.array(pts)


def beam_rays(theta_rad, epd, z_stop, grid=None, phi_rad=0.0):
    """Collimated beam of diameter epd at field angle theta (in the plane at azimuth phi from y), centred on the axis at z_stop.
    The beam is sampled across its own cross-section (a circle normal to its direction), as a galvo-steered beam is."""
    g = pupil_grid() if grid is None else grid
    d = np.array([math.sin(theta_rad) * math.sin(phi_rad), math.sin(theta_rad) * math.cos(phi_rad), math.cos(theta_rad)])
    e_x = np.array([math.cos(phi_rad), -math.sin(phi_rad), 0.0])
    e_p = np.cross(d, e_x)
    e_p /= np.linalg.norm(e_p)
    P = np.array([0.0, 0.0, z_stop]) + (epd / 2) * (g[:, :1] * e_x + g[:, 1:2] * (-e_p))
    D = np.broadcast_to(d, P.shape).copy()
    return P, D, g


def best_focus(P, D, axis=None):
    """Plane z (along the axis) that minimises the RMS spread of the rays about their centroid. axis=None: radial;
    axis=0 or 1: spread in x only (sagittal for a y-field) or y only (tangential). Returns (z, rms at z)."""
    z0 = P[:, 2].mean()
    Q = to_plane(P, D, z0)
    s = D[:, :2] / D[:, 2:3]
    a = Q[:, :2] - Q[:, :2].mean(0)
    b = s - s.mean(0)
    if axis is not None:
        a, b = a[:, axis:axis + 1], b[:, axis:axis + 1]
    dz = -np.sum(a * b) / max(np.sum(b * b), 1e-30)
    rms = math.sqrt(np.mean(np.sum((a + dz * b) ** 2, axis=1)))
    return z0 + dz, rms


def rms_at(P, D, z):
    Q = to_plane(P, D, z)
    c = Q[:, :2].mean(0)
    return math.sqrt(np.mean(np.sum((Q[:, :2] - c) ** 2, axis=1))), c
