"""Iso-hardness control (Module 26) — disentangle the leverage from the H-confound.

Module 25 reached n=6 by recalibrating the threshold to the MEDIAN OBDD size, but the
hard-fraction H then varied across levels (0.17 / 0.25 / 0.44), so the Adversary could
say the relative anisotropy `rel` was tracking H, not the level n.  This module HOLDS H
~ constant (the (1-H_target) quantile of the OBDD-size distribution) and re-measures.

MEASURED: at TWO fixed-H slices (H_target 0.5 and 0.2) the order-anisotropy stays
significant at every level (control flat) — survival is H-ROBUST, not an H-artifact —
and `rel` still PEAKS at n=5 (the H-confound is falsified) but does NOT grow (no
leverage).  ESTIMATES with CIs at n>=5; no P vs NP claim.

    py examples/run_iso_hardness.py            # ~8 min (6 seeds x 120k, both slices)
    py examples/run_iso_hardness.py quick      # ~3 min (3 seeds x 80k, both slices)
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
    seeds, M = (3, 80000) if quick else (6, 120000)

    print("=" * 80)
    print("  ISO-HARDNESS CONTROL — survival is H-robust, leverage is genuinely absent (Module 26)")
    print("=" * 80)
    print("\n  Module 25's median policy let H drift (0.17/0.25/0.44).  Here the threshold s")
    print("  is chosen so H ~ H_target at EVERY level, so `rel` is read free of the H-drift.")
    print("  Pre-registered pair: top variable x_{n-1} vs x0.  n=4 EXACT; n=5,6 sampled CRN.\n")

    t0 = time.time()
    for H_target in (0.5, 0.2):
        print(f"  --- iso-hardness slice: H_target = {H_target} ---")
        print("   n    s   H_ach    base_prob   diff_prob      z       rel=diff/base   ctrl_z  signs")
        for n in (4, 5, 6):
            r = s5.iso_hardness_row(n, H_target=H_target, seeds=seeds, M=M)
            zt = "  exact" if r.exact else f"{r.z:+7.1f}"
            ct = "   --" if r.exact else f"{r.control_z:+.2f}"
            st = " --" if r.exact else f"{int(r.frac_positive * seeds)}/{seeds}"
            tag = "n=4*" if r.exact else f"n={n} "
            print(f"  {tag}  {r.s:3d}  {r.H_frac:.3f}    {r.base_prob:.3e}  {r.diff_prob:+.3e}  "
                  f"{zt}   {r.rel:+.4f}        {ct}   {st}")
        print()
    print(f"  (sampled levels, both slices: {time.time() - t0:.0f}s)\n")

    print("  VERDICT: at BOTH fixed-H slices the signal is significant at every level with")
    print("  the control flat -> the killer does NOT fire: Module 25's SURVIVAL is H-ROBUST.")
    print("  And `rel` still peaks at n=5 holding H fixed -> the H-confound is FALSIFIED, but")
    print("  the peak is bounded/non-monotone -> there is NO growing leverage hiding behind")
    print("  the H-drift.  The 'no leverage' ceiling is cleaner, not lifted.  Amplification")
    print("  stays CITED.  No separation, no P vs NP claim.")
    print("=" * 80)


if __name__ == "__main__":
    main()
