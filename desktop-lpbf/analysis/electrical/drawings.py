"""Electrical drawings for electrical.md: single-line diagram, interlock schematic, and the panel layouts to scale.

Outputs (desktop-lpbf/analysis/out/electrical/):
  single_line.png   supply at the dock -> main disconnect -> branches -> loads; UPS-backed vs unbacked; DC rails
  interlock.png     safety inputs -> XS26-2 safety controller -> final elements (two per hazard) with EDM read-back
  panels.png        to scale: the 4U control drawer (Middle Atlantic UD/D-class drawer, 403 x 368 mm inside), the drawer
                    section with the deepest DIN part against 3U and 4U, and the power box PB1 backplate (16 x 12 in)
Device sizes are the makers' published W x H x D where read (electrical-bom.csv); the few marked "~" are assumed.

Run: /tmp/venv/bin/python desktop-lpbf/analysis/electrical/drawings.py
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parents[1] / "out" / "electrical"
OUT.mkdir(parents=True, exist_ok=True)

C_AC, C_UPS, C_DC, C_SAFE, C_SIG, C_HEAT = "#c0392b", "#8e44ad", "#2c7fb8", "#e67e22", "#555555", "#d35400"


def box(ax, x, y, w, h, text, fc="#ffffff", ec="#333333", fs=7, bold=False, lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal", wrap=True)


def line(ax, pts, c="#333333", lw=1.4, ls="-"):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=c, lw=lw, ls=ls, solid_capstyle="round")


def single_line():
    fig, ax = plt.subplots(figsize=(17, 11))
    ax.set_xlim(0, 34)
    ax.set_ylim(0, 22)
    ax.axis("off")
    ax.set_title("Desktop LPBF tray: single-line diagram (electrical.md §1). Red: unbacked AC; purple: UPS-backed AC; blue: DC; orange: safety-switched", fontsize=11)
    # supply
    box(ax, 0.3, 18.6, 3.6, 2.6, "Lab panel\n208Y/120 V\n30 A 2-pole breaker\n(byu-vcl PR 318 dock)", fc="#fdecea", fs=7.5)
    box(ax, 4.5, 18.6, 3.6, 2.6, "Tray dock\nHarting Han-Modular\ndocking frame:\nHan C 40 A L1 L2 N PE (PE leads),\nRJ45, 12-pin signal, air", fc="#fff7e0", fs=6.5)
    line(ax, [(3.9, 19.9), (4.5, 19.9)], C_AC, 2.5)
    box(ax, 8.8, 18.6, 3.8, 2.6, "PB1 power box (left of the rack)\nQ0 main disconnect, 3P 30 A,\nUL 98, lockable (Socomec 22013003 + 147E1111)\nSCCR: see §1.3", fc="#fdecea", fs=5.8, bold=False)
    line(ax, [(8.1, 19.9), (8.8, 19.9)], C_AC, 2.5)
    ax.text(4.6, 18.1, "dock -> PB1: 10 AWG, 2.7 m along the back duct", fontsize=6, color=C_AC)
    # bus
    line(ax, [(10.7, 18.6), (10.7, 17.6), (31.5, 17.6)], C_AC, 3.0)
    ax.text(11.0, 17.75, "L1, L2, N, PE bus in PB1", fontsize=7, color=C_AC)
    branches = [
        (11.0, "Q1 2P 15 A D\nKM0 laser mains\ncontactor (PLC)", "IPG YLR-500-U3\n208 V L1-L2\n1.7 kW / 1.9 kVA\nrear terminal L1 L2 PE", C_AC),
        (15.2, "Q2 2P 15 A D\n(multiwire,\nhandle-tied)", "UPS Eaton 5PX1500RTG2\n120 V L1-N, 1,440 W\n(see backed side)", C_AC),
        (19.4, "Q2 (L2-N leg)", "Heater supply\nMean Well LRS-350-24\n24 V 14.6 A (unbacked)", C_AC),
        (23.6, "Q3 1P 15 A C\nKM1 + overload", "Vacuum pump 4396K21\n115 V 7 A, 1/2 hp\n(gas module, 2.3 m)", C_AC),
        (27.8, "Q4 1P 6 A C\nKM2", "Recirculation blower\n(AC upper bound 230 W;\nor 24 V brushless)", C_AC),
    ]
    for x, brk, load, c in branches:
        line(ax, [(x + 1.6, 17.6), (x + 1.6, 16.6)], c, 2.0)
        box(ax, x, 15.0, 3.2, 1.6, brk, fc="#fdecea", fs=6.3)
        line(ax, [(x + 1.6, 15.0), (x + 1.6, 14.2)], c, 2.0)
        box(ax, x, 12.4, 3.2, 1.8, load, fc="#ffffff", fs=6.3)
    # UPS backed side
    line(ax, [(16.8, 12.4), (16.8, 11.4), (2.0, 11.4), (2.0, 10.6)], C_UPS, 2.2)
    ax.text(5.0, 11.55, "UPS outputs (5-15R): backed AC, ~240 W while building, 791 W rated", fontsize=7, color=C_UPS)
    ups_loads = [
        (0.3, "Scan PC (2U)\nSCANLAB RTC6 PCIe\nXY2-100 + laser signals", C_UPS),
        (4.3, "SDR-240-24\n+24 V CTRL 10 A\n(PB1)", C_DC),
        (8.3, "SDR-240-48\n+48 V SERVO 5 A\n(PB1)", C_DC),
        (12.3, "HDR-100-24\n+24 V GALVO 3.8 A\n(basiCube 20: 24 V, <= 2.6 A)", C_DC),
    ]
    for x, t, c in ups_loads:
        line(ax, [(x + 1.7, 11.4), (x + 1.7, 10.6)], C_UPS, 1.8)
        box(ax, x, 8.9, 3.4, 1.7, t, fc="#f4ecf7" if c == C_UPS else "#eaf2fb", fs=6.3)
    # DC distribution
    line(ax, [(6.0, 8.9), (6.0, 8.1), (1.0, 8.1)], C_DC, 1.8)
    box(ax, 0.3, 5.9, 5.0, 2.2, "+24 V CTRL via Phoenix CBMC E4\n(4 x electronic breakers 1-10 A):\n1 safety controller + guard lock + E-stops\n2 PLC + I/O + sensors + valves\n3 ClearCore + stepper drive + fans\n4 PB2 box (Pi 5, NFC, load cell, camera)", fc="#eaf2fb", fs=6.0)
    line(ax, [(10.0, 8.9), (10.0, 7.2)], C_DC, 1.8)
    box(ax, 6.2, 5.9, 4.6, 1.3, "K3A + K3B in series\n(safety outputs; no STO on ClearPath-SD)", fc="#fdf2e9", ec=C_SAFE, fs=6.2)
    line(ax, [(8.5, 5.9), (8.5, 5.2)], C_SAFE, 1.8)
    box(ax, 6.2, 3.7, 4.6, 1.5, "ClearPath-SD x2 (recoater, Z)\n48 V bus, 1.6 m 18 AWG\nstep/dir/enable from ClearCore", fc="#ffffff", fs=6.2)
    line(ax, [(14.0, 8.9), (14.0, 7.2)], C_DC, 1.8)
    box(ax, 11.5, 5.9, 5.0, 1.3, "basiCube 20 galvo, 1.6 m 18 AWG\nXY2-100 from RTC6 (shielded, < 3 m)", fc="#ffffff", fs=6.2)
    # heater chain
    line(ax, [(21.0, 12.4), (21.0, 10.9)], C_HEAT, 2.0)
    box(ax, 18.6, 8.6, 5.0, 2.3, "24 V heater chain (PB1):\nF 15 A -> K1 (XS26 safety output)\n-> K2 (CN708 latching limit, own TC)\n-> SSR D1D20 (PLC PI, 1 s cycle)\n-> M12 L-coded -> rod-end feedthrough", fc="#fdf2e9", ec=C_SAFE, fs=6.0)
    line(ax, [(21.0, 8.6), (21.0, 7.6)], C_HEAT, 2.0)
    box(ax, 18.6, 5.6, 5.0, 2.0, "Module heaters 2/3/5 x 50 W 24 V\n(10.4 A max, L75), RT240 TCO in series\n3 type K: control, edge -> PLC;\nlimit -> CN708 (K2)", fc="#ffffff", fs=6.0)
    # control network
    box(ax, 24.6, 8.6, 4.2, 2.3, "4U control drawer (rack)\nBanner XS26-2 + XS16si + XS2so\nProductivity1000 PLC\nTeknic ClearCore + SureStep drive\nK4/K5 laser-loop relays\nEthernet switch", fc="#eef7ee", fs=6.0, bold=False)
    box(ax, 29.2, 8.6, 4.5, 2.3, "PB2 box (process module)\nRaspberry Pi 5 supervisor + HQ camera\nPN532 NFC, NAU7802 load cell\nE3NX fibre amp, M12 junction", fc="#eef7ee", fs=6.0)
    box(ax, 24.0, 5.4, 9.9, 2.6, "Ethernet: PC (RTC6 host) - Pi 5 (recipe, REST API) - PLC (Modbus TCP) - ClearCore - laser (status) - UPS card - dock uplink\nHard-wired safety: E-stops (rack, guard, gas module), guard sensor + lock, key, reset, room/Shuttle O2 relays,\nrobot Safe Home, tray docked, shutter switches, CN708 relay, plate < 50 C relay, laser status -> XS26-2", fc="#f7f7f7", fs=4.9)
    # notes
    ax.text(0.3, 2.6, "Notes: PE bonded in PB1 to the tray frame and every module base (two PE paths through the dock: protective-conductor current ~8 mA estimated, IEC 60204-1 8.2.8). "
                      "Pump and laser never run together (PLC): worst leg 17.9 A of 24 A. "
                      "Inrush: laser + UPS + heater supply at once ~120 A against the dock breaker's 150 A lowest C-curve trip: the PLC closes KM0 (laser mains) 5 s after power-up.", fontsize=6.5, wrap=True)
    ax.text(0.3, 1.6, "Not shown: argon NC valves (24 V, opened only through the O2-monitor relays and the exhaust flow switch in series), pneumatic valves, fans, lamps, and the 0 V/PE details (electrical-io.csv).", fontsize=6.5)
    fig.savefig(OUT / "single_line.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


def interlock():
    fig, ax = plt.subplots(figsize=(16, 10.5))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 21)
    ax.axis("off")
    ax.set_title("Interlock schematic (electrical.md §4; logic checked in interlock_logic.py): two channels in, two final elements out per hazard", fontsize=11)
    ins = [
        ("E-stop, rack panel (2 NC)", 2), ("E-stop, guard front (2 NC)", 2), ("E-stop, gas module (2 NC)", 2),
        ("Guard closed: coded sensor (2 OSSD)", 2), ("Guard lock monitored (2 ch)", 2), ("Key switch (2 ch)", 2),
        ("Reset, manual (trailing edge)", 1), ("Room + Shuttle O2 relays (1 per ch)", 2), ("Plate < 50 C: K8DT relay + PLC", 2),
        ("Robot Safe Home (UR safety out, 2 ch)", 2), ("Tray docked (dock pins, 2 ch)", 2), ("Shutter closed switches (2)", 2),
        ("CN708 limit relay (aux)", 1), ("Chamber at ambient: pressure switch", 1), ("Exhaust flow switch", 1),
        ("PLC process permissive + over-temp", 2), ("Laser status: Ready / Emission", 2), ("EDM: K1, K3A+K3B, K4+K5 mirror", 3),
    ]
    y = 19.6
    for name, n in ins:
        box(ax, 0.2, y - 0.38, 7.6, 0.76, f"{name}", fc="#fffaf0" if n == 2 else "#ffffff", fs=6.4)
        for k in range(n):
            line(ax, [(7.8, y - 0.15 + 0.15 * k), (11.0, y - 0.15 + 0.15 * k)], C_SAFE if n >= 2 else C_SIG, 0.9)
        y -= 1.05
    box(ax, 11.0, 1.0, 5.6, 19.0, "Banner XS26-2\n+ XS16si (16 safety inputs)\n+ XS2so (2 safety outputs)\n\n26 + 16 inputs\n4 + 2 safety outputs\n(PNP OSSD, 0.5 A each)\n\nTest pulses on the\ninput pairs, 0.5 s\ndiscrepancy check,\nmanual reset after\nany trip or power loss\n(21 CFR 1040.10(f)(10))\n\nStatus to the PLC\nover Ethernet\n(XS26-2E) or 4\nconvertible outputs", fc="#fdf2e9", ec=C_SAFE, fs=8, bold=False, lw=1.8)
    outs = [
        (18.6, "O1 -> K4 (mirror contacts)", "IPG interlock channel 1 (dry contact, pins 1-4 in the 2012 YLR guide)"),
        (16.6, "O2 -> K5 (mirror contacts)", "IPG interlock channel 2 (pins 2-3); 500 ms laser response"),
        (14.6, "K4 + K5 NO in series", "shutter coil (power to open, spring closed, ~20-50 ms) <- RTC6/PLC request; emission lamps"),
        (12.6, "O3 -> K3A, O4 -> K3B", "48 V servo bus, two contactors in series (no STO on ClearPath-SD)"),
        (10.6, "O5 (XS2so) -> K1", "heater 24 V, in series with K2 (CN708, hard-wired) and the SSR"),
        (8.6, "O6 (XS2so) -> guard lock", "spring-lock, power to unlock (IDEC HS5L-VC44M-G): unlock only laser off, shutter closed, plate < 50 C, chamber ambient"),
        (6.6, "Standard outputs (PLC)", "robot entry permitted (UR reduced mode lifts the guard plane), VLM may move, stack light, HOT lamp"),
        (4.6, "Hard-wired, no controller", "argon supply valve: 24 V through both O2-monitor relays + exhaust flow switch in series"),
        (2.6, "Hard-wired, no controller", "CN708 latching limit opens K2 on its own; RT240 TCO in the block (see heater_loop.md: holding 205 C)"),
    ]
    for yy, a, b in outs:
        line(ax, [(16.6, yy), (18.0, yy)], C_SAFE, 1.4)
        box(ax, 18.0, yy - 0.55, 5.2, 1.1, a, fc="#fdf2e9", ec=C_SAFE, fs=6.6)
        line(ax, [(23.2, yy), (23.8, yy)], C_SAFE, 1.4)
        box(ax, 23.8, yy - 0.55, 8.0, 1.1, b, fc="#ffffff", fs=6.0)
    line(ax, [(20.6, 18.05), (20.6, 17.15)], C_SIG, 0.8, "--")
    ax.text(20.75, 17.6, "mirror contacts -> EDM", fontsize=5.8)
    ax.text(0.2, 0.3, "Laser hazard: two diverse final elements (laser interlock loop via K4+K5, and the shutter). Servo motion: K3A + K3B. Heater: K1 (safety controller) + K2 (CN708) + PLC over-temperature (diverse). "
                      "The RTC6 gate and the PLC only request; neither can close a safety output.", fontsize=6.8)
    fig.savefig(OUT / "interlock.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


def dev(ax, x, y, w, h, label, fc, fs=5.5, rot=90):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="#222222", lw=0.6))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, rotation=rot if w < 40 else 0)


def panels():
    fig = plt.figure(figsize=(17, 11))
    # ---- (a) 4U drawer floor plan, to scale: Middle Atlantic D/UD-class drawer, 403 x 368 mm inside (A1 rows P16)
    ax = fig.add_axes([0.03, 0.40, 0.45, 0.55])
    W, D = 403.0, 368.0
    ax.add_patch(Rectangle((0, 0), W, D, fc="#f2f2f2", ec="k", lw=1.2))
    ax.add_patch(Rectangle((-40, -48), 483, 520, fc="none", ec="#999999", lw=0.8, ls="--"))
    ax.text(-38, 470, "model's DIN-drawer box: 446.6 x 530 mm (cad/lpbf_low.py); front panel 483 mm", fontsize=6, color="#777777")
    # rails along x; front of the drawer at y = 0
    rails = [(12, 140), (166, 300), (322, 360)]
    for y0, y1 in rails:
        ax.add_patch(Rectangle((8, (y0 + y1) / 2 - 17.5), W - 16, 35, fc="#d9d9d9", ec="#888888", lw=0.5))
    # duct between rows
    for yd in (142, 302):
        ax.add_patch(Rectangle((8, yd), W - 16, 22, fc="#cfe2f3", ec="#6fa8dc", lw=0.5))
        ax.text(W / 2, yd + 11, "wire duct 25 x 25", fontsize=5, ha="center", va="center", color="#3d85c6")
    x = 14
    row1 = [(45, 110, "XS26-2\n45x110x129", "#f9cb9c"), (22.5, 110, "XS16si", "#f9cb9c"), (22.5, 110, "XS2so ~", "#f9cb9c"),
            (38.4, 95.4, "P1-540\nCPU", "#b6d7a8")] + [(20.6, 93.6, n, "#b6d7a8") for n in ("16ND3", "16ND3", "16TD2", "16TD2", "04THM", "08ADL", "04DAL")]
    for w, h, lab, fc in row1:
        dev(ax, x, 76 - h / 2, w, h, lab, fc)
        x += w + 1
    ax.text(x + 2, 76, f"row 1: {x - 14:.0f} mm", fontsize=6, va="center")
    x = 14
    row2 = [(89, 127, "ClearCore\n(on DIN-MNT)\n127 x 89", "#a4c2f4"), (30, 100, "SureStep\nSTP-DRV ~", "#a4c2f4"),
            (45, 68, "K3A\nCWBS9", "#f6b26b"), (45, 68, "K3B\nCWBS9", "#f6b26b"), (45, 68, "K4\nCWBS9", "#f6b26b"), (45, 68, "K5\nCWBS9", "#f6b26b"),
            (30, 100, "switch\nSE3-SW8U ~", "#d5a6bd"), (36, 90, "CBMC E4\n36x90x98", "#ffe599")]
    for w, h, lab, fc in row2:
        dev(ax, x, 233 - h / 2, w, h, lab, fc)
        x += w + 1
    ax.text(x + 2, 233, f"row 2: {x - 14:.0f} mm", fontsize=6, va="center")
    x = 14
    for i in range(40):
        dev(ax, x, 341 - 22, 6.2, 44, "", "#eeeeee")
        x += 6.2
    ax.text(x + 4, 341, "row 3: 40 terminal blocks\n(field wiring, 0 V, PE)", fontsize=6, va="center")
    ax.text(W / 2, -24, "front (drawer face, 4U = 177.8 mm): 80 mm fan intake, exhaust at the back; clear height ~164 mm assumed", fontsize=6.5, ha="center")
    ax.set_xlim(-50, 500)
    ax.set_ylim(-60, 490)
    ax.set_aspect("equal")
    ax.set_title("(a) 4U control drawer, floor plan to scale (mm). Inside 403 x 368 (Middle Atlantic D/UD class); '~' = size assumed", fontsize=8)
    ax.set_xlabel("x (mm), across the rack")
    # ---- (b) section: deepest DIN parts vs 3U and 4U drawers
    ax2 = fig.add_axes([0.53, 0.62, 0.44, 0.33])
    parts = [("XS26-2 / SC26-2", 129.0), ("SDR-480-24 / -48", 128.5), ("SDR-240-24 / -48", 113.5), ("CBMC E4", 98.0), ("ClearCore on DIN", 30.0)]
    for i, (n, d) in enumerate(parts):
        ax2.add_patch(Rectangle((i * 60 + 10, 7.5), 40, d, fc="#f9cb9c" if d > 110 else "#b6d7a8", ec="k", lw=0.6))
        ax2.text(i * 60 + 30, 7.5 + d + 3, f"{n}\n{d:.1f}", fontsize=6, ha="center", va="bottom")
    ax2.add_patch(Rectangle((0, 0), 310, 7.5, fc="#bbbbbb", ec="k", lw=0.5))
    for h, lab, c in ((120.0, "3U drawer: ~120 mm clear inside (133.35 outside, sheet + slides)", "#c0392b"),
                      (164.0, "4U drawer: ~164 mm clear (177.8 outside)", "#27ae60")):
        ax2.axhline(h, color=c, lw=1.2, ls="--")
        ax2.text(312, h, lab, fontsize=6.5, color=c, va="center")
    ax2.set_xlim(0, 470)
    ax2.set_ylim(0, 190)
    ax2.set_aspect("equal")
    ax2.set_title("(b) Section: DIN parts stand on a 7.5 mm rail on the drawer floor; depth from the rail (mm)", fontsize=8)
    ax2.set_xticks([])
    # ---- (c) PB1 backplate 16 x 12 in (406 x 305 mm), to scale
    ax3 = fig.add_axes([0.53, 0.05, 0.44, 0.50])
    PW, PH = 406.0, 305.0
    ax3.add_patch(Rectangle((0, 0), PW, PH, fc="#f2f2f2", ec="k", lw=1.2))
    # top row: disconnect + breakers + contactors
    x = 10
    top = [(35, 68, "Q0\nSIRCO M\n30 A", "#ea9999"), (36, 90, "Q1 2P\nD15 ~", "#ea9999"), (36, 90, "Q2 2P\nD15 ~", "#ea9999"),
           (18, 90, "Q3\nC15 ~", "#ea9999"), (18, 90, "Q4\nC6 ~", "#ea9999"), (45, 68, "KM0\nlaser ~", "#f6b26b"),
           (45, 68, "KM1\npump ~", "#f6b26b"), (45, 68, "KM2 ~", "#f6b26b"), (45, 68, "K1\nCWBS12", "#f6b26b"), (45, 68, "K2\nCWBS12", "#f6b26b")]
    for w, h, lab, fc in top:
        dev(ax3, x, 250 - h / 2, w, h, lab, fc)
        x += w + 2
    # middle: DIN supplies
    x = 10
    mid = [(63, 125.2, "SDR-240-24\n+24 V CTRL\n63x125x113.5", "#a4c2f4"), (63, 125.2, "SDR-240-48\n+48 V SERVO", "#a4c2f4"),
           (70, 90, "HDR-100-24\nGALVO", "#a4c2f4"), (17.5, 90, "K8DT\n<50 C", "#ffe599")]
    for w, h, lab, fc in mid:
        dev(ax3, x, 135 - h / 2, w, h, lab, fc)
        x += w + 2
    # heater supply lying flat + SSR heat sink
    dev(ax3, 232, 75, 115, 215 / 2.0, "LRS-350-24\n(215 x 115 x 30,\nchassis, flat)", "#ea9999", rot=0)
    ax3.add_patch(Rectangle((232, 10), 70, 55, fc="#cccccc", ec="k", lw=0.6))
    ax3.text(267, 37, "SSR D1D20 on\nHS151 heat sink\n(through the wall)", fontsize=5.5, ha="center", va="center")
    dev(ax3, 310, 10, 86, 55, "terminals, PE bar\nreceptacle for the\nUPS cord (backed)", "#eeeeee", rot=0)
    ax3.text(PW / 2, -18, "door: CN708 (cutout 71 x 29); Q0 handle Socomec 147E1111 on the front side wall; Fandis 120 mm filter fan + grille", fontsize=6.5, ha="center")
    ax3.set_xlim(-20, 430)
    ax3.set_ylim(-30, 330)
    ax3.set_aspect("equal")
    ax3.set_title("(c) PB1 power box backplate, 16 x 12 in (406 x 305 mm), to scale", fontsize=8)
    fig.savefig(OUT / "panels.png", dpi=120, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    single_line()
    interlock()
    panels()
    print("ok")
