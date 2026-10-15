"""
Shared data and styling for LPBF parameter space visualization panels.

All 36 LPBF parameters across 7 categories, with optimization status encoding.
Color palettes are color-blind-safe (Okabe-Ito inspired).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ─── Publication typography ───────────────────────────────────────────────────

RCPARAMS = {
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "figure.titlesize": 17,
    "figure.titleweight": "bold",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "svg.fonttype": "none",
}


def apply_rcparams():
    """Apply publication-quality matplotlib settings."""
    plt.rcParams.update(RCPARAMS)


# ─── Color-blind-safe palette (Okabe-Ito inspired) ───────────────────────────

# Primary encoding: optimization status
# Vermilion vs gold hue-separated per Edison iter 3 (was 1.7:1, now ~4:1 contrast)
STATUS_COLORS = {
    "optimized": "#C92A2A",   # True red — actively optimized (hue-separated from gold)
    "selective": "#E69F00",   # Amber/gold — selectively optimized
    "fixed":    "#5C6B77",   # Dark gray — typically fixed (visible as accent bar)
    "neglected": "#0072B2",   # Blue — often neglected
}

STATUS_LABELS = {
    "optimized": "Actively optimized",
    "selective": "Selectively optimized",
    "fixed":    "Typically fixed",
    "neglected": "Often neglected",
}

# Secondary encoding: category identity
CAT_COLORS = {
    "beam":        "#D96B00",  # Deep orange (distinct from STATUS_COLORS red)
    "scan":        "#D98C2E",
    "layer":       "#2A9D8F",
    "powder":      "#264653",
    "atmosphere":  "#6A4C93",
    "thermal":     "#1982C4",
    "machine":     "#7BAE37",
}

# ─── Data: 36 LPBF parameters across 7 categories ────────────────────────────

CATEGORIES = [
    ("Beam / Energy", "beam", [
        ("Laser power", "optimized"),
        ("Scan speed", "optimized"),
        ("Spot size", "fixed"),
        ("Beam profile", "fixed"),
        ("Wavelength", "fixed"),
        ("CW / Pulsed", "fixed"),
        ("Pulse params", "selective"),
        ("Beam oscillation", "selective"),
    ]),
    ("Scan Strategy", "scan", [
        ("Hatch spacing", "optimized"),
        ("Scan pattern", "selective"),
        ("Rotation angle", "selective"),
        ("Vector length", "selective"),
        ("Contour params", "selective"),
        ("Contour passes", "fixed"),
        ("Skywriting", "fixed"),
        ("Scan vs. gas flow", "neglected"),
    ]),
    ("Layer / Build", "layer", [
        ("Layer thickness", "optimized"),
        ("Build orientation", "selective"),
        ("Support strategy", "selective"),
        ("Plate location", "neglected"),
    ]),
    ("Powder / Feedstock", "powder", [
        ("PSD", "fixed"),
        ("Morphology", "fixed"),
        ("Flowability", "fixed"),
        ("Packing density", "fixed"),
        ("Moisture content", "neglected"),
        ("Recycling state", "neglected"),
    ]),
    ("Atmosphere", "atmosphere", [
        ("Gas type", "fixed"),
        ("Gas flow rate", "neglected"),
        ("O\u2082 content", "fixed"),
        ("Chamber pressure", "fixed"),
    ]),
    ("Thermal Mgmt", "thermal", [
        ("Baseplate preheat", "selective"),
        ("Inter-layer dwell", "neglected"),
        ("Build height", "fixed"),
    ]),
    ("Machine-Specific", "machine", [
        ("Recoater type", "fixed"),
        ("Recoater speed", "fixed"),
        ("Dosing factor", "fixed"),
    ]),
]

# Convenience: total parameter count
TOTAL_PARAMS = sum(len(params) for _, _, params in CATEGORIES)
