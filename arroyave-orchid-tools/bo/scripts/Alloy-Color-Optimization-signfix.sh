#!/bin/bash
# Two-line patch to test the price-sign finding (run in a copy of the repo):
#   price GP models -price (BoTorch EHVI maximises all outputs; the HV front uses -price)
#   printed Pareto front uses is_non_dominated(-train_obj) (minimisation)
sed -e 's/price_gp = SingleTaskGP(compositions, price_norm_all.unsqueeze(-1))/price_gp = SingleTaskGP(compositions, -price_norm_all.unsqueeze(-1))/' \
    -e 's/pareto_mask = is_non_dominated(train_obj)/pareto_mask = is_non_dominated(-train_obj)/' \
    multiobjective_ehvi.py > multiobjective_ehvi_signfix.py
python multiobjective_ehvi_signfix.py --csv color_quinary_5%.csv --plot out/multiobj_objectives_signfix.png
