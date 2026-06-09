"""Test esatti del Modulo 18 -- EXACTNESS COMPOSES (killer search).

Tutto su istanze minuscole, aritmetica razionale esatta (Fraction).
"""

from fractions import Fraction

import pytest

from pnp_lab.exactness_composes import (
    as_matrix,
    cover_number,
    frac_cover,
    gstar,
    is_integral,
    lift,
    lift_counterexamples,
    lift_named,
    maximal_one_rectangles,
    smallest_gap_matrix,
    smallest_lift_counterexample,
    tensor,
    tensor_closure_holds,
    GADGETS_1BIT,
    base_function,
)


# --- core: G* di base ---------------------------------------------------------

def test_empty_and_full_matrices_are_integral():
    assert gstar(as_matrix([[0, 0], [0, 0]])) == 0
    assert gstar(as_matrix([[1, 1], [1, 1]])) == 0


def test_identity_2x2_cover_two_lp_two():
    I = as_matrix([[1, 0], [0, 1]])
    assert cover_number(I) == 2
    assert frac_cover(I) == 2
    assert gstar(I) == 0


def test_three_cycle_is_integral_not_a_gap():
    # 6-ciclo bipartito: Cov = LP = 3 (NON e' un gap, contro l'intuizione set-cover)
    M = as_matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    assert cover_number(M) == 3
    assert frac_cover(M) == 3
    assert gstar(M) == 0


@pytest.mark.slow
@pytest.mark.timeout(900)
@pytest.mark.parametrize("m,n", [(2, 2), (2, 3), (3, 3), (2, 4), (3, 4)])
def test_no_gap_below_4x4(m, n):
    # esaustivo: nessuna matrice <= 3x4 (o 2x4) ha un gap di integralita'
    # (slow: il caso 3x4 = 4096 matrici, ognuna con un set-cover esatto)
    import itertools
    for bits in itertools.product([0, 1], repeat=m * n):
        M = as_matrix([bits[i * n:(i + 1) * n] for i in range(m)])
        assert gstar(M) == 0


# --- (1) la piu' piccola matrice con gap --------------------------------------

@pytest.mark.slow
@pytest.mark.timeout(900)
def test_smallest_gap_matrix_is_4x4_half():
    # slow: enumera esaustivamente fino alle 4x4 cercando il primo gap
    res = smallest_gap_matrix()
    assert res is not None
    M, g = res
    assert len(M) == 4 and len(M[0]) == 4
    assert g == Fraction(1, 2)


# --- (2) versione tensore: VERA (chiusura) ------------------------------------

def test_tensor_closure_holds_and_lp_multiplicative():
    closed, pairs, mult = tensor_closure_holds(shapes=((2, 2), (2, 3)))
    assert closed is True
    assert mult is True
    assert pairs > 0


def test_tensor_of_integral_specific_pair_is_integral():
    A = as_matrix([[1, 0], [0, 1]])
    B = as_matrix([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    assert is_integral(A) and is_integral(B)
    assert gstar(tensor(A, B)) == 0


# --- (3) versione lift: FALSA (controesempio) ---------------------------------

def test_all_1bit_gadgets_are_integral():
    # i fattori-gadget sono tutti integrali (G* = 0): il gap NON viene da loro
    for name, g in GADGETS_1BIT.items():
        assert gstar(g) == 0, name


def test_smallest_lift_counterexample_is_inequality_matrix():
    fname, gname, k, M, cov, lp = smallest_lift_counterexample()
    assert (fname, gname, k) == ("OR", "XOR", 2)
    # J - I_4 : zero sulla diagonale, 1 fuori
    expected = as_matrix([[0, 1, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [1, 1, 1, 0]])
    assert M == expected
    assert cov == 4
    assert lp == 3
    assert gstar(M) == 1


def test_or_eq_lift_also_opens_gap():
    # gadget alternativo integrale, stesso gap
    M = lift_named("OR", "EQ", 2)
    assert gstar(M) == 1


def test_no_lift_counterexample_at_k1():
    # k=1 => matrice 2x2 => sempre integrale: il gap richiede k>=2
    rows = lift_counterexamples(ks=(1,))
    assert rows == []


@pytest.mark.slow
@pytest.mark.timeout(900)
def test_lift_counterexamples_all_have_integral_gadget():
    # slow: sweep f x gadget x k={2,3}; il k=3 denso e' un LP su 8x8 (~600s)
    rows = lift_counterexamples()
    assert rows, "ci si aspetta almeno un controesempio-lift"
    for fname, gname, k, gv in rows:
        assert gstar(GADGETS_1BIT[gname]) == 0  # gadget integrale
        assert gv > 0                            # ma il lift ha un gap


def test_lp_certificate_value_three_on_witness():
    # certificato esplicito: peso 1/2 sui 6 rettangoli bilanciati copre tutto
    M = lift_named("OR", "XOR", 2)
    rects = [r for r in maximal_one_rectangles(M) if len(r) == 4]
    assert len(rects) == 6
    from collections import defaultdict
    cov = defaultdict(lambda: Fraction(0))
    for r in rects:
        for e in r:
            cov[e] += Fraction(1, 2)
    from pnp_lab.exactness_composes import ones
    assert all(cov[e] >= 1 for e in ones(M))
    assert Fraction(1, 2) * len(rects) == 3  # = LP(M)
