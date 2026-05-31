"""Demo del Modulo 2 — Oracle Separation Sandbox.

Uso:
    py examples/run_oracles.py
"""

import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pnp_lab.oracles import (  # noqa: E402
    build_separating_oracle,
    EXAMPLE_MACHINES,
    solve_sat_via_oracle,
    relativization_summary,
)


def main() -> None:
    print()
    print("  P/NP RESEARCH LAB — Modulo 2: Oracle Separation Sandbox")
    print()

    # --- Mondo B: P^B ≠ NP^B ------------------------------------------------
    result = build_separating_oracle(EXAMPLE_MACHINES)
    print(result)
    print()

    # --- Mondo A: P^A = NP^A, illustrato con SAT via oracolo TQBF -----------
    print("=" * 72)
    print("  ORACOLO COLLASSANTE A = TQBF  —  NP^A ⊆ P^A reso concreto su SAT")
    print("=" * 72)

    # Esempio 1: (x1 ∨ x2) ∧ (¬x1 ∨ x2)   → soddisfacibile (x2 = vero)
    cnf_sat = [[("x1", True), ("x2", True)], [("x1", False), ("x2", True)]]
    r1 = solve_sat_via_oracle(cnf_sat, ["x1", "x2"])
    print(f"  (x1 ∨ x2) ∧ (¬x1 ∨ x2):  {r1}")

    # Esempio 2: x1 ∧ ¬x1   → non soddisfacibile
    cnf_unsat = [[("x1", True)], [("x1", False)]]
    r2 = solve_sat_via_oracle(cnf_unsat, ["x1"])
    print(f"  x1 ∧ ¬x1:               {r2}")

    print("  -> Con l'oracolo PSPACE-completo il 'guess' di NP diventa superfluo:")
    print("     SAT è deciso in modo deterministico con UNA query. NP^A ⊆ P^A.")
    print()

    # --- La morale ----------------------------------------------------------
    print(relativization_summary())


if __name__ == "__main__":
    main()
