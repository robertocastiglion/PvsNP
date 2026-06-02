"""Test del Modulo 14 riparato verso (S): lenti non-tautologiche su una misura
condivisa (sintesi-SAT, classe a risorse, metrica stratificata)."""

from pnp_lab.circuits import parity_table
from pnp_lab.meta_complexity import complexity_map
from pnp_lab.enriched_meta import (
    circuit_exists_cnf,
    circuit_size,
    critical_window,
    feature_vector,
    price_of_constructivity,
    proof_axis,
    recognize_axis,
    refutation_length,
    reverdict,
    shared_measure,
    size_distribution,
)
from pnp_lab.proof_complexity import dpll


def _tt(bits):
    v = 0
    for t, b in enumerate(bits):
        if b:
            v |= 1 << t
    return v


XOR2 = _tt([0, 1, 1, 0])
AND2 = _tt([0, 0, 0, 1])
AND3 = _tt([0, 0, 0, 0, 0, 0, 0, 1])


# ── la misura condivisa: dimensione di circuito esatta via SAT ────────────

def test_circuit_size_known_values_n2():
    assert circuit_size(AND2, 2).size == 1          # un solo gate AND
    assert circuit_size(XOR2, 2).size == 3          # XOR De Morgan = 3 gate
    # una variabile è dimensione 0 (letterale)
    x1 = _tt([0, 1, 0, 1])                            # proiezione su var 1
    assert circuit_size(x1, 2).size == 0


def test_synthesis_sat_progression_is_monotone():
    # XOR2: UNSAT a s<3, SAT a s>=3 (il lower bound è genuino)
    assert not dpll(circuit_exists_cnf(XOR2, 2, 2)).satisfiable
    assert dpll(circuit_exists_cnf(XOR2, 2, 3)).satisfiable


def test_shared_measure_n2_distribution():
    size2 = shared_measure(2)
    dist = size_distribution(size2)
    assert dist[0] == 4                              # x1,¬x1,x2,¬x2
    assert dist[3] == 2                              # XOR e ¬XOR
    assert sum(dist.values()) == 16


# ── lente "dimostrare": refutazione reale, non tautologica ────────────────

def test_refutation_is_a_real_lower_bound():
    pr = refutation_length(XOR2, 2, 2)              # size(XOR2)=3 ⇒ size>2 vero
    assert pr.is_lower_bound
    assert pr.refutation_nodes > 1                  # la prova ha lunghezza non banale
    assert not pr.aborted


def test_no_lower_bound_when_satisfiable():
    # alla soglia = size, la CNF è SAT: nessun lower bound
    pr = refutation_length(XOR2, 2, 3)
    assert not pr.is_lower_bound


def test_proof_axis_feasible_samples():
    pts = proof_axis([("AND3", AND3, 3), ("XOR2", XOR2, 2)])
    by = {p.name: p for p in pts}
    assert by["XOR2"].size == 3 and by["XOR2"].is_lower_bound
    assert by["AND3"].size == 2 and by["AND3"].is_lower_bound
    assert by["XOR2"].refutation_nodes > 0


# ── lente "riconoscere": classe a risorse, errore residuo ─────────────────

def test_feature_vector_shape_and_influence():
    fv = feature_vector(parity_table(3), 3)
    assert len(fv) == 4
    assert fv[0] == (1 << 3) * 3                     # parità: influenza totale massima


def test_price_of_constructivity_non_increasing():
    ct = complexity_map(3)
    win = critical_window(ct.cost, 3, half_width=1)
    curve = price_of_constructivity(ct.cost, 3, 3, max_depth=3, stratum=win)
    rates = [c.error_rate for c in curve]
    # più risorse (profondità) non peggiorano mai l'errore
    assert all(rates[i] >= rates[i + 1] for i in range(len(rates) - 1))


def test_recognize_residual_does_not_vanish_n3():
    # sulla finestra critica a n=3 l'errore della classe NON arriva a 0 (prezzo
    # della costruttività) — a differenza della media uniforme della v1
    ct = complexity_map(3)
    ax = recognize_axis(ct.cost, 3, s=3, max_depth=3, half_width=1)
    assert ax.window_size > 0
    assert ax.residual > 0.0
    assert not ax.vanishes


def test_critical_window_is_a_band():
    ct = complexity_map(3)
    win = critical_window(ct.cost, 3, half_width=1)
    assert all(2 <= ct.cost[t] <= 4 for t in win)


# ── ri-verdetto onesto ─────────────────────────────────────────────────────

def test_reverdict_is_honest():
    rv = reverdict()
    assert "candidato" in rv.classification.lower()
    assert "asintotica" in rv.open_point.lower()
    # i due artefatti della v1 sono dichiarati rimossi
    assert "brute" in rv.tautology_removed.lower()
    assert "concentrazione" in rv.vanishing_removed.lower()
