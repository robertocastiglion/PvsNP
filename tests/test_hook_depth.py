"""Tests for pnp_lab.gct_kronecker.hook_depth (Entry 41).

Tests are split by compute cost:
  - Fast (no marker):    d <= 8 at N=2 (char tables <=16, all < 1s)
  - Moderate (no mark):  d=9,10 at N=2 (tables 18,20; ~10s each in fresh process)
  - Slow (marked):       d=11..13 at N=2, d=8,9 at N=3 (tables 22-27; 24-272s)

All assertions are EXACT integers (no floats, no approximations).
"""

from __future__ import annotations

import pytest

from pnp_lab.gct_kronecker.hook_depth import (
    g_hook_diag, hook_lam, hook_depth_row, HOOK_MAX_D,
    predicted_d0, predicted_T, last_hole_value,
    fat_hook_lam, fat_hook_diag, predicted_fat_d0,
)


# ---------------------------------------------------------------------------
# hook_lam sanity
# ---------------------------------------------------------------------------

def test_hook_lam_basic():
    assert hook_lam(2) == (2,)
    assert hook_lam(3) == (2, 1)
    assert hook_lam(5) == (2, 1, 1, 1)
    assert hook_lam(8) == (2, 1, 1, 1, 1, 1, 1)


def test_hook_lam_sum():
    for d in range(2, 15):
        assert sum(hook_lam(d)) == d, f"sum(hook_lam({d})) != {d}"


# ---------------------------------------------------------------------------
# N=1: g(lam_d) for small d (all fast)
# ---------------------------------------------------------------------------

def test_n1_positive_d3_d4():
    """g(lam_3) = 1, g(lam_4) = 1: NOT zeros at N=1."""
    assert g_hook_diag(3, 1) == 1, "g(lam_3) should be 1"
    assert g_hook_diag(4, 1) == 1, "g(lam_4) should be 1"


def test_n1_zero_d5_to_8():
    """g(lam_d) = 0 for d=5..8 (from diagonal census)."""
    for d in range(5, 9):
        g = g_hook_diag(d, 1)
        assert g == 0, f"d={d}: g(lam_d, lam_d, lam_d) = {g}, expected 0"


# ---------------------------------------------------------------------------
# N=2: HOLE at d=5,6,7; ZERO (uncovered) at d=8 (all fast, tables <=16)
# ---------------------------------------------------------------------------

def test_n2_hole_d5():
    """g(2*lam_5) = 10: HOLE (depth=2 for d=5)."""
    assert g_hook_diag(5, 2) == 10


def test_n2_hole_d6():
    """g(2*lam_6) = 9: HOLE (depth=2 for d=6)."""
    assert g_hook_diag(6, 2) == 9


def test_n2_hole_d7():
    """g(2*lam_7) = 2: HOLE (depth=2 for d=7)."""
    assert g_hook_diag(7, 2) == 2


def test_n2_zero_d8():
    """g(2*lam_8) = 0: key threshold — depth > 2 for d=8. char_table(16) fast."""
    assert g_hook_diag(8, 2) == 0


def test_n2_zero_d9():
    """g(2*lam_9) = 0: depth > 2 for d=9. char_table(18) ~10s."""
    assert g_hook_diag(9, 2) == 0


def test_n2_zero_d10():
    """g(2*lam_10) = 0: depth > 2 for d=10. char_table(20) ~9s."""
    assert g_hook_diag(10, 2) == 0


@pytest.mark.slow
def test_n2_zero_d11():
    """g(2*lam_11) = 0: depth > 2 for d=11. char_table(22) ~24s."""
    assert g_hook_diag(11, 2) == 0


@pytest.mark.slow
def test_n2_zero_d12():
    """g(2*lam_12) = 0: depth > 2 for d=12. char_table(24) ~58s."""
    assert g_hook_diag(12, 2) == 0


@pytest.mark.slow
def test_n2_zero_d13():
    """g(2*lam_13) = 0: depth > 2 for d=13. char_table(26) ~173s.
    HOOK_MAX_D=27 >= 26, so this is feasible (but slow)."""
    assert g_hook_diag(13, 2) == 0  # 13*2=26 <= HOOK_MAX_D=27


# ---------------------------------------------------------------------------
# N=3: confirm HOLE (depth=3) for d=8 and d=9
# ---------------------------------------------------------------------------

@pytest.mark.slow
def test_n3_hole_d8():
    """g(3*lam_8) = 1646: confirms depth=3 for d=8. char_table(24) ~58s."""
    assert g_hook_diag(8, 3) == 1646


@pytest.mark.slow
def test_n3_hole_d9():
    """g(3*lam_9) = 1209: confirms depth=3 for d=9. char_table(27) ~272s."""
    assert g_hook_diag(9, 3) == 1209


# ---------------------------------------------------------------------------
# Infeasibility boundary
# ---------------------------------------------------------------------------

def test_infeasibility_large_d():
    """d*N > HOOK_MAX_D=27 => g_hook_diag returns None (wall)."""
    # d=14, N=2: 28 > 27 => None
    assert g_hook_diag(14, 2) is None
    # d=9, N=4: 36 > 27 => None
    assert g_hook_diag(9, 4) is None


# ---------------------------------------------------------------------------
# hook_depth_row: depth bifurcation
# ---------------------------------------------------------------------------

def test_depth_row_d5_depth2():
    """d=5: values=[0, 10], depth=2."""
    row = hook_depth_row(5, N_max=2)
    assert row["values"] == [0, 10], f"d=5 values={row['values']}"
    assert row["depth"] == 2


def test_depth_row_d7_depth2():
    """d=7: values=[0, 2], depth=2."""
    row = hook_depth_row(7, N_max=2)
    assert row["values"] == [0, 2], f"d=7 values={row['values']}"
    assert row["depth"] == 2


def test_depth_row_d8_no_depth_at_n2():
    """d=8: values=[0, 0], depth=None (not found within N_max=2)."""
    row = hook_depth_row(8, N_max=2)
    assert row["values"] == [0, 0], f"d=8 values={row['values']}"
    assert row["depth"] is None, f"d=8 depth={row['depth']} (expected None)"


def test_threshold_at_d8():
    """Depth bifurcation: d=5,6,7 have depth=2; d=8 has depth>2."""
    for d in [5, 6, 7]:
        row = hook_depth_row(d, N_max=2)
        assert row["depth"] == 2, f"d={d}: depth={row['depth']} (expected 2)"
    row8 = hook_depth_row(8, N_max=2)
    assert row8["depth"] is None, f"d=8 depth={row8['depth']} (expected None/depth>2)"


# ---------------------------------------------------------------------------
# Entry 42: Threshold conjecture d_0(a)=3a-1 and T(a)=3a+2
# ---------------------------------------------------------------------------

def test_predicted_d0_formula():
    """predicted_d0(a) = 3a-1 for a=1..5."""
    expected = {1: 2, 2: 5, 3: 8, 4: 11, 5: 14}
    for a, d0 in expected.items():
        assert predicted_d0(a) == d0, f"predicted_d0({a})={predicted_d0(a)}, expected {d0}"


def test_predicted_T_formula():
    """predicted_T(a) = 3a+2 for a=1..5."""
    expected = {1: 5, 2: 8, 3: 11, 4: 14, 5: 17}
    for a, T in expected.items():
        assert predicted_T(a) == T, f"predicted_T({a})={predicted_T(a)}, expected {T}"


def test_last_hole_value_formula():
    """last_hole_value(a) = a for a=1..5."""
    for a in range(1, 6):
        assert last_hole_value(a) == a


def test_d0_a2_verified():
    """d_0(2)=5: first zero at d=5 for hook (2,1^3), none at d=4."""
    assert g_hook_diag(4, 1) == 1, "g(lam_4)>0 (d<d_0)"
    assert g_hook_diag(5, 1) == 0, "g(lam_5)=0 (d=d_0(2)=5)"


def test_d0_a3_verified():
    """d_0(3)=8: first zero at d=8 for hook (3,1^5), none at d=7."""
    # Hook (3,1^4) |- 7: g>0 (d < d_0(3))
    lam7 = (3, 1, 1, 1, 1)
    assert g_fast_or_gfast(lam7) == 1, "g((3,1^4)^3) should be 1"
    # Hook (3,1^5) |- 8: g=0 (d = d_0(3)=8)
    lam8 = (3, 1, 1, 1, 1, 1)
    assert g_fast_or_gfast(lam8) == 0, "g((3,1^5)^3) should be 0"


def test_d0_a4_verified():
    """d_0(4)=11: first zero at d=11 for hook (4,1^7), none at d=10."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam10 = (4,) + (1,)*6  # (4,1^6) |- 10
    assert g_fast(lam10, lam10, lam10) == 1, "g((4,1^6)^3) should be 1"
    lam11 = (4,) + (1,)*7  # (4,1^7) |- 11
    assert g_fast(lam11, lam11, lam11) == 0, "g((4,1^7)^3) should be 0"


def test_d0_a5_verified():
    """d_0(5)=14: first zero at d=14 for hook (5,1^9), none at d=13."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam13 = (5,) + (1,)*8  # (5,1^8) |- 13
    assert g_fast(lam13, lam13, lam13) == 1, "g((5,1^8)^3) should be 1"
    lam14 = (5,) + (1,)*9  # (5,1^9) |- 14
    assert g_fast(lam14, lam14, lam14) == 0, "g((5,1^9)^3) should be 0"


def test_T_a1_verified():
    """T(1)=5: g((2^5),(2^5),(2^5))=0 (first vanish); g((2^4))=1=a=1."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam4 = (2, 2, 2, 2)  # 2*(1^4)
    lam5 = (2, 2, 2, 2, 2)  # 2*(1^5)
    assert g_fast(lam4, lam4, lam4) == 1, "g((2^4)^3) = 1 = a = last_hole"
    assert g_fast(lam5, lam5, lam5) == 0, "g((2^5)^3) = 0 = T(1)=5 threshold"


def test_last_hole_a1():
    """Last hole for a=1: g((2^4)^3) = 1 = a = last_hole_value(1)."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam = (2, 2, 2, 2)
    assert g_fast(lam, lam, lam) == last_hole_value(1), "last hole for a=1 should be 1"


def test_last_hole_a2():
    """Last hole for a=2: g(2*(2,1^5)^3) = 2 = a = last_hole_value(2)."""
    assert g_hook_diag(7, 2) == last_hole_value(2), "last hole for a=2 should be 2"


def test_last_hole_a3():
    """Last hole for a=3: g(2*(3,1^7)^3) = 3 = a = last_hole_value(3)."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam = (3,) + (1,)*7  # (3,1^7) |- 10 = T(3)-1
    lam2 = tuple(2*x for x in lam)  # (6,2^7) |- 20
    assert g_fast(lam2, lam2, lam2) == last_hole_value(3), "last hole for a=3 should be 3"


@pytest.mark.slow
def test_last_hole_a4():
    """Last hole for a=4: g(2*(4,1^9)^3) = 4 = a. char_table(26) ~161s."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam = (4,) + (1,)*9   # (4,1^9) |- 13 = T(4)-1=14-1
    lam2 = tuple(2*x for x in lam)  # (8,2^9) |- 26
    assert g_fast(lam2, lam2, lam2) == last_hole_value(4), "last hole for a=4 should be 4"


# ---------------------------------------------------------------------------
# Entry 42 addendum: d_0(6)=17; g(lam_{3a-2})=1 for ALL a=1..6
# ---------------------------------------------------------------------------

def test_d0_a6_verified():
    """d_0(6)=17: first zero at d=17 for hook (6,1^11), none at d=16."""
    from pnp_lab.gct_kronecker.fast import g_fast
    lam16 = (6,) + (1,)*10  # (6,1^10) |- 16 = 3*6-2
    lam17 = (6,) + (1,)*11  # (6,1^11) |- 17 = 3*6-1 = d_0(6)
    assert g_fast(lam16, lam16, lam16) == 1, "g((6,1^10)^3) should be 1"
    assert g_fast(lam17, lam17, lam17) == 0, "g((6,1^11)^3) should be 0 (d=d_0(6)=17)"


def test_g_at_d0_minus1_equals_1():
    """g(lam_{3a-2}^3)=1 for ALL a=1..6: value just before first zero is always 1."""
    from pnp_lab.gct_kronecker.fast import g_fast
    expected_one = {
        1: (2,),             # (2,) |- 1 = 3*1-2 [d_0=2]
        2: (2, 1, 1),        # (2,1^2) |- 4 = 3*2-2 [d_0=5]
        3: (3, 1, 1, 1, 1),  # (3,1^4) |- 7 = 3*3-2 [d_0=8]
        4: (4,) + (1,)*6,    # (4,1^6) |- 10 = 3*4-2 [d_0=11]
        5: (5,) + (1,)*8,    # (5,1^8) |- 13 = 3*5-2 [d_0=14]
        6: (6,) + (1,)*10,   # (6,1^10) |- 16 = 3*6-2 [d_0=17]
    }
    for a, lam in expected_one.items():
        g = g_fast(lam, lam, lam)
        assert g == 1, f"a={a}: g(lam_{{3a-2}})={g}, expected 1"


# ---------------------------------------------------------------------------
# Entry 44: Fat-hook d_0(a, b=2) = 3a+4 and slope-3 universality
# ---------------------------------------------------------------------------

def test_fat_hook_lam_basic():
    """fat_hook_lam shape sanity."""
    assert fat_hook_lam(3, 2, 1) == (3, 2)
    assert fat_hook_lam(4, 2, 3) == (4, 2, 2, 2)
    assert fat_hook_lam(5, 3, 2) == (5, 3, 3)
    # Sum = a + b*k
    for a, b, k in [(3, 2, 2), (4, 2, 4), (5, 3, 3)]:
        lam = fat_hook_lam(a, b, k)
        assert sum(lam) == a + b * k


def test_predicted_fat_d0_b1():
    """predicted_fat_d0(a, 1) == 3a-1 (same as predicted_d0)."""
    for a in range(1, 7):
        assert predicted_fat_d0(a, 1) == 3 * a - 1 == predicted_d0(a)


def test_predicted_fat_d0_b2():
    """predicted_fat_d0(a, 2) == 3a+4 for a=2..6 (C44)."""
    expected = {2: 10, 3: 13, 4: 16, 5: 19, 6: 22}
    for a, d0 in expected.items():
        assert predicted_fat_d0(a, 2) == d0, f"a={a}: {predicted_fat_d0(a, 2)} != {d0}"


def test_predicted_fat_d0_unknown_b():
    """predicted_fat_d0 returns None for b not in {1,2}."""
    assert predicted_fat_d0(4, 3) is None


def test_fat_d0_a2_b2_verified():
    """d_0(2,b=2)=10: g((2,2^3)^3)=1>0, g((2,2^4)^3)=0."""
    assert fat_hook_diag(2, 2, 3) == 1  # d=8, g>0
    assert fat_hook_diag(2, 2, 4) == 0  # d=10, first zero


def test_fat_d0_a3_b2_verified():
    """d_0(3,b=2)=13: g((3,2^4)^3)=1>0, g((3,2^5)^3)=0."""
    assert fat_hook_diag(3, 2, 4) == 1  # d=11, g>0
    assert fat_hook_diag(3, 2, 5) == 0  # d=13, first zero


def test_fat_d0_a4_b2_verified():
    """d_0(4,b=2)=16: g((4,2^5)^3)=2>0, g((4,2^6)^3)=0."""
    assert fat_hook_diag(4, 2, 5) == 2  # d=14, g>0
    assert fat_hook_diag(4, 2, 6) == 0  # d=16, first zero


def test_fat_d0_a5_b2_verified():
    """d_0(5,b=2)=19: g((5,2^6)^3)=2>0, g((5,2^7)^3)=0."""
    assert fat_hook_diag(5, 2, 6) == 2  # d=17, g>0
    assert fat_hook_diag(5, 2, 7) == 0  # d=19, first zero


@pytest.mark.slow
def test_fat_d0_a6_b2_verified():
    """d_0(6,b=2)=22: g((6,2^7)^3)=3>0, g((6,2^8)^3)=0. char_table(22) ~24s."""
    assert fat_hook_diag(6, 2, 7) == 3  # d=20, g>0
    assert fat_hook_diag(6, 2, 8) == 0  # d=22, first zero


def test_slope3_universality():
    """Slope-3 in a: d_0(a,1)=3a-1 and d_0(a,2)=3a+4 differ by 5 (constant)."""
    for a in range(2, 7):
        d0_b1 = predicted_fat_d0(a, 1)
        d0_b2 = predicted_fat_d0(a, 2)
        assert d0_b2 - d0_b1 == 5, f"a={a}: offset={d0_b2-d0_b1} (expected 5)"


def test_fat_hook_infeasibility():
    """fat_hook_diag returns None when d > HOOK_MAX_D=27."""
    assert fat_hook_diag(10, 2, 10) is None  # d=10+20=30 > 27
    assert fat_hook_diag(6, 2, 12) is None  # d=6+24=30 > 27
    assert fat_hook_diag(4, 3, 9) is None   # d=4+27=31 > 27


def g_fast_or_gfast(lam):
    """Helper: g_fast(lam, lam, lam)."""
    from pnp_lab.gct_kronecker.fast import g_fast
    return g_fast(lam, lam, lam)
