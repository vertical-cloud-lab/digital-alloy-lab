## orchid-mcp

**What it is.** An MCP server (15 tools, 4 resources, 1 prompt) over the ORCHID data release. It serves literature
values with provenance, the calculated SGTE binary diagrams, Materials Project and OQMD hulls, and the TDB catalogue.
It runs either on the official `mcp` SDK (pinned `mcp==2.3.0`) or on a stdlib-only built-in JSON-RPC stdio loop.
Commit tested: `f3a4743` (2026-11-02). Local data: orchid-data `c4ebfb6` (2026-10-30) and orchid-project.org
`786f64f` (2026-11-01). Both were read-only. The tests ran from a copy at `/tmp/arroyave/work/orchid-mcp`.

**Outcome: PASS.** Both installs worked. The full test suite passed in both venvs, with and without local data. The
stdio server ran offline on both back ends (SDK and fallback) and answered every requested tool for Al–Cu, Al–Si,
Al–Mg, Al–Zr and Cu–Ni. The two back ends returned byte-identical payloads for all 40 non-error tool calls. No tool
crashed. The only errors were the ones I provoked on purpose, plus the "no data" errors listed under the findings.

### Commands
```bash
U=/home/runner/.local/bin/uv; V=/tmp/arroyave/venvs; W=/tmp/arroyave/work/orchid-mcp
D=/tmp/arroyave/src/orchid-calphad__orchid-data; S=/tmp/arroyave/src/orchid-calphad__orchid-project.org/data
cp -a /tmp/arroyave/src/orchid-calphad__orchid-mcp $W
/tmp/sbx/clean $U venv --python 3.12 $V/orchid-mcp-plain && /tmp/sbx/clean $U venv --python 3.12 $V/orchid-mcp-mcp
/tmp/sbx/clean $U pip install --python $V/orchid-mcp-plain/bin/python -e "$W[test]"       # 7 pkgs, 0.6 s
/tmp/sbx/clean $U pip install --python $V/orchid-mcp-mcp/bin/python   -e "$W[mcp,test]"   # 35 pkgs (mcp 2.3.0), 0.8 s
# tests, CI mode (no data) and with local data, in each venv
/tmp/sbx/clean bash -c "cd $W && $V/orchid-mcp-<v>/bin/python -m pytest -q -p no:cacheprovider -rs"
/tmp/sbx/clean env ORCHID_TEST_DATA_DIR=$D ORCHID_TEST_SITE_DATA_DIR=$S bash -c "cd $W && $V/orchid-mcp-<v>/bin/python -m pytest -q -p no:cacheprovider -rs --durations=10"
# JSON-RPC driver: starts `orchid-mcp` with ORCHID_DATA_DIR=$D ORCHID_SITE_DATA_DIR=$S ORCHID_OFFLINE=1
/tmp/sbx/clean $V/orchid-mcp-mcp/bin/python -I scripts/orchid_mcp_drive.py --server "$V/orchid-mcp-mcp/bin/orchid-mcp" \
   --label sdk --data-dir $D --site-dir $S --cache-dir /tmp/arroyave/work/orchid-mcp-cache --out data --log logs/orchid-mcp-stdio-sdk.log --save-trimmed
/tmp/sbx/clean $V/orchid-mcp-plain/bin/python -I scripts/orchid_mcp_drive.py --server "$V/orchid-mcp-plain/bin/orchid-mcp" --label fallback ...
/tmp/sbx/clean $V/orchid-mcp-mcp/bin/python -I scripts/orchid_mcp_probe.py ...          # accepted-vs-all and SGTE-vs-literature follow-ups
/tmp/sbx/clean $V/orchid-mcp-<v>/bin/python -I scripts/orchid_mcp_readme_sizes.py ...    # re-measures the README's CU-ZR size table
```
The driver sends `initialize`, then `notifications/initialized`, `tools/list` and 41 `tools/call` requests, each with
a 120 s timeout. For each of the 5 systems it calls `get_invariant_reactions` (`source="both"`, `limit=200`),
`get_phase_diagram` once with no point and once at 1 or 2 (x, T) points, `list_tdb_files` (pair, then `exact`) and
`compare_to_dft`. It then calls `get_formation_enthalpy` for Al2Cu, Al3Zr and Al3Mg2, plus `list_tdb_files`,
`search_systems([Al])` and `search_systems([Cu])`, and one call with a deliberately bad assessment name.

### Tests and timings
| venv | pytest, no data (CI mode) | pytest, with local data |
|---|---|---|
| plain (stdlib fallback) | 28 passed, 24 skipped, 1.4 s | 51 passed, 1 skipped (`mcp SDK not installed`), 4.3 s |
| `[mcp]` (mcp 2.3.0) | 28 passed, 24 skipped, 1.5 s | **52 passed**, 5.9 s |

Server timings over stdio:
- **Startup (`initialize`):** 2.0–3.1 s on the SDK, mostly from importing `mcp`/pydantic; 0.12–0.15 s on the fallback.
- **The 41 tool calls:** median 10 ms on the SDK and 5 ms on the fallback. The slowest call was 0.35 s
  (`get_invariant_reactions("Al-Zr", limit=200)`).
- **Whole session wall time:** 4.8–6.3 s on the SDK and 1.4–1.8 s on the fallback.

### Key numbers
Columns, left to right: accepted literature invariants (all records in brackets); SGTE diagrams; calculated
invariants per assessment; of those, how many have a literature match (same phase set), how many have an
experimental match, and how many experimental matches fall within 10 K; and the median |dT| of the best
experimental match.
| system | lit. invariants accepted (all) | SGTE diagrams | calc. invariants / lit. match / exp. match / exp. within 10 K | median \|dT\| best exp. match |
|---|---|---|---|---|
| Al–Cu | 80 (83) | 5 | 02Mie 7/4/3/2 · 04Wit 14/1/0/0 · 15Lia 17/7/7/4 · 21Kro 19/13/11/9 · 98Sau-LB 14/1/0/0 | 1.4 · – · 9.3 · 1.7 · – K |
| Al–Si | **0 (9)** | 5 | 1/0/0/0 each (eutectic 850.1–853.3 K) | – |
| Al–Mg | 31 (31) | 10 | 4–7 calc.; 3–5 lit.; 0–4 exp. matches | 0.1–1.7 K |
| Al–Zr | 178 (182) | 8 | 12–16 calc.; 12–14 lit.; 8–13 exp.; 5–13 within 10 K | 0.7 (01Wan) – 12.7 (86Sau) K |
| Cu–Ni | 0 (2) | 4 | 0 (isomorphous, correct) | – |

- **Peritectic and eutectic temperatures.** The Al–Zr peritectic L + Al3Zr → (Al) comes out at 929.7–934.1 K in all
  8 assessments, and every one matches literature within 1.05 K. The Al–Mg eutectic L → (Al) + β comes out at
  718.9–728.5 K, and all 10 assessments match literature (only 93Zuo matches an experimental record, at −0.84 K).
- **`phase_at`, 9 points.** Over all assessments the 9 points gave 54 answers. Leaving out the dilute Al–Zr point
  (finding 5), 44 of 46 matched what we expected: FCC_A1 at Al–2Cu/800 K, θ AL2CU_C16 at Al–33Cu/700 K,
  FCC_A1+DIAMOND_A4 at Al–10Si/800 K, LIQUID at Al–12.6Si/900 K, FCC_A1 at Al–5Mg/700 K, AL3ZR_D023 at Al–25Zr/1000 K,
  and FCC_A1 then LIQUID for Cu–30Ni/1000 K and Cu–50Ni/1650 K. The two exceptions are AlCu-02Mie, which gives
  `BCC_A2` at Al–33Cu (finding 4), and AlCu-21Kro, which gives FCC_A1+θ at Al–2Cu/800 K. The second is right at the
  solvus, so it is plausible.
- **`list_tdb_files`, exact pair counts.** Al–Cu 5, Al–Si 6 (includes AlSi-24Zob-3g, which has no diagram), Al–Mg 11
  (includes 1 `manual`-tier file), Al–Zr 8 and Cu–Ni 4. All are `bundled` except that one. Files containing both
  elements, binary or higher: 24, 21, 24, 21 and 20.
- **`get_formation_enthalpy`, kJ/mol-atom.**
  - Al3Zr: 37 literature values (9 experimental, mean −46.7, median −48.4; 24 model; 4 DFT), plus 27 in other
    units. MP gives −47.01 and OQMD −47.08, both D0_23 on the hull.
  - Al2Cu: see the finding below.
  - Al3Mg2: nothing at x(Mg)=0.400. β is really Al140Mg89 at x=0.389, and the composition match tolerance is 2e-3.
- **`compare_to_dft`.** Al–Zr: 9 compounds, default subset n=45, MAE 5.61 (MP) and 5.60 (OQMD) kJ/mol-atom, mean
  residual (DFT − literature) +3.6. Al–Cu, Al–Si, Al–Mg and Cu–Ni return no compounds, because there are no accepted
  literature HM_FORM values at DFT compositions. The 11 Al–Mg formation records are all DFT end-member values.

### Problems and findings, with exact lines
1. **No accepted Al–Si invariants.** Al–Si has 13 literature records and none is accepted, even though there are 8
   records of the 850.15 K eutectic. With `source="literature"` the call fails:
   `Error executing tool get_invariant_reactions: no invariant data for AL-SI`. Cu–Ni fails the same way
   (`... no invariant data for CU-NI`). The cause is the data gate: those records have
   `{'code': 'state_phases_missing', 'detail': 'INVARIANT_TEMPERATURE without the phases of its state (reactions_in_quote:0)', 'effect': 'not_accepted', 'gate': 'R3'}`,
   or their phases are not mapped to a model (`('Liquid', None), ('fcc-Al', None), ('diamond', None)`). The cause is
   in orchid-data, not the server; `source="both"` returns the calculated invariants alone.
2. **The Al–Cu eutectic L → (Al) + θ never matches literature.** It is calculated at 820.6–821.7 K in all 4
   assessments that model θ. Literature record `ORC-FNCFSLFUOM` (820.7 K) maps `('AlCu-θ', None)` and carries
   `label_conflicts_composition: AlCu-θ printed x(CU)=0.318, formula 0.5`: the phase label "AlCu-θ" was parsed as
   the formula AlCu. Experimental record `ORC-NHZUNBHOEB` (823.15 K) has no phases (gate R3). This is the key invariant
   for Al–Cu alloys, so it is a data bug worth reporting to orchid-data.
3. **Matching depends on phase names.** It requires the exact model phase set, so AlCu-04Wit and AlCu-98Sau-LB match
   1 of 14 invariants each. Their names are AL4CU9_D82 and ALCU_ETA; the literature is mapped to GAMMA_D82 and
   ALCU_ETA_HT, as in 21Kro. A low match count can mean naming, not disagreement.
4. **The Cu-side assessment AlCu-02Mie is computed and served over the whole composition range** with
   `status: "ok"` and no warning. Its TDB has only `AL4CU9_GAMMA, BCC_A2, FCC_A1, HCP_A3, LIQUID`, with no θ or η, so
   `phase_at` at x(Cu)=0.33 and 700 K returns `["BCC_A2"]`. The diagram also has an FCC_A1+HCP_A3+LIQUID invariant
   at 881 K on the Al-rich side, which does not exist. Do not use it for Al-rich alloys.
5. **The stored grid is too coarse for dilute alloys** (dx = 0.01, dT = 10 K). x(Zr)=0.002 snaps to the pure-Al
   column. Questions about dilute solubility, such as Zr, Sc or Mn in Al, need pycalphad run on the TDB. At that
   point, 18Tam answers `AL3ZR_D023+FCC_A1` and the other seven assessments answer `FCC_A1`.
6. **The DFT "lowest" value for Al2Cu is not θ.** `dft_mp_lowest` −17.18 and `dft_oqmd_lowest` −16.88 kJ/mol-atom both
   come from a theoretical 3-atom Fm-3m (fluorite-type) entry. θ (I4/mcm) lies 12.5 meV/atom above the MP hull, at
   −15.97 kJ/mol-atom. This is the known zero-kelvin ordering problem (doi:10.1103/PhysRevLett.86.5518, "Entropically
   favored ordering: the metallurgy of Al2Cu revisited"). ORCHID has no literature HM_FORM for Al2Cu, even with
   `accepted_only=false`.
7. **The README size table is out of date.** For CU-ZR, measured payload versus README "after":
   - `get_system_data`: 83,240 B vs 23,234 (3.6×)
   - `get_invariant_reactions`: 149,078 vs 83,218 (1.8×)
   - `get_formation_enthalpy("CuZr2")`: 2.0×
   - `compare_to_dft`: 1.4×
   - the other three calls: within 10 %

   Al–Zr defaults are larger still (`compare_to_dft` 230 KB on the SDK), which is costly for LLM context. Details
   are in `data/mcp_readme_sizes_*.csv`.
8. **The fallback server sends twice the bytes.** It returns both `content[0].text` and an identical
   `structuredContent`, so its messages are about 2× the SDK's. The payloads themselves are identical.
9. **Error formats differ between back ends.** For the same bad assessment, the SDK returns
   `Error executing tool get_phase_diagram: assessment 'no-such-assessment' not found for AL-CU; available: ['AlCu-02Mie.tdb', ...]`
   and also writes it to stderr as `Tool 'get_phase_diagram' failed: ...`. The fallback returns
   `{"error": "assessment 'no-such-assessment' not found ..."}`.
10. **Minor points.**
    - In plain mode, `orchid-mcp --transport http` exits 2 with `streamable HTTP needs the MCP SDK: pip install mcp`,
      as documented.
    - The `[test]` extra leaves pytest unpinned (we got 9.2.0), while CI pins `pytest==9.1.1` on Python 3.13. We used
      3.12.3 with no problems.

**Files.**
- Scripts: `scripts/orchid_mcp_drive.py`, `scripts/orchid_mcp_probe.py`, `scripts/orchid_mcp_readme_sizes.py`.
- Logs: `logs/orchid-mcp-{install,tests-plain,tests-mcp,stdio-sdk,stdio-fallback,probe,cli,readme-sizes}.log`.
- Data:
  - `data/mcp_{alcu,alsi,almg,alzr,cuni}_responses.json`: trimmed responses, with citation author strings replaced
    by a pointer to the DOI.
  - `data/mcp_misc_responses.json`
  - `data/mcp_summary_{sdk,fallback}.json`
  - `data/mcp_call_timings_{sdk,fallback}.csv`
  - `data/mcp_probe_accepted_vs_all.json`
  - `data/mcp_invariants_sgte_vs_literature.csv`: 247 calculated invariants with their best literature and
    experimental matches.
  - `data/mcp_readme_sizes_{sdk,fallback}.csv`

| orchid-mcp | PASS (uv, py3.12; plain 7 pkgs and `[mcp]` 35 pkgs, <1 s each) | pytest in 2 venvs × 2 modes (52/52 with data and SDK); stdio JSON-RPC on SDK and fallback, 41 tool calls × 5 systems | PASS | identical payloads on both back ends; Al–Si has 0 accepted invariants; the Al–Cu θ eutectic is unmatched (label-parse gate); AlCu-02Mie served Al-rich without warning; README size table stale |
