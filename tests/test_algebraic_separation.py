"""Test del Modulo 10 — la separazione P^Ã ≠ NP^Ã (cuore di query complexity)."""

from pnp_lab.algebrization import Field
from pnp_lab.algebraic_separation import (
    boolean_kernel_witness,
    cancellation_example,
    chi_vector,
    deterministic_lower_bound,
    evaluate,
    kills_all_kernels,
    verify_nondet_one_query,
)


# ── il modello: funzionali di valutazione ─────────────────────────────────

def test_chi_vector_on_cube_is_indicator():
    # sul cubo, χ_z(z') = 1 se z=z' altrimenti 0 → l'estensione coincide con A
    F = Field(7)
    m = 2
    # punto cubo (1,0): solo χ_{(1,0)} = 1
    chi = chi_vector((1, 0), m, F)
    # bits(a,2): a=2 -> (1,0)
    assert chi[2] == 1
    assert sum(chi) % 7 == 1  # un solo 1


def test_evaluate_matches_cube_values():
    F = Field(5)
    values = (0, 1, 1, 0)  # m=2
    # sul cubo Ã = A
    assert evaluate(values, (0, 0), F) == 0
    assert evaluate(values, (0, 1), F) == 1
    assert evaluate(values, (1, 0), F) == 1
    assert evaluate(values, (1, 1), F) == 0


# ── lato NP: una sola query ───────────────────────────────────────────────

def test_nondet_one_query_suffices():
    assert verify_nondet_one_query(2, 3)
    assert verify_nondet_one_query(2, 5)
    assert verify_nondet_one_query(3, 3)


# ── lato P: lower bound κ via avversario ───────────────────────────────────

def test_one_query_insufficient_small_field():
    # N = 2^m = 4 > p-1 = 2  ⇒  una query non basta (κ ≥ 2): la separazione
    res = deterministic_lower_bound(2, 3, cap=4)
    assert res.det_exact
    assert res.det_lower_bound == 2
    assert not res.one_query_enough
    assert res.nondet_queries == 1


def test_one_query_enough_large_field():
    # N = 4 ≤ p-1 = 4  ⇒  una query basta (κ = 1): niente separazione (campo grande)
    res = deterministic_lower_bound(2, 5, cap=4)
    assert res.det_exact
    assert res.det_lower_bound == 1
    assert res.one_query_enough


def test_gap_grows_with_n():
    # fissato p=3: κ cresce con N = 2^m (separazione che si allarga)
    r2 = deterministic_lower_bound(2, 3, cap=4)
    r3 = deterministic_lower_bound(3, 3, cap=8)
    assert r2.det_lower_bound == 2
    assert r3.det_lower_bound == 4
    assert r3.det_lower_bound > r2.det_lower_bound > r2.nondet_queries


def test_cancellation_adversary_is_blind():
    # l'avversario di cancellazione dà davvero Ã(r) = 0 (come il tutto-zero)
    F = Field(3)
    adv = cancellation_example(2, 3)
    assert adv is not None
    assert len(adv.ones_positions) >= 2
    # ricostruisci l'oracolo dai segreti e verifica Ã(r) = 0
    m = adv.m
    ones = set()
    for pos in adv.ones_positions:
        ones.add(sum(b << (m - 1 - i) for i, b in enumerate(pos)))
    A = tuple(1 if z in ones else 0 for z in range(1 << m))
    assert evaluate(A, adv.query_point, F) == 0
    # ma A non è il tutto-zero
    assert any(A)


def test_kernel_witness_consistency():
    # se una singola query ha un nucleo booleano, non determina OR
    F = Field(3)
    w = boolean_kernel_witness([(2, 2)], 2, F)
    assert w is not None and any(w)
    assert evaluate(w, (2, 2), F) == 0
    # il cubo intero invece elimina ogni nucleo (determina l'oracolo)
    cube = [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert kills_all_kernels(cube, 2, F)
