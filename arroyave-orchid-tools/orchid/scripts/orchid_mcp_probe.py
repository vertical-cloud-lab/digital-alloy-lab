#!/usr/bin/env python3
"""Follow-up probes on the orchid-mcp stdio server: accepted vs all records for the gaps the main driver found
(Al-Si and Cu-Ni literature invariants, Al2Cu literature formation enthalpy), the DFT entries behind the Al2Cu
"lowest" values, and literature-vs-SGTE invariant matches for Al-Cu / Al-Mg / Al-Zr.

Usage: /tmp/sbx/clean <venv>/bin/python -I orchid_mcp_probe.py --server <venv>/bin/orchid-mcp \
          --data-dir D --site-dir S --cache-dir C --out <results>/data --log <results>/logs/orchid-mcp-probe.log
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orchid_mcp_drive import Client, parse_result  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    for k in ("--server", "--data-dir", "--site-dir", "--cache-dir", "--out", "--log"):
        ap.add_argument(k, required=True)
    a = ap.parse_args()
    env = {k: os.environ[k] for k in ("PATH", "HOME", "LANG", "LC_ALL", "TMPDIR") if k in os.environ}
    env.update({"ORCHID_DATA_DIR": a.data_dir, "ORCHID_SITE_DATA_DIR": a.site_dir, "ORCHID_OFFLINE": "1",
                "ORCHID_CACHE_DIR": a.cache_dir, "XDG_CACHE_HOME": a.cache_dir})
    log = open(a.log, "w")

    def say(s: str) -> None:
        print(s, flush=True)
        log.write(s + "\n")

    cl = Client(shlex.split(a.server), env, Path(a.log).with_suffix(".stderr.log"))
    cl.request("initialize", {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "probe", "version": "0"}})
    cl.notify("notifications/initialized")

    def tool(name: str, args: dict):
        msg, dt, nb = cl.request("tools/call", {"name": name, "arguments": args})
        err, payload, etext = parse_result(msg)
        say(f"{name}({json.dumps(args)}) {dt*1000:.1f} ms {nb} B {'ERROR ' + str(etext)[:300] if err else 'ok'}")
        return payload

    out: dict = {"accepted_vs_all": {}, "al2cu_dft_entries": {}, "invariant_matches": {}}
    for system in ("Al-Si", "Cu-Ni", "Al-Cu", "Al-Mg", "Al-Zr"):
        row = {}
        for acc in (True, False):
            p = tool("get_invariant_reactions", {"system": system, "source": "literature", "accepted_only": acc, "limit": 1})
            row[f"literature_invariants_accepted_only={acc}"] = p.get("literature_total") if isinstance(p, dict) else p
        sd = tool("get_system_data", {"system": system, "limit": 1})
        if isinstance(sd, dict):
            row["system_data_total_accepted"] = sd.get("total")
            row["system_data_by_property_group"] = sd.get("matching_by_property_group")
        sd2 = tool("get_system_data", {"system": system, "limit": 1, "accepted_only": False})
        if isinstance(sd2, dict):
            row["system_data_total_all"] = sd2.get("total")
        out["accepted_vs_all"][system] = row
    for formula in ("Al2Cu", "Al3Zr"):
        row = {}
        for acc in (True, False):
            p = tool("get_formation_enthalpy", {"formula": formula, "accepted_only": acc})
            if isinstance(p, dict):
                lit = p.get("literature") or []
                row[f"accepted_only={acc}"] = {
                    "n_literature": len(lit), "n_literature_other_units": len(p.get("literature_other_units") or []),
                    "literature": [{k: r.get(k) for k in ("id", "value", "unit", "T_K", "phases", "evidence_class", "accepted",
                                                           "gate_failures", "doi", "page", "system")} for r in lit[:12]],
                    "summary": p.get("summary")}
                if acc:
                    for layer, d in (p.get("dft") or {}).items():
                        out["al2cu_dft_entries"].setdefault(formula, {})[layer] = [
                            {k: e.get(k) for k in ("formula", "phase", "spacegroup_symbol", "spacegroup_number", "theoretical",
                                                   "on_hull", "energy_above_hull_eV", "formation_energy_kJ_per_mol_atom", "nsites")}
                            for e in (d.get("entries") or [])[:8]]
        out["accepted_vs_all"][formula] = row
    flat = []
    for system in ("Al-Cu", "Al-Mg", "Al-Zr", "Al-Si", "Cu-Ni"):
        # source="both" so literature_matches are computed against every accepted literature invariant;
        # limit=1 keeps the literature page itself small.
        p = tool("get_invariant_reactions", {"system": system, "source": "both", "limit": 1})
        rows = []
        for c in (p or {}).get("calculated") or []:
            for inv in c.get("invariants") or []:
                pts = inv.get("points") or []
                bm = inv.get("literature_matches") or []
                ex = [m for m in bm if m.get("evidence_class") == "experimental"]
                row = {"system": system, "tdb": c.get("tdb"), "T_calc_K": inv.get("T"),
                       "phases": "+".join(sorted({(q.get("phase") or "") for q in pts})),
                       "x_points": ";".join(f"{q.get('x')}" for q in pts),
                       "n_lit_matches_shown": len(bm),
                       "best_T_lit_K": bm[0]["T_K"] if bm else None, "best_dT_K": bm[0]["dT_K"] if bm else None,
                       "best_evidence_class": bm[0]["evidence_class"] if bm else None,
                       "best_exp_T_lit_K": ex[0]["T_K"] if ex else None, "best_exp_dT_K": ex[0]["dT_K"] if ex else None,
                       "best_exp_id": ex[0]["id"] if ex else None}
                rows.append(row)
                flat.append(row)
        out["invariant_matches"][system] = rows
    import csv
    with open(Path(a.out, "mcp_invariants_sgte_vs_literature.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(flat[0]))
        w.writeheader()
        w.writerows(flat)
    cl.close()
    Path(a.out, "mcp_probe_accepted_vs_all.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    log.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
