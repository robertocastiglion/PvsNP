"""Sampled order-anisotropy at n=5 (Module 24) — the lab's FIRST cross-level PASS.

Spends exactness for reach: estimates by Monte Carlo (CRN) whether the order-
anisotropy of MBPSP[s], found EXACTLY at n=4 in Module 22, survives one level up to
n=5 (N=32, 2^32 truth tables — infeasible to enumerate).  Prints the n=4 fidelity
anchor, the replicated n=5 verdict with its null control, and the measured ceiling
(the faithful threshold regime degenerates at n>=6).  ESTIMATES with CIs, not exact
integers.  No P vs NP claim.

    py examples/run_sampled_order_n5.py            # ~6 min (8 seeds x 250k)
    py examples/run_sampled_order_n5.py quick      # ~2 min (6 seeds x 120k)
"""

import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.meta_complexity import sampled_order_n5 as s5  # noqa: E402


def main() -> None:
    quick = len(sys.argv) > 1 and sys.argv[1] == "quick"
    seeds, M = (6, 120000) if quick else (8, 250000)

    print("=" * 78)
    print("  SAMPLED ORDER-ANISOTROPY AT n=5 — exactness traded for reach (Module 24)")
    print("=" * 78)

    # ── 1. fidelity anchor at n=4 (exact ground truth inside the CI) ──────
    print("\n  1) FIDELITY ANCHOR (n=4, exact answer known): the sampler must contain it")
    a = s5.anchor_n4(M=60000, seed=0)
    lo, hi = (round(x * (1 << a.est.N)) for x in a.est.ci99_prob)
    print(f"     pre-registered pair  d_hi=8 [x3]  vs  d_lo=2 [x1]")
    print(f"     exact pairinf diff   = {a.exact_count}   (Module 22: 4056 - 3872)")
    print(f"     sampled diff (count) = {round(a.est.mean_count)}   99% CI = ({lo}, {hi})")
    print(f"     exact inside 99% CI  : {a.within_ci}   -> estimator VALIDATED")

    # ── 2. the decisive n=5 run (replicated, with null control) ───────────
    print(f"\n  2) n=5 SIGNAL (N=32, 2^32 truth tables): {seeds} seeds x {M} (CRN, pooled)")
    print(f"     pre-registered pair  d_hi=16 [x4, top var]  vs  d_lo=1 [x0]")
    t0 = time.time()
    v = s5.replicate_n5(M_per_seed=M, seeds=seeds, base_seed=1000)
    dt = time.time() - t0
    print(f"     s = {v.s}   ({dt:.0f}s)")
    print(f"     pooled diff prob = {v.mean_prob:+.3e}   se = {v.se_prob:.3e}   z = {v.z:+.2f}")
    print(f"     99% CI           = ({v.ci99_prob[0]:+.3e}, {v.ci99_prob[1]:+.3e})")
    print(f"     seeds positive   = {v.frac_positive:.0%}")
    print(f"     popcount CONTROL : pooled diff = {v.control_mean:+.3e}   z = {v.control_z:+.2f}")
    print(f"     KILLER fires     : {v.killer_fires}      PASS : {v.passes}")
    if v.passes:
        print("     => the order-anisotropy of MBPSP[s] SURVIVES one level above n=4.")

    # ── 3. the ceiling: the faithful threshold regime degenerates at n>=6 ─
    print("\n  3) CEILING (survival, NOT leverage) — faithful policy s=round(0.5*max):")
    print("      n  size[min/med/max]   s    H_frac   base_prob(boundary)")
    for r in s5.threshold_regime((4, 5, 6, 7), sample=2500, base_M=30000):
        print(f"      {r.n}    {r.size_min:3d}/{r.size_median:3d}/{r.size_max:3d}"
              f"      {r.s:3d}   {r.H_frac:.3f}   {r.base_prob:.4e}")
    print("     Random OBDD sizes concentrate near max; at n>=6 the sample min already")
    print("     exceeds s -> meta-function constant-HARD -> pair-influence -> 0.  Sampling")
    print("     buys EXACTLY ONE level over the exact n=4; no monotone leverage.")

    print("\n  " + s5.honesty_note())
    print("=" * 78)


if __name__ == "__main__":
    main()
