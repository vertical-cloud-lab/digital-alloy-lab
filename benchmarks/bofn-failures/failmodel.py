"""Which stage evaluations fail, and why: the failure "truth" layered on the two networks.

Every physical stage can fail in one of two ways, which are what Ax's two statuses are for:

* **transient** (Ax `FAILED`): a fault unrelated to the inputs. The run says nothing about the
  design and could be repeated. Examples from the lab's own record: the induction generator
  tripping mid-pour (Nov 5), a plate that never started atomizing on its second use (Oct 28,
  Nov 13), a bar breaking outside the gauge.
* **input-caused** (Ax `ABANDONED`): the inputs make the stage impossible. Repeating it will fail
  again. Here these are physical regions of each stage's own inputs: severe hot cracking that
  curls parts into the recoater, lack of fusion so bad the layers delaminate, keyhole spatter,
  a deposit that never fuses at the small DED machine's power cap, and too little usable powder
  to spread or feed (a known threshold on a measured intermediate).

The probability of an input-caused failure is a steep logistic of a physical score, so it is
nearly deterministic away from a thin boundary. Its arguments are the stage's *true* inputs
(design variables and the true parent outputs), so in design space the failure regions are
curved, and they move with the composition through CALPHAD's outputs.

Each failure also gets a *label*, which is what the lab writes down. With `label_noise = e`, the
label is the wrong kind with probability e (the operator can't always tell a bad plate from a bad
alloy). Draws come from one random stream per (seed, stage), consumed in attempt order, so every
strategy faces the same sequence of transient faults and label flips.
"""

from __future__ import annotations

import math

import numpy as np

Q_MIN = 0.25  # usable-powder threshold (scaled): below it a lot can't be spread (LPBF) or fed (DED)

# transient (input-independent) failure probability per stage attempt; see README "Assumptions"
P_TRANSIENT = {
    "al": {"A": 0.15, "L": 0.08, "T": 0.03},
    "cu": {"A": 0.20, "U": 0.05, "M": 0.08, "T": 0.03, "I": 0.05},
}
# stages that can fail because of their inputs
INPUT_STAGES = {"al": ("L",), "cu": ("U", "M")}
# stages a failed precondition (q < Q_MIN) blocks; the lab knows q, so it never pays for them
PRECONDITION_STAGES = {"al": ("L",), "cu": ("U", "M")}

SCENARIOS = {
    # name: (input-caused failures on, transient scale, label noise)
    "mixed": (True, 1.0, 0.0),  # the main scenario: both kinds, labelled correctly
    "mislabel": (True, 1.0, 0.3),  # both kinds, 30% of labels wrong
    "transient": (False, 1.0, 0.0),  # transient faults only
    "nofail": (False, 0.0, 0.0),  # reference: nothing fails (the source benchmarks' world)
    "edge": (True, 1.0, 0.0),  # as mixed, but the aluminum crack crash reaches up to the optimum (CRACK_CRASH)
}
# the hot-cracking crash of an LPBF build: P(crash) = top * sigmoid((crack - mid) / width). By default only
# the most cracked builds crash; in "edge" builds crash from a crack severity of about 0.12, which puts the
# boundary next to the kappa = 1 optimum (crack 0.07 there: 6 % of its builds crash)
CRACK_CRASH = {"default": dict(mid=0.9, width=0.03, top=0.6), "edge": dict(mid=0.12, width=0.02, top=0.9)}


def sig(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def p_input_lpbf(P, v, f, g, kappa, mid=0.9, width=0.03, top=0.6):
    """Aluminum LPBF build: P(crash) from the build's true inputs (bofn-prelim's rho terms).

    - severe hot cracking: up to 60% of the most cracked builds (crack severity above about 0.9)
      curl and catch the recoater, so this failure is input-caused but not certain;
    - lack of fusion: far below the energy-density ridge (u < -0.35, where the truth's window
      term is below 0.05) layers don't bond and the parts delaminate;
    - keyholing at the top of the power range (P above about 0.92): spatter and swelling.
    """
    u = P - v - (0.05 + 0.25 * f)
    g = max(g, 0.0)
    f_eff = f * (1 - kappa * 0.85 * g / (g + 0.12))
    crack = sig((f_eff - 0.38) / 0.05)  # the truth's crack term (bofn-prelim AlloyTruth, node rho)
    p_crack = top * sig((crack - mid) / width)
    p_lof = sig((-u - 0.35) / 0.03)
    p_key = sig((P - 0.92) / 0.02)
    return 1 - (1 - p_crack) * (1 - p_lof) * (1 - p_key), dict(crack=crack, u=u)


def p_input_ded(P, v, f, g, h, kappa, f_crack, utah, p_cap):
    """Copper DED session: P(no usable deposit) from the session's true inputs (bofn-cu-ded's terms).

    - Utah (power capped): the deposit never fuses (lack-of-fusion index above about 0.85);
    - Mines: hot tearing delaminates up to 60% of the most cracked deposits (crack severity
      above about 0.9), the deposit never fuses, or keyholing (P above about 0.92).
    """
    Pe = min(P, p_cap) if utah else P
    lof = sig((h - Pe) / 0.08)  # the truth's lack-of-fusion term
    p_lof = sig((lof - 0.85) / 0.03)
    if utah:
        return p_lof, dict(lof=lof)
    g = max(g, 0.0)
    f_eff = f * (1 - kappa * 0.85 * g / (g + 0.12))
    crack = sig((f_eff - f_crack) / 0.05)
    p_crack = 0.6 * sig((crack - 0.9) / 0.03)
    p_key = sig((P - 0.92) / 0.02)
    return 1 - (1 - p_crack) * (1 - p_lof) * (1 - p_key), dict(crack=crack, lof=lof)


class FailureModel:
    """Decides the outcome of each stage attempt for one run (one seed, one scenario)."""

    def __init__(self, family: str, scenario: str, seed: int, kappa: float, f_crack: float = 0.56, p_cap: float = 0.5):
        self.family = family
        self.inputs_on, scale, self.label_noise = SCENARIOS[scenario]
        self.p_tr = {s: min(1.0, p * scale) for s, p in P_TRANSIENT[family].items()}
        self.kappa, self.f_crack, self.p_cap = kappa, f_crack, p_cap
        self.crash = CRACK_CRASH.get(scenario, CRACK_CRASH["default"])
        self._rng = {}
        self.seed = seed
        self.stage_index = {s: i for i, s in enumerate("CAULMSTKI")}

    def _draws(self, stage):
        if stage not in self._rng:
            self._rng[stage] = np.random.default_rng([7919, self.seed, self.stage_index[stage]])
        return self._rng[stage].random(3)  # (input-caused, transient, label flip)

    def p_input(self, stage, z):
        """Probability that the inputs make this stage fail; z holds the true node inputs."""
        if not self.inputs_on or stage not in INPUT_STAGES[self.family]:
            return 0.0, {}
        if self.family == "al":
            return p_input_lpbf(z["P"], z["v"], z["f"], z["g"], self.kappa, **self.crash)
        return p_input_ded(z["P"], z["v"], z["f"], z["g"], z["h"], self.kappa, self.f_crack, stage == "U", self.p_cap)

    def attempt(self, stage, z):
        """Outcome of one attempt: (status, true kind, label), status COMPLETED or FAILED."""
        u_in, u_tr, u_lab = self._draws(stage)
        p_in, _ = self.p_input(stage, z)
        if u_in < p_in:
            kind = "input"
        elif u_tr < self.p_tr.get(stage, 0.0):
            kind = "transient"
        else:
            return "COMPLETED", None, None
        label = kind
        if u_lab < self.label_noise:
            label = "transient" if kind == "input" else "input"
        return "FAILED", kind, label
