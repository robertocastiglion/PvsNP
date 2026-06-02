"""Test della strada #3 — policy di branching pluggabili per il CDCL (M11 ↔ CDCL)."""

from pnp_lab.proof_complexity import pigeonhole_cnf
from pnp_lab.enriched_meta import (
    LLMBranchPolicy,
    branch_summary,
    compare_policies,
    random_policy,
    static_policy,
    vsids_policy,
)
from pnp_lab.enriched_meta.cdcl import solve
from pnp_lab.enriched_meta.synthesis_sat import circuit_exists_cnf


def _tt(bits):
    v = 0
    for t, b in enumerate(bits):
        if b:
            v |= 1 << t
    return v


XOR2 = _tt([0, 1, 1, 0])


# ── la policy non cambia il verdetto (correttezza preservata) ─────────────

def test_all_policies_agree_on_verdict_unsat():
    cnf = pigeonhole_cnf(5, 4)            # UNSAT
    pols = {"vsids": None, "static": static_policy, "random": random_policy(0),
            "llm": LLMBranchPolicy()}
    res = compare_policies(cnf, pols)
    assert all(not r.satisfiable for r in res)
    assert all(r.conflicts > 0 for r in res)   # serve refutare


def test_all_policies_agree_on_verdict_sat():
    cnf = circuit_exists_cnf(XOR2, 2, 3)        # SAT (size XOR2 = 3)
    pols = {"vsids": None, "static": static_policy, "random": random_policy(1)}
    res = compare_policies(cnf, pols)
    assert all(r.satisfiable for r in res)


def test_custom_policy_matches_default_verdict():
    cnf = circuit_exists_cnf(XOR2, 2, 2)        # UNSAT
    d = solve(cnf)
    c = solve(cnf, decide=static_policy)
    assert d.satisfiable == c.satisfiable == False


# ── le policy ritornano literali validi ───────────────────────────────────

def test_policies_return_valid_literals():
    un = [1, 2, 3]
    act = {1: 0.5, 2: 0.9, 3: 0.1}
    assert vsids_policy(un, act, 3) == 2          # attività massima
    assert static_policy(un, act, 3) == 1         # indice minimo
    r = random_policy(0)(un, act, 3)
    assert abs(r) in un


# ── LLM policy: fallback e parsing (stub, nessun modello reale) ────────────

def test_llm_policy_falls_back_to_vsids_without_call_fn():
    un = [1, 2, 3]
    act = {1: 0.5, 2: 0.9, 3: 0.1}
    assert LLMBranchPolicy()(un, act, 3) == 2     # = VSIDS


def test_llm_policy_uses_parsed_variable():
    un = [1, 2, 3]
    act = {1: 0.5, 2: 0.9, 3: 0.1}
    pol = LLMBranchPolicy(call_fn=lambda prompt: "scelgo la 3")
    assert pol(un, act, 3) == 3
    # se il modello propone una variabile non libera, fallback a VSIDS
    pol2 = LLMBranchPolicy(call_fn=lambda prompt: "99")
    assert pol2(un, act, 3) == 2


def test_branch_summary_is_honest():
    b = branch_summary()
    assert "resolution" in b.theory.lower()
    assert "nessun risultato nuovo" in b.honest_limit.lower()
