"""Tabella s*(d) per partizioni self-conjugate 3-hook — H65.

Esegui con:  py examples/run_crossing.py
"""

import sys
sys.stdout.reconfigure(encoding="utf-8")

from fractions import Fraction
from pnp_lab.gct_kronecker.crossing import enum_sc3hook, compute_crossing

D_LIST = [13, 15, 21, 23, 25, 27]

print("=" * 72)
print("H65 — Crossing s*(d) per self-conjugate 3-hook")
print(f"{'d':>4}  {'#shape':>6}  {'s*':>8}  {'R_min':>10}  {'R_max':>10}")
print("-" * 72)

crossings = {}
for d in D_LIST:
    pts = enum_sc3hook(d)
    n = len(pts)
    c = compute_crossing(d)
    crossings[d] = c
    if pts:
        r_min = min(float(p[3]) for p in pts)
        r_max = max(float(p[3]) for p in pts)
        r_min_s = f"{r_min:.4f}"
        r_max_s = f"{r_max:.4f}"
    else:
        r_min_s = r_max_s = "  n/a"
    c_str = f"{float(c):.4f}" if c is not None else "  none"
    print(f"{d:>4}  {n:>6}  {c_str:>8}  {r_min_s:>10}  {r_max_s:>10}")

print("-" * 72)
print()
print("|Delta s*| tra d consecutivi (solo d con crossing):")
valid = [(d, crossings[d]) for d in D_LIST if crossings[d] is not None]
for i in range(len(valid) - 1):
    da, ca = valid[i]
    db, cb = valid[i + 1]
    delta = abs(float(cb) - float(ca))
    print(f"  d={da}->{db}:  |Delta s*| = {delta:.4f}")

print()
print("Predizioni H65:")
print("  s*(23) in [0.55, 0.62]")
print("  s*(25) in [0.55, 0.61]")
print("  s*(27) in [0.55, 0.60]")
print("  |Delta s*| monotona decrescente; ultimo passo < 0.02")
print("=" * 72)
