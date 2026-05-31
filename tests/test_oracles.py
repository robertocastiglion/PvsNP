"""Test del Modulo 2 — Oracle Separation Sandbox.

Eseguibili con: py tests/test_oracles.py   (oppure py -m pytest)
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.oracles import (  # noqa: E402
    build_separating_oracle,
    EXAMPLE_MACHINES,
    OracleMachine,
    language_L_B,
    eval_qbf,
    tqbf_oracle,
    cnf_to_qbf,
    solve_sat_via_oracle,
)
from pnp_lab.oracles.separation import _binary, _first_unqueried  # noqa: E402


# --- separation ------------------------------------------------------------

def test_all_example_machines_defeated():
    result = build_separating_oracle(EXAMPLE_MACHINES)
    assert result.all_machines_defeated
    for stage in result.stages:
        assert stage.machine_accepts != stage.L_B_value


def test_budget_strictly_below_2_to_the_n():
    result = build_separating_oracle(EXAMPLE_MACHINES)
    for stage in result.stages:
        assert stage.budget_at_length < (1 << stage.length)


def test_lengths_are_fresh_and_increasing():
    result = build_separating_oracle(EXAMPLE_MACHINES)
    lengths = [s.length for s in result.stages]
    assert len(lengths) == len(set(lengths)), "ogni stadio usa una lunghezza fresca"
    assert lengths == sorted(lengths)


def test_final_oracle_consistent_with_L_B():
    # Rieseguire ogni macchina sull'oracolo FINALE deve confermare l'errore.
    result = build_separating_oracle(EXAMPLE_MACHINES)
    B = result.B
    by_name = {m.name: m for m in EXAMPLE_MACHINES}
    for stage in result.stages:
        machine = by_name[stage.machine]
        answer = machine.decide(stage.length, lambda s: s in B)
        truth = language_L_B(B, stage.length)
        assert answer != truth, f"{stage.machine}: dovrebbe sbagliare su L_B"


def test_rejecting_machine_forces_addition():
    # Una macchina che rifiuta sempre deve far aggiungere una stringa a B.
    only_reject = [
        OracleMachine(name="always_reject", decide=lambda n, q: False, budget=lambda n: 0)
    ]
    result = build_separating_oracle(only_reject)
    stage = result.stages[0]
    assert stage.added_to_B is not None
    assert stage.L_B_value is True
    assert stage.machine_is_wrong


def test_first_unqueried():
    assert _first_unqueried(set(), 3) == _binary(0, 3) == "000"
    assert _first_unqueried({"000", "001"}, 3) == "010"


# --- collapse (TQBF) -------------------------------------------------------

def test_eval_qbf_basic():
    # ∃x. x  -> vero ;  ∀x. x -> falso
    assert eval_qbf(("exists", "x", ("var", "x"))) is True
    assert eval_qbf(("forall", "x", ("var", "x"))) is False
    # ∀x ∃y. (x = y) codificato come (x∧y) ∨ (¬x∧¬y)
    eq = ("or", ("and", ("var", "x"), ("var", "y")),
          ("and", ("not", ("var", "x")), ("not", ("var", "y"))))
    assert eval_qbf(("forall", "x", ("exists", "y", eq))) is True


def test_tqbf_oracle_is_eval():
    f = ("exists", "x", ("and", ("var", "x"), ("not", ("var", "x"))))
    assert tqbf_oracle(f) is False  # nessun x rende x ∧ ¬x vero


def test_sat_via_oracle_single_query():
    cnf = [[("x1", True), ("x2", True)], [("x1", False), ("x2", True)]]
    r = solve_sat_via_oracle(cnf, ["x1", "x2"])
    assert r.satisfiable is True
    assert r.oracle_queries == 1


def test_unsat_via_oracle():
    cnf = [[("x1", True)], [("x1", False)]]  # x1 ∧ ¬x1
    r = solve_sat_via_oracle(cnf, ["x1"])
    assert r.satisfiable is False
    assert r.oracle_queries == 1


def _brute_force_sat(cnf, variables):
    """Soddisfacibilità per forza bruta: prova tutti i 2^k assegnamenti."""
    from itertools import product

    for combo in product((False, True), repeat=len(variables)):
        assign = dict(zip(variables, combo))
        if all(any(assign[name] == pol for name, pol in clause) for clause in cnf):
            return True
    return False


def test_cnf_to_qbf_matches_bruteforce():
    # La QBF (∃…) deve essere vera se e solo se la CNF è soddisfacibile.
    cases = [
        ([[("a", True), ("b", False)], [("a", False), ("b", True)]], ["a", "b"]),
        ([[("a", True)], [("a", False)]], ["a"]),                      # UNSAT
        ([[("a", True), ("b", True), ("c", True)]], ["a", "b", "c"]),  # SAT
    ]
    for cnf, variables in cases:
        qbf_answer = tqbf_oracle(cnf_to_qbf(cnf, variables))
        assert qbf_answer == _brute_force_sat(cnf, variables)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in fns:
        try:
            fn()
            print(f"  PASS  {fn.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  FAIL  {fn.__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  ERROR {fn.__name__}: {type(e).__name__}: {e}")
    print()
    print(f"  {len(fns) - failed}/{len(fns)} test superati")
    sys.exit(1 if failed else 0)
