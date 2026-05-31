"""Oracle Separation Sandbox — la barriera della relativizzazione.

Baker–Gill–Solovay (1975) dimostrarono che esistono due oracoli:
  - A tale che P^A = NP^A   (le classi collassano)
  - B tale che P^B ≠ NP^B   (le classi si separano)

Conseguenza: qualsiasi tecnica di dimostrazione che *relativizza* (cioè vale
identica rispetto a ogni oracolo) NON può risolvere P vs NP, perché dovrebbe
dare la stessa risposta nei due mondi A e B, che sono in contraddizione. Quasi
tutta la diagonalizzazione classica relativizza: ecco perché da sola non basta.

Questo modulo rende le due costruzioni eseguibili:
  - ``separation``: costruisce B per diagonalizzazione (P^B ≠ NP^B) e lo verifica.
  - ``collapse``: usa un oracolo PSPACE-completo (TQBF) per illustrare P^A = NP^A.
"""

from .separation import (
    OracleMachine,
    SeparationStage,
    SeparationResult,
    language_L_B,
    build_separating_oracle,
    EXAMPLE_MACHINES,
)
from .collapse import (
    eval_qbf,
    tqbf_oracle,
    cnf_to_qbf,
    solve_sat_via_oracle,
    SatResult,
)
from .relativization import relativization_summary

__all__ = [
    "OracleMachine",
    "SeparationStage",
    "SeparationResult",
    "language_L_B",
    "build_separating_oracle",
    "EXAMPLE_MACHINES",
    "eval_qbf",
    "tqbf_oracle",
    "cnf_to_qbf",
    "solve_sat_via_oracle",
    "SatResult",
    "relativization_summary",
]
