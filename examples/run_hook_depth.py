"""Entry 41 example: hook diagonal depth bifurcation.

Prints the depth table for hook lam_d = (2,1^(d-2)), d=3..10.
Columns N=1,2 are fast (char tables <=20); N=3 is slow for d>=8 (marked).

Usage:
    py -m examples.run_hook_depth
"""

from pnp_lab.gct_kronecker.hook_depth import summary

if __name__ == "__main__":
    # N_max=2 only — N=3 requires char_table(24..27) and takes minutes
    summary(d_min=3, d_max=10, N_max=2)
    print()
    print("Anchors (slow, precomputed):")
    print("  d=8 N=3: g(3*lam_8, 3*lam_8, 3*lam_8) = 1646  (HOLE: depth=3)")
    print("  d=9 N=3: g(3*lam_9, 3*lam_9, 3*lam_9) = 1209  (HOLE: depth=3)")
    print("  d=13 N=2: g(2*lam_13, ...) = 0  (depth>2 holds at 6th data point)")
