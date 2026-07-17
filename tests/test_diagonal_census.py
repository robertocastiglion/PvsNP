"""Test per pnp_lab.gct_kronecker.diagonal_census (Entry 40).

Tutti i test sono RAPIDI e deterministici (nessun float, nessun campionamento casuale).
La tavola dei caratteri viene memoizzata da g_fast -> character_table, quindi
chiamate ripetute sullo stesso d non ricomputano nulla.

Test inclusi:
  1. test_no_zeros_d1
  2. test_sign_rep_zeros
  3. test_two_row_zero
  4. test_hook_zero
  5. test_anchor_d9_residual
  6. test_all_zeros_d1_to_6_covered
  7. test_stretch_feasibility
  8. test_coverage_redundancy
"""

from __future__ import annotations

import pytest

from pnp_lab.gct_kronecker.fast import g_fast
from pnp_lab.gct_kronecker.kronecker import partitions
from pnp_lab.gct_kronecker.coverage import covered
from pnp_lab.gct_kronecker.diagonal_census import (
    diagonal_zeros,
    classify_diag,
    stretch_diagonal,
    STRETCH_MAX_D,
)


# ---------------------------------------------------------------------------
# 1. test_no_zeros_d1
# ---------------------------------------------------------------------------
def test_no_zeros_d1():
    """d=1: l'unica partizione e' (1,), g((1,),(1,),(1,))=1 (triviale), nessun zero."""
    ps = partitions(1)
    assert ps == [(1,)], f"partitions(1) inatteso: {ps}"
    g = g_fast((1,), (1,), (1,))
    assert g == 1, f"g((1,),(1,),(1,))={g}, atteso 1"
    zeros = diagonal_zeros(d_max=1)
    assert zeros == [], f"diagonal_zeros(1) dovrebbe essere vuota, ottenuto: {zeros}"


# ---------------------------------------------------------------------------
# 2. test_sign_rep_zeros
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", [2, 3, 4, 5, 6])
def test_sign_rep_zeros(d):
    """(1^d) ha g((1^d),(1^d),(1^d))=0 per d=2..6 e classify_diag restituisce 'sign'."""
    lam = tuple([1] * d)
    g = g_fast(lam, lam, lam)
    assert g == 0, f"d={d}: g(sign,sign,sign)={g}, atteso 0"
    cat = classify_diag(d, lam)
    assert cat == "sign", f"d={d}: classify_diag({lam})='{cat}', atteso 'sign'"


# ---------------------------------------------------------------------------
# 3. test_two_row_zero
# ---------------------------------------------------------------------------
def test_two_row_zero():
    """Esiste almeno una partizione two_row con g(lam,lam,lam)=0 a d<=10.
    Esempio noto: (3,3) a d=6 -> g=0, is_two_row=True."""
    found = None
    for d in range(1, 11):
        for lam in partitions(d):
            if g_fast(lam, lam, lam) == 0:
                cat = classify_diag(d, lam)
                if cat == "two_row":
                    found = (d, lam)
                    break
        if found:
            break
    assert found is not None, "Nessuna partizione two_row con g(lam,lam,lam)=0 trovata a d<=10"
    d, lam = found
    # Verifica diretta
    assert g_fast(lam, lam, lam) == 0
    assert classify_diag(d, lam) == "two_row"


# ---------------------------------------------------------------------------
# 4. test_hook_zero
# ---------------------------------------------------------------------------
def test_hook_zero():
    """Esiste almeno un hook lam (non two_row) con g(lam,lam,lam)=0 a d<=10.
    Esempio noto: (2,1,1,1) a d=5: hook, ell=4 > 2 (non two_row), g=0."""
    lam = (2, 1, 1, 1)
    d = sum(lam)  # 5
    g = g_fast(lam, lam, lam)
    assert g == 0, f"g({lam},{lam},{lam})={g}, atteso 0"
    cat = classify_diag(d, lam)
    assert cat == "hook", f"classify_diag(5, (2,1,1,1))='{cat}', atteso 'hook'"
    # Conferma che non e' two_row
    from pnp_lab.gct_kronecker.coverage import is_two_row, is_hook
    assert not is_two_row(lam), "(2,1,1,1) non dovrebbe essere two_row"
    assert is_hook(lam), "(2,1,1,1) dovrebbe essere hook"


# ---------------------------------------------------------------------------
# 5. test_anchor_d9_residual
# ---------------------------------------------------------------------------
def test_anchor_d9_residual():
    """Ancora documentata (Entry 34/40): lambda=(3,2,1,1,1,1), d=9.
    Requisiti:
      - g(lam,lam,lam) = 0
      - classify_diag(9, lam) = 'uncovered'
      - stretch_diagonal(lam, N=2) > 0  (HOLE: g(2lam,2lam,2lam)=14345)
    """
    lam = (3, 2, 1, 1, 1, 1)
    d = sum(lam)
    assert d == 9

    g = g_fast(lam, lam, lam)
    assert g == 0, f"g(lam,lam,lam)={g}, atteso 0"

    cat = classify_diag(d, lam)
    assert cat == "uncovered", f"classify_diag(9, {lam})='{cat}', atteso 'uncovered'"

    s = stretch_diagonal(lam, N=2)
    assert s is not None, "stretch_diagonal dovrebbe essere calcolabile (d*2=18 <= 18)"
    assert s > 0, f"stretch_diagonal(lam, 2)={s}, atteso > 0 (HOLE, valore noto: 14345)"
    # Valore esatto documentato
    assert s == 14345, f"stretch={s}, valore noto 14345"


# ---------------------------------------------------------------------------
# 6. test_all_zeros_d1_to_6_covered
# ---------------------------------------------------------------------------
def test_all_zeros_d1_to_6_covered():
    """Per d=1..6 TUTTI i vanishing diagonali hanno classify != 'uncovered'.
    Coerente con Entry 30: su d<=6 ogni zero e' coperto dalle famiglie note."""
    uncovered_found = []
    for d in range(1, 7):
        for lam in partitions(d):
            if g_fast(lam, lam, lam) == 0:
                cat = classify_diag(d, lam)
                if cat == "uncovered":
                    uncovered_found.append((d, lam, cat))
    assert uncovered_found == [], (
        f"Trovati {len(uncovered_found)} zeri 'uncovered' a d<=6 (atteso 0): "
        f"{uncovered_found}"
    )


# ---------------------------------------------------------------------------
# 7. test_stretch_feasibility
# ---------------------------------------------------------------------------
def test_stretch_feasibility():
    """stretch_diagonal:
      - lam=(10,): d=10, d*2=20 <= 24 => calcola un intero (non None)
      - lam=(13,): d=13, d*2=26 > 24 => None
    STRETCH_MAX_D aggiornato a 24 (character_table(24) fattibile in ~60s).
    """
    s10 = stretch_diagonal((10,), N=2)
    assert s10 is not None, f"stretch_diagonal((10,), 2) dovrebbe essere non-None (d*2=20<={STRETCH_MAX_D})"
    assert isinstance(s10, int), f"stretch dovrebbe essere int, ottenuto {type(s10)}"

    s13 = stretch_diagonal((13,), N=2)
    assert s13 is None, (
        f"stretch_diagonal((13,), 2) dovrebbe essere None (d*2=26>{STRETCH_MAX_D}), "
        f"ottenuto {s13}"
    )


# ---------------------------------------------------------------------------
# 8. test_coverage_redundancy
# ---------------------------------------------------------------------------
def test_coverage_redundancy():
    """Per ogni zero con categoria in {sign, two_row, hook, two_col,
    hook_conj, two_row_conj}, covered((lam,lam,lam)) deve essere True.

    Verifica che le categorie esplicite siano SOTTOINSIEMI di 'orbit_covered'
    (sanity check: le formule chiuse note coprono quelle forme).
    Eseguito su d=1..9 (< 1s con tavola memoizzata).
    """
    explicit_cats = {"sign", "two_row", "hook", "two_col", "hook_conj", "two_row_conj"}
    violations = []
    for d in range(1, 10):
        for lam in partitions(d):
            if g_fast(lam, lam, lam) == 0:
                cat = classify_diag(d, lam)
                if cat in explicit_cats:
                    if not covered((lam, lam, lam)):
                        violations.append((d, lam, cat))
    assert violations == [], (
        f"covered() = False per categorie esplicite (incoerenza): {violations}"
    )
