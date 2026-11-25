You are reviewing a physics-based "truth" for a Bayesian-optimization benchmark of copper alloys for blown-powder laser DED
(ONR YIP proposal; exclude publications by Sterling G. Baird). The uploaded files are the whole folder: truth_phys.py
(the truth), calphad_grid.py and calphad_grid.csv (pycalphad + scheil with the open MatCalc mc_ni v2.036 database, 864
Ni-Al-Fe-Mn compositions), calibrate_corrosion.py and calibration_fit.txt (the corrosion-model fit), check_phys.py,
phys_tables.md and phys_tables_c70600.md (its outputs), README.md (the write-up and conclusions), and the two Edison
literature answers used for the calibration (same-test-rates.md, kinetics-constants.md).

The question it answers: the earlier hand-written truth let nothing below about 6 wt% Ni pass a 30-day seawater immersion
test whose bar is "mass loss no greater than dense wrought 70-30 Cu-Ni (C71500)". The new truth concludes the floor is
about 15 wt% Ni with that bar (even 90-10 fails) and about 9 wt% with 90-10 as the bar, mainly because the fit makes Al
nearly useless over a month, Fe in solution strongly protective, and the Ni benefit linear to 30 wt%.

Please check, with code where useful (run the scripts; the grid CSV is included so nothing needs pycalphad):
1. Does the corrosion model's structure (paralinear film, O2 limit, fast/slow film terms, beta-prime selective dissolution,
   porosity) and its fit follow from the cited same-test data, or do the conclusions depend on arbitrary choices (targets,
   weights, bounds, the linear Ni term, the 900 C alpha composition)? Which of the three constants that land on bounds
   matter for the nickel floor? Re-fit with reasonable alternatives and report how the floor (lowest Ni that can pass)
   moves for both bars.
2. Is the use of the CALPHAD grid sound (multilinear interpolation, Scheil range as the crack index, beta at 900 C as the
   beta-prime tendency, Fe-rich solid above the solidus as the nucleant, the conductivity-based lack-of-fusion threshold)?
   Flag anything physically wrong or any bug in truth_phys.py, including the feasibility rules.
3. Are the README's statements supported by the code and tables? List any number that does not match.
Be concrete and quantitative; say plainly what you could not check.
