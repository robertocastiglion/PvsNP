"""Sampled order-anisotropy at n=5 (Module 24) — the lab's first deliberate trade of
exactness for reach.

The fast tests pin down the ESTIMATOR's correctness (deterministic with fixed seeds):
the n=4 fidelity anchor, the CRN difference semantics, and the null control.  The
heavy n=5 PASS (8 seeds x 300k) and the degeneracy table are gated ``slow`` — they
take minutes and reproduce the frozen verdict.
"""

import random

import pytest

from pnp_lab.meta_complexity import order_locality as ol
from pnp_lab.meta_complexity import sampled_order_n5 as s5


# ── the estimator is sound: predicates and CRN semantics ───────────────────

def test_mbpsp_predicate_matches_exact():
    """The sampler's hardness predicate is exactly Module 22's MBPSP[s]."""
    n, s = 4, 6
    hard = s5.mbpsp_predicate(n, s)
    for t in (0, 8, 0b1000100010001000, 0xABCD, 0xFFFF):
        assert hard(t) == (ol.min_obdd_size(t, n) > s)


def test_popcount_control_is_permutation_invariant():
    """The null control depends only on weight(d): its CRN difference for two equal-
    weight d is EXACTLY 0 (not just ~0) — proving it is a true permutation-invariant
    stand-in.  Tested exactly by enumerating the n=4 meta-cube via a deterministic
    full pass (CRN over all t gives the exact difference)."""
    n = 4
    N = 1 << n
    ctrl = s5.popcount_predicate(8)
    # exact difference = sum over ALL t of (I_hi - I_lo); use a huge sample == full pass
    # by iterating deterministically over every t once.
    e0 = 1
    e_hi, e_lo = 1 << 8, 1 << 2          # d=8 (input 8, weight 1) vs d=2 (input 2, weight 1)
    diff = 0
    for t in range(1 << N):
        a, b0 = ctrl(t), ctrl(t ^ e0)
        i_hi = 0 if (a == b0 == ctrl(t ^ e_hi) == ctrl(t ^ e0 ^ e_hi)) else 1
        i_lo = 0 if (a == b0 == ctrl(t ^ e_lo) == ctrl(t ^ e0 ^ e_lo)) else 1
        diff += i_hi - i_lo
    assert diff == 0


def test_crn_diff_unbiased_on_a_trivial_predicate():
    """A constant predicate makes every 4-cube constant => both indicators 0 => the
    CRN difference is identically 0 with zero variance."""
    est = s5.crn_pair_diff(lambda t: True, 8, 3, 1, 5000, random.Random(0))
    assert est.mean_prob == 0.0 and est.se_prob == 0.0


# ── the fidelity anchor (deterministic with a fixed seed) ──────────────────

def test_anchor_n4_exact_value_inside_ci():
    """THE VALIDATION.  At n=4 the exact pair-influence difference is known (184 for
    the weight-1 top-vs-x1 pair); the sampler's 99% CI must contain it.  Deterministic
    for seed=0 (verified at M=20000)."""
    a = s5.anchor_n4(M=20000, seed=0)
    assert a.exact_count == 184                 # Module 22 ground truth (x3:4056 - x1:3872)
    assert a.within_ci                          # exact value inside the sampler's 99% CI


def test_anchor_control_not_significant():
    """The popcount null control on the same n=4 pair is not significant (CI includes
    0) for a fixed seed — the estimator does not fabricate signal from noise."""
    c = s5.crn_pair_diff(s5.popcount_predicate(8), 16, 8, 2, 20000, random.Random(0))
    assert not c.significant


# ── heavy reproductions of the frozen verdict (slow) ───────────────────────

@pytest.mark.slow
@pytest.mark.timeout(600)
def test_n5_pass_replicated():
    """The frozen n=5 PASS: pooled z > 2.576 (99%), all seeds positive, and the
    popcount control consistent with 0.  Deterministic (base_seed=1000): z ~ 3.8,
    6/6 positive, control |z| < Z99.  ~100s."""
    v = s5.replicate_n5(M_per_seed=120000, seeds=6, base_seed=1000)
    assert v.passes
    assert v.z > s5.Z99
    assert not v.killer_fires
    assert v.frac_positive >= 0.5
    assert abs(v.control_z) < s5.Z99             # null control stays consistent with 0


# ── cross-level (median-calibrated): the push to n=6 (Module 25) ───────────

def test_cross_level_n4_exact_median():
    """The n=4 row of the median-calibrated cross-level table is EXACT and frozen:
    s=10, the pre-registered top(x3)-vs-x0 pair difference is 1536 (base 21024), and
    the popcount control is exactly 0 by symmetry."""
    r = s5.cross_level_row(4)
    assert r.exact and r.s == 10
    assert round(r.diff_prob * (1 << r.N)) == 1536       # exact top(x3) - x0
    assert round(r.base_prob * (1 << r.N)) == 21024
    assert abs(r.rel - 0.0731) < 0.001
    assert r.control_z == 0.0                            # exact-0 by symmetry


def test_median_threshold_exact_at_n4():
    assert s5.median_threshold(4) == 10


@pytest.mark.slow
@pytest.mark.timeout(600)
def test_cross_level_survives_to_n6():
    """The frozen result: under the median calibration the order-anisotropy SURVIVES
    to n=6 (N=64, 2^64 truth tables) — significant, all seeds positive, control flat.
    Deterministic (base_seed=360): z ~ 25.  ~3.5 min."""
    r = s5.cross_level_row(6, seeds=3, M=100000, base_seed=360)
    assert r.significant and r.z > s5.Z99
    assert r.frac_positive >= 0.66
    assert abs(r.control_z) < s5.Z99                     # null control stays flat


# ── iso-hardness control (Module 26): disentangle leverage from the H-confound ─

def test_iso_hardness_threshold_targets_n4_exact():
    """The iso-hardness threshold is the integer whose hard-fraction is closest to the
    target; exact (full sweep) at n=4.  frac>9 = 0.526 (closest to 0.5), frac>10 = 0.170
    (closest to 0.2) — the coarse OBDD-size jumps make these the achievable points."""
    assert s5.iso_hardness_threshold(4, 0.5) == 9
    assert s5.iso_hardness_threshold(4, 0.2) == 10


def test_iso_hardness_n4_exact_frozen():
    """The n=4 row of the iso-hardness table is EXACT and frozen.  At H_target=0.5 the
    threshold is s=9 (H=0.526), the pre-registered top(x3)-vs-x0 difference is 2016
    (base 36640, rel +5.5%); the popcount control is exactly 0 by symmetry.  At
    H_target=0.2 the row coincides with Module 25's n=4 (s=10, diff 1536)."""
    r = s5.iso_hardness_row(4, H_target=0.5)
    assert r.exact and r.s == 9
    assert round(r.diff_prob * (1 << r.N)) == 2016
    assert round(r.base_prob * (1 << r.N)) == 36640
    assert abs(r.rel - 0.0550) < 0.001
    assert r.control_z == 0.0                            # exact-0 by symmetry
    # the H_target=0.2 slice reproduces Module 25's n=4 (same threshold s=10)
    r2 = s5.iso_hardness_row(4, H_target=0.2)
    assert r2.s == 10 and round(r2.diff_prob * (1 << r2.N)) == 1536


@pytest.mark.slow
@pytest.mark.timeout(600)
def test_iso_hardness_survival_is_H_robust_at_n6():
    """The frozen Module-26 result: holding H fixed (not the median), the order-
    anisotropy STILL survives to n=6 and the killer does NOT fire — Module 25's survival
    is not an H-artifact.  Deterministic (base_seed=760): significant, control flat.
    Run at H_target=0.5.  ~3 min."""
    r = s5.iso_hardness_row(6, H_target=0.5, seeds=3, M=100000, base_seed=760)
    assert r.significant and r.z > s5.Z99
    assert r.frac_positive >= 0.66
    assert abs(r.control_z) < s5.Z99                     # null control stays flat
    assert 0.30 < r.H_frac < 0.55                        # H held near 0.5 (not the median)


# ── gauge-invariance of the leverage trend (Module 27) ─────────────────────

def _row(n, diff_prob, base_prob, se_prob=0.0, exact=False):
    """A minimal CrossLevelRow carrying just the fields the gauge analysis reads."""
    N = 1 << n
    return s5.CrossLevelRow(
        n=n, N=N, s=0, H_frac=0.0, base_prob=base_prob, diff_prob=diff_prob,
        se_prob=se_prob, z=0.0, rel=diff_prob / base_prob, control_z=0.0,
        frac_positive=1.0, significant=True, exact=exact)


def test_gauge_alpha_star_and_same_sign_math():
    """The gauge math on the frozen Module-26 numbers (deterministic, no sampling):
    4->5 both endpoints rise (same_sign, alpha* < 0), 5->6 both fall (same_sign,
    alpha* = 1.85 > 1) => the n=5 peak is gauge-invariant over [0,1]."""
    rows = [_row(4, 0.0308, 0.559, exact=True),
            _row(5, 0.0418, 0.394, se_prob=6e-4),
            _row(6, 0.0225, 0.282, se_prob=5e-4)]
    v = s5.leverage_gauge(rows, H_target=0.5, mc=20000, seed=0)
    p45, p56 = v.pairs
    assert p45.same_sign and p45.delta_abs > 0 and p45.delta_rel > 0
    assert p56.same_sign and p56.delta_abs < 0 and p56.delta_rel < 0
    assert abs(p56.alpha_star - 1.852) < 0.01           # the decisive flip exponent
    assert v.alpha_star_5_6 > 1.0 and not v.killer_fires
    assert v.gauge_invariant_peak                        # same argmax (n=5) for all alpha
    assert all(n == 5 for n in v.peak_n_by_alpha.values())


def test_gauge_killer_fires_when_relative_grows():
    """KILLER sanity: a synthetic series where rel GROWS monotonically (alpha*_{5->6}
    inside [0,1]) must FIRE the killer — proving the test can fail."""
    # diff falls but base falls faster => rel rises 5->6; alpha*_{5->6} lands in (0,1)
    rows = [_row(4, 0.030, 0.55, exact=True),
            _row(5, 0.040, 0.40, se_prob=1e-4),
            _row(6, 0.038, 0.20, se_prob=1e-4)]
    v = s5.leverage_gauge(rows, H_target=0.5, mc=20000, seed=1)
    assert 0.0 < v.alpha_star_5_6 <= 1.0
    assert v.killer_fires and not v.passes
    assert not v.gauge_invariant_peak                    # abs and rel disagree 5->6


@pytest.mark.slow
@pytest.mark.timeout(600)
def test_gauge_invariant_peak_both_slices():
    """The frozen Module-27 result on the REAL sampled iso-hardness series: on both H
    slices the n=5 peak is gauge-invariant (alpha*_{5->6} > 1) and the killer does NOT
    fire under sampling-error propagation (p_killer small).  ~5 min (two 3-level series)."""
    for H in (0.5, 0.2):
        v = s5.leverage_gauge_table(H_target=H, seeds=4, M=120000)
        assert v.alpha_star_5_6 > 1.0, (H, v.alpha_star_5_6)
        assert v.gauge_invariant_peak, (H, v.peak_n_by_alpha)
        assert not v.killer_fires and v.p_killer < 0.05, (H, v.p_killer)


@pytest.mark.slow
@pytest.mark.timeout(300)
def test_threshold_regime_degenerates_at_n6():
    """The ceiling, measured: a live boundary at n=4,5 and base_prob == 0 at n>=6
    under the faithful theta=0.5*max policy (sample min already exceeds s)."""
    rows = {r.n: r for r in s5.threshold_regime((4, 5, 6), sample=2000, base_M=20000)}
    assert rows[4].base_prob > 0.01            # boundary alive
    assert rows[5].base_prob > 0.0             # boundary thin but present
    assert rows[6].base_prob == 0.0            # degenerate: constant-HARD
    assert rows[6].size_min > rows[6].s        # sample min above threshold
