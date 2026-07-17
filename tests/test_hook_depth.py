"""Tests for pnp_lab.gct_kronecker.hook_depth (Entry 41).

Tests are split by compute cost:
  - Fast (no marker):    d <= 8 at N=2 (char tables <=16, all < 1s)
  - Moderate (no mark):  d=9,10 at N=2 (tables 18,20; ~10s each in fresh process)
  - Slow (marked):       d=11..13 at N=2, d=8,9 at N=3 (tables 22-27; 24-272s)

All assertions are EXACT integers (no floats, no approximations).
"""

from __future__ import annotations

import pytest

from pnp_lab.gct_kronecker.hook_depth import g_hook_diag, hook_lam, hook_depth_row, HOOK_MAX_D


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
