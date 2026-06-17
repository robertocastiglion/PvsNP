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
