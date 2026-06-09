"""Test ESATTI per pattern_gap.py (ciclo 2): il primo gap di lift NON-J-I a 3 bit.

Veloci di default (outer sparsi a 3 bit -> matrici 8x8 con poche entrate-1, LP/cover
esatti in <1s ciascuno). Il censimento esaustivo delle 256 funzioni e' marcato `slow`.
"""

from __future__ import annotations

from fractions import Fraction

import pytest

from pnp_lab.exactness_composes.gap import as_matrix, cover_number, frac_cover, gstar
from pnp_lab.exactness_composes.pattern_gap import (
    all_3bit_outers,
    first_non_JI_gap,
    is_J_minus_I_up_to_perm,
    named_3bit_outers,
    pattern_matrix,
    truth_table_fn,
    _ones,
)


# --- il detector J - I -------------------------------------------------------

def test_is_JI_true_on_J_minus_I_4():
    M = as_matrix([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
    assert is_J_minus_I_up_to_perm(M)


def test_is_JI_true_under_row_col_perm():
    # J - I_4 con zeri spostati su un matching qualsiasi (perm di righe/colonne)
    M = as_matrix([[1, 0, 1, 1], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 1, 0]])
    assert is_J_minus_I_up_to_perm(M)


def test_is_JI_false_when_too_many_zeros():
    # adiacenza Q3 (ONE_IN_3): 40 zeri, non un matching -> non J - I
    M = pattern_matrix(named_3bit_outers()["ONE_IN_3"], 3)
    assert not is_J_minus_I_up_to_perm(M)


def test_is_JI_false_when_zeros_not_a_matching():
    # 4 zeri ma non un matching perfetto (due nella stessa riga)
    M = as_matrix([[0, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]])
    assert not is_J_minus_I_up_to_perm(M)


def test_OR2_lift_is_JI():
    # sanita': il controesempio storico (OR2 ∘ XOR^2) E' J - I_4
    f = lambda z: int(any(z))
    M = pattern_matrix(f, 2)  # = lift OR_2 ∘ XOR^2
    assert is_J_minus_I_up_to_perm(M)
    assert gstar(M) == 1


# --- il KILLER: ONE_IN_3 e' un gap non-J-I (adiacenza dell'ipercubo Q3) ------

def test_ONE_IN_3_is_nonJI_gap():
    M = pattern_matrix(named_3bit_outers()["ONE_IN_3"], 3)
    cov, lp = cover_number(M), frac_cover(M)
    assert _ones(M) == 24                 # 8 vertici x 3 spigoli = adiacenza Q3
    assert cov == 8
    assert lp == Fraction(6)
    assert cov - lp == Fraction(2)        # G* = 2, piu' grande del +1 di J-I
    assert not is_J_minus_I_up_to_perm(M)


def test_ONE_IN_3_matrix_is_Q3_adjacency():
    # M[x][y] = 1  <=>  Hamming(x XOR y) = 1  =  adiacenza dell'ipercubo a 3 dim
    M = pattern_matrix(named_3bit_outers()["ONE_IN_3"], 3)
    for x in range(8):
        for y in range(8):
            hw = bin(x ^ y).count("1")
            assert M[x][y] == (1 if hw == 1 else 0)


def test_NAE_is_nonJI_gap():
    # not-all-equal: zeri = I + diagonale inversa (16 zeri) -> G*=1 ma NON J-I
    M = pattern_matrix(named_3bit_outers()["NAE"], 3)
    cov, lp = cover_number(M), frac_cover(M)
    assert _ones(M) == 48
    assert cov - lp == Fraction(1)
    assert not is_J_minus_I_up_to_perm(M)


def test_first_non_JI_gap_found_among_named():
    # sparsity_skip evita le celle 8x8 DENSE (set-cover esatto costoso, >120s);
    # il killer (ONE_IN_3, peso 24) cade comodamente nella finestra sparsa.
    outs = list(named_3bit_outers().items())
    res = first_non_JI_gap(outs, k=3, sparsity_skip=(1, 24))
    assert res is not None
    name, M, cov, lp, g = res
    assert g > 0
    assert not is_J_minus_I_up_to_perm(M)


# --- censimento esaustivo (lento): tutte le 256 funzioni a 3 bit, sparse ----

@pytest.mark.slow
@pytest.mark.timeout(900)
def test_all_3bit_sparse_gaps_are_nonJI():
    """Tutte le 256 funzioni a 3 bit con pattern-matrix <=32 ones: ogni gap e'
    non-J-I (sono i 56 della classe peso-24, G*=2, adiacenza Q3 e traslati)."""
    gaps = 0
    for name, f in all_3bit_outers():
        M = pattern_matrix(f, 3)
        if _ones(M) > 32:
            continue
        g = gstar(M)
        if g > 0:
            gaps += 1
            assert g == Fraction(2)
            assert not is_J_minus_I_up_to_perm(M)
            assert _ones(M) == 24
    assert gaps == 56
