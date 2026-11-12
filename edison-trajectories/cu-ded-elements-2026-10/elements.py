"""The 50 elements queried one by one for the copper/DED search space (PR #117).

The aluminum/LPBF palette was chosen in two steps: elements were short-listed by
CALPHAD database coverage and supply risk (../edison-search-space-reframing.md),
then each palette element got its own Edison query for a conservative and a
non-conservative bound (branch copilot/determine-bounds-for-elements,
edison-trajectories/element-bounds/). Here the per-element queries come first and
are wider: 50 elements, each asked whether it belongs in the space at all, and
if so with what bounds. Cu is one of the 50, as Al was one of the 16.

How the 50 were picked (Cu plus 49 of the 117 other elements):
- excluded without a query (68): noble gases; halogens; elements with no stable
  isotope (Tc, Pm, Po and every element from Fr up, including Th and U); the
  heavy alkali metals Na, K, Rb, Cs and the alkaline earth Ba; the platinum
  group metals other than Pd, plus Re and Au; Hg and Tl; and the lanthanides
  other than La, Ce, Pr, Nd, Gd and Er. Each class has no use in seawater
  copper alloys, or costs thousands of dollars per kilogram;
- queried (50): every element that appears in a commercial copper alloy, a
  copper alloy specification (as an addition or as an impurity limit), a
  copper welding filler, a copper deoxidizing practice, or the atomizer's
  crucible and sonotrode materials; plus one representative of each excluded
  class that is not obviously irrelevant (Pd for the platinum group, Sr for the
  heavy alkaline earths, Gd for the heavy lanthanides), so that the exclusion
  of the class rests on an answer rather than an assumption.

Each entry: group, and a hint that names the alloys and specifications in which
the element appears, so that Edison starts from the right literature.
"""

ELEMENTS = {
    # --- matrix -------------------------------------------------------------
    "Cu": ("matrix", "Copper is the balance element. Navy seawater alloys span "
           "about 65-70 wt% Cu (70-30 Cu-Ni, C71500), 86-89 wt% (90-10, "
           "C70600), 78-82 wt% (NAB, C95800) and 71-78 wt% (Mn-Al bronze, "
           "C95700)."),
    # --- major additions in Navy seawater copper alloys ----------------------
    "Ni": ("major seawater addition", "C70600 (9-11 Ni), C71500 (29-33 Ni), "
           "C71640 (Cu-30Ni-2Fe-2Mn), C72200 (15-18 Ni, Cr), NAB C95800 and "
           "C63000 (4-5.5 Ni), MARINEL (Cu-19Ni-4.6Mn-1.9Al). Nickel raises the "
           "liquidus (70-30 melts at about 1,171-1,238 C) and is a US critical "
           "mineral."),
    "Al": ("major seawater addition", "Aluminum bronzes: C95800 (8.5-9.5 Al), "
           "C63000 (9-11 Al), C95700 Mn-Al bronze (7-8.5 Al); aluminum brass "
           "C68700 (1.8-2.5 Al); Cu-Ni-Al alloys (e.g. the Hiduron series, "
           "MARINEL with about 1.9 Al, cast Cu-7Ni-3Al). Above about 9.4 wt% Al, beta and "
           "martensitic beta-prime are retained on fast cooling."),
    "Fe": ("major seawater addition", "Cu-Ni: 1.0-1.8 Fe in C70600, 0.4-1.0 in "
           "C71500, 1.7-2.3 in C71640; NAB: about 2-5 Fe (kappa phases). Fe controls "
           "the protective film and erosion-corrosion resistance of Cu-Ni, but "
           "Fe out of solid solution harms it. Dilution from steel substrates "
           "adds Fe."),
    "Mn": ("major seawater addition", "Cu-Ni: up to 1 Mn (deoxidizer), C71640 "
           "1.5-2.5 Mn; NAB 0.8-3.5 Mn; Mn-Al bronze C95700 11-14 Mn; MARINEL "
           "4.6 Mn. Mn has a high vapor pressure and is lost in laser "
           "processing; it is a candidate nickel substitute."),
    "Cr": ("major seawater addition", "C72200 (Cu-16Ni-0.5Cr), cast CuNi30Cr2 "
           "(e.g. IN-768 type, up to about 2-3 Cr), Cu-Cr precipitation alloys "
           "C18200 (about 1 Cr). Solubility of Cr in Cu is small (under 1 wt% "
           "at the eutectic). Reported to raise erosion-corrosion resistance of "
           "Cu-Ni but to pit in still seawater."),
    "Sn": ("major seawater addition", "Tin bronzes and gunmetals (C90300, "
           "C90500: 8-10 Sn), phosphor bronze C51000 (5 Sn), Cu-Ni-Sn spinodal "
           "C72900 (Cu-15Ni-8Sn), admiralty brass (1 Sn). Wide freezing range "
           "and Sn-rich delta phase."),
    "Zn": ("major seawater addition", "Brasses: naval brass C46400 (about 39 "
           "Zn), aluminum brass C68700 (about 21 Zn), admiralty brass C44300 "
           "(28 Zn); Zn is limited to 0.5-1 wt% in Cu-Ni specifications. "
           "Dezincification in seawater; Zn boils at 907 C, so lasers "
           "evaporate it."),
    "Si": ("major seawater addition", "Silicon bronze C65500 (2.8-3.8 Si), "
           "aluminum-silicon bronze C64200 (1.5-2.2 Si), Cu-Ni-Si Corson alloys "
           "(C70250, Ni2Si precipitates), silicon brass C87500; Si is also a "
           "deoxidizer and a weld-cracking concern in Cu-Ni."),
    "Nb": ("major seawater addition", "Cast Cu-Ni: C96200 (90-10) and C96400 "
           "(70-30) contain Nb (up to about 1-1.5 wt%), added for weldability; Cu-Cr-Nb "
           "(GRCop, Cr2Nb). Nb is nearly insoluble in Cu and is a US critical "
           "mineral."),
    # --- precipitation, grain-refining and strengthening additions ----------
    "Be": ("strengthening addition", "Beryllium coppers C17200 (1.8-2.0 Be), "
           "C17510 (0.2-0.6 Be with 1.4-2.2 Ni), C17500 (Co-Be); Navy uses "
           "include undersea housings and non-sparking tools. Be powder and "
           "fume are toxic (OSHA 2017 beryllium standard)."),
    "Co": ("strengthening addition", "C17500 (2.4-2.7 Co with Be), Cu-Ni-Co-Si "
           "(C70350), Co in some Cu-Ni and Al bronze variants. Cobalt is a US "
           "critical mineral; could it replace part of the nickel?"),
    "Ti": ("strengthening addition", "Cu-Ti C19900 (about 3 Ti); ERCuNi welding "
           "filler (AWS A5.7) carries 0.2-0.5 Ti as a deoxidizer; 0.1 wt% Ti in "
           "wire-arc NAB lowered corrosion current (Zhang et al. 2026). Ti "
           "attacks ceramic crucibles and forms intermetallics with Ni and "
           "Cu."),
    "Zr": ("strengthening addition", "Cu-Zr C15000 (0.1-0.2 Zr), CuCrZr C18150 "
           "(0.05-0.25 Zr); grain refinement of cast aluminum bronze; Zr can "
           "be picked up from zirconia crucibles."),
    "Hf": ("strengthening addition", "Cu-Hf precipitation alloys, studied as "
           "an analogue of Cu-Zr; Hf is costly and a US critical mineral."),
    "Mg": ("strengthening addition", "Deoxidizer for copper; Cu-Mg conductor "
           "alloys (about 0.1-0.7 Mg); Mg in some aluminum bronzes. High vapor "
           "pressure; MgO crucibles."),
    "Ag": ("strengthening addition", "Silver-bearing coppers (C10700, C11300 "
           "series, 0.03-0.1 Ag), Cu-Ag high-strength conductors (several wt% "
           "Ag). Costly; silver was added to the US critical minerals list in "
           "2025."),
    "V": ("strengthening addition", "Vanadium is rarely used in copper alloys; "
          "check for any use in aluminum bronzes, Cu-Ni, or grain refinement, "
          "and for its solubility in Cu."),
    "B": ("strengthening addition", "Boron-deoxidized copper; boron as a grain "
          "refiner in copper and aluminum bronze castings; borides with Ni, Fe, "
          "Cr; boron nitride crucibles and coatings."),
    # --- dezincification inhibitors and deoxidizers ---------------------------
    "As": ("dealloying inhibitor", "Arsenical admiralty brass C44300 and "
           "aluminum brass C68700 (0.02-0.06 As) to inhibit dezincification; "
           "As is limited in Cu-Ni. Toxic; volatile."),
    "Sb": ("dealloying inhibitor", "Inhibited admiralty brass C44400 (0.02-0.10 "
           "Sb); impurity limit in Cu-Ni and bronzes; hot shortness."),
    "P": ("dealloying inhibitor", "Phosphorus-deoxidized copper C12200 "
          "(0.015-0.040 P), phosphor bronzes (0.03-0.35 P), inhibited admiralty "
          "C44500; impurity limit in Cu-Ni (about 0.02 wt% for weldable "
          "grades) because P promotes hot cracking in Cu-Ni welds."),
    # --- free-machining and low-melting additions, usually impurities --------
    "Pb": ("impurity / free-machining", "Leaded bronzes and brasses; Cu-Ni "
           "specifications limit Pb to about 0.02-0.05 wt% for welding; hot "
           "cracking; toxic, restricted (RoHS)."),
    "Bi": ("impurity / free-machining", "Lead-free free-machining brasses and "
           "bronzes (e.g. C89833 type); bismuth films on grain boundaries embrittle "
           "copper at ppm levels; impurity limit."),
    "Se": ("impurity / free-machining", "Free-machining with Bi (SeBiLOY "
           "C89510); impurity limit in Cu-Ni and copper."),
    "Te": ("impurity / free-machining", "Tellurium copper C14500 (0.4-0.7 Te); "
           "impurity limit in Cu-Ni; hot shortness."),
    "S": ("impurity / free-machining", "Sulfur copper C14700; Cu-Ni "
          "specifications limit S to about 0.02 wt% for welding; hot cracking. "
          "(Sulfide in polluted seawater is a separate issue: answer for S in "
          "the alloy, and mention the polluted-water effect only briefly.)"),
    "Cd": ("impurity / free-machining", "Cadmium copper C16200 (0.7-1.2 Cd); "
           "toxic, restricted (RoHS, OSHA); boils at 767 C."),
    # --- interstitials and gases in powder and deposits ----------------------
    "O": ("interstitial / gas", "Oxygen in copper powder and deposits: oxygen-"
          "free vs tough-pitch copper, Cu2O, steam porosity with hydrogen, "
          "oxide films on powder; no literature-certified oxygen limit for "
          "copper DED powder was found earlier. Answer as an impurity limit in "
          "ppm for powder and deposit, and say which deoxidizers (Al, Mn, Ti, "
          "Si, P, B, Mg, Li) control it."),
    "H": ("interstitial / gas", "Hydrogen embrittlement (steam reaction with "
          "Cu2O) and porosity in Cu-Ni welds; moisture on powder. Answer as an "
          "impurity limit (ppm) and as a process control."),
    "N": ("interstitial / gas", "Nitrogen porosity in Cu-Ni welds (from "
          "shielding or air), nitrogen solubility rising with Ni content; Ti "
          "and Al as nitride formers. Answer as an impurity limit and a "
          "process control."),
    "C": ("interstitial / gas", "C71500 limits C to 0.05 wt%; carbon is picked "
          "up from graphite crucibles or carbon-fiber sonotrodes; carbon "
          "solubility in Cu is tiny but higher in Ni-rich melts; graphite "
          "flakes and carbides with Cr, Ti, Nb. Answer as an impurity limit."),
    # --- refractory metals nearly immiscible with Cu -------------------------
    "Mo": ("refractory, immiscible", "Mo raises the pitting resistance of "
           "stainless steels and nickel alloys; does it do anything in Cu-Ni "
           "or aluminum bronze? Cu-Mo is nearly immiscible. TZM (Mo alloy) is "
           "a candidate sonotrode material, so Mo pickup matters."),
    "W": ("refractory, immiscible", "Cu-W pseudo-alloys and composites; W is "
          "nearly insoluble in liquid and solid Cu and melts at 3,422 C."),
    "Ta": ("refractory, immiscible", "Nanocrystalline Cu-Ta (e.g. Cu-3Ta, "
           "Army Research Laboratory) made by mechanical alloying; any "
           "corrosion data in NaCl or seawater; Ta melts at 3,017 C."),
    # --- p-block solid-solution elements ------------------------------------
    "Ga": ("solid solution", "Cu-Ga alpha solid solution (wide); low melting "
           "point; gallium is a US critical mineral; any corrosion data for "
           "Cu-Ga or Cu-Ni-Ga."),
    "Ge": ("solid solution", "Cu-Ge alpha solid solution; germanium makes "
           "silver alloys tarnish resistant; critical mineral; any corrosion "
           "data in chloride."),
    "In": ("solid solution", "Cu-In and Cu-Ni-In; indium is a US critical "
           "mineral; any corrosion or dealloying data in chloride."),
    # --- alkali and alkaline earth deoxidizers -------------------------------
    "Li": ("deoxidizer", "Lithium as a deoxidizer for copper melts; any Cu-Li "
           "alloy use; volatility and reactivity with crucibles."),
    "Ca": ("deoxidizer", "Calcium (and CaB6) as deoxidizer and desulfurizer in "
           "copper; any use in Cu-Ni or bronzes."),
    "Sr": ("deoxidizer", "Representative of the heavier alkaline earths "
           "(Sr, Ba): any use as a modifier, grain refiner or deoxidizer in "
           "copper alloys."),
    # --- rare earths and Sc/Y -----------------------------------------------
    "Sc": ("rare earth", "Cu-Sc precipitation and grain refinement; scandium "
           "cost and supply."),
    "Y": ("rare earth", "Yttrium as an oxygen getter and grain refiner in "
          "copper and Cu-Ni; yttria crucibles and coatings."),
    "La": ("rare earth", "Lanthanum (often with Ce as mischmetal) added to "
           "B10/B30 Cu-Ni and bronzes, claimed to refine grains, scavenge S and "
           "O, and improve the corrosion film."),
    "Ce": ("rare earth", "Cerium additions to 90-10 and 70-30 Cu-Ni and to "
           "aluminum bronze (mostly cast or wrought studies, often Chinese "
           "literature): corrosion and film effects, amounts used."),
    "Pr": ("rare earth", "Praseodymium additions to copper alloys, if any."),
    "Nd": ("rare earth", "Neodymium additions to copper alloys, if any."),
    "Er": ("rare earth", "Erbium additions to copper alloys, if any."),
    "Gd": ("rare earth", "Representative of the heavy lanthanides (Gd through "
           "Lu): any use in copper alloys."),
    # --- platinum group ------------------------------------------------------
    "Pd": ("platinum group", "Representative of the platinum group metals: "
           "small Pd or Ru additions make titanium and stainless steels "
           "passivate (cathodic modification); is there any analogue for "
           "copper alloys in seawater, and any Cu-Pd corrosion data?"),
}

assert len(ELEMENTS) == 50, len(ELEMENTS)
