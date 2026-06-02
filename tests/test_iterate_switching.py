"""Test per lo switching ITERATO in profondità d (Modulo 8, passo #2).

Verifichiamo, in modo esatto su n piccolo:
  - il circuito AC0 concreto valuta correttamente e la parità-come-DNF è la parità;
  - sotto restrizione la parità NON collassa: D(parità|ρ) = #variabili libere, sempre;
  - lo switching iterato fa crollare un AC0 round dopo round, mentre la parità resta
    sulla diagonale (stessa ρ per entrambi ⇒ #liberi identico);
  - il conto quantitativo (forma di Håstad) restituisce numeri sensati e monotoni.
"""

import random

from pnp_lab.switching import (
    AC0Circuit,
    random_ac0,
    parity_as_dnf,
    parity_value,
    tabulate,
    optimal_dt_depth,
    iterate_collapse,
    iterate_collapse_joint,
    depth_reduction_demo,
    default_schedule,
    parity_lower_bound,
    ascii_report_iterated,
    bound_report,
    to_svg_trajectory,
    iterate_summary,
)
from pnp_lab.switching.restriction import random_restriction, free_vars


# ── circuito AC0 concreto ────────────────────────────────────────────────
def test_ac0_evaluate_matches_definition():
    # (x0 AND x1) OR (NOT x2)  — profondità 2
    c = AC0Circuit(n=3, bottom=[((0, True), (1, True)), ((2, False),)], layers=[("OR", [[0, 1]])])
    assert c.depth == 2
    assert c.bottom_fanin == 2
    assert c.size == 3
    for a in range(8):
        bits = [(a >> (2 - i)) & 1 for i in range(3)]
        expected = 1 if ((bits[0] and bits[1]) or (not bits[2])) else 0
        assert c.evaluate(bits) == expected


def test_parity_as_dnf_is_parity():
    for n in (2, 3, 4):
        c = parity_as_dnf(n)
        assert c.bottom_fanin == n
        assert len(c.bottom) == (1 << (n - 1))  # 2^(n-1) mintermini dispari
        tt = c.truth_table()
        for a in range(1 << n):
            bits = [(a >> (n - 1 - i)) & 1 for i in range(n)]
            assert tt[a] == (sum(bits) & 1)


def test_random_ac0_well_formed():
    rng = random.Random(1)
    c = random_ac0(n=10, depth=4, bottom_fanin=3, rng=rng, bottom_terms=8, fanin=3)
    assert c.depth == 4
    assert c.bottom_fanin <= 3
    # ultimo livello = una sola porta di uscita
    assert len(c.layers[-1][1]) == 1
    # operatori alternati a partire da OR (bottom è AND)
    ops = [op for op, _ in c.layers]
    assert ops[0] == "OR"
    for i in range(1, len(ops)):
        assert ops[i] != ops[i - 1]
    # valutazione coerente con la tabella di verità
    tt = c.truth_table()
    assert len(tt) == 1024
    assert all(v in (0, 1) for v in tt)


# ── la parità non collassa: invariante esatto ────────────────────────────
def test_parity_dt_depth_equals_free_vars_exact():
    rng = random.Random(123)
    for _ in range(40):
        n = rng.randint(2, 10)
        p = rng.choice([0.2, 0.4, 0.6])
        rho = random_restriction(n, p, rng)
        table, free = tabulate(parity_value, rho)
        # D(parità|ρ) = numero di variabili libere, ESATTAMENTE
        assert optimal_dt_depth(table) == len(free) == len(free_vars(rho))


# ── switching iterato: l'AC0 crolla, la parità no ────────────────────────
def test_iterated_switching_collapses_ac0_not_parity():
    rng = random.Random(7)
    c = random_ac0(n=50, depth=3, bottom_fanin=2, rng=rng, bottom_terms=14, fanin=3)
    ac0, par = depth_reduction_demo(c, rng, trials=200, schedule=[0.18, 0.18])

    # stessa ρ ⇒ #liberi identico, e D(parità) == #liberi a ogni round (esatto)
    for ra, rp in zip(ac0.rounds, par.rounds):
        assert ra.avg_free == rp.avg_free
        assert abs(rp.avg_dt_depth - rp.avg_free) < 1e-9

    # l'AC0 collassa: alla fine quasi sempre profondità ≤ soglia
    assert ac0.final_collapsed_frac >= 0.90
    # e la sua profondità media è ben sotto quella della parità (= #liberi)
    assert ac0.rounds[0].avg_dt_depth < par.rounds[0].avg_dt_depth
    # la parità NON collassa finché restano variabili libere
    assert par.rounds[0].avg_dt_depth > 1.0


def test_iterate_collapse_joint_shares_free_counts():
    rng = random.Random(99)
    res = iterate_collapse_joint(
        {"parità": parity_value, "zero": lambda a: 0},
        n=12, schedule=[0.5, 0.5], rng=rng, trials=50,
    )
    # i conteggi di #liberi sono identici tra le due funzioni (stessa ρ)
    for r1, r2 in zip(res["parità"].rounds, res["zero"].rounds):
        assert r1.avg_free == r2.avg_free
    # la funzione costante ha profondità DT 0 sempre
    assert all(r.avg_dt_depth == 0.0 for r in res["zero"].rounds)
    # la parità resta = #liberi
    assert all(abs(r.avg_dt_depth - r.avg_free) < 1e-9 for r in res["parità"].rounds)


def test_iterate_collapse_single_wrapper():
    rng = random.Random(5)
    c = random_ac0(n=30, depth=3, bottom_fanin=2, rng=rng, bottom_terms=10, fanin=3)
    res = iterate_collapse(c.as_evaluator(), c.n, [0.2, 0.2], rng, trials=100)
    assert len(res.rounds) == 2
    # profondità media non cresce round dopo round (collasso monotòno in media)
    assert res.rounds[1].avg_dt_depth <= res.rounds[0].avg_dt_depth + 1e-9


def test_default_schedule_hastad():
    sched = default_schedule(depth=4, bottom_fanin=2)
    assert len(sched) == 3  # d - 1 round
    # 5·p·w = 1 al fondo
    assert all(abs(5 * p * 2 - 1.0) < 1e-9 for p in sched)


# ── chiusura quantitativa ────────────────────────────────────────────────
def test_parity_lower_bound_sane_and_monotone():
    b3 = parity_lower_bound(n=1000, depth=3)
    assert b3.rounds == 2
    assert b3.fanin_threshold > 0
    assert b3.expected_survivors > 0
    # la dimensione minima cresce con n a profondità fissa
    small = parity_lower_bound(n=100, depth=3).size_lower_bound
    big = parity_lower_bound(n=10000, depth=3).size_lower_bound
    assert big > small
    # più profondità ⇒ bound più debole (la parità diventa "più facile" per AC0)
    deep = parity_lower_bound(n=10000, depth=5).size_lower_bound
    shallow = parity_lower_bound(n=10000, depth=3).size_lower_bound
    assert shallow > deep


# ── report ───────────────────────────────────────────────────────────────
def test_reports_render():
    rng = random.Random(3)
    c = random_ac0(n=24, depth=3, bottom_fanin=2, rng=rng, bottom_terms=8, fanin=3)
    ac0, par = depth_reduction_demo(c, rng, trials=60, schedule=[0.2, 0.2])
    txt = ascii_report_iterated(ac0, par)
    assert "Switching ITERATO" in txt and "parità ∉ AC0" in txt
    svg = to_svg_trajectory(ac0, par)
    assert svg.startswith("<svg") and svg.rstrip().endswith("</svg>")
    assert "parità ∉ AC0" in iterate_summary()
    assert "Håstad" in bound_report(parity_lower_bound(n=500, depth=4))
