"""Hook diagonal depth — Entry 41.

For the hook family lam_d = (2, 1^(d-2)), d >= 2, studies the DEPTH

    depth(d) = min N >= 1 such that g(N*lam_d, N*lam_d, N*lam_d) > 0.

Empirical table (all values EXACT via g_fast / Murnaghan-Nakayama):

  d   lam_d          g(1*lam)  g(2*lam)  g(3*lam)   depth
  3   (2,1)               1        ?          ?          1
  4   (2,1,1)             1        ?          ?          1
  5   (2,1,1,1)           0       10          ?          2
  6   (2,1,...,1)         0        9          ?          2
  7   (2,1,...,1)         0        2          ?          2
  8   (2,1^6)             0        0       1646          3
  9   (2,1^7)             0        0       1209          3
 10   (2,1^8)             0        0          ?         >=3
 11   (2,1^9)             0        0          ?         >=3
 12   (2,1^10)            0        0          ?         >=3
 13   (2,1^11)            0        0          ?         >=3

The intermediate partition 2*lam_d = (4, 2^(d-2)) is UNCOVERED by the
B1-B7 coverage dictionary (not two-row, hook, two-col, rectangle, or
orbit-covered) AND vanishes diagonally for d >= 8.  This is a new family
of uncovered diagonal zeros distinct from the original hook zeros (which
are covered by B2/Blasiak).

The zeros g(2*lam_d) = 0 for d=8,9 are confirmed HOLES (g(3*lam_d) > 0),
restating Kronecker non-saturation (Stembridge; BCI 2011) at a second scale.

Feasibility limit: STRETCH_MAX_D from diagonal_census controls when
g(N*lam_d) can be computed (N*d <= STRETCH_MAX_D).
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from .fast import g_fast
from .diagonal_census import STRETCH_MAX_D

Partition = Tuple[int, ...]

# Entry 41 extended wall: character_table(26) ~173s is feasible in a
# dedicated run, though too slow for the default test suite.  Tests at
# d=13 (N*d=26) are marked @pytest.mark.slow.
HOOK_MAX_D: int = 27  # max N*d we're willing to compute (matches d=9 N=3)


def hook_lam(d: int) -> Partition:
    """Hook partition (2, 1^(d-2)) for d >= 2.  For d=2 returns (2,)."""
    if d < 2:
        raise ValueError(f"d must be >= 2, got {d}")
    if d == 2:
        return (2,)
    return (2,) + (1,) * (d - 2)


def g_hook_diag(d: int, N: int, max_d: Optional[int] = None) -> Optional[int]:
    """g(N*lam_d, N*lam_d, N*lam_d) where lam_d = hook_lam(d).

    Returns None if N*d > max_d (default: HOOK_MAX_D).
    Returns an exact integer otherwise.
    """
    limit = HOOK_MAX_D if max_d is None else max_d
    if N * d > limit:
        return None
    lam = hook_lam(d)
    scaled: Partition = tuple(N * x for x in lam)
    return g_fast(scaled, scaled, scaled)


def hook_depth_row(d: int, N_max: int = 3) -> Dict:
    """Compute g(N*lam_d) for N=1..N_max and return depth info.

    Returns dict:
      'd'      : d
      'lam'    : hook_lam(d)
      'values' : [g(1*lam), g(2*lam), ..., g(N_max*lam)]  (None = infeasible)
      'depth'  : first N in 1..N_max with g > 0, or None if not found
    """
    lam = hook_lam(d)
    values: List[Optional[int]] = []
    depth: Optional[int] = None
    for N in range(1, N_max + 1):
        g = g_hook_diag(d, N)
        values.append(g)
        if g is not None and g > 0 and depth is None:
            depth = N
    return {"d": d, "lam": lam, "values": values, "depth": depth}


def predicted_d0(a: int) -> int:
    """Predicted first d with g(hook_{a,d}^3) = 0.

    Conjecture (Entry 42): d_0(a) = 3a - 1.
    Verified for a=1 (sign rep: d_0=2), a=2 (d_0=5), a=3 (d_0=8),
    a=4 (d_0=11), a=5 (d_0=14).
    """
    return 3 * a - 1


def predicted_T(a: int) -> int:
    """Predicted depth-bifurcation threshold T(a).

    Conjecture (Entry 42): T(a) = 3a + 2.
    g(2*hook_{a,d}, ...) = 0 first at d = T(a).
    Verified for a=1 (T=5), a=2 (T=8), a=3 (T=11).
    Predicted for a=4 (T=14) and a=5 (T=17) — not yet computable.

    Equivalently: T(a) = d_0(a) + 3.
    """
    return 3 * a + 2


def last_hole_value(a: int) -> int:
    """Predicted g(2*hook_{a,T(a)-1}, ...) = a (the last non-zero value before threshold).

    Conjecture (Entry 42): the minimum non-zero g(2*lam_{a,d}) over feasible d equals a.
    Verified for a=1 (g=1), a=2 (g=2), a=3 (g=3).
    Predicted for a=4 (g=4 at d=13).
    """
    return a


def fat_hook_lam(a: int, b: int, k: int) -> Partition:
    """Fat-hook partition (a, b^k) for a >= b >= 1, k >= 1.

    Entry 44: b=2 family (a, 2^k) studied for a=2..6.
    """
    if a < b:
        raise ValueError(f"a={a} must be >= b={b} for a valid partition")
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    return (a,) + (b,) * k


def fat_hook_diag(a: int, b: int, k: int, max_d: Optional[int] = None) -> Optional[int]:
    """g(lam, lam, lam) where lam = fat_hook_lam(a, b, k) = (a, b^k).

    Returns None if d = a + b*k > max_d (default HOOK_MAX_D).
    """
    limit = HOOK_MAX_D if max_d is None else max_d
    d = a + b * k
    if d > limit:
        return None
    lam = fat_hook_lam(a, b, k)
    return g_fast(lam, lam, lam)


def predicted_fat_d0(a: int, b: int) -> Optional[int]:
    """Predicted first d with g(fat_hook(a,b,k)^3) = 0 (Entry 44).

    Conjectures:
      b=1: d_0 = 3a - 1  (C42, verified a=1..6)
      b=2: d_0 = 3a + 4  (C44, verified a=2..6)
    Returns None for b not in {1, 2}.
    """
    if b == 1:
        return 3 * a - 1
    if b == 2:
        return 3 * a + 4
    return None


def summary(d_min: int = 3, d_max: int = 13, N_max: int = 3) -> List[Dict]:
    """Print depth table for hook lam_d, d=d_min..d_max, N=1..N_max.

    Returns list of hook_depth_row dicts.
    """
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    header_cols = "  ".join(f"g(N={n})" for n in range(1, N_max + 1))
    print("=" * 76)
    print("Hook diagonal depth: g(N*lam_d, N*lam_d, N*lam_d), lam_d = (2, 1^(d-2))")
    print(f"{'d':>3}  {'lam_d':<20}  {header_cols}  depth")
    print("-" * 76)

    rows: List[Dict] = []
    for d in range(d_min, d_max + 1):
        row = hook_depth_row(d, N_max)
        vals = []
        for v in row["values"]:
            if v is None:
                vals.append("?".rjust(8))
            else:
                vals.append(str(v).rjust(8))
        depth_str = str(row["depth"]) if row["depth"] is not None else f">{N_max}"
        print(f"{d:>3}  {str(row['lam']):<20}  {'  '.join(vals)}  {depth_str}")
        rows.append(row)

    print("-" * 76)
    print("'?' = N*d > STRETCH_MAX_D = infeasible at current wall")
    print("\nKey claim (Entry 41):")
    print("  depth(lam_d) = 2 for d=5,6,7   [g(lam)=0, g(2*lam)>0]")
    print("  depth(lam_d) = 3 for d=8,9     [g(lam)=g(2*lam)=0, g(3*lam)>0]")
    print("  depth(lam_d) >=3 for d=10..13  [g(lam)=g(2*lam)=0; N=3 infeasible]")
    print("  threshold at d=8 (partition 2*lam_d=(4,2^(d-2)) UNCOVERED by B1-B7)")
    print("=" * 76)
    return rows
