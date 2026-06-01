"""Test del Modulo 8 — Switching Lemma Lab."""

import random

from pnp_lab.switching import (
    eval_dnf,
    free_vars,
    optimal_dt_depth,
    parity_depth_under_restriction,
    parity_value,
    random_dnf,
    random_restriction,
    restrict_dnf,
    run_switching,
    tabulate,
)


# ── albero di decisione ───────────────────────────────────────────────────

def test_dt_depth_constant_is_zero():
    assert optimal_dt_depth((0, 0, 0, 0)) == 0
    assert optimal_dt_depth((1, 1)) == 0


def test_dt_depth_single_var():
    # f(x) = x  → un solo livello
    assert optimal_dt_depth((0, 1)) == 1


def test_dt_depth_parity_equals_n():
    # D(parità su k variabili) = k, per k = 1..4
    for k in range(1, 5):
        table = tuple(bin(a).count("1") & 1 for a in range(1 << k))
        assert optimal_dt_depth(table) == k


def test_dt_depth_and_is_shallow():
    # AND a 3 variabili: profondità ottima 3? no — basta leggere finché trovi uno 0,
    # ma nel caso peggiore (tutti 1) servono tutte: D(AND_k) = k
    for k in range(1, 4):
        table = tuple(1 if a == (1 << k) - 1 else 0 for a in range(1 << k))
        assert optimal_dt_depth(table) == k


# ── restrizioni ───────────────────────────────────────────────────────────

def test_random_restriction_marks_free_and_fixed():
    rng = random.Random(0)
    rho = random_restriction(20, 0.3, rng)
    assert len(rho) == 20
    assert all(v in (0, 1, None) for v in rho)
    # con p=0.3 su 20 variabili ci si aspetta qualche libera e qualche fissata
    assert 0 < len(free_vars(rho)) < 20


def test_restrict_dnf_term_dies_and_simplifies():
    # DNF = (x0 ∧ x1) ∨ (¬x0 ∧ x2)
    dnf = [((0, True), (1, True)), ((0, False), (2, True))]
    # ρ: x0=1  → primo termine diventa (x1), secondo muore
    rho = (1, None, None)
    r = restrict_dnf(dnf, rho)
    assert r == [((1, True),)]


def test_restrict_dnf_becomes_constant_true():
    dnf = [((0, True), (1, True))]
    rho = (1, 1, None)  # entrambi i letterali soddisfatti → termine vuoto ≡ VERO
    assert restrict_dnf(dnf, rho) == [()]


def test_tabulate_matches_eval():
    rng = random.Random(1)
    dnf = random_dnf(6, 3, 5, rng)
    rho = random_restriction(6, 0.5, rng)
    table, free = tabulate(lambda a: eval_dnf(dnf, a), rho)
    assert len(table) == (1 << len(free))


# ── lo switching lemma in azione ──────────────────────────────────────────

def test_parity_depth_equals_free_count():
    rng = random.Random(2)
    pdep = parity_depth_under_restriction(14, 0.4, 400, rng)
    # per ogni numero di liberi osservato, la profondità DT è esattamente quel numero
    for k, depth in pdep.items():
        assert depth == k


def test_switching_bound_holds():
    # p < 1/(5w): il bound (5pw)^s deve dominare la frequenza empirica
    rng = random.Random(3)
    n, w, p, trials = 16, 3, 0.05, 4000
    dnf = random_dnf(n, w, 12, rng)
    stats = run_switching(dnf, n, p, trials, rng, width=w, max_s=4)
    assert 5 * p * w < 1
    for s in stats.bound:
        assert stats.empirical_ge[s] <= stats.bound[s] + 1e-9


def test_switching_dnf_stays_shallower_than_parity():
    # a parità di #variabili libere, la DNF è in media molto più bassa della parità
    rng = random.Random(4)
    n, w, p, trials = 16, 3, 0.06, 4000
    dnf = random_dnf(n, w, 12, rng)
    stats = run_switching(dnf, n, p, trials, rng, width=w)
    avg = stats.avg_dnf_depth_by_free()
    # su gruppi con almeno 3 variabili libere la DNF resta in media < #liberi
    for k, a in avg.items():
        if k >= 3 and len(stats.dnf_depth_by_free[k]) >= 20:
            assert a < k
