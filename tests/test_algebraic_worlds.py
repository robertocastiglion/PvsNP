"""Test del Modulo 9 — Algebraic Query Model (mondi algebrici)."""

import random

from pnp_lab.algebrization import Field
from pnp_lab.algebraic_worlds import (
    Poly,
    count_agreements,
    count_zeros,
    cube_queries,
    interpolation_lower_bound,
    planted_detection,
    random_queries,
    verify_schwartz_zippel,
)


# ── polinomi su GF(p) ─────────────────────────────────────────────────────

def test_poly_eval_and_degree():
    F = Field(7)
    # 3*x0*x1 + 2*x0  in 2 variabili
    poly = Poly(2, F, {(1, 1): 3, (1, 0): 2})
    assert poly.total_degree == 2
    assert poly.eval((1, 1)) == (3 + 2) % 7
    assert poly.eval((2, 3)) == (3 * 2 * 3 + 2 * 2) % 7  # 18+4=22 -> 1
    assert poly.eval((0, 5)) == 0


def test_poly_zero_reduction():
    F = Field(5)
    poly = Poly(1, F, {(1,): 5, (0,): 0})  # coeff 5 ≡ 0, e 0
    assert poly.is_zero


# ── Schwartz–Zippel ───────────────────────────────────────────────────────

def test_schwartz_zippel_holds_random():
    F = Field(11)
    rng = random.Random(0)
    for _ in range(20):
        # polinomio casuale di grado ≤ 2 in 2 variabili
        terms = {}
        for exp in [(0, 0), (1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]:
            terms[exp] = rng.randrange(11)
        poly = Poly(2, F, terms)
        if poly.is_zero:
            continue
        chk = verify_schwartz_zippel(poly)
        assert chk.holds  # zeri ≤ d · p^(n-1)


def test_schwartz_zippel_linear_exact():
    # x0 - x1 (grado 1) su GF(p)^2: zeri = la diagonale, esattamente p punti = d·p^(n-1)
    F = Field(7)
    poly = Poly(2, F, {(1, 0): 1, (0, 1): F.neg(1)})
    chk = verify_schwartz_zippel(poly)
    assert chk.zeros == 7
    assert chk.bound == 7
    assert chk.holds


def test_agreement_is_zeros_of_difference():
    F = Field(5)
    f = Poly(1, F, {(1,): 1})           # x
    g = Poly(1, F, {(0,): 0})           # 0
    # x e 0 coincidono solo in x=0 → 1 punto
    assert count_agreements(f, g) == 1
    assert count_zeros(f) == 1


# ── Mondo 1: potenza dell'accesso algebrico ───────────────────────────────

def test_planted_detection_algebraic_beats_boolean():
    det = planted_detection(m=4, p=17, planted_index=5)
    # una query algebrica rileva con prob alta…
    assert det.algebraic_detect_prob > 0.5
    # …e coincide con la formula esatta (1-1/p)^m
    assert abs(det.algebraic_detect_prob - det.exact_prob_formula) < 1e-9
    # …mentre una query booleana ha solo 1/2^m
    assert det.boolean_detect_prob_one_query == 1 / 16
    assert det.algebraic_detect_prob > det.boolean_detect_prob_one_query * 5


# ── Mondo 2: limite — lower bound di interpolazione ───────────────────────

def test_interpolation_underdetermined_with_few_queries():
    m, p = 3, 11
    rng = random.Random(1)
    queries = random_queries(m, p, k=(1 << m) - 1, rng=rng)  # 7 < 2^3 = 8
    b = interpolation_lower_bound(m, p, queries)
    assert not b.determined
    assert b.rank < (1 << m)
    assert b.adversary is not None and not b.adversary.is_zero
    # l'avversario si annulla su TUTTE le query…
    for q in queries:
        assert b.adversary.eval(q) == 0
    # …ma differisce dall'oracolo zero su un punto del cubo
    assert b.witness_cube_point is not None
    assert b.adversary.eval(b.witness_cube_point) != 0


def test_interpolation_determined_by_full_cube():
    m, p = 3, 11
    b = interpolation_lower_bound(m, p, cube_queries(m))  # 2^m query = il cubo
    assert b.determined
    assert b.rank == (1 << m)
    assert b.adversary is None


def test_interpolation_rank_grows_with_queries():
    m, p = 3, 13
    rng = random.Random(2)
    last = -1
    for k in [1, 2, 4, 8]:
        b = interpolation_lower_bound(m, p, random_queries(m, p, k, rng))
        assert b.rank <= min(k, 1 << m)
        last = b.rank
    assert last == (1 << m)  # con 8 query casuali (generiche) il rango è pieno
