import pathlib
import sys

import pytest

CONTROL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(CONTROL))

from ftctl.clock import SimClock  # noqa: E402
from ftctl.config import Config  # noqa: E402
from ftctl.hw.sim import make_sim_machine  # noqa: E402
from ftctl.logger import BuildLog  # noqa: E402
from ftctl.scanprog import find_program, load_npz, synthetic  # noqa: E402
from ftctl.supervisor import Supervisor  # noqa: E402


@pytest.fixture(scope="session")
def program():
    """The process worker's scan program if it is on this machine, else a synthetic 10 x 10 mm square."""
    p = find_program()
    return load_npz(p) if p else synthetic(80)


class Rig:
    def __init__(self, program, out_dir, cfg=None, seed=1):
        self.cfg = cfg or Config()
        self.clock = SimClock()
        self.prog = program
        self.m = make_sim_machine(self.cfg, self.clock, program.timing(), seed=seed)
        self.w = self.m.world
        self.log = BuildLog(out_dir, self.clock)
        self.sup = Supervisor(self.m, self.cfg, program, self.log, self.clock)

    def run(self, n_layers, **kw):
        self.summary = self.sup.run(list(range(n_layers)), **kw)
        return self.summary

    def assert_safe(self):
        """After a fault: beam off, list stopped, nothing moving, vibrator off, heaters off, state STOPPED."""
        w, m = self.w, self.m
        assert self.summary["result"] == "fault"
        assert self.summary["final_state"] == "STOPPED"
        assert not w.emission
        assert not w.list_busy
        assert not m.piston.busy() and not m.recoater.busy()
        assert not m.io.out["VIBRATOR"]
        assert not m.io.out["HEAT_EN"]
        assert not m.plate.running and not m.block.running
        codes = [e["code"] for e in self.log.events if e["kind"] == "fault"]
        assert codes == [self.summary["fault"]["code"]]


@pytest.fixture
def rig(program, tmp_path):
    def make(cfg=None, seed=1, prog=None):
        return Rig(prog or program, tmp_path, cfg, seed)
    return make
