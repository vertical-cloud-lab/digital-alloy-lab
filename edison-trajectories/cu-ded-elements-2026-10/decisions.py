"""Final decision for each of the 50 queried elements, with the reason.

Edison's own verdict is in verdicts.md (parsed from phase1/). The decision here
also weighs the joint answer (phase1/joint-shortlist.md), the subagent checks
(checks.md), the TCCU7 coverage (tccu7_coverage.md) and the ANALYSIS
syntheses (phase2/, phase3/). "search" = in the palette; "optional" = held for
later rounds; "limit" = impurity limit only; "exclude" = not added, no limit
needed beyond normal feedstock certificates.
"""

DECISIONS = {
    "Cu": ("balance", "Balance, at least 65 wt%. The calculated liquidus (at most 1,250 C) is the binding limit: Cu-Ni above about 33 Ni melts too high to atomize. The 60 wt% floor Edison offered is not used in the first campaign."),
    "Ni": ("search", "Main film-former in Cu-Ni and a kappa former in NAB; the strongest route to C71500-class resistance. Capped by the liquidus near the atomizer limit (70-30 melts to about 1,240 C). Nickel burden is an objective, not a bound."),
    "Al": ("search", "Defines the aluminum bronze branch and the Cu-Ni-Al region between the families. The upper range keeps the retained-beta boundary inside the space, so the process-aware CALPHAD screen (H3) can be tested on it, and it includes the duplex alpha+beta bronzes, which crack less as weld filler than single-phase ones but risk selective attack of beta."),
    "Fe": ("search", "Needed for the Cu-Ni film and for kappa phases in NAB. Bounded by family rules: kept in solid solution in Cu-Ni (at most 2.3), Ni at least equal to Fe in NAB."),
    "Mn": ("search", "Deoxidizer and partial nickel substitute (C71640, MARINEL). Upper bound set by evaporation and oxidation in melting and DED; Mn-Al bronze (11-14 Mn) is left out for that reason."),
    "Cr": ("search", "Raises erosion-corrosion resistance of Cu-Ni (C72200 critical velocity about 3 times that of C71500), but higher-Cr Cu-Ni had worse crevice attack in still water. Cu-Ni and Cu-Ni-Al only."),
    "Sn": ("optional", "An impurity in the target alloys (C63000 at most 0.20; EN Cu-Ni grades at most 0.03-0.05). About 1 wt% refined cast NAB grains and raised strength (Poojary et al. 2023), but the only chloride series is a porous sintered shape-memory alloy, and Sn widens the freezing range. A Year-2 option for NAB only."),
    "Zn": ("limit", "Boils at 907 C (evaporation in melting and DED), dezincifies in seawater; Cu-Ni welding grades limit it to 0.5."),
    "Si": ("search", "Deoxidizer, and with Nb a strengthener of cast 70-30 Cu-Ni (Si up to 0.5 in C96400, with Nb at least about twice Si). Silicides and weld cracking above that; C95800 allows only 0.10, so Si is a Cu-Ni variable. Silicon bronze levels (about 3) are not a seawater-repair target."),
    "Nb": ("search", "Added to cast Cu-Ni (C96400, 0.5-1.5) for weldability and present in MARINEL (0.6-0.9). Must be added as a master alloy (Nb melts at 2,477 C). Cu-Ni branch only."),
    "Be": ("exclude", "Beryllium powder and fume are a severe inhalation hazard (OSHA 2017 standard); not compatible with in-house atomization and laser deposition."),
    "Co": ("exclude", "Counted with Ni in Cu-Ni specifications; costlier and scarcer than Ni, with no seawater benefit shown over Ni and Fe."),
    "Ti": ("search", "Deoxidizer in the ERCuNi welding filler (0.20-0.50), the closest analogue of a laser-deposited Cu-Ni. Oxide and nitride inclusions and crucible attack above that. In NAB only up to 0.1 is supported (0.1 Ti lowered the corrosion current of wire-arc NAB by about 16%)."),
    "Zr": ("optional", "Grain refiner (C15000; cast bronzes from about 0.01), but about half is lost on melting, the excess above its solubility (about 0.1-0.2) goes to grain boundaries, and Cu-Ni-Zr is not assessed in TCCU7. A Year-2 option."),
    "Hf": ("exclude", "Works only after aging, costly, reacts with alumina, not in TCCU7."),
    "Mg": ("limit", "Deoxidizer residual only; boils at about 1,090 C, below the melt temperature, and attacks alumina; harmful to NAB hot ductility."),
    "Ag": ("exclude", "Edison's 'include' rested on one Ag-nanoparticle study in a shape-memory Cu-Al-Ni alloy, read through a review. Residual Ag is counted with Cu, as the specifications do."),
    "V": ("exclude", "No use or benefit found in seawater copper alloys; not in TCCU7. Watch for pickup from a Ti-6Al-4V sonotrode."),
    "B": ("optional", "Grain refiner at 0.002-0.02 in cast bronzes, but borides, a Ni-B eutectic (about 1,090 C) below the Cu-30Ni solidus, and dosing at 0.5 kg scale make it a later-round option. No Cu-B-X ternary in TCCU7."),
    "As": ("limit", "Dezincification inhibitor in brasses (0.02-0.06), not needed without Zn; toxic and volatile."),
    "Sb": ("limit", "Dezincification inhibitor in brasses; hot shortness; not in TCCU7."),
    "P": ("limit", "Deoxidizer residual; promotes hot cracking in Cu-Ni welds (welding grades: at most 0.02)."),
    "Pb": ("limit", "Insoluble, forms low-melting films (hot cracking); toxic. Welding grades: at most 0.02."),
    "Bi": ("limit", "Grain-boundary films embrittle copper at ppm levels."),
    "Se": ("limit", "Free-machining addition; hot shortness; oxygen-free copper carries only ppm."),
    "Te": ("limit", "Free-machining addition; hot shortness; not in TCCU7."),
    "S": ("limit", "Low-melting sulfide films (hot cracking, porosity); ERCuNi allows at most 0.01."),
    "Cd": ("limit", "Toxic (RoHS, OSHA) and boils at 767 C; never added."),
    "O": ("limit", "Oxide films, inclusions and steam porosity; ultrasonically atomized NAB powder carried 0.013. Measured per lot by inert-gas fusion."),
    "H": ("limit", "Porosity and steam embrittlement with oxygen; controlled by dry powder and argon."),
    "N": ("limit", "Porosity in Cu-Ni welds and nitrides with Ti and Zr; controlled by shielding."),
    "C": ("limit", "Picked up from graphite crucibles or carbon-fiber plates; welding grades allow 0.05. Edison's 0.005 had no data behind it."),
    "Mo": ("limit", "Nearly immiscible with Cu and no seawater benefit in Cu alloys, so never added; capped because a TZM (Mo alloy) sonotrode can add it."),
    "W": ("exclude", "Immiscible with Cu; melts at 3,422 C."),
    "Ta": ("exclude", "Immiscible; melts at 3,017 C; nanocrystalline Cu-Ta needs mechanical alloying."),
    "Ga": ("exclude", "No seawater use found; critical mineral; not in TCCU7."),
    "Ge": ("exclude", "Edison's 'include' rested on one heat-treated powder-metallurgy NAB sample whose Mn, Fe and Ni also changed; Ge costs about $1,000-4,000/kg, is a critical mineral under export controls, and Cu-Al-Ge and Cu-Ni-Ge are not in TCCU7."),
    "In": ("exclude", "No benefit found; critical mineral; not in TCCU7."),
    "Li": ("exclude", "Deoxidizer only; volatile and reactive with crucibles; not in TCCU7."),
    "Ca": ("exclude", "Deoxidizer only; no use in Cu-Ni or bronzes found."),
    "Sr": ("exclude", "No use in copper alloys found (stands in for Sr and Ba)."),
    "Sc": ("exclude", "No seawater benefit; very costly; not in TCCU7."),
    "Y": ("exclude", "One cast 90-10 abstract only; not in TCCU7. Ce or La would take the single rare-earth slot."),
    "La": ("optional", "Shares one rare-earth variable with Ce (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 La resisted 3.5% NaCl better than Cu-10Ni, and better than with Ce (Du et al. 2025); Cu-La-Ni is assessed in TCCU7."),
    "Ce": ("optional", "Shares one rare-earth variable with La (0-0.1 retained, Cu-Ni, Year 2). B10 with 0.1 Ce resisted 3.5% NaCl better than Cu-10Ni (Du et al. 2025); Edison's 0.04 cap came from mischmetal retention in brass. Cu-Ni-Ce and Al-Ce-Cu are assessed in TCCU7."),
    "Pr": ("exclude", "No data in copper alloys; not in TCCU7."),
    "Nd": ("exclude", "No data in copper alloys; not in TCCU7."),
    "Er": ("exclude", "No data in copper alloys; not in TCCU7."),
    "Gd": ("exclude", "No data in seawater copper alloys; not in TCCU7 (stands in for the heavy lanthanides)."),
    "Pd": ("exclude", "Cathodic modification works for titanium and stainless steels, not shown for copper alloys; thousands of dollars per kg (stands in for the platinum group)."),
}

assert len(DECISIONS) == 50, len(DECISIONS)
