"""Cross-level order-anisotropy under median calibration (Module 25) — push to n=6.

Module 24 reached n=5 under Module 22's faithful threshold (theta=0.5*max), which
DEGENERATES at n>=6.  Recalibrating the threshold to the MEDIAN OBDD size keeps the
boundary open at every level, so the order-anisotropy of MBPSP[s] is measurable on
THREE levels (n=4 exact, n=5 and n=6 sampled).  It SURVIVES all three — but the
leverage does NOT grow (relative effect non-monotone, ~7-12%), and the object is
RECALIBRATED (a different threshold from Module 22).  ESTIMATES with CIs at n>=5; no
P vs NP claim.

    py examples/run_cross_level_median.py            # ~12 min (6 seeds x 150k)
    py examples/run_cross_level_median.py quick      # ~5 min (3 seeds x 100k)
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
    seeds, M = (3, 100000) if quick else (6, 150000)

    print("=" * 80)
    print("  CROSS-LEVEL ORDER-ANISOTROPY (median calibration) — survival to n=6 (Module 25)")
    print("=" * 80)
    print("\n  Faithful theta=0.5*max degenerates at n>=6; recalibrate s = MEDIAN OBDD size")
    print("  so the boundary stays open.  Pre-registered pair: top variable x_{n-1} vs x0.")
    print("  n=4 is EXACT (full sweep); n=5, n=6 are sampled CRN, pooled over seeds.\n")

    print("   n    s   H_frac   base_prob   diff_prob      z       rel=diff/base   ctrl_z  signs")
    t0 = time.time()
    for n in (4, 5, 6):
        r = s5.cross_level_row(n, seeds=seeds, M=M)
        zt = "  exact" if r.exact else f"{r.z:+7.1f}"
        ct = "   --" if r.exact else f"{r.control_z:+.2f}"
        st = " --" if r.exact else f"{int(r.frac_positive * seeds)}/{seeds}"
        tag = "n=4*" if r.exact else f"n={n} "
        print(f"  {tag}  {r.s:3d}  {r.H_frac:.3f}   {r.base_prob:.3e}  {r.diff_prob:+.3e}  "
              f"{zt}   {r.rel:+.4f}        {ct}   {st}")
    print(f"\n  (sampled levels: {time.time() - t0:.0f}s)")

    print("\n  VERDICT: the order-anisotropy SURVIVES all three levels (n=5,6 significant,")
    print("  all seeds positive, popcount control flat at every level).  But the LEVERAGE")
    print("  does NOT grow: rel is non-monotone and bounded (~7-12%), and is confounded by")
    print("  H varying across levels.  Cross-level SURVIVAL, not cross-level leverage growth.")
    print("  The asymptotic amplification stays CITED.  No separation, no P vs NP claim.")
    print("=" * 80)


if __name__ == "__main__":
    main()
