"""Renders of the robot shop's tightest moments (pyvista, offscreen; called by shop_checks.py under xvfb-run)."""
from __future__ import annotations

import numpy as np

import shop_cell as S
import shop_render as R

OUT = R.OUT


def _set_held(arm, seg):
    if seg is not None and seg.get("held") is not None:
        arm.held = seg["held"]
    else:
        arm.held = None


def _mir_items(mirs):
    out = []
    for k, (Mm, dx) in enumerate(mirs):
        for n, vf, c in S.mir_items(dx):
            out.append((f"mir{k}/{n}", S.xf(vf, Mm), c))
    return out


def render_all(shop, ctxs, res):
    see = ("front panel", "roof", "left wall", "back wall", "right wall")
    lay_arms, lay_items = [], []
    if "P3" in ctxs and ctxs["P3"][1].get("q_first"):
        c3 = ctxs["P3"][1]
        c3["A"].place(np.array(c3["q_first"][0]), c3["A"].close)
        c3["B"].place(np.array(c3["q_first"][1]), c3["B"].close)
        lay_arms = [c3["A"], c3["B"]]
        lay_items = _mir_items(c3["mirs"])
    routes = [leg["poly"] for leg in res.get("routes", {}).get("legs", [])]
    R.layout(shop, OUT / "shop_layout.png", arms=lay_arms, extra_items=lay_items, routes=routes)
    if "P1" in ctxs:
        plan, ctx = ctxs["P1"]
        st, arm = ctx["station"], ctx["arm"]
        mir = _mir_items([(S.dock_frame(st, ctx["x_mir"]), S.ARM_DX)])
        cam = [tuple(st.to_world((-1500, -2300, 2300))), tuple(st.to_world((250, 450, 1100))), (0, 0, 1)]
        r = res["P1_vf4_single_arm"]
        tt = r.get("tightest_transit")
        if tt and tt.get("q") is not None:
            seg = plan.segments[tt["segment"]]
            _set_held(arm, seg)
            arm.place(np.array(tt["q"]), seg["close"])
            items = ctx["items"] + mir
            extra = [] if arm.held is not None else [(ctx["part"], S.COL["part"])]
            if arm.held is None:
                ctx["part"].place(ctx["T_vise"])
            R.snap(OUT / "p1_vf4_tightest.png", items, [arm], cam,
                   f"P1 VF-4: tightest moment, {tt['robot_body']} {tt['clear_mm']} mm from {tt['world_body']}",
                   extra=extra, alpha_names=see)
        _set_held(arm, dict(held=ctx["held"]))
        arm.place(ctx["q_place"], plan.segments[5]["close"])
        R.snap(OUT / "p1_vf4_in_vise.png", ctx["items"] + mir, [arm], cam,
               f"P1 VF-4: frame blank (version B, {ctx['kg']:.1f} kg) set in the open vise; HRT210 + tailstock on the left",
               alpha_names=see)
    if "P1b" in ctxs:
        plan, ctx = ctxs["P1b"]
        st, arm = ctx["station"], ctx["arm"]
        tt = res.get("P1_vf4_single_arm_door_1251", {}).get("tightest_transit")
        if tt and tt.get("q") is not None and "x_mir" in ctx:
            seg = plan.segments[tt["segment"]]
            _set_held(arm, seg)
            arm.place(np.array(tt["q"]), seg["close"])
            if arm.held is None:
                ctx["part"].place(ctx["T_vise"])
            mir = _mir_items([(S.dock_frame(st, ctx["x_mir"]), S.ARM_DX)])
            cam = [tuple(st.to_world((-1500, -2300, 2300))), tuple(st.to_world((250, 450, 1100))), (0, 0, 1)]
            R.snap(OUT / "p1_vf4_tightest_door1251.png", ctx["items"] + mir, [arm], cam,
                   f"P1, older 1251 mm door: {tt['robot_body']} {tt['clear_mm']} mm from {tt['world_body']}",
                   extra=[] if arm.held is not None else [(ctx["part"], S.COL["part"])], alpha_names=see)
    if "P2" in ctxs:
        plan, ctx = ctxs["P2"]
        st, arm = ctx["station"], ctx["arm"]
        tt = res.get("P2_lathe", {}).get("tightest_transit")
        if tt and tt.get("q") is not None:
            seg = plan.segments[tt["segment"]]
            _set_held(arm, seg)
            arm.place(np.array(tt["q"]), seg["close"])
            mir = _mir_items([(S.dock_frame(st, 150.0 - S.ARM_DX), S.ARM_DX)])
            cam = [tuple(st.to_world((1600, -2000, 2300))), tuple(st.to_world((0, 0, 1200))), (0, 0, 1)]
            extra = []
            if arm.held is None and "T_deck" in ctx:
                ctx["part"].place(ctx["T_deck"] if tt["segment"] <= 2 else ctx["T_chuck"])
                extra = [(ctx["part"], S.COL["part"])]
            R.snap(OUT / "p2_lathe_tightest.png", ctx["items"] + mir, [arm], cam,
                   f"P2 lathe: tightest moment, {tt['robot_body']} {tt['clear_mm']} mm from {tt['world_body']}",
                   extra=extra, alpha_names=see)
        if "q_in" in ctx:
            mir = _mir_items([(S.dock_frame(st, 150.0 - S.ARM_DX), S.ARM_DX)])
            _set_held(arm, dict(held=ctx["held"]))
            arm.place(ctx["q_in"], plan.segments[6]["close"])
            cam = [tuple(st.to_world((-900, -2200, 2000))), tuple(st.to_world((150, 350, 1000))), (0, 0, 1)]
            R.snap(OUT / "p2_lathe_in_chuck.png", ctx["items"] + mir, [arm], cam,
                   "P2 lathe (ST-10 door, 592 mm): 2-1/8 in. slug pushed into the open jaws", alpha_names=see)
    if "P3" in ctxs:
        r, ctx = ctxs["P3"]
        tt = r.get("tightest") or {}
        if tt.get("qa") is not None:
            A, B = ctx["A"], ctx["B"]
            st = shop["vf4"]
            B.place(np.array(tt["qb"]), B.close)
            A.place(np.array(tt["qa"]), A.close)
            mir = _mir_items(ctx["mirs"])
            cam = [tuple(st.to_world((-1400, -2500, 2500))), tuple(st.to_world((300, 300, 1100))), (0, 0, 1)]
            R.snap(OUT / "p3_two_arms_tightest.png", ctx["items"] + mir, [A, B], cam,
                   f"P3 two arms: roughed block (version A, {r['kg']} kg) drawn toward the door; "
                   f"{tt['bodies'][0]} {tt['clear_mm']} mm from {tt['bodies'][1]}", alpha_names=see)
    if "P6" in ctxs:
        r, ctx = ctxs["P6"]
        if ctx.get("q_first"):
            A, B = ctx["A"], ctx["B"]
            st = shop["vf4"]
            B.place(np.array(ctx["q_first"][1]), B.close)
            A.place(np.array(ctx["q_first"][0]), A.close)
            mir = _mir_items(ctx["mirs"])
            cam = [tuple(st.to_world((-1400, -2500, 2500))), tuple(st.to_world((0, 400, 1050))), (0, 0, 1)]
            R.snap(OUT / "p6_two_arms_plate.png", ctx["items"] + mir, [A, B], cam,
                   f"P6 two arms: optics bridge stock plate ({r['kg']} kg) on its fixture, held by two bolted lifting tabs",
                   alpha_names=see)
    if "P4" in ctxs:
        r, ctx = ctxs["P4"]
        if ctx.get("qs"):
            arm = ctx["arm"]
            arm.held = ctx["held"]
            arm.place(ctx["qs"][len(ctx["qs"]) // 2], arm.close)
            st = shop["receiving"]
            cam = [tuple(st.to_world((1300, -2300, 2200))), tuple(st.to_world((-250, 200, 950))), (0, 0, 1)]
            R.snap(OUT / "p4_box_seam.png", ctx["items"] + _mir_items(ctx.get("mirs", [])), [arm], cam,
                   "P4 receiving: a cutter in the 2F-85 runs along a box's tape seam on the lift table")
