"""Approximate degree (6th arena) — exact tests via the dual-polynomial LP.

Anchors (deterministic, exact): parity = full degree n, constants = 0, dictator = 1; the
exhaustive n=3 reduce-to-known (adeg collapses into the joint orbit-invariant dictionary).
"""

from fractions import Fraction

import pytest

from pnp_lab.approx_degree import adeg as A


def _parity_tt(n: int) -> int:
    return sum((bin(x).count("1") % 2) << x for x in range(1 << n))


def _or_tt(n: int) -> int:
    return sum((1 if x else 0) << x for x in range(1 << n))


# ── anchors: exact known approximate degrees ───────────────────────────────

def test_constants_have_degree_zero():
    assert A.approx_degree(0b00, 1) == 0           # const 0
    assert A.approx_degree(0b11, 1) == 0           # const 1


def test_dictator_has_degree_one():
    assert A.approx_degree(0b10, 1) == 1           # f(x)=x0
    assert A.approx_degree(0b1010, 2) == 1         # f(x)=x0 on 2 vars


def test_parity_has_full_degree():
    """Parity is the hardest: adeg = n (it needs the full-degree monomial)."""
    assert A.approx_degree(_parity_tt(2), 2) == 2
    assert A.approx_degree(_parity_tt(3), 3) == 3


def test_error_decreases_and_vanishes_at_full_degree():
    tt = _or_tt(3)
    errs = [A.error_degree_d(tt, 3, d) for d in range(4)]
    assert errs[0] == Fraction(1, 2)               # non-constant: E_0 = 1/2
    assert all(errs[i] >= errs[i + 1] for i in range(3))   # monotone non-increasing
    assert errs[3] == 0                            # full degree interpolates exactly


def test_chi_and_monomials():
    assert A.chi(0b101, 0b111) == 1                # S={0,2} subset of support {0,1,2}
    assert A.chi(0b101, 0b011) == 0               # bit 2 missing
    assert sorted(A.monomial_masks(2, 1)) == [0b00, 0b01, 0b10]   # deg<=1: {}, {0}, {1}


# ── the decisive reduce-to-known (exhaustive n=3) ──────────────────────────

def test_adeg_crosscuts_cost_but_collapses_into_joint_dictionary():
    """adeg is INCOMPARABLE with formula-size cost alone (neither refines the other) — a
    genuine fact — yet it is RECONSTRUCTIBLE from the joint orbit-invariant dictionary
    (cost, gf2_degree, sensitivity, block_sensitivity) on n=3: it separates no pair those
    four agree on.  RESTATEMENT-of-known, the 6th-arena collapse."""
    _, refines, crefines = A.adeg_vs_cost(3)
    assert not refines and not crefines            # adeg ⊥ cost (cross-cutting)
    reconstructible, splits = A.adeg_vs_dictionary(3)
    assert reconstructible and splits == []        # but inside the joint dictionary


@pytest.mark.slow
def test_adeg_distribution_n3():
    """The frozen exhaustive distribution at n=3 (256 functions)."""
    from collections import Counter
    dist = dict(sorted(Counter(A.adeg_table(3).values()).items()))
    assert dist == {0: 2, 1: 102, 2: 134, 3: 18}
