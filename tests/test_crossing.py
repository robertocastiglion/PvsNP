"""Test esatti per pnp_lab/gct_kronecker/crossing.py — H65.

Strategia test-first:
  - Valori noti (Entry 64/baseline): d=13 → 2 shape 3-hook; d=21 → crossing
    tra {13,7,1} R<1 e {15,5,1} R>1 con s*~0.580.
  - Predizioni H65: d=23,25,27 con s* in [0.55,0.62]; |Delta s*| decrescente;
    a d=25 almeno un punto con R>1 e uno con R<1.
  - I calcoli g_fast per d<=21 terminano in secondi; d=23/25/27 marcati slow.
"""

from __future__ import annotations

import pytest
from fractions import Fraction

from pnp_lab.gct_kronecker.crossing import (
    enum_sc3hook,
    sc_partition_from_hooks,
    frame_robinson_thrall,
    compute_crossing,
    delta_s_star,
)
from pnp_lab.gct_kronecker.fast import g_fast


# ---------------------------------------------------------------------------
# Test strutturali (veloci)
# ---------------------------------------------------------------------------

class TestScPartitionFromHooks:
    """Verifica la costruzione partizione self-conjugate da hook diagonali."""

    def test_hooks_5_3_1(self):
        # d=9: (5,3,1) -> partizione self-conjugate di 9
        lam = sc_partition_from_hooks(5, 3, 1)
        assert sum(lam) == 9
        # self-conjugate: lam = conjugate(lam)
        conj = _conjugate(lam)
        assert lam == conj

    def test_hooks_7_3_1(self):
        # d=11
        lam = sc_partition_from_hooks(7, 3, 1)
        assert sum(lam) == 11
        assert lam == _conjugate(lam)

    def test_hooks_9_3_1(self):
        # d=13
        lam = sc_partition_from_hooks(9, 3, 1)
        assert sum(lam) == 13
        assert lam == _conjugate(lam)

    def test_hooks_7_5_1(self):
        # d=13
        lam = sc_partition_from_hooks(7, 5, 1)
        assert sum(lam) == 13
        assert lam == _conjugate(lam)

    def test_hooks_13_7_1(self):
        # d=21: baseline nota
        lam = sc_partition_from_hooks(13, 7, 1)
        assert sum(lam) == 21
        assert lam == _conjugate(lam)

    def test_hooks_15_5_1(self):
        # d=21: baseline nota
        lam = sc_partition_from_hooks(15, 5, 1)
        assert sum(lam) == 21
        assert lam == _conjugate(lam)


class TestEnumD13:
    """d=13: attesi esattamente 2 shape 3-hook (Entry 64 baseline)."""

    def test_count(self):
        pts = enum_sc3hook(13)
        assert len(pts) == 2, f"Attesi 2 punti a d=13, trovati {len(pts)}: {pts}"

    def test_hooks_correct(self):
        pts = enum_sc3hook(13)
        hook_sets = {p[0] for p in pts}
        assert (9, 3, 1) in hook_sets
        assert (7, 5, 1) in hook_sets

    def test_d_even_empty(self):
        assert enum_sc3hook(12) == []
        assert enum_sc3hook(14) == []
        assert enum_sc3hook(24) == []

    def test_d_small_empty(self):
        assert enum_sc3hook(3) == []  # d<5
        assert enum_sc3hook(1) == []


class TestRExact_D21:
    """Verifica i valori R esatti a d=21 (baseline H65)."""

    def test_shape_13_7_1_R_lt_1(self):
        """(h1,h2,h3)=(13,7,1): R deve essere <1, ~0.9967 secondo baseline."""
        pts = enum_sc3hook(21)
        found = {p[0]: p for p in pts}
        assert (13, 7, 1) in found, f"Shape (13,7,1) non trovata in {list(found.keys())}"
        hooks, lam, s, R = found[(13, 7, 1)]
        # R esatto come Fraction, confrontato con range
        assert R < 1, f"Atteso R<1 per (13,7,1), trovato R={R} = {float(R):.6f}"
        assert R > Fraction(99, 100), f"R troppo basso: {float(R):.6f}"

    def test_shape_15_5_1_R_gt_1(self):
        """(h1,h2,h3)=(15,5,1): R deve essere >1, ~1.0352 secondo baseline."""
        pts = enum_sc3hook(21)
        found = {p[0]: p for p in pts}
        assert (15, 5, 1) in found, f"Shape (15,5,1) non trovata in {list(found.keys())}"
        hooks, lam, s, R = found[(15, 5, 1)]
        assert R > 1, f"Atteso R>1 per (15,5,1), trovato R={R} = {float(R):.6f}"
        assert R < Fraction(11, 10), f"R troppo alto: {float(R):.6f}"

    def test_spread_13_7_1(self):
        """Spread s = (13-1)/21 = 12/21 = 4/7 ~ 0.5714."""
        pts = enum_sc3hook(21)
        found = {p[0]: p for p in pts}
        _, _, s, _ = found[(13, 7, 1)]
        assert s == Fraction(12, 21), f"Spread atteso 12/21, trovato {s}"

    def test_spread_15_5_1(self):
        """Spread s = (15-1)/21 = 14/21 = 2/3 ~ 0.6667."""
        pts = enum_sc3hook(21)
        found = {p[0]: p for p in pts}
        _, _, s, _ = found[(15, 5, 1)]
        assert s == Fraction(14, 21), f"Spread atteso 14/21, trovato {s}"


class TestCrossingD21:
    """Crossing s*(21) ~ 0.580 (baseline)."""

    def test_crossing_exists(self):
        c = compute_crossing(21)
        assert c is not None, "s*(21) non trovato"

    def test_crossing_range(self):
        c = compute_crossing(21)
        assert c is not None
        fc = float(c)
        assert 0.55 <= fc <= 0.62, f"s*(21) = {fc:.4f} fuori da [0.55, 0.62]"

    def test_crossing_approx_580(self):
        """Baseline: s*(21) ~ 0.580."""
        c = compute_crossing(21)
        assert c is not None
        assert abs(float(c) - 0.580) < 0.01, f"s*(21) = {float(c):.4f}, atteso ~0.580"

    def test_d15_no_crossing(self):
        """d=15: max R=0.9924 < 1, nessun crossing (baseline)."""
        c = compute_crossing(15)
        assert c is None, f"s*(15) atteso None, trovato {c}"


# ---------------------------------------------------------------------------
# Test predizioni H65 — marcati slow (g_fast su d=23,25,27)
# ---------------------------------------------------------------------------

@pytest.mark.slow
@pytest.mark.timeout(300)
class TestCrossingD23:
    def test_crossing_exists(self):
        c = compute_crossing(23)
        assert c is not None, "s*(23) non trovato"

    def test_crossing_range(self):
        c = compute_crossing(23)
        fc = float(c)
        assert 0.55 <= fc <= 0.62, f"s*(23) = {fc:.4f} fuori da [0.55, 0.62]"


@pytest.mark.slow
@pytest.mark.timeout(600)
class TestCrossingD25:
    def test_crossing_exists(self):
        c = compute_crossing(25)
        assert c is not None, "s*(25) non trovato"

    def test_crossing_range(self):
        c = compute_crossing(25)
        fc = float(c)
        assert 0.50 <= fc <= 0.65, f"s*(25) = {fc:.4f} fuori da [0.50, 0.65]"

    def test_range_tight(self):
        c = compute_crossing(25)
        fc = float(c)
        assert 0.55 <= fc <= 0.61, f"s*(25) = {fc:.4f} fuori da [0.55, 0.61] (H65)"

    def test_both_sides_of_1(self):
        """A d=25 deve esistere almeno un punto con R>1 e uno con R<1."""
        pts = enum_sc3hook(25)
        Rs = [float(p[3]) for p in pts]
        assert any(r > 1 for r in Rs), f"Nessun R>1 a d=25; Rs={Rs}"
        assert any(r < 1 for r in Rs), f"Nessun R<1 a d=25; Rs={Rs}"


@pytest.mark.slow
@pytest.mark.timeout(600)
class TestCrossingD27:
    def test_crossing_range(self):
        c = compute_crossing(27)
        if c is not None:
            fc = float(c)
            assert 0.55 <= fc <= 0.60, f"s*(27) = {fc:.4f} fuori da [0.55, 0.60]"


@pytest.mark.slow
@pytest.mark.timeout(1200)
def test_delta_monotone():
    """|Delta s*| deve essere monotona decrescente su 13->21->23->25->27."""
    d_list = [13, 21, 23, 25, 27]
    crossings = [compute_crossing(d) for d in d_list]
    # Filtra None
    valid = [(d, c) for d, c in zip(d_list, crossings) if c is not None]
    assert len(valid) >= 3, f"Troppo pochi crossing validi: {valid}"
    deltas = [abs(float(valid[i+1][1]) - float(valid[i][1])) for i in range(len(valid)-1)]
    for i in range(len(deltas) - 1):
        assert deltas[i+1] <= deltas[i] + 1e-9, (
            f"|Delta s*| non monotona: {deltas}"
        )
    assert deltas[-1] < 0.02, f"Ultimo |Delta s*| = {deltas[-1]:.4f} >= 0.02"


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _conjugate(lam):
    """Coniugata della partizione lam."""
    if not lam:
        return ()
    max_len = lam[0]
    return tuple(sum(1 for r in lam if r > j) for j in range(max_len))
