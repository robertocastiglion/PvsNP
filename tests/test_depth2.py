"""Test della strada 2 — #SAT esplicito per profondità-2 (DNF) più veloce di 2^n."""

import random

from pnp_lab.algorithmic_method import (
    analytic_speedup,
    benchmark,
    count_sat_bruteforce,
    count_sat_inclusion_exclusion,
    disjoint_terms_dnf,
)


def _random_dnf(n, num_terms, width, seed):
    rng = random.Random(seed)
    dnf = []
    for _ in range(num_terms):
        vs = rng.sample(range(n), min(width, n))
        dnf.append([(v, rng.random() < 0.5) for v in vs])
    return dnf


def test_inclusion_exclusion_matches_bruteforce_random():
    # correttezza: i due conteggi coincidono su DNF casuali (anche con termini sovrapposti)
    for seed in range(20):
        n = 8
        dnf = _random_dnf(n, num_terms=5, width=3, seed=seed)
        b = count_sat_bruteforce(dnf, n)
        ie = count_sat_inclusion_exclusion(dnf, n)
        assert b.value == ie.value


def test_empty_dnf_has_no_models():
    b = count_sat_bruteforce([], 5)
    ie = count_sat_inclusion_exclusion([], 5)
    assert b.value == 0 and ie.value == 0


def test_single_term_counts_correctly():
    # un solo AND di k variabili (positive) ha 2^(n-k) modelli
    n, k = 6, 3
    dnf = [[(i, True) for i in range(k)]]
    ie = count_sat_inclusion_exclusion(dnf, n)
    assert ie.value == (1 << (n - k))


def test_contradictory_intersection_contributes_zero():
    # due termini in conflitto su una variabile: l'intersezione è vuota
    n = 4
    dnf = [[(0, True)], [(0, False)]]   # x0  OR  ¬x0  = tautologia
    ie = count_sat_inclusion_exclusion(dnf, n)
    assert ie.value == (1 << n)         # tutte le assegnazioni soddisfano


def test_analytic_speedup_is_exponential_when_sparse():
    # m piccolo, n grande ⇒ speedup analitico 2^(n-m) enorme
    assert analytic_speedup(20, 3) == (1 << 17)


def test_benchmark_agrees_and_speeds_up():
    rows = benchmark(num_terms=3, term_width=2, ns=[8, 12, 16])
    assert all(r.agree for r in rows)                 # correttezza
    # lo speedup analitico cresce con n (m resta fisso)
    factors = [r.speedup_analytic for r in rows]
    assert all(factors[i] < factors[i + 1] for i in range(len(factors) - 1))
