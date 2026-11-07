"""Build an AkaiKKR CPA input for fcc Cu70Ni30 with akaitools.InputFile, write it, parse it back,
and check the round trip. Usage: python -I akaitools_cuni_input.py <out_dir>"""
import sys
from pathlib import Path

from akaitools import InputFile
from akaitools.models import AtomicComponent, AtomPosition, AtomType

out = Path(sys.argv[1])
cuni = InputFile(
    mode="go", data_file="data/cuni", bravais="fcc", a=6.75,  # ~3.57 A in bohr
    atom_types=[AtomType(name="CuNi", rmt=0.0, field=0.0, lmxtyp=2,
                         components=[AtomicComponent(anclr=29.0, conc=0.7), AtomicComponent(anclr=28.0, conc=0.3)])],
    positions=[AtomPosition(x=0.0, y=0.0, z=0.0, atom_type="CuNi")],
)
text = cuni.to_string()
print(text)
cuni.write(out / "cuni_cpa.in")
back = InputFile.from_file(out / "cuni_cpa.in")
print("round trip identical:", back.to_string() == text)
