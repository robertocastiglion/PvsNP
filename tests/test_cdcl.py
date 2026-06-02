"""Test del solver CDCL (strada #1: solver più forte per spingere a n=4)."""

from pnp_lab.proof_complexity import pigeonhole_cnf, dpll
from pnp_lab.enriched_meta.cdcl import solve, _luby
from pnp_lab.enriched_meta import circuit_size, circuit_size_cdcl
from pnp_lab.enriched_meta.synthesis_sat import circuit_exists_cnf


def _model_ok(cnf, model):
    return all(any((model[abs(l)] if l > 0 else not model[abs(l)]) for l in c)
               for c in cnf.clauses)


def _tt(bits):
    v = 0
    for t, b in enumerate(bits):
        if b:
            v |= 1 << t
    return v


XOR2 = _tt([0, 1, 1, 0])


# ── il CDCL concorda col DPLL sui verdetti ────────────────────────────────

def test_cdcl_matches_dpll_on_php():
    for p, h in [(2, 2), (3, 2), (4, 3), (5, 4)]:
        cnf = pigeonhole_cnf(p, h)
        r = solve(cnf)
        d = dpll(cnf, node_budget=3_000_000)
        assert r.satisfiable == d.satisfiable
        if r.satisfiable:
            assert _model_ok(cnf, r.model)


def test_cdcl_unsat_has_no_model():
    cnf = pigeonhole_cnf(4, 3)              # insoddisfacibile
    r = solve(cnf)
    assert not r.satisfiable and r.model is None
    assert r.conflicts > 0                  # ha imparato qualcosa per refutare


# ── sulle istanze di sintesi ──────────────────────────────────────────────

def test_cdcl_synthesis_progression_and_model():
    assert not solve(circuit_exists_cnf(XOR2, 2, 2)).satisfiable
    r3 = solve(circuit_exists_cnf(XOR2, 2, 3))
    assert r3.satisfiable
    assert _model_ok(circuit_exists_cnf(XOR2, 2, 3), r3.model)


def test_circuit_size_cdcl_agrees_with_dpll_n2():
    # stesso valore del solver DPLL sulle funzioni n=2
    for tt in range(16):
        assert circuit_size_cdcl(tt, 2).size == circuit_size(tt, 2).size


# ── la sequenza di Luby (per i restart) ───────────────────────────────────

def test_luby_sequence():
    assert [_luby(i) for i in range(15)] == \
        [1, 1, 2, 1, 1, 2, 4, 1, 1, 2, 1, 1, 2, 4, 8]


def test_cdcl_conflict_budget_aborts():
    # con budget minuscolo su un'istanza dura, ritorna non-SAT (interrotto)
    r = solve(pigeonhole_cnf(7, 6), conflict_budget=1)
    assert not r.satisfiable
