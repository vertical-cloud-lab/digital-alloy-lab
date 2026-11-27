# Draft upstream issue for ArroyaveLab/eagar-tsai (not filed)

**Title:** Linux wheels for 0.6.0 reference `__exp_finite`, so the C integrand fails to import and the pure-Python
fallback runs without a warning

On Linux with glibc 2.31 or newer (checked on Ubuntu 24.04, glibc 2.39, Python 3.12), `pip install eagar-tsai==0.6.0`
installs `eagar_tsai-0.6.0-cp312-cp312-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl`, and the
compiled integrand does not load:

```
>>> import eagar_tsai._integrand_ext
ImportError: .../eagar_tsai/_integrand_ext.cpython-312-x86_64-linux-gnu.so: undefined symbol: __exp_finite
>>> from eagar_tsai._core import _INTEGRAND; type(_INTEGRAND)
<class 'function'>      # expected scipy LowLevelCallable
```

`_core._get_integrand()` catches the `ImportError` and silently falls back to `eagar_tsai_integrand`. One `quad`
call then takes about 137 µs instead of 6 µs, and whole melt-pool rows run about 25× slower. Nothing tells the user.

**Cause.** `nm -D` on the extension shows an unversioned `U __exp_finite`. `setup.py` compiles with
`-O3 -ffast-math`. With `-ffast-math`, glibc headers older than 2.31 redirect `exp()` to `__exp_finite`, and the
manylinux build images are older than 2.31. From glibc 2.31 on, the `*_finite` functions exist only as compat symbols
for already-linked binaries, and an unversioned reference cannot bind to them. The extension is not linked against
`libm`, so auditwheel never sees the reference. The cp313 and cp314 manylinux wheels carry the same reference, while the
cp312 musllinux wheel references plain `exp`. The Windows and macOS wheels aren't built against glibc, so they shouldn't be
affected (not checked).

**Workaround.** `pip install --force-reinstall --no-deps --no-binary eagar-tsai eagar-tsai`. This needs a C compiler.

**Suggested fixes.**
1. Drop `-ffast-math` from `extra_compile_args`, or add `-fno-finite-math-only`, or link `libm`
   (`libraries=["m"]`) so the symbol is versioned.
2. Log a warning when `_get_integrand()` falls back to the Python integrand.
3. In the release workflow, test the built wheel on a current Linux image by importing `_integrand_ext` (cibuildwheel's
   `test-command`).
