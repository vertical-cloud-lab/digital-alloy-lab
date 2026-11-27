"""FT-1 control diagrams, drawn from code.

  interlock-ladder.{png,svg}   24 V control circuits as ladder rungs: the G9SE-201's two input channels, its reset, its
                               outputs into the laser's two interlock loops and the RTC5's /STOP; the heater contactors
                               K1 (E-stop + software) and K2 (CN708 limit) and the heater power path; the room-O2 relay
                               K4 and the gas valves; the status lamps
  power-single-line.{png,svg}  the room's circuits to every load
  signal-flow.{png,svg}        PC, RTC5/RTC4, laser, head, Zaber chain, Pi I/O node, analyzers, cameras, recorder, and
                               how the clock and the layer marker tie them to one time base

Run: python desktop-lpbf/fast-track/control/diagrams/draw.py   (schemdraw 0.23, matplotlib)
Pin numbers are from io-list.csv; the laser's are the 24-pin YLR guide's and must be mapped on the 2015 EOS unit.
"""
from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import schemdraw  # noqa: E402
import schemdraw.elements as elm  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
RED, ORANGE, BLUE, GREY, GREEN, PURPLE = "#b2182b", "#d6604d", "#2166ac", "#4d4d4d", "#1b7837", "#762a83"


# ------------------------------------------------------------------------------------------------ ladder
def ladder():
    schemdraw.config(fontsize=9, inches_per_unit=0.42, lw=1.2)
    d = schemdraw.Drawing(show=False)
    W = 30.0          # rail-to-rail width in drawing units
    dy = 2.1

    def rail_label(y, text, color=GREY):
        d.add(elm.Label().at((W / 2, y + 0.9)).label(text, color=color, fontsize=10, halign="center"))

    def rung(y, parts, end, tag="", color="black"):
        """Left rail -> parts (element, label) -> end box -> right rail."""
        d.add(elm.Dot().at((0, y)))
        d.add(elm.Line().at((0, y)).right(0.6).color(color))
        for e, lab in parts:
            d.add(e.right().label(lab, loc="top", fontsize=8).color(color))
            d.add(elm.Line().right(0.4).color(color))
        x_end = d.here[0]
        box_w = 7.0
        x0 = W - box_w - 0.6
        d.add(elm.Line().right(max(x0 - x_end, 0.3)).color(color))
        d.add(elm.Rect(corner1=(0, -0.45), corner2=(box_w, 0.45)).at((x0, y)).color(color))
        d.add(elm.Label().at((x0 + box_w / 2, y)).label(end, fontsize=8, color=color, halign="center", valign="center"))
        d.add(elm.Line().at((x0 + box_w, y)).right(0.6).color(color))
        d.add(elm.Dot())
        if tag:
            d.add(elm.Label().at((-0.4, y)).label(tag, halign="right", fontsize=8, color=GREY))

    y = 0.0
    rail_label(y + 0.6, "LASER SAFETY CHAIN (hard-wired; software can only request emission)", RED)
    rung(y, [(elm.Switch(nc=True), "E-stop NC1"), (elm.Switch(nc=True), "lid D4NS NC1"),
             (elm.Switch(nc=True), "beam tube NC1"), (elm.Switch(action=None), "key NO1 (on)"),
             (elm.Switch(nc=True), "TS tube 75 C"), (elm.Switch(nc=True), "TS window 75 C")],
         "G9SE in 1: T11-T12", "ch 1", RED)
    y -= dy
    rung(y, [(elm.Switch(nc=True), "E-stop NC2"), (elm.Switch(nc=True), "lid D4NS NC2"),
             (elm.Switch(nc=True), "beam tube NC2"), (elm.Switch(action=None), "key NO2 (on)"),
             (elm.Switch(nc=True), "TS tube 75 C"), (elm.Switch(nc=True), "TS window 75 C")],
         "G9SE in 2: T21-T22", "ch 2", RED)
    y -= dy
    rung(y, [(elm.Button(), "SAFETY RESET (NO)")], "G9SE reset: T31-T32", "reset", RED)
    y -= dy
    rung(y, [(elm.Switch(action=None), "G9SE 13-14")], "laser loop ch1: pins 1-4", "out 1", RED)
    y -= dy
    rung(y, [(elm.Switch(action=None), "G9SE 23-24")], "laser loop ch2: pins 2-3", "out 2", RED)
    y -= dy
    rung(y, [(elm.Line().length(2.0), "G9SE X1 (aux, PNP)")], "K3 coil + Pi SAFETY_OK", "status", ORANGE)
    y -= dy
    rung(y, [(elm.Switch(nc=True), "K3 NC (drops with X1)")], "RTC5 /STOP pin 11 -> GND", "hw stop", ORANGE)
    y -= dy
    rung(y, [(elm.Button(), "LASER START (NO)")], "laser Remote START: pins 10-11", "start", ORANGE)
    y -= dy
    rung(y, [(elm.Switch(action=None), "key NO3")], "laser Remote key: pins 8-9", "key", ORANGE)

    y -= 1.6 * dy
    rail_label(y + 0.6, "HEATERS: two contactors in series with the SSRs, neither owned by the PID controllers", BLUE)
    rung(y, [(elm.Switch(nc=True), "E-stop NC3"), (elm.Switch(action=None), "Pi relay HEAT_EN")],
         "K1 coil (5.8 W)", "K1", BLUE)
    y -= dy
    rung(y, [(elm.Switch(action=None), "CN708 relay (opens in alarm, latching)")], "K2 coil (5.8 W)", "K2", BLUE)
    y -= dy
    rung(y, [(elm.Fuse(), "F1 15 A"), (elm.Switch(action=None), "K1"), (elm.Switch(action=None), "K2"),
             (elm.Switch(action=None), "SSR1 D1D20 <- SOLO plate")],
         "plate heaters 2 x 50 W", "24 V HEAT", BLUE)
    y -= dy
    rung(y, [(elm.Line().length(9.6), "(after K2)"), (elm.Switch(action=None), "SSR2 D1D20 <- SOLO block")],
         "block heaters 2 x 50 W", "", BLUE)

    y -= 1.6 * dy
    rail_label(y + 0.6, "GAS: the room-O2 monitor closes the argon in hardware; the Pi only requests", GREEN)
    rung(y, [(elm.Switch(nc=True), "OX-6 alarm relay (NC set, opens at 19.5 %)")], "K4 coil", "K4", GREEN)
    y -= dy
    rung(y, [(elm.Switch(action=None), "K4 NO"), (elm.Switch(action=None), "Pi relay ARGON")],
         "argon main valve (NC)", "argon", GREEN)
    y -= dy
    rung(y, [(elm.Switch(action=None), "K4 NO"), (elm.Switch(action=None), "Pi relay ARGON_LOW")],
         "argon low-flow valve (NC)", "", GREEN)
    y -= dy
    rung(y, [(elm.Switch(action=None), "Pi relay VENT")], "vent valve (NC)", "vent", GREEN)
    y -= dy
    rung(y, [(elm.Switch(action=None), "Pi relay TRACE_SAMPLE (only < 1.5 % O2)")], "trace-cell sample valve (NC)",
         "O2", GREEN)

    y -= 1.6 * dy
    rail_label(y + 0.6, "LAMPS", PURPLE)
    rung(y, [(elm.Line().length(2.0), "laser pin 23 PS Active")], "amber LASER ARMED", "", PURPLE)
    y -= dy
    rung(y, [(elm.Line().length(2.0), "laser pin 24 Emission ON")], "red EMISSION", "", PURPLE)
    y -= dy
    rung(y, [(elm.Switch(action=None), "Pi relay BEACON")], "green SAFE TO OPEN", "", PURPLE)
    # rails
    top, bot = 1.2, y - 0.8
    d.add(elm.Line().at((0, top)).to((0, bot)).color(GREY).linewidth(2.5))
    d.add(elm.Line().at((W, top)).to((W, bot)).color(GREY).linewidth(2.5))
    d.add(elm.Label().at((0, top + 0.5)).label("+24 V CTRL", fontsize=10))
    d.add(elm.Label().at((W, top + 0.5)).label("0 V", fontsize=10))
    d.add(elm.Label().at((W / 2, bot - 1.0)).label(
        "Rungs 'ch 1' and 'ch 2' run from the G9SE's own T11/T21 test outputs, not from the rail. Laser loops: the laser's "
        "own 24 V through the G9SE's dry contacts.\n24 V HEAT rungs: the LRS-350-24 output, not the control rail. Pin "
        "numbers: io-list.csv (laser pins from IPG's 24-pin YLR guide; map the 2015 EOS unit on arrival).",
        fontsize=8, halign="center", color=GREY))
    return d


# ------------------------------------------------------------------------------------------------ block helpers
def box(ax, x, y, w, h, text, fc="#ffffff", ec="#333333", fs=8, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12", fc=fc, ec=ec, lw=1.0))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, weight="bold" if bold else "normal")


def arrow(ax, p0, p1, color=GREY, text="", lw=1.3, ls="-", both=False, fs=6.5, off=(0, 0.12)):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="<|-|>" if both else "-|>", mutation_scale=10, color=color, lw=lw,
                                 ls=ls, shrinkA=2, shrinkB=2))
    if text:
        ax.text((p0[0] + p1[0]) / 2 + off[0], (p0[1] + p1[1]) / 2 + off[1], text, fontsize=fs, color=color,
                ha="center", va="bottom")


def single_line():
    fig, ax = plt.subplots(figsize=(15, 8.6))
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 17.5)
    ax.axis("off")
    ax.set_title("FT-1 power: the room's circuits to every load (power-budget.csv). The E-stop acts through the G9SE "
                 "(laser) and K1 (heaters); mains stay on so the PC, Pi, O2 monitors and argon keep working.", fontsize=10)
    box(ax, 0.3, 14.2, 5.2, 2.6, "Circuit A\n208 or 240 V, 1-phase, L1-L2-PE\n2-pole 15 A breaker (IPG: <= 20 A)\n"
        "lockable disconnect within reach", fc="#fde0dd", fs=8)
    box(ax, 7.0, 14.6, 6.0, 1.8, "IPG YLR-400-SM-EOS\nlabel: 200-240 VAC 10 A max\n~1.4 kW at 400 W out (estimate)",
        fc="#fff5eb", fs=8)
    arrow(ax, (5.5, 15.5), (7.0, 15.5), RED, "", lw=2.2)
    box(ax, 14.5, 14.6, 6.0, 1.8, "interlock loops <- G9SE-201\nmodulation, analog <- RTC5\nRS-232 <- PC", fs=7.5,
        fc="#f7f7f7")
    arrow(ax, (13.0, 15.5), (14.5, 15.5), GREY, "", ls="--")
    box(ax, 0.3, 6.0, 5.2, 7.2, "Circuit B\n120 V, 20 A\n(16 A continuous)\n\ntypical ~440 W (3.7 A)\nmax ~1.1 kW, 14.4 A\n"
        "(sum of rated inputs)\n\npower strip with\nper-load fuses", fc="#fde0dd", fs=8)
    loads = [
        ("PC + monitor (RTC5 or RTC4 in a PCIe slot)", "200 / 400 W"),
        ("2 x 15 V 7 A supplies -> hurrySCAN POWER IN (+/-15 V, DB-9)", "60 / 200 W"),
        ("Mean Well LRS-350-24 -> F1 -> K1 -> K2 -> SSR1/SSR2 -> 4 x 50 W heaters", "70 / 230 W"),
        ("24 V 10 A CTRL supply -> G9SE, SOLO x2, CN708, K1-K4, valves, AO3000, OX-6 x2, lamps, fan, LEDs", "70 / 140 W"),
        ("Zaber PS14S-48V37 48 V -> X-VSR20A -> X-LSM100B (power on the M8 chain)", "20 / 70 W"),
        ("Pi 5 27 W supply (MCC 134, MCC 128, camera, RS-485)", "10 / 27 W"),
        ("LDS12B (photodiode), DCPL2 28 V (AE), PicoScope on USB", "10 / 15 W"),
    ]
    for i, (t, p) in enumerate(loads):
        yy = 12.4 - i * 1.05
        box(ax, 7.0, yy, 15.5, 0.85, t, fs=7.5, fc="#f7fbff")
        ax.text(22.8, yy + 0.42, p, fontsize=7.5, va="center")
        arrow(ax, (5.5, 9.6), (7.0, yy + 0.42), RED, "", lw=1.0)
    ax.text(22.8, 13.45, "typical / max", fontsize=7.5, color=GREY)
    box(ax, 0.3, 2.6, 5.2, 2.4, "Circuit C (only if the laser\nis water-cooled)\n120 V, 15-20 A", fc="#fde0dd", fs=8)
    box(ax, 7.0, 3.1, 9.5, 1.4, "chiller ~1.4 kW cooling (TEYU CW-5200 class):\n0.57-0.79 kW, up to 6.7 A at 110 V",
        fc="#fff5eb", fs=8)
    arrow(ax, (5.5, 3.8), (7.0, 3.8), RED, "", lw=1.6)
    ax.text(0.3, 1.2, "Room must provide: A (208/240 V 15-20 A 2-pole, dedicated, disconnect within reach), B (120 V 20 A), "
            "C if water-cooled; PE bonding of the box, stages and laser (powder: <= 0.1 ohm, PR 266).\nNot computed: "
            "inrush coordination (LRS-350-24 cold start 60 A; the laser's inrush is not published), earth leakage, "
            "available fault current.", fontsize=7.5, color=GREY, va="bottom")
    return fig


def signal_flow():
    fig, ax = plt.subplots(figsize=(16, 8.6))
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 16.2)
    ax.axis("off")
    ax.set_title("FT-1 signal flow and time base. Master clock for the beam: the RTC5's 10 us list clock. The RTC5 raises "
                 "DIGITAL OUT1 for each layer's list; the recorder samples that marker and LASERON with the fast signals.",
                 fontsize=10)
    box(ax, 0.5, 9.0, 7.0, 6.2, "PC (Windows)\n\nftctl supervisor\n(state machine, faults, layer loop)\n\nlog: HDF5, one "
        "time base\n(PC monotonic clock, t = 0 at start)\n\nRTC5 DLL via ctypes\n(RTC4 backend for the XY2-100 head)",
        fc="#f7fbff", fs=8.5, bold=False)
    box(ax, 9.5, 12.8, 6.2, 2.6, "SCANLAB RTC5 PCIe\n10 us list clock (master)\nlist per layer, set_trigger4 trace\n"
        "LASER: LASERON, ANALOG OUT1,\nDIGITAL OUT1 marker, /STOP", fc="#fff5eb", fs=8)
    box(ax, 18.0, 13.6, 5.6, 1.8, "XY2-100 converter\n(RTC5 only; RTC4 direct)", fc="#fff5eb", fs=8)
    box(ax, 25.5, 13.2, 6.0, 2.6, "hurrySCAN 25 + f = 254 mm\nXY2-100 16-bit, 3 status bits/axis\n+/-15 V, water, air",
        fc="#fff5eb", fs=8)
    box(ax, 9.5, 8.8, 6.2, 2.8, "IPG YLR-400-SM-EOS\ngate (modulation), analog 1-10 V\ninterlock ch1/ch2\nRS-232: EMON, STA "
        "(bit 3: back reflection)", fc="#fde0dd", fs=8)
    box(ax, 18.0, 9.9, 5.6, 1.8, "Omron G9SE-201\nE-stop, lid, beam tube, key,\ntemperature switches", fc="#fde0dd", fs=8)
    box(ax, 25.5, 9.0, 6.0, 2.6, "PicoScope 4824A (recorder, USB 3 to the PC)\nA photodiode PDA36A2\nB AE R15I-AST\nC LASERON  D marker\n"
        "E laser power monitor", fc="#f1e4f3", fs=8)
    box(ax, 0.5, 3.4, 7.0, 4.4, "Zaber chain (RS-232 ASCII,\n115,200 baud, M8 daisy chain)\nX-VSR20A piston\n"
        "X-LSM100B recoater\nflags F* = STAGE_FAULT", fc="#e5f5e0", fs=8)
    box(ax, 9.5, 2.2, 8.5, 5.4, "Raspberry Pi 5 I/O node\n(JSON lines over a direct Ethernet link;\n5 s watchdog drops "
        "HEAT_EN)\n\nrelays: ARGON, ARGON_LOW, VENT,\nTRACE_SAMPLE, VIBRATOR, HEAT_EN, LEDS, BEACON\ninputs: SAFETY_OK, "
        "LASER_*, LIMIT_OK,\nROOM_O2_OK, WATER_OK, LID_CLOSED, K1_ON\nMCC 134: window, beam tube, box air, stage TCs\n"
        "MCC 128: 4-20 mA O2 (ppm), O2 (%), room O2", fc="#e5f5e0", fs=7.5)
    box(ax, 20.0, 4.3, 5.4, 2.2, "SOLO PID x 2 (plate, block)\nRS-485 Modbus RTU\n-> SSRs; CN708 limit -> K2",
        fc="#e5f5e0", fs=8)
    box(ax, 20.0, 1.0, 5.4, 2.6, "O2: Alpha Omega 3000 (trace)\n+ % transmitter on the exhaust\nroom: Macurco OX-6\n(4-20 mA each)",
        fc="#e5f5e0", fs=8)
    box(ax, 27.0, 6.0, 4.5, 2.3, "Pi HQ camera\n+ raking LEDs\n(software-timed after\nspread and scan)", fc="#e5f5e0", fs=8)
    # links
    arrow(ax, (7.5, 14.0), (9.5, 14.0), BLUE, "PCIe", both=True)
    arrow(ax, (15.7, 14.5), (18.0, 14.5), BLUE, "SL2-100")
    arrow(ax, (23.6, 14.5), (25.5, 14.5), BLUE, "XY2-100")
    arrow(ax, (12.6, 12.8), (12.6, 11.6), ORANGE, "LASERON gate\nANALOG OUT1", off=(1.6, -0.2))
    arrow(ax, (7.5, 10.6), (9.5, 10.6), GREY, "RS-232", both=True)
    arrow(ax, (18.0, 10.8), (15.7, 10.8), RED, "13-14, 23-24", lw=2.0)
    arrow(ax, (15.7, 13.4), (25.5, 11.0), PURPLE, "LASERON + DIGITAL OUT1 marker (pins 2, 12)", fs=7, off=(1.0, 0.2))
    arrow(ax, (15.7, 9.3), (25.5, 9.3), PURPLE, "power monitor 0-5 V (pin 13)", fs=7, off=(0, -0.45))
    arrow(ax, (19.0, 11.7), (15.7, 12.9), RED, "X1 -> K3 -> /STOP", fs=7, off=(-0.2, 0.05))
    arrow(ax, (4.0, 9.0), (4.0, 7.8), GREEN, "USB-RS232", off=(1.0, 0.0))
    arrow(ax, (7.5, 9.6), (11.0, 7.6), GREEN, "Ethernet (direct)", both=True, off=(-1.4, 0.0))
    arrow(ax, (18.0, 5.4), (20.0, 5.4), GREEN, "RS-485", both=True)
    arrow(ax, (20.0, 2.3), (18.0, 2.9), GREEN, "4-20 mA", both=False)
    arrow(ax, (18.0, 7.15), (27.0, 7.15), GREEN, "CSI (<= 0.5 m: the Pi sits by the camera)", fs=7)
    arrow(ax, (19.0, 9.9), (17.0, 7.6), RED, "X1 status", fs=7, off=(-0.9, -0.1))
    ax.text(0.5, 0.4, "Time base: every supervisor record carries the PC's monotonic time. Fast data: the PicoScope's sample "
            "clock, aligned to each layer by the marker's rising edge and to each vector by LASERON (the same edges are in "
            "the RTC5's own trace).\nSlow data (O2, temperatures, inputs): polled from the Pi at 20 Hz and stamped on the PC "
            "on arrival (< 10 ms on the direct link); logged at 1 Hz.", fontsize=7.5, color=GREY)
    return fig


def main():
    d = ladder()
    d.save(str(HERE / "interlock-ladder.svg"))
    d.save(str(HERE / "interlock-ladder.png"), dpi=150)
    for name, fn in (("power-single-line", single_line), ("signal-flow", signal_flow)):
        fig = fn()
        fig.savefig(HERE / f"{name}.png", dpi=150, bbox_inches="tight")
        fig.savefig(HERE / f"{name}.svg", bbox_inches="tight")
        plt.close(fig)
    print("wrote", sorted(p.name for p in HERE.glob("*.png")))


if __name__ == "__main__":
    main()
