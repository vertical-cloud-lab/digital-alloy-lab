#!/usr/bin/env python3
"""Run the DuckDB and pandas loading examples printed in orchid-data's DATASET_CARD.md ("How to load") against a
local checkout, read-only, and print row counts / heads. Usage: python -I orchid_data_duckdb_card_examples.py --data DIR
"""
import argparse
import os
import time

import duckdb
import pandas as pd

SQL = {
    "invariants_vs_sgte": """
SELECT v.system, v.reaction, v.temperature_K AS T_lit, i.T_K AS T_calc, i.tdb
FROM 'parquet/literature_values.parquet' v
JOIN 'parquet/phase_diagram_invariants.parquet' i USING (system)
WHERE v.property = 'INVARIANT_TEMPERATURE' AND v.evidence_class = 'experimental' AND v.accepted
  AND abs(v.temperature_K - i.T_K) < 20""",
    "dft_vs_experiment": """
SELECT dft_source, count(*) AS n, avg(abs(residual_kJ_per_mol_atom)) AS mae
FROM 'parquet/dft_parity.parquet' WHERE default_subset GROUP BY dft_source""",
    "hull_al_ni": """
SELECT source, formula, x, formation_energy_kJ_per_mol_atom, material_id
FROM 'parquet/hull_vertices.parquet' WHERE system = 'AL-NI' AND NOT is_endpoint ORDER BY source, x""",
    "values_with_papers_cu_zn": """
SELECT v.id, v.property, v.value, v.unit, p.citation, p.year
FROM 'parquet/literature_values.parquet' v JOIN 'parquet/papers.parquet' p ON p.id = v.paper_id
WHERE v.system = 'CU-ZN' LIMIT 20""",
    # same join as the first example, restricted to the Al and Cu binaries of interest
    "invariants_vs_sgte_al_cu_subset": """
SELECT v.system, count(DISTINCT v.id) AS n_lit_exp_accepted, count(*) AS n_pairs_within_20K
FROM 'parquet/literature_values.parquet' v
JOIN 'parquet/phase_diagram_invariants.parquet' i USING (system)
WHERE v.property = 'INVARIANT_TEMPERATURE' AND v.evidence_class = 'experimental' AND v.accepted
  AND abs(v.temperature_K - i.T_K) < 20
  AND v.system IN ('AL-CU','AL-SI','AL-MG','AL-ZR','CU-NI','CU-ZR')
GROUP BY v.system ORDER BY v.system""",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    os.chdir(ap.parse_args().data)  # the card's SQL uses paths relative to the checkout
    con = duckdb.connect()
    pd.set_option("display.width", 200)
    pd.set_option("display.max_colwidth", 60)
    for name, q in SQL.items():
        t = time.time()
        df = con.execute(q).df()
        print(f"== {name}: {len(df)} rows in {time.time() - t:.2f} s")
        if "citation" in df.columns:  # keep author names out of the public log; report coverage only
            print(f"   citation non-null: {int(df.citation.notna().sum())}/{len(df)} (column not printed)")
            df = df.drop(columns=["citation"])
        print(df.head(8).to_string(index=False))
    # pandas example from the card (row-group pruning on system)
    t = time.time()
    df = pd.read_parquet("parquet/literature_values.parquet", filters=[("system", "==", "AL-NI")])
    hf = df[(df.property == "HM_FORM") & (df.unit == "kJ/mol-atom") & (df.evidence_class == "experimental")
            & df.accepted & ~df.flag_unsigned_in_print]
    comps = df.explode("compositions").dropna(subset=["compositions"])
    print(f"== pandas AL-NI example: {len(df)} values, {len(hf)} accepted experimental HM_FORM, "
          f"{len(comps)} exploded composition rows ({time.time() - t:.2f} s)")


if __name__ == "__main__":
    main()
