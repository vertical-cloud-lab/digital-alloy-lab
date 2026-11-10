#!/bin/bash
# Reproduce the no-licence runs of ArroyaveLab/CALPHAD. Args: <work copy of repo> <venv python> <scripts dir>
set -u
W=$1; PY=$2; S=$3
cd "$W" || exit 1
# (1) composition generator as shipped (Ti-V-Co, resolution 200) -- timing only
( cd Setup && /usr/bin/time -f "Compositions.py as shipped: %e s, %M KB" $PY Compositions.py && ls -la *.csv | head -12 && wc -l TiVCo_n3_d200_*.csv )
# (2) same generator, resolution 20 (the file TC_Equilibrium.py's __main__ expects), and an Al-Cu-Mg-Si grid
mkdir -p Equilibrium/run && cp Setup/thermocalc_library.py Equilibrium/
sed -e 's/^resolution = 200/resolution = 20/' Setup/Compositions.py > Equilibrium/run/Compositions_d20.py
sed -e "s/^elements = \['Ti','V','Co'\]/elements = ['Al','Cu','Mg','Si']/" -e 's/^resolution = 200/resolution = 20/' Setup/Compositions.py > Equilibrium/run/Compositions_AlCuMgSi_d20.py
( cd Equilibrium/run && $PY Compositions_d20.py && $PY Compositions_AlCuMgSi_d20.py && wc -l *single_system.csv *all_systems.csv )
# (3) TC_Equilibrium.py with a MOCK tc_python, 2 divisions on 2 cores instead of 10/10
sed -e 's/^    file_divisions: int = 10/    file_divisions: int = 2/' -e 's/^    cpu_cores: int = 10/    cpu_cores: int = 2/' Equilibrium/TC_Equilibrium.py > Equilibrium/run/TC_Equilibrium_mock2.py
cp Equilibrium/thermocalc_library.py Equilibrium/run/
( cd Equilibrium/run && PYTHONPATH=$S/mock_tc_python /usr/bin/time -f "TC_Equilibrium (mock) wall %e s" $PY TC_Equilibrium_mock2.py 2>&1 | tail -8; ls TiVCo_n3_d20_single_system_TCequi1/; head -3 TiVCo_n3_d20_single_system_TCequi1/All_data.csv; wc -l TiVCo_n3_d20_single_system_TCequi1/All_data.csv )
