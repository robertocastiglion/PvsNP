#!/usr/bin/env python3
"""Quick test script for engine3 cross-check C53."""
import sys
sys.path.insert(0, 'pnp_lab/gct_kronecker')

from engine3 import g3
import time

# C53 cross-check: g((6^6)^3) d=36 must equal 9309
lam = (6, 6, 6, 6, 6, 6)
mu = (6, 6, 6, 6, 6, 6)
nu = (6, 6, 6, 6, 6, 6)

print(f"engine3 cross-check C53: g{lam}^3 at d=36")
print(f"  Killer pre-declared: 9309")
print(f"  Computing g3{lam}, {mu}, {nu})...")

start = time.time()
result = g3(lam, mu, nu)
elapsed = time.time() - start

print(f"  Result: g3 = {result}")
print(f"  Time: {elapsed:.1f}s")

if result == 9309:
    print(f"  ✓ CONFIRMED dual-engine: C53 kill valid!")
    sys.exit(0)
else:
    print(f"  ✗ MISMATCH: expected 9309, got {result}")
    print(f"  → C53 kill INVALIDATED, potential erratum-dati")
    sys.exit(1)
