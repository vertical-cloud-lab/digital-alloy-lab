| Element | Edison | Decision | Reason | TCCU7 tier |
| --- | --- | --- | --- | --- |
| [Cu](phase1/el-01-Cu.md) | LIMIT | balance | Balance, at least 65 wt%. The calculated liquidus (at most 1,250 C) is the binding limit: Cu-Ni above about 33 Ni melts too high to atomize. The 60 wt% floor Edison offered is not used in the first campaign. | matrix |
| [Ni](phase1/el-02-Ni.md) | INCLUDE | search | Main film-former in Cu-Ni and a kappa former in NAB; the strongest route to C71500-class resistance. Capped by the liquidus near the atomizer limit (70-30 melts to about 1,240 C). Nickel burden is an objective, not a bound. | 1 |
| [Al](phase1/el-03-Al.md) | INCLUDE | search | Defines the aluminum bronze branch and the Cu-Ni-Al region between the families. The upper range keeps the retained-beta boundary inside the space, so the process-aware CALPHAD screen (H3) can be tested on it, and it includes the duplex alpha+beta bronzes, which crack less as weld filler than single-phase ones but risk selective attack of beta. | 1 |
| [Fe](phase1/el-04-Fe.md) | INCLUDE | search | Needed for the Cu-Ni film and for kappa phases in NAB. Bounded by family rules: kept in solid solution in Cu-Ni (at most 2.3), Ni at least equal to Fe in NAB. | 1 |
| [Mn](phase1/el-05-Mn.md) | INCLUDE | search | Deoxidizer and partial nickel substitute (C71640, MARINEL). Upper bound set by evaporation and oxidation in melting and DED; Mn-Al bronze (11-14 Mn) is left out for that reason. | 1 |
| [Cr](phase1/el-06-Cr.md) | INCLUDE | search | Raises erosion-corrosion resistance of Cu-Ni (C72200 critical velocity about 3 times that of C71500), but higher-Cr Cu-Ni had worse crevice attack in still water. Cu-Ni and Cu-Ni-Al only. | 1 |
| [Sn](phase1/el-07-Sn.md) | INCLUDE | optional | An impurity in the target alloys (C63000 at most 0.20; EN Cu-Ni grades at most 0.03-0.05). About 1 wt% refined cast NAB grains and raised strength (Poojary et al. 2023), but the only chloride series is a porous sintered shape-memory alloy, and Sn widens the freezing range. A Year-2 option for NAB only. | 1 |
| [Zn](phase1/el-08-Zn.md) | LIMIT | limit | Boils at 907 C (evaporation in melting and DED), dezincifies in seawater; Cu-Ni welding grades limit it to 0.5. | 1 |
| [Si](phase1/el-09-Si.md) | INCLUDE | search | Deoxidizer, and with Nb a strengthener of cast 70-30 Cu-Ni (Si up to 0.5 in C96400, with Nb at least about twice Si). Silicides and weld cracking above that; C95800 allows only 0.10, so Si is a Cu-Ni variable. Silicon bronze levels (about 3) are not a seawater-repair target. | 1 |
| [Nb](phase1/el-10-Nb.md) | INCLUDE | search | Added to cast Cu-Ni (C96400, 0.5-1.5) for weldability and present in MARINEL (0.6-0.9). Must be added as a master alloy (Nb melts at 2,477 C). Cu-Ni branch only. | 2 |
| [Be](phase1/el-11-Be.md) | LIMIT | exclude | Beryllium powder and fume are a severe inhalation hazard (OSHA 2017 standard); not compatible with in-house atomization and laser deposition. | 3 |
| [Co](phase1/el-12-Co.md) | INCLUDE | exclude | Counted with Ni in Cu-Ni specifications; costlier and scarcer than Ni, with no seawater benefit shown over Ni and Fe. | 1 |
| [Ti](phase1/el-13-Ti.md) | INCLUDE | search | Deoxidizer in the ERCuNi welding filler (0.20-0.50), the closest analogue of a laser-deposited Cu-Ni. Oxide and nitride inclusions and crucible attack above that. In NAB only up to 0.1 is supported (0.1 Ti lowered the corrosion current of wire-arc NAB by about 16%). | 2 |
| [Zr](phase1/el-14-Zr.md) | INCLUDE | optional | Grain refiner (C15000; cast bronzes from about 0.01), but about half is lost on melting, the excess above its solubility (about 0.1-0.2) goes to grain boundaries, and Cu-Ni-Zr is not assessed in TCCU7. A Year-2 option. | 2 |
| [Hf](phase1/el-15-Hf.md) | EXCLUDE | exclude | Works only after aging, costly, reacts with alumina, not in TCCU7. | 4 |
| [Mg](phase1/el-16-Mg.md) | LIMIT | limit | Deoxidizer residual only; boils at about 1,090 C, below the melt temperature, and attacks alumina; harmful to NAB hot ductility. | 2 |
| [Ag](phase1/el-17-Ag.md) | INCLUDE | exclude | Edison's 'include' rested on one Ag-nanoparticle study in a shape-memory Cu-Al-Ni alloy, read through a review. Residual Ag is counted with Cu, as the specifications do. | 1 |
| [V](phase1/el-18-V.md) | EXCLUDE | exclude | No use or benefit found in seawater copper alloys; not in TCCU7. Watch for pickup from a Ti-6Al-4V sonotrode. | 4 |
| [B](phase1/el-19-B.md) | INCLUDE | optional | Grain refiner at 0.002-0.02 in cast bronzes, but borides, a Ni-B eutectic (about 1,090 C) below the Cu-30Ni solidus, and dosing at 0.5 kg scale make it a later-round option. No Cu-B-X ternary in TCCU7. | 3 |
| [As](phase1/el-20-As.md) | LIMIT | limit | Dezincification inhibitor in brasses (0.02-0.06), not needed without Zn; toxic and volatile. | 3 |
| [Sb](phase1/el-21-Sb.md) | LIMIT | limit | Dezincification inhibitor in brasses; hot shortness; not in TCCU7. | 4 |
| [P](phase1/el-22-P.md) | LIMIT | limit | Deoxidizer residual; promotes hot cracking in Cu-Ni welds (welding grades: at most 0.02). | 2 |
| [Pb](phase1/el-23-Pb.md) | LIMIT | limit | Insoluble, forms low-melting films (hot cracking); toxic. Welding grades: at most 0.02. | 2 |
| [Bi](phase1/el-24-Bi.md) | LIMIT | limit | Grain-boundary films embrittle copper at ppm levels. | 3 |
| [Se](phase1/el-25-Se.md) | LIMIT | limit | Free-machining addition; hot shortness; oxygen-free copper carries only ppm. | 3 |
| [Te](phase1/el-26-Te.md) | LIMIT | limit | Free-machining addition; hot shortness; not in TCCU7. | 4 |
| [S](phase1/el-27-S.md) | LIMIT | limit | Low-melting sulfide films (hot cracking, porosity); ERCuNi allows at most 0.01. | 1 |
| [Cd](phase1/el-28-Cd.md) | LIMIT | limit | Toxic (RoHS, OSHA) and boils at 767 C; never added. | 3 |
| [O](phase1/el-29-O.md) | LIMIT | limit | Oxide films, inclusions and steam porosity; ultrasonically atomized NAB powder carried 0.013. Measured per lot by inert-gas fusion. | 2 |
| [H](phase1/el-30-H.md) | LIMIT | limit | Porosity and steam embrittlement with oxygen; controlled by dry powder and argon. | 4 |
| [N](phase1/el-31-N.md) | LIMIT | limit | Porosity in Cu-Ni welds and nitrides with Ti and Zr; controlled by shielding. | 4 |
| [C](phase1/el-32-C.md) | LIMIT | limit | Picked up from graphite crucibles or carbon-fiber plates; welding grades allow 0.05. Edison's 0.005 had no data behind it. | 3 |
| [Mo](phase1/el-33-Mo.md) | LIMIT | limit | Nearly immiscible with Cu and no seawater benefit in Cu alloys, so never added; capped because a TZM (Mo alloy) sonotrode can add it. | 2 |
| [W](phase1/el-34-W.md) | EXCLUDE | exclude | Immiscible with Cu; melts at 3,422 C. | 4 |
| [Ta](phase1/el-35-Ta.md) | EXCLUDE | exclude | Immiscible; melts at 3,017 C; nanocrystalline Cu-Ta needs mechanical alloying. | 3 |
| [Ga](phase1/el-36-Ga.md) | LIMIT | exclude | No seawater use found; critical mineral; not in TCCU7. | 4 |
| [Ge](phase1/el-37-Ge.md) | INCLUDE | exclude | Edison's 'include' rested on one heat-treated powder-metallurgy NAB sample whose Mn, Fe and Ni also changed; Ge costs about $1,000-4,000/kg, is a critical mineral under export controls, and Cu-Al-Ge and Cu-Ni-Ge are not in TCCU7. | 3 |
| [In](phase1/el-38-In.md) | LIMIT | exclude | No benefit found; critical mineral; not in TCCU7. | 4 |
| [Li](phase1/el-39-Li.md) | LIMIT | exclude | Deoxidizer only; volatile and reactive with crucibles; not in TCCU7. | 4 |
| [Ca](phase1/el-40-Ca.md) | EXCLUDE | exclude | Deoxidizer only; no use in Cu-Ni or bronzes found. | 3 |
| [Sr](phase1/el-41-Sr.md) | EXCLUDE | exclude | No use in copper alloys found (stands in for Sr and Ba). | 4 |
| [Sc](phase1/el-42-Sc.md) | EXCLUDE | exclude | No seawater benefit; very costly; not in TCCU7. | 4 |
| [Y](phase1/el-43-Y.md) | INCLUDE | exclude | One cast 90-10 abstract only; not in TCCU7. Ce or La would take the single rare-earth slot. | 4 |
| [La](phase1/el-44-La.md) | INCLUDE | optional | Shares one rare-earth variable with Ce (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 La resisted 3.5% NaCl better than Cu-10Ni, and better than with Ce (Du et al. 2025); Cu-La-Ni is assessed in TCCU7. | 2 |
| [Ce](phase1/el-45-Ce.md) | LIMIT | optional | Shares one rare-earth variable with La (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 Ce resisted 3.5% NaCl better than Cu-10Ni (Du et al. 2025); Edison's 0.04 cap came from mischmetal retention in brass. Cu-Ni-Ce and Al-Ce-Cu are assessed in TCCU7. | 2 |
| [Pr](phase1/el-46-Pr.md) | EXCLUDE | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Nd](phase1/el-47-Nd.md) | LIMIT | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Er](phase1/el-48-Er.md) | EXCLUDE | exclude | No data in copper alloys; not in TCCU7. | 4 |
| [Gd](phase1/el-49-Gd.md) | EXCLUDE | exclude | No data in seawater copper alloys; not in TCCU7 (stands in for the heavy lanthanides). | 4 |
| [Pd](phase1/el-50-Pd.md) | EXCLUDE | exclude | Cathodic modification works for titanium and stainless steels, not shown for copper alloys; thousands of dollars per kg (stands in for the platinum group). | 4 |
