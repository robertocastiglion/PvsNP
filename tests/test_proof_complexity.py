"""Test del Modulo 5 — Proof Complexity Lab."""

from pnp_lab.proof_complexity import (
    dpll,
    horn_chain_cnf,
    pigeonhole_cnf,
    refute,
    resolve,
    run_growth_study,
)


# ── codifica della piccionaia ────────────────────────────────────────────

def test_php_overflow_is_unsat():
    # 3 piccioni in 2 buche: insoddisfacibile
    cnf = pigeonhole_cnf(3, 2)
    assert dpll(cnf).satisfiable is False


def test_php_matching_is_sat():
    # n piccioni in n buche: soddisfacibile
    assert dpll(pigeonhole_cnf(3, 3)).satisfiable is True
    assert dpll(pigeonhole_cnf(4, 4)).satisfiable is True


def test_php_clause_counts():
    # PHP 3/2: 3 clausole-piccione + 2 buche * C(3,2)=3 = 3 + 6 = 9
    cnf = pigeonhole_cnf(3, 2)
    assert cnf.num_vars == 6
    assert cnf.num_clauses == 9


# ── regola di resolution ─────────────────────────────────────────────────

def test_resolve_basic():
    a = frozenset({1, 2})       # x1 ∨ x2
    b = frozenset({-1, 3})      # ¬x1 ∨ x3
    assert resolve(a, b, 1) == frozenset({2, 3})


def test_resolve_to_empty():
    a = frozenset({1})          # x1
    b = frozenset({-1})         # ¬x1
    assert resolve(a, b, 1) == frozenset()


def test_resolve_tautology_discarded():
    a = frozenset({1, 2})       # x1 ∨ x2
    b = frozenset({-1, -2})     # ¬x1 ∨ ¬x2
    assert resolve(a, b, 1) is None  # risolvente x2 ∨ ¬x2 = tautologia


# ── refutazione per saturazione sui casi piccoli ─────────────────────────

def test_refute_small_php_finds_empty():
    res = refute(pigeonhole_cnf(2, 1))
    assert res.found_empty is True


def test_refute_php_3_2_finds_empty():
    res = refute(pigeonhole_cnf(3, 2), max_clauses=50000)
    assert res.found_empty is True


def test_refute_satisfiable_no_empty():
    # 2 piccioni in 2 buche è soddisfacibile: nessuna clausola vuota
    res = refute(pigeonhole_cnf(2, 2))
    assert res.found_empty is False


# ── catena di Horn (contrasto facile) ────────────────────────────────────

def test_horn_chain_unsat_but_easy():
    cnf = horn_chain_cnf(8)
    res = dpll(cnf)
    assert res.satisfiable is False
    # refutazione lineare: la propagazione unitaria basta, zero decisioni
    assert res.decisions == 0


# ── crescita esponenziale ────────────────────────────────────────────────

def test_growth_is_exponential():
    study = run_growth_study(max_holes=4, node_budget=2_000_000, time_budget=5.0)
    assert len(study.rows) >= 3
    gf = study.growth_factor
    assert gf is not None and gf > 1.5  # crescita più che lineare, esponenziale


def test_growth_nodes_increase():
    study = run_growth_study(max_holes=4, node_budget=2_000_000, time_budget=30.0)
    good = [r for r in study.rows if not r.aborted]
    nodes = [r.tree_nodes for r in good]
    assert nodes == sorted(nodes)  # monotòna non decrescente
    assert nodes[-1] > nodes[0]
