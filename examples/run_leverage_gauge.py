"""Module 27 — is the cross-level leverage trend GAUGE-INVARIANT?

Settles Module 24's open flag ("abs decays / rel grows" => leverage ill-posed) on the
consistent Module-26 iso-hardness series.  For each H slice it builds the 3-level rows
(n=4 exact, n=5,6 sampled CRN) and runs the exact gauge post-analysis: do the absolute
(alpha=0) and relative (alpha=1) trends AGREE, so the n=5 peak holds for every alpha in
[0,1]?  And is the decisive flip exponent alpha*_{5->6} > 1, robustly under sampling
error?

Run:  py examples/run_leverage_gauge.py
"""

from pnp_lab.meta_complexity import sampled_order_n5 as s5


def main() -> None:
    for H in (0.5, 0.2):
        v = s5.leverage_gauge_table(H_target=H, seeds=6, M=120000)
        print(f"\n=== H_target = {H} ===")
        for p in v.pairs:
            print(f"  {p.n_lo}->{p.n_hi}:  Delta_abs(a=0) = {p.delta_abs:+.4f}   "
                  f"Delta_rel(a=1) = {p.delta_rel:+.4f}   alpha* = {p.alpha_star:+.3f}   "
                  f"same_sign = {p.same_sign}")
        print(f"  peak level by alpha: {v.peak_n_by_alpha}")
        print(f"  gauge_invariant_peak = {v.gauge_invariant_peak}")
        print(f"  alpha*_(5->6) = {v.alpha_star_5_6:.3f}   "
              f"p_killer = P(alpha*<=1) = {v.p_killer:.4f}   "
              f"killer_fires = {v.killer_fires}   PASS = {v.passes}")


if __name__ == "__main__":
    main()
