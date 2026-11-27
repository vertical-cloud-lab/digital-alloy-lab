"""PAIPAI-shim/sitecustomize.py: compatibility shim used only for the PAIPAI test run.

PAIPAI 00ff18b's workers call GraceCalculator(model=..., device=..., verbose=True, fmax=...,
max_steps=...) and later set calc.max_steps. ArroyaveLab MaterialsFramework 0ec8168 (v1.0.0)
has no `device` or `max_steps` parameter (it uses `steps`), so the call raises
"TypeError: object.__init__() takes exactly one argument". This shim, put on PYTHONPATH so
Python imports it at start-up, swaps in a subclass that drops `device` (TensorFlow runs on CPU
here) and maps max_steps -> steps. It changes nothing else.
"""
try:
    import materialsframework.calculators as _mfc
    from materialsframework.calculators.grace import GraceCalculator as _Grace

    class GraceCalculator(_Grace):
        def __init__(self, *args, device=None, max_steps=None, **kwargs):
            if max_steps is not None:
                kwargs.setdefault("steps", max_steps)
            super().__init__(*args, **kwargs)

        @property
        def max_steps(self):
            return self.steps

        @max_steps.setter
        def max_steps(self, value):
            self.steps = value

    _mfc.GraceCalculator = GraceCalculator
except Exception as exc:  # pragma: no cover - only reached outside the PAIPAI venv
    import sys

    print(f"[PAIPAI-shim] not active: {exc}", file=sys.stderr)
