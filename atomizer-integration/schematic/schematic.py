#!/usr/bin/env python3
"""Schematics for #151: the whole data-capture system (block diagram) and the STG1 power tap (circuit).

    python schematic.py      # -> system_schematic.png/.svg, stg1_tap.png/.svg in this folder
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

HERE = Path(__file__).resolve().parent

# signal colours (also the legend)
C = dict(eth="#1f6fd1", analog="#d62728", usb="#222222", csi="#e8780c", rs485="#7b3fb5", wifi="#3fa7d6",
         optical="#8a8a8a", existing="#9a9a9a", ok="#c0161b")
FILL = dict(amazemet="#eef0f3", lab="#fff6ec", pi="#fde8ea", net="#e9f4fb", film="#cfe9fb")


def rbox(ax, x, y, w, h, title, lines=(), fc="white", ec="#333333", lw=1.2, ls="-", tsize=10.0, lsize=8.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.0,rounding_size=0.6", fc=fc, ec=ec, lw=lw, ls=ls,
                                zorder=2))
    ax.text(x + 0.6, y + h - 0.55, title, ha="left", va="top", fontsize=tsize, fontweight="bold", zorder=3)
    for i, t in enumerate(lines):
        ax.text(x + 0.6, y + h - 2.25 - 1.55 * i, t, ha="left", va="top", fontsize=lsize, zorder=3, color="#222")


def line(ax, pts, color, lw=2.2, ls="-", z=1, arrow=False):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=z, solid_capstyle="round")
    if arrow:
        (x0, y0), (x1, y1) = pts[-2], pts[-1]
        ax.annotate("", xy=(x1, y1), xytext=(x0 + (x1 - x0) * 0.6, y0 + (y1 - y0) * 0.6),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=lw), zorder=z)


def tag(ax, x, y, text, color="#222", size=7.6, ha="left", va="center", bg="white", rot=0):
    ax.text(x, y, text, ha=ha, va=va, fontsize=size, color=color, zorder=5, rotation=rot,
            bbox=dict(boxstyle="round,pad=0.18", fc=bg, ec="none", alpha=0.92))


def camera(ax, x, y, label, facing="left"):
    """A small camera glyph: body plus a lens on the side it looks out of."""
    ax.add_patch(Rectangle((x - 1.1, y - 0.8), 2.2, 1.6, fc=C["csi"], ec="#7a3d00", lw=1.0, zorder=4))
    lx = x - 1.1 - 0.6 if facing == "left" else x + 1.1
    ax.add_patch(Rectangle((lx, y - 0.45), 0.6, 0.9, fc="#222", ec="#222", zorder=4))
    ax.text(x, y + 1.25, label, ha="center", va="bottom", fontsize=7.4, zorder=5)


def system():
    fig, ax = plt.subplots(figsize=(17.0, 9.6), dpi=150)
    ax.set_xlim(0, 100)
    ax.set_ylim(-3.2, 55)
    ax.axis("off")
    ax.text(0.5, 54.4, "rePowder data capture (#151): cameras, network and the STG1 power tap", fontsize=15,
            fontweight="bold", va="top")
    ax.text(0.5, 52.4, "Steps 1-2 only watch screens. Steps 3-4 connect to AMAZEMET's controls and wait for their OK "
            "(red outline). Nothing draws power from the machine.", fontsize=9.5, va="top", color="#333")

    # regions
    for (x, w, title, fc) in ((1, 31.5, "AMAZEMET rePowder (their controls, unchanged)", FILL["amazemet"]),
                              (34.5, 30, "Added by the lab", FILL["lab"]),
                              (66.5, 22, "Raspberry Pi 5s", FILL["pi"]),
                              (90.5, 9, "Lab side", FILL["net"])):
        ax.add_patch(FancyBboxPatch((x, 0.2), w, 50.3, boxstyle="round,pad=0,rounding_size=0.8", fc=fc, ec="#c9ccd1",
                                    lw=1.0, zorder=0))
        ax.text(x + 0.7, 49.9, title, fontsize=10.5, fontweight="bold", va="top", color="#444")

    # ------------------------------------------------------------------ AMAZEMET side
    rbox(ax, 2.5, 37.5, 27, 10, "HMI: Weintek cMT2166X (15.6 in, 1920 x 1080)",
         ["1 x Ethernet 10/100, 1 x USB host, COM1/COM3 (RS-232/485)",
          "VNC server (view-only monitor mode), EasyWeb 2.0, FTP",
          "Passwords held by AMAZEMET; ask for the History level"])
    ax.add_patch(Rectangle((29.5, 38.2), 0.8, 8.6, fc=FILL["film"], ec="#6aaad8", lw=0.8, zorder=3))
    tag(ax, 29.9, 47.4, "anti-glare film", size=7.0, ha="center", va="bottom", bg=FILL["amazemet"])
    rbox(ax, 2.5, 26.5, 12.5, 8.5, "PLC", ["model unknown", "right-hand side door", "(TechDoku drawings", "should name it)"])
    rbox(ax, 16.5, 26.5, 13, 8.5, "GU 500 furnace", ["controller: LCD + keypad", "RS-232 + Ethernet for", "Indutherm DMS (Windows)"])
    ax.add_patch(Rectangle((29.5, 27.2), 0.8, 7.0, fc=FILL["film"], ec="#6aaad8", lw=0.8, zorder=3))
    rbox(ax, 16.5, 16.0, 13, 7.5, "Viewing windows", ["front port, door sight", "glass, lid window"])
    rbox(ax, 2.5, 2.0, 27, 11.5, "STG1 ultrasonic generator (SONICTECH, 40 kHz)",
         ["X3 DB15: power OUT 0-10 V, amplitude IN 0-10 V,",
          "   start, clear error, 24 V status lines",
          "X5/X6 RJ45: RS-485 Modbus RTU, address 170",
          "looks like the BASIC variant (no screen), so the HMI is its display"])
    # existing links inside the machine
    line(ax, [(6.0, 13.5), (6.0, 26.5)], C["rs485"], lw=2.0)
    tag(ax, 6.4, 19.0, "RS-485 Modbus RTU\n(PLC is the one master)", color=C["rs485"], size=7.0, bg=FILL["amazemet"])

    # ------------------------------------------------------------------ cameras next to what they watch
    camera(ax, 32.6, 44.5, "CM3 Wide")
    line(ax, [(31.4, 44.5), (30.4, 44.5)], C["optical"], lw=1.4, ls=(0, (2, 1.5)), arrow=True)
    camera(ax, 32.6, 31.5, "CM3")
    line(ax, [(31.4, 31.5), (30.4, 31.5)], C["optical"], lw=1.4, ls=(0, (2, 1.5)), arrow=True)
    camera(ax, 32.6, 19.8, "x3 units")
    line(ax, [(31.4, 19.8), (29.6, 19.8)], C["optical"], lw=1.4, ls=(0, (2, 1.5)), arrow=True)

    # ------------------------------------------------------------------ lab additions
    rbox(ax, 37.5, 39.0, 12, 6.2, "5-port switch", ["USB-C powered", "only if the HMI port is taken"], ec=C["ok"], lw=1.8)
    rbox(ax, 36.0, 26.0, 12.5, 6.0, "Indutherm DMS PC", ["optional, later;", "not part of this plan"], ec="#999", ls="--",
         fc="#fafafa")
    line(ax, [(30.3, 29.0), (36.0, 29.0)], C["existing"], lw=1.6, ls=(0, (3, 2)))
    rbox(ax, 35.5, 5.0, 10.5, 7.5, "DB15 breakout", ["pass-through: all", "15 pins + screw", "terminals"],
         ec=C["ok"], lw=1.8)
    # isolated ADC box with its chain inside
    ax.add_patch(FancyBboxPatch((47.5, 1.4), 16.4, 13.6, boxstyle="round,pad=0,rounding_size=0.6", fc="white",
                                ec=C["ok"], lw=1.8, zorder=2))
    ax.text(48.1, 14.4, "Isolated ADC box", fontsize=9.4, fontweight="bold", va="top", zorder=3)
    for (x, w, t) in ((48.1, 3.4, "200 k /\n100 k\ndivider"), (52.1, 3.3, "ADS1115\n16-bit"), (56.2, 3.6, "MCP2221A\nUSB-I2C"),
                      (60.4, 3.1, "USB\nisolator")):
        ax.add_patch(Rectangle((x, 5.4), w, 5.2, fc="#f3f6ff", ec="#556", lw=0.9, zorder=3))
        ax.text(x + w / 2, 8.0, t, ha="center", va="center", fontsize=7.0, zorder=4)
    for (x0, x1, t) in ((51.5, 52.1, ""), (55.4, 56.2, "I2C"), (59.8, 60.4, "USB")):
        line(ax, [(x0, 8.0), (x1, 8.0)], "#333", lw=1.4, z=3)
        if t:
            ax.text((x0 + x1) / 2, 11.1, t, ha="center", fontsize=6.6, zorder=4)
    line(ax, [(61.95, 2.0), (61.95, 13.2)], C["ok"], lw=1.6, ls=(0, (4, 2)), z=4)
    ax.text(63.6, 1.85, "isolation barrier", ha="right", va="bottom", fontsize=6.8, color=C["ok"], zorder=4)
    ax.text(48.1, 13.25, "printed, clips on the DIN rail;\ninput side floats on the STG1's 0 V", fontsize=6.4, color="#444", va="top", zorder=4, linespacing=1.1)

    # ------------------------------------------------------------------ Pis
    rbox(ax, 67.5, 36.5, 20, 11, "HMI camera Pi (existing)",
         ["Camera Module 3 Wide, flip shutter", "eth0: the HMI's subnet only (static IP)",
          "Wi-Fi: lab network; no routing between", "logs VNC frames, HMI logs, STG1 power"])
    rbox(ax, 67.5, 26.5, 20, 8, "Panel camera Pi (existing)",
         ["Camera Module 3, flip shutter", "reads the GU 500's LCD"])
    rbox(ax, 67.5, 12.5, 20, 12, "Viewport units x3 (PR #189)",
         ["front: HQ (M12) + CM3 Wide,", "   5 in HDMI display", "left: CM3 Wide, 5 in DSI display",
          "top: HQ + 16 mm, 2.8 in DSI display", "each shows its feed locally too"])
    rbox(ax, 91.2, 12.5, 7.8, 35, "Lab network", ["Wi-Fi", "", "Tailscale", "(CI, SSH)", "", "YouTube", "livestreams",
                                                   "", "run log /", "data files"], fc="white")

    # ------------------------------------------------------------------ links
    # CSI ribbons: cameras -> Pis
    line(ax, [(33.7, 44.5), (36.0, 44.5), (36.0, 47.2), (66.0, 47.2), (66.0, 45.5), (67.5, 45.5)], C["csi"], lw=2.4)
    tag(ax, 50.0, 47.2, "camera ribbon (CSI), 500 mm", color=C["csi"], size=7.0, ha="center", bg=FILL["lab"])
    line(ax, [(33.7, 31.5), (35.0, 31.5), (35.0, 33.8), (65.6, 33.8), (65.6, 31.0), (67.5, 31.0)], C["csi"], lw=2.4)
    line(ax, [(33.7, 19.8), (65.2, 19.8), (65.2, 18.5), (67.5, 18.5)], C["csi"], lw=2.4)
    # Ethernet: HMI -> switch -> PLC, switch -> Pi
    line(ax, [(30.3, 41.6), (37.5, 41.6)], C["eth"], lw=2.6)
    line(ax, [(43.5, 39.0), (43.5, 36.2), (11.5, 36.2), (11.5, 35.0)], C["eth"], lw=2.6)
    tag(ax, 26.0, 36.2, "the HMI's existing cable, moved to the switch", color=C["eth"], size=6.8, ha="center",
        bg=FILL["amazemet"])
    line(ax, [(49.5, 42.0), (67.5, 42.0)], C["eth"], lw=2.6)
    tag(ax, 58.5, 43.0, "VNC :5900 (view-only)\nEasyWeb :80, FTP :21", color=C["eth"], size=7.0, ha="center",
        bg=FILL["lab"])
    # X3 through the breakout and back to the PLC
    line(ax, [(29.5, 9.0), (35.5, 9.0)], C["analog"], lw=2.6)
    tag(ax, 32.5, 10.0, "X3", color=C["analog"], size=7.2, ha="center", bg=FILL["amazemet"])
    line(ax, [(40.8, 12.5), (40.8, 24.8), (12.5, 24.8), (12.5, 26.5)], C["existing"], lw=2.2)
    tag(ax, 26.5, 24.8, "X3's existing cable to the PLC, now plugged into the breakout", color="#666", size=6.8,
        ha="center", bg=FILL["amazemet"])
    line(ax, [(46.0, 8.6), (48.1, 8.6)], C["analog"], lw=2.0)
    line(ax, [(46.0, 7.2), (48.1, 7.2)], "#111", lw=2.0)
    tag(ax, 47.3, 3.6, "power out + 0 V", color=C["analog"], size=6.6, ha="right", bg=FILL["lab"])
    # USB: ADC box -> HMI camera Pi
    line(ax, [(63.9, 8.0), (64.8, 8.0), (64.8, 38.0), (67.5, 38.0)], C["usb"], lw=2.4)
    tag(ax, 64.8, 27.6, "USB", color=C["usb"], size=7.0, ha="center", bg=FILL["lab"], rot=90)
    # Wi-Fi: Pis -> lab network
    for y in (41.0, 30.0, 18.0):
        line(ax, [(87.5, y), (91.2, y)], C["wifi"], lw=2.0, ls=(0, (1.2, 1.2)))

    # legend
    items = [("Ethernet", C["eth"], "-"), ("analog 0-10 V", C["analog"], "-"), ("USB", C["usb"], "-"),
             ("camera ribbon (CSI)", C["csi"], "-"), ("RS-485 (existing)", C["rs485"], "-"),
             ("Wi-Fi", C["wifi"], (0, (1.2, 1.2))), ("camera's view", C["optical"], (0, (2, 1.5))),
             ("existing cable", C["existing"], "-")]
    x = 1.0
    for t, col, ls in items:
        ax.plot([x, x + 2.4], [-1.9, -1.9], color=col, lw=2.6, ls=ls)
        ax.text(x + 2.8, -1.9, t, va="center", fontsize=8.2)
        x += 4.0 + 0.62 * len(t)
    ax.add_patch(Rectangle((x, -2.5), 2.4, 1.2, fc="white", ec=C["ok"], lw=1.8))
    ax.text(x + 2.8, -1.9, "needs AMAZEMET's OK", va="center", fontsize=8.2)
    fig.tight_layout(pad=0.4)
    for ext in ("png", "svg"):
        fig.savefig(HERE / f"system_schematic.{ext}", facecolor="white")
    plt.close(fig)


def tap():
    import schemdraw
    import schemdraw.elements as elm

    schemdraw.config(fontsize=11, lw=1.6)
    d = schemdraw.Drawing(show=False)
    d.config(unit=2.5)
    pin = elm.IcPin
    x3 = d.add(elm.Ic(pins=[pin(name="PWR OUT", anchorname="pwr", side="right", slot="2/2"),
                            pin(name="0 V", anchorname="zero", side="right", slot="1/2")],
                      size=(4.6, 2.6), label="STG1\nX3 (DB15)").theta(0))
    d.add(elm.Line().at(x3.pwr).right(1.4))
    n_bo = d.add(elm.Dot())
    d.add(elm.Line().at(n_bo.center).up(1.6).color("#888888"))
    d.add(elm.Label().at((n_bo.center[0], n_bo.center[1] + 2.0)).label("to the PLC: the breakout passes all 15 pins",
                                                                      color="#666666", fontsize=10))
    d.add(elm.Resistor().at(n_bo.center).right().label("R1  200 kΩ"))
    n_a = d.add(elm.Dot())
    y_rail = n_a.center[1] - 3.4
    d.add(elm.Resistor().at(n_a.center).down().toy(y_rail).label("R2\n100 kΩ", loc="bottom"))
    d.add(elm.Line().at(n_a.center).right(2.4))
    n_c = d.add(elm.Dot())
    d.add(elm.Capacitor().at(n_c.center).down().toy(y_rail).label("C1\n100 nF", loc="bottom"))
    d.add(elm.Line().at(n_c.center).right(1.4))
    a0 = d.here
    # 0 V rail from X3's 0 V pin
    d.add(elm.Line().at(x3.zero).right(1.4))
    d.add(elm.Line().toy(y_rail))
    rail0 = d.here
    ads = d.add(elm.Ic(pins=[pin(name="A0", anchorname="a0", side="left", slot="3/3"),
                             pin(name="GND", anchorname="gnd", side="left", slot="1/3"),
                             pin(name="VDD", anchorname="vdd", side="top"),
                             pin(name="SDA", anchorname="sda", side="right", slot="2/2"),
                             pin(name="SCL", anchorname="scl", side="right", slot="1/2")],
                       size=(5.2, 3.4), label="ADS1115\n16-bit\nPGA ±4.096 V").theta(0).anchor("a0").at(a0))
    d.add(elm.Line().at(ads.gnd).left(0.7))
    d.add(elm.Line().toy(y_rail))
    d.add(elm.Line().at(rail0).tox(ads.gnd[0] - 0.7))
    d.add(elm.Ground().at(((rail0[0] + ads.gnd[0]) / 2, y_rail)).label("floating 0 V (= the STG1's 0 V)", loc="right",
                                                                        fontsize=10))
    d.add(elm.Line().at(ads.vdd).up(0.9))
    d.add(elm.Label().at((ads.vdd[0], ads.vdd[1] + 1.3)).label("+5 V from the isolated side", fontsize=10))
    mcp = d.add(elm.Ic(pins=[pin(name="SDA", anchorname="sda", side="left", slot="2/2"),
                             pin(name="SCL", anchorname="scl", side="left", slot="1/2"),
                             pin(name="USB", anchorname="usb", side="right")],
                       size=(4.6, 2.8), label="MCP2221A\nUSB-I2C").theta(0).anchor("sda")
                .at((ads.sda[0] + 2.2, ads.sda[1])))
    d.add(elm.Line().at(ads.sda).to(mcp.sda))
    d.add(elm.Line().at(ads.scl).to(mcp.scl))
    iso = d.add(elm.Ic(pins=[pin(name="iso side", anchorname="iso", side="left"), pin(name="Pi side", anchorname="pi", side="right")],
                       size=(5.4, 2.8), label="USB isolator\nADuM3160 class").theta(0).anchor("iso")
                .at((mcp.usb[0] + 1.8, mcp.usb[1])))
    d.add(elm.Line().at(mcp.usb).to(iso.iso))
    cx = (iso.iso[0] + iso.pi[0]) / 2
    d.add(elm.Line().at((cx, iso.iso[1] - 3.0)).to((cx, iso.iso[1] + 3.0)).linestyle("--").color("#c0161b"))
    d.add(elm.Label().at((cx, iso.iso[1] - 3.5)).label("isolation barrier", color="#c0161b", fontsize=10))
    d.add(elm.Line().at(iso.pi).right(1.4))
    d.add(elm.Label().label("USB to the\nHMI camera Pi", loc="right", fontsize=10).at((iso.pi[0] + 1.5, iso.pi[1])))
    d.add(elm.Label().at((x3.zero[0] - 3.4, y_rail - 2.6)).label(
        "0-10 V ÷ 3 → 0-3.33 V at A0.  The STG1 output sees 300 kΩ (33 µA at 10 V).  "
        "R1 limits the current into A0 if the input ever goes over range.\n"
        "Pin numbers for PWR OUT and 0 V: STG1 manual pp. 21-27; check them on the breakout before wiring.",
        fontsize=9.5, halign="left"))
    d.save(str(HERE / "stg1_tap.svg"))
    d.save(str(HERE / "stg1_tap.png"), dpi=170)


if __name__ == "__main__":
    system()
    tap()
    print("wrote", *sorted(p.name for p in HERE.glob("*.png")))
