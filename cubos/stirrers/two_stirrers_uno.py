"""Draw how a second stir module joins the first on the CubXL's Arduino Uno, for #236 (2026-11-13).

    python cubos/stirrers/two_stirrers_uno.py

writes two_stirrers_uno.png next to this file. Matplotlib only.

The pins are the four-stirrer plan's (byu-vcl#269, "Four stirrers on one Uno", 2026-10-30;
#180's alloy-corrosion/stirrers/BUILD.md stage 4): stirrer A (built) keeps D10 and D2,
stirrer B takes D5 for its gate and D8 for its Hall sensor, and both share the Uno's one 5V pin
and a GND through a hub. Each stirrer is wired as byu-vcl's wiring_uno.png draws it, so only
the Uno end is drawn here.

check() runs first and stops the script if a stirrer lead lands on a pin the PANDA firmware
uses for the capper, the pipette or the USB serial, on D13 (the bootloader blinks it), or on a
pin another lead has. Pin positions, colours and the Uno, JST-XH and cable-break drawings are
copied from byu-vcl's hardware/vial-stirrer-cubxl/wiring_diagram.py at 4d5446c, so the two
figures match.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patheffects as pe  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "two_stirrers_uno.png"
W, H = 17.4, 10.6

C = {
    "5V": "#d62728",
    "GND": "#262626",
    "PWM": "#1fa493",
    "HALL": "#1f5fbf",
    "usb": "#5b6b7b",
    "board": "#2f6b45",
    "board_edge": "#1d4a2e",
    "uno": "#2b7c99",
    "uno_edge": "#1b5568",
    "warn": "#e8890c",
}

# Uno R3 headers, inches from the board's lower-left corner with the USB at the left
UNO_TOP = [("SCL", 0.84), ("SDA", 0.94), ("AREF", 1.04), ("GND", 1.14), ("13", 1.24), ("12", 1.34),
           ("11", 1.44), ("10", 1.54), ("9", 1.64), ("8", 1.74), ("7", 1.90), ("6", 2.00),
           ("5", 2.10), ("4", 2.20), ("3", 2.30), ("2", 2.40), ("1", 2.50), ("0", 2.60)]
UNO_BOTTOM = [("", 1.10), ("IOREF", 1.20), ("RESET", 1.30), ("3.3V", 1.40), ("5V", 1.50),
              ("GND", 1.60), ("GND", 1.70), ("VIN", 1.80), ("A0", 2.00), ("A1", 2.10),
              ("A2", 2.20), ("A3", 2.30), ("A4", 2.40), ("A5", 2.50)]

# What the PANDA firmware on the Uno uses (byu-vcl stirrer README, "Four stirrers on one Uno"):
# the capper's line-break sensor D4, the pipette's limit switch D9, the electromagnet D11, the
# TMC2209 on A0-A4, and the USB serial on D0 and D1. These must never get a stirrer lead.
IN_USE = {"4": "capper line-break sensor", "9": "pipette limit switch", "11": "electromagnet",
          "A0": "TMC2209", "A1": "TMC2209", "A2": "TMC2209", "A3": "TMC2209", "A4": "TMC2209",
          "0": "USB serial", "1": "USB serial"}
# Claimed by the firmware for lights that aren't wired. The four-stirrer firmware gives D5-D7 to
# the stirrers' gates; the ring on D3 stays.
LIGHTS = {"3": "NeoPixel ring", "5": "NeoPixel dot 1", "6": "NeoPixel dot 2", "7": "line-break LED"}
NEVER = {"13": "the bootloader blinks it at every reset"}

# JST-XH pin -> net, the same for every stirrer (byu-vcl BUILD.md pinout table)
CORE_NET = {1: "5V", 2: "GND", 3: "PWM", 4: "HALL"}
# stirrer -> its gate and Hall pins (the four-stirrer plan); 5V and GND come from the hub
STIRRERS = {"A": {3: "10", 4: "2"}, "B": {3: "5", 4: "8"}}
HUB = {"5V": ("B", 1.50), "GND": ("B", 1.60)}    # the hub's two leads take the pins A uses today


def check():
    """Every stirrer lead on a pin of its own, none on a pin the firmware needs."""
    used = {}
    for s, pins in STIRRERS.items():
        for core, pin in pins.items():
            assert pin not in IN_USE, f"stirrer {s} pin {core} on D{pin}: {IN_USE[pin]}"
            assert pin not in NEVER, f"stirrer {s} pin {core} on D{pin}: {NEVER[pin]}"
            assert pin not in used, f"D{pin} twice: {used[pin]} and {s}{core}"
            used[pin] = f"{s}{core}"
        # a Hall input must be on a pin nothing drives: a light pin would fight the sensor's output
        assert pins[4] not in LIGHTS, f"stirrer {s}'s Hall input on D{pins[4]}, which the firmware drives"
    names = {n for n, _ in UNO_TOP} | {n for n, _ in UNO_BOTTOM}
    assert all(p in names for pins in STIRRERS.values() for p in pins.values())
    assert [n for n, x in UNO_BOTTOM if ("B", x) == HUB["5V"]] == ["5V"]
    assert [n for n, x in UNO_BOTTOM if ("B", x) == HUB["GND"]] == ["GND"]
    return used


def wire(ax, pts, colour, lw=3.0, z=3, halo=3.5, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=C.get(colour, colour), lw=lw, zorder=z, solid_capstyle="round", ls=ls,
            solid_joinstyle="round",
            path_effects=[pe.Stroke(linewidth=lw + halo, foreground="white"), pe.Normal()])


def text(ax, x, y, s, size=11, weight="normal", colour="#1a1a1a", ha="center", va="center", **kw):
    return ax.text(x, y, s, fontsize=size, fontweight=weight, color=colour, ha=ha, va=va, **kw)


def chip(ax, x, y, s, colour, ha="center", size=9.5, z=12):
    return ax.text(x, y, s, fontsize=size, fontweight="bold", color="white", ha=ha, va="center", zorder=z,
                   bbox=dict(boxstyle="round,pad=0.25", fc=C.get(colour, colour), ec="none"))


def draw_uno(ax, x0, y0, k, pin_net):
    """Uno R3 to scale, k units per mm. pin_net maps (row, x) to the net a stirrer lead puts there.
    Returns every pin's (x, y), by (row, x): names repeat (the power header has two GNDs)."""
    mm = 25.4 * k
    ax.add_patch(FancyBboxPatch((x0, y0), 68.58 * k, 53.34 * k, boxstyle="round,pad=0,rounding_size=0.06",
                                fc=C["uno"], ec=C["uno_edge"], lw=2, zorder=1))
    ax.add_patch(Rectangle((x0 - 6.35 * k, y0 + 32 * k), 16.3 * k, 12 * k, fc="#c9c9c9", ec="#555555",
                           lw=1.4, zorder=2))
    text(ax, x0 + 1.8 * k, y0 + 38 * k, "USB-B", 7.5, "bold", "#222222", zorder=3)
    ax.add_patch(Rectangle((x0 - 1.9 * k, y0 + 3.3 * k), 14.9 * k, 9 * k, fc="#222222", ec="#111111",
                           lw=1.2, zorder=2))
    ax.add_patch(Rectangle((x0 + 1.18 * mm, y0 + 0.40 * mm), 1.38 * mm, 0.30 * mm, fc="#1e1e1e",
                           ec="#000000", lw=1, zorder=2))
    text(ax, x0 + 1.87 * mm, y0 + 0.55 * mm, "ATmega328P", 7.5, colour="#bbbbbb", zorder=3)
    text(ax, x0 + 0.62 * mm, y0 + 1.02 * mm, "UNO", 17, "bold", "#d8eef5", zorder=2)
    pins = {}
    s = 1.95 * k
    for row, yy, labels, split in (("T", 2.0, UNO_TOP, 1.85), ("B", 0.1, UNO_BOTTOM, 1.95)):
        xs = [x for _, x in labels]
        for g in ([x for x in xs if x < split], [x for x in xs if x > split]):
            ax.add_patch(Rectangle((x0 + (g[0] - 0.05) * mm, y0 + (yy - 0.05) * mm), (g[-1] - g[0] + 0.1) * mm,
                                   0.1 * mm, fc="#151515", ec="#151515", lw=0.5, zorder=2))
        for name, x in labels:
            net = pin_net.get((row, x))
            px, py = x0 + x * mm, y0 + yy * mm
            busy = name in IN_USE or name in LIGHTS
            ax.add_patch(Rectangle((px - s / 2, py - s / 2), s, s,
                                   fc=C[net] if net else ("#8d8d8d" if busy else "#dcdcdc"),
                                   ec="#111111" if net else "#444444", lw=1.4 if net else 0.6, zorder=4))
            pins[(row, x)] = (px, py)
            if name:
                text(ax, px, py + (-0.11 if row == "T" else 0.11), name, 7.2,
                     "bold" if net else "normal",
                     colour="#ffffff" if net else ("#9fc4d2" if busy else "#eaf5f9"),
                     va="top" if row == "T" else "bottom", rotation=90, zorder=3)
    return pins, s


def draw_jst(ax, x0, ys, w=0.42, label=True):
    """A JST-XH pair, mated: housing (Uno side, recessed contacts) left, plug (cable side) right.
    ys are the pins' heights, pin 1 first."""
    top, bot = max(ys) + 0.2, min(ys) - 0.2
    ax.add_patch(Rectangle((x0, bot), w, top - bot, fc="#f4f1e6", ec="#555555", lw=1.6, zorder=5))
    ax.add_patch(Rectangle((x0 + w, bot + 0.05), w * 0.8, top - bot - 0.1, fc="#ebe6d4", ec="#555555", lw=1.6,
                           zorder=5))
    for i, y in enumerate(ys):
        ax.add_patch(Rectangle((x0 + 0.12, y - 0.07), 0.14, 0.14, fc="#7a7a7a", ec="#444444", lw=0.8, zorder=6))
        if label:
            text(ax, x0 + w + w * 0.4, y, str(i + 1), 11, "bold", "#222222", zorder=6)
    return x0, x0 + w * 1.8


def draw_break(ax, x, y, h=0.42):
    ax.add_patch(Rectangle((x - 0.06, y - h / 2 - 0.02), 0.12, h + 0.04, fc="white", ec="none", zorder=7))
    for dx in (-0.06, 0.06):
        ax.plot([x + dx - 0.05, x + dx + 0.05], [y - h / 2 - 0.03, y + h / 2 + 0.03], color="#444444", lw=1.6,
                zorder=8)


def cable(ax, x_from, ys, x_to, y_jacket, lw=15):
    """Four cores from a plug's pins into heat shrink, then the grey jacket to x_to. Returns the
    jacket's start."""
    for c, y in zip((1, 2, 3, 4), ys):
        wire(ax, [(x_from, y), (x_from + 0.12, y), (x_from + 0.28, y_jacket + 0.06 * (c - 2.5))], CORE_NET[c],
             lw=2.2, halo=2.2, z=6)
    ax.add_patch(Rectangle((x_from + 0.28, y_jacket - 0.22), 0.13, 0.44, fc="#333333", ec="none", zorder=7))
    ax.plot([x_from + 0.41, x_to], [y_jacket, y_jacket], color="#8d8d8d", lw=lw, solid_capstyle="butt", zorder=5)
    return x_from + 0.41


def stirrer_box(ax, x, y, w, h, title, lines):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.08", fc="#eef3ee",
                                ec=C["board_edge"], lw=1.8, zorder=4))
    text(ax, x + w / 2, y + h - 0.24, title, 11, "bold", zorder=5)
    for i, line in enumerate(lines):
        text(ax, x + w / 2, y + h - 0.52 - 0.21 * i, line, 8.6, colour="#333333", zorder=5)


def tag(ax, x, y, s, net):
    """A lead's free end: a male pin, and the Uno pin it goes into."""
    ax.add_patch(Rectangle((x - 0.2, y - 0.035), 0.2, 0.07, fc="#b8b8b8", ec="#555555", lw=0.8, zorder=7))
    chip(ax, x - 0.3, y, s, net, ha="right", size=9.5)


def figure():
    fig = plt.figure(figsize=(W, H), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")
    text(ax, 0.3, 10.3, "Two stir modules on the CubXL's Uno: stirrer B's fan on D5 and its Hall sensor on D8, "
         "sharing 5V and GND with stirrer A", 15.5, "bold", ha="left")
    text(ax, 0.3, 9.96, "The four-stirrer plan's pins (byu-vcl#269, 2026-10-30; #180 alloy-corrosion/stirrers/"
         "BUILD.md stage 4). Each stirrer is wired as in byu-vcl's wiring_uno.png; only the Uno end changes. "
         "Drawn by two_stirrers_uno.py.", 10.2, colour="#444444", ha="left")

    # --- the Uno, with every stirrer lead's pin ------------------------------------------------------
    k = 0.09
    ux, uy = 1.15, 3.05
    top = {n: x for n, x in UNO_TOP}                    # the digital header's names are unique
    pin_net = {("B", x): net for net, (_, x) in HUB.items()}
    for s, pins in STIRRERS.items():
        for core, pin in pins.items():
            x = next(x for n, x in UNO_TOP if n == pin)
            pin_net[("T", x)] = CORE_NET[core]
    pins, sq = draw_uno(ax, ux, uy, k, pin_net)
    text(ax, ux + 34.29 * k, 2.12, "Arduino Uno R3 on the CubXL", 15, "bold")
    text(ax, ux + 34.29 * k, 1.83, "dark grey: in use by the capper, pipette or USB serial, or claimed for lights",
         9, colour="#444444")

    # callouts over the top header: the left pair goes up and left, the right pair up and right,
    # each pair nested so no leader crosses another
    callouts = [("10", 8.25, "left", "D10: A's fan PWM", "PWM"),
                ("8", 8.75, "left", "D8: B's Hall in  (new)", "HALL"),
                ("2", 8.25, "right", "D2: A's Hall in", "HALL"),
                ("5", 8.75, "right", "D5: B's fan PWM  (new)", "PWM")]
    for pin, y, side, label, net in callouts:
        px, py = pins[("T", top[pin])]
        xe = ux + 3.0 if side == "left" else ux + 6.05
        wire(ax, [(px, py + sq / 2), (px, y), (xe, y)], net, lw=2.4, halo=2.4, z=6)
        chip(ax, xe + (-0.08 if side == "left" else 0.08), y, label, net, ha="right" if side == "left" else "left")
    # the in-use pins right beside B's: one hole off puts a stirrer lead on them
    hy = pins[("T", top["9"])][1]
    for pin, label in (("9", "D9: pipette\nlimit switch"), ("4", "D4: capper\nline-break")):
        px, py = pins[("T", top[pin])]
        ax.add_patch(Circle((px, py), sq * 0.95, fc="none", ec=C["warn"], lw=2.6, zorder=8))
        ax.plot([px, px], [py - sq * 0.95, hy - 0.62], color=C["warn"], lw=1.4, zorder=7)
        text(ax, px, hy - 0.66, label, 7.8, "bold", C["warn"], va="top", linespacing=1.05, zorder=8,
             bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=C["warn"], lw=1.0))
    # the hub's two leads on the power header
    for name, y, xe in (("5V", 2.62, ux + 2.55), ("GND", 2.38, ux + 2.55)):
        px, py = pins[HUB[name]]
        wire(ax, [(px, py - sq / 2), (px, y), (xe, y)], name, lw=2.4, halo=2.4, z=6)
        chip(ax, xe - 0.08, y, f"{name}: the hub's {name} lead", name, ha="right")

    # --- the hub at the Uno ----------------------------------------------------------------------
    jx = 11.55
    ya = {4: 7.35, 3: 7.05, 2: 6.75, 1: 6.45}          # A's socket, pin 4 on top
    yb = {1: 4.05, 2: 3.75, 3: 3.45, 4: 3.15}          # B's socket turned over, pin 1 on top
    tx = 9.3                                            # where the leads' male pins end
    bx0, bx1, by0, by1 = 9.85, 10.85, 3.6, 6.9          # the hub's piece of perfboard
    xg, x5 = 10.13, 10.53                               # its GND and 5V rails
    ax.add_patch(FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=C["board"], ec=C["board_edge"], lw=1.6, zorder=2))
    for cx in (bx0 + 0.14 + 0.254 * i for i in range(4)):
        for cy in (by0 + 0.15 + 0.254 * j for j in range(13)):
            ax.add_patch(Circle((cx, cy), 0.045, fc="#d8d2bf", ec="#1d4a2e", lw=0.5, zorder=3))
    wire(ax, [(xg, yb[2]), (xg, ya[2])], "GND", lw=7, halo=1.5, z=4)
    wire(ax, [(x5, yb[1]), (x5, ya[1])], "5V", lw=7, halo=1.5, z=4)
    for i, line in enumerate(("The hub: a piece of the BOM's perfboard strip",
                              "(item 10) with a GND rail and a 5V rail. The 5V",
                              "lead crosses the GND rail without touching it.",
                              "Each lead ends in a male pin (half a male–male",
                              "jumper) for the Uno pin on its tag.")):
        text(ax, 9.2, 8.6 - 0.2 * i, line, 8.6, colour="#333333", ha="left")
    # each socket's leads: pins 1 and 2 onto the rails, pins 3 and 4 to their own Uno pins
    for ys_, s in ((ya, "A"), (yb, "B")):
        for c in (1, 2):
            xr = x5 if c == 1 else xg
            wire(ax, [(jx, ys_[c]), (xr, ys_[c])], CORE_NET[c], lw=2.6, halo=2.4, z=6)
            ax.add_patch(Circle((xr, ys_[c]), 0.075, fc=C[CORE_NET[c]], ec="white", lw=1.2, zorder=9))
        for c in (3, 4):
            wire(ax, [(jx, ys_[c]), (tx, ys_[c])], CORE_NET[c], lw=2.6, halo=2.4, z=6)
            tag(ax, tx, ys_[c], f"D{STIRRERS[s][c]}", CORE_NET[c])
    # the rails' leads to the Uno: the 5V lead hops over the GND rail, it doesn't touch it
    ym_g, ym_5 = 5.55, 5.0
    wire(ax, [(xg, ym_g), (tx, ym_g)], "GND", lw=2.6, halo=2.4, z=6)
    ax.add_patch(Circle((xg, ym_g), 0.075, fc=C["GND"], ec="white", lw=1.2, zorder=9))
    tag(ax, tx, ym_g, "GND", "GND")
    wire(ax, [(x5, ym_5), (tx, ym_5)], "5V", lw=2.6, halo=4.5, z=8)
    ax.add_patch(Circle((x5, ym_5), 0.075, fc=C["5V"], ec="white", lw=1.2, zorder=9))
    tag(ax, tx, ym_5, "5V", "5V")

    # --- the sockets, the plugs and the cables -------------------------------------------------------
    _, xa = draw_jst(ax, jx, [ya[c] for c in (1, 2, 3, 4)])
    text(ax, jx + 0.38, ya[1] - 0.45, "socket A", 10, "bold")
    _, xb = draw_jst(ax, jx, [yb[c] for c in (1, 2, 3, 4)])
    text(ax, jx + 0.38, yb[1] + 0.45, "socket B", 10, "bold")
    # A: its own cable, as built
    yja = (ya[1] + ya[4]) / 2
    cable(ax, xa, [ya[c] for c in (1, 2, 3, 4)], 15.05, yja)
    draw_break(ax, 13.9, yja)
    text(ax, 13.9, yja + 0.42, "≈ 1.5 m, as built", 9.5, "bold", "#333333")
    stirrer_box(ax, 15.05, yja - 0.62, 2.1, 1.24, "Stirrer A", ("built; keeps D10 and D2", "wiring_uno.png"))
    # B: an extension lead between socket B and B's own, shorter cable
    yjb = (yb[1] + yb[4]) / 2
    ex = 13.35
    cable(ax, xb, [yb[c] for c in (1, 2, 3, 4)], ex - 0.42, yjb, lw=11)
    draw_break(ax, 12.73, yjb, h=0.34)
    for c in (1, 2, 3, 4):
        wire(ax, [(ex - 0.42, yjb + 0.06 * (2.5 - c)), (ex - 0.2, yb[c]), (ex, yb[c])], CORE_NET[c], lw=2.2,
             halo=2.2, z=6)
    _, xe2 = draw_jst(ax, ex, [yb[c] for c in (1, 2, 3, 4)], label=False)
    cable(ax, xe2, [yb[c] for c in (1, 2, 3, 4)], 15.05, yjb)
    draw_break(ax, 14.62, yjb)
    text(ax, 14.55, yb[4] - 0.12, "B's own\ncable", 8.6, "bold", "#333333", va="top", linespacing=1.05)
    stirrer_box(ax, 15.05, yjb - 0.62, 2.1, 1.24, "Stirrer B", ("the same build", "wiring_uno.png"))
    ax.add_patch(FancyBboxPatch((11.92, yb[4] - 0.32), 1.85, yb[1] - yb[4] + 0.64,
                                boxstyle="round,pad=0,rounding_size=0.06", fc="none", ec="#777777", lw=1.3,
                                ls=(0, (4, 3)), zorder=3))
    for i, line in enumerate(("Dashed: an extension lead, if B's cable is short.",
                              "One JST-XH pair (BOM item 9) on 22 AWG × 4, pin 1",
                              "to pin 1: its plug goes into socket B, and B's",
                              "plug goes into its socket.")):
        text(ax, 11.6, 2.6 - 0.2 * i, line, 8.6, colour="#333333", ha="left")

    # --- legend ------------------------------------------------------------------------------------
    text(ax, 10.05, 9.4, "Nets:", 9.5, "bold", ha="left")
    x, renderer = 10.7, fig.canvas.get_renderer()
    for net, label in (("5V", "5V, JST pin 1"), ("GND", "GND, pin 2"), ("PWM", "fan PWM (gate), pin 3"),
                       ("HALL", "Hall, pin 4")):
        t = chip(ax, x, 9.4, label, net, ha="left", size=9)
        x += t.get_window_extent(renderer=renderer).width / fig.dpi + 0.28

    # --- notes ---------------------------------------------------------------------------------------
    ax.add_patch(Rectangle((0.25, 0.15), W - 0.5, 1.42, fc="#f7f7f7", ec="#bbbbbb", lw=1.2, zorder=0))
    notes = (
        "B only runs on D5 and D8 once the four-stirrer firmware is flashed, and it isn't written yet. The image on "
        "the Uno (flashed 2026-11-03) drives one stirrer, on D10 and D2.\n"
        "Until then, test B by unplugging A at its socket and plugging B in instead. Plugged into D5 and D8 today, B "
        "sits still: the firmware sends D5 only microseconds of light data, and never reads D8.\n"
        "Wire the hub with the Uno's USB unplugged, and meter it first: 5V to GND is not a short, and each socket's "
        "pins 3 and 4 reach only their own Uno pins.\n"
        "Orange rings: D9 and D4 are in use, right beside B's pins. One hole off puts a stirrer lead on the pipette's "
        "limit switch or the capper's sensor."
    )
    text(ax, 0.42, 0.86, notes, 10, colour="#222222", ha="left", linespacing=1.55)
    return fig


if __name__ == "__main__":
    used = check()
    print("stirrer pins:", ", ".join(f"{v}=D{k}" for k, v in sorted(used.items(), key=lambda kv: kv[1])))
    fig = figure()
    fig.savefig(OUT, dpi=200, facecolor="white")
    plt.close(fig)
    print("wrote", OUT)
