#!/usr/bin/env python3
"""ORCHID data coverage for the Al and Cu systems of interest, and the experimental literature invariants.

Reads a local orchid-data checkout (read-only) and writes:
  <out>/al-cu-coverage.csv               one row per chemical system (binaries, their subsystems, ternaries, quaternaries)
  <out>/al-cu-literature-invariants.csv  experimental literature invariant reactions for 6 binaries

Usage:
  python -I orchid_data_coverage.py --data /path/to/orchid-data --out /path/to/results/data

Column definitions are printed with --describe (and recorded in the report). Only pandas + pyarrow are needed.
"""
import argparse
import itertools
import json
import os
import sys

import pandas as pd

SYMBOLS = {"AL": "Al", "CU": "Cu", "SI": "Si", "MG": "Mg", "ZR": "Zr", "MN": "Mn", "CR": "Cr", "FE": "Fe",
           "NI": "Ni", "SC": "Sc", "SN": "Sn", "BE": "Be"}
REQUESTED = ["AL-CU", "AL-SI", "AL-MG", "AL-ZR", "AL-MN", "AL-CR", "AL-FE", "AL-NI", "AL-SC",
             "CU-NI", "CU-ZR", "CU-SN", "CU-CR", "CU-FE", "CU-BE"]
FAMILIES = {"Al-Si-Mg": ["AL", "SI", "MG"], "Al-Mn-Cr-Zr": ["AL", "MN", "CR", "ZR"], "Cu-Al-Ni-Fe": ["CU", "AL", "NI", "FE"]}
INVARIANT_SYSTEMS = ["AL-SI", "AL-CU", "AL-MG", "AL-ZR", "CU-NI", "CU-ZR"]  # Cu-Al is AL-CU in ORCHID naming


def sysname(elements):
    return "-".join(sorted(elements))


def label(system):
    return "–".join(SYMBOLS.get(e, e.title()) for e in system.split("-"))


def system_list():
    rows = [(sysname(s.split("-")), "requested binary") for s in REQUESTED]
    seen = {sysname(s.split("-")) for s in REQUESTED}
    for fam, els in FAMILIES.items():
        for k in range(2, len(els) + 1):
            for combo in itertools.combinations(els, k):
                s = sysname(combo)
                if s in seen:
                    continue
                seen.add(s)
                rows.append((s, f"{'subsystem binary' if k == 2 else ('ternary' if k == 3 else 'quaternary')} of {fam}"))
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    D = a.data.rstrip("/") + "/"
    os.makedirs(a.out, exist_ok=True)

    systems = system_list()
    names = [s for s, _ in systems]

    lv = pd.read_parquet(D + "parquet/literature_values.parquet")
    lv = lv[lv.system.isin(names)].copy()
    ei = pd.read_csv(D + "espei/index.csv")
    pdi = pd.read_parquet(D + "parquet/phase_diagram_index.parquet")
    pinv = pd.read_parquet(D + "parquet/phase_diagram_invariants.parquet")
    apa = pd.read_parquet(D + "assessed-phase-assemblages/records.parquet", columns=["id", "system"])
    hv = pd.read_parquet(D + "parquet/hull_vertices.parquet")
    dp = pd.read_parquet(D + "parquet/dft_parity.parquet")
    papers = pd.read_parquet(D + "parquet/papers.parquet")

    out = []
    for s, group in systems:
        v = lv[lv.system == s]
        acc = v[v.accepted]
        inv = v[v.property == "INVARIANT_TEMPERATURE"]
        inv_exp = inv[inv.evidence_class == "experimental"]
        e = ei[ei.system == s]
        d = pdi[pdi.system == s]
        reg_path = D + f"phases/systems/{s}.json"
        n_reg = len(json.load(open(reg_path))["phases"]) if os.path.exists(reg_path) else 0
        h = hv[(hv.system == s) & (~hv.is_endpoint)]
        row = {
            "system": s, "label": label(s), "group": group, "n_elements": len(s.split("-")),
            # literature_values (parquet), filtered on `system` (the system of the record's own state)
            "lit_values_all": len(v),
            "lit_values_accepted": int(v.accepted.sum()),
            "lit_values_accepted_unique": int((v.accepted & v.duplicate_of.isna()).sum()),
            "lit_papers": v.paper_id.nunique(),
            "lit_acc_experimental": int((acc.evidence_class == "experimental").sum()),
            "lit_acc_model": int((acc.evidence_class == "model").sum()),
            "lit_acc_dft": int((acc.evidence_class == "dft").sum()),
            "lit_acc_unspecified": int((acc.evidence_class == "unspecified").sum()),
            "lit_espei_ready": int(v.flag_espei_ready.fillna(False).astype(bool).sum()),
            "lit_espei_certified": int(v.flag_espei_certified.fillna(False).astype(bool).sum()),
            "lit_hm_form_exp_accepted": int(((acc.property == "HM_FORM") & (acc.evidence_class == "experimental")).sum()),
            "lit_phase_composition_exp_accepted": int(((acc.property == "PHASE_COMPOSITION") & (acc.evidence_class == "experimental")).sum()),
            "inv_all": len(inv),
            "inv_accepted": int(inv.accepted.sum()),
            "inv_experimental_all": len(inv_exp),
            "inv_experimental_accepted": int(inv_exp.accepted.sum()),
            "inv_experimental_accepted_unique": int((inv_exp.accepted & inv_exp.duplicate_of.isna()).sum()),
            "inv_model_accepted": int(((inv.evidence_class == "model") & inv.accepted).sum()),
            "inv_plausibility_pass": int((inv.plausibility_result == "pass").sum()),
            "inv_plausibility_fail": int((inv.plausibility_result == "fail").sum()),
            # espei/index.csv, one row per ESPEI dataset file, by `folder`
            "espei_datasets_total": len(e),
            "espei_values_total": int(e.n_values.fillna(0).sum()),
            "espei_experimental": int((e.folder == "experimental").sum()),
            "espei_invariants": int((e.folder == "invariants").sum()),
            "espei_model": int((e.folder == "model").sum()),
            "espei_dft_literature": int((e.folder == "dft/literature").sum()),
            "espei_dft_mp": int((e.folder == "dft/mp").sum()),
            "espei_dft_oqmd": int((e.folder == "dft/oqmd").sum()),
            "espei_assessed": int((e.folder == "assessed").sum()),
            "espei_derived": int(e.folder.str.startswith("derived/").sum()),
            # phase_diagram_index / phase_diagram_invariants: SGTE binary collection TDBs computed with pycalphad
            "sgte_tdbs_ok": int((d.status == "ok").sum()),
            "sgte_tdbs_failed": int((d.status != "ok").sum()),
            "sgte_tdb_files": ";".join(sorted(d.tdb.tolist())),
            "sgte_calc_invariants": int((pinv.system == s).sum()),
            "assessed_assemblage_points": int((apa.system == s).sum()),
            "phase_registry_phases": n_reg,
            "hull_vertices_mp": int((h.source == "mp").sum()),
            "hull_vertices_oqmd": int((h.source == "oqmd").sum()),
            "dft_parity_rows": int((dp.system == s).sum()),
            "dft_parity_default_subset": int(((dp.system == s) & dp.default_subset).sum()),
        }
        out.append(row)
    cov = pd.DataFrame(out)
    cov.to_csv(os.path.join(a.out, "al-cu-coverage.csv"), index=False)

    # ---- experimental literature invariants for six binaries
    pmeta = papers.set_index("id")[["title", "year"]]
    inv = lv[(lv.system.isin(INVARIANT_SYSTEMS)) & (lv.property == "INVARIANT_TEMPERATURE")
             & (lv.evidence_class == "experimental")].copy()

    def comps(row):
        b = row.system.split("-")[1]
        a_ = row.system.split("-")[0]
        parts, js = [], []
        for c in (row.compositions if row.compositions is not None else []):
            js.append({k: (None if (isinstance(c[k], float) and pd.isna(c[k])) else c[k]) for k in ("phase", "element", "value", "basis", "source")})
            if c.get("basis") != "mole_fraction" or c.get("value") is None:
                continue
            x = c["value"] if c["element"] == b else (1 - c["value"] if c["element"] == a_ else None)
            if x is not None:
                parts.append(f"{c['phase']}={round(float(x), 5)}")
        return pd.Series({"x_component": b, "x_by_phase": "; ".join(parts), "n_compositions": len(js),
                          "compositions_json": json.dumps(js, ensure_ascii=False) if js else ""})

    def lst(x):
        return "; ".join(str(i) for i in x) if x is not None and len(x) else ""

    def gate_codes(x):
        if x is None or not len(x):
            return ""
        return "; ".join(sorted({(g.get("code", "") if isinstance(g, dict) else str(g)) for g in x}))

    def strip_doi(x):
        # origin_measured_in is "doi:<doi>" when resolved; other forms ("unresolved:...", "this_work") -> ""
        if not isinstance(x, str):
            return ""
        return x[4:] if x.startswith("doi:") else ""

    inv = pd.concat([inv, inv.apply(comps, axis=1)], axis=1)
    res = pd.DataFrame({
        "system": inv.system, "system_label": inv.system.map(label), "record_id": inv.id, "pid": inv.pid,
        "duplicate_of": inv.duplicate_of, "accepted": inv.accepted,
        "espei_ready": inv.flag_espei_ready, "espei_certified": inv.flag_espei_certified,
        "T_K": inv.temperature_K, "T_C": (inv.temperature_K - 273.15).round(2), "temperature_printed": inv.temperature_printed,
        "reaction_printed": inv.reaction, "reaction_type": inv.reaction_type, "transition_kind": inv.transition_kind,
        "phases": inv.phases.map(lst), "model_phases": inv.model_phases.map(lst),
        "x_component": inv.x_component, "x_by_phase_mole_fraction": inv.x_by_phase,
        "n_compositions": inv.n_compositions, "compositions_json": inv.compositions_json,
        "plausibility_result": inv.plausibility_result, "plausibility_dT_K": inv.plausibility_dT_K,
        "plausibility_model_tdb": inv.plausibility_model,
        "paper_doi": inv.paper_doi, "paper_title": inv.paper_id.map(pmeta.title), "paper_year": inv.paper_id.map(pmeta.year),
        "measured_in_doi": inv.origin_measured_in.map(strip_doi), "measured_in_raw": inv.origin_measured_in,
        "cited_dois": inv.cited_dois.map(lst),
        "origin": inv.origin, "conditions_kind": inv.conditions_kind, "record_kind": inv.record_kind,
        "observation_type": inv.observation_type, "page": inv.page, "table_row": inv.table_row,
        "reader_agreement": inv.reader_agreement_label, "gate_failure_codes": inv.gate_failures.map(gate_codes),
    }).sort_values(["system", "T_K", "record_id"])
    res.to_csv(os.path.join(a.out, "al-cu-literature-invariants.csv"), index=False)

    # ---- summary to stdout
    pd.set_option("display.width", 250)
    cols = ["system", "group", "lit_values_all", "lit_values_accepted", "lit_acc_experimental", "lit_acc_model",
            "lit_acc_dft", "inv_all", "inv_experimental_accepted", "espei_datasets_total", "sgte_tdbs_ok",
            "sgte_calc_invariants", "assessed_assemblage_points"]
    print(cov[cols].to_string(index=False))
    print()
    print("experimental literature invariants:", len(res), "rows;",
          res.groupby("system").agg(n=("record_id", "size"), accepted=("accepted", "sum"),
                                    with_x=("n_compositions", lambda s: int((s > 0).sum())),
                                    espei_ready=("espei_ready", "sum")).to_dict("index"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
