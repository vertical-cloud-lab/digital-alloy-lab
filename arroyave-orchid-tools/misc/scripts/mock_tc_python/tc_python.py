"""Minimal stand-in for Thermo-Calc's TC-Python, only to exercise ArroyaveLab/CALPHAD's
orchestration (input checks, core splitting, per-process sessions, CSV writing, concatenation)
without a licence. It returns made-up, deterministic numbers: NOT thermodynamics.
Covers only the calls TC_Equilibrium.py / thermocalc_library.py make.
"""
__version__ = "MOCK-0.0"


class ThermodynamicQuantity:
    @staticmethod
    def temperature():
        return ("T",)

    @staticmethod
    def mole_fraction_of_a_component(el):
        return ("X", el)

    @staticmethod
    def volume_fraction_of_a_phase(ph):
        return ("VPV", ph)

    @staticmethod
    def molar_volume_of_phase(ph):
        return ("VM", ph)


class CompositionUnit:
    MOLE_FRACTION = "mole_fraction"


class _Result:
    def __init__(self, cond):
        self.cond = dict(cond)

    def get_phases(self):
        return ["BCC_A2", "FCC_A1", "LIQUID"]

    def _x(self):
        return {k[1]: v for k, v in self.cond.items() if k[0] == "X"}

    def get_value_of(self, q):
        x = self._x()
        T = self.cond.get(("T",), 298.15)
        s = sum(x.values())
        if q[0] == "VPV":  # fake: BCC grows with the 2nd element, liquid above 1800 K
            liq = min(1.0, max(0.0, (T - 1800) / 400))
            bcc = (1 - liq) * min(1.0, 0.2 + 0.8 * (list(x.values())[1] if len(x) > 1 else 0.5))
            return {"BCC_A2": bcc, "FCC_A1": max(0.0, 1 - liq - bcc), "LIQUID": liq}[q[1]]
        if q[0] == "VM":
            return 7e-6 + 1e-6 * s
        raise KeyError(q)

    def change_temperature(self, T):
        c = dict(self.cond)
        c[("T",)] = T
        return _Result(c)


class _Calc:
    def __init__(self):
        self.cond = {}

    def set_condition(self, q, v):
        self.cond[q] = v
        return self

    def calculate(self):
        return _Result(self.cond)


class _System:
    def with_single_equilibrium_calculation(self):
        return _Calc()


class _Builder:
    def get_system(self):
        return _System()


class TCPython:
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def select_database_and_elements(self, db, els):
        return _Builder()

    def get_databases(self):
        return ["TCHEA7", "TCAL9", "MOBHEA3"]
