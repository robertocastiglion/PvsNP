"""Test di ancoraggio per pnp_lab.gct_kronecker.fast.

Verifica (>=10 test):
  1.  g_fast == kronecker su TUTTE le terne d=1..5  (0 mismatch)
  2.  g_fast == kronecker su campione d=6
  3.  Sigma_lambda dim(S^lambda)^2 = d!  per d=1..8
  4.  g([d], mu, nu) = delta_{mu,nu}  (tensore con la triviale)
  5.  g([1^d], mu, nu) = delta_{mu, nu'}  (tensore con il segno)
  6.  Simmetria S_3 completa su campione d=7
  7.  Coniugio simultaneo su campione d=7  (g(l,m,n)=g(l',m',n)=g(l',m,n'))
  8.  Ortogonalita' righe della tavola per d=1..5
  9.  Ortogonalita' righe della tavola per d=7
 10.  g_fast >= 0 e intero su tutte le terne d=1..5
 11.  census(5) coerente con vanishing_table(5)
 12.  g_fast == kronecker su campione d=7  (slow: riscalda la tavola d=7)
"""

from __future__ import annotations

import random
from itertools import permutations
from math import factorial

import pytest

from pnp_lab.gct_kronecker.fast import character_table, g_fast, census
from pnp_lab.gct_kronecker.kronecker import (
    kronecker,
    partitions,
    transpose,
    vanishing_table,
    _triples,
)


# ---------------------------------------------------------------------------
# Utilita' locali
# ---------------------------------------------------------------------------
def _sign_partition(d: int):
    """La partizione (1^d) = rappresentazione segno."""
    return tuple([1] * d)


def _trivial_partition(d: int):
    """La partizione (d,) = rappresentazione triviale."""
    return (d,)


# ---------------------------------------------------------------------------
# 1. g_fast == kronecker su TUTTE le terne d=1..5
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", [1, 2, 3, 4, 5])
def test_g_fast_equals_kronecker_all_triples_d1_to_d5(d):
    """g_fast e kronecker devono coincidere su ogni terna non ordinata di d."""
    mismatches = []
    for lam, mu, nu in _triples(d):
        gf = g_fast(lam, mu, nu)
        gk = kronecker(lam, mu, nu)
        if gf != gk:
            mismatches.append((lam, mu, nu, gf, gk))
    assert mismatches == [], f"d={d}: {len(mismatches)} mismatch: {mismatches[:3]}"


# ---------------------------------------------------------------------------
# 2. g_fast == kronecker su campione d=6
# ---------------------------------------------------------------------------
def test_g_fast_equals_kronecker_sample_d6():
    """Campione di 60 terne da d=6: g_fast deve coincidere con kronecker."""
    rng = random.Random(42)
    triples_d6 = _triples(6)
    sample = rng.sample(triples_d6, min(60, len(triples_d6)))
    for lam, mu, nu in sample:
        assert g_fast(lam, mu, nu) == kronecker(lam, mu, nu), (lam, mu, nu)


# ---------------------------------------------------------------------------
# 3. Sigma dim(S^lambda)^2 = d!  per d=1..8
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", list(range(1, 9)))
def test_sum_of_squared_dims_equals_d_factorial(d):
    """Prima relazione di Burnside: sum_lambda dim^2 = |S_d| = d!
    dim(S^lambda) = chi^lambda(identita') = carattere sulla classe (1^d)."""
    ct = character_table(d)
    # La classe identita' e' (1,1,...,1): la partizione con tutte parti uguali a 1
    id_class = _sign_partition(d) if d > 0 else ()
    id_idx = ct.part_index[id_class]
    total = sum(ct.chi[i][id_idx] ** 2 for i in range(len(ct.parts)))
    assert total == factorial(d), f"d={d}: sum dim^2 = {total} != {factorial(d)}"


# ---------------------------------------------------------------------------
# 4. g([d], mu, nu) = delta_{mu,nu}
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", [2, 3, 4, 5, 6])
def test_trivial_rep_gives_identity_matrix(d):
    """Tensore con la triviale: g((d), mu, nu) = delta_{mu,nu}.
    Segue dall'ortogonalita' dei caratteri: sum_alpha |C_alpha| chi^mu chi^nu / d! = delta_{mu,nu}."""
    triv = _trivial_partition(d)
    ps = partitions(d)
    for mu in ps:
        for nu in ps:
            expected = 1 if mu == nu else 0
            got = g_fast(triv, mu, nu)
            assert got == expected, f"d={d}: g({triv},{mu},{nu})={got}, atteso {expected}"


# ---------------------------------------------------------------------------
# 5. g([1^d], mu, nu) = delta_{mu, nu'}
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", [2, 3, 4, 5, 6])
def test_sign_rep_gives_conjugate_delta(d):
    """Tensore con il segno: g((1^d), mu, nu) = delta_{nu, mu'} = delta_{mu, nu'}.
    Equivalente a chi^{(1^d)} * chi^mu = chi^{mu'}: g e' 1 sse nu = trasposta di mu."""
    sign = _sign_partition(d)
    ps = partitions(d)
    for mu in ps:
        mu_prime = transpose(mu)
        for nu in ps:
            expected = 1 if nu == mu_prime else 0
            got = g_fast(sign, mu, nu)
            assert got == expected, f"d={d}: g(sign,{mu},{nu})={got}, atteso {expected}"


# ---------------------------------------------------------------------------
# 6. Simmetria S_3 su campione d=7
# ---------------------------------------------------------------------------
def test_s3_symmetry_sample_d7():
    """g e' invariante sotto TUTTE le 6 permutazioni di (lam, mu, nu) per d=7."""
    # Campione fisso di terne di d=7
    ps = partitions(7)
    sample = [
        (ps[0], ps[1], ps[2]),    # ((7,), (6,1), (5,2))
        (ps[2], ps[5], ps[8]),
        (ps[3], ps[7], ps[10]),
        (ps[1], ps[4], ps[9]),
        (ps[0], ps[0], ps[0]),
        (ps[6], ps[6], ps[6]),
    ]
    for t in sample:
        g_base = g_fast(*t)
        for perm in permutations(t):
            g_perm = g_fast(*perm)
            assert g_perm == g_base, f"Asimmetria in d=7: base={t}, perm={perm}, {g_base} != {g_perm}"


# ---------------------------------------------------------------------------
# 7. Coniugio simultaneo su campione d=7
# ---------------------------------------------------------------------------
def test_double_conjugation_symmetry_d7():
    """g(lam,mu,nu) = g(lam',mu',nu) = g(lam',mu,nu') = g(lam,mu',nu') per campione d=7."""
    ps = partitions(7)
    sample = [
        (ps[0], ps[2], ps[4]),
        (ps[3], ps[5], ps[7]),
        (ps[1], ps[6], ps[9]),
        (ps[2], ps[2], ps[8]),
    ]
    for lam, mu, nu in sample:
        lp, mp, np_ = transpose(lam), transpose(mu), transpose(nu)
        g_base = g_fast(lam, mu, nu)
        assert g_fast(lp, mp, nu) == g_base, (lam, mu, nu, "lam',mu',nu")
        assert g_fast(lp, mu, np_) == g_base, (lam, mu, nu, "lam',mu,nu'")
        assert g_fast(lam, mp, np_) == g_base, (lam, mu, nu, "lam,mu',nu'")


# ---------------------------------------------------------------------------
# 8. Ortogonalita' righe della tavola per d=1..5  (prima relazione di Schur)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", list(range(1, 6)))
def test_row_orthogonality_d1_to_d5(d):
    """Prima relazione di ortogonalita' dei caratteri:
        sum_j  |C_j| * chi[i][j] * chi[k][j]  =  delta_{i,k} * d!
    Verifica sia la correttezza della tavola sia quella di class_sizes."""
    ct = character_table(d)
    n = len(ct.parts)
    d_fact = factorial(d)
    for i in range(n):
        for k in range(i, n):
            dot = sum(
                ct.class_sizes[j] * ct.chi[i][j] * ct.chi[k][j]
                for j in range(n)
            )
            expected = d_fact if i == k else 0
            assert dot == expected, (
                f"d={d}: ortogonalita' fallita per i={i}({ct.parts[i]}), "
                f"k={k}({ct.parts[k]}): dot={dot}, atteso={expected}"
            )


# ---------------------------------------------------------------------------
# 9. Ortogonalita' righe della tavola per d=7
# ---------------------------------------------------------------------------
def test_row_orthogonality_d7():
    """Prima relazione di ortogonalita' dei caratteri per d=7 (15 irriducibili)."""
    d = 7
    ct = character_table(d)
    n = len(ct.parts)
    d_fact = factorial(d)
    for i in range(n):
        for k in range(i, n):
            dot = sum(
                ct.class_sizes[j] * ct.chi[i][j] * ct.chi[k][j]
                for j in range(n)
            )
            expected = d_fact if i == k else 0
            assert dot == expected, (
                f"d=7: ortogonalita' fallita per ({ct.parts[i]},{ct.parts[k]}): "
                f"dot={dot}, atteso={expected}"
            )


# ---------------------------------------------------------------------------
# 10. g_fast >= 0 e intero su tutte le terne d=1..5
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("d", [1, 2, 3, 4, 5])
def test_g_fast_nonneg_integer_all_d1_to_d5(d):
    """g_fast ritorna int >= 0 su tutte le terne non ordinate di d."""
    for lam, mu, nu in _triples(d):
        g = g_fast(lam, mu, nu)
        assert isinstance(g, int), f"g_fast non e' int: {type(g)}"
        assert g >= 0, f"g_fast < 0: g({lam},{mu},{nu}) = {g}"


# ---------------------------------------------------------------------------
# 11. census(5) coerente con vanishing_table(5)
# ---------------------------------------------------------------------------
def test_census_d5_matches_vanishing_table():
    """census(5) deve dare lo stesso conteggio di zeri di vanishing_table(5)."""
    # Conta gli zeri nella tabella di riferimento
    vt = vanishing_table(5)
    expected_zeros = sum(1 for _, (g, _, _) in vt.items() if g == 0)
    expected_triples = len(vt)

    n_triples, n_zeros, zeros_list = census(5)

    assert n_triples == expected_triples, (
        f"census(5): n_triples={n_triples}, atteso {expected_triples}"
    )
    assert n_zeros == expected_zeros, (
        f"census(5): n_zeros={n_zeros}, atteso {expected_zeros}"
    )
    # Ogni terna nella lista zeri deve davvero avere g=0
    for lam, mu, nu in zeros_list:
        assert g_fast(lam, mu, nu) == 0, f"census: falso zero ({lam},{mu},{nu})"


# ---------------------------------------------------------------------------
# 12. g_fast == kronecker su campione d=7  (slow: riscalda la tavola d=7)
# ---------------------------------------------------------------------------
@pytest.mark.slow
@pytest.mark.timeout(120)
def test_g_fast_equals_kronecker_sample_d7():
    """Campione di 100 terne da d=7: g_fast deve coincidere con kronecker.
    Marcato slow perche' kronecker() usa Fraction (piu' lento di g_fast)."""
    rng = random.Random(7)
    triples_d7 = _triples(7)
    sample = rng.sample(triples_d7, min(100, len(triples_d7)))
    for lam, mu, nu in sample:
        assert g_fast(lam, mu, nu) == kronecker(lam, mu, nu), (lam, mu, nu)
